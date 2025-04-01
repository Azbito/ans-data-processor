<script setup>
import Moon from '@/assets/icons/moon.svg';
import Sun from '@/assets/icons/sun.svg';
import Icon from '@/components/icon.vue';
import { useTheme } from '@/composables/use-theme';

const { theme, toggleTheme } = useTheme();
</script>

<template>
    <button
        class="bg-primary group flex min-h-12 min-w-12 cursor-pointer items-center justify-center rounded-md border border-black transition-all hover:bg-black dark:hover:bg-white"
        @click="toggleTheme">
        <Icon
            :name="theme === 'light' ? 'sun' : 'moon'"
            class="group-hover:text-primary h-8 w-8 text-black dark:text-white" />
    </button>
</template>
