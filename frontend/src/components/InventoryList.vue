<script setup>
import { ref, computed, watch } from 'vue';
import AppIcon from './AppIcon.vue';
import { deleteBarang } from '../services/api';
import { confirmDialog, toast } from '../composables/useFeedback';
import { LOW_STOCK, getStatus, formatNumber } from '../constants';

const props = defineProps({
  barangList: { type: Array, default: () => [] },
  isLoading: { type: Boolean, default: false },
});
const emit = defineEmits(['refresh', 'edit', 'add']);

const PAGE_SIZE = 10;

const searchQuery = ref('');
const categoryFilter = ref('all');
const statusFilter = ref('all');
const sortKey = ref('nama-asc');
const page = ref(1);
const deletingId = ref(null);

const sortOptions = [
  { value: 'nama-asc', label: 'Nama A–Z' },
  { value: 'nama-desc', label: 'Nama Z–A' },
  { value: 'stok-asc', label: 'Stok terendah' },
  { value: 'stok-desc', label: 'Stok tertinggi' },
];

const statusTabs = [
  { value: 'all', label: 'Semua' },
  { value: 'aman', label: 'Aman' },
  { value: 'menipis', label: 'Menipis' },
  { value: 'habis', label: 'Habis' },
];

const categories = computed(() =>
  [...new Set(props.barangList.map((b) => b.kategori).filter(Boolean))].sort((a, b) => a.localeCompare(b))
);

const statusCounts = computed(() => {
  const c = { all: props.barangList.length, aman: 0, menipis: 0, habis: 0 };
  props.barangList.forEach((b) => c[getStatus(b.jumlah_stok).key]++);
  return c;
});

// Skala bar stok: relatif terhadap stok terbesar (minimal 2x batas menipis)
const maxStok = computed(() =>
  props.barangList.reduce((m, b) => Math.max(m, Number(b.jumlah_stok) || 0), LOW_STOCK * 2)
);
const tickPercent = computed(() => (LOW_STOCK / maxStok.value) * 100);
const fillPercent = (stok) => Math.min(100, Math.max(0, ((Number(stok) || 0) / maxStok.value) * 100));

const filtered = computed(() => {
  const q = searchQuery.value.trim().toLowerCase();
  const result = props.barangList.filter((b) => {
    const matchQ =
      !q ||
      (b.nama ?? '').toLowerCase().includes(q) ||
      (b.kategori ?? '').toLowerCase().includes(q) ||
      (b.lokasi_gudang ?? '').toLowerCase().includes(q);
    const matchCat = categoryFilter.value === 'all' || b.kategori === categoryFilter.value;
    const matchStatus = statusFilter.value === 'all' || getStatus(b.jumlah_stok).key === statusFilter.value;
    return matchQ && matchCat && matchStatus;
  });

  const [key, dir] = sortKey.value.split('-');
  const sign = dir === 'asc' ? 1 : -1;
  return result.sort((a, b) =>
    key === 'nama'
      ? sign * (a.nama ?? '').localeCompare(b.nama ?? '')
      : sign * ((Number(a.jumlah_stok) || 0) - (Number(b.jumlah_stok) || 0))
  );
});

const totalPages = computed(() => Math.max(1, Math.ceil(filtered.value.length / PAGE_SIZE)));
const pageItems = computed(() => filtered.value.slice((page.value - 1) * PAGE_SIZE, page.value * PAGE_SIZE));
const rangeStart = computed(() => (filtered.value.length ? (page.value - 1) * PAGE_SIZE + 1 : 0));
const rangeEnd = computed(() => Math.min(page.value * PAGE_SIZE, filtered.value.length));

const hasActiveFilter = computed(
  () => searchQuery.value.trim() !== '' || categoryFilter.value !== 'all' || statusFilter.value !== 'all'
);

watch([searchQuery, categoryFilter, statusFilter, sortKey], () => (page.value = 1));
watch(totalPages, (n) => {
  if (page.value > n) page.value = n;
});

