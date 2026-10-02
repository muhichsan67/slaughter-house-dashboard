<script setup>
import { ref } from 'vue';
import { postBarang } from '../services/api';

const emit = defineEmits(['refresh']);
const formData = ref({ nama: '', kategori: '', jumlah_stok: 0, lokasi_gudang: '' });

const simpanData = async () => {
  try {
    await postBarang(formData.value);
    formData.value = { nama: '', kategori: '', jumlah_stok: 0, lokasi_gudang: '' };
    emit('refresh');
  } catch (err) {
    alert(err.message);
  }
};
</script>

<template>
  <form @submit.prevent="simpanData" class="row g-2 mb-4 align-items-center">
    <div class="col-sm-3"><input v-model="formData.nama" type="text" class="form-control" placeholder="Nama Barang" required></div>
    <div class="col-sm-2"><input v-model="formData.kategori" type="text" class="form-control" placeholder="Kategori" required></div>
    <div class="col-sm-2"><input v-model.number="formData.jumlah_stok" type="number" min="0" class="form-control" placeholder="Stok" required></div>
    <div class="col-sm-3"><input v-model="formData.lokasi_gudang" type="text" class="form-control" placeholder="Lokasi" required></div>
    <div class="col-sm-2"><button type="submit" class="btn btn-primary w-100">Tambah</button></div>
  </form>
</template>