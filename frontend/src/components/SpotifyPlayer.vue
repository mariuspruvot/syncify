<template>
  <div class="bg-base-200 rounded-box p-4">
    <div v-if="currentTrack" class="space-y-4">
      <!-- Player Info -->
      <div class="flex items-center gap-4">
        <img 
          :src="currentTrack.album.images[0].url" 
          :alt="currentTrack.name" 
          class="w-16 h-16 rounded-lg shadow-lg"
        />
        <div class="flex-1">
          <h3 class="font-bold truncate">{{ currentTrack.name }}</h3>
          <p class="text-sm opacity-70 truncate">{{ currentTrack.artists[0].name }}</p>
          <div class="flex items-center gap-2 mt-2">
            <span class="text-xs">{{ formatTime(position) }}</span>
            <progress 
              class="progress progress-success flex-1" 
              :value="position" 
              :max="currentTrack.duration_ms"
            ></progress>
            <span class="text-xs">{{ formatTime(currentTrack.duration_ms) }}</span>
          </div>
        </div>
      </div>
 
      <!-- Controls -->
      <div class="flex items-center justify-between">
        <PlayerControls 
          :is-playing="isPlaying"
          @toggle-play="togglePlay"
          @next-track="nextTrack"
          @previous-track="previousTrack"
        />
        
        <VolumeControl
          v-model:volume="volume"
          @update:volume="updateVolume"
        />
      </div>
 
      <!-- Queue Preview -->
      <div v-if="queue.length" class="mt-4">
        <div class="collapse collapse-arrow bg-base-100">
          <input type="checkbox" /> 
          <div class="collapse-title text-sm font-medium">
            Next in queue ({{ queue.length }})
          </div>
          <div class="collapse-content">
            <ul class="space-y-2">
              <li v-for="track in queue.slice(0, 4)" :key="track.id" class="flex items-center gap-2">
                <img 
                  :src="track.album.images[track.album.images.length - 1].url" 
                  :alt="track.name"
                  class="w-8 h-8 rounded"
                />
                <div class="flex-1 min-w-0">
                  <p class="truncate text-sm">{{ track.name }}</p>
                  <p class="truncate text-xs opacity-70">{{ track.artists[0].name }}</p>
                </div>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
 
    <!-- Loading State -->
    <div v-else class="text-center py-4">
      <span class="loading loading-spinner loading-lg"></span>
      <p class="mt-2">Connecting to Spotify...</p>
    </div>
 
    <!-- Error Toast -->
    <div v-if="error" class="toast toast-end">
      <div class="alert alert-error">
        <span>{{ error }}</span>
        <button class="btn btn-ghost btn-sm" @click="error = null">Dismiss</button>
      </div>
    </div>
  </div>
 </template>
 
 <script setup lang="ts">
 import { ref, watch, onMounted, onUnmounted } from 'vue'
 import { useSpotifySDK } from '~/composables/useSpotifySDK'
 import type { SpotifyTrack } from '~/types/spotify'
  import PlayerControls from './PlayerControl.vue'
 import VolumeControl from './VolumeControl.vue'
 
 const storedToken = localStorage.getItem('spotify_token')
 const volume = ref(50)
 const error = ref<string | null>(null)
 const queue = ref<SpotifyTrack[]>([])
 
 let queueInterval: ReturnType<typeof setInterval>
 
 const {
  player,
  currentTrack,
  isPlaying,
  position,
  formatTime,
 } = useSpotifySDK(storedToken || '')
 
 // Player controls
 async function togglePlay() {
  try {
    await player.value?.togglePlay()
  } catch (e) {
    error.value = 'Failed to toggle playback'
    setTimeout(() => {
      error.value = null
    }, 3000)
  }
 }
 
 async function nextTrack() {
  try {
    await player.value?.nextTrack()
  } catch (e) {
    error.value = 'Failed to skip track'
    setTimeout(() => {
      error.value = null
    }, 3000)
  }
 }
 
 async function previousTrack() {
  try {
    await player.value?.previousTrack()
  } catch (e) {
    error.value = 'Failed to go to previous track'
    setTimeout(() => {
      error.value = null
    }, 3000)
  }
 }
 
 async function updateVolume(newVolume: number) {
  try {
    await player.value?.setVolume(newVolume / 100)
  } catch (e) {
    error.value = 'Failed to update volume'
    setTimeout(() => {
      error.value = null
    }, 3000)
  }
 }
 
 // Queue management
 async function fetchQueue() {
  try {
    const token = localStorage.getItem('spotify_token')
    const response = await fetch('https://api.spotify.com/v1/me/player/queue', {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    if (response.ok) {
      const data = await response.json()
      queue.value = data.queue
    }
  } catch (e) {
    console.error('Failed to fetch queue:', e)
  }
 }
 
 onMounted(() => {
  console.log('Stored token:', storedToken) // Debug log
  fetchQueue()
  queueInterval = setInterval(fetchQueue, 10000)
 })
 
 onUnmounted(() => {
  if (queueInterval) {
    clearInterval(queueInterval)
  }
 })
 
 // Watch for token changes
 watch(() => storedToken, (newToken) => {
  if (newToken) {
    player.value?.connect()
  }
 })
 </script>