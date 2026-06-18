/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      fontFamily: {
        sans: ["Inter", "ui-sans-serif", "system-ui", "sans-serif"],
      },
      colors: {
        ink: "#080B12",
        panel: "rgba(14, 20, 32, 0.72)",
        line: "rgba(255,255,255,0.12)",
        mint: "#7EE7C4",
        coral: "#FF8A7A",
        gold: "#F4C95D",
        sky: "#7CB7FF",
      },
      boxShadow: {
        premium: "0 24px 80px rgba(0,0,0,0.38)",
      },
    },
  },
  plugins: [],
};
