<script setup>
import { onMounted, provide, ref } from 'vue';

const theme = ref('light');

onMounted(() => {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
        theme.value = savedTheme;
        if (savedTheme === 'dark') {
            document.documentElement.classList.add('dark');
        }
    }
});

const themeSetter = (newTheme) => {
    theme.value = newTheme;

    if (newTheme === 'dark') {
        document.documentElement.classList.add('dark');
    } else {
        document.documentElement.classList.remove('dark');
    }

    localStorage.setItem('theme', newTheme);
};

provide('theme', theme);
provide('themeSetter', themeSetter);
</script>

<template>
    <slot />
</template>
