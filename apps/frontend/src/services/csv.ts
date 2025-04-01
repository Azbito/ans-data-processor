import { API } from '@/libs/api';

export async function getCSV() {
    const { data } = await API.get('/csv/download-table');

    return data;
}
