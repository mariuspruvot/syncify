from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException


from backend.settings.base import GLOBAL_SETTINGS
from backend.utils.redis.redis_config import RedisConfig

from backend.services.spotify_api.auth.auth import SpotifyAuth
from fastapi.responses import RedirectResponse


spotify_router = APIRouter()


@spotify_router.get("/health-check", tags=["spotify"])
def health_check():
    return {"status": "ok"}


@spotify_router.get("/authorize", tags=["spotify"], status_code=307)
def authorize_user():
    try:
        auth = SpotifyAuth(
            GLOBAL_SETTINGS.SPOTIFY_CLIENT_ID, GLOBAL_SETTINGS.SPOTIFY_CLIENT_SECRET
        )
        authorization_url = auth.get_authorization_url()
        return RedirectResponse(authorization_url)
    except Exception as err:
        raise HTTPException(
            status_code=500, detail=f"Error during Spotify authorization: {err}"
        )


@spotify_router.get("/callback", tags=["spotify"])
def spotify_callback(code: str, redis: Annotated[RedisConfig, Depends()]):
    try:
        auth = SpotifyAuth(
            GLOBAL_SETTINGS.SPOTIFY_CLIENT_ID, GLOBAL_SETTINGS.SPOTIFY_CLIENT_SECRET
        )
        auth.retrieve_token(code)
        token = auth.get_token()
        redis.set_key("spotify_token", token)
        return {"status": "ok", "token": token}

    except ValueError as err:
        raise HTTPException(status_code=401, detail=str(err))

    except Exception as err:
        raise HTTPException(
            status_code=500, detail=f"Error during Spotify callback: {err}"
        )


@spotify_router.get("/token", tags=["spotify"])
def get_token(redis: Annotated[RedisConfig, Depends()]):
    try:
        token = redis.get_key("spotify_token")
        if token:
            return {"status": "ok", "token": token}

        raise HTTPException(
            status_code=401, detail="Token not found. Please authorize via /authorize."
        )
    except Exception as err:
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error occurred while retrieving token: {err}",
        )
