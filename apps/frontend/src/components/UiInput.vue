<script lang="ts" setup>
import { defineEmits, defineProps } from 'vue';

defineProps({
    modelValue: String,
    label: String,
    placeholder: String,
    type: {
        type: String,
        default: 'text',
    },
    error: String,
});

const emit = defineEmits(['update:modelValue']);

const onInput = (event: Event) => {
    emit('update:modelValue', (event.target as HTMLInputElement).value);
};
</script>

<template>
    <div class="flex w-full flex-col">
        <label v-if="label" class="text-text mb-1 text-sm font-medium">{{ label }}</label>
        <input
            :type="type"
            :value="modelValue"
            @input="onInput"
            :placeholder="placeholder"
            class="bg-foreground text-text rounded-lg px-3 py-2 transition-all" />
        <p v-if="error" class="mt-1 text-xs text-red-800">{{ error }}</p>
    </div>
</template>
