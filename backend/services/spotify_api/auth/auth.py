import httpx
from urllib.parse import urlencode

from backend.services.spotify_api.exceptions import SpotifyAuthenticationException
from backend.settings.base import GLOBAL_SETTINGS
from backend.services.spotify_api.schemas.token import SpotifyToken


class SpotifyAuth:
    def __init__(self, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.token: SpotifyToken | None = None
        self.redirect_uri = GLOBAL_SETTINGS.SPOTIFY_REDIRECT_URI
        self.authorization_url = GLOBAL_SETTINGS.SPOTIFY_AUTH_URL
        self.token_url = GLOBAL_SETTINGS.SPOTIFY_TOKEN_URL

    def get_authorization_url(self) -> str:
        """
        Generates the authorization URL for the user to grant access to the app.
        """
        params = {
            "client_id": self.client_id,
            "response_type": "code",
            "redirect_uri": self.redirect_uri,
            "scope": "user-read-playback-state user-modify-playback-state user-read-private",
            "show_dialog": "true",
        }
        return f"{self.authorization_url}?{urlencode(params)}"

    def retrieve_token(self, authorization_code: str):
        """
        Extracts the access token from the authorization code.
        """

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
        }
        data = {
            "grant_type": "authorization_code",
            "code": authorization_code,
            "redirect_uri": self.redirect_uri,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }
        try:
            response = httpx.post(self.token_url, data=data, headers=headers)
            response.raise_for_status()
            response_data = response.json()

            self._update_tokens(response_data)

        except httpx.HTTPStatusError as err:
            raise SpotifyAuthenticationException(f"Failed to retrieve token: {err}")
        except httpx.RequestError as err:
            raise SpotifyAuthenticationException(f"Failed to retrieve token: {err}")

    def get_token(self) -> str:
        """
        Returns the access token.
        """
        if not self.token.access_token:
            raise ValueError(
                "Access token is not set. Retrieve or refresh the token first."
            )
        return self.token.access_token

    def refresh_token(self):
        """
        Updates the access token using the refresh token.
        """
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
        }
        data = {
            "grant_type": "refresh_token",
            "refresh_token": self.token.refresh_token,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }
        try:
            response = httpx.post(self.token_url, data=data, headers=headers)
            response.raise_for_status()
            response_data = response.json()

            self._update_tokens(response_data)

        except httpx.HTTPStatusError as err:
            raise SpotifyAuthenticationException(f"Failed to refresh token: {err}")
        except httpx.RequestError as err:
            raise SpotifyAuthenticationException(f"Failed to refresh token: {err}")

    def _update_tokens(self, response_data: dict):
        self.token = SpotifyToken(**response_data)
