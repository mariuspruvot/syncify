<!-- components/SessionParticipants.vue -->
<template>
    <div class="flex gap-2 my-4">
      <div class="avatar-group -space-x-6 rtl:space-x-reverse">
        <div v-for="participant in visibleParticipants" :key="participant.id" class="avatar">
          <div class="w-12">
            <img 
              :src="participant.avatar" 
              :alt="participant.name"
              :title="participant.name"
            />
            <div v-if="participant.isHost" class="absolute -top-1 -right-1 badge badge-primary badge-xs"></div>
          </div>
        </div>
        <div v-if="remainingCount > 0" class="avatar placeholder">
          <div class="w-12 bg-neutral text-neutral-content">
            <span>+{{ remainingCount }}</span>
          </div>
        </div>
      </div>
  
      <div class="dropdown dropdown-end ml-2">
        <label tabindex="0" class="btn btn-circle btn-sm btn-ghost">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
            <path d="M6 10a2 2 0 11-4 0 2 2 0 014 0zM12 10a2 2 0 11-4 0 2 2 0 014 0zM16 12a2 2 0 100-4 2 2 0 000 4z" />
          </svg>
        </label>
        <ul tabindex="0" class="dropdown-content z-[1] menu p-2 shadow bg-base-100 rounded-box w-52">
          <li v-for="participant in participants" :key="participant.id">
            <a class="flex justify-between">
              <span>{{ participant.name }}</span>
              <span v-if="participant.isHost" class="badge badge-primary badge-sm">Host</span>
            </a>
          </li>
        </ul>
      </div>
    </div>
  </template>
  
  <script setup lang="ts">
  import { computed } from 'vue'
  import type { Participant } from '~/types';
  
  const props = defineProps<{
    participants: Participant[]
  }>()
  
  const MAX_VISIBLE = 3
  
  const visibleParticipants = computed(() => 
    props.participants.slice(0, MAX_VISIBLE)
  )
  
  const remainingCount = computed(() => 
    Math.max(0, props.participants.length - MAX_VISIBLE)
  )
  </script>