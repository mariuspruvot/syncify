from backend.services.spotify_api.schemas.spotifyuser import SpotifyUser
from backend.settings.base import GLOBAL_SETTINGS
import httpx
from backend.services.spotify_api.exceptions import SpotifyAPIException
import logging

logger = logging.getLogger("USER MANAGER")


class UserManager:
    def __init__(self, token: str):
        self.token = token
        self.user_url = GLOBAL_SETTINGS.SPOTIFY_BASE_URL + "v1/"

    async def get_current_user(self) -> SpotifyUser:
        """
        Gets the current user's information.
        """
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}",
        }
        try:
            response = httpx.get(self.user_url + "me", headers=headers)
            response.raise_for_status()
            return SpotifyUser(**response.json())

        except httpx.HTTPStatusError as err:
            logger.error(f"Failed to get current user: {err}")
            raise SpotifyAPIException(f"Failed to get current user: {err}")
        except httpx.RequestError as err:
            logger.error(f"Failed to get current user: {err}")
            raise SpotifyAPIException(f"Failed to get current user: {err}")
        except Exception as err:
            logger.error(f"An unexpected error occurred: {err}")
            raise SpotifyAPIException(f"Failed to get current user: {err}")

    async def get_user(self, user_id: str) -> SpotifyUser:
        """
        Gets a user's information.
        """
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}",
        }
        try:
            response = httpx.get(self.user_url + "users/" + user_id, headers=headers)
            response.raise_for_status()
            return SpotifyUser(**response.json())
        except httpx.HTTPStatusError as err:
            raise SpotifyAPIException(f"Failed to get user: {err}")
        except httpx.RequestError as err:
            raise SpotifyAPIException(f"Failed to get user: {err}")
        except Exception as err:
            raise SpotifyAPIException(f"Failed to get user: {err}")
