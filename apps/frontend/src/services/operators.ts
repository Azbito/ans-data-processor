import { API } from '@/libs/api';

export async function importOperatorCSV(file: File) {
    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await API.post('/operators/import', formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        });

        return response;
    } catch (error) {
        console.error('Erro ao enviar CSV:', error);
        throw error;
    }
}
export async function getOperatorsByQueries({
    name,
    city,
    state,
    modality,
}: {
    name: string;
    city: string;
    state: string;
    modality: string;
}) {
    const params = {
        name,
        city,
        state,
        modality,
    };

    const { data } = await API.get('/operators/search', { params });

    return data.items;
}
