<!-- components/VolumeControl.vue -->
<template>
  <div class="flex items-center gap-2">
    <button 
      class="btn btn-ghost btn-sm btn-circle"
      @click="toggleMute"
    >
      <svg
        xmlns="http://www.w3.org/2000/svg"
        class="h-4 w-4"
        fill="none"
        viewBox="0 0 24 24"
        stroke="currentColor"
      >
        <path
          v-if="volume === 0"
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="2"
          d="M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-4.707C10.923 3.663 12 4.109 12 5v14c0 .891-1.077 1.337-1.707.707L5.586 15z"
        />
        <path
          v-else
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="2"
          d="M15.536 8.464a5 5 0 010 7.072M18.364 5.636a9 9 0 010 12.728M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-4.707C10.923 3.663 12 4.109 12 5v14c0 .891-1.077 1.337-1.707.707L5.586 15z"
        />
      </svg>
    </button>
    <input
      type="range"
      min="0"
      max="100"
      v-model="localVolume"
      class="range range-xs range-primary"
      @input="updateVolume"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'

const props = defineProps<{
  volume: number
}>()

const emit = defineEmits<{
  'update:volume': [value: number]
}>()

const localVolume = ref(props.volume)
const previousVolume = ref(props.volume)

watch(() => props.volume, (newValue) => {
  localVolume.value = newValue
})

function updateVolume() {
  emit('update:volume', localVolume.value)
}

function toggleMute() {
  if (localVolume.value === 0) {
    localVolume.value = previousVolume.value
  } else {
    previousVolume.value = localVolume.value
    localVolume.value = 0
  }
  emit('update:volume', localVolume.value)
}
</script>

<style scoped>
.range::-webkit-slider-thumb {
  cursor: pointer;
}
</style>-