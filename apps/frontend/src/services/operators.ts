import { API } from '@/libs/api';

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

    const { data: res } = data;

    return res;
}
