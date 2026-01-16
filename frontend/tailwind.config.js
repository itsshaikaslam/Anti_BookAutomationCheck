/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        neo: {
          yellow: '#FFDD00',
          pink: '#FF00FF',
          cyan: '#00FFFF',
          black: '#000000',
          white: '#FFFFFF',
          gray: '#EEEEEE',
        }
      },
      boxShadow: {
        neo: '6px 6px 0px 0px #000000',
        'neo-sm': '4px 4px 0px 0px #000000',
        'neo-lg': '10px 10px 0px 0px #000000',
      },
      borderWidth: {
        '4': '4px',
        '8': '8px',
      }
    },
  },
  plugins: [],
}
