import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  build: {
    // Enable minification
    minify: 'terser',
    terserOptions: {
      compress: {
        drop_console: true, // Remove console.log in production
        drop_debugger: true,
      },
    },
    // Code splitting configuration
    rollupOptions: {
      output: {
        manualChunks: {
          // Separate React vendor bundle
          'react-vendor': ['react', 'react-dom'],
          // Separate Three.js bundle (largest dependency)
          'three-vendor': ['three', '@react-three/fiber', '@react-three/drei'],
          // Separate charts bundle
          'charts': ['recharts'],
          // Separate icons
          'icons': ['lucide-react'],
        },
      },
    },
    // Performance hints
    chunkSizeWarningLimit: 500,
    // Enable source maps for production debugging
    sourcemap: false,
  },
  // Optimize dependencies
  optimizeDeps: {
    include: ['react', 'react-dom', 'three'],
  },
  server: {
    proxy: {
      "/api": "http://localhost:8000",
      "/ws": {
        target: "ws://localhost:8000",
        ws: true,
      },
    },
  },
})

