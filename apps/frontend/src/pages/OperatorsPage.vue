<template>
    <div class="flex w-screen flex-col items-center px-12 pb-16">
        <h1 class="text-text mb-4 mt-32 text-2xl font-bold">{{ $t('searchOperators') }}</h1>
        <form
            @submit.prevent="fetchOperators"
            class="mt-32 flex w-full gap-4 max-[1020px]:flex-col">
            <UiInput v-model="filters.name" :placeholder="$t('name')" class="w-full" />
            <UiInput v-model="filters.city" :placeholder="$t('city')" class="w-full" />
            <UiInput v-model="filters.state" :placeholder="$t('state')" class="w-full" />
            <UiInput v-model="filters.modality" :placeholder="$t('modality')" class="w-full" />
            <UiButton class="w-100 max-[1020px]:w-full" type="submit">{{ $t('search') }}</UiButton>
        </form>

        <UiButton class="mt-4 w-full" @click="showUploadModal = true">{{
            $t('uploadCsv')
        }}</UiButton>

        <UiModal v-model="showUploadModal" :title="$t('uploadCsv')">
            <UiFileUpload accept=".csv" :label="$t('uploadCsv')" :on-upload="handleFileUpload" />
        </UiModal>

        <div class="mt-6 max-w-full !overflow-x-auto">
            <table v-if="operators.length" class="rounded-lg shadow-lg max-[765px]:w-max">
                <thead>
                    <tr class="bg-primary text-text text-left">
                        <th class="p-4">{{ $t('ansRegister') }}</th>
                        <th class="p-4">{{ $t('social') }}</th>
                        <th class="p-4">{{ $t('cnpj') }}</th>
                        <th class="p-4">{{ $t('ansDateRegister') }}</th>
                    </tr>
                </thead>
                <tbody>
                    <tr
                        v-for="(operator, index) in operators"
                        :key="operator.registro_ans"
                        :class="[
                            'bg-background last:rounded-b-lg',
                            (index & 1) === 0 ? 'bg-table-primary' : 'bg-table-secondary',
                        ]">
                        <td class="text-text p-4">{{ operator.registro_ans }}</td>
                        <td class="text-text p-4">{{ operator.razao_social }}</td>
                        <td class="text-text p-4">{{ formatCNPJ(operator.cnpj) }}</td>
                        <td class="text-text p-4">{{ formatDate(operator.data_registro_ans) }}</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
    <UiPreloader :isLoading="isLoading" />
</template>

<script lang="ts">
import UiButton from '@/components/UiButton.vue';
import UiFileUpload from '@/components/UiFileUpload.vue';
import UiInput from '@/components/UiInput.vue';
import UiModal from '@/components/UiModal.vue';
import UiPreloader from '@/components/UiPreloader.vue';
import { useToast } from '@/composables/useToast';
import { getOperatorsByQueries, importOperatorCSV } from '@/services/operators';
import { formatCNPJ } from '@/utils/formatCNPJ';
import { formatDate } from '@/utils/formatDate';
import { defineComponent, ref } from 'vue';

interface OperatorProps {
    registro_ans: number;
    cnpj: string;
    razao_social: string;
    nome_fantasia: string;
    modalidade: string;
    logradouro: string;
    numero: string;
    complemento: string;
    bairro: string;
    cidade: string;
    uf: string;
    cep: number;
    ddd: number;
    telefone: number;
    fax: number;
    endereco_eletronico: string;
    representante: string;
    cargo_representante: string;
    regiao_de_comercializacao: number;
    data_registro_ans: string;
}

const { showToast } = useToast();

export default defineComponent({
    components: { UiInput, UiButton, UiPreloader, UiFileUpload, UiModal },
    setup() {
        const filters = ref({
            name: '',
            city: '',
            state: '',
            modality: '',
        });

        const operators = ref<OperatorProps[]>([]);
        const isLoading = ref(false);
        const showUploadModal = ref(false);

        const executeWithLoading = async (fn: () => Promise<void>) => {
            isLoading.value = true;
            try {
                await fn();
            } catch (error) {
                console.error(error);
            } finally {
                isLoading.value = false;
            }
        };

        const fetchOperators = async () => {
            await executeWithLoading(async () => {
                operators.value = await getOperatorsByQueries(filters.value);
            });
        };

        const handleFileUpload = async (file: File) => {
            await executeWithLoading(async () => {
                await importOperatorCSV(file);
                showToast({ message: 'fileUploaded', type: 'success' });
            });
        };

        return {
            filters,
            operators,
            isLoading,
            showUploadModal,
            fetchOperators,
            formatCNPJ,
            formatDate,
            handleFileUpload,
        };
    },
});
</script>
