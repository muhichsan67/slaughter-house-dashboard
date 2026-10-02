<script setup>
import { ref, onMounted } from 'vue';
import { fetchBarang } from './services/api';
import DashboardStats from './components/DashboardStats.vue';
import InventoryForm from './components/InventoryForm.vue';
import InventoryList from './components/InventoryList.vue';

const barangList = ref([]);
const isLoading = ref(false);
const errorMsg = ref('');

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

onMounted(() => loadData());
</script>

<template>
  <div class="container py-4">
    <h1 class="mb-4">Dashboard Inventaris Gudang RPA</h1>
    
    <div v-if="isLoading" class="alert alert-info">Memuat data...</div>
    <div v-else-if="errorMsg" class="alert alert-danger">{{ errorMsg }}</div>
    
    <DashboardStats :barangList="barangList" />
    <InventoryForm @refresh="loadData" />
    <InventoryList :barangList="barangList" :isLoading="isLoading" @refresh="loadData" />
  </div>
</template>