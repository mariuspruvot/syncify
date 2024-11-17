// src/types/index.ts
export interface User {
    id: string
    country: string | null
    email: string
    display_name: string
    isOnline?: boolean
    avatar: string | null
    currentlyPlaying?: {
        track: string
        artist: string
        startedAt: number
        uri: string
    }
}

export interface UserStats {
    activeSessions: number | null
    onlineFriends: number | null
    totalListeningTime: number | null
}

export interface Participant {
    id: string | null
    name: string | null
    avatar: string | null
    isHost: boolean | null
}

export interface Session {
    id: string
    code: string
    name: string
    hostId: string
    status: 'active' | 'ended'
    participants: Participant[]
    startTime: string
    duration: number
}

export interface Friend {
    id: string;
    name: string;
    avatar: string;
    isOnline: boolean;
    currentlyPlaying?: string;
  }