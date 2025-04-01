import { inject, type Ref } from 'vue';

type Themes = 'light' | 'dark';

export function useTheme() {
    const theme = inject<Ref<Themes>>('theme');
    const themeSetter = inject<(newTheme: Themes) => void>('themeSetter');

    if (!theme || !themeSetter) {
        return {
            theme: 'light',
            themeSetter: () => {},
        };
    }

    const toggleTheme = () => {
        const newTheme = theme.value === 'light' ? 'dark' : 'light';
        themeSetter(newTheme);
    };

    return {
        theme,
        toggleTheme,
    };
}
