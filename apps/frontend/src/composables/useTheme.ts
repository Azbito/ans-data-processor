import { inject, type Ref, ref, computed } from 'vue';

type Themes = 'light' | 'dark';

export function useTheme() {
    const theme = inject<Ref<Themes>>('theme');
    const themeSetter = inject<(newTheme: Themes) => void>('themeSetter');

    if (!theme || !themeSetter) {
        const localTheme = ref<Themes>('light');
        const toggleTheme = () => {
            localTheme.value = localTheme.value === 'light' ? 'dark' : 'light';
        };

        return {
            theme: computed(() => localTheme.value),
            toggleTheme,
        };
    }

    const toggleTheme = () => {
        const newTheme = theme.value === 'light' ? 'dark' : 'light';
        themeSetter(newTheme);
    };

    return {
        theme: computed(() => theme.value),
        toggleTheme,
    };
}
