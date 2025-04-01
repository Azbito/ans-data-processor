<script lang="ts" setup>
import { defineProps, useAttrs } from 'vue';

interface ButtonProps {
    title?: string;
    class?: string;
}

const props = defineProps<ButtonProps>();
const attrs = useAttrs();

const defaultStyles =
    'group text-text bg-primary hover:bg-black px-4 py-2 rounded-md transition-all cursor-pointer border-black dark:border-white border dark:hover:bg-white shadow-md';
</script>

<template>
    <button v-bind="attrs" :class="[defaultStyles, props.class]" :title="props.title">
        <span class="group-hover:text-primary">
            <slot></slot>
        </span>
    </button>
</template>
