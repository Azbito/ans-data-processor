<template>
    <main class="w-screen px-6 py-32 md:px-16">
        <div class="flex w-full flex-col justify-center gap-8 md:flex-row">
            <div class="flex w-full max-w-3xl flex-col max-[768px]:mt-16">
                <b class="text-text bg-primary mb-6 rounded-md px-4 py-2 text-xl md:mb-8">
                    {{ $t('recentEntries') }}
                </b>

                <div class="entries-container space-y-6">
                    <div
                        v-for="(entry, index) in entries"
                        :key="index"
                        class="dark:bg-primary w-full rounded-lg bg-white p-6 shadow-lg transition-transform hover:scale-[1.02]">
                        <div class="flex items-center justify-between">
                            <h3 class="text-xl font-semibold">{{ formatDate(entry.data) }}</h3>
                        </div>

                        <div class="mt-4 space-y-3">
                            <div class="flex items-center gap-2">
                                <UiIcon name="operator" class="text-text" />
                                <span class="text-text">ANS: {{ entry.reg_ans }}</span>
                            </div>
                            <div class="flex items-center gap-2">
                                <UiIcon name="account" class="text-text" />
                                <span class="text-text"
                                    >Account: {{ entry.cd_conta_contabil }}</span
                                >
                            </div>
                            <div class="flex items-center gap-2">
                                <UiIcon name="description" class="text-text" />
                                <span class="text-text">{{ entry.descricao }}</span>
                            </div>
                            <div class="flex items-center gap-2">
                                <UiIcon name="initial" class="text-text" />
                                <span class="text-text"
                                    >Initial Balance:
                                    {{ formatToBRL(entry.vl_saldo_inicial) }}</span
                                >
                            </div>
                            <div class="flex items-center gap-2">
                                <UiIcon name="final" class="text-text" />
                                <span class="text-text"
                                    >Final Balance: {{ formatToBRL(entry.vl_saldo_final) }}</span
                                >
                            </div>
                        </div>
                    </div>
                </div>

                <div v-if="loading" class="mt-4 flex justify-center">
                    <UiPreloader :isLoading="true" />
                </div>

                <div ref="lastEntryRef" class="invisible h-1"></div>
            </div>

            <div
                class="fixed right-4 top-20 flex w-64 flex-col space-y-4 max-[1400px]:w-full min-[1400px]:relative min-[1400px]:top-0 min-[1400px]:w-screen min-[1400px]:max-w-xs min-[1400px]:space-y-6">
                <div
                    class="fixed left-1/2 top-20 flex w-64 -translate-x-1/2 flex-col items-center space-y-4 max-[1400px]:w-full max-[1400px]:flex-row max-[1400px]:items-center max-[1400px]:justify-center max-[1400px]:gap-4 min-[1400px]:relative min-[1400px]:top-0 min-[1400px]:w-screen min-[1400px]:max-w-xs min-[1400px]:space-y-6">
                    <div
                        class="flex flex-col gap-4 max-[1400px]:w-[90%] max-[1400px]:flex-row max-[1400px]:items-center max-[1400px]:justify-center max-[1400px]:gap-4 max-[1400px]:space-y-0 min-[1400px]:ml-4 min-[1400px]:w-full">
                        <UiInput
                            v-model="searchOperator"
                            :placeholder="$t('searchOperator')"
                            class="w-full placeholder:text-sm" />
                        <UiButton
                            @click="searchOperatorEntries"
                            class="group h-10 w-fit whitespace-nowrap !px-2 !py-0 min-[1400px]:w-full">
                            <UiIcon
                                v-if="windowWidth < 540"
                                name="search"
                                class="text-text group-hover:text-white dark:group-hover:text-black" />
                            <template v-else>{{ $t('search') }}</template>
                        </UiButton>
                        <UiButton
                            class="h-10 w-fit whitespace-nowrap !px-2 !py-0 min-[1400px]:w-full"
                            @click="showImportModal = true">
                            <UiIcon
                                v-if="windowWidth < 540"
                                name="upload"
                                class="text-text min-h-5 min-w-5 group-hover:text-white dark:group-hover:text-black" />
                            <template v-else>{{ $t('importData') }}</template>
                        </UiButton>
                    </div>
                </div>
            </div>
        </div>

        <UiModal v-model="showImportModal" :title="$t('importData')">
            <div class="space-y-4">
                <UiFileUpload
                    accept=".csv"
                    :label="$t('selectCsvFile')"
                    :on-upload="handleFileUpload" />
            </div>
        </UiModal>
    </main>
