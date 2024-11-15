<template>
  <div class="min-h-screen bg-base-200">
    <!-- Loading State -->
    <div v-if="isLoading" class="flex justify-center items-center min-h-screen">
      <span class="loading loading-spinner loading-lg"></span>
    </div>
 
    <!-- Main Content -->
    <div v-else class="container mx-auto p-8">
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <!-- Left Column: User Profile -->
        <div class="lg:col-span-1">
          <UserProfile :user="user" :stats="userStats" />
        </div>
 
        <!-- Middle Column -->
        <div class="lg:col-span-2 flex flex-col">
          <!-- Spotify Player Section -->
          <div class="w-full card bg-base-100 shadow-xl mb-8">
            <div class="card-body">
              <h2 class="card-title text-spotify-green text-xl mb-4">Music Player</h2>
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
 
          <!-- Active Session -->
          <div class="w-full card bg-base-100 shadow-xl mb-8">
            <div class="card-body">
              <div class="flex justify-between items-center mb-4">
                <h2 class="card-title text-spotify-green text-xl">
                  {{ currentSession?.name || "No Active Session" }}
                  <div v-if="currentSession" class="badge badge-secondary">
                    LIVE
                  </div>
                </h2>
                <div v-if="currentSession" class="dropdown dropdown-end">
                  <label tabindex="0" class="btn btn-ghost btn-circle">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 5v.01M12 12v.01M12 19v.01M12 6a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2z" />
                    </svg>
                  </label>
                  <ul tabindex="0" class="dropdown-content z-[1] menu p-2 shadow bg-base-100 rounded-box w-52">
                    <li><a @click="copySessionCode">Copy Session Code</a></li>
                    <li><a @click="() => handleLeaveSession()">Leave Session</a></li>
                    <li v-if="isHost"><a class="text-error" @click="endSession">End Session</a></li>
                  </ul>
                </div>
              </div>
 
              <div v-if="currentSession" class="space-y-6">
                <SessionParticipants :participants="currentSession.participants" />
              </div>
              <div v-else class="text-center py-8 text-base-content/70">
                Create or join a session to start listening with friends
              </div>
            </div>
          </div>
 
          <!-- Session Actions -->
          <div class="w-full max-w-2xl mx-auto mb-8">
            <SessionActions
              @create-session="createSession"
              @join-session="joinSession"
            />
          </div>
 
          <!-- Recent Sessions -->
          <div class="w-full">
            <RecentSessions
              :sessions="recentSessions"
              @join-session="joinExistingSession"
              @leave-session="handleLeaveSession"
              @delete-session="deleteSession"
            />
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
import { ref, computed, onMounted } from "vue";
import type { Session, User, UserStats } from "~/types";
import SpotifyPlayer from "~/components/SpotifyPlayer.vue";
import SessionParticipants from "~/components/SessionParticipants.vue";
import SessionActions from "~/components/SessionActions.vue";
import RecentSessions from "~/components/RecentSessions.vue";

// State
const isLoading = ref(true);
const user = ref<User | null>(null);
const userStats = ref<UserStats | null>(null);
const currentSession = ref<Session | null>(null);
const recentSessions = ref<Session[]>([]);
const spotifyToken = ref("");
const toast = ref<{
  type: "info" | "success" | "error";
  message: string;
} | null>(null);

// Computed
const isHost = computed(() => {
  return currentSession.value?.hostId === user.value?.id;
});

// Session Management Functions
async function copySessionCode() {
  if (currentSession.value?.code) {
    try {
      await navigator.clipboard.writeText(currentSession.value.code);
      showToast("success", "Session code copied to clipboard");
    } catch (e) {
      showToast("error", "Failed to copy session code");
    }
  }
}

async function handleLeaveSession(sessionId?: string) {
  const id = sessionId || currentSession.value?.id;
  if (!id) return;

  try {
    const response = await fetch(`http://localhost:8000/sessions/${id}/leave`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
    });

    if (response.ok) {
      if (id === currentSession.value?.id) {
        currentSession.value = null;
      }
      await fetchRecentSessions();
      showToast("success", "Left session successfully");
    } else {
      throw new Error("Failed to leave session");
    }
  } catch (e) {
    console.error("Leave session error:", e);
    showToast("error", "Failed to leave session");
  }
}

