import contextlib
from typing import AsyncIterator

from fastapi import FastAPI

import core
from api.routers import main_router
from core.config import settings


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    core.db_manager.init(settings.database_url)
    yield
    await core.db_manager.close()

app = FastAPI(
    title=settings.app_title,
    description=settings.app_description,
    lifespan=lifespan
)

app.include_router(main_router)
