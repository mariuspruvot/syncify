<template>
  <div class="navbar bg-base-100">
    <div class="flex-1">
      <NuxtLink class="hover:text-spotify-green btn btn-ghost text-xl" to="/">Syncify</NuxtLink>
    </div>
    
    <div class="flex-none">
      <!-- Menu burger pour mobile -->
      <div class="dropdown dropdown-end">
        <label tabindex="0" class="btn btn-ghost lg:hidden">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h8m-8 6h16" />
          </svg>
        </label>
        <ul tabindex="0" class="menu menu-sm dropdown-content mt-3 z-[1] p-2 shadow bg-base-100 rounded-box w-52">
          <li><NuxtLink to="/home" class="hover:text-spotify-green">Home</NuxtLink></li>
          <li><NuxtLink to="/about" class="hover:text-spotify-green">About</NuxtLink></li>
          <li><NuxtLink to="/information" class="hover:text-spotify-green">Information</NuxtLink></li>
          <li><NuxtLink to="/contact" class="hover:text-spotify-green">Contact</NuxtLink></li>
        </ul>
      </div>

      <!-- Menu normal pour desktop -->
      <ul class="menu menu-horizontal p-0 hidden lg:flex">
        <li>
          <NuxtLink to="/home" class="hover:text-spotify-green transition-colors duration-200">
            Home
          </NuxtLink>
        </li>
        <li>
          <NuxtLink to="/about" class="hover:text-spotify-green transition-colors duration-200">
            About
          </NuxtLink>
        </li>
        <li>
          <NuxtLink to="/information" class="hover:text-spotify-green transition-colors duration-200">
            Information
          </NuxtLink>
        </li>
        <li>
          <NuxtLink to="/contact" class="hover:text-spotify-green transition-colors duration-200">
            Contact
          </NuxtLink>
        </li>
      </ul>
    </div>
  </div>
</template>
