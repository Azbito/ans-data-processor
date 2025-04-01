import { en } from '@/i18n/en';
import { pt } from '@/i18n/pt';

export const translations = {
    pt,
    en,
} as const;

export type Languages = 'pt' | 'en';
