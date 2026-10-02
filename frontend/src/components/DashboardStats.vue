<script setup>
import { computed } from 'vue';

const props = defineProps(['barangList']);

const totalBarang = computed(() => props.barangList.length);
const stokBermasalah = computed(() => props.barangList.filter(b => b.jumlah_stok <= 20).length);
const jumlahKategori = computed(() => new Set(props.barangList.map(b => b.kategori)).size);
const totalUnit = computed(() => props.barangList.reduce((acc, b) => acc + b.jumlah_stok, 0));
</script>

<template>
  <div class="row mb-4">
    <div class="col-md-3 col-sm-6 mb-2">
      <div class="card bg-primary text-white text-center p-3">
        <h5>Total Barang</h5><h3>{{ totalBarang }}</h3>
      </div>
    </div>
    <div class="col-md-3 col-sm-6 mb-2">
      <div class="card bg-warning text-dark text-center p-3">
        <h5>Stok Menipis/Habis</h5><h3>{{ stokBermasalah }}</h3>
      </div>
    </div>
    <div class="col-md-3 col-sm-6 mb-2">
      <div class="card bg-success text-white text-center p-3">
        <h5>Jumlah Kategori</h5><h3>{{ jumlahKategori }}</h3>
      </div>
    </div>
    <div class="col-md-3 col-sm-6 mb-2">
      <div class="card bg-info text-white text-center p-3">
        <h5>Total Unit</h5><h3>{{ totalUnit }}</h3>
      </div>
    </div>
  </div>
</template>