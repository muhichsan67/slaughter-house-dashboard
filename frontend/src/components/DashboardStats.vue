<script setup>
import { computed } from 'vue';

const props = defineProps(['dataBarang']);

const totalBarang = computed(() => props.dataBarang.length);
const stokMenipis = computed(() => props.dataBarang.filter(b => b.jumlah_stok <= 20).length);
const totalUnit = computed(() => props.dataBarang.reduce((total, b) => total + b.jumlah_stok, 0));
const jumlahKategori = computed(() => {
  const kategoriUnik = [];
  props.dataBarang.forEach(b => {
    if (!kategoriUnik.includes(b.kategori)) kategoriUnik.push(b.kategori);
  });
  return kategoriUnik.length;
});
</script>

<template>
  <div class="row mb-4">
    <div class="col-md-3">
      <div class="card bg-primary text-white p-3 text-center">
        <h5>Total Barang</h5><h3>{{ totalBarang }}</h3>
      </div>
    </div>
    <div class="col-md-3">
      <div class="card bg-warning text-dark p-3 text-center">
        <h5>Stok Menipis</h5><h3>{{ stokMenipis }}</h3>
      </div>
    </div>
    <div class="col-md-3">
      <div class="card bg-success text-white p-3 text-center">
        <h5>Jumlah Kategori</h5><h3>{{ jumlahKategori }}</h3>
      </div>
    </div>
    <div class="col-md-3">
      <div class="card bg-info text-white p-3 text-center">
        <h5>Total Unit</h5><h3>{{ totalUnit }}</h3>
      </div>
    </div>
  </div>
</template>