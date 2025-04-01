<script lang="ts">
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
            class="hover:bg-foreground group flex cursor-pointer items-center justify-center gap-2 rounded-md px-4 py-2 transition-all">
            <img src="@/assets/icons/br.png" :alt="$t('brazilianFlag')" width="32" />
            <b
                :class="
                    cn(
                        'group-hover:text-orange-500',
                        currentLanguage === 'pt' ? 'text-text' : 'text-disabled',
                    )
                ">
                PT
            </b>
        </button>
        <button
            @click="changeLanguage('en')"
            :title="$t('changeToEnglish')"
            class="hover:bg-foreground group flex cursor-pointer items-center justify-center gap-2 rounded-md px-4 py-2 transition-all">
            <img src="@/assets/icons/us.png" :alt="$t('englishFlag')" width="32" />
            <b
                :class="
                    cn(
                        'group-hover:text-orange-500',
                        currentLanguage === 'en' ? 'text-text' : 'text-disabled',
                    )
                ">
                EN
            </b>
        </button>
    </div>
</template>
