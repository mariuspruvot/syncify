from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
import uuid
import bcrypt
from pydantic import EmailStr
from backend.app.models.tokens import Token


class FriendAssociation(SQLModel, table=True):
    """
    Association table for managing user friendships
    """

    __tablename__ = "friends_association"

    user_id: str = Field(foreign_key="users.id", primary_key=True, max_length=36)
    friend_id: str = Field(foreign_key="users.id", primary_key=True, max_length=36)


class UserBase(SQLModel):
    """
    Base User model with common fields
    """

    spotify_id: str | None = Field(default=None, max_length=255)
    country: str | None = Field(default=None, max_length=255)
    display_name: str = Field(max_length=255)
    email: EmailStr
    avatar: str | None = Field(default=None, max_length=255)
    is_online: bool = Field(default=False)
    currently_playing: str | None = Field(default=None, max_length=255)


class User(UserBase, table=True):
    """
    Database User model with all fields including sensitive data
    """

    __tablename__ = "users"

    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()), primary_key=True, max_length=36
    )
    password_hash: str = Field(max_length=255)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime | None = Field(default=None)

    # Relations
    friends: list["User"] = Relationship(
        back_populates="friended_by",
        link_model=FriendAssociation,  # Maintenant on utilise la classe directement
        sa_relationship_kwargs={
            "secondary": "friends_association",
            "primaryjoin": "User.id==FriendAssociation.user_id",
            "secondaryjoin": "User.id==FriendAssociation.friend_id",
        },
    )
    friended_by: list["User"] = Relationship(
        back_populates="friends",
        link_model=FriendAssociation,  # Maintenant on utilise la classe directement
        sa_relationship_kwargs={
            "secondary": "friends_association",
            "primaryjoin": "User.id==FriendAssociation.friend_id",
            "secondaryjoin": "User.id==FriendAssociation.user_id",
        },
    )
    tokens: list[Token] = Relationship(
        back_populates="user", sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )

    def set_password(self, password: str) -> None:
        """Hashes and sets the user password"""
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
        self.password_hash = hashed_password.decode("utf-8")

    def check_password(self, password: str) -> bool:
        """Verifies the user password"""
        return bcrypt.checkpw(
            password.encode("utf-8"), self.password_hash.encode("utf-8")
        )


class UserOut(UserBase):
    """
    Public User model without sensitive data
    """

    id: str
    created_at: datetime
    friends_count: int | None = None

    @classmethod
    def from_user(cls, user: User, include_friends_count: bool = False):
        """Creates a UserOut instance from a User instance"""
        user_dict = user.model_dump(
            exclude={"password_hash", "friended_by", "friends", "updated_at"}
        )
        if include_friends_count:
            user_dict["friends_count"] = len(user.friends)
        return cls(**user_dict)


class UserCreate(UserBase):
    """
    Model for creating a new user
    """

    password: str


class UserLogin(SQLModel):
    """
    Model for user login
    """

    email: str
    password: str


class UserUpdate(SQLModel):
    """
    Model for updating user information
    """

    display_name: str | None = None
    email: EmailStr | None = None
    country: str | None = None
    avatar: str | None = None
    password: str | None = Field(default=None, min_length=8, max_length=50)


class PaginatedUsers(SQLModel):
    """
    Response model for paginated users list
    """

    total: int
    users: list[UserOut]
    page: int = Field(ge=1)
    per_page: int = Field(ge=1, le=100)
    pages: int
