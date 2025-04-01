export function cn(...classes: (string | boolean)[]): string {
    return classes.filter(Boolean).join(' ');
}
