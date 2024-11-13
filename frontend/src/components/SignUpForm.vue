<template>
  <div class="flex items-center justify-center min-h-screen bg-base-200 p-12">
    <!-- Loader Component -->
    <div
      class="absolute inset-0 flex items-center justify-center bg-opacity-50 bg-base-300"
      v-if="isLoading"
    >
      <Loader />
    </div>

    <!-- Card for Signup Form -->
    <div class="card w-96 bg-base-100 shadow-xl">
      <div class="card-body">
        <h2 class="card-title text-2xl font-bold mb-6 text-center">Sign Up</h2>
        <form @submit.prevent="handleSubmit">
          <!-- Name Field -->
          <div class="form-control mb-4">
            <label class="label">
              <span class="label-text">First Name</span>
            </label>
            <input
              type="text"
              class="input input-bordered"
              placeholder="John"
              v-model="firstName"
              required
            />
          </div>
          <div class="form-control mb-4">
            <label class="label">
              <span class="label-text">Last Name</span>
            </label>
            <input
              type="text"
              class="input input-bordered"
              placeholder="Doe"
              v-model="lastName"
              required
            />
          </div>

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
          </div>

          <!-- Confirm Password Field -->
          <div class="form-control mb-4">
            <label class="label">
              <span class="label-text">Confirm Password</span>
            </label>
            <input
              type="password"
              class="input input-bordered"
              placeholder="Confirm your password"
              v-model="confirmPassword"
              required
            />
            <label class="label">
              <span
                class="label-text-alt text-red-500"
                v-if="password !== confirmPassword"
              >
                Passwords do not match
              </span>
            </label>
          </div>

          <!-- Date of Birth Field -->
          <div class="form-control mb-4">
            <label class="label">
              <span class="label-text">Date of Birth</span>
            </label>
            <input
              type="date"
              class="input input-bordered"
              v-model="dob"
              required
            />
          </div>

          <!-- Address Field -->
          <div class="form-control mb-4">
            <label class="label">
              <span class="label-text">Address</span>
            </label>
            <textarea
              class="textarea textarea-bordered"
              placeholder="Enter your address"
              v-model="address"
              required
            ></textarea>
          </div>

          <!-- Terms and Conditions Checkbox -->
          <div class="form-control mb-4">
            <label class="label cursor-pointer">
              <input
                type="checkbox"
                class="checkbox"
                v-model="acceptTerms"
                required
              />
              <span class="label-text ml-2"
                >I agree to the terms and conditions</span
              >
            </label>
          </div>

          <!-- Submit Button -->
          <div class="form-control mt-6">
            <button
              class="btn bg-spotify-green text-white hover:bg-green-700"
              type="submit"
            >
              Sign Up
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import Loader from "@/components/Loader.vue"; // Importing the Loader component

export default {
  components: {
    Loader, // Registering the Loader component
  },
  data() {
    return {
      firstName: "",
      lastName: "",
      email: "",
      password: "",
      confirmPassword: "",
      dob: "",
      address: "",
      acceptTerms: false,
      isLoading: false,
      isSuccess: false,
    };
  },
  methods: {
    async handleSubmit() {
      if (this.password !== this.confirmPassword) {
        console.log("Passwords do not match");
        return;
      }
      this.isLoading = true;

      try {
        const formData = {
          firstName: this.firstName,
          lastName: this.lastName,
          email: this.email,
          password: this.password,
          dob: this.dob,
          address: this.address,
          acceptTerms: this.acceptTerms,
        };

        const response = await fetch("/api/signup", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(formData),
        });

        if (response.ok) {
          this.isSuccess = true;
          this.$router.push("/cards"); // Redirect to the "cards" page after successful signup
        } else {
          this.isSuccess = false;
          alert("Signup failed! Please try again.");
        }
      } catch (error) {
        console.error("Error submitting form:", error);
        alert("An error occurred! Please try again.");
      } finally {
        this.isLoading = false;
      }
    },
  },
};
</script>

<style scoped>
/* Custom styles for the form */
</style>
