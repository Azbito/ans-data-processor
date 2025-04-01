<script lang="ts">
import Button from '@/components/button.vue';
import { defineComponent } from 'vue';
import { useRouter } from 'vue-router';

export default defineComponent({
    name: 'HomePaths',
    components: { Button },

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
            <Button>{{ $t('accountingEntries') }}</Button>
            <Button @click="goToOperatorsPage">{{ $t('healthOperators') }}</Button>
            <Button>{{ $t('analytics') }}</Button>
            <Button @click="goToExtractorPage">{{ $t('extractFiles') }}</Button>
        </div>
    </div>
</template>
