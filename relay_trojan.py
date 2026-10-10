# relay_trojan.py
#
# Trojan over WebSocket relay.
#
# چرا WebSocket؟ این پنل هیچ‌وقت خودش TLS را terminate نمی‌کند؛ TLS همیشه در لبه‌ی
# Cloudflare (worker.js) بسته می‌شود و فقط ترابردهای WS/gRPC/XHTTP/پلین‌TCP به بک‌اند
# می‌رسند. پس فریم استاندارد Trojan (که معمولاً مستقیم روی TLS می‌نشیند) اینجا داخل
# WebSocket حمل می‌شود — دقیقاً مثل مسیر VLESS-WS.
#
# ساختار درخواست Trojan (RFC عملی Trojan):
#   +-----------------------+-------+----------------+-------+---------+
#   | hex(SHA224(password))  | CRLF  | Trojan Request | CRLF  | Payload |
#   +-----------------------+-------+----------------+-------+---------+
#   |          56 بایت       | 0D0A  |    متغیر        | 0D0A  |  متغیر   |
#
#   Trojan Request:
#   +-----+------+----------+----------+
#   | CMD | ATYP | DST.ADDR | DST.PORT |
#   +-----+------+----------+----------+
#   CMD: 0x01=CONNECT (پشتیبانی‌شده) ، 0x03=UDP ASSOCIATE (پشتیبانی نمی‌شود)
#   ATYP: 0x01=IPv4 ، 0x03=Domain ، 0x04=IPv6

import asyncio
import hashlib
import secrets
from datetime import datetime

from fastapi import WebSocket, WebSocketDisconnect

from speed_limit import throttle

RELAY_BUF = 256 * 1024  # 256 KB

CRLF = b"\r\n"


def _ws_client_ip(ws: WebSocket) -> str:
    from main import extract_client_ip
    host = ws.client.host if ws.client else None
    return extract_client_ip(ws.headers, host)


def trojan_password_hash(password: str) -> str:
    """هش استاندارد Trojan برای یک رمز: hex(SHA224(password))."""
    return hashlib.sha224(password.encode("utf-8")).hexdigest()


def parse_trojan_header(chunk: bytes):
    """پارس اولین پیام Trojan. خروجی: (password_hex, command, address, port, payload)."""
    # 56 بایت هش + CRLF + حداقل (CMD+ATYP+1+2) + CRLF
    if len(chunk) < 60:
        raise ValueError("chunk too small for trojan header")

    password_hex = chunk[0:56].decode("ascii", errors="ignore")
    if chunk[56:58] != CRLF:
        raise ValueError("missing CRLF after password hash")

    pos = 58
    command = chunk[pos]; pos += 1
    atyp = chunk[pos]; pos += 1

    if atyp == 1:  # IPv4
        if len(chunk) < pos + 4:
            raise ValueError("truncated IPv4 address")
        address = ".".join(str(b) for b in chunk[pos:pos + 4]); pos += 4
    elif atyp == 3:  # Domain
        dlen = chunk[pos]; pos += 1
        if len(chunk) < pos + dlen:
            raise ValueError("truncated domain address")
        address = chunk[pos:pos + dlen].decode("utf-8", errors="ignore"); pos += dlen
    elif atyp == 4:  # IPv6
        if len(chunk) < pos + 16:
            raise ValueError("truncated IPv6 address")
        ab = chunk[pos:pos + 16]; pos += 16
        address = ":".join(f"{ab[i]:02x}{ab[i+1]:02x}" for i in range(0, 16, 2))
    else:
        raise ValueError(f"unknown atyp: {atyp}")

    if len(chunk) < pos + 2:
        raise ValueError("truncated port")
    port = int.from_bytes(chunk[pos:pos + 2], "big"); pos += 2

    # CRLF جداکننده‌ی هدر از payload
    if chunk[pos:pos + 2] == CRLF:
        pos += 2
    payload = chunk[pos:]
    return password_hex, command, address, port, payload


async def relay_ws_to_tcp(ws: WebSocket, writer: asyncio.StreamWriter, conn_id: str, uid: str):
    from main import stats, connections, check_and_use
    try:
        while True:
            msg = await ws.receive()
            if msg["type"] == "websocket.disconnect":
                break
            data = msg.get("bytes") or (msg.get("text") or "").encode()
            if not data:
                continue
            if not await check_and_use(uid, len(data)):
                await ws.close(code=1008, reason="quota/disabled/unknown")
                break
            await throttle(uid, len(data))
            stats["total_requests"] += 1
            if conn_id in connections:
                connections[conn_id]["bytes"] += len(data)
            writer.write(data)
            if writer.transport.get_write_buffer_size() > RELAY_BUF:
                await writer.drain()
    except (WebSocketDisconnect, Exception):
        pass
    finally:
        try:
            writer.write_eof()
        except Exception:
            pass


