#!/usr/bin/env python3
"""Raw-socket client that sends a WebSocket upgrade request to Caddy and
prints the raw response header block as JSON.

Usage: client_ws.py <port> [plain]
"""
import json
import socket
import sys

port = int(sys.argv[1])
plain = len(sys.argv) > 2 and sys.argv[2] == "plain"

if plain:
    req = b"GET / HTTP/1.1\r\nHost: localhost\r\nConnection: close\r\n\r\n"
else:
    req = (
        b"GET /ws HTTP/1.1\r\n"
        b"Host: localhost\r\n"
        b"Upgrade: websocket\r\n"
        b"Connection: Upgrade\r\n"
        b"Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==\r\n"
        b"Sec-WebSocket-Version: 13\r\n"
        b"\r\n"
    )
s = socket.create_connection(("127.0.0.1", port), timeout=15)
s.sendall(req)
data = b""
s.settimeout(10)
try:
    while b"\r\n\r\n" not in data:
        chunk = s.recv(65536)
        if not chunk:
            break
        data += chunk
except socket.timeout:
    pass

header_block = data.split(b"\r\n\r\n", 1)[0].decode("latin-1")
lines = header_block.split("\r\n")
result = {
    "status_line": lines[0] if lines else "",
    "headers": lines[1:],
    "raw_head_len": len(header_block),
}
print(json.dumps(result, indent=1))
try:
    s.close()
except OSError:
    pass
