from fastapi import FastAPI
from typing import AsyncIterator
from backend.utils.redis.redis_config import RedisConfig
from contextlib import asynccontextmanager
import uvicorn

from backend.routes.spotify import spotify_router
from backend.settings.logging import logger


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    logger.info("Startup")
    # init redis connection
    RedisConfig().init_connection()

    yield
    # close redis connection
    RedisConfig().close_connection()
    logger.info("Shutdown")


app = FastAPI(
    title="Syncify",
    description="Syncify is a music syncing service that allows you to sync your music across multiple devices.",
    version="0.1.0",
    lifespan=lifespan,
)
app.include_router(spotify_router, prefix="/spotify")


### Main HEALTH CHECK ###
@app.get("/health-check")
def health_check():
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
