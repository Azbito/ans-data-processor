import { API } from '@/libs/api';

export async function getAnalytics({ period }: { period: 'yearly' | 'quarterly' }) {
    const { data } = await API.get(`/analytics/expenses/${period}`);

    return data;
}
