<template>
    <button
        v-if="isShowing"
        class="fixed bottom-4 right-4 -translate-y-4 cursor-pointer rounded-lg p-4 text-white opacity-0 shadow-lg transition-transform duration-300 ease-out"
        :class="[
            toastClasses,
            isShowing ? '-translate-y-15 opacity-100' : 'translate-y-5 opacity-0',
        ]"
        role="toast"
        @click="hideToast">
        <div class="flex items-center gap-3">
            <div class="flex-1">
                {{ $t(currentToast?.message || '') }}
            </div>
            <button class="text-white hover:text-gray-200" @click.stop="hideToast">×</button>
        </div>
    </button>
</template>

<script setup lang="ts">
import { useToast } from '@/composables/use-toast';
import { computed } from 'vue';

const { currentToast, isShowing } = useToast();

const hideToast = () => {
    isShowing.value = false;
    currentToast.value = null;
};

const toastClasses = computed(() => {
    if (!currentToast.value) return '';

    switch (currentToast.value.type) {
        case 'success':
            return 'bg-green-500';
        case 'info':
            return 'bg-blue-500';
        case 'error':
        default:
            return 'bg-red-500';
    }
});
</script>
