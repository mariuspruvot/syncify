// src/router.ts
import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'

const routes: RouteRecordRaw[] = [
  {
    path: '/connect-spotify',
    name: 'ConnectSpotify',
    component: () => import('./pages/connect-spotify.vue')
  },
  {
    path: '/auth-success',
    name: 'AuthSuccess',
    component: () => import('./pages/auth-success.vue')
  }
  // ... your other routes
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router