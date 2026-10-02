import { reactive } from 'vue';

/* ---------- Toast ---------- */
export const toasts = reactive([]);
let toastId = 0;

export function dismissToast(id) {
  const i = toasts.findIndex((t) => t.id === id);
  if (i !== -1) toasts.splice(i, 1);
}

export function toast(message, type = 'success', duration = 3800) {
  const id = ++toastId;
  toasts.push({ id, message, type });
  if (duration > 0) setTimeout(() => dismissToast(id), duration);
  return id;
}

/* ---------- Dialog konfirmasi ---------- */
export const confirmState = reactive({
  open: false,
  title: '',
  message: '',
  confirmLabel: 'Ya',
  cancelLabel: 'Batal',
  danger: false,
  resolve: null,
});

export function confirmDialog(options = {}) {
  return new Promise((resolve) => {
    Object.assign(confirmState, {
      title: '',
      message: '',
      confirmLabel: 'Ya',
      cancelLabel: 'Batal',
      danger: false,
      ...options,
      open: true,
      resolve,
    });
  });
}

export function answerConfirm(value) {
  const resolve = confirmState.resolve;
  confirmState.open = false;
  confirmState.resolve = null;
  if (resolve) resolve(value);
}
