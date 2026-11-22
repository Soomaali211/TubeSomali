import react from '@vitejs/plugin-react';
import { defineConfig } from 'vitest/config';

// Separate chunks per mode so the YouTube chunk can be checked for forbidden modules (AT-YT-03).
export default defineConfig({
  plugins: [react()],
  build: {
    rollupOptions: {
      output: {
        manualChunks(id: string) {
          if (id.includes('/src/modes/youtube/')) return 'mode-youtube';
          if (id.includes('/src/modes/authorized/')) return 'mode-authorized';
          return undefined;
        },
      },
    },
  },
  test: { environment: 'jsdom', include: ['tests/**/*.test.tsx'] },
});
