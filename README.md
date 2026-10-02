# Mini Dashboard Full-Stack: Inventaris Gudang RPA

Proyek ini dibangun untuk memenuhi tugas Ujian Tengah Semester (UTS) mata kuliah Web Application Development (Soal B - Dashboard Inventaris untuk NIM Genap)[cite: 1, 3]. 

Aplikasi ini dirancang dengan struktur yang ramah pemula (*newbie-friendly*), menggunakan **FastAPI** di sisi Backend dan **Vue 3 (Composition API + Vite)** di sisi Frontend. Tampilan antarmuka mengandalkan class bawaan **Bootstrap 5** melalui CDN.

## 🚀 Fitur Utama
- **Dashboard Ringkasan:** Menampilkan 4 tile metrik (Total Barang, Stok Menipis, Jumlah Kategori, Total Unit) yang dihitung secara dinamis menggunakan *computed properties* native[cite: 1, 3].
- **Pencarian & Filter:** Filter data secara asinkron berdasarkan Nama Barang atau Kategori[cite: 3].
- **Pengurutan (Sorting):** Urutkan barang dari A-Z atau Z-A berdasarkan nama barang menggunakan computed berantai[cite: 3].
- **Manajemen Data (CRUD):** Tambah data baru, Hapus data, dan Edit data (Fitur Bonus) menggunakan tampilan Popup Modal native dari Bootstrap[cite: 2, 4].
- **Indikator Status Stok:** Badge warna dinamis berdasarkan ambang batas stok[cite: 1, 3].
- **Responsif:** Tampilan UI optimal di perangkat Desktop, Tablet, maupun Mobile menggunakan sistem Grid Bootstrap[cite: 2].

## 📊 Ambang Batas (Threshold) Status Stok
Berdasarkan ketentuan operasional gudang inventaris[cite: 3], status stok dikategorikan sebagai berikut:
- 🔴 **Habis (Stok == 0):** Barang sama sekali tidak tersedia di gudang. Operasional atau produksi yang membutuhkan barang ini terhenti.
- 🟡 **Menipis (Stok 1 - 20):** Mencapai batas *buffer* / *safety stock*. Membutuhkan tindakan pemesanan ulang (restock) segera ke supplier RPA.
- 🟢 **Aman (Stok > 20):** Ketersediaan barang dalam batas wajar untuk memenuhi kebutuhan produksi.

---

## 🛠️ Prasyarat
Pastikan Anda telah menginstal perangkat lunak berikut di komputer Anda:
- [Python 3.8+](https://www.python.org/downloads/) (Untuk menjalankan Backend)
- [Node.js 16+](https://nodejs.org/) (Untuk menjalankan Frontend)

---

## ⚙️️ Cara Menjalankan Aplikasi

### 1. Menjalankan Backend (FastAPI)
Backend menangani logika REST API dan menggunakan penyimpanan *in-memory* berbasis Python List yang dimuat dari file `data.json`[cite: 2].

1. Buka terminal dan masuk ke folder backend:
```bash
cd backend
```

2. (Opsional namun disarankan) Buat dan aktifkan *Virtual Environment*:
* **Windows:**
```bash
python -m venv venv
venv\Scripts\activate

```


* **Mac/Linux:**
```bash
python -m venv venv
source venv/bin/activate

```




3. Instal library yang dibutuhkan:
```bash
pip install fastapi uvicorn pydantic

```


4. Jalankan server lokal:
```bash
uvicorn main:app --reload

```


Backend akan berjalan di `http://127.0.0.1:8000`. Anda bisa mengakses dokumentasi API interaktif di `http://127.0.0.1:8000/docs`.



### 2. Menjalankan Frontend (Vue 3 + Vite)

Frontend menangani antarmuka pengguna (UI) dan berkomunikasi dengan backend melalui Fetch API bawaan browser tanpa library tambahan. Seluruh logika *state management* dipusatkan di `App.vue`.

1. Buka **terminal baru** (biarkan terminal backend tetap berjalan) dan masuk ke folder frontend:
```bash
cd frontend

```


2. Instal semua dependencies node:
```bash
npm install

```


3. Jalankan server pengembangan:
```bash
npm run dev

```


*Aplikasi frontend dapat diakses melalui browser pada tautan yang diberikan di terminal (biasanya `http://localhost:5173`).*

---

## 📁 Struktur Proyek

Proyek ini memisahkan UI dan API secara rapi dengan arsitektur yang disederhanakan:

```text
warehouse-dashboard/
├── backend/
│   ├── main.py              # Entry point FastAPI & konfigurasi CORS
│   ├── model.py             # Skema Pydantic untuk validasi tipe data request/response
│   ├── database.py          # Logika penyimpanan in-memory & muat data seed JSON
│   ├── route.py             # Endpoint API REST (GET, POST, PUT, DELETE)
│   └── data.json            # 20 Data seed awal buatan sendiri
├── frontend/
│   ├── index.html           # File HTML utama (memuat Bootstrap 5 via CDN)
│   ├── src/
│   │   ├── main.js          # Inisialisasi aplikasi Vue (tanpa import CSS eksternal)
│   │   ├── App.vue          # Halaman utama pusat logika (State, fetch, modal actions)
│   │   ├── services/
│   │   │   └── api.js       # Kumpulan fungsi HTTP (Fetch API) ke server backend
│   │   └── components/
│   │       ├── DashboardStats.vue  # Komponen 4 Tile Ringkasan statis (menerima props)
│   │       ├── InventoryList.vue   # Komponen Tabel daftar, Filter, Sort
│   │       └── InventoryModal.vue  # Komponen Popup Form untuk Tambah & Edit
│   ├── package.json
│   └── vite.config.js
└── README.md

```

## 📝 Catatan Penting

* Pastikan server backend terus berjalan di *background* saat Anda membuka dan menggunakan aplikasi frontend agar fungsi CRUD dan penampilan data berjalan lancar.
* Konfigurasi CORS telah diaktifkan di sisi backend sehingga frontend lokal (`localhost` atau `127.0.0.1`) tidak akan diblokir oleh peramban (browser).


* Peringatan aksi penghapusan dan penyimpanan data menggunakan fungsi *native* `alert()` dan `confirm()` bawaan browser untuk menjaga kode tetap sederhana dan ringan.

```

```