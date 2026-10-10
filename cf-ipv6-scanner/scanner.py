#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
cf-ipv6-scanner - Cloudflare IPv6 clean-IP scanner

What it does:
  1) Reads Cloudflare IPv6 ranges from a txt file (default: ranges.txt next to
     this script).
  2) Samples a few RANDOM addresses from each range (the ranges are far too
     large to scan one by one).
  3) Phase 1 - latency screen: performs TCP connects to port 443 and measures
     latency (ICMP ping needs admin rights on Windows; TCP latency is what
     actually matters for a proxy anyway).
  4) Phase 2 - speed test: for the best IPs, measures real download and upload
     speed via speed.cloudflare.com (served from the chosen edge IP itself).
  5) Prints the results in a clean, colored table in the terminal.

Uses only the Python standard library; no external dependencies required.

Examples:
    python scanner.py
    python scanner.py --per-range 60 --top 8 --download-mb 10 --upload-mb 3
    python scanner.py --ranges-file ranges.txt --connect-timeout 2 --concurrency 120
"""

import argparse
import concurrent.futures as cf
import ctypes
import ipaddress
import os
import random
import socket
import ssl
import sys
import time
from dataclasses import dataclass
from pathlib import Path

# -- Constants ------------------------------------------------------------------
SPEED_HOST = "speed.cloudflare.com"   # served from any CF edge -> tests that IP
PING_PORT = 443

# Coloring thresholds (for display only)
PING_GOOD, PING_OK = 150.0, 400.0      # ms
SPEED_GOOD, SPEED_OK = 20.0, 5.0       # Mbps


# -- Terminal colors (ANSI) -----------------------------------------------------
class C:
    RESET = "\033[0m"; BOLD = "\033[1m"; DIM = "\033[2m"
    RED = "\033[31m"; GREEN = "\033[32m"; YELLOW = "\033[33m"
    BLUE = "\033[34m"; MAGENTA = "\033[35m"; CYAN = "\033[36m"; GREY = "\033[90m"
    BG_BLUE = "\033[44m"; WHITE = "\033[97m"


def enable_utf8() -> None:
    """Force UTF-8 console output so box-drawing chars render on Windows."""
    if os.name == "nt":
        try:
            ctypes.windll.kernel32.SetConsoleOutputCP(65001)
            ctypes.windll.kernel32.SetConsoleCP(65001)
        except Exception:
            pass
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass


def enable_ansi() -> bool:
    """Enable ANSI colors on the Windows console (Win10+). No-op elsewhere."""
    if os.name != "nt":
        return True
    try:
        kernel32 = ctypes.windll.kernel32
        handle = kernel32.GetStdHandle(-11)  # STD_OUTPUT_HANDLE
        mode = ctypes.c_uint32()
        if not kernel32.GetConsoleMode(handle, ctypes.byref(mode)):
            return False
        # ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004
        kernel32.SetConsoleMode(handle, mode.value | 0x0004)
        return True
    except Exception:
        return False


USE_COLOR = True


def c(text: str, *codes: str) -> str:
    if not USE_COLOR or not codes:
        return text
    return "".join(codes) + text + C.RESET


# -- Result model ---------------------------------------------------------------
@dataclass
class Result:
    ip: str
    ping_ms: float | None = None       # average TCP latency
    jitter_ms: float | None = None     # latency spread
    loss: float = 1.0                  # fraction of failed attempts (0=best, 1=all failed)
    down_mbps: float | None = None
    up_mbps: float | None = None
    note: str = ""


# -- Loading and sampling ranges ------------------------------------------------
def load_ranges(path: Path) -> list[ipaddress.IPv6Network]:
    nets: list[ipaddress.IPv6Network] = []
    if not path.exists():
        sys.exit(c(f"Ranges file not found: {path}", C.RED, C.BOLD))
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        try:
            net = ipaddress.ip_network(line, strict=False)
        except ValueError:
            print(c(f"Skipped (invalid): {line}", C.YELLOW))
            continue
        if isinstance(net, ipaddress.IPv6Network):
            nets.append(net)
        else:
            print(c(f"Skipped (IPv4, not IPv6): {line}", C.YELLOW))
    if not nets:
        sys.exit(c("No valid IPv6 ranges in the file.", C.RED, C.BOLD))
    return nets


def random_ip_in(net: ipaddress.IPv6Network) -> str:
    """Generate a random address inside an IPv6 range."""
    size = net.num_addresses
    offset = random.randrange(size) if size > 1 else 0
    return str(net.network_address + offset)


def sample_ips(nets: list[ipaddress.IPv6Network], per_range: int) -> list[str]:
    ips: list[str] = []
    seen: set[str] = set()
    for net in nets:
        picked = 0
        attempts = 0
        # Cap attempts to avoid looping forever on very small ranges
        while picked < per_range and attempts < per_range * 5:
            attempts += 1
            ip = random_ip_in(net)
            if ip in seen:
                continue
            seen.add(ip)
            ips.append(ip)
            picked += 1
    random.shuffle(ips)
    return ips


# -- Phase 1: TCP latency test --------------------------------------------------
def tcp_ping(ip: str, timeout: float, tries: int = 3) -> tuple[float | None, float | None, float]:
    """Connect to port 443 a few times; return (avg ms, jitter ms, loss ratio)."""
    samples: list[float] = []
    fails = 0
    for _ in range(tries):
        start = time.perf_counter()
        s = None
        try:
            s = socket.create_connection((ip, PING_PORT), timeout=timeout)
            samples.append((time.perf_counter() - start) * 1000.0)
        except Exception:
            fails += 1
        finally:
            if s is not None:
                try:
                    s.close()
                except Exception:
                    pass
    loss = fails / tries
    if not samples:
        return None, None, loss
    avg = sum(samples) / len(samples)
    jitter = (max(samples) - min(samples)) if len(samples) > 1 else 0.0
    return avg, jitter, loss


# -- Phase 2: speed test (download/upload) pinned to a specific IP --------------
def _open_tls(ip: str, timeout: float) -> ssl.SSLSocket:
    raw = socket.create_connection((ip, 443), timeout=timeout)
    ctx = ssl.create_default_context()
    # Certificate is validated against the real hostname, but the socket is
    # connected to the IP we chose.
    return ctx.wrap_socket(raw, server_hostname=SPEED_HOST)


def http_download(ip: str, nbytes: int, timeout: float) -> float | None:
    """Measure download speed (Mbps) by fetching nbytes from __down."""
    try:
        s = _open_tls(ip, timeout)
    except Exception:
        return None
    try:
        s.settimeout(timeout)
        req = (
            f"GET /__down?bytes={nbytes} HTTP/1.1\r\n"
            f"Host: {SPEED_HOST}\r\n"
            f"User-Agent: cf-ipv6-scanner\r\n"
            f"Accept: */*\r\n"
            f"Connection: close\r\n\r\n"
        )
        s.sendall(req.encode())
        total = 0
        start = None
        while True:
            chunk = s.recv(65536)
            if not chunk:
                break
            if start is None:
                start = time.perf_counter()
            total += len(chunk)
        end = time.perf_counter()
        if start is None or end <= start or total <= 0:
            return None
        return total * 8 / (end - start) / 1e6
    except Exception:
        return None
    finally:
        try:
            s.close()
        except Exception:
            pass


def http_upload(ip: str, nbytes: int, timeout: float) -> float | None:
    """Measure upload speed (Mbps) by sending nbytes to __up."""
    try:
        s = _open_tls(ip, timeout)
    except Exception:
        return None
    try:
        s.settimeout(timeout)
        head = (
            f"POST /__up HTTP/1.1\r\n"
            f"Host: {SPEED_HOST}\r\n"
            f"User-Agent: cf-ipv6-scanner\r\n"
            f"Content-Type: application/octet-stream\r\n"
            f"Content-Length: {nbytes}\r\n"
            f"Connection: close\r\n\r\n"
        )
        s.sendall(head.encode())
        payload = b"\x00" * 65536
        remaining = nbytes
        start = time.perf_counter()
        while remaining > 0:
            block = payload if remaining >= len(payload) else payload[:remaining]
            s.sendall(block)
            remaining -= len(block)
        try:
            s.recv(4096)  # make sure the server accepted the whole body
        except Exception:
            pass
        end = time.perf_counter()
        if end <= start:
            return None
        return nbytes * 8 / (end - start) / 1e6
    except Exception:
        return None
    finally:
        try:
            s.close()
        except Exception:
            pass


# -- Display --------------------------------------------------------------------
def banner() -> None:
    line = "=" * 58
    print(c(line, C.CYAN))
    print(c("  cf-ipv6-scanner  ", C.BOLD, C.WHITE, C.BG_BLUE) +
          c("  Cloudflare IPv6 clean-IP scanner", C.CYAN, C.BOLD))
    print(c(line, C.CYAN))


def progress(done: int, total: int, found: int, label: str) -> None:
    width = 32
    frac = done / total if total else 1.0
    filled = int(frac * width)
    bar = "#" * filled + "-" * (width - filled)
    msg = (f"\r{c(label, C.CYAN)} {c(bar, C.GREEN)} "
           f"{done:>5}/{total:<5} ({frac*100:5.1f}%)  "
           f"{c('alive:', C.GREY)} {c(str(found), C.GREEN, C.BOLD)}  ")
    sys.stdout.write(msg)
    sys.stdout.flush()
    if done >= total:
        sys.stdout.write("\n")


def ping_color(v: float | None) -> str:
    if v is None:
        return c("-", C.RED)
    if v <= PING_GOOD:
        return c(f"{v:6.1f}", C.GREEN)
    if v <= PING_OK:
        return c(f"{v:6.1f}", C.YELLOW)
    return c(f"{v:6.1f}", C.RED)


def speed_color(v: float | None) -> str:
    if v is None:
        return c("-", C.RED)
    if v >= SPEED_GOOD:
        return c(f"{v:7.2f}", C.GREEN)
    if v >= SPEED_OK:
        return c(f"{v:7.2f}", C.YELLOW)
    return c(f"{v:7.2f}", C.RED)


def _vlen(s: str) -> int:
    """Visible length of a string, ignoring ANSI color codes."""
    out = 0
    i = 0
    while i < len(s):
        if s[i] == "\033":
            j = s.find("m", i)
            if j != -1:
                i = j + 1
                continue
        out += 1
        i += 1
    return out


def _pad(s: str, width: int, align: str = "left") -> str:
    gap = width - _vlen(s)
    if gap <= 0:
        return s
    if align == "right":
        return " " * gap + s
    if align == "center":
        left = gap // 2
        return " " * left + s + " " * (gap - left)
    return s + " " * gap


def render_table(results: list[Result]) -> None:
    headers = ["#", "IPv6 Address", "Ping(ms)", "Jitter", "Loss", "Down(Mbps)", "Up(Mbps)"]
    rows: list[list[str]] = []
    for i, r in enumerate(results, 1):
        rows.append([
            str(i),
            r.ip,
            ping_color(r.ping_ms),
            (c(f"{r.jitter_ms:.1f}", C.GREY) if r.jitter_ms is not None else c("-", C.RED)),
            (c(f"{int(r.loss*100)}%", C.GREEN if r.loss == 0 else C.YELLOW)),
            speed_color(r.down_mbps),
            speed_color(r.up_mbps),
        ])

    widths = [_vlen(h) for h in headers]
    for row in rows:
        for idx, cell in enumerate(row):
            widths[idx] = max(widths[idx], _vlen(cell))

    def sep(left: str, mid: str, right: str) -> str:
        return left + mid.join("─" * (w + 2) for w in widths) + right

    aligns = ["right", "left", "right", "right", "right", "right", "right"]

    print(c(sep("┌", "┬", "┐"), C.GREY))
    header_line = "│" + "│".join(
        " " + _pad(c(h, C.BOLD, C.CYAN), widths[i], "center") + " " for i, h in enumerate(headers)
    ) + "│"
    print(header_line)
    print(c(sep("├", "┼", "┤"), C.GREY))
    for row in rows:
        line = "│" + "│".join(
            " " + _pad(cell, widths[i], aligns[i]) + " " for i, cell in enumerate(row)
        ) + "│"
        print(line)
    print(c(sep("└", "┴", "┘"), C.GREY))


# -- IPv6 availability check ----------------------------------------------------
def has_ipv6() -> bool:
    probes = ["2606:4700:4700::1111", "2606:4700:4700::1001"]
    for ip in probes:
        s = None
        try:
            s = socket.create_connection((ip, 443), timeout=4)
            return True
        except Exception:
            continue
        finally:
            if s is not None:
                try:
                    s.close()
                except Exception:
                    pass
    return False


# -- Main -----------------------------------------------------------------------
def parse_args() -> argparse.Namespace:
    here = Path(__file__).resolve().parent
    p = argparse.ArgumentParser(
        description="Cloudflare IPv6 clean-IP scanner (download/upload/ping)",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    p.add_argument("--ranges-file", type=Path, default=here / "ranges.txt",
                   help="File with IPv6 ranges (CIDR, one per line)")
    p.add_argument("--per-range", type=int, default=50,
                   help="Number of random addresses sampled from each range")
    p.add_argument("--concurrency", type=int, default=100,
                   help="Number of concurrent connections in the ping screen")
    p.add_argument("--connect-timeout", type=float, default=2.0,
                   help="Timeout for each TCP connect in the ping phase (seconds)")
    p.add_argument("--ping-tries", type=int, default=3,
                   help="Number of ping attempts per IP")
    p.add_argument("--max-loss", type=float, default=0.5,
                   help="Drop IPs whose loss ratio exceeds this (0 to 1)")
    p.add_argument("--top", type=int, default=8,
                   help="How many best-ping IPs go into the speed test")
    p.add_argument("--download-mb", type=float, default=10.0,
                   help="Download test size (megabytes)")
    p.add_argument("--upload-mb", type=float, default=3.0,
                   help="Upload test size (megabytes)")
    p.add_argument("--speed-timeout", type=float, default=20.0,
                   help="Timeout for each speed test (seconds)")
    p.add_argument("--no-color", action="store_true", help="Disable colors")
    p.add_argument("--no-ipv6-check", action="store_true",
                   help="Skip the initial IPv6 availability check")
    return p.parse_args()


def main() -> None:
    global USE_COLOR
    enable_utf8()
    args = parse_args()
    USE_COLOR = (not args.no_color) and enable_ansi()

    banner()

    if not args.no_ipv6_check:
        print(c("* Checking this machine's IPv6 connectivity...", C.CYAN))
        if not has_ipv6():
            print(c("  x This connection appears to have no IPv6, or Cloudflare "
                    "IPv6 is blocked.", C.RED, C.BOLD))
            print(c("    If you are sure you have IPv6, re-run with --no-ipv6-check.",
                    C.YELLOW))
            return
        print(c("  + IPv6 is available.", C.GREEN))

    nets = load_ranges(args.ranges_file)
    print(c(f"* Loaded {len(nets)} ranges from {args.ranges_file.name}.", C.CYAN))

    candidates = sample_ips(nets, args.per_range)
    print(c(f"* Sampled {len(candidates)} random addresses for screening "
            f"({args.per_range} per range).", C.CYAN))
    print()

    # -- Phase 1: ping screen --
    print(c("Phase 1 - TCP latency screen on port 443:", C.BOLD, C.MAGENTA))
    alive: list[Result] = []
    total = len(candidates)
    done = 0
    with cf.ThreadPoolExecutor(max_workers=args.concurrency) as ex:
        futs = {
            ex.submit(tcp_ping, ip, args.connect_timeout, args.ping_tries): ip
            for ip in candidates
        }
        for fut in cf.as_completed(futs):
            ip = futs[fut]
            done += 1
            try:
                avg, jitter, loss = fut.result()
            except Exception:
                avg, jitter, loss = None, None, 1.0
            if avg is not None and loss <= args.max_loss:
                alive.append(Result(ip=ip, ping_ms=avg, jitter_ms=jitter, loss=loss))
            progress(done, total, len(alive), "  screen")

    if not alive:
        print(c("\nNo healthy IP found. "
                "Increase --per-range or check your connection/firewall.",
                C.RED, C.BOLD))
        return

    alive.sort(key=lambda r: (r.ping_ms if r.ping_ms is not None else 9e9))
    top = alive[:args.top]
    print(c(f"* {len(alive)} healthy IPs; top {len(top)} go into the speed test.",
            C.CYAN))
    print()

    # -- Phase 2: speed test --
    print(c("Phase 2 - download/upload speed test (sequential, for accuracy):",
            C.BOLD, C.MAGENTA))
    down_bytes = int(args.download_mb * 1024 * 1024)
    up_bytes = int(args.upload_mb * 1024 * 1024)
    for idx, r in enumerate(top, 1):
        sys.stdout.write(c(f"\r  [{idx}/{len(top)}] {r.ip} ... download", C.CYAN) + " " * 20)
        sys.stdout.flush()
        r.down_mbps = http_download(r.ip, down_bytes, args.speed_timeout)
        sys.stdout.write(c(f"\r  [{idx}/{len(top)}] {r.ip} ... upload  ", C.CYAN) + " " * 20)
        sys.stdout.flush()
        r.up_mbps = http_upload(r.ip, up_bytes, args.speed_timeout)
    sys.stdout.write("\r" + " " * 70 + "\r")
    sys.stdout.flush()

    # Final ordering: higher download first, then lower ping
    top.sort(key=lambda r: (-(r.down_mbps or 0.0), r.ping_ms or 9e9))

    print()
    print(c("Final results (sorted by download speed):", C.BOLD, C.GREEN))
    render_table(top)

    best = top[0]
    print()
    print(c("* Best Clean IP suggestion:", C.BOLD, C.YELLOW))
    print("  " + c(best.ip, C.BOLD, C.GREEN) +
          c(f"   (ping {best.ping_ms:.0f}ms"
            f" | down {(best.down_mbps or 0):.1f}"
            f" | up {(best.up_mbps or 0):.1f} Mbps)", C.GREY))
    print(c("  Put this value in the config's Clean IP field (in the panel).", C.CYAN))
    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(c("\nAborted.", C.YELLOW))
