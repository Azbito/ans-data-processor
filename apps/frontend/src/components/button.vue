<script setup>
const props = defineProps({
    title: {
        type: String,
        required: false,
    },
    class: {
        type: String,
        required: false,
    },
    onclick: {
        type: Function,
        required: true,
    },
});

const defaultStyles =
    'group text-text bg-primary hover:bg-black px-4 py-2 rounded-md transition-all cursor-pointer border-black dark:border-white border dark:hover:bg-white shadow-md';
</script>

<template>
    <button @click="props.onclick" :title="props.title" :class="[props.class, defaultStyles]">
        <span class="group-hover:text-primary">
            <slot></slot>
        </span>
    </button>
</template>
