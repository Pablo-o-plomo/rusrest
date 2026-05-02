# Restaurant Ops Dashboard / iiko Email Reports Collector

Backend для импорта отчетов iiko из email, ручной загрузки и Telegram-бота.

## Локальный запуск API
```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

## Seed
```bash
python -m app.seed_iiko
```

## Ручная загрузка
`POST /imports/manual-upload` (restaurant_code, report_code, file)

## Загрузка через Telegram-бота
1. Укажите `ADMIN_TELEGRAM_BOT_TOKEN` в `.env`.
2. Запустите:
```bash
./start_bot.sh
```
3. Отправьте файл боту с caption: `SOCHI R02 2026-05-01`.

## Загрузка через Email (IMAP)
1. Укажите EMAIL_* переменные в `.env`.
2. Разовый запуск: `POST /email/check-now`.
3. Фоновый worker каждые 10 минут:
```bash
./start_email_worker.sh
```

## Railway (рекомендуемая схема)
- Service 1 (API): `./start.sh`
- Service 2 (Bot worker): `./start_bot.sh`
- Service 3 (Email worker): `./start_email_worker.sh`
