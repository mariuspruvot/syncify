<!-- src/components/SpotifyConnect.vue -->
<template>
  <div class="flex items-center justify-center min-h-screen bg-base-200 p-12">
    <div class="card w-96 bg-base-100 shadow-xl">
      <div class="card-body flex flex-col items-center text-center">
        <h2 class="card-title text-2xl font-bold mb-6 text-spotify-green">
          Connect Spotify
        </h2>
        <div class="w-full mb-6">
          <p class="text-left text-base-content">
            Syncify uses your Spotify account to access your music library and
            playlists. Connect your Spotify account to get started.
          </p>
        </div>
        
        <div v-if="error" class="alert alert-error mb-4">
          {{ error }}
        </div>

        <button
          class="btn btn-primary bg-spotify-green text-white hover:bg-green-700 mt-6"
          @click="connectSpotify"
          :disabled="isLoading"
        >
          <span v-if="isLoading" class="loading loading-spinner"></span>
          {{ isLoading ? 'Connecting...' : 'Connect Spotify' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const API_BASE = 'http://localhost:8000'
const isLoading = ref(false)
const error = ref<string | null>(null)

async function connectSpotify(): Promise<void> {
  isLoading.value = true
  error.value = null
  
  try {
    const response = await fetch(`${API_BASE}/spotify/authorize`, {
      method: 'GET',
      headers: {
        'Accept': 'application/json'
      }
    })
    
    if (!response.ok) {
      throw new Error('Failed to get authorization URL')
    }
    
    const data = await response.json()
    
    if (data.url) {
      window.location.href = data.url
    } else {
      throw new Error('No authorization URL received')
    }
    
  } catch (e) {
    console.error('Error connecting to Spotify:', e)
    error.value = 'Failed to connect to Spotify. Please try again.'
    isLoading.value = false
  }
}
</script>

<style scoped>
.text-spotify-green {
  color: #1DB954;
}

.bg-spotify-green {
  background-color: #1DB954;
}
</style>