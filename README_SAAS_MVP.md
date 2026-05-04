# Restaurant Ops Dashboard MVP

Рабочий MVP на Next.js (App Router) + Prisma/PostgreSQL + Tailwind.

## Что есть
- Dashboard `/` с карточками ресторанов и цветом риска по ФОТ.
- Restaurants `/restaurants` с формой добавления ресторана.
- Restaurant Details `/restaurants/[id]` с метриками и задачами.
- Tasks `/tasks` с таблицей статусов.
- API routes:
  - `GET/POST /api/restaurants`
  - `GET/POST /api/tasks`
  - `GET /api/metrics`
- Автологика: при создании ресторана с `laborCost > 12` создается задача **"Снизить ФОТ"**.

## Быстрый старт
1. `npm install`
2. Создать `.env`:
   - `DATABASE_URL=postgresql://...`
3. `npx prisma migrate dev --name init`
4. `npx prisma generate`
5. `npm run dev`

Открыть `http://localhost:3000`.

## Railway (важно)
В вашем текущем деплое runtime — Python, поэтому `npm` недоступен (ошибка `exec: npm: не найден`).

### Если это Python сервис (текущий `rusrest`)
- Оставьте `startCommand: ./start.sh`
- По умолчанию `start.sh` запускает backend (`APP_TARGET=backend`)

### Для веб-интерфейса Next.js
Создайте **второй Railway service** с Node runtime:
- Root: корень репозитория
- Build command: `npm install && npm run build`
- Start command: `APP_TARGET=frontend ./start.sh`
- Или просто `npm run start`
