<template>
    <div
        v-if="modelValue"
        class="fixed inset-0 z-50 flex items-center justify-center bg-black/20 bg-opacity-50 backdrop-blur"
        @click.self="$emit('update:modelValue', false)">
        <div class="bg-background dark:bg-foreground w-full max-w-md rounded-lg p-6 shadow-lg">
            <h2 class="text-text mb-4 text-xl font-semibold">{{ title }}</h2>
            <slot></slot>
        </div>
    </div>
</template>

<script lang="ts" setup>
import { defineEmits, defineProps } from 'vue';

defineProps<{
    modelValue: boolean;
    title: string;
}>();

defineEmits<{
    (e: 'update:modelValue', value: boolean): void;
}>();
</script>
