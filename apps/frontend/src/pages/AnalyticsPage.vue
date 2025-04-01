<template>
    <main class="w-screen px-16 py-32">
        <div class="flex w-full justify-center gap-8 max-[956px]:flex-col">
            <div class="flex flex-col">
                <b class="text-text bg-primary mb-8 text-xl" v-if="quarterly.length">{{
                    $t('quarterly')
                }}</b>

                <div
                    v-for="(item, index) in quarterly"
                    :key="'quarterly-' + index"
                    class="dark:bg-primary mb-6 w-full rounded-lg bg-white p-6 shadow-lg">
                    <h3 class="text-text mb-4 text-xl font-semibold">#{{ index + 1 }}</h3>
                    <b class="bg-primary mt-4 w-fit px-2 py-1 dark:bg-white">{{
                        item.razao_social
                    }}</b>
                    <p class="bg-primary mt-2 w-fit px-2 py-1 dark:bg-white">
                        ANS: {{ item.registro_ans }}
                    </p>
                    <p class="bg-primary mt-2 w-fit px-2 py-1 dark:bg-white">
                        {{ formatToBRL(item.valor_despesa) }}
                    </p>
                </div>
            </div>

            <div class="flex flex-col">
                <b class="text-text bg-primary mb-8 text-xl" v-if="yearly.length">{{
                    $t('yearly')
                }}</b>
                <div
                    v-for="(item, index) in yearly"
                    :key="'yearly-' + index"
                    class="dark:bg-primary mb-6 w-full rounded-lg bg-white p-6 shadow-lg">
                    <h3 class="text-text mb-4 text-xl font-semibold">#{{ index + 1 }}</h3>
                    <b class="bg-primary mt-4 w-fit px-2 py-1 dark:bg-white">{{
                        item.razao_social
                    }}</b>
                    <p class="bg-primary mt-2 w-fit px-2 py-1 dark:bg-white">
                        ANS: {{ item.registro_ans }}
                    </p>
                    <p class="bg-primary mt-2 w-fit px-2 py-1 dark:bg-white">
                        {{ formatToBRL(item.valor_despesa) }}
                    </p>
                </div>
            </div>
        </div>
    </main>

    <UiPreloader :isLoading="loading" />
</template>

<script lang="ts" setup>
import UiPreloader from '@/components/UiPreloader.vue';
import { getAnalytics } from '@/services/analytics';
import { formatToBRL } from '@/utils/formatToBRL';
import { onMounted, ref } from 'vue';

interface AnalyticsProps {
    razao_social: string;
    registro_ans: number;
    valor_despesa: number;
}

const quarterly = ref<AnalyticsProps[]>([]);
const yearly = ref<AnalyticsProps[]>([]);
const loading = ref(true);

onMounted(async () => {
    try {
        const [quarterlyData, yearlyData] = await Promise.all([
            getAnalytics({ period: 'quarterly' }),
            getAnalytics({ period: 'yearly' }),
        ]);

        quarterly.value = quarterlyData;
        yearly.value = yearlyData;
    } catch (error) {
        console.error('Failed to fetch analytics:', error);
    } finally {
        loading.value = false;
    }
});
</script>
