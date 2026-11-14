import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [
    react(),
    tailwindcss(),
  ],

  server: {
    port: Number(process.env.AEGIS_FRONTEND_PORT) || 5173,
    // Local machine only by default: the dev server proxies the API, and
    // the camera agent pairs on 127.0.0.1 anyway. Set AEGIS_DEV_HOST=0.0.0.0
    // to deliberately expose it on the local network.
    host: process.env.AEGIS_DEV_HOST || '127.0.0.1',
    strictPort: true,

    proxy: {
      '/api': {
        target: process.env.AEGIS_API_URL || 'http://127.0.0.1:8000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ''),
      },
    },
  },
})