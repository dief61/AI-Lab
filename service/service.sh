#!/usr/bin/env bash

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
BASE_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
PORT=8000
APP="service.main:app"
PID_FILE="/tmp/uvicorn-demo.pid"
LOG_FILE="/tmp/uvicorn.log"

get_pid() {
  pid=$(lsof -ti :"$PORT" 2>/dev/null)
  echo "$pid"
}

print_header() {
  clear
  echo "========================================"
  echo "      AI-Demo Service Manager"
  echo "========================================"
  echo
}

status_line() {
  pid=$(get_pid)
  if [ -n "$pid" ]; then
    echo "  Status:  [RUNNING]  (PID: $pid)"
  else
    echo "  Status:  [STOPPED]"
  fi
  echo "  Port:    $PORT"
  echo "  Log:     $LOG_FILE"
  echo "----------------------------------------"
  echo
}

start_service() {
  pid=$(get_pid)
  if [ -n "$pid" ]; then
    echo "Service läuft bereits (PID: $pid)"
    sleep 2
    return
  fi
  nohup "$BASE_DIR/.venv/bin/uvicorn" "$APP" --reload --host 0.0.0.0 --port "$PORT" > "$LOG_FILE" 2>&1 &
  spid=$!
  echo "$spid" > "$PID_FILE"
  sleep 2
  echo "Service gestartet (PID: $spid)"
  sleep 2
}

stop_service() {
  pid=$(get_pid)
  if [ -z "$pid" ]; then
    echo "Läuft nicht."
    sleep 2
    return
  fi
  kill "$pid" 2>/dev/null
  sleep 1
  echo "Service beendet (PID: $pid)"
  sleep 2
}

restart_service() {
  stop_service
  start_service
}

while true; do
  print_header
  status_line

  pid=$(get_pid)
  if [ -n "$pid" ]; then
    echo "  [1] Neu starten"
    echo "  [2] Beenden"
    echo "  [3] Beenden (Skript)"
    echo
    read -rp "  Auswahl [1-3]: " choice
    case "$choice" in
      1) restart_service ;;
      2) stop_service ;;
      3) clear; echo "Tschüss!"; exit 0 ;;
      *) ;;
    esac
  else
    echo "  [1] Starten"
    echo "  [2] Beenden (Skript)"
    echo
    read -rp "  Auswahl [1-2]: " choice
    case "$choice" in
      1) start_service ;;
      2) clear; echo "Tschüss!"; exit 0 ;;
      *) ;;
    esac
  fi
done
