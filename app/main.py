from fastapi import FastAPI

from app.api.routers import main_router
from app.core.config import settings

app = FastAPI(
    title=settings.app_title,
    description=settings.description,
    # docs_url=None,
    redoc_url=None,
)

app.include_router(main_router)
