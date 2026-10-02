// Batas stok yang dianggap menipis (sama dengan logika lama: <= 20)
export const LOW_STOCK = 20;

export const STATUS = {
  aman: { key: 'aman', label: 'Aman' },
  menipis: { key: 'menipis', label: 'Menipis' },
  habis: { key: 'habis', label: 'Habis' },
};

export const getStatus = (stok) => {
  const n = Number(stok) || 0;
  if (n <= 0) return STATUS.habis;
  if (n <= LOW_STOCK) return STATUS.menipis;
  return STATUS.aman;
};

export const formatNumber = (n) => Number(n || 0).toLocaleString('id-ID');
