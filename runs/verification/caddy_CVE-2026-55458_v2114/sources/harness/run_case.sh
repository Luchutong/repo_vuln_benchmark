#!/usr/bin/env bash
# Driver for the Caddy hop-by-hop header reproduction.
# Usage: run_case.sh <label> <caddy-binary> <client-mode: ws|plain> <upstream-mode: 101|200> <proxy-port> <upstream-port>
set -u
LABEL="$1"; BIN="$2"; CLIENT_MODE="$3"; UP_MODE="$4"; PPORT="$5"; UPORT="$6"
DIR="/tmp/recon_run/$LABEL"
rm -rf "$DIR"; mkdir -p "$DIR/data" "$DIR/config"
cat > "$DIR/Caddyfile" <<EOF
{
	auto_https off
	admin off
	log default {
		level ERROR
	}
}

:$PPORT {
	reverse_proxy 127.0.0.1:$UPORT
}
EOF
echo "=== label=$LABEL bin=$BIN client=$CLIENT_MODE upstream=$UP_MODE proxy=:$PPORT upstream=:$UPORT"
echo "=== Caddyfile ==="; cat "$DIR/Caddyfile"
"$BIN" adapt --config "$DIR/Caddyfile" --adapter caddyfile > "$DIR/adapt.json" 2> "$DIR/adapt.err"
echo "adapt_exit=$? adapt_bytes=$(wc -c < "$DIR/adapt.json")"; head -c 300 "$DIR/adapt.err"

python3 /tmp/recon_scripts/upstream.py "$UPORT" "$UP_MODE" > "$DIR/upstream.log" 2>&1 &
UP_PID=$!
sleep 0.5

XDG_DATA_HOME="$DIR/data" XDG_CONFIG_HOME="$DIR/config" "$BIN" run --config "$DIR/Caddyfile" --adapter caddyfile > "$DIR/caddy.log" 2>&1 &
CADDY_PID=$!

# wait for the proxy port
for i in $(seq 1 100); do
  if (exec 3<>/dev/tcp/127.0.0.1/$PPORT) 2>/dev/null; then exec 3>&-; break; fi
  sleep 0.1
done
sleep 0.3

if [ "$CLIENT_MODE" = "plain" ]; then
  python3 /tmp/recon_scripts/client_ws.py "$PPORT" plain > "$DIR/client.json" 2> "$DIR/client.err"
elif [ "$CLIENT_MODE" = "curl" ]; then
  curl -sv --max-time 10 \
    -H "Upgrade: websocket" \
    -H "Connection: Upgrade" \
    -H "Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==" \
    -H "Sec-WebSocket-Version: 13" \
    "http://localhost:$PPORT/ws" > "$DIR/curl.body" 2> "$DIR/curl.verbose"
  cp "$DIR/curl.verbose" "$DIR/client.json"
else
  python3 /tmp/recon_scripts/client_ws.py "$PPORT" > "$DIR/client.json" 2> "$DIR/client.err"
fi
CLIENT_EXIT=$?
sleep 0.5
kill "$CADDY_PID" 2>/dev/null; kill "$UP_PID" 2>/dev/null
wait "$CADDY_PID" 2>/dev/null; wait "$UP_PID" 2>/dev/null

echo "=== client exit=$CLIENT_EXIT ==="
cat "$DIR/client.json"
echo "=== upstream log ==="; cat "$DIR/upstream.log"
echo "=== caddy log (tail) ==="; tail -20 "$DIR/caddy.log"
