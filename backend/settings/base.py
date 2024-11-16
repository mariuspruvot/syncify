from pydantic_settings import BaseSettings

from pathlib import Path


class Settings(BaseSettings):
    # PostgreSQL
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432

    # Spotify API
    SPOTIFY_CLIENT_ID: str
    SPOTIFY_CLIENT_SECRET: str
    SPOTIFY_BASE_URL: str = "https://api.spotify.com/"
    SPOTIFY_REDIRECT_URI: str
    SPOTIFY_AUTH_URL: str
    SPOTIFY_TOKEN_URL: str

    # Redis
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_URL: str = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"

    # JWT
    JWT_SECRET_KEY: str

    class Config:
        env_file = Path(__file__).resolve().parent.parent.parent / ".env"

    def get_database_url(self):
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"


GLOBAL_SETTINGS = Settings()
