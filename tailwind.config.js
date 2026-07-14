/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./src/**/*.{html,js,svelte,ts}",
    "./node_modules/flowbite-svelte/**/*.{html,js,svelte,ts}"
  ],
  plugins: [
    require('flowbite/plugin'),
    require('@tailwindcss/typography'),
  ],
  darkMode: 'class',
  theme: {
    extend: {
      borderRadius: {
        none: '0',
        sm: '0',
        DEFAULT: '0',
        md: '0',
        lg: '0',
        xl: '0',
        '2xl': '0',
        '3xl': '0',
        full: '0',
      },
      boxShadow: {
        hard: '4px 4px 0 #f59e0b',
        'hard-blue': '4px 4px 0 #3b82f6',
        'hard-dim': '3px 3px 0 rgba(241,245,249,0.12)',
      },
      typography: {
        DEFAULT: {
          css: {
            maxWidth: '65ch',
            color: 'inherit',
            a: {
              color: '#f59e0b',
              '&:hover': {
                color: '#fbbf24',
              },
            },
            h1: {
              color: '#f1f5f9',
              fontFamily: 'Inter, system-ui, sans-serif',
            },
            h2: {
              color: '#f1f5f9',
              fontFamily: 'Inter, system-ui, sans-serif',
            },
            h3: {
              color: '#e2e8f0',
              fontFamily: 'Inter, system-ui, sans-serif',
            },
            h4: {
              color: '#e2e8f0',
              fontFamily: 'Inter, system-ui, sans-serif',
            },
          },
        },
      },
      colors: {
        // Aligned with theme.css amber palette
        primary: {
          50: '#fffbeb',
          100: '#fef3c7',
          200: '#fde68a',
          300: '#fcd34d',
          400: '#fbbf24',
          500: '#f59e0b',
          600: '#d97706',
          700: '#b45309',
          800: '#92400e',
          900: '#78350f'
        }
      }
    }
  }
}
