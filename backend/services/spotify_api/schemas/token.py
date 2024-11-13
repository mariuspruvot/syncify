from pydantic import BaseModel


class SpotifyToken(BaseModel):
    access_token: str | None = None
    token_type: str | None = None
    scope: str | None = None
    expires_in: int | None = None
    refresh_token: str | None = None
