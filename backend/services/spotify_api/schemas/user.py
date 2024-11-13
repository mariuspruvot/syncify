from typing import Optional

from pydantic import BaseModel


"""
Spotify User Schema: It defines the structure of the user object returned by the Spotify API.
"""


class ExplicitContent(BaseModel):
    filter_enabled: bool
    filter_locked: bool


class ExternalUrls(BaseModel):
    spotify: str


class Followers(BaseModel):
    href: str
    total: int


class Image(BaseModel):
    url: str
    height: int
    width: int


class User(BaseModel):
    country: Optional[str] = None
    display_name: Optional[str] = None
    email: Optional[str] = None
    explicit_content: Optional[ExplicitContent] = None
    external_urls: Optional[ExternalUrls] = None
    followers: Optional[Followers] = None
    href: Optional[str] = None
    id: Optional[str] = None
    images: Optional[list[Image]] = None
    product: Optional[str] = None
    type: Optional[str] = None
    uri: Optional[str] = None
