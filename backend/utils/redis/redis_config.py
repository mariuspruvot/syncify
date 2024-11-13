import redis
from backend.settings.base import GLOBAL_SETTINGS
import logging
import json

logger = logging.getLogger(__name__)


class RedisConfig:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.connection = None
        return cls._instance

    def __init__(self):
        if not hasattr(self, "connection"):
            self.connection = None

    def init_connection(self):
        if self.connection is None:
            self.connection = redis.Redis.from_url(
                url=GLOBAL_SETTINGS.REDIS_URL, decode_responses=True
            )
            logger.info("Redis connection established.")

    def close_connection(self):
        """Closes the Redis connection."""
        self.connection.close()

    def set_key(self, key: str, value: str, expire: int = None) -> bool:
        """Sets a key in Redis with an optional expiration time."""
        try:
            self.connection.set(name=key, value=json.dumps(value), ex=expire)
            return True
        except redis.RedisError as e:
            print(f"Error setting key in Redis: {e}")
            return False

    def get_key(self, key: str) -> str | None:
        """Gets a value for a given key from Redis."""
        try:
            return json.loads(self.connection.get(name=key))
        except redis.RedisError as e:
            print(f"Error getting key from Redis: {e}")
            return None

    def delete_key(self, key: str) -> bool:
        """Deletes a key from Redis."""
        try:
            self.connection.delete(key)
            return True
        except redis.RedisError as e:
            print(f"Error deleting key from Redis: {e}")
            return False
