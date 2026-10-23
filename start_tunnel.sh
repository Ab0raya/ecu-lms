#!/usr/bin/env bash
set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "$DIR"

echo "=== Starting ECU LMS Mobile Backend ==="
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
else
    source .venv/bin/activate
fi

# Start FastAPI server in background
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 &
SERVER_PID=$!

sleep 2

echo "=== Launching Cloudflare Tunnel ==="
./bin/cloudflared tunnel --url http://127.0.0.1:8000

kill $SERVER_PID 2>/dev/null || true
