# Inventaris Gudang RPA

Aplikasi web untuk mengelola stok karkas dan daging di gudang secara terpusat. Staf gudang bisa melihat kondisi stok sekilas, mencari barang, lalu menambah, mengubah, atau menghapus data saat barang masuk dan keluar.

Proyek ini terdiri dari dua bagian yang dijalankan terpisah:

- **Frontend**: Vue 3 + Vite, antarmuka responsif dengan mode terang/gelap.
- **Backend**: REST API dengan FastAPI (Python). Data dimuat dari `data.json` ke memori saat server menyala.

## Daftar isi

- [Fitur](#fitur)
- [Teknologi](#teknologi)
- [Struktur proyek](#struktur-proyek)
- [Prasyarat](#prasyarat)
- [Cara menjalankan](#cara-menjalankan)
- [Konfigurasi](#konfigurasi)
- [Dokumentasi API](#dokumentasi-api)
- [Build untuk produksi](#build-untuk-produksi)
- [Mengakses dari HP](#mengakses-dari-hp)
- [Pemecahan masalah](#pemecahan-masalah)
- [Catatan dan keterbatasan](#catatan-dan-keterbatasan)

## Fitur

- **Ringkasan kondisi stok**: bar distribusi Aman / Menipis / Habis, ditambah total barang, total unit, jumlah kategori, dan jumlah barang yang perlu restok.
- **Daftar barang**: pencarian (nama, kategori, lokasi), filter kategori, filter status stok, empat pilihan urutan, dan paginasi 10 baris per halaman.
- **Bar level stok**: setiap barang punya bar level dengan garis penanda batas menipis.
- **Tambah dan edit barang**: form dengan tombol +/− untuk stok, serta saran kategori dan lokasi dari data yang sudah ada.
- **Hapus dengan konfirmasi**: dialog konfirmasi sebelum data dihapus, lalu notifikasi (toast) hasilnya.
- **Responsif**: di layar kecil tabel berubah menjadi kartu, dan form tampil sebagai bottom sheet.
- **Mode terang dan gelap**: mengikuti pengaturan perangkat, bisa diganti manual, dan pilihannya diingat.
- **Status loading, kosong, dan error** yang jelas, lengkap dengan tombol "Coba lagi".

Status stok ditentukan seperti ini:

| Status  | Kondisi        |
| ------- | -------------- |
| Aman    | stok lebih dari 20 |
| Menipis | stok 1 sampai 20   |
| Habis   | stok 0             |

Batas 20 bisa diubah lewat konstanta `LOW_STOCK` di `frontend/src/constants.js`.

## Teknologi

| Bagian   | Teknologi |
| -------- | --------- |
| Frontend | Vue 3 (`<script setup>`), Vite, CSS murni (tanpa library UI) |
| Backend  | Python, FastAPI, Pydantic, Uvicorn |
| Data     | File `data.json` yang dimuat ke memori |

## Struktur proyek

Struktur di bawah mengasumsikan frontend dan backend berada dalam satu repositori. Sesuaikan nama folder backend dengan yang Anda pakai.

```
slaughter-house-dashboard/
├── backend/
│   ├── main.py          # entry point FastAPI, CORS, dan startup event
│   ├── route.py         # endpoint CRUD barang
│   ├── model.py         # model data Barang (Pydantic)
│   ├── database.py      # penyimpanan in-memory dan pemuat data.json
│   └── data.json        # data awal (20 barang contoh)
├── frontend/
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   └── src/
│       ├── App.vue                  # halaman utama
│       ├── constants.js             # batas stok menipis dan helper status
│       ├── style.css                # token desain, tema, dan responsif
│       ├── components/
│       │   ├── AppHeader.vue        # top bar, tombol tema dan tambah barang
│       │   ├── AppIcon.vue          # ikon SVG inline
│       │   ├── DashboardStats.vue   # ringkasan kondisi stok
│       │   ├── InventoryList.vue    # pencarian, filter, tabel/kartu, paginasi
│       │   ├── InventoryModal.vue   # form tambah dan edit
│       │   ├── ConfirmDialog.vue    # dialog konfirmasi hapus
│       │   └── ToastHost.vue        # notifikasi
│       ├── composables/
│       │   ├── useFeedback.js       # state toast dan dialog konfirmasi
│       │   └── useTheme.js          # tema terang/gelap
│       └── services/api.js          # pemanggilan API
└── README.md
```

## Prasyarat

- **Python** 3.10 atau lebih baru
- **Node.js** `^20.19.0` atau `>=22.12.0` (persyaratan Vite yang dipakai proyek ini) beserta npm
- **Git** (opsional, untuk mengunduh repositori)

Cek versi yang terpasang:

```bash
python --version
node --version
npm --version
```

## Cara menjalankan

Backend dan frontend dijalankan di dua terminal terpisah. **Jalankan backend lebih dulu.**

### 1. Unduh proyek

```bash
git clone https://github.com/muhichsan67/slaughter-house-dashboard.git
cd slaughter-house-dashboard
```

### 2. Jalankan backend

Buka terminal pertama, lalu masuk ke folder backend:

```bash
cd backend
```

Buat dan aktifkan virtual environment:

```bash
# Windows (PowerShell)
python -m venv .venv
.venv\Scripts\Activate.ps1

# Windows (Command Prompt)
python -m venv .venv
.venv\Scripts\activate.bat

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
```

Pasang dependensi:

```bash
pip install fastapi "uvicorn[standard]"
```

Jalankan server:

```bash
uvicorn main:app --reload
```

> **Penting:** jalankan perintah ini dari dalam folder yang berisi `main.py` dan `data.json`. Backend membaca `data.json` lewat path relatif, sehingga kalau dijalankan dari folder lain, daftar barang akan kosong tanpa pesan error.

Backend sekarang aktif di `http://127.0.0.1:8000`. Untuk memastikannya, buka salah satu alamat ini di browser:

- `http://127.0.0.1:8000/api/barang/` menampilkan data barang dalam format JSON.
- `http://127.0.0.1:8000/docs` menampilkan dokumentasi API interaktif (Swagger UI) yang dibuat otomatis oleh FastAPI.

### 3. Jalankan frontend

Buka terminal kedua, lalu masuk ke folder frontend:

```bash
cd frontend
npm install
npm run dev
```

Buka alamat yang ditampilkan di terminal, biasanya `http://localhost:5173`. Jika backend berjalan, tabel akan langsung terisi 20 barang contoh dari `data.json`.

### Menghentikan aplikasi

Tekan `Ctrl + C` di masing-masing terminal. Untuk keluar dari virtual environment Python, jalankan `deactivate`.

## Konfigurasi

### Alamat API (frontend)

Secara bawaan, frontend memanggil `http://127.0.0.1:8000/api/barang`. Untuk mengubahnya, buat file `.env` di folder `frontend`:

```env
VITE_API_URL=http://127.0.0.1:8001/api/barang
```

Restart `npm run dev` setelah mengubah file `.env`.

### Port backend

Untuk memakai port lain:

```bash
uvicorn main:app --reload --port 8001
```

Jangan lupa menyesuaikan `VITE_API_URL` di frontend.

## Dokumentasi API

Base URL: `http://127.0.0.1:8000/api/barang`

| Method   | Endpoint | Fungsi |
| -------- | -------- | ------ |
| `GET`    | `/`      | Mengambil semua barang |
| `POST`   | `/`      | Menambah barang baru |
| `PUT`    | `/{id}`  | Mengubah barang berdasarkan ID |
| `DELETE` | `/{id}`  | Menghapus barang berdasarkan ID |

Permintaan ke `/api/barang` tanpa garis miring di akhir otomatis dialihkan FastAPI ke `/api/barang/`.

### Model data Barang

| Field           | Tipe    | Keterangan |
| --------------- | ------- | ---------- |
| `id`            | integer | Dibuat otomatis oleh server (ID terbesar saat ini + 1). Diabaikan pada `POST` dan `PUT`. |
| `nama`          | string  | Nama barang |
| `kategori`      | string  | Contoh: `Daging Unggas`, `Daging Merah`, `Jeroan` |
| `jumlah_stok`   | integer | Jumlah stok dalam unit |
| `lokasi_gudang` | string  | Contoh: `Cold Storage A` |

### Contoh penggunaan

**Mengambil semua barang**

```bash
curl http://127.0.0.1:8000/api/barang/
```

```json
[
  {
    "id": 1,
    "nama": "Karkas Ayam Utuh",
    "kategori": "Daging Unggas",
    "jumlah_stok": 50,
    "lokasi_gudang": "Cold Storage A"
  }
]
```

**Menambah barang**

```bash
curl -X POST http://127.0.0.1:8000/api/barang/ \
  -H "Content-Type: application/json" \
  -d '{"nama": "Ati Ayam", "kategori": "Jeroan", "jumlah_stok": 35, "lokasi_gudang": "Cold Storage C"}'
```

```json
{
  "message": "Data berhasil ditambahkan",
  "data": {
    "id": 21,
    "nama": "Ati Ayam",
    "kategori": "Jeroan",
    "jumlah_stok": 35,
    "lokasi_gudang": "Cold Storage C"
  }
}
```

**Mengubah barang**

```bash
curl -X PUT http://127.0.0.1:8000/api/barang/21 \
  -H "Content-Type: application/json" \
  -d '{"nama": "Ati Ayam", "kategori": "Jeroan", "jumlah_stok": 10, "lokasi_gudang": "Cold Storage C"}'
```

Respons berhasil: `{"message": "Data berhasil diubah", "data": {...}}`

**Menghapus barang**

```bash
curl -X DELETE http://127.0.0.1:8000/api/barang/21
```

Respons berhasil: `{"message": "Data berhasil dihapus", "data": {...}}`

### Kode respons

| Kode  | Arti |
| ----- | ---- |
| `200` | Berhasil |
| `404` | Barang dengan ID tersebut tidak ditemukan (`{"detail": "Barang tidak ditemukan"}`) |
| `422` | Body request tidak valid, misalnya field kurang atau tipe data salah |

## Build untuk produksi

Untuk frontend:

```bash
cd frontend
npm run build      # hasil ada di folder dist/
npm run preview    # mencoba hasil build secara lokal
```

Isi folder `dist/` bisa disajikan oleh web server statis apa pun. Pastikan `VITE_API_URL` sudah mengarah ke alamat backend yang benar **sebelum** menjalankan `npm run build`, karena nilainya ditanam saat build.

Untuk backend, jalankan Uvicorn tanpa `--reload`:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

## Mengakses dari HP

Agar aplikasi bisa dibuka dari HP di jaringan Wi-Fi yang sama:

1. Cari alamat IP komputer Anda di jaringan lokal (misalnya `192.168.1.10`). Di Windows pakai `ipconfig`, di macOS/Linux pakai `ifconfig` atau `ip a`.
2. Jalankan backend agar bisa dijangkau dari perangkat lain:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0
   ```
3. Buat `frontend/.env` dengan IP komputer tersebut. `127.0.0.1` di HP merujuk ke HP itu sendiri, bukan komputer Anda.
   ```env
   VITE_API_URL=http://192.168.1.10:8000/api/barang
   ```
4. Jalankan frontend agar bisa dijangkau dari perangkat lain:
   ```bash
   npm run dev -- --host
   ```
5. Di HP, buka `http://192.168.1.10:5173` (ganti dengan IP dan port yang ditampilkan Vite).

Jika tidak bisa terhubung, periksa firewall komputer dan pastikan kedua perangkat berada di jaringan yang sama.

## Pemecahan masalah

**Muncul banner "Gagal mengambil data server"**
Frontend tidak bisa menghubungi backend. Pastikan backend berjalan, lalu buka `http://127.0.0.1:8000/docs` di browser. Jika halaman itu tidak terbuka, backend belum aktif atau memakai port lain. Periksa juga nilai `VITE_API_URL` jika Anda memakai file `.env`.

**Tabel kosong, tetapi tidak ada error**
Kemungkinan besar Uvicorn dijalankan dari folder yang tidak berisi `data.json`. Hentikan server, masuk ke folder `backend`, lalu jalankan ulang `uvicorn main:app --reload`.

**`uvicorn` atau `pip` tidak dikenali**
Virtual environment belum aktif. Jalankan perintah aktivasi pada langkah [Jalankan backend](#2-jalankan-backend). Jika tetap gagal, coba `python -m uvicorn main:app --reload`.

**Error saat mengaktifkan venv di PowerShell ("running scripts is disabled")**
Jalankan perintah ini sekali, lalu coba lagi:
```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

**Port 8000 atau 5173 sudah dipakai**
Jalankan backend dengan `--port` lain dan sesuaikan `VITE_API_URL`. Vite otomatis memilih port berikutnya jika 5173 terpakai.

**Perubahan di `.env` tidak berpengaruh**
Restart `npm run dev`. Vite hanya membaca file `.env` saat dijalankan.

**`npm install` gagal karena versi Node**
Perbarui Node.js ke versi yang memenuhi `^20.19.0` atau `>=22.12.0`.

**Muncul peringatan *deprecated* di terminal backend**
Kode backend memakai `@app.on_event("startup")` dan `.dict()` yang sudah ditandai usang di FastAPI/Pydantic versi baru. Aplikasi tetap berjalan normal.

## Catatan dan keterbatasan

- **Data tidak tersimpan permanen.** Backend menyimpan data di memori. Perubahan (tambah, ubah, hapus) hilang saat server di-restart, dan data kembali ke isi `data.json`. Dengan opsi `--reload`, server juga restart otomatis setiap ada file Python yang berubah.
- **Belum ada autentikasi.** Siapa pun yang bisa menjangkau API dapat mengubah dan menghapus data.
- **CORS terbuka untuk semua origin** (`allow_origins=["*"]`). Ini praktis untuk pengembangan, tetapi sebaiknya dibatasi ke alamat frontend Anda saat dipakai di server sungguhan.
- **Validasi stok ada di frontend.** Form mencegah stok negatif, sedangkan API sendiri hanya memeriksa bahwa `jumlah_stok` berupa angka bulat.