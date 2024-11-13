<template>
  <div class="flex items-center justify-center min-h-screen bg-base-200">
    <div class="card w-96 bg-base-100 shadow-xl">
      <div class="card-body">
        <h2 class="card-title text-2xl font-bold mb-6 text-center">Login</h2>
        <form @submit.prevent="handleSubmit">
          <!-- Email Field -->
          <div class="form-control mb-4">
            <label class="label">
              <span class="label-text">Email</span>
            </label>
            <input
              type="email"
              class="input input-bordered"
              placeholder="email@example.com"
              v-model="email"
              required
            />
          </div>

          <!-- Password Field -->
          <div class="form-control mb-4">
            <label class="label">
              <span class="label-text">Password</span>
            </label>
            <input
              type="password"
              class="input input-bordered"
              placeholder="Enter password"
              v-model="password"
              required
            />
            <label class="label">
              <a href="#" class="label-text-alt link link-hover"
                >Forgot password?</a
              >
            </label>
          </div>

          <!-- Submit Button -->
          <div class="form-control mt-6">
            <button class="btn bg-spotify-green text-white hover:bg-green-700">
              Login
            </button>
          </div>

          <!-- Divider -->
          <div class="divider">OR</div>

          <!-- Sign Up Link -->
          <div class="text-center">
            <p>Don't have an account?</p>
            <NuxtLink to="/signup" class="link link-primary text-spotify-green"
              >Sign up</NuxtLink
            >
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      email: "",
      password: "",
    };
  },
  methods: {
    handleSubmit() {
      // Gérer la soumission du formulaire
      console.log("Email:", this.email);
      console.log("Password:", this.password);
    },
  },
};
</script>

<style scoped>
/* Tailwind colors can be customized here */
</style>
