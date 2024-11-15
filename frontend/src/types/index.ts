// src/types/index.ts
export interface User {
    id: string
    name: string
    avatar: string
}

export interface UserStats {
    activeSessions: number
    onlineFriends: number
    totalListeningTime: number
}

export interface Participant {
    id: string
    name: string
    avatar: string
    isHost: boolean
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