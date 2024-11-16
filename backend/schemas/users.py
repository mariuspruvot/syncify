from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional, List
from datetime import datetime


class UserBase(BaseModel):
    display_name: str = Field(..., min_length=2, max_length=50)
    country: Optional[str] = Field(None, max_length=2)
    email: EmailStr = Field(
        ...,
        description="Valid email is required",
    )
    avatar: Optional[str] = None
    is_online: bool = False
    currently_playing: Optional[str] = None

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
            raise ValueError("Le nom ne peut pas être vide")
        return v.strip()


class UserCreate(UserBase):
    spotify_id: str = Field(..., min_length=5)
    password: str = Field(..., min_length=8, max_length=50)

    @classmethod
    @field_validator("password")
    def password_must_be_strong(cls, v):
        if not any(c.isupper() for c in v):
            raise ValueError("Le mot de passe doit contenir au moins une majuscule")
        if not any(c.islower() for c in v):
            raise ValueError("Le mot de passe doit contenir au moins une minuscule")
        if not any(c.isdigit() for c in v):
            raise ValueError("Le mot de passe doit contenir au moins un chiffre")
        return v


class UserUpdate(BaseModel):
    display_name: Optional[str] = Field(None, min_length=2, max_length=50)
    country: Optional[str] = Field(None, max_length=2)
    email: Optional[EmailStr] = None
    avatar: Optional[str] = None
    currently_playing: Optional[str] = None


class UserResponse(UserBase):
    pass


class User(UserBase):
    id: str
    spotify_id: str
    friends: List["User"] = []
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class UserList(BaseModel):
    total: int
    users: List[User]

    class Config:
        orm_mode = True
