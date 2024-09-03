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
      typography: {
        DEFAULT: {
          css: {
            maxWidth: '65ch',
            color: 'inherit',
            a: {
              color: '#ff7708',
              '&:hover': {
                color: '#ff9933',
              },
            },
            h1: {
              color: '#ff7708',
              fontFamily: 'Orbitron, sans-serif',
            },
            h2: {
              color: '#ff7708',
              fontFamily: 'Orbitron, sans-serif',
            },
            h3: {
              color: '#ff7708',
              fontFamily: 'Orbitron, sans-serif',
            },
            h4: {
              color: '#ff7708',
              fontFamily: 'Orbitron, sans-serif',
            },
            // ... you can add more specific styles here
          },
        },
      },
      colors: {
        // flowbite-svelte
        primary: {
          50: '#FFF5F2',
          100: '#FFF1EE',
          200: '#FFE4DE',
          300: '#FFD5CC',
          400: '#FFBCAD',
          500: '#FE795D',
          600: '#EF562F',
          700: '#EB4F27',
          800: '#CC4522',
          900: '#A5371B'
        }
      }
    }
  }
}