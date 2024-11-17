from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from backend.app.services.spotify_api.auth import SpotifyAuth
from backend.app.services.spotify_api.schemas.spotify_user import SpotifyUser
from backend.app.services.spotify_api.user_management.user_manager import UserManager
from backend.app.settings import GLOBAL_SETTINGS
from backend.app.utils.redis.redis_config import RedisConfig

spotify_router = APIRouter()


def get_spotify_auth() -> SpotifyAuth:
    return SpotifyAuth(
        GLOBAL_SETTINGS.SPOTIFY_CLIENT_ID, GLOBAL_SETTINGS.SPOTIFY_CLIENT_SECRET
    )


@spotify_router.get("/health-check", tags=["spotify"])
def health_check():
    return {"status": "ok"}


@spotify_router.get("/authorize", tags=["spotify"], status_code=200)
def authorize_user(auth: Annotated[SpotifyAuth, Depends(get_spotify_auth)]):
    """
    Generates the authorization URL for the user to grant access to the app.
    """
    try:
        return {"url": auth.get_authorization_url()}
    except Exception as err:
        raise HTTPException(
            status_code=500, detail=f"Error during Spotify authorization: {err}"
        )


@spotify_router.get("/callback", tags=["spotify"], status_code=200)
def spotify_callback(
    code: str,
    auth: Annotated[SpotifyAuth, Depends(get_spotify_auth)],
    redis: Annotated[RedisConfig, Depends()],
):
    """
    Retrieves the access token from the authorization code.
    """
    try:
        token = auth.retrieve_token(code)
        redis.set_key("spotify_token", token.access_token)

        return {"token": token}

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


@spotify_router.get("/user", tags=["spotify"], status_code=200)
async def get_current_user(token: str) -> SpotifyUser:
    """
    Gets the current user's information.
    """
    try:
        user_manager = UserManager(token)
        return await user_manager.get_current_user()
    except Exception as err:
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error occurred while retrieving user: {err}",
        )


@spotify_router.get("/user/{user_id}", tags=["spotify"], status_code=200)
async def get_user(token: str, user_id: str) -> SpotifyUser:
    """
    Gets a user's information.
    """
    try:
        user_manager = UserManager(token)
        return await user_manager.get_user(user_id)
    except Exception as err:
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error occurred while retrieving user: {err}",
        )
