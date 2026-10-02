<script setup>
import { ref, onMounted } from 'vue';
import { fetchBarang, postBarang, putBarang, deleteBarang } from './services/api';
import DashboardStats from './components/DashboardStats.vue';
import InventoryList from './components/InventoryList.vue';
import InventoryModal from './components/InventoryModal.vue';

// State Utama
const barangList = ref([]);
const isLoading = ref(false);
const pesanError = ref('');

// State Modal (Popup)
const tampilkanModal = ref(false);
const dataYangDiedit = ref(null);

// Fungsi Ambil Data
const muatDataBarang = async () => {
  isLoading.value = true;
  pesanError.value = '';
  try {
    barangList.value = await fetchBarang();
  } catch (error) {
    pesanError.value = error.message;
  } finally {
    isLoading.value = false;
  }
};

// Fungsi Simpan Data (Tambah / Edit)
const simpanDataBarang = async (dataForm) => {
  try {
    if (dataForm.id) {
      await putBarang(dataForm.id, dataForm); // Mode Edit
    } else {
      await postBarang(dataForm); // Mode Tambah Baru
    }
    tampilkanModal.value = false;
    alert('Data berhasil disimpan!');
    await muatDataBarang(); // Refresh data di tabel
  } catch (error) {
    alert(error.message);
  }
};

// Fungsi Hapus Data
const hapusDataBarang = async (id) => {
  if (!confirm('Apakah Anda yakin ingin menghapus barang ini?')) return;
  try {
    await deleteBarang(id);
    alert('Data berhasil dihapus!');
    await muatDataBarang();
  } catch (error) {
    alert(error.message);
  }
};

// Navigasi Modal
const bukaModalTambah = () => {
  dataYangDiedit.value = null; // Pastikan form kosong
  tampilkanModal.value = true;
};

const bukaModalEdit = (barang) => {
  dataYangDiedit.value = barang; // Isi form dengan data yang dipilih
  tampilkanModal.value = true;
};

onMounted(() => {
  muatDataBarang();
});
</script>

<template>
  <div class="container py-5">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2>Dashboard Inventaris RPA</h2>
      <button @click="bukaModalTambah" class="btn btn-primary">
        + Tambah Barang Baru
      </button>
    </div>

    <!-- Pesan Status -->
    <div v-if="isLoading" class="alert alert-info">Sedang memuat data...</div>
    <div v-if="pesanError" class="alert alert-danger">{{ pesanError }}</div>

    <!-- 4 Kotak Ringkasan -->
    <DashboardStats :dataBarang="barangList" />

    <!-- Tabel Daftar Barang -->
    <InventoryList 
      :dataBarang="barangList" 
      @mintaEdit="bukaModalEdit"
      @mintaHapus="hapusDataBarang"
    />

    <!-- Popup Modal Form -->
    <InventoryModal 
      v-if="tampilkanModal"
      :dataEdit="dataYangDiedit"
      @tutupModal="tampilkanModal = false"
      @simpanData="simpanDataBarang"
    />
  </div>
</template>