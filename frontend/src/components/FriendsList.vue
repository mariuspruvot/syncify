<!-- components/UserList.vue -->
<template>
  <div class="card bg-base-100 shadow-xl">
    <div class="card-body">
      <div class="flex justify-between items-center mb-4">
        <h2 class="card-title text-spotify-green">Spotify Users</h2>
        <button class="btn btn-circle btn-sm btn-ghost" @click="showSearchModal = true">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
        </button>
      </div>

      <!-- Users List -->
      <div class="space-y-4">
        <div v-for="user in users" :key="user.id" 
             class="flex items-center gap-3 p-3 rounded-lg hover:bg-base-200 transition-colors">
          <div class="avatar">
            <div class="relative w-12 rounded-full">
              <img 
                :src="user.images[0]?.url || 'https://via.placeholder.com/48'" 
                :alt="user.display_name" 
              />
              <div v-if="user.isOnline" 
                   class="absolute -bottom-1 -right-1 w-4 h-4 bg-success rounded-full border-2 border-base-100 flex items-center justify-center">
                <div class="w-2 h-2 bg-green-300 rounded-full animate-pulse"></div>
              </div>
            </div>
          </div>
          
          <div class="flex-1 min-w-0">
            <p class="font-medium truncate">{{ user.display_name }}</p>
            <p v-if="user.currentlyPlaying" class="text-xs text-green-500 truncate">
              <span class="mr-1">▶</span>{{ user.currentlyPlaying.track }} - {{ user.currentlyPlaying.artist }}
            </p>
            <p v-else class="text-xs opacity-50">Not listening</p>
          </div>

          <button v-if="user.isOnline && user.currentlyPlaying"
                  class="btn btn-sm btn-primary"
                  @click="joinListening(user)">
            Join
          </button>
        </div>
      </div>
    </div>

    <!-- Search Modal -->
    <dialog class="modal" :class="{ 'modal-open': showSearchModal }">
      <div class="modal-box">
        <h3 class="font-bold text-lg mb-4">Search Spotify Users</h3>
        <div class="form-control">
          <div class="input-group">
            <input type="text" 
                   placeholder="Search by username..."
                   class="input input-bordered flex-1"
                   v-model="searchQuery"
                   @keyup.enter="searchUsers"
            />
            <button class="btn btn-square" @click="searchUsers">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </button>
          </div>
        </div>

        <!-- Search Results -->
        <div v-if="isSearching" class="py-8 text-center">
          <span class="loading loading-spinner loading-md"></span>
        </div>

        <div v-else class="mt-4 space-y-2">
          <div v-for="user in searchResults" :key="user.id"
               class="flex items-center gap-3 p-2 rounded-lg">
            <div class="avatar">
              <div class="w-10 rounded-full">
                <img 
                  :src="user.images[0]?.url || 'https://via.placeholder.com/40'" 
                  :alt="user.display_name" 
                />
              </div>
            </div>
            <div class="flex-1">
              <p class="font-medium">{{ user.display_name }}</p>
              <p class="text-xs opacity-70">{{ user.country }}</p>
            </div>
          </div>
        </div>

        <div class="modal-action">
          <button class="btn" @click="showSearchModal = false">Close</button>
        </div>
      </div>
      <form method="dialog" class="modal-backdrop">
        <button @click="showSearchModal = false">close</button>
      </form>
    </dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import type { User } from '~/types'

const users = ref<User[]>([])
const searchQuery = ref('')
const searchResults = ref<User[]>([])
const showSearchModal = ref(false)
const isSearching = ref(false)
const error = ref<string | null>(null)

async function fetchUsers() {
  try {
    const response = await fetch('http://localhost:8000/users', {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('spotify_token')}`
      }
    })
    
    if (response.ok) {
      const data = await response.json()
      users.value = data.users
    }
  } catch (e) {
    console.error('Failed to fetch users:', e)
    error.value = 'Failed to load users'
  }
}

async function searchUsers() {
  if (!searchQuery.value.trim()) return
  
  isSearching.value = true
  try {
    const response = await fetch(`http://localhost:8000/spotify/user/search?q=${searchQuery.value}`, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('spotify_token')}`
      }
    })
    
    if (response.ok) {
      searchResults.value = await response.json()
    }
  } catch (e) {
    console.error('Failed to search users:', e)
    error.value = 'Search failed'
  } finally {
    isSearching.value = false
  }
}

async function joinListening(user: User) {
  if (!user.currentlyPlaying) return
  
  emit('join-listening', {
    userId: user.id,
    track: user.currentlyPlaying
  })
}

const emit = defineEmits<{
  'join-listening': [{
    userId: string,
    track: NonNullable<User['currentlyPlaying']>
  }]
}>()

onMounted(() => {
  fetchUsers()
})
</script>