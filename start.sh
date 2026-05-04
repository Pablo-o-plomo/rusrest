#!/usr/bin/env bash
set -euo pipefail

APP_TARGET="${APP_TARGET:-backend}"

if [ "$APP_TARGET" = "frontend" ]; then
  if ! command -v npm >/dev/null 2>&1; then
    echo "[start.sh] npm not found in runtime image. Set APP_TARGET=backend or use Node service for frontend." >&2
    exit 1
  fi
  exec npm run start -- --port "${PORT:-3000}"
fi

cd backend
exec uvicorn app.main:app --host 0.0.0.0 --port "${PORT:-8000}"
