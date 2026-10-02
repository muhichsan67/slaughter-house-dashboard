<script setup>
import { ref, computed } from 'vue';

const props = defineProps(['dataBarang']);
const emit = defineEmits(['mintaEdit', 'mintaHapus']);

const kataKunci = ref('');
const urutan = ref('asc');

const dataTampil = computed(() => {
  // 1. Filter Pencarian
  let hasil = props.dataBarang.filter(barang => 
    barang.nama.toLowerCase().includes(kataKunci.value.toLowerCase()) ||
    barang.kategori.toLowerCase().includes(kataKunci.value.toLowerCase())
  );

  // 2. Urutkan Data
  hasil.sort((a, b) => {
    if (urutan.value === 'asc') return a.nama.localeCompare(b.nama);
    else return b.nama.localeCompare(a.nama);
  });

  return hasil;
});

const ubahUrutan = () => {
  urutan.value = urutan.value === 'asc' ? 'desc' : 'asc';
};
</script>

<template>
  <div class="card p-3 shadow-sm mb-4">
    <div class="d-flex justify-content-between mb-3">
      <input v-model="kataKunci" type="text" class="form-control w-50" placeholder="Cari nama atau kategori...">
      <button @click="ubahUrutan" class="btn btn-secondary">
        Urutkan {{ urutan === 'asc' ? 'Z-A' : 'A-Z' }}
      </button>
    </div>

    <table class="table table-bordered table-hover">
      <thead class="table-light">
        <tr>
          <th>Nama Barang</th>
          <th>Kategori</th>
          <th>Stok</th>
          <th>Lokasi</th>
          <th>Aksi</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="barang in dataTampil" :key="barang.id">
          <td>{{ barang.nama }}</td>
          <td>{{ barang.kategori }}</td>
          <td>
            {{ barang.jumlah_stok }} 
            <span v-if="barang.jumlah_stok === 0" class="badge bg-danger">Habis</span>
            <span v-else-if="barang.jumlah_stok <= 20" class="badge bg-warning text-dark">Menipis</span>
            <span v-else class="badge bg-success">Aman</span>
          </td>
          <td>{{ barang.lokasi_gudang }}</td>
          <td>
            <button @click="$emit('mintaEdit', barang)" class="btn btn-sm btn-primary me-2">Edit</button>
            <button @click="$emit('mintaHapus', barang.id)" class="btn btn-sm btn-danger">Hapus</button>
          </td>
        </tr>
        <tr v-if="dataTampil.length === 0">
          <td colspan="5" class="text-center text-muted">Data tidak ditemukan.</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>