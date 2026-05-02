# Restaurant Ops Dashboard / iiko Email Reports Collector
Запускает backend для импорта отчетов iiko из email/ручной загрузки, парсинга и алертов.

## Локальный запуск
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

## Manual upload
POST `/imports/manual-upload` (restaurant_code, report_code, file)
