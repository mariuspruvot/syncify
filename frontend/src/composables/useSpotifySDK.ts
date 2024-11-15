// composables/useSpotifySDK.ts
import { ref, onMounted, onUnmounted } from 'vue'
import type { SpotifyTrack, SpotifyPlayer } from '~/types/spotify'

export function useSpotifySDK(token: string) {
  const player = ref<SpotifyPlayer | null>(null)
  const deviceId = ref<string>('')
  const currentTrack = ref<SpotifyTrack | null>(null)
  const isPlaying = ref(false)
  const position = ref(0)
  let progressInterval: ReturnType<typeof setInterval>

  function formatTime(ms: number): string {
    const seconds = Math.floor((ms / 1000) % 60)
    const minutes = Math.floor((ms / (1000 * 60)) % 60)
    return `${minutes}:${seconds.toString().padStart(2, '0')}`
  }

  async function initializePlayer() {
    try {
      await fetch('https://api.spotify.com/v1/me/player', {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          device_ids: [deviceId.value],
          play: false,
        }),
      })
    } catch (error) {
      console.error('Error initializing player:', error)
    }
  }

  onMounted(() => {
    const script = document.createElement('script')
    script.src = 'https://sdk.scdn.co/spotify-player.js'
    script.async = true
    document.body.appendChild(script)

    window.onSpotifyWebPlaybackSDKReady = () => {
      player.value = new window.Spotify.Player({
        name: 'Syncify Web Player',
        getOAuthToken: cb => { cb(token) },
        volume: 0.5
      })

      player.value.addListener('ready', ({ device_id }: { device_id: string }) => {
        console.log('Ready with Device ID', device_id)
        deviceId.value = device_id
        initializePlayer()
      })

      player.value.addListener('player_state_changed', (state: any) => {
        if (!state) return

        currentTrack.value = state.track_window.current_track
        isPlaying.value = !state.paused
        position.value = state.position

        if (progressInterval) {
          clearInterval(progressInterval)
        }
        
        if (isPlaying.value) {
          progressInterval = setInterval(() => {
            position.value += 1000
          }, 1000)
        }
      })

      player.value.connect()
    }
  })

  onUnmounted(() => {
    if (progressInterval) {
      clearInterval(progressInterval)
    }
    if (player.value) {
      player.value.disconnect()
    }
  })

  return {
    player,
    currentTrack,
    isPlaying,
    position,
    formatTime,
  }
}