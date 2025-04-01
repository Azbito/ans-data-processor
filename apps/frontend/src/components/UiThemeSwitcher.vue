<script setup lang="ts">
import Icon from '@/components/UiIcon.vue';
import { useTheme } from '@/composables/useTheme';
import { computed } from 'vue';

const { theme, toggleTheme } = useTheme();

const buttonClasses = computed(() => {
    return theme.value === 'light' ? 'bg-primary hover:bg-black' : 'bg-black hover:bg-white';
});

const iconClasses = computed(() => {
    return theme.value === 'light'
        ? 'text-black group-hover:text-primary'
        : 'text-white group-hover:text-black';
});

const icon = computed(() => {
    return theme.value === 'light' ? 'sun' : 'moon';
});
</script>

<template>
    <button
        class="group flex min-h-12 min-w-12 cursor-pointer items-center justify-center rounded-md border border-black transition-all"
        :class="buttonClasses"
        @click="toggleTheme">
        <Icon :name="icon" class="h-8 w-8" :class="iconClasses" />
    </button>
</template>
