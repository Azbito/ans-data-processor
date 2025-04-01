<template>
    <div v-if="isLoading" class="preloader">
        <div class="spinner"></div>
    </div>
</template>

<script lang="ts" setup>
import { defineProps } from 'vue';

defineProps<{ isLoading: boolean }>();
</script>
