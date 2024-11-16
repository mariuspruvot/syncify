from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
import uuid
from backend.models.base import BaseModel
import jwt
import os

from backend.settings.base import GLOBAL_SETTINGS


class Token(BaseModel):
    __tablename__ = "tokens"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    token = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    @staticmethod
    def generate_bearer_token(user_id) -> str:
        """
        Generates a cryptographically secure random JWT token to be used as a bearer token.
        The token is signed using a secret key stored in an environment variable.
        """
        secret_key = GLOBAL_SETTINGS.JWT_SECRET_KEY
        payload = {"user_id": user_id}
        jwt_token = jwt.encode(payload, secret_key, algorithm="HS256")
        return jwt_token
