<template>
  <div class="hero bg-base-200 min-h-screen">
    <div class="hero-content text-center">
      <div class="max-w-md">
        <h1 class="text-5xl font-bold relative overflow-hidden">
          <span
            v-for="(letter, index) in letters"
            :key="index"
            :class="'letter letter-' + index"
          >
            {{ letter }}
          </span>
        </h1>
        <p class="py-4 text-spotify-green"></p>
        <nuxt-link to="/connect-spotify">
          <button
            class="btn bg-spotify-green text-white hover:bg-green-700 w-full mb-4 flex justify-center gap-4"
          >
            <img
              src="assets/spotify/logo.png"
              alt="Spotify logo"
              class="w-6 h-6"
            />
            Login with Spotify
          </button>
        </nuxt-link>
      </div>
    </div>
  </div>
</template>
<script>
export default {
  data() {
    return {
      letters: "Syncify".split(""),
    };
  },
};
</script>

<style scoped>
.letter {
  display: inline-block;
  font-size: 4rem; /* Taille des lettres */
  font-weight: normal; /* Suppression du style gras */
  font-variant-ligatures: common-ligatures;
  position: relative;
  opacity: 0;
  color: rgba(255, 255, 255, 0.664); /* Couleur initiale */
  transition: color 0.3s ease, transform 0.3s ease;
  animation: arrive 1.5s cubic-bezier(0.68, -0.55, 0.27, 1.55) forwards;
}

/* Couleur Spotify Green au hover */
.letter:hover {
  color: #1db954; /* Spotify Green */
  transform: scale(1.1); /* Légère mise en avant au hover */
}

/* Animation pour chaque lettre */
.letter-0 {
  animation-delay: 0s;
  transform: translate(-100vw, -100vh);
}
.letter-1 {
  animation-delay: 0.1s;
  transform: translate(100vw, -100vh);
}
.letter-2 {
  animation-delay: 0.2s;
  transform: translate(-100vw, 100vh);
}
.letter-3 {
  animation-delay: 0.3s;
  transform: translate(100vw, 100vh);
}
.letter-4 {
  animation-delay: 0.4s;
  transform: translate(-100vw, -100vh);
}
.letter-5 {
  animation-delay: 0.5s;
  transform: translate(100vw, -100vh);
}

/* Animation arrive */
@keyframes arrive {
  0% {
    opacity: 0;
    transform: translate(0, 0) scale(0.8);
  }
  70% {
    opacity: 1;
    transform: translate(0, 0) scale(1.2); /* Petit effet d'agrandissement avant de se stabiliser */
  }
  100% {
    opacity: 1;
    transform: translate(0, 0) scale(1);
  }
}
</style>
