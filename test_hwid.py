"""
Functional test for the HWID device-limit system.

Runs the real enforcement logic from main.py (is_hwid_allowed / extract_hwid /
check_hwid_from_headers) against an in-memory subscription, asserting that:
  * distinct devices are registered up to the limit,
  * the (limit+1)-th NEW device is rejected,
  * already-registered devices keep connecting,
  * resetting hwids frees the slots,
  * SOCKS5-style connections (no User-Agent) are exempt,
  * an explicit X-HWID header takes priority over User-Agent.

Run:  python test_hwid.py
"""
import sys
import main


class FakeHeaders:
    """Minimal case-insensitive headers mapping, like Starlette's Headers."""
    def __init__(self, data: dict):
        self._d = {k.lower(): v for k, v in data.items()}

    def get(self, name, default=None):
        return self._d.get(name.lower(), default)

    def items(self):
        return self._d.items()


def ua(agent: str) -> FakeHeaders:
    return FakeHeaders({"user-agent": agent})


PASS = 0
FAIL = 0


def check(name: str, cond: bool):
    global PASS, FAIL
    if cond:
        PASS += 1
        print(f"  [PASS] {name}")
    else:
        FAIL += 1
        print(f"  [FAIL] {name}")


def setup_sub(limit: int) -> str:
    sid = "test-sub-" + main.generate_uuid()
    main.SUBS[sid] = {
        "label": "HWID test",
        "username": "tester",
        "active": True,
        "limit_bytes": 0,
        "used_bytes": 0,
        "ip_limit": 0,
        "hwid_limit": limit,
        "hwids": {},
        "links": [],
    }
    return sid


def main_test():
    print("HWID system test")
    print("-" * 50)

    # ── Scenario 1: limit = 3, four distinct devices ──
    print("Scenario 1: hwid_limit = 3, four different devices")
    sid = setup_sub(3)
    d1 = main.check_hwid_from_headers(sid, ua("v2rayNG/1.8.5"), ip="2001:db8::1")
    d2 = main.check_hwid_from_headers(sid, ua("Hiddify/2.0.0"), ip="2001:db8::2")
    d3 = main.check_hwid_from_headers(sid, ua("sing-box/1.9"), ip="2001:db8::3")
    d4 = main.check_hwid_from_headers(sid, ua("Streisand/1.2"), ip="2001:db8::4")
    check("1st device allowed", d1 is True)
    check("2nd device allowed", d2 is True)
    check("3rd device allowed", d3 is True)
    check("4th NEW device REJECTED (limit reached)", d4 is False)
    check("exactly 3 devices registered", len(main.SUBS[sid]["hwids"]) == 3)

    # already-registered device reconnects -> still allowed, no new slot
    again = main.check_hwid_from_headers(sid, ua("v2rayNG/1.8.5"), ip="2001:db8::9")
    check("already-registered device still allowed", again is True)
    check("still exactly 3 devices (no new slot)", len(main.SUBS[sid]["hwids"]) == 3)

    # ── Scenario 2: reset frees the slots ──
    print("Scenario 2: reset_hwids frees the slots")
    main.SUBS[sid]["hwids"] = {}
    d_new = main.check_hwid_from_headers(sid, ua("Streisand/1.2"), ip="2001:db8::4")
    check("after reset, previously-rejected device is allowed", d_new is True)

    # ── Scenario 3: unlimited (limit = 0) ──
    print("Scenario 3: hwid_limit = 0 (unlimited)")
    sid0 = setup_sub(0)
    results = [
        main.check_hwid_from_headers(sid0, ua(f"client-{i}"), ip=f"2001:db8::{i}")
        for i in range(10)
    ]
    check("all 10 devices allowed when unlimited", all(results))
    check("all 10 recorded for visibility", len(main.SUBS[sid0]["hwids"]) == 10)

    # ── Scenario 4: SOCKS5-style (no User-Agent) is exempt ──
    print("Scenario 4: no User-Agent (SOCKS5-style) is exempt")
    sid_s = setup_sub(1)
    # register one real device to fill the limit
    main.check_hwid_from_headers(sid_s, ua("only-device"), ip="2001:db8::1")
    noua = main.check_hwid_from_headers(sid_s, FakeHeaders({}), ip="2001:db8::2")
    check("connection without identifiable HWID is allowed", noua is True)
    check("no-UA connection did not consume a slot", len(main.SUBS[sid_s]["hwids"]) == 1)

    # ── Scenario 5: explicit X-HWID beats User-Agent ──
    print("Scenario 5: explicit X-HWID header")
    h1 = FakeHeaders({"user-agent": "same-ua", "x-hwid": "DEVICE-AAA"})
    h2 = FakeHeaders({"user-agent": "same-ua", "x-hwid": "DEVICE-BBB"})
    hwid1 = main.extract_hwid(h1)
    hwid2 = main.extract_hwid(h2)
    check("explicit HWID uses 'id:' prefix", hwid1.startswith("id:"))
    check("same UA but different X-HWID => different device ids", hwid1 != hwid2)
    ua_only = main.extract_hwid(ua("same-ua"))
    check("UA-only uses 'ua:' prefix", ua_only.startswith("ua:"))

    sid_x = setup_sub(1)
    x1 = main.check_hwid_from_headers(sid_x, h1, ip="2001:db8::1")
    x2 = main.check_hwid_from_headers(sid_x, h2, ip="2001:db8::2")
    check("1st explicit-HWID device allowed", x1 is True)
    check("2nd explicit-HWID device rejected (limit=1)", x2 is False)

    # cleanup
    for s in (sid, sid0, sid_s, sid_x):
        main.SUBS.pop(s, None)

    print("-" * 50)
    print(f"RESULT: {PASS} passed, {FAIL} failed")
    return FAIL == 0


if __name__ == "__main__":
    ok = main_test()
    sys.exit(0 if ok else 1)
