import asyncio
import struct
import secrets
import uuid
from datetime import datetime
from fastapi import Request, HTTPException
from fastapi.responses import StreamingResponse

from speed_limit import throttle
from relay_vless import parse_vless_header

RELAY_BUF = 256 * 1024

def _grpc_client_ip(request: Request) -> str:
    from main import extract_client_ip
    host = request.client.host if request.client else None
    return extract_client_ip(request.headers, host)

def encode_varint(n: int) -> bytes:
    res = bytearray()
    while True:
        towrite = n & 0x7F
        n >>= 7
        if n:
            res.append(towrite | 0x80)
        else:
            res.append(towrite)
            break
    return bytes(res)

def decode_varint(buffer: bytes, offset: int = 0) -> tuple[int, int]:
    res = 0
    shift = 0
    idx = offset
    while idx < len(buffer):
        b = buffer[idx]
        res |= (b & 0x7F) << shift
        idx += 1
        if not (b & 0x80):
            break
        shift += 7
    return res, idx

def extract_vless_payload(payload: bytes) -> bytes:
    """پارس پیام‌های Protobuf استریم gRPC در Xray/v2ray (تگ 0x0a + Length Varint)"""
    if payload.startswith(b"\x0a"):
        try:
            length, start = decode_varint(payload, 1)
            if len(payload) >= start + length:
                return payload[start:start+length]
            return payload[start:]
        except Exception:
            return payload
    return payload

async def unwrap_grpc_frames(request: Request):
    buffer = b""
    async for chunk in request.stream():
        buffer += chunk
        while len(buffer) >= 5:
            compressed, length = struct.unpack(">B I", buffer[:5])
            if len(buffer) < 5 + length:
                break
            payload = buffer[5:5+length]
            buffer = buffer[5+length:]
            yield extract_vless_payload(payload)

def wrap_grpc_frame(payload: bytes) -> bytes:
    """بسته‌بندی پاسخ‌های TCP در فریم gRPC استاندارد همراه با تگ Protobuf 0x0a"""
    pb_msg = b"\x0a" + encode_varint(len(payload)) + payload
    return struct.pack(">B I", 0, len(pb_msg)) + pb_msg

async def grpc_tunnel(request: Request):
    from main import (
        LINKS_LOCK, check_and_use, is_ip_allowed, get_speed_limit,
        stats, error_logs, connections, logger, save_state, log_activity,
        check_hwid_from_headers,
    )

    ip = _grpc_client_ip(request)
    
    frame_gen = unwrap_grpc_frames(request)
    try:
        first_chunk = await frame_gen.__anext__()
    except StopAsyncIteration:
        raise HTTPException(status_code=400, detail="Empty request")
    except Exception as e:
        logger.error(f"gRPC read error: {e}")
        raise HTTPException(status_code=400, detail="Stream error")
    
    if not first_chunk or len(first_chunk) < 24:
        raise HTTPException(status_code=400, detail="Invalid VLESS header")
    
    try:
        command, address, port, payload = await parse_vless_header(first_chunk)
    except ValueError as e:
        logger.error(f"VLESS parse error: {e}")
        raise HTTPException(status_code=400, detail="Invalid VLESS format")
    
    import uuid
    try:
        uid = str(uuid.UUID(bytes=first_chunk[1:17]))
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid UUID")

    if not await check_and_use(uid, 0):
        logger.warning(f"🚫 gRPC rejected uuid={uid[:8]}… (not allowed)")
        raise HTTPException(status_code=403, detail="not authorized")

    if not is_ip_allowed(uid, ip):
        logger.warning(f"🚫 gRPC rejected uuid={uid[:8]}… ip={ip} (ip limit reached)")
        log_activity("connection", f"اتصال gRPC {ip} با شناسه {uid[:8]} رد شد (محدودیت تعداد آی‌پی)", "warn")
        raise HTTPException(status_code=403, detail="ip limit reached")

    if not check_hwid_from_headers(uid, request.headers, ip):
        logger.warning(f"🚫 gRPC rejected uuid={uid[:8]}… ip={ip} (hwid limit reached)")
        log_activity("connection", f"اتصال gRPC {ip} با شناسه {uid[:8]} رد شد (محدودیت تعداد دستگاه)", "warn")
        raise HTTPException(status_code=403, detail="hwid limit reached")

    if not await check_and_use(uid, len(first_chunk)):
        raise HTTPException(status_code=403, detail="quota/disabled")

    conn_id = secrets.token_urlsafe(6)
    connections[conn_id] = {
        "uuid": uid,
        "ip": ip,
        "transport": "vless-grpc",
        "connected_at": datetime.now().isoformat(),
        "bytes": len(first_chunk),
    }
    logger.info(f"✅ gRPC [{conn_id}] uuid={uid[:8]}… ip={ip} total={len(connections)}")
    log_activity("connection", f"اتصال جدید gRPC از {ip} با شناسه {uid[:8]}", "info")

    stats["total_requests"] += 1
    logger.info(f"➡️  [{conn_id}] → {address}:{port}")

    try:
        reader, writer = await asyncio.wait_for(
            asyncio.open_connection(address, port),
            timeout=10.0
        )
    except Exception as exc:
        stats["total_errors"] += 1
        error_logs.append({"error": str(exc), "time": datetime.now().isoformat()})
        connections.pop(conn_id, None)
        raise HTTPException(status_code=502, detail="upstream connection error")

    sock = writer.transport.get_extra_info('socket')
    if sock:
        import socket
        try:
            sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        except Exception:
            pass

    if payload:
        writer.write(payload)
        await writer.drain()

    async def client_to_upstream():
        try:
            async for chunk in frame_gen:
                if not chunk:
                    continue
                if not await check_and_use(uid, len(chunk)):
                    break
                await throttle(uid, len(chunk))
                connections[conn_id]["bytes"] += len(chunk)
                writer.write(chunk)
                if writer.transport.get_write_buffer_size() > RELAY_BUF:
                    await writer.drain()
        except Exception:
            pass
        finally:
            try:
                writer.write_eof()
            except Exception:
                pass

    ctou_task = asyncio.create_task(client_to_upstream())

    async def upstream_to_client():
        first = True
        try:
            while True:
                data = await reader.read(RELAY_BUF)
                if not data:
                    break
                if not await check_and_use(uid, len(data)):
                    break
                await throttle(uid, len(data))
                connections[conn_id]["bytes"] += len(data)
                
                payload_out = (b"\x00\x00" + data) if first else data
                first = False
                yield wrap_grpc_frame(payload_out)
        except Exception:
            pass
        finally:
            ctou_task.cancel()
            try:
                writer.close()
                await writer.wait_closed()
            except Exception:
                pass
            connections.pop(conn_id, None)
            logger.info(f"🔌 gRPC closed [{conn_id}] total={len(connections)}")
            asyncio.create_task(save_state())

    return StreamingResponse(upstream_to_client(), media_type="application/grpc")
