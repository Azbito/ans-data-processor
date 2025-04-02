import { API } from '@/libs/api';

export interface AccountingEntry {
    data: string;
    reg_ans: number;
    cd_conta_contabil: number;
    descricao: string;
    vl_saldo_inicial: number;
    vl_saldo_final: number;
}

export interface PaginatedResponse {
    data: AccountingEntry[];
    next_cursor: string;
}

export const getAccountingEntries = async (params: {
    limit?: number;
    cursor?: string;
}): Promise<PaginatedResponse> => {
    return API.get('/accounting', { params }).then((response) => response.data);
};

export const getAccountingEntriesByOperator = async (
    reg_ans: number,
): Promise<AccountingEntry[]> => {
    return API.get(`/accounting/${reg_ans}`).then((response) => response.data);
};

export const importAccountingData = async (file: File): Promise<void> => {
    const formData = new FormData();
    formData.append('file', file);

    return API.post('/accounting/import', formData, {
        headers: {
            'Content-Type': 'multipart/form-data',
        },
    });
};
