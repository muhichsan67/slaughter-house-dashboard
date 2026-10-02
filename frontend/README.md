# Inventaris Gudang RPA — Frontend

Vue 3 + Vite. Tanpa dependensi UI tambahan (Bootstrap CDN sudah dihapus).

## Menjalankan

```bash
npm install
npm run dev
```

## Mengubah alamat API

Buat file `.env` di folder ini:

```
VITE_API_URL=http://192.168.1.10:8000/api/barang
```

Default-nya `http://127.0.0.1:8000/api/barang`. Saat mengetes dari HP, pakai IP komputer Anda di jaringan yang sama.

## Struktur

```
src/
  App.vue                  halaman utama
  constants.js             batas stok menipis (LOW_STOCK) & helper status
  style.css                design system (token warna, tema terang/gelap, responsif)
  components/
    AppHeader.vue          top bar, tombol tema & tambah barang
    AppIcon.vue            ikon SVG inline
    DashboardStats.vue     ringkasan kondisi stok
    InventoryList.vue      pencarian, filter, tabel/kartu, paginasi
    InventoryModal.vue     form tambah/edit
    ConfirmDialog.vue      pengganti confirm()
    ToastHost.vue          pengganti alert()
  composables/
    useFeedback.js         state toast & dialog konfirmasi
    useTheme.js            tema terang/gelap
  services/api.js          pemanggilan API (kontrak tidak berubah)
```
