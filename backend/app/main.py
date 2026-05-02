from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router
from app.api.iiko_routes import router as iiko_router
from app.core.config import settings
from app.db.base import Base
from app.db.session import engine
import app.models.iiko_mvp

Base.metadata.create_all(bind=engine)
app=FastAPI(title=settings.app_name,version='1.0.0')
app.add_middleware(CORSMiddleware,allow_origins=[x.strip() for x in settings.backend_cors_origins.split(',')],allow_credentials=True,allow_methods=['*'],allow_headers=['*'])
app.include_router(router)
app.include_router(iiko_router)
