import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    host: true, // needed to accept external connections
    port: 5173,
    allowedHosts: [
      '3ca3-49-224-81-158.ngrok-free.ap' // 👈 your ngrok hostname
    ]
  }
})