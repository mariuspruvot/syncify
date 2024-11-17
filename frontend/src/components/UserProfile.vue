<!-- components/UserProfile.vue -->

<template>
  <div class="card bg-base-100 shadow-xl w-full max-w-md mx-auto">
    <div class="card-body items-center text-center p-4 sm:p-6 md:p-8">
      <div class="avatar">
        <div class="w-16 sm:w-20 md:w-24 rounded-full ring ring-primary ring-offset-base-100 ring-offset-2">
          <img 
            :src="user?.avatar || 'https://via.placeholder.com/96'" 
            :alt="user?.display_name"
            class="w-full h-full object-cover"
          />
        </div>
      </div>

      <h2 class="card-title text-lg sm:text-xl md:text-2xl mt-2 sm:mt-3 md:mt-4">
        {{ user?.display_name }}
      </h2>
      <p class="text-xs sm:text-sm opacity-70">{{ user?.country }}</p>

      <div class="stats shadow-lg mt-4 sm:mt-5 md:mt-6 w-full grid grid-cols-2">
        <div class="stat text-center p-2 sm:p-3 md:p-4">
          <div class="stat-title text-[10px] sm:text-xs md:text-sm whitespace-nowrap overflow-hidden text-ellipsis">
            Active Sessions
          </div>
          <div class="stat-value text-lg sm:text-xl md:text-2xl">
            {{ stats?.activeSessions || 0 }}
          </div>
        </div>
        <div class="stat text-center p-2 sm:p-3 md:p-4">
          <div class="stat-title text-[10px] sm:text-xs md:text-sm whitespace-nowrap overflow-hidden text-ellipsis">
            Online Friends
          </div>
          <div class="stat-value text-lg sm:text-xl md:text-2xl">
            {{ stats?.onlineFriends || 0 }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
  
  <script setup lang="ts">
  import type { User, UserStats } from '~/types'
  
  defineProps<{
    user: User | null
    stats: UserStats | null
  }>()
  </script>