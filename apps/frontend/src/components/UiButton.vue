<script lang="ts" setup>
import { defineProps } from 'vue';

const props = defineProps<{
    title?: string;
    class?: string;
    onClick?: (event: MouseEvent) => void;
}>();

const defaultStyles =
    'group text-text bg-primary hover:bg-black px-4 py-2 rounded-md transition-all cursor-pointer border-black dark:border-white border dark:hover:bg-white shadow-md';
</script>

<template>
    <button @click="props.onClick" :title="props.title" :class="[props.class, defaultStyles]">
        <span class="group-hover:text-primary">
            <slot></slot>
        </span>
    </button>
</template>
