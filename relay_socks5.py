# relay_socks5.py
import asyncio
import secrets
from datetime import datetime
from fastapi import WebSocket, WebSocketDisconnect
from speed_limit import throttle

RELAY_BUF = 256 * 1024  # 256 KB

def _ws_client_ip(ws: WebSocket) -> str:
    from main import extract_client_ip
    host = ws.client.host if ws.client else None
    return extract_client_ip(ws.headers, host)

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
            connections[conn_id]["bytes"] += len(data)
            writer.write(data)
            if writer.transport.get_write_buffer_size() > RELAY_BUF:
                await writer.drain()
    except Exception:
        pass
    finally:
        try:
            writer.write_eof()
        except Exception:
            pass

async def relay_tcp_to_ws(ws: WebSocket, reader: asyncio.StreamReader, conn_id: str, uid: str):
    from main import connections, check_and_use
    try:
        while True:
            data = await reader.read(RELAY_BUF)
            if not data:
                break
            if not await check_and_use(uid, len(data)):
                await ws.close(code=1008, reason="quota/disabled/unknown")
                break
            await throttle(uid, len(data))
            connections[conn_id]["bytes"] += len(data)
            await ws.send_bytes(data)
    except Exception:
        pass

async def handle_socks5_ws(ws: WebSocket, uid: str):
    from main import is_ip_allowed, connections, stats, error_logs, logger, log_activity, check_and_use
    await ws.accept()

    if not await check_and_use(uid, 0):
        await ws.close(code=1008, reason="Unauthorized/Expired/Disabled")
        return

    conn_id = secrets.token_hex(8)
    client_ip = _ws_client_ip(ws)
    connections[conn_id] = {
        "uuid": uid,
        "ip": client_ip,
        "connected_at": datetime.now().isoformat(),
        "last_connected_at": datetime.now().isoformat(),
        "bytes": 0,
        "type": "SOCKS5-WS",
        "transport": "socks5-ws",
    }

    try:
        # SOCKS5 Handshake - Greeting
        msg1 = await ws.receive()
        b1 = msg1.get("bytes") or (msg1.get("text") or "").encode()
        if not b1 or b1[0] != 0x05:
            await ws.close(code=1003, reason="Not SOCKS5")
            return
        
        # Respond No Auth required
        await ws.send_bytes(b"\x05\x00")

        # SOCKS5 Request
        msg2 = await ws.receive()
        b2 = msg2.get("bytes") or (msg2.get("text") or "").encode()
        if len(b2) < 7 or b2[0] != 0x05 or b2[1] != 0x01: # 0x01 = CONNECT
            await ws.close(code=1003, reason="Unsupported SOCKS5 cmd")
            return

        atyp = b2[3]
        pos = 4
        if atyp == 1: # IPv4
            target_host = ".".join(str(x) for x in b2[pos:pos+4])
            pos += 4
        elif atyp == 3: # Domain
            dlen = b2[pos]
            pos += 1
            target_host = b2[pos:pos+dlen].decode("utf-8", errors="ignore")
            pos += dlen
        elif atyp == 4: # IPv6
            ab = b2[pos:pos+16]
            pos += 16
            target_host = ":".join(f"{ab[i]:02x}{ab[i+1]:02x}" for i in range(0, 16, 2))
        else:
            await ws.close(code=1003, reason="Bad ATYP")
            return

        if not is_ip_allowed(uid, client_ip):
            logger.warning(f"🚫 SOCKS5 rejected uuid={uid[:8]}… ip={client_ip} (ip limit reached)")
            log_activity("connection", f"اتصال SOCKS5 {client_ip} با شناسه {uid[:8]} رد شد (محدودیت آی‌پی)", "warn")
            await ws.close(code=1008, reason="IP Limit")
            return

        target_port = int.from_bytes(b2[pos:pos+2], "big")
        initial_data = b2[pos+2:]

        # Connect to destination
        try:
            log_activity("connection", f"اتصال جدید SOCKS5 از {client_ip} با شناسه {uid[:8]}", "info")
            reader, writer = await asyncio.wait_for(
                asyncio.open_connection(target_host, target_port), timeout=10.0
            )
        except Exception as e:
            # SOCKS5 error response
            await ws.send_bytes(b"\x05\x05\x00\x01\x00\x00\x00\x00\x00\x00")
            await ws.close()
            error_logs.append({"time": datetime.now().isoformat(), "msg": f"SOCKS5 dial {target_host}:{target_port} error: {e}"})
            return

        # SOCKS5 Success response
        await ws.send_bytes(b"\x05\x00\x00\x01\x00\x00\x00\x00\x00\x00")

        if initial_data:
            writer.write(initial_data)
            await writer.drain()

        # Run relay
        t1 = asyncio.create_task(relay_ws_to_tcp(ws, writer, conn_id, uid))
        t2 = asyncio.create_task(relay_tcp_to_ws(ws, reader, conn_id, uid))
        done, pending = await asyncio.wait([t1, t2], return_when=asyncio.FIRST_COMPLETED)
        for p in pending:
            p.cancel()

        try:
            writer.close()
            await writer.wait_closed()
        except Exception:
            pass

    except Exception as e:
        error_logs.append({"time": datetime.now().isoformat(), "msg": f"SOCKS5 WS error: {e}"})
    finally:
        connections.pop(conn_id, None)
        from main import save_state
        asyncio.create_task(save_state())


