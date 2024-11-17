from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy.sql import func
import uuid
import jwt

from backend.app.settings import GLOBAL_SETTINGS


class Token(SQLModel, table=True):
    """
    Token model for user authentication with JWT support
    """

    __tablename__ = "tokens"

    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()), primary_key=True, max_length=36
    )
    user_id: str = Field(
        foreign_key="users.id",
        max_length=36,
        sa_column_kwargs={"index": True},  # Si tu veux un index sur user_id
    )
    token: str = Field(max_length=255, nullable=False)
    is_active: bool = Field(default=True)

    # Timestamps
    created_at: datetime = Field(
        default_factory=datetime.now, sa_column_kwargs={"server_default": func.now()}
    )
    updated_at: datetime | None = Field(
        default=None, sa_column_kwargs={"onupdate": func.now()}
    )

    # Relation with User model - The ondelete CASCADE is specified here
    user: "User" = Relationship(
        back_populates="tokens",
        sa_relationship_kwargs={"cascade": "all, delete", "passive_deletes": True},
    )

    @staticmethod
    def generate_bearer_token(user_id: str) -> str:
        """
        Generates a JWT bearer token.

        Args:
            user_id: The ID of the user

        Returns:
            str: The generated JWT token
        """
        secret_key = GLOBAL_SETTINGS.JWT_SECRET_KEY
        payload = {"user_id": user_id}
        jwt_token = jwt.encode(payload, secret_key, algorithm="HS256")
        return jwt_token

    class Config:
        from_attributes = True
