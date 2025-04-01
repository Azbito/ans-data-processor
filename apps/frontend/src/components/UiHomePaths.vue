<script lang="ts">
import UiInput from '@/components/UiButton.vue';
import { defineComponent } from 'vue';
import { useRouter } from 'vue-router';

export default defineComponent({
    name: 'HomePaths',
    components: { UiInput },

    setup() {
        const router = useRouter();

        const goToExtractorPage = () => {
            router.push('/extract');
        };

        const goToOperatorsPage = () => {
            router.push('/operators');
        };

        return {
            goToExtractorPage,
            goToOperatorsPage,
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
            <UiInput>{{ $t('accountingEntries') }}</UiInput>
            <UiInput @click="goToOperatorsPage">{{ $t('healthOperators') }}</UiInput>
            <UiInput>{{ $t('analytics') }}</UiInput>
            <UiInput @click="goToExtractorPage">{{ $t('extractFiles') }}</UiInput>
        </div>
    </div>
</template>
