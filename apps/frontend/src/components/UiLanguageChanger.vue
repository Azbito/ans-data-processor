<script lang="ts">
import type { Languages } from '@/i18n';
import { cn as className } from '@/utils/cn';

export default {
    name: 'LanguageSwitcher',
    data() {
        return {
            currentLanguage: this.$i18n.locale as Languages,
        };
    },
    computed: {
        cn() {
            return className;
        },
    },
    methods: {
        changeLanguage(language: Languages) {
            this.$i18n.locale = language;
            localStorage.setItem('language', language);
        },
    },
    watch: {
        '$i18n.locale'(newLocale: Languages) {
            this.currentLanguage = newLocale;
        },
    },
};
</script>

<template>
    <div class="flex gap-4">
        <button
            @click="changeLanguage('pt')"
            :title="$t('changeToPortuguese')"
            class="group flex cursor-pointer items-center justify-center gap-2 rounded-md px-4 py-2 transition-all hover:bg-black/20">
            <img src="@/assets/icons/br.png" :alt="$t('brazilianFlag')" width="32" />
            <b
                :class="
                    cn(
                        'hidden group-hover:text-orange-500 sm:inline',
                        currentLanguage === 'pt' ? 'text-text' : 'text-disabled',
                    )
                ">
                PT
            </b>
        </button>
        <button
            @click="changeLanguage('en')"
            :title="$t('changeToEnglish')"
            class="group flex cursor-pointer items-center justify-center gap-2 rounded-md px-4 py-2 transition-all hover:bg-black/20">
            <img src="@/assets/icons/us.png" :alt="$t('englishFlag')" width="32" />
            <b
                :class="
                    cn(
                        'hidden group-hover:text-orange-500 sm:inline',
                        currentLanguage === 'en' ? 'text-text' : 'text-disabled',
                    )
                ">
                EN
            </b>
        </button>
    </div>
</template>
