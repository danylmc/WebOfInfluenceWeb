import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    host: true, // needed to accept external connections
    allowedHosts: [
      '3327-49-224-81-158.ngrok-free.app' // 👈 your ngrok hostname
    ]
  }
})