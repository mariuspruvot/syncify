<template>
  <Loader v-if="isLoading" />
  <SpotifyConnect v-else-if="!code" />
  <div v-else>
    <!-- Handle the callback -->
  </div>
 </template>
 
 <script setup lang="ts">
 import { ref, onMounted } from 'vue'
 import { useRoute, useRouter } from 'vue-router'
 import type { ApiResponse } from '../types/spotify'
 import SpotifyConnect from '../components/SpotifyConnect.vue'
 import Loader from '../components/Loader.vue'
 
 const route = useRoute()
 const router = useRouter()
 const isLoading = ref<boolean>(false)
 const error = ref<string | null>(null)
 const code = ref<string | null>(null)
 
 const API_BASE = 'http://localhost:8000'
 
 onMounted(async () => {
  const queryCode = route.query.code as string | undefined
  
  if (queryCode) {
    code.value = queryCode
    isLoading.value = true
    try {
      const response = await fetch(`${API_BASE}/spotify/callback?code=${queryCode}`)
      const data: ApiResponse = await response.json()
      console.log('data', data)
      
      if (data.token) {
        // Store token in localStorage
        localStorage.setItem('spotify_token', data.token.access_token)
        localStorage.setItem('spotify_refresh_token', data.token.refresh_token)
        localStorage.setItem('spotify_expires_at', String(Date.now() + data.token.expires_in * 1000))
        
        router.push('/home')
      } else {
        throw new Error(data.error || 'Failed to get token')
      }
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'Failed to connect to Spotify. Please try again.'
      console.error('Authentication error:', e)
    } finally {
      isLoading.value = false
    }
  }
 })
 </script>