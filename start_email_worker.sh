#!/usr/bin/env bash
set -euo pipefail
cd backend
exec python -m app.services.email_worker
