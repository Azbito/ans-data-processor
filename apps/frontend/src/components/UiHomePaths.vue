<script lang="ts">
import UiButton from '@/components/UiButton.vue';
import { defineComponent } from 'vue';
import { useRouter } from 'vue-router';

export default defineComponent({
    name: 'HomePaths',
    components: { UiButton },

    setup() {
        const router = useRouter();

        const goToExtractorPage = () => {
            router.push('/extract');
        };

        const goToOperatorsPage = () => {
            router.push('/operators');
        };

        const goToAnalyticsPage = () => {
            router.push('/analytics');
        };

        const goToAccountingEntriesPage = () => {
            router.push('/accounting');
        };

        return {
            goToExtractorPage,
            goToOperatorsPage,
            goToAnalyticsPage,
            goToAccountingEntriesPage,
        };
    },
});
</script>

<template>
    <div class="min-h-screen px-16">
        <div class="mt-32 flex flex-col">
            <h1 class="text-text text-4xl">{{ $t('title') }}</h1>
            <p class="text-text bg-primary w-fit px-2 py-1 text-2xl">{{ $t('description') }}</p>
        </div>

        <div class="mt-16 flex gap-4 max-[956px]:flex-col">
            <UiButton @click="goToAccountingEntriesPage">{{ $t('accountingEntries') }}</UiButton>
            <UiButton @click="goToOperatorsPage">{{ $t('healthOperators') }}</UiButton>
            <UiButton @click="goToAnalyticsPage">{{ $t('analytics') }}</UiButton>
            <UiButton @click="goToExtractorPage">{{ $t('extractFiles') }}</UiButton>
        </div>
    </div>
</template>
