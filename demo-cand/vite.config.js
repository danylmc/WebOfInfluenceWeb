import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    host: true, // needed to accept external connections
    port: 5173,
    allowedHosts: 'all' // ✅ Allow any hostname for ngrok
  }
})
