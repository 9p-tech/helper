/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
        heading: ['Montserrat', 'sans-serif'],
      },
      colors: {
        snitch: {
          black: '#000000',
          white: '#FFFFFF',
          surface: '#F9F9F9',
          border: '#E5E5E5',
          muted: '#737373',
          red: '#D93025',
        }
      },
      spacing: {
        base: '4px',
        xs: '8px',
        sm: '16px',
        md: '24px',
        lg: '48px',
        xl: '80px',
      },
      borderRadius: {
        none: '0px',
        sm: '2px',
      }
    },
  },
  plugins: [],
}
