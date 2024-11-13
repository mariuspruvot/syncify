from pydantic import BaseModel, HttpUrl
from typing import Optional

"""
Spotify Player Schema: It defines the structure of the player object returned by the Spotify API.
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


class ExternalIds(BaseModel):
    isrc: Optional[str] = None
    ean: Optional[str] = None
    upc: Optional[str] = None


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
    restrictions: Optional[dict[str, str]] = None
    name: Optional[str] = None
    popularity: Optional[int] = None
    preview_url: Optional[HttpUrl] = None
    track_number: Optional[int] = None
    type: Optional[str] = None
    uri: Optional[str] = None
    is_local: Optional[bool] = None


class Device(BaseModel):
    id: Optional[str] = None
    is_active: Optional[bool] = None
    is_private_session: Optional[bool] = None
    is_restricted: Optional[bool] = None
    name: Optional[str] = None
    type: Optional[str] = None
    volume_percent: Optional[int] = None
    supports_volume: Optional[bool] = None


class Context(BaseModel):
    type: Optional[str] = None
    href: Optional[str] = None
    external_urls: Optional[ExternalUrls] = None
    uri: Optional[str] = None


class Actions(BaseModel):
    interrupting_playback: Optional[bool] = None
    pausing: Optional[bool] = None
    resuming: Optional[bool] = None
    seeking: Optional[bool] = None
    skipping_next: Optional[bool] = None
    skipping_prev: Optional[bool] = None
    toggling_repeat_context: Optional[bool] = None
    toggling_shuffle: Optional[bool] = None
    toggling_repeat_track: Optional[bool] = None
    transferring_playback: Optional[bool] = None


class CurrentlyPlaying(BaseModel):
    device: Optional[Device] = None
    repeat_state: Optional[str] = None
    shuffle_state: Optional[bool] = None
    context: Optional[Context] = None
    timestamp: Optional[int] = None
    progress_ms: Optional[int] = None
    is_playing: Optional[bool] = None
    item: Optional[Track] = None
    currently_playing_type: Optional[str] = None
    actions: Optional[Actions] = None
