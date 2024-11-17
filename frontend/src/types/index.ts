// src/types/index.ts
export interface Image {
    url: string | null
    width: number | null
    height: number | null
}

export interface User {
    id: string
    country: string | null
    displayName: string
    images: Image[]
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