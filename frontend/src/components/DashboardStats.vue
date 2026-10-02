<script setup>
import { computed } from 'vue';

const props = defineProps(['barangList']);

const totalBarang = computed(() => props.barangList.length);
const stokBermasalah = computed(() => props.barangList.filter(b => b.jumlah_stok <= 20).length);
const jumlahKategori = computed(() => new Set(props.barangList.map(b => b.kategori)).size);
const totalUnit = computed(() => props.barangList.reduce((acc, b) => acc + b.jumlah_stok, 0));
</script>

<template>
  <div class="row g-3 mb-4">
    <div class="col-md-3 col-sm-6">
      <div class="card border-0 shadow-sm rounded-4 text-white" style="background: linear-gradient(135deg, #0d6efd, #0b5ed7);">
        <div class="card-body p-4 d-flex justify-content-between align-items-center">
          <div><p class="mb-1 text-white-50 small fw-bold text-uppercase">Total Barang</p><h2 class="mb-0 fw-bold">{{ totalBarang }}</h2></div>
          <i class="bi bi-box-seam fs-1 opacity-50"></i>
        </div>
      </div>
    </div>
    <div class="col-md-3 col-sm-6">
      <div class="card border-0 shadow-sm rounded-4 text-white" style="background: linear-gradient(135deg, #fd7e14, #d35400);">
        <div class="card-body p-4 d-flex justify-content-between align-items-center">
          <div><p class="mb-1 text-white-50 small fw-bold text-uppercase">Stok Menipis</p><h2 class="mb-0 fw-bold">{{ stokBermasalah }}</h2></div>
          <i class="bi bi-exclamation-triangle fs-1 opacity-50"></i>
        </div>
      </div>
    </div>
    <div class="col-md-3 col-sm-6">
      <div class="card border-0 shadow-sm rounded-4 text-white" style="background: linear-gradient(135deg, #198754, #146c43);">
        <div class="card-body p-4 d-flex justify-content-between align-items-center">
          <div><p class="mb-1 text-white-50 small fw-bold text-uppercase">Kategori</p><h2 class="mb-0 fw-bold">{{ jumlahKategori }}</h2></div>
          <i class="bi bi-tags fs-1 opacity-50"></i>
        </div>
      </div>
    </div>
    <div class="col-md-3 col-sm-6">
      <div class="card border-0 shadow-sm rounded-4 text-white" style="background: linear-gradient(135deg, #0dcaf0, #0bacbe);">
        <div class="card-body p-4 d-flex justify-content-between align-items-center">
          <div><p class="mb-1 text-white-50 small fw-bold text-uppercase">Total Unit</p><h2 class="mb-0 fw-bold">{{ totalUnit }}</h2></div>
          <i class="bi bi-boxes fs-1 opacity-50"></i>
        </div>
      </div>
    </div>
  </div>
</template>