<script setup>
import { ref, watch } from 'vue';
import { postBarang, putBarang } from '../services/api';

const props = defineProps(['show', 'editData']);
const emit = defineEmits(['close', 'refresh']);

const formData = ref({ nama: '', kategori: '', jumlah_stok: 0, lokasi_gudang: '' });
const isEdit = ref(false);

watch(() => props.editData, (newVal) => {
  if (newVal) {
    formData.value = { ...newVal };
    isEdit.value = true;
  } else {
    formData.value = { nama: '', kategori: '', jumlah_stok: 0, lokasi_gudang: '' };
    isEdit.value = false;
  }
}, { immediate: true });

const simpanData = async () => {
  try {
    if (isEdit.value) {
      await putBarang(formData.value.id, formData.value);
    } else {
      await postBarang(formData.value);
    }
    emit('refresh');
    emit('close');
  } catch (err) {
    alert(err.message);
  }
};
</script>

<template>
  <div v-if="show" class="modal fade show d-block" tabindex="-1" style="background: rgba(0,0,0,0.5);">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content border-0 shadow-lg rounded-4">
        <div class="modal-header border-bottom-0">
          <h5 class="modal-title fw-bold">{{ isEdit ? 'Edit Barang' : 'Tambah Barang Baru' }}</h5>
          <button @click="$emit('close')" type="button" class="btn-close"></button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="simpanData">
            <div class="mb-3">
              <label class="form-label text-muted small">Nama Barang</label>
              <input v-model="formData.nama" type="text" class="form-control form-control-lg bg-light border-0" required>
            </div>
            <div class="mb-3">
              <label class="form-label text-muted small">Kategori</label>
              <input v-model="formData.kategori" type="text" class="form-control form-control-lg bg-light border-0" required>
            </div>
            <div class="row mb-4">
              <div class="col-6">
                <label class="form-label text-muted small">Jumlah Stok</label>
                <input v-model.number="formData.jumlah_stok" type="number" min="0" class="form-control form-control-lg bg-light border-0" required>
              </div>
              <div class="col-6">
                <label class="form-label text-muted small">Lokasi Gudang</label>
                <input v-model="formData.lokasi_gudang" type="text" class="form-control form-control-lg bg-light border-0" required>
              </div>
            </div>
            <div class="d-grid gap-2">
              <button type="submit" class="btn btn-primary btn-lg rounded-3">
                <i class="bi bi-save me-2"></i>Simpan Data
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>