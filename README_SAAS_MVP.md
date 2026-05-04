# Restaurant Ops Dashboard MVP

Node.js/Next.js frontend готовый для Railway (Nixpacks) + сохранённый Python backend в репозитории.

## Маршруты frontend
- `/` — Dashboard
- `/restaurants` — список ресторанов
- `/tasks` — список задач

## Тестовые данные (frontend)
Рестораны:
- Клёво Ростов
- Клёво Сахалин
- Клёво Сочи

Метрики:
- выручка
- ФОТ %
- food cost %
- открытые задачи

Задачи:
- Проверить ФОТ
- Проверить списания
- Проверить закупочные цены

## Локальный запуск
1. `npm install`
2. `npm run build`
3. `npm run start`

## Railway
Конфиг в `railway.toml` и `nixpacks.toml` принудительно запускает Node/Next.js:
- build: `npm install && npm run build`
- start: `npm run start`

Python backend не удалён, но больше не является основным entrypoint для Railway frontend деплоя.
