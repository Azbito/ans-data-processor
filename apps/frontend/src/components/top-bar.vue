<script lang="ts">
import LanguageChanger from '@/components/language-changer.vue';
import ThemeSwitcher from '@/components/theme-switcher.vue';
import { defineComponent } from 'vue';
import { useRouter } from 'vue-router';

export default defineComponent({
    name: 'TopBar',
    components: {
        ThemeSwitcher,
        LanguageChanger,
    },
    setup() {
        const router = useRouter();

        const goHome = () => {
            router.push('/');
        };

        return {
            goHome,
        };
    },
});
</script>

<template>
    <div
        class="bg-background dark:bg-foreground fixed top-0 flex w-screen justify-between py-4 shadow">
        <div class="flex w-fit items-center justify-center px-4 text-center">
            <button class="cursor-pointer" @click="goHome">
                <strong class="text-text text-2xl">ADP</strong>
            </button>
        </div>
        <div class="flex items-center justify-center gap-6 pr-8">
            <LanguageChanger />
            <ThemeSwitcher />
        </div>
    </div>
</template>
