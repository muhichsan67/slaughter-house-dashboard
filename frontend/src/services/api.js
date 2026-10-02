const API_URL = 'http://127.0.0.1:8000/api/barang';

export const fetchBarang = async () => {
  const res = await fetch(API_URL);
  if (!res.ok) throw new Error('Gagal mengambil data server');
  return res.json();
};

export const postBarang = async (data) => {
  const res = await fetch(API_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  });
  if (!res.ok) throw new Error('Gagal menambah data');
  return res.json();
};

export const deleteBarang = async (id) => {
  const res = await fetch(`${API_URL}/${id}`, { method: 'DELETE' });
  if (!res.ok) throw new Error('Gagal menghapus data');
  return res.json();
};