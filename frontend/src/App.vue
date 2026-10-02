<script setup>
import { ref, computed, onMounted } from 'vue';
import { fetchBarang } from './services/api';
import AppHeader from './components/AppHeader.vue';
import AppIcon from './components/AppIcon.vue';
import DashboardStats from './components/DashboardStats.vue';
import InventoryList from './components/InventoryList.vue';
import InventoryModal from './components/InventoryModal.vue';
import ToastHost from './components/ToastHost.vue';
import ConfirmDialog from './components/ConfirmDialog.vue';

const barangList = ref([]);
const isLoading = ref(false);
const errorMsg = ref('');

// State untuk modal tambah/edit
const showModal = ref(false);
const editData = ref(null);

const categories = computed(() => [...new Set(barangList.value.map((b) => b.kategori).filter(Boolean))].sort());
const locations = computed(() => [...new Set(barangList.value.map((b) => b.lokasi_gudang).filter(Boolean))].sort());

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
  <AppHeader @add="openAddModal" />

  <main class="page">
    <div class="page__intro">
      <h1>Inventaris gudang</h1>
      <p>Pantau stok karkas dan daging, lalu perbarui saat barang masuk atau keluar.</p>
    </div>

    <div v-if="errorMsg" class="banner banner--error" role="alert">
      <AppIcon name="alert" :size="20" />
      <div class="banner__body">
        <strong>{{ errorMsg }}</strong>
        <span>Periksa apakah server API sedang berjalan dan bisa dijangkau, lalu coba lagi.</span>
      </div>
      <button type="button" class="btn btn--ghost btn--sm" :disabled="isLoading" @click="loadData">
        <AppIcon name="refresh" :size="16" :class="{ spin: isLoading }" />
        Coba lagi
      </button>
    </div>

    <DashboardStats :barangList="barangList" :isLoading="isLoading" />

    <InventoryList
      :barangList="barangList"
      :isLoading="isLoading"
      @refresh="loadData"
      @edit="openEditModal"
      @add="openAddModal"
    />
  </main>

  <InventoryModal
    :show="showModal"
    :editData="editData"
    :categories="categories"
    :locations="locations"
    @close="showModal = false"
    @refresh="loadData"
  />

  <ConfirmDialog />
  <ToastHost />
</template>
