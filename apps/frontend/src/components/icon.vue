<script setup>
import { computed, defineAsyncComponent } from 'vue';

const props = defineProps({
    name: {
        type: String,
        required: true,
    },
    class: {
        type: String,
        required: false,
    },
});

const icons = import.meta.glob('@/assets/icons/*.svg');

const icon = computed(() => {
    const path = `/src/assets/icons/${props.name}.svg`;
    return icons[path] ? defineAsyncComponent(icons[path]) : null;
});
</script>

<template>
    <component v-if="icon" :is="icon" :class="props.class" />
</template>
