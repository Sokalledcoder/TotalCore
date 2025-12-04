#!/usr/bin/env bash
set -euo pipefail
cd /home/soka/Desktop/TradeCore
LOG=server.log
if pgrep -f "uvicorn app.api:app" >/dev/null; then
  pkill -f "uvicorn app.api:app"
  sleep 1
fi
source .venv/bin/activate
nohup uvicorn app.api:app --host 0.0.0.0 --port 8001 >"$LOG" 2>&1 &
PID=$!
sleep 1
echo "uvicorn started (PID $PID). tail -f $LOG"
head -n 5 "$LOG"
