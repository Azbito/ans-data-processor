<script lang="ts" setup>
import { onMounted, provide, ref } from 'vue';

const theme = ref<'light' | 'dark'>('light');

const themeSetter = (newTheme: 'light' | 'dark') => {
    theme.value = newTheme;
    document.documentElement.className = newTheme;
    localStorage.setItem('theme', newTheme);
};

onMounted(() => {
    const savedTheme = localStorage.getItem('theme') as 'light' | 'dark';
    if (savedTheme) {
        theme.value = savedTheme;
        document.documentElement.className = savedTheme;
    }
});

provide('theme', theme);
provide('themeSetter', themeSetter);
</script>

<template>
    <slot />
</template>