const resetFilters = () => {
  searchQuery.value = '';
  categoryFilter.value = 'all';
  statusFilter.value = 'all';
};

const hapusData = async (barang) => {
  const ok = await confirmDialog({
    title: `Hapus ${barang.nama}?`,
    message: 'Barang ini akan dihapus dari inventaris dan tidak bisa dikembalikan.',
    confirmLabel: 'Hapus barang',
    cancelLabel: 'Batal',
    danger: true,
  });
  if (!ok) return;

  deletingId.value = barang.id;
  try {
    await deleteBarang(barang.id);
    toast('Barang dihapus');
    emit('refresh');
  } catch (err) {
    toast(err.message, 'error');
  } finally {
    deletingId.value = null;
  }
};
</script>

<template>
  <section class="inventory" aria-labelledby="inventory-title">
    <div class="inventory__head">
      <h2 id="inventory-title" class="inventory__title">Daftar barang</h2>
      <button type="button" class="btn btn--ghost btn--sm" :disabled="isLoading" @click="$emit('refresh')">
        <AppIcon name="refresh" :size="16" :class="{ spin: isLoading }" />
        Muat ulang
      </button>
    </div>

    <div class="toolbar">
      <label class="field field--search">
        <span class="sr-only">Cari barang</span>
        <AppIcon name="search" :size="18" />
        <input v-model="searchQuery" type="search" placeholder="Cari nama, kategori, atau lokasi" autocomplete="off" />
      </label>

      <label class="field field--select">
        <span class="sr-only">Filter kategori</span>
        <select v-model="categoryFilter">
          <option value="all">Semua kategori</option>
          <option v-for="c in categories" :key="c" :value="c">{{ c }}</option>
        </select>
      </label>

      <label class="field field--select">
        <span class="sr-only">Urutkan</span>
        <select v-model="sortKey">
          <option v-for="o in sortOptions" :key="o.value" :value="o.value">{{ o.label }}</option>
        </select>
      </label>
    </div>

    <div class="chips" role="group" aria-label="Filter status stok">
      <button
        v-for="t in statusTabs"
        :key="t.value"
        type="button"
        class="chip"
        :class="[{ 'chip--active': statusFilter === t.value }, t.value !== 'all' ? `chip--${t.value}` : '']"
        :aria-pressed="statusFilter === t.value"
        @click="statusFilter = t.value"
      >
        <span v-if="t.value !== 'all'" class="dot" :class="`dot--${t.value}`"></span>
        {{ t.label }}
        <span class="chip__count">{{ formatNumber(statusCounts[t.value]) }}</span>
      </button>
    </div>

    <!-- Memuat -->
    <div v-if="isLoading && !barangList.length" class="skeleton-list" aria-busy="true" aria-label="Memuat data">
      <div v-for="n in 5" :key="n" class="skeleton skeleton--row"></div>
    </div>

    <!-- Belum ada data sama sekali -->
    <div v-else-if="!barangList.length" class="empty">
      <span class="empty__icon"><AppIcon name="inbox" :size="26" /></span>
      <h3>Belum ada barang</h3>
      <p>Tambahkan barang pertama untuk mulai mencatat stok gudang.</p>
      <button type="button" class="btn btn--primary" @click="$emit('add')">
        <AppIcon name="plus" /> Tambah barang
      </button>
    </div>

    <!-- Filter tidak menemukan hasil -->
    <div v-else-if="!filtered.length" class="empty">
      <span class="empty__icon"><AppIcon name="search" :size="26" /></span>
      <h3>Tidak ada barang yang cocok</h3>
      <p>Coba kata kunci lain atau hapus filter yang sedang aktif.</p>
      <button v-if="hasActiveFilter" type="button" class="btn btn--ghost" @click="resetFilters">Hapus filter</button>
    </div>

    <template v-else>
      <div class="table-wrap">
        <table class="table" role="table">
          <thead role="rowgroup">
            <tr role="row">
              <th role="columnheader" scope="col">Nama barang</th>
              <th role="columnheader" scope="col">Kategori</th>
              <th role="columnheader" scope="col" class="col-stok">Stok</th>
              <th role="columnheader" scope="col">Status</th>
              <th role="columnheader" scope="col">Lokasi</th>
              <th role="columnheader" scope="col" class="col-aksi"><span class="sr-only">Aksi</span></th>
            </tr>
          </thead>
          <tbody role="rowgroup">
            <tr v-for="barang in pageItems" :key="barang.id" role="row" :data-status="getStatus(barang.jumlah_stok).key">
              <td role="cell" class="td-nama">{{ barang.nama }}</td>
              <td role="cell" class="td-kategori">
                <span class="tag"><AppIcon name="tag" :size="14" />{{ barang.kategori }}</span>
              </td>
              <td role="cell" class="td-stok">
                <div class="stock">
                  <span class="stock__num">{{ formatNumber(barang.jumlah_stok) }}</span>
                  <div
                    class="gauge"
                    :class="`gauge--${getStatus(barang.jumlah_stok).key}`"
                    role="img"
                    :aria-label="`Stok ${barang.jumlah_stok}`"
                  >
                    <span class="gauge__fill" :style="{ width: fillPercent(barang.jumlah_stok) + '%' }"></span>
                    <span class="gauge__tick" :style="{ left: tickPercent + '%' }"></span>
                  </div>
                </div>
              </td>
              <td role="cell" class="td-status">
                <span class="badge" :class="`badge--${getStatus(barang.jumlah_stok).key}`">
                  <span class="dot" :class="`dot--${getStatus(barang.jumlah_stok).key}`"></span>
                  {{ getStatus(barang.jumlah_stok).label }}
                </span>
              </td>
              <td role="cell" class="td-lokasi">
                <span class="loc"><AppIcon name="pin" :size="14" />{{ barang.lokasi_gudang }}</span>
              </td>
              <td role="cell" class="td-aksi">
                <div class="row-actions">
                  <button
                    type="button"
                    class="btn btn--ghost btn--sm btn--row"
                    :aria-label="`Edit ${barang.nama}`"
                    title="Edit"
                    @click="$emit('edit', barang)"
                  >
                    <AppIcon name="edit" :size="16" /><span class="btn-label">Edit</span>
                  </button>
                  <button
                    type="button"
                    class="btn btn--ghost btn--sm btn--row btn--danger-text"
                    :aria-label="`Hapus ${barang.nama}`"
                    title="Hapus"
                    :disabled="deletingId === barang.id"
                    @click="hapusData(barang)"
                  >
                    <AppIcon name="trash" :size="16" /><span class="btn-label">Hapus</span>
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="inventory__foot">
        <p class="foot-note">
          <span class="foot-note__tick"></span>
          Garis pada bar stok menandai batas menipis ({{ LOW_STOCK }} unit)
        </p>

        <div class="pager">
          <span class="pager__info">
            {{ rangeStart }}–{{ rangeEnd }} dari {{ formatNumber(filtered.length) }}
          </span>
          <div class="pager__btns" v-if="totalPages > 1">
            <button
              type="button"
              class="btn btn--ghost btn--icon btn--sm"
              aria-label="Halaman sebelumnya"
              :disabled="page <= 1"
              @click="page--"
            >
              <AppIcon name="chevL" :size="16" />
            </button>
            <span class="pager__page">{{ page }} / {{ totalPages }}</span>
            <button
              type="button"
              class="btn btn--ghost btn--icon btn--sm"
              aria-label="Halaman berikutnya"
              :disabled="page >= totalPages"
              @click="page++"
            >
              <AppIcon name="chevR" :size="16" />
            </button>
          </div>
        </div>
      </div>
    </template>
  </section>
</template>
