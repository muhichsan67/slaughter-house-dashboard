import { ref, watchEffect } from 'vue';

const read = () => {
  try {
    return localStorage.getItem('theme');
  } catch {
    return null;
  }
};

const initial =
  read() ||
  (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');

const theme = ref(initial);

watchEffect(() => {
  document.documentElement.dataset.theme = theme.value;
});

export function useTheme() {
  const toggle = () => {
    theme.value = theme.value === 'dark' ? 'light' : 'dark';
    try {
      localStorage.setItem('theme', theme.value);
    } catch {
      /* abaikan bila storage diblokir */
    }
  };
  return { theme, toggle };
}
