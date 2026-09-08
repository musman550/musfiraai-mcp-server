#!/usr/bin/env python3
"""
Runs against a checkout of musfiraai-mcp-server (with requirements already
installed) to verify the server actually works before any change is pushed
live. Exits non-zero on ANY failure — the workflow treats that as "do not
deploy this change."

Checks:
  1. server.py imports cleanly
  2. HTTP server boots in streamable-http mode
  3. GET /        -> 200 (docs page)
  4. GET /health  -> 200
  5. POST /mcp    -> valid MCP initialize handshake, 200
  6. tools/list   -> returns at least as many tools as before (never silently
                     loses functionality)
"""
import json
import os
import signal
import subprocess
import sys
import time
import urllib.request

PORT = 8399
BASE = f"http://127.0.0.1:{PORT}"
MIN_EXPECTED_TOOLS = 18


def check(name, fn):
    try:
        fn()
        print(f"PASS: {name}")
        return True
    except Exception as e:
        print(f"FAIL: {name} -> {e}")
        return False


def http_get(path):
    with urllib.request.urlopen(BASE + path, timeout=10) as r:
        return r.status


def http_post_json(path, payload, session_id=None):
    data = json.dumps(payload).encode()
    req = urllib.request.Request(
        BASE + path, data=data, method="POST",
        headers={"Content-Type": "application/json", "Accept": "application/json, text/event-stream"},
    )
    if session_id:
        req.add_header("Mcp-Session-Id", session_id)
    with urllib.request.urlopen(req, timeout=10) as r:
        session = r.headers.get("Mcp-Session-Id")
        body = r.read().decode()
        return r.status, body, session


def main():
    ok = check("server.py imports cleanly", lambda: subprocess.run(
        [sys.executable, "-c", "import server"], check=True, capture_output=True, timeout=30
    ))
    if not ok:
        sys.exit(1)

    env = dict(os.environ)
    env["MCP_TRANSPORT"] = "streamable-http"
    env["PORT"] = str(PORT)
    proc = subprocess.Popen([sys.executable, "server.py"], env=env,
                             stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    time.sleep(3)

    results = []
    try:
        results.append(check("GET / returns 200", lambda: (_ for _ in ()).throw(
            AssertionError(f"got {s}")) if (s := http_get("/")) != 200 else None))
        results.append(check("GET /health returns 200", lambda: (_ for _ in ()).throw(
            AssertionError(f"got {s}")) if (s := http_get("/health")) != 200 else None))

        session_holder = {}

        def do_init():
            status, body, session = http_post_json("/mcp", {
                "jsonrpc": "2.0", "id": 1, "method": "initialize",
                "params": {"protocolVersion": "2025-03-26", "capabilities": {},
                           "clientInfo": {"name": "smoke-test", "version": "1.0"}},
            })
            assert status == 200, f"initialize returned {status}"
            assert session, "no Mcp-Session-Id returned"
            session_holder["id"] = session

        results.append(check("POST /mcp initialize succeeds", do_init))

        def do_tools_list():
            sid = session_holder.get("id")
            assert sid, "no session from initialize step"
            http_post_json("/mcp", {"jsonrpc": "2.0", "method": "notifications/initialized"}, sid)
            status, body, _ = http_post_json("/mcp", {"jsonrpc": "2.0", "id": 2, "method": "tools/list"}, sid)
            assert status == 200, f"tools/list returned {status}"
            tools = []
            for line in body.splitlines():
                if line.startswith("data:"):
                    d = json.loads(line[5:])
                    tools = d.get("result", {}).get("tools", [])
            assert len(tools) >= MIN_EXPECTED_TOOLS, f"only {len(tools)} tools, expected >= {MIN_EXPECTED_TOOLS}"

        results.append(check(f"tools/list returns >= {MIN_EXPECTED_TOOLS} tools", do_tools_list))
    finally:
        proc.send_signal(signal.SIGINT)
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()

    if all(results):
        print("SMOKE TEST: ALL PASSED")
        sys.exit(0)
    else:
        print("SMOKE TEST: FAILED — refusing to deploy this change")
        sys.exit(1)


if __name__ == "__main__":
    main()
