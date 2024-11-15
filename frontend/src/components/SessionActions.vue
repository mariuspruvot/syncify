<!-- components/SessionActions.vue -->
<template>
    <div class="space-y-4">
      <!-- Quick Actions -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <button 
          class="btn btn-primary btn-lg"
          @click="showCreateModal = true"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
          </svg>
          Create New Session
        </button>
        <button 
          class="btn btn-secondary btn-lg"
          @click="showJoinModal = true"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
          </svg>
          Join Session
        </button>
      </div>
  
      <!-- Create Session Modal -->
      <dialog :class="{ 'modal': true, 'modal-open': showCreateModal }">
        <div class="modal-box">
          <h3 class="font-bold text-lg">Create New Session</h3>
          <div class="form-control w-full">
            <label class="label">
              <span class="label-text">Session Name</span>
            </label>
            <input 
              v-model="newSessionName"
              type="text" 
              placeholder="My Awesome Session" 
              class="input input-bordered w-full"
            />
          </div>
          <div class="form-control w-full mt-4">
            <label class="label">
              <span class="label-text">Privacy</span>
            </label>
            <select v-model="sessionPrivacy" class="select select-bordered w-full">
              <option value="public">Public</option>
              <option value="private">Private</option>
            </select>
          </div>
          <div class="modal-action">
            <button class="btn" @click="showCreateModal = false">Cancel</button>
            <button 
              class="btn btn-primary" 
              :disabled="!newSessionName"
              @click="createSession"
            >
              Create
            </button>
          </div>
        </div>
        <form method="dialog" class="modal-backdrop">
          <button @click="showCreateModal = false">close</button>
        </form>
      </dialog>
  
      <!-- Join Session Modal -->
      <dialog :class="{ 'modal': true, 'modal-open': showJoinModal }">
        <div class="modal-box">
          <h3 class="font-bold text-lg">Join Session</h3>
          <div class="form-control w-full">
            <label class="label">
              <span class="label-text">Session Code</span>
            </label>
            <input 
              v-model="sessionCode"
              type="text" 
              placeholder="Enter session code" 
              class="input input-bordered w-full"
            />
          </div>
          <div class="modal-action">
            <button class="btn" @click="showJoinModal = false">Cancel</button>
            <button 
              class="btn btn-primary" 
              :disabled="!sessionCode"
              @click="joinSession"
            >
              Join
            </button>
          </div>
        </div>
        <form method="dialog" class="modal-backdrop">
          <button @click="showJoinModal = false">close</button>
        </form>
      </dialog>
    </div>
  </template>
  
  <script setup lang="ts">
  import { ref } from 'vue'
  
  const showCreateModal = ref(false)
  const showJoinModal = ref(false)
  const newSessionName = ref('')
  const sessionPrivacy = ref('public')
  const sessionCode = ref('')
  
  const emit = defineEmits<{
    'create-session': [{ name: string, privacy: 'public' | 'private' }]
    'join-session': [{ code: string }]
  }>()
  
  async function createSession() {
    emit('create-session', {
      name: newSessionName.value,
      privacy: sessionPrivacy.value as 'public' | 'private'
    })
    showCreateModal.value = false
    newSessionName.value = ''
    sessionPrivacy.value = 'public'
  }
  
  async function joinSession() {
    emit('join-session', { code: sessionCode.value })
    showJoinModal.value = false
    sessionCode.value = ''
  }
  </script>