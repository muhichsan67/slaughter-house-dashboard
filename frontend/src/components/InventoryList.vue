<script setup>
import { ref, computed } from 'vue';
import { deleteBarang } from '../services/api';

const props = defineProps(['barangList', 'isLoading']);
const emit = defineEmits(['refresh', 'edit']);

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
  if(!confirm('Yakin ingin menghapus data ini?')) return;
  try {
    await deleteBarang(id);
    emit('refresh');
  } catch (err) {
    alert(err.message);
  }
};
</script>

<template>
  <div class="bg-white p-4 rounded-4 shadow-sm border border-light">
    <div class="d-flex flex-column flex-md-row justify-content-between gap-3 mb-4">
      <div class="position-relative flex-grow-1" style="max-width: 400px;">
        <i class="bi bi-search position-absolute top-50 start-0 translate-middle-y ms-3 text-muted"></i>
        <input v-model="searchQuery" type="text" class="form-control form-control-lg bg-light border-0 ps-5" placeholder="Cari nama atau kategori...">
      </div>
      <button @click="toggleSort" class="btn btn-light border px-4 shadow-sm">
        <i class="bi bi-sort-alpha-down"></i> Urutkan {{ sortOrder === 'asc' ? 'Z-A' : 'A-Z' }}
      </button>
    </div>

    <div v-if="filteredAndSorted.length === 0 && !isLoading" class="text-center py-5 text-muted">
      <i class="bi bi-inbox fs-1 d-block mb-2"></i>
      Data tidak ditemukan.
    </div>
    
    <div class="table-responsive" v-if="filteredAndSorted.length > 0">
      <table class="table table-hover align-middle mb-0">
        <thead class="table-light">
          <tr>
            <th class="border-0 rounded-start">Nama Barang</th>
            <th class="border-0">Kategori</th>
            <th class="border-0">Stok</th>
            <th class="border-0">Status</th>
            <th class="border-0">Lokasi</th>
            <th class="border-0 rounded-end text-end">Aksi</th>
          </tr>
        </thead>
        <tbody class="border-top-0">
          <tr v-for="barang in filteredAndSorted" :key="barang.id">
            <td class="fw-semibold">{{ barang.nama }}</td>
            <td><span class="text-muted">{{ barang.kategori }}</span></td>
            <td class="fw-bold">{{ barang.jumlah_stok }}</td>
            <td><span class="badge rounded-pill px-3 py-2" :class="getBadgeClass(barang.jumlah_stok)">{{ getBadgeText(barang.jumlah_stok) }}</span></td>
            <td>{{ barang.lokasi_gudang }}</td>
            <td class="text-end">
              <button @click="$emit('edit', barang)" class="btn btn-sm btn-outline-primary rounded-3 me-2">
                <i class="bi bi-pencil-square"></i>
              </button>
              <button @click="hapusData(barang.id)" class="btn btn-sm btn-outline-danger rounded-3">
                <i class="bi bi-trash3"></i>
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>