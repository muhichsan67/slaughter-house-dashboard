<script setup>
import { ref, onMounted } from 'vue';

const props = defineProps(['dataEdit']);
const emit = defineEmits(['tutupModal', 'simpanData']);

const form = ref({
  nama: '',
  kategori: '',
  jumlah_stok: 0,
  lokasi_gudang: ''
});

// Jika ada data yang dikirim (Mode Edit), isikan ke dalam form
onMounted(() => {
  if (props.dataEdit) {
    form.value = { ...props.dataEdit };
  }
});

const kirimData = () => {
  emit('simpanData', form.value);
};
</script>

<template>
  <div class="modal fade show d-block" style="background-color: rgba(0,0,0,0.5);">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">{{ dataEdit ? 'Edit Barang' : 'Tambah Barang Baru' }}</h5>
          <button type="button" class="btn-close" @click="$emit('tutupModal')"></button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="kirimData">
            <div class="mb-3">
              <label>Nama Barang</label>
              <input v-model="form.nama" type="text" class="form-control" required>
            </div>
            <div class="mb-3">
              <label>Kategori</label>
              <input v-model="form.kategori" type="text" class="form-control" required>
            </div>
            <div class="mb-3">
              <label>Jumlah Stok</label>
              <input v-model="form.jumlah_stok" type="number" class="form-control" required>
            </div>
            <div class="mb-3">
              <label>Lokasi Gudang</label>
              <input v-model="form.lokasi_gudang" type="text" class="form-control" required>
            </div>
            <div class="d-flex justify-content-end mt-4">
              <button type="button" class="btn btn-secondary me-2" @click="$emit('tutupModal')">Batal</button>
              <button type="submit" class="btn btn-primary">Simpan Data</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>