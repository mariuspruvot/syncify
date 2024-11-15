<!-- components/PlayerControls.vue -->
<template>
  <div class="flex items-center justify-center h-full">
    <div class="flex gap-4">
      <button 
        class="hover:bg-spotify-green btn btn-circle btn-primary flex items-center justify-center" 
        @click="$emit('previous-track')"
        aria-label="Previous Track"
      >
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-6 h-6">
          <path d="M9.195 18.44c1.25.714 2.805-.189 2.805-1.629v-2.34l6.945 3.968c1.25.715 2.805-.188 2.805-1.628V8.69c0-1.44-1.555-2.343-2.805-1.628L12 11.029v-2.34c0-1.44-1.555-2.343-2.805-1.628l-7.108 4.061c-1.26.72-1.26 2.536 0 3.256l7.108 4.061Z" />
        </svg>
      </button>

      <button 
        class="hover:bg-spotify-green btn btn-circle btn-primary flex items-center justify-center"
        @click="$emit('toggle-play')"
        aria-label="Play/Pause"
      >
        <svg 
          v-if="!isPlaying" 
          xmlns="http://www.w3.org/2000/svg" 
          class="w-6 h-6" 
          fill="none" 
          viewBox="0 0 24 24" 
          stroke="currentColor"
        >
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 3l14 9-14 9V3z" />
        </svg>
        <svg 
          v-else 
          xmlns="http://www.w3.org/2000/svg" 
          class="w-6 h-6" 
          fill="none" 
          viewBox="0 0 24 24" 
          stroke="currentColor"
        >
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 4h4v16H6zM14 4h4v16h-4z" />
        </svg>
      </button>

      <button 
      class="hover:bg-spotify-green btn btn-circle btn-primary flex items-center justify-center" 
        @click="$emit('next-track')"
        aria-label="Next Track"
      >
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-6 h-6">
          <path d="M5.055 7.06C3.805 6.347 2.25 7.25 2.25 8.69v8.122c0 1.44 1.555 2.343 2.805 1.628L12 14.471v2.34c0 1.44 1.555 2.343 2.805 1.628l7.108-4.061c1.26-.72 1.26-2.536 0-3.256l-7.108-4.061C13.555 6.346 12 7.249 12 8.689v2.34L5.055 7.061Z" />
        </svg>
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  isPlaying: boolean
}>()

defineEmits<{
  'toggle-play': []
  'next-track': []
  'previous-track': []
}>()
</script>
