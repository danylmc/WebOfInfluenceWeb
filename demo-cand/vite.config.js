import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    host: true, // needed to accept external connections
    port: 5173,
    allowedHosts: [
      '619b-2404-440c-2302-8f00-b533-7844-25e5-31b4.ngrok-free.app' //ngrok hostname
    ]
  }
})