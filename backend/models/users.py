from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import bcrypt
from backend.models.base import BaseModel

# Friends association table
friends_association = Table(
    "friends_association",
    BaseModel.metadata,
    Column("user_id", String(36), ForeignKey("users.id"), primary_key=True),
    Column("friend_id", String(36), ForeignKey("users.id"), primary_key=True),
)


class User(BaseModel):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    spotify_id = Column(String(255), unique=True, nullable=True)
    country = Column(String(255), nullable=True)
    display_name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=True, unique=True)
    avatar = Column(String(255), nullable=True)
    is_online = Column(Boolean, default=False)
    currently_playing = Column(String(255), nullable=True)

    password_hash = Column(String(255), nullable=False)

    # Relationships
    friends = relationship(
        "User",
        secondary=friends_association,
        primaryjoin=id == friends_association.c.user_id,
        secondaryjoin=id == friends_association.c.friend_id,
        backref="friended_by",
    )

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def set_password(self, password: str) -> None:
        """
        Hashes the user's password with bcrypt and stores it in the password_hash field.
        """
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
        self.password_hash = hashed_password.decode("utf-8")
        return None

    def check_password(self, password: str) -> bool:
        """
        Checks if the given password matches the stored hashed password.
        """
        return bcrypt.checkpw(
            password.encode("utf-8"), self.password_hash.encode("utf-8")
        )
