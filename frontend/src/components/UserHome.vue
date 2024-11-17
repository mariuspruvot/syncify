<template>
  <div class="min-h-screen bg-base-200">
    <!-- Loading State -->
    <div v-if="isLoading" class="flex justify-center items-center min-h-screen">
      <span class="loading loading-spinner loading-lg"></span>
    </div>
 
    <!-- Main Content -->
    <div v-else class="container mx-auto p-8">
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <!-- Left Column: User Profile & Friends -->
        <div class="lg:col-span-1 flex flex-col gap-8">
          <!-- User Profile -->
          <UserProfile :user="user" :stats="userStats" />
          
          <!-- Friends List -->
          <FriendsList />
        </div>
 
        <!-- Right Column: Player & Activity -->
        <div class="lg:col-span-2 flex flex-col gap-8">
          <!-- Spotify Player Section -->
          <div class="w-full card bg-base-100 shadow-xl">
            <div class="card-body">
              <div class="flex justify-between items-center">
                <h2 class="card-title text-spotify-green text-xl">Now Playing</h2>
                <div class="badge badge-primary">LIVE</div>
              </div>
              <SpotifyPlayer
                v-if="!isLoading && spotifyToken"
                :token="spotifyToken"
                @player-error="handlePlayerError"
              />
              <div v-else-if="isLoading" class="text-center py-4">
                <span class="loading loading-spinner loading-md"></span>
              </div>
              <div v-else class="text-center py-4 text-base-content/70">
                Unable to load Spotify Player
              </div>
            </div>
          </div>

          <!-- Listening Activity -->
          <div class="w-full card bg-base-100 shadow-xl">
            <div class="card-body">
              <h2 class="card-title text-spotify-green text-xl mb-4">
                Friend Activity
              </h2>
              <div class="space-y-4">
                <!-- We'll add friend activity here later -->
                <div class="text-center py-4 text-base-content/70">
                  See what your friends are listening to
                </div>
              </div>
            </div>
          </div>

          <!-- Recently Played Together -->
          <div class="w-full card bg-base-100 shadow-xl">
            <div class="card-body">
              <h2 class="card-title text-spotify-green text-xl mb-4">
                Recently Played Together
              </h2>
              <div class="space-y-4">
                <!-- We'll add shared listening history here -->
                <div class="text-center py-4 text-base-content/70">
                  No recent shared sessions
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
 
    <!-- Toast Messages -->
    <div class="toast toast-end">
      <div v-if="toast" :class="['alert', `alert-${toast.type}`]">
        <span>{{ toast.message }}</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import type { User, UserStats } from "~/types";
import SpotifyPlayer from "~/components/SpotifyPlayer.vue";
import UserProfile from "./UserProfile.vue";
import FriendsList from "./FriendsList.vue";

// State
const isLoading = ref(false);
const user = ref<User | null>(null); 
const userStats = ref<UserStats | null>(null);
const spotifyToken = ref("");
const toast = ref<{
  type: "info" | "success" | "error";
  message: string;
} | null>(null);



// Error Handling
function handlePlayerError(error: Error) {
  console.error("Spotify player error:", error);
  showToast("error", error.message);
}

// Utils
function showToast(type: "success" | "error" | "info", message: string) {
  toast.value = { type, message };
  setTimeout(() => {
    toast.value = null;
  }, 3000);
}

// Data Fetching
async function initializeUser() {
  try {
    const spotifyToken = localStorage.getItem('spotify_token');
    
    if (!spotifyToken) {
      throw new Error('No Spotify token found');
    }

    // Ajoutons un log ici pour voir la structure des données
    const spotifyUserResponse = await fetch(`http://localhost:8000/spotify/user?token=${spotifyToken}`);
    if (!spotifyUserResponse.ok) {
      throw new Error('Failed to fetch Spotify user data');
    }

    const spotifyUserData = await spotifyUserResponse.json();
    console.log('Spotify User Data:', spotifyUserData);

    try {
      const verifyResponse = await fetch(`http://localhost:8000/app-auth/verify/${spotifyUserData.id}`);
      if (verifyResponse.ok) {
        const userData = await verifyResponse.json();
        localStorage.setItem('user_id', userData.id);
        return userData;
      }
    } catch (error) {
      console.warn('User verification failed, proceeding with registration');
    }

    // Si l'utilisateur n'existe pas, l'enregistrer
    const registerResponse = await fetch('http://localhost:8000/app-auth/register', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        spotify_id: spotifyUserData.id,
        email: spotifyUserData.email,
        display_name: spotifyUserData.display_name,
        avatar: spotifyUserData.images?.[0]?.url || null,
        country: spotifyUserData.country,
      }),
    });

    if (!registerResponse.ok) {
      throw new Error('Failed to register user');
    }

    const registeredUser = await registerResponse.json();
    localStorage.setItem('user_id', registeredUser.id);
    return registeredUser;

  } catch (error) {
    console.error('Failed to initialize user:', error);
    showToast('error', 'Failed to initialize user');
    throw error;
  }
}

async function fetchSpotifyToken() {
  try {
    const response = await fetch("http://localhost:8000/spotify/token");
    console.log("Spotify token response:", response.status);
    if (response.ok) {
      const data = await response.json();
      console.log("Spotify token data:", data);
      if (data.status === "ok" && data.token) {
        spotifyToken.value = data.token;
      } else {
        throw new Error("Invalid token response");
      }
    } else {
      throw new Error("Failed to fetch Spotify token");
    }
  } catch (e) {
    console.error("Fetch Spotify token error:", e);
  }
}

// Lifecycle Hooks
onMounted(async () => {
  try {
    isLoading.value = true;
    const userData = await initializeUser();
    console.log('User Data:', userData);
    user.value = userData;
    
    if (userData) {
      await fetchSpotifyToken();
    }
  } catch (error) {
    console.error('Initialization error:', error);
  } finally {
    isLoading.value = false;
  }
});
</script>