#!/usr/bin/env bash
set -euo pipefail

APP_TARGET="${APP_TARGET:-frontend}"

if [ "$APP_TARGET" = "backend" ]; then
  cd backend
  exec uvicorn app.main:app --host 0.0.0.0 --port "${PORT:-8000}"
fi

exec npm run start -- --port "${PORT:-3000}"
