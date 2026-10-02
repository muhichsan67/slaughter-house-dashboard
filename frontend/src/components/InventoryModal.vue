<script setup>
import { ref, watch, nextTick, onBeforeUnmount } from 'vue';
import AppIcon from './AppIcon.vue';
import { postBarang, putBarang } from '../services/api';
import { toast } from '../composables/useFeedback';
import { getStatus } from '../constants';

const props = defineProps({
  show: { type: Boolean, default: false },
  editData: { type: Object, default: null },
  categories: { type: Array, default: () => [] },
  locations: { type: Array, default: () => [] },
});
const emit = defineEmits(['close', 'refresh']);

const emptyForm = () => ({ nama: '', kategori: '', jumlah_stok: 0, lokasi_gudang: '' });

const formData = ref(emptyForm());
const isEdit = ref(false);
const isSaving = ref(false);
const firstInput = ref(null);
const dialogEl = ref(null);
let lastFocused = null;

const close = () => {
  if (!isSaving.value) emit('close');
};

const onKey = (e) => {
  if (e.key === 'Escape') return close();
  if (e.key !== 'Tab' || !dialogEl.value) return;

  // Jaga fokus tetap di dalam dialog
  const items = dialogEl.value.querySelectorAll(
    'button:not([disabled]), input:not([disabled]), select:not([disabled]), [href]'
  );
  if (!items.length) return;
  const first = items[0];
  const last = items[items.length - 1];
  if (e.shiftKey && document.activeElement === first) {
    e.preventDefault();
    last.focus();
  } else if (!e.shiftKey && document.activeElement === last) {
    e.preventDefault();
    first.focus();
  }
};

// Form di-reset setiap kali dialog dibuka, jadi sisa ketikan sebelumnya tidak ikut terbawa
watch(
  () => props.show,
  async (open) => {
    if (open) {
      if (props.editData) {
        formData.value = { ...props.editData };
        isEdit.value = true;
      } else {
        formData.value = emptyForm();
        isEdit.value = false;
      }
      lastFocused = document.activeElement;
      document.addEventListener('keydown', onKey);
      document.documentElement.classList.add('modal-open');
      await nextTick();
      firstInput.value?.focus();
    } else {
      document.removeEventListener('keydown', onKey);
      document.documentElement.classList.remove('modal-open');
      lastFocused?.focus?.();
    }
  },
  { immediate: true }
);

onBeforeUnmount(() => {
  document.removeEventListener('keydown', onKey);
  document.documentElement.classList.remove('modal-open');
});

const adjustStok = (delta) => {
  formData.value.jumlah_stok = Math.max(0, (Number(formData.value.jumlah_stok) || 0) + delta);
};

const simpanData = async () => {
  if (isSaving.value) return;
  const payload = {
    ...formData.value,
    nama: formData.value.nama.trim(),
    kategori: formData.value.kategori.trim(),
    lokasi_gudang: formData.value.lokasi_gudang.trim(),
    jumlah_stok: Math.max(0, Number(formData.value.jumlah_stok) || 0),
  };

  isSaving.value = true;
  try {
    if (isEdit.value) {
      await putBarang(payload.id, payload);
      toast('Perubahan disimpan');
    } else {
      await postBarang(payload);
      toast('Barang ditambahkan');
    }
    emit('refresh');
    emit('close');
  } catch (err) {
    toast(err.message, 'error');
  } finally {
    isSaving.value = false;
  }
};
</script>

<template>
  <Teleport to="body">
    <Transition name="overlay">
      <div v-if="show" class="overlay overlay--sheet" @mousedown.self="close">
        <div ref="dialogEl" class="dialog" role="dialog" aria-modal="true" aria-labelledby="modal-title">
          <div class="dialog__head">
            <div>
              <h2 id="modal-title" class="dialog__title">{{ isEdit ? 'Edit barang' : 'Tambah barang' }}</h2>
              <p class="dialog__sub">
                {{ isEdit ? 'Perbarui data stok dan lokasi barang.' : 'Catat barang baru ke inventaris gudang.' }}
              </p>
            </div>
            <button type="button" class="btn btn--ghost btn--icon" aria-label="Tutup" @click="close">
              <AppIcon name="x" />
            </button>
          </div>

          <form class="form" @submit.prevent="simpanData">
            <div class="form__group">
              <label for="f-nama">Nama barang</label>
              <input
                id="f-nama"
                ref="firstInput"
                v-model="formData.nama"
                type="text"
                placeholder="Contoh: Karkas ayam utuh"
                autocomplete="off"
                required
              />
            </div>

            <div class="form__group">
              <label for="f-kategori">Kategori</label>
              <input
                id="f-kategori"
                v-model="formData.kategori"
                type="text"
                list="dl-kategori"
                placeholder="Contoh: Karkas"
                autocomplete="off"
                required
              />
              <datalist id="dl-kategori">
                <option v-for="c in categories" :key="c" :value="c" />
              </datalist>
            </div>

            <div class="form__row">
              <div class="form__group">
                <label for="f-stok">Jumlah stok</label>
                <div class="stepper">
                  <button type="button" class="stepper__btn" aria-label="Kurangi stok" @click="adjustStok(-1)">
                    <AppIcon name="minus" :size="16" />
                  </button>
                  <input id="f-stok" v-model.number="formData.jumlah_stok" type="number" min="0" inputmode="numeric" required />
                  <button type="button" class="stepper__btn" aria-label="Tambah stok" @click="adjustStok(1)">
                    <AppIcon name="plus" :size="16" />
                  </button>
                </div>
                <p class="form__hint">
                  Status:
                  <span class="badge badge--sm" :class="`badge--${getStatus(formData.jumlah_stok).key}`">
                    <span class="dot" :class="`dot--${getStatus(formData.jumlah_stok).key}`"></span>
                    {{ getStatus(formData.jumlah_stok).label }}
                  </span>
                </p>
              </div>

              <div class="form__group">
                <label for="f-lokasi">Lokasi gudang</label>
                <input
                  id="f-lokasi"
                  v-model="formData.lokasi_gudang"
                  type="text"
                  list="dl-lokasi"
                  placeholder="Contoh: Chiller A"
                  autocomplete="off"
                  required
                />
                <datalist id="dl-lokasi">
                  <option v-for="l in locations" :key="l" :value="l" />
                </datalist>
              </div>
            </div>

            <div class="dialog__actions">
              <button type="button" class="btn btn--ghost" :disabled="isSaving" @click="close">Batal</button>
              <button type="submit" class="btn btn--primary" :disabled="isSaving">
                <AppIcon v-if="isSaving" name="refresh" :size="16" class="spin" />
                {{ isSaving ? 'Menyimpan…' : isEdit ? 'Simpan perubahan' : 'Tambah barang' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>
