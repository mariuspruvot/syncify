from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional, List
from datetime import datetime


class UserBase(BaseModel):
    display_name: str | None = Field(None, min_length=2, max_length=50)
    country: str | None = Field(None, max_length=2)
    email: EmailStr = Field(
        ...,
        description="Valid email is required",
    )
    avatar: str | None = None
    spotify_id: str | None = None
    is_online: bool = False
    currently_playing: str | None = None

    @classmethod
    @field_validator("email")
    def email_must_be_valid_domain(cls, v):
        if not v.endswith((".com", ".fr", ".net")):
            raise ValueError("Domain name must end with .com, .fr or .net")
        return v

    @classmethod
    @field_validator("display_name")
    def name_must_be_valid(cls, v):
        if not v.strip():
            raise ValueError("Name cannot be empty")
        return v.strip()

    @classmethod
    @field_validator("display_name")
    def name_must_be_unique(cls, v, values):
        if v and v.strip() in [user.display_name for user in values]:
            raise ValueError("Name already in use")
        return v


class UserCreate(UserBase):
    spotify_id: str | None = Field(None, min_length=5)
    password: str = Field(..., min_length=8, max_length=50)

    @classmethod
    @field_validator("password")
    def password_must_be_strong(cls, v):
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(c.islower() for c in v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one digit")
        return v


class UserUpdate(BaseModel):
    display_name: Optional[str] = Field(None, min_length=2, max_length=50)
    country: Optional[str] = Field(None, max_length=2)
    email: Optional[EmailStr] = None
    avatar: Optional[str] = None
    currently_playing: Optional[str] = None


class UserResponse(UserBase):
    id: str | None = None
    spotify_id: str | None = None
    friends: List["UserResponse"] | None = None

    class Config:
        orm_mode = True


class UserList(BaseModel):
    total: int
    users: list[UserResponse]

    class Config:
        orm_mode = True