async def relay_tcp_to_tcp(reader: asyncio.StreamReader, writer: asyncio.StreamWriter, conn_id: str, uid: str):
    from main import connections, check_and_use
    from speed_limit import throttle
    try:
        while True:
            data = await reader.read(RELAY_BUF)
            if not data:
                break
            if not await check_and_use(uid, len(data)):
                break
            await throttle(uid, len(data))
            if conn_id in connections:
                connections[conn_id]["bytes"] += len(data)
            writer.write(data)
            await writer.drain()
    except Exception:
        pass
    finally:
        try:
            writer.write_eof()
        except Exception:
            pass

async def handle_socks5_tcp(client_reader: asyncio.StreamReader, client_writer: asyncio.StreamWriter):
    from main import is_ip_allowed, connections, error_logs, logger, log_activity, check_and_use
    conn_id = secrets.token_hex(8)
    try:
        client_ip = client_writer.get_extra_info('peername')[0]
    except Exception:
        client_ip = "unknown"
    uid = None
    
    try:
        # 1. Greeting
        b1 = await client_reader.readexactly(2)
        if b1[0] != 0x05:
            return
        nmethods = b1[1]
        methods = await client_reader.readexactly(nmethods)
        
        # Require Username/Password auth (0x02)
        if 0x02 not in methods:
            client_writer.write(b"\x05\xFF") # No acceptable methods
            await client_writer.drain()
            return
        
        client_writer.write(b"\x05\x02")
        await client_writer.drain()
        
        # 2. Auth Request
        auth_ver = await client_reader.readexactly(1)
        if auth_ver[0] != 0x01:
            return
        
        ulen = (await client_reader.readexactly(1))[0]
        uname = (await client_reader.readexactly(ulen)).decode('utf-8', 'ignore') if ulen > 0 else ""
        
        plen = (await client_reader.readexactly(1))[0]
        passwd = (await client_reader.readexactly(plen)).decode('utf-8', 'ignore') if plen > 0 else ""
        
        # We can accept UUID or username in either username or password.
        auth_str = uname if uname else passwd
        
        from main import SUBS
        found_uid = None
        for s_id, s_data in SUBS.items():
            if s_id == auth_str or s_data.get("username") == auth_str:
                found_uid = s_id
                break
                
        if not found_uid:
            client_writer.write(b"\x01\x01") # Auth failed
            await client_writer.drain()
            return
            
        uid = found_uid
        
        if not await check_and_use(uid, 0):
            client_writer.write(b"\x01\x01") # Auth failed
            await client_writer.drain()
            return
        
        client_writer.write(b"\x01\x00") # Auth success
        await client_writer.drain()
        
        # 3. Request
        req = await client_reader.readexactly(4)
        if req[0] != 0x05 or req[1] != 0x01: # Only CONNECT supported
            client_writer.write(b"\x05\x07\x00\x01\x00\x00\x00\x00\x00\x00")
            await client_writer.drain()
            return
        
        atyp = req[3]
        if atyp == 1:
            addr_b = await client_reader.readexactly(4)
            target_host = ".".join(str(x) for x in addr_b)
        elif atyp == 3:
            dlen = (await client_reader.readexactly(1))[0]
            addr_b = await client_reader.readexactly(dlen)
            target_host = addr_b.decode('utf-8', 'ignore')
        elif atyp == 4:
            addr_b = await client_reader.readexactly(16)
            target_host = ":".join(f"{addr_b[i]:02x}{addr_b[i+1]:02x}" for i in range(0, 16, 2))
        else:
            return
        
        port_b = await client_reader.readexactly(2)
        target_port = int.from_bytes(port_b, 'big')
        
        if not is_ip_allowed(uid, client_ip):
            logger.warning(f"🚫 SOCKS5 TCP rejected uuid={uid[:8]}… ip={client_ip}")
            log_activity("connection", f"اتصال SOCKS5-TCP {client_ip} رد شد (محدودیت آی‌پی)", "warn")
            client_writer.write(b"\x05\x02\x00\x01\x00\x00\x00\x00\x00\x00")
            await client_writer.drain()
            return
        
        connections[conn_id] = {
            "uuid": uid,
            "ip": client_ip,
            "connected_at": datetime.now().isoformat(),
            "last_connected_at": datetime.now().isoformat(),
            "bytes": 0,
            "type": "SOCKS5-TCP",
            "transport": "socks5-tcp",
        }
        
        try:
            log_activity("connection", f"اتصال جدید SOCKS5-TCP از {client_ip}", "info")
            remote_reader, remote_writer = await asyncio.wait_for(
                asyncio.open_connection(target_host, target_port), timeout=10.0
            )
        except Exception as e:
            client_writer.write(b"\x05\x05\x00\x01\x00\x00\x00\x00\x00\x00")
            await client_writer.drain()
            return
            
        # Success response
        client_writer.write(b"\x05\x00\x00\x01\x00\x00\x00\x00\x00\x00")
        await client_writer.drain()
        
        # Relay
        t1 = asyncio.create_task(relay_tcp_to_tcp(client_reader, remote_writer, conn_id, uid))
        t2 = asyncio.create_task(relay_tcp_to_tcp(remote_reader, client_writer, conn_id, uid))
        
        done, pending = await asyncio.wait([t1, t2], return_when=asyncio.FIRST_COMPLETED)
        for p in pending:
            p.cancel()
            
        try:
            remote_writer.close()
            await remote_writer.wait_closed()
        except Exception: pass

    except Exception as e:
        error_logs.append({"time": datetime.now().isoformat(), "msg": f"SOCKS5 TCP error: {e}"})
    finally:
        connections.pop(conn_id, None)
        from main import save_state
        asyncio.create_task(save_state())
        try:
            client_writer.close()
            await client_writer.wait_closed()
        except Exception: pass

async def start_socks5_tcp_server():
    from main import SETTINGS, logger
    import os
    port = int(os.environ.get("SOCKS5_PORT") or SETTINGS.get("socks5_port", 1081))
    try:
        server = await asyncio.start_server(handle_socks5_tcp, '0.0.0.0', port)
        logger.info(f"SOCKS5 TCP server listening on 0.0.0.0:{port}")
        async with server:
            await server.serve_forever()
    except Exception as e:
        logger.error(f"Failed to start SOCKS5 TCP server on port {port}: {e}")
