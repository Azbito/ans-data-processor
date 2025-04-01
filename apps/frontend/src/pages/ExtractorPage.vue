<script lang="ts" setup>
import UiButton from '@/components/UiButton.vue';
import UiInput from '@/components/UiInput.vue';
import UiPreloader from '@/components/UiPreloader.vue';
import UiToast from '@/components/UiToast.vue';
import { useToast } from '@/composables/useToast';
import { getCSV } from '@/services/csv.ts';
import { getANSZippedPDFs, getPDF } from '@/services/pdf.ts';
import { ref } from 'vue';

const { showToast } = useToast();

const targetUrl = ref('');
const targetFile = ref('');
const isLoading = ref(false);

const downloadFile = (url: string, filename?: string) => {
    const link = document.createElement('a');
    link.href = url;
    link.download = filename || 'download.pdf';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
};

const handleGetPDF = async () => {
    if (!targetUrl.value.trim()) {
        showToast({ message: 'invalidUrl', type: 'error' });
        return;
    }

    try {
        isLoading.value = true;
        const response = await getPDF({ url: targetUrl.value, filename: targetFile.value });

        if (response?.url) {
            downloadFile(response.url, targetFile.value);
            showToast({ message: 'downloadSuccess', type: 'success' });
        }
    } catch (err) {
        console.error(err);
        showToast({ message: 'error', type: 'error' });
    } finally {
        isLoading.value = false;
    }
};

const handleGetCSV = async () => {
    try {
        isLoading.value = true;
        const response = await getCSV();

        if (response?.url) {
            downloadFile(response.url);
            showToast({ message: 'downloadSuccess', type: 'success' });
        }
    } catch (err) {
        console.error(err);
        showToast({ message: 'error', type: 'error' });
    } finally {
        isLoading.value = false;
    }
};

const extractPdf = async () => {
    if (!targetUrl.value.trim()) {
        showToast({ message: 'invalidUrl', type: 'error' });
        return;
    }

    try {
        isLoading.value = true;
        const response = await getANSZippedPDFs({ url: targetUrl.value });

        if (response?.url) {
            downloadFile(response.url);
            showToast({ message: 'downloadSuccess', type: 'success' });
        }
    } catch (err) {
        console.error(err);
        showToast({ message: 'error', type: 'error' });
    } finally {
        isLoading.value = false;
    }
};
</script>

<template>
    <div class="mt-32 flex flex-wrap gap-6 px-16">
        <UiInput
            v-model.trim="targetUrl"
            :label="$t('targetUrl')"
            :placeholder="$t('targetUrlPlaceholder')" />

        <div class="bg-primary w-120 flex flex-col justify-between gap-6 p-6">
            <b class="text-text text-lg">{{ $t('extractZip') }}</b>
            <UiButton :title="$t('getZIP')" :disabled="isLoading" :onclick="extractPdf">
                {{ $t('getZIP') }}
            </UiButton>
        </div>

        <div class="bg-primary w-120 flex flex-col gap-6 p-6 max-[450px]:w-full">
            <b class="text-text text-lg">{{ $t('extractZip') }}</b>
            <UiInput
                v-model.trim="targetFile"
                :label="$t('targetFile')"
                :placeholder="$t('targetFilePlaceholder')" />
            <UiButton :title="$t('getFile')" :disabled="isLoading" :onclick="handleGetPDF">
                {{ $t('getFile') }}
            </UiButton>
        </div>

        <div class="bg-primary w-120 flex flex-col gap-6 p-6 max-[450px]:w-full">
            <b class="text-text text-lg">{{ $t('getCSV') }}</b>

            <UiButton :title="$t('getFile')" :disabled="isLoading" :onclick="handleGetCSV">
                {{ $t('getFile') }}
            </UiButton>
        </div>
    </div>
    <UiToast />
    <UiPreloader :isLoading="isLoading" />
</template>
