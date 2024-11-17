from pydantic import BaseModel, HttpUrl
from typing import Optional


"""
Spotify Artist Schema: It defines the structure of the artist object returned by the Spotify API.
"""


class ExternalUrls(BaseModel):
    spotify: Optional[HttpUrl] = None


class Followers(BaseModel):
    href: Optional[str] = None
    total: Optional[int] = None


class Image(BaseModel):
    url: Optional[HttpUrl] = None
    height: Optional[int] = None
    width: Optional[int] = None


class Artist(BaseModel):
    external_urls: Optional[ExternalUrls] = None
    followers: Optional[Followers] = None
    genres: Optional[list[str]] = None
    href: Optional[str] = None
    id: Optional[str] = None
    images: Optional[list[Image]] = None
    name: Optional[str] = None
    popularity: Optional[int] = None
    type: Optional[str] = None
    uri: Optional[str] = None
