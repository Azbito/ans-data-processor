<script setup lang="ts">
import TopBar from '@/components/top-bar.vue';
import ThemeProvider from '@/providers/theme-provider.vue';
import { onMounted, ref } from 'vue';
</script>

<template>
    <ThemeProvider>
        <TopBar />
        <main>
            <router-view />
        </main>
    </ThemeProvider>
</template>
