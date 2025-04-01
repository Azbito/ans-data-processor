import { ref } from 'vue';

interface ToastOptions {
    message: string;
    type?: 'success' | 'error' | 'info';
    duration?: number;
}

const toastQueue = ref<ToastOptions[]>([]);
const currentToast = ref<ToastOptions | null>(null);
const isShowing = ref(false);

const DEFAULT_DURATION = 3000;

const showToast = (options: ToastOptions) => {
    const toast: ToastOptions = {
        message: options.message,
        type: options.type || 'info',
        duration: options.duration || DEFAULT_DURATION,
    };

    toastQueue.value.push(toast);
    showNextToast();
};

const showNextToast = () => {
    if (isShowing.value || toastQueue.value.length === 0) return;

    const nextToast = toastQueue.value.shift();
    if (!nextToast) return;

    currentToast.value = nextToast;
    isShowing.value = true;

    setTimeout(() => {
        currentToast.value = null;
        isShowing.value = false;
        showNextToast();
    }, nextToast.duration);
};

export const useToast = () => ({
    showToast,
    currentToast,
    isShowing,
});
