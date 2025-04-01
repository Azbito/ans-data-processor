<script lang="ts" setup>
import UiLanguageChanger from '@/components/UiLanguageChanger.vue';
import UiThemeSwitcher from '@/components/UiThemeSwitcher.vue';
import { useRouter } from 'vue-router';

const router = useRouter();

const goHome = () => {
    router.push('/');
};
</script>

<template>
    <div
        class="bg-primary fixed top-0 flex h-16 w-full items-center justify-between px-16 shadow-lg">
        <button class="text-xl font-bold" title="Home" @click="goHome">
            {{ $t('home') }}
        </button>

        <div class="flex items-center gap-4">
            <UiLanguageChanger />
            <UiThemeSwitcher />
        </div>
    </div>
</template>
