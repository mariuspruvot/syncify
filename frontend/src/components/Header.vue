<template>
  <div class="navbar bg-base-100">
    <div class="flex-1">
      <NuxtLink class="btn btn-ghost text-xl" to="/">Syncify</NuxtLink>
    </div>
    <div class="flex-none">
      <ul class="menu menu-horizontal p-0">
        <li>
          <NuxtLink
            to="/home"
            class="hover:text-spotify-green transition-colors duration-200"
            >Home</NuxtLink
          >
        </li>
        <li>
          <NuxtLink
            to="/about"
            class="hover:text-spotify-green transition-colors duration-200"
            >About</NuxtLink
          >
        </li>
        <li>
          <NuxtLink
            to="/information"
            class="hover:text-spotify-green transition-colors duration-200"
            >Information</NuxtLink
          >
        </li>
        <li>
          <NuxtLink
            to="/contact"
            class="hover:text-spotify-green transition-colors duration-200"
            >Contact</NuxtLink
          >
        </li>
      </ul>
    </div>
  </div>
</template>
