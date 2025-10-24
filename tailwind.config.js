/** @type {import('tailwindcss').Config} */
export const content = [
    // Add your file paths here to let Tailwind know which files to scan for classes.
    // Example for a React project:
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
];
export const theme = {
    extend: {
        // 1. Define the custom keyframes (the animation steps)
        keyframes: {
            'pan-background': {
                '0%': { 'background-position': '0% 0%' },
                '100%': { 'background-position': '100% 100%' },
            },
        },
        // 2. Define the custom animation utility (how the steps are played)
        animation: {
            // Class name: 'animate-pan-background'
            // Animation: [keyframes-name] [duration] [iteration-count] [timing-function] [direction]
            'pan-background': 'pan-background 60s infinite linear alternate',
        },
    },
};
export const plugins = [];