async def relay_tcp_to_ws(ws: WebSocket, reader: asyncio.StreamReader, conn_id: str, uid: str):
    from main import connections, check_and_use
    # Trojan هیچ هدر پاسخی ندارد؛ داده‌ی upstream بدون هیچ پیشوندی برمی‌گردد.
    try:
        while True:
            data = await reader.read(RELAY_BUF)
            if not data:
                break
            if not await check_and_use(uid, len(data)):
                await ws.close(code=1008, reason="quota/disabled/unknown")
                break
            await throttle(uid, len(data))
            if conn_id in connections:
                connections[conn_id]["bytes"] += len(data)
            await ws.send_bytes(data)
    except Exception:
        pass


async def trojan_ws_tunnel(ws: WebSocket, uuid: str):
    from main import (
        is_ip_allowed, logger, log_activity, connections, stats, error_logs,
        save_state, check_and_use, SUBS, check_hwid_from_headers,
    )
    await ws.accept()

    if not await check_and_use(uuid, 0):
        logger.warning(f"🚫 Trojan rejected uuid={uuid[:8]}… (not allowed)")
        await ws.close(code=1008, reason="not authorized")
        return

    ip = _ws_client_ip(ws)

    if not is_ip_allowed(uuid, ip):
        logger.warning(f"🚫 Trojan rejected uuid={uuid[:8]}… ip={ip} (ip limit reached)")
        log_activity("connection", f"اتصال Trojan {ip} با شناسه {uuid[:8]} رد شد (محدودیت تعداد آی‌پی)", "warn")
        await ws.close(code=1008, reason="ip limit reached")
        return

    if not check_hwid_from_headers(uuid, ws.headers, ip):
        logger.warning(f"🚫 Trojan rejected uuid={uuid[:8]}… ip={ip} (hwid limit reached)")
        log_activity("connection", f"اتصال Trojan {ip} با شناسه {uuid[:8]} رد شد (محدودیت تعداد دستگاه)", "warn")
        await ws.close(code=1008, reason="hwid limit reached")
        return

    conn_id = secrets.token_urlsafe(6)
    connections[conn_id] = {
        "uuid": uuid,
        "ip": ip,
        "transport": "trojan-ws",
        "connected_at": datetime.now().isoformat(),
        "bytes": 0,
    }
    logger.info(f"✅ Trojan [{conn_id}] uuid={uuid[:8]}… ip={ip} total={len(connections)}")
    log_activity("connection", f"اتصال جدید Trojan از {ip} با شناسه {uuid[:8]}", "info")
    writer = None

    try:
        first_msg = await asyncio.wait_for(ws.receive(), timeout=15.0)
        if first_msg["type"] == "websocket.disconnect":
            return
        first_chunk = first_msg.get("bytes") or (first_msg.get("text") or "").encode()
        if not first_chunk:
            return

        password_hex, command, address, port, payload = parse_trojan_header(first_chunk)

        # تأیید رمز: رمز Trojan برابر username اشتراک است. اگر اشتراک قابل‌تشخیص بود و
        # هش نخواند، اتصال مثل یک سرور Trojan واقعی قطع می‌شود (مقاومت در برابر پروب).
        sub = SUBS.get(uuid)
        if sub is not None:
            expected = trojan_password_hash(sub.get("username", uuid))
            if password_hex != expected:
                logger.warning(f"🚫 Trojan bad password uuid={uuid[:8]}…")
                await ws.close(code=1008, reason="auth failed")
                return

        # فقط CONNECT پشتیبانی می‌شود (مانند بقیه‌ی ترابردهای TCP این پنل).
        if command != 1:
            await ws.close(code=1003, reason="unsupported command")
            return

        if not await check_and_use(uuid, len(first_chunk)):
            await ws.close(code=1008, reason="quota/disabled")
            return

        stats["total_requests"] += 1
        connections[conn_id]["bytes"] += len(first_chunk)
        logger.info(f"➡️  [{conn_id}] → {address}:{port}")

        reader, writer = await asyncio.wait_for(
            asyncio.open_connection(address, port),
            timeout=10.0
        )
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

        done, pending = await asyncio.wait(
            {
                asyncio.create_task(relay_ws_to_tcp(ws, writer, conn_id, uuid)),
                asyncio.create_task(relay_tcp_to_ws(ws, reader, conn_id, uuid)),
            },
            return_when=asyncio.FIRST_COMPLETED,
        )
        for t in pending:
            t.cancel()
            try:
                await t
            except asyncio.CancelledError:
                pass

        asyncio.create_task(save_state())

    except WebSocketDisconnect:
        pass
    except asyncio.TimeoutError:
        stats["total_errors"] += 1
        error_logs.append({"error": "connection timeout", "time": datetime.now().isoformat()})
    except ValueError as exc:
        stats["total_errors"] += 1
        error_logs.append({"error": f"trojan parse: {exc}", "time": datetime.now().isoformat()})
        logger.error(f"Trojan parse error [{conn_id}]: {exc}")
    except Exception as exc:
        stats["total_errors"] += 1
        error_logs.append({"error": str(exc), "time": datetime.now().isoformat()})
        logger.error(f"Trojan error [{conn_id}]: {exc}")
    finally:
        if writer:
            try:
                writer.close()
                await writer.wait_closed()
            except Exception:
                pass
        connections.pop(conn_id, None)
        logger.info(f"🔌 Trojan closed [{conn_id}] total={len(connections)}")
