from pydantic import BaseModel, HttpUrl
from typing import Optional


"""
Spotify Album Schema: It defines the structure of the album object returned by the Spotify API.
"""


class ExternalUrls(BaseModel):
    spotify: Optional[HttpUrl] = None


class Image(BaseModel):
    url: Optional[HttpUrl] = None
    height: Optional[int] = None
    width: Optional[int] = None


class Artist(BaseModel):
    external_urls: Optional[ExternalUrls] = None
    href: Optional[str] = None
    id: Optional[str] = None
    name: Optional[str] = None
    type: Optional[str] = None
    uri: Optional[str] = None


class LinkedFrom(BaseModel):
    external_urls: Optional[ExternalUrls] = None
    href: Optional[str] = None
    id: Optional[str] = None
    type: Optional[str] = None
    uri: Optional[str] = None


class Track(BaseModel):
    artists: Optional[list[Artist]] = None
    available_markets: Optional[list[str]] = None
    disc_number: Optional[int] = None
    duration_ms: Optional[int] = None
    explicit: Optional[bool] = None
    external_urls: Optional[ExternalUrls] = None
    href: Optional[str] = None
    id: Optional[str] = None
    is_playable: Optional[bool] = None
    linked_from: Optional[LinkedFrom] = None
    restrictions: Optional[dict[str, str]] = None
    name: Optional[str] = None
    preview_url: Optional[HttpUrl] = None
    track_number: Optional[int] = None
    type: Optional[str] = None
    uri: Optional[str] = None
    is_local: Optional[bool] = None


class Tracks(BaseModel):
    href: Optional[HttpUrl] = None
    limit: Optional[int] = None
    next: Optional[HttpUrl] = None
    offset: Optional[int] = None
    previous: Optional[HttpUrl] = None
    total: Optional[int] = None
    items: Optional[list[Track]] = None


class Copyright(BaseModel):
    text: Optional[str] = None
    type: Optional[str] = None


class ExternalIds(BaseModel):
    isrc: Optional[str] = None
    ean: Optional[str] = None
    upc: Optional[str] = None


class Album(BaseModel):
    album_type: Optional[str] = None
    total_tracks: Optional[int] = None
    available_markets: Optional[list[str]] = None
    external_urls: Optional[ExternalUrls] = None
    href: Optional[str] = None
    id: Optional[str] = None
    images: Optional[list[Image]] = None
    name: Optional[str] = None
    release_date: Optional[str] = None
    release_date_precision: Optional[str] = None
    restrictions: Optional[dict[str, str]] = None
    type: Optional[str] = None
    uri: Optional[str] = None
    artists: Optional[list[Artist]] = None
    tracks: Optional[Tracks] = None
    copyrights: Optional[list[Copyright]] = None
    external_ids: Optional[ExternalIds] = None
    genres: Optional[list[str]] = None
    label: Optional[str] = None
    popularity: Optional[int] = None
