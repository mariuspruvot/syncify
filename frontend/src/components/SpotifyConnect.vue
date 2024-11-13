<template>
  <div class="flex items-center justify-center min-h-screen bg-base-200 p-12">
    <!-- Card for Signup Form -->
    <div class="card w-96 bg-base-100 shadow-xl">
      <div class="card-body flex flex-col items-center text-center">
        <h2 class="card-title text-2xl font-bold mb-6 text-spotify-green">
          Connect Spotify
        </h2>

        <!-- Left-aligned text content -->
        <div class="w-full mb-6">
          <p class="text-left text-base-content">
            Syncify uses your Spotify account to access your music library and
            playlists. Connect your Spotify account to get started.
          </p>
        </div>

        <button
          class="btn btn-primary bg-spotify-green text-white hover:bg-green-700 mt-6"
          @click="connectSpotify"
        >
          Connect Spotify
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
const spotifyAuthUrl = `http://localhost:8000/spotify/authorize`;

function connectSpotify() {
  window.location.href = spotifyAuthUrl;
}
</script>
