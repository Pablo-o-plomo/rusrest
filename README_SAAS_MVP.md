# Restaurant Ops Map MVP

Next.js + TypeScript + Prisma/PostgreSQL приложение для визуального управления ресторанными процессами.

## Структура
- app/
- components/
- lib/
- prisma/
- services/

## Локальный запуск (frontend)
1. `npm install`
2. создать `.env` с `DATABASE_URL`
3. `npx prisma generate`
4. `npm run dev`

## Railway деплой (рекомендуется 2 сервиса)

### 1) Frontend service (Next.js)
- Root directory: корень репозитория
- Start command: `./start.sh`
- Environment variable: `APP_TARGET=frontend`
- Public domain: включить

### 2) Backend service (FastAPI)
- Root directory: корень репозитория (или `backend`, если создадите отдельный сервис из подпапки)
- Start command: `./start_backend.sh` (или `./start.sh` + `APP_TARGET=backend`)
- Public domain: включить при необходимости публичного API

## Быстрый single-service режим
Можно запускать через один `start.sh` и переключать `APP_TARGET`:
- `APP_TARGET=frontend` → веб-интерфейс
- `APP_TARGET=backend` → API

> Для production рекомендуем два отдельных Railway service, чтобы UI и API были доступны одновременно.
