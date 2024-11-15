<!-- src/components/AuthSuccess.vue -->
<template>
  <div class="flex items-center justify-center min-h-screen bg-base-200 p-12">
    <div class="card w-96 bg-base-100 shadow-xl">
      <div class="card-body flex flex-col items-center text-center">
        <div class="text-success mb-4">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            class="h-16 w-16"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M5 13l4 4L19 7"
            />
          </svg>
        </div>
        <h2 class="card-title text-2xl font-bold mb-6 text-spotify-green">
          Authentication Successful!
        </h2>
        <p class="text-base-content mb-6">
          Your Spotify account has been successfully connected to Syncify.
        </p>
        <button
          class="btn bg-spotify-green text-white hover:bg-green-700"
          @click="goHome"
        >
          Continue to Home
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()

function goHome(): void {
  router.push('/home')
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