/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./src/**/*.{vue,js,ts,jsx,tsx}", // Ensure Tailwind scans all the right files
  ],
  theme: {
    extend: {
      fontFamily: {
        "jetbrains-mono": ["JetBrains Mono", "monospace"], // Custom font
      },
      colors: {
        "spotify-green": "#1DB954", // Custom Spotify color
      },
    },
  },
  plugins: [
    require("daisyui"), // DaisyUI plugin for Tailwind
  ],
};
