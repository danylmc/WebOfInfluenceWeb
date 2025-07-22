import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

/* using ngrok free version */
/* export default defineConfig({
  plugins: [react()],
  server: {
    host: true, // needed to accept external connections
    port: 5173,
    allowedHosts: ['.ngrok-free.app'] // ✅ Allow any hostname for ngrok
  }
}) */

/* using github pages */
export default defineConfig({
  base: '/WebOfInfluenceResearch/',
  plugins: [react()],
})
