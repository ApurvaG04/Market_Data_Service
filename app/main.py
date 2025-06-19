from contextlib import asynccontextmanager
import logging
from fastapi import FastAPI
from app.api.routes import router
from app.core.db import engine
from app.models.base import Base


logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initializing database...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database initialized.")

    yield

app = FastAPI(title="Market Data Service", lifespan=lifespan)

app.include_router(router)