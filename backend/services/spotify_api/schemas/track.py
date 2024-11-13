from typing import Any, Dict, Optional

from pydantic import BaseModel

"""
Spotify Track Schema: It defines the structure of the track object returned by the Spotify API.
"""


class ExternalUrls(BaseModel):
    spotify: str


class Image(BaseModel):
    url: str
    height: int
    width: int


class Restrictions(BaseModel):
    reason: str


class Artist(BaseModel):
    external_urls: ExternalUrls
    href: str
    id: str
    name: str
    type: str
    uri: str


class Album(BaseModel):
    album_type: str
    total_tracks: int
    available_markets: list[str]
    external_urls: ExternalUrls
    href: str
    id: str
    images: list[Image]
    name: str
    release_date: str
    release_date_precision: str
    restrictions: Restrictions
    type: str
    uri: str
    artists: list[Artist]


class ExternalIds(BaseModel):
    isrc: str
    ean: str
    upc: str


class Track(BaseModel):
    album: Optional[Album] = None
    artists: Optional[list[Artist]] = None
    available_markets: Optional[list[str]] = None
    disc_number: Optional[int] = None
    duration_ms: Optional[int] = None
    explicit: Optional[bool] = None
    external_ids: Optional[ExternalIds] = None
    external_urls: Optional[ExternalUrls] = None
    href: Optional[str] = None
    id: Optional[str] = None
    is_playable: Optional[bool] = None
    linked_from: Optional[Dict[str, Any]] = None
    restrictions: Optional[Restrictions] = None
    name: Optional[str] = None
    popularity: Optional[int] = None
    preview_url: Optional[str] = None
    track_number: Optional[int] = None
    type: Optional[str] = None
    uri: Optional[str] = None
    is_local: Optional[bool] = None
