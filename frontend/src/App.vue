<script setup>
import { ref, onMounted } from 'vue';
import { fetchBarang } from './services/api';
import DashboardStats from './components/DashboardStats.vue';
import InventoryModal from './components/InventoryModal.vue';
import InventoryList from './components/InventoryList.vue';

const barangList = ref([]);
const isLoading = ref(false);
const errorMsg = ref('');

// State untuk Modal Modal
const showModal = ref(false);
const editData = ref(null);

const loadData = async () => {
  isLoading.value = true;
  errorMsg.value = '';
  try {
    barangList.value = await fetchBarang();
  } catch (error) {
    errorMsg.value = error.message;
  } finally {
    isLoading.value = false;
  }
};

const openAddModal = () => {
  editData.value = null; // Kosongkan data untuk form tambah baru
  showModal.value = true;
};

const openEditModal = (barang) => {
  editData.value = barang; // Oper data barang yang diklik ke modal
  showModal.value = true;
};

onMounted(() => loadData());
</script>

<template>
  <div class="container py-5">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <div>
        <h2 class="fw-bold mb-0">Inventaris Warehouse RPA</h2>
        <p class="text-muted">Manajemen stok karkas dan daging terpusat</p>
      </div>
      <button @click="openAddModal" class="btn btn-primary btn-lg rounded-pill shadow-sm px-4">
        <i class="bi bi-plus-lg me-2"></i> Tambah Barang
      </button>
    </div>
    
    <div v-if="isLoading" class="alert alert-info border-0 rounded-3"><i class="bi bi-hourglass-split me-2"></i>Memuat data dari server...</div>
    <div v-else-if="errorMsg" class="alert alert-danger border-0 rounded-3"><i class="bi bi-bug me-2"></i>{{ errorMsg }}</div>
    
    <DashboardStats :barangList="barangList" />
    
    <InventoryList 
      :barangList="barangList" 
      :isLoading="isLoading" 
      @refresh="loadData"
      @edit="openEditModal" 
    />

    <InventoryModal 
      :show="showModal" 
      :editData="editData" 
      @close="showModal = false" 
      @refresh="loadData" 
    />
  </div>
</template>