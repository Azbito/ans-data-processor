import Extractor from '@/pages/extractor.vue';
import Home from '@/pages/home.vue';
import Operators from '@/pages/operators.vue';
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
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;