async function createSession(data: {
  name: string;
  privacy: "public" | "private";
}) {
  try {
    console.log("Creating session with data:", data);
    const response = await fetch("http://localhost:8000/sessions", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });

    console.log("Response status:", response.status);
    const responseData = await response.json();
    console.log("Response data:", responseData);

    if (response.ok) {
      currentSession.value = responseData;
      await fetchRecentSessions();
      showToast("success", "Session created successfully");
    } else {
      throw new Error(responseData.message || "Failed to create session");
    }
  } catch (e) {
    console.error("Create session error:", e);
    showToast("error", "Failed to create session");
  }
}

async function endSession() {
  if (!currentSession.value?.id) return;

  try {
    const response = await fetch(
      `http://localhost:8000/sessions/${currentSession.value.id}`,
      {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
        },
      }
    );

    if (response.ok) {
      currentSession.value = null;
      await fetchRecentSessions();
      showToast("success", "Session ended successfully");
    } else {
      throw new Error("Failed to end session");
    }
  } catch (e) {
    console.error("End session error:", e);
    showToast("error", "Failed to end session");
  }
}

async function joinSession(data: { code: string }) {
  try {
    console.log("Joining session with code:", data.code);
    const response = await fetch(`http://localhost:8000/sessions/join`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });

    if (response.ok) {
      const session = await response.json();
      currentSession.value = session;
      showToast("success", "Joined session successfully");
    } else {
      throw new Error("Failed to join session");
    }
  } catch (e) {
    console.error("Join session error:", e);
    showToast("error", "Failed to join session");
  }
}

async function joinExistingSession(sessionId: string) {
  try {
    const response = await fetch(
      `http://localhost:8000/sessions/${sessionId}/join`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
      }
    );

    if (response.ok) {
      const session = await response.json();
      currentSession.value = session;
      showToast("success", "Joined session successfully");
    } else {
      throw new Error("Failed to join existing session");
    }
  } catch (e) {
    console.error("Join existing session error:", e);
    showToast("error", "Failed to join session");
  }
}

async function deleteSession(sessionId: string) {
  try {
    const response = await fetch(`http://localhost:8000/sessions/${sessionId}`, {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
      },
    });

    if (response.ok) {
      await fetchRecentSessions();
      showToast("success", "Session deleted successfully");
    } else {
      throw new Error("Failed to delete session");
    }
  } catch (e) {
    console.error("Delete session error:", e);
    showToast("error", "Failed to delete session");
  }
}

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
async function fetchUser() {
  try {
    const response = await fetch("http://localhost:8000/me");
    console.log("User response:", response.status);
    if (response.ok) {
      user.value = await response.json();
      console.log("User data:", user.value);
    } else {
      throw new Error("Failed to fetch user");
    }
  } catch (e) {
    console.error("Fetch user error:", e);
  }
}

async function fetchUserStats() {
  try {
    const response = await fetch("http://localhost:8000/me/stats");
    console.log("Stats response:", response.status);
    if (response.ok) {
      userStats.value = await response.json();
      console.log("Stats data:", userStats.value);
    } else {
      throw new Error("Failed to fetch user stats");
    }
  } catch (e) {
    console.error("Fetch stats error:", e);
  }
}

async function fetchRecentSessions() {
  try {
    const response = await fetch("http://localhost:8000/sessions/recent");
    console.log("Recent sessions response:", response.status);
    if (response.ok) {
      recentSessions.value = await response.json();
      console.log("Recent sessions data:", recentSessions.value);
    } else {
      throw new Error("Failed to fetch recent sessions");
    }
  } catch (e) {
    console.error("Fetch recent sessions error:", e);
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
    await Promise.all([
      fetchUser(),
      fetchUserStats(),
      fetchRecentSessions(),
      fetchSpotifyToken(),
    ]);
  } catch (e) {
    console.error("Initial data load error:", e);
    showToast("error", "Failed to load some data");
  } finally {
    isLoading.value = false;
  }
});
</script>