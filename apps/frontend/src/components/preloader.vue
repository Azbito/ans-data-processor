<template>
    <div v-if="isLoading" class="preloader">
        <div class="spinner"></div>
    </div>
</template>

<script setup lang="ts">
import { defineProps } from 'vue';

defineProps<{ isLoading: boolean }>();
</script>
