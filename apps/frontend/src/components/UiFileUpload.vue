<template>
    <div
        class="file-drop-zone flex w-full flex-col items-center justify-center rounded-lg border-2 border-dashed border-gray-300 p-6 text-center dark:border-gray-700"
        :class="{ 'border-blue-500 bg-blue-100 dark:bg-gray-800': isDragging }"
        @dragover.prevent="handleDragOver"
        @dragleave.prevent="handleDragLeave"
        @drop.prevent="handleDrop">
        <div class="mb-4 flex flex-col items-center justify-center space-y-2">
            <h3 v-if="!isDragging" class="text-lg font-medium text-gray-900 dark:text-white">
                {{ $t('dragAndDrop') }}
            </h3>
            <h3 v-else class="text-lg font-medium text-blue-600 dark:text-blue-400">
                {{ $t('dropHere') }}
            </h3>
            <p v-if="!isDragging" class="text-sm text-gray-500 dark:text-gray-400">
                {{ $t('orClickToUpload') }}
            </p>
        </div>

        <div class="mt-4 flex flex-col items-center justify-center space-y-2">
            <UiButton v-if="!isDragging" @click="handleClick" class="w-full max-w-xs">
                {{ label }}
            </UiButton>
        </div>

        <input
            ref="inputRef"
            type="file"
            :accept="accept"
            class="hidden"
            @change="handleFileSelect" />
    </div>
</template>

<script lang="ts" setup>
import { onMounted, ref } from 'vue';
import { useI18n } from 'vue-i18n';
import UiButton from './UiButton.vue';

const props = defineProps<{
    accept?: string;
    label: string;
    onUpload: (file: File) => Promise<void>;
}>();

const emit = defineEmits<{
    (e: 'error', message: string): void;
}>();

const { t } = useI18n();
const inputRef = ref<HTMLInputElement | null>(null);
const isDragging = ref(false);

const handleClick = () => {
    inputRef.value?.click();
};

const handleFileSelect = async (event: Event) => {
    const target = event.target as HTMLInputElement;
    const file = target.files?.[0];

    if (!file) return;

    try {
        await props.onUpload(file);
    } catch {
        emit('error', t('uploadFailed'));
    }
};

const handleDragOver = (e: DragEvent) => {
    e.preventDefault();
    isDragging.value = true;
};

const handleDragLeave = (e: DragEvent) => {
    e.preventDefault();
    isDragging.value = false;
};

const handleDrop = async (e: DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    isDragging.value = false;

    const file = e.dataTransfer?.files?.[0];

    if (!file) {
        return;
    }

    try {
        await props.onUpload(file);
    } catch {
        emit('error', t('uploadFailed'));
    }
};

onMounted(() => {
    document.addEventListener('dragover', (e) => e.preventDefault());
    document.addEventListener('drop', (e) => e.preventDefault());
});
</script>
