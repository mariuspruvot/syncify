// src/types/spotify.ts
export interface SpotifyToken {
  access_token: string
  refresh_token: string
  expires_in: number
  token_type: string
}

export interface ApiResponse {
  token?: SpotifyToken
  error?: string
}

export interface SpotifyTrack {
  id: string
  name: string
  artists: { name: string }[]
  album: {
      images: { url: string }[]
  }
  duration_ms: number
}

export interface SpotifyPlayer {
  connect: () => Promise<boolean>
  disconnect: () => void
  togglePlay: () => Promise<void>
  nextTrack: () => Promise<void>
  previousTrack: () => Promise<void>
  setVolume: (volume: number) => Promise<void>
  addListener: (event: string, callback: (state: any) => void) => void
}

declare global {
  interface Window {
      Spotify: {
          Player: new (options: {
              name: string
              getOAuthToken: (cb: (token: string) => void) => void
              volume: number
          }) => SpotifyPlayer
      }
      onSpotifyWebPlaybackSDKReady: () => void
  }
}