<script setup lang="ts">
import Icon from '@/components/UiIcon.vue';
import { useTheme } from '@/composables/useTheme';

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
