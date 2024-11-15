<!-- components/RecentSessions.vue -->
<template>
    <div class="mt-6">
      <div class="flex justify-between items-center mb-4">
        <h3 class="text-lg font-bold">Recent Sessions</h3>
        <select v-model="filter" class="select select-sm select-bordered">
          <option value="all">All Sessions</option>
          <option value="active">Active</option>
          <option value="ended">Ended</option>
        </select>
      </div>
      
      <div class="overflow-x-auto">
        <table class="table">
          <thead>
            <tr>
              <th>Name</th>
              <th>Participants</th>
              <th>Duration</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="session in filteredSessions" :key="session.id">
              <td>
                <div class="font-bold">{{ session.name }}</div>
                <div class="text-sm opacity-50">{{ formatDate(new Date(session.startTime)) }}</div>
              </td>
              <td>
                <div class="avatar-group -space-x-4 rtl:space-x-reverse">
                  <div 
                    v-for="participant in session.participants.slice(0, 2)" 
                    :key="participant.id" 
                    class="avatar"
                  >
                    <div class="w-8">
                      <img :src="participant.avatar" :alt="participant.name" />
                    </div>
                  </div>
                  <div 
                    v-if="session.participants.length > 2" 
                    class="avatar placeholder"
                  >
                    <div class="w-8 bg-neutral text-neutral-content">
                      <span>+{{ session.participants.length - 2 }}</span>
                    </div>
                  </div>
                </div>
              </td>
              <td>{{ formatDuration(session.duration) }}</td>
              <td>
                <div 
                  :class="[
                    'badge',
                    session.status === 'active' ? 'badge-success' : 'badge-ghost'
                  ]"
                >
                  {{ session.status }}
                </div>
              </td>
              <td>
                <div class="flex gap-2">
                  <button 
                    v-if="session.status === 'active'"
                    class="btn btn-sm btn-primary"
                    @click="$emit('join-session', session.id)"
                  >
                    Join
                  </button>
                  <button 
                    v-if="session.status === 'active'"
                    class="btn btn-sm btn-ghost"
                    @click="$emit('leave-session', session.id)"
                  >
                    Leave
                  </button>
                  <button 
                    v-else
                    class="btn btn-sm btn-ghost"
                    @click="$emit('delete-session', session.id)"
                  >
                    Delete
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </template>
  
  <script setup lang="ts">
  import { ref, computed } from 'vue'
  import type { Session, Participant } from '~/types';
  const props = defineProps<{
    sessions: Session[]
  }>()
  
  const filter = ref<'all' | 'active' | 'ended'>('all')
  
  const filteredSessions = computed(() => {
    if (filter.value === 'all') return props.sessions
    return props.sessions.filter(session => session.status === filter.value)
  })
  
  function formatDate(date: Date): string {
    return new Intl.DateTimeFormat('en-US', {
      month: 'short',
      day: 'numeric',
      hour: 'numeric',
      minute: '2-digit'
    }).format(date)
  }
  
  function formatDuration(ms: number): string {
    const hours = Math.floor(ms / (1000 * 60 * 60))
    const minutes = Math.floor((ms % (1000 * 60 * 60)) / (1000 * 60))
    return `${hours}h ${minutes}m`
  }
  
  defineEmits<{
    'join-session': [id: string]
    'leave-session': [id: string]
    'delete-session': [id: string]
  }>()
  </script>