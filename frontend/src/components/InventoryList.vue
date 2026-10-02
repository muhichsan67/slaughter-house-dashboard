<script setup>
import { ref, computed } from 'vue';
import { deleteBarang } from '../services/api';

const props = defineProps(['barangList', 'isLoading']);
const emit = defineEmits(['refresh']);

const searchQuery = ref('');
const sortOrder = ref('asc');

const filteredAndSorted = computed(() => {
  let result = props.barangList.filter(b => 
    b.nama.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
    b.kategori.toLowerCase().includes(searchQuery.value.toLowerCase())
  );
  return result.sort((a, b) => sortOrder.value === 'asc' 
    ? a.nama.localeCompare(b.nama) 
    : b.nama.localeCompare(a.nama)
  );
});

const toggleSort = () => sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc';
const getBadgeClass = (stok) => stok === 0 ? 'bg-danger' : (stok <= 20 ? 'bg-warning text-dark' : 'bg-success');
const getBadgeText = (stok) => stok === 0 ? 'Habis' : (stok <= 20 ? 'Menipis' : 'Aman');

const hapusData = async (id) => {
  if(!confirm('Hapus?')) return;
  try {
    await deleteBarang(id);
    emit('refresh');
  } catch (err) {
    alert(err.message);
  }
};
</script>

<template>
  <div>
    <div class="d-flex flex-wrap gap-2 mb-3">
      <input v-model="searchQuery" type="text" class="form-control w-auto" placeholder="Cari nama/kategori...">
      <button @click="toggleSort" class="btn btn-secondary">Urutkan {{ sortOrder === 'asc' ? 'Z-A' : 'A-Z' }}</button>
    </div>

    <div v-if="filteredAndSorted.length === 0 && !isLoading" class="alert alert-warning">Data tidak ditemukan.</div>
    
    <div class="table-responsive" v-if="filteredAndSorted.length > 0">
      <table class="table table-striped align-middle">
        <thead class="table-dark">
          <tr><th>Nama</th><th>Kategori</th><th>Stok</th><th>Status</th><th>Lokasi</th><th>Aksi</th></tr>
        </thead>
        <tbody>
          <tr v-for="barang in filteredAndSorted" :key="barang.id">
            <td>{{ barang.nama }}</td><td>{{ barang.kategori }}</td><td>{{ barang.jumlah_stok }}</td>
            <td><span class="badge" :class="getBadgeClass(barang.jumlah_stok)">{{ getBadgeText(barang.jumlah_stok) }}</span></td>
            <td>{{ barang.lokasi_gudang }}</td>
            <td><button @click="hapusData(barang.id)" class="btn btn-sm btn-danger">Hapus</button></td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>