<script setup lang="ts">
import TopBar from '@/components/UiTopBar.vue';
import ThemeProvider from '@/providers/ThemeProvider.vue';
</script>

<template>
    <ThemeProvider>
        <TopBar />
        <main>
            <router-view />
        </main>
    </ThemeProvider>
</template>
