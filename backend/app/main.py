from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, RedirectResponse

from app.api.routes import router
from app.api.iiko_routes import router as iiko_router
from app.core.config import settings
from app.db.base import Base
from app.db.session import engine
import app.models.iiko_mvp  # noqa: F401

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.app_name,
    version='1.0.0',
    docs_url='/docs',
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[x.strip() for x in settings.backend_cors_origins.split(',')],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(router)
app.include_router(iiko_router)


@app.get('/', response_class=HTMLResponse, tags=['ui'])
def landing_page() -> str:
    return """
    <!doctype html>
    <html lang='ru'>
      <head>
        <meta charset='UTF-8' />
        <meta name='viewport' content='width=device-width, initial-scale=1.0' />
        <title>Restaurant Ops Dashboard</title>
        <style>
          body { font-family: Inter, Arial, sans-serif; background: #0b1220; color: #e5e7eb; margin: 0; }
          .wrap { max-width: 920px; margin: 40px auto; padding: 0 20px; }
          .card { background: #111827; border: 1px solid #1f2937; border-radius: 12px; padding: 24px; }
          h1 { margin: 0 0 10px; font-size: 32px; }
          p { color: #9ca3af; }
          .grid { display: grid; gap: 12px; grid-template-columns: repeat(auto-fit, minmax(220px,1fr)); margin-top: 18px; }
          a.btn { display:block; text-decoration:none; color:#fff; background:#2563eb; padding:14px 16px; border-radius:10px; font-weight:600; }
          a.btn.alt { background:#374151; }
          .muted { margin-top: 18px; font-size: 14px; color: #9ca3af; }
        </style>
      </head>
      <body>
        <div class='wrap'>
          <div class='card'>
            <h1>Restaurant Ops Dashboard</h1>
            <p>API и сервис импорта отчётов iiko (email / manual / telegram).</p>
            <div class='grid'>
              <a class='btn' href='/docs'>Открыть Swagger API</a>
              <a class='btn alt' href='/health'>Проверить Health</a>
              <a class='btn alt' href='/restaurants'>Список ресторанов (JSON)</a>
            </div>
            <div class='muted'>Подсказка: для ручной загрузки отчётов используйте endpoint <code>POST /imports/manual-upload</code> в Swagger.</div>
          </div>
        </div>
      </body>
    </html>
    """


@app.get('/favicon.ico', include_in_schema=False)
def favicon_redirect() -> RedirectResponse:
    return RedirectResponse(url='https://fastapi.tiangolo.com/img/favicon.png')
