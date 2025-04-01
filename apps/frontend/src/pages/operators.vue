<template>
    <div class="flex w-screen flex-col items-center">
        <h1 class="text-text mb-4 mt-32 text-2xl font-bold">{{ $t('searchOperators') }}</h1>
        <form
            @submit.prevent="fetchOperators"
            class="mt-32 flex w-full gap-4 px-16 max-[1020px]:flex-col">
            <Input v-model="filters.name" :placeholder="$t('name')" class="w-full" />
            <Input v-model="filters.city" :placeholder="$t('city')" class="w-full" />
            <Input v-model="filters.state" :placeholder="$t('state')" class="w-full" />
            <Input v-model="filters.modality" :placeholder="$t('modality')" class="w-full" />
            <Button class="w-100 max-[1020px]:w-full" type="submit">{{ $t('search') }}</Button>
        </form>

        <table v-if="operators.length" class="mt-6 w-[90%] shadow-md">
            <thead>
                <tr class="bg-primary">
                    <th class="text-text border p-2">{{ $t('ansRegister') }}</th>
                    <th class="text-text border p-2">{{ $t('social') }}</th>
                    <th class="text-text border p-2">{{ $t('cnpj') }}</th>
                    <th class="text-text border p-2">{{ $t('ansDateRegister') }}</th>
                </tr>
            </thead>
            <tbody>
                <tr
                    v-for="operator in operators"
                    :key="operator.registro_ans"
                    class="bg-foreground">
                    <td class="text-text border p-2">{{ operator.registro_ans }}</td>
                    <td class="text-text border p-2">{{ operator.razao_social }}</td>
                    <td class="text-text border p-2">{{ formatCNPJ(operator.cnpj) }}</td>
                    <td class="text-text border p-2">
                        {{ formatDate(operator.data_registro_ans) }}
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
</template>

<script>
import Button from '@/components/button.vue';
import Input from '@/components/input.vue';
import { getOperatorsByQueries } from '@/services/operators';
import { formatCNPJ } from '@/utils/format-cnpj';
import { formatDate } from '@/utils/format-date';

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
    },
};
</script>
