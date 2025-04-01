import { fileURLToPath, URL } from 'node:url';
import tailwindcss from '@tailwindcss/vite';
import vue from '@vitejs/plugin-vue';
import { defineConfig } from 'vite';
import vueDevTools from 'vite-plugin-vue-devtools';
import svgLoader from 'vite-svg-loader';

// https://vite.dev/config/
export default defineConfig({
    server: {
        host: true,
        port: 5173,
        strictPort: true,
        watch: {
            usePolling: true,
            interval: 1000,
        },
        hmr: {
            clientPort: 5173,
        },
    },
    plugins: [vue(), vueDevTools(), tailwindcss(), svgLoader()],
    resolve: {
        alias: {
            '@': fileURLToPath(new URL('./src', import.meta.url)),
        },
    },
});
