import type { Config } from 'tailwindcss';

export default {
  content: ['./app/**/*.{ts,tsx}', './components/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        bg: '#0b0f17',
        panel: '#151b26',
        text: '#e5e7eb',
        ok: '#22c55e',
        warn: '#eab308',
        risk: '#ef4444'
      }
    }
  },
  plugins: []
} satisfies Config;
