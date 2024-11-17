from fastapi import FastAPI
from typing import AsyncIterator

from backend.app.routes.spotify import spotify_router
from backend.app.routes.users import users_router
from backend.app.config.logging import logger, LOGGING_CONFIG

from contextlib import asynccontextmanager
from backend.app.utils.redis.redis_config import RedisConfig
import logging.config
import uvicorn

from fastapi.middleware.cors import CORSMiddleware

import logging


logging.config.dictConfig(LOGGING_CONFIG)


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    logger.info("Startup")
    RedisConfig().init_connection()

    yield
    RedisConfig().close_connection()
    logger.info("Shutdown")


app = FastAPI(
    title="Syncify",
    description="Syncify is a music syncing service that allows you to sync your music across multiple devices.",
    version="0.1.0",
    lifespan=lifespan,
)
app.include_router(spotify_router, prefix="/spotify")
app.include_router(users_router, prefix="/users")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_origin_regex=None,
    expose_headers=["*"],
    max_age=600,
)


@app.get("/health-check")
def health_check():
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
