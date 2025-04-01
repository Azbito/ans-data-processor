<script lang="ts" setup>
import { computed, defineAsyncComponent } from 'vue';

interface SvgComponent {
    template: string;
}

const props = defineProps<{
    name: string;
    class?: string;
}>();

const icons = import.meta.glob('@/assets/icons/*.svg', { eager: true }) as Record<string, SvgComponent>;

const icon = computed(() => {
    const path = `/src/assets/icons/${props.name}.svg`;
    return icons[path] ? defineAsyncComponent(() => Promise.resolve(icons[path])) : null;
});
</script>

<template>
    <component v-if="icon" :is="icon" :class="props.class" />
</template>
