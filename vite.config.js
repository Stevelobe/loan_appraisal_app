import { defineConfig } from 'vite'
import tailwindcss from '@tailwindcss/vite'
export default defineConfig({
   server: {
    host: '0.0.0.0', // or use your specific local IP like '192.168.x.x'
    port: 5173,       // Ensure this matches the port you're using
  },
  plugins: [
    tailwindcss(),
  ],
})