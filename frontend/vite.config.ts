import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { resolve } from 'path'

// Output to Django's static dir
export default defineConfig({
  plugins: [react()],
  root: '.',
  base: '/static/frontend/',
  build: {
    outDir: resolve(__dirname, '../core/static/frontend'),
    emptyOutDir: true,
    manifest: false,
    rollupOptions: {
      input: resolve(__dirname, 'src/main.tsx'),
      output: {
        entryFileNames: 'assets/main.js',
        chunkFileNames: 'assets/[name].js',
        assetFileNames: 'assets/[name][extname]'
      }
    }
  },
  server: {
    port: 5173,
    strictPort: true
  }
})