</template>

<script lang="ts" setup>
import UiButton from '@/components/UiButton.vue';
import UiFileUpload from '@/components/UiFileUpload.vue';
import UiIcon from '@/components/UiIcon.vue';
import UiInput from '@/components/UiInput.vue';
import UiModal from '@/components/UiModal.vue';
import UiPreloader from '@/components/UiPreloader.vue';
import {
    getAccountingEntries,
    getAccountingEntriesByOperator,
    importAccountingData,
} from '@/services/accounting';
import { formatDate } from '@/utils/formatDate';
import { formatToBRL } from '@/utils/formatToBRL';
import { onMounted, onUnmounted, ref } from 'vue';

interface AccountingEntry {
    data: string;
    reg_ans: number;
    cd_conta_contabil: number;
    descricao: string;
    vl_saldo_inicial: number;
    vl_saldo_final: number;
}

const entries = ref<AccountingEntry[]>([]);
const loading = ref<boolean>(false);
const hasMore = ref<boolean>(true);
const searchOperator = ref<string>('');
const showImportModal = ref<boolean>(false);
const cursor = ref<string | undefined>(undefined);
const lastEntryRef = ref<HTMLElement | null>(null);
const uploadProgress = ref<number>(0);
const uploadedBytes = ref<number>(0);
const fileSize = ref<number>(0);
const windowWidth = ref<number>(window.innerWidth);

const updateWindowWidth = () => {
    windowWidth.value = window.innerWidth;
};

const loadEntries = async (params: { cursor?: string } = {}) => {
    if (loading.value || !hasMore.value) return;

    try {
        loading.value = true;
        const { data, next_cursor } = await getAccountingEntries({
            limit: 10,
            ...params,
        });

        entries.value = [...entries.value, ...data];
        cursor.value = next_cursor;
        hasMore.value = !!next_cursor;
    } catch (error) {
        console.error('Failed to load accounting entries:', error);
    } finally {
        loading.value = false;
    }
};

const handleFileUpload = async (file: File) => {
    try {
        if (file.size > 5 * 1024 * 1024) return;

        loading.value = true;
        showImportModal.value = false;
        fileSize.value = file.size;
        uploadedBytes.value = 0;

        await importAccountingData(file);
        entries.value = [];
        cursor.value = undefined;
        loadEntries();
    } catch (error) {
        console.error('Failed to import accounting data:', error);
    } finally {
        loading.value = false;
        uploadProgress.value = 0;
        uploadedBytes.value = 0;
        fileSize.value = 0;
    }
};

const searchOperatorEntries = async () => {
    if (!searchOperator.value) return;

    try {
        loading.value = true;
        const operatorEntries = await getAccountingEntriesByOperator(
            parseInt(searchOperator.value),
        );
        entries.value = operatorEntries;
        cursor.value = undefined;
        hasMore.value = false;
    } catch (error) {
        console.error('Failed to search operator entries:', error);
    } finally {
        loading.value = false;
    }
};

const initInfiniteScroll = () => {
    if (observer) {
        observer.disconnect();
    }

    observer = new IntersectionObserver(
        (entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting && !loading.value && hasMore.value) {
                    loadEntries({ cursor: cursor.value });
                }
            });
        },
        {
            threshold: 0.1,
        },
    );

    if (lastEntryRef.value) {
        observer.observe(lastEntryRef.value);
    }
};

let observer: IntersectionObserver | null = null;

onMounted(() => {
    loadEntries();
    initInfiniteScroll();
    window.addEventListener('resize', updateWindowWidth);
});

onUnmounted(() => {
    window.removeEventListener('resize', updateWindowWidth);

    if (observer) {
        observer.disconnect();
        observer = null;
    }
});
</script>
