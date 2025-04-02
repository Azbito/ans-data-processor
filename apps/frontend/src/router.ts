import Analytics from '@/pages/AnalyticsPage.vue';
import Extractor from '@/pages/ExtractorPage.vue';
import Home from '@/pages/HomePage.vue';
import Operators from '@/pages/OperatorsPage.vue';
import Accounting from '@/pages/AccountingPage.vue';
import { createRouter, createWebHistory } from 'vue-router';

const routes = [
    {
        path: '/',
        component: Home,
    },
    {
        path: '/extract',
        component: Extractor,
    },
    {
        path: '/operators',
        component: Operators,
    },
    {
        path: '/analytics',
        component: Analytics,
    },
    {
        path: '/accounting',
        component: Accounting,
    },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;
