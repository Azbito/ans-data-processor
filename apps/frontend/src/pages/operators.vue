<template>
    <div class="flex w-screen flex-col items-center px-12 pb-16">
        <h1 class="text-text mb-4 mt-32 text-2xl font-bold">{{ $t('searchOperators') }}</h1>
        <form
            @submit.prevent="fetchOperators"
            class="mt-32 flex w-full gap-4 max-[1020px]:flex-col">
            <Input v-model="filters.name" :placeholder="$t('name')" class="w-full" />
            <Input v-model="filters.city" :placeholder="$t('city')" class="w-full" />
            <Input v-model="filters.state" :placeholder="$t('state')" class="w-full" />
            <Input v-model="filters.modality" :placeholder="$t('modality')" class="w-full" />
            <Button class="w-100 max-[1020px]:w-full" type="submit">{{ $t('search') }}</Button>
        </form>

        <Button class="mt-4 w-full" @click="triggerFileInput">{{ $t('uploadCsv') }}</Button>
        <input
            type="file"
            ref="fileInput"
            @change="handleFileUpload"
            accept=".csv"
            class="hidden" />

        <div class="mt-6 max-w-full !overflow-x-auto">
            <table v-if="operators.length" class="w-max rounded-lg shadow-lg">
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
</template>

<script>
import Button from '@/components/button.vue';
import Input from '@/components/input.vue';
import { useToast } from '@/composables/use-toast';
import { getOperatorsByQueries, importOperatorCSV } from '@/services/operators';
import { formatCNPJ } from '@/utils/format-cnpj';
import { formatDate } from '@/utils/format-date';

const { showToast } = useToast();

export default {
    components: { Input, Button },
    data() {
        return {
            filters: {
                name: '',
                city: '',
                state: '',
                modality: '',
            },
            operators: [],
        };
    },
    methods: {
        async fetchOperators() {
            this.operators = await getOperatorsByQueries(this.filters);
        },
        formatCNPJ,
        formatDate,
        triggerFileInput() {
            this.$refs.fileInput.click();
        },
        async handleFileUpload(event) {
            const file = event.target.files[0];
            try {
                await importOperatorCSV(file);
            } catch {
                showToast({ message: 'errorUpload', type: 'error' });
            }
        },
    },
};
</script>
