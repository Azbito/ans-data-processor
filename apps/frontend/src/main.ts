import App from '@/app.vue';
import { createApp } from 'vue';
import '@/assets/styles/global.css';
import router from '@/router';
import { createI18n } from 'vue-i18n';
import { translations } from './i18n';

const storedLanguage = localStorage.getItem('language');

const i18n = createI18n({
    legacy: false,
    locale: storedLanguage || 'pt',
    messages: translations,
});

const app = createApp(App);
app.use(router);
app.use(i18n);
app.mount('#app');
