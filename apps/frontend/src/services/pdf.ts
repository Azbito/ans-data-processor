import { API } from '@/libs/api';

export async function getANSZippedPDFs({ url }: { url: string }) {
    const params = {
        target_url: url,
    };

    const { data } = await API.get('/pdf/ans', { params });

    return data;
}

export async function getPDF({ url, filename }: { url: string; filename: string }) {
    const params = {
        target_url: url,
        target_file: filename,
    };

    const { data } = await API.get('/pdf/scrap', { params });

    return data;
}
