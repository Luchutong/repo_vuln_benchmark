#!/usr/bin/env python3
"""Minimal raw-TCP upstream for the Caddy hop-by-hop header reproduction.

Usage: upstream.py <port> <101|200> [tag]
Serves exactly one request then exits, printing a JSON line describing what
the Caddy proxy actually sent upstream.
"""
import json
import socket
import sys

port = int(sys.argv[1])
mode = sys.argv[2]

HOP = (
    b'Alt-Svc: h2="attacker.example.com:443"; ma=86400\r\n'
    b'Keep-Alive: timeout=999\r\n'
    b'Proxy-Authenticate: Basic realm="phish"\r\n'
    b'Set-Cookie: injected=malicious; Path=/\r\n'
)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(("127.0.0.1", port))
s.listen(1)
s.settimeout(60)
print(json.dumps({"upstream": "listening", "port": port, "mode": mode}), flush=True)
conn, addr = s.accept()
conn.settimeout(15)
data = b""
try:
    while b"\r\n\r\n" not in data:
        chunk = conn.recv(65536)
        if not chunk:
            break
        data += chunk
except socket.timeout:
    pass
head = data.split(b"\r\n\r\n", 1)[0].decode("latin-1")
print(json.dumps({"upstream": "request_line", "line": head.split("\r\n")[0]}), flush=True)
print(json.dumps({"upstream": "request_headers", "headers": head.split("\r\n")[1:]}), flush=True)

if mode == "101conn":
    resp = (
        b"HTTP/1.1 101 Switching Protocols\r\n"
        b"Upgrade: websocket\r\n"
        b"Connection: Upgrade, X-Custom-ID\r\n"
        b"Sec-WebSocket-Accept: s3pPLMBiTxaQ9kYGzzhZRbK+xOo=\r\n"
        b"X-Custom-ID: should-be-stripped\r\n"
        b"Alt-Svc: h2=\"attacker.example.com:443\"; ma=86400\r\n"
        b"\r\n"
    )
elif mode == "101":
    resp = (
        b"HTTP/1.1 101 Switching Protocols\r\n"
        b"Upgrade: websocket\r\n"
        b"Connection: Upgrade\r\n"
        b"Sec-WebSocket-Accept: s3pPLMBiTxaQ9kYGzzhZRbK+xOo=\r\n"
        + HOP
        + b"\r\n"
    )
else:
    body = b"hello"
    resp = (
        b"HTTP/1.1 200 OK\r\n"
        b"Content-Type: text/plain\r\n"
        b"Content-Length: " + str(len(body)).encode() + b"\r\n"
        + HOP
        + b"\r\n" + body
    )
conn.sendall(resp)
try:
    conn.shutdown(socket.SHUT_WR)
except OSError:
    pass
conn.settimeout(2)
try:
    conn.recv(65536)  # drain whatever the proxy tunnels
except Exception:
    pass
conn.close()
s.close()
print(json.dumps({"upstream": "done", "mode": mode}), flush=True)
