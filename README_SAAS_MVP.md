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

## Railway
### Frontend service
- Start command: `./start.sh`
- Env: `APP_TARGET=frontend`

### Backend service (опционально для FastAPI из старой части репо)
- Start command: `./start_backend.sh`
- Env: `APP_TARGET=backend`
