<script setup>
import { computed } from 'vue';
import AppIcon from './AppIcon.vue';
import { getStatus, formatNumber } from '../constants';

const props = defineProps({
  barangList: { type: Array, default: () => [] },
  isLoading: { type: Boolean, default: false },
});

const total = computed(() => props.barangList.length);
const totalUnit = computed(() => props.barangList.reduce((acc, b) => acc + (Number(b.jumlah_stok) || 0), 0));
const jumlahKategori = computed(() => new Set(props.barangList.map((b) => b.kategori)).size);

const counts = computed(() => {
  const c = { aman: 0, menipis: 0, habis: 0 };
  props.barangList.forEach((b) => c[getStatus(b.jumlah_stok).key]++);
  return c;
});

// Sama dengan hitungan "Stok Menipis" sebelumnya (stok <= 20, termasuk yang habis)
const perluRestok = computed(() => counts.value.menipis + counts.value.habis);

const percent = (n) => (total.value ? (n / total.value) * 100 : 0);

const segments = computed(() => [
  { key: 'aman', label: 'Aman', value: counts.value.aman },
  { key: 'menipis', label: 'Menipis', value: counts.value.menipis },
  { key: 'habis', label: 'Habis', value: counts.value.habis },
]);

const headline = computed(() => {
  if (!total.value) return 'Belum ada barang di gudang';
  if (!perluRestok.value) return 'Semua stok dalam kondisi aman';
  return `${perluRestok.value} dari ${total.value} barang perlu restok`;
});
</script>

<template>
  <section class="summary" aria-labelledby="summary-title">
    <div class="summary__top">
      <div>
        <h2 id="summary-title" class="summary__label">Kondisi stok</h2>
        <p v-if="isLoading && !total" class="skeleton skeleton--title"></p>
        <p v-else class="summary__headline">{{ headline }}</p>
      </div>

      <ul class="legend" v-if="total">
        <li v-for="s in segments" :key="s.key">
          <span class="dot" :class="`dot--${s.key}`"></span>
          {{ s.label }} <strong>{{ formatNumber(s.value) }}</strong>
        </li>
      </ul>
    </div>

    <div
      class="distribution"
      :class="{ 'distribution--empty': !total }"
      role="img"
      :aria-label="`Aman ${counts.aman}, menipis ${counts.menipis}, habis ${counts.habis}`"
    >
      <span
        v-for="s in segments"
        :key="s.key"
        class="distribution__seg"
        :class="`seg--${s.key}`"
        :style="{ width: percent(s.value) + '%' }"
      ></span>
    </div>

    <dl class="metrics">
      <div class="metric">
        <dt><AppIcon name="box" :size="16" /> Total barang</dt>
        <dd v-if="isLoading && !total" class="skeleton skeleton--num"></dd>
        <dd v-else>{{ formatNumber(total) }}</dd>
      </div>
      <div class="metric">
        <dt><AppIcon name="layers" :size="16" /> Total unit</dt>
        <dd v-if="isLoading && !total" class="skeleton skeleton--num"></dd>
        <dd v-else>{{ formatNumber(totalUnit) }}</dd>
      </div>
      <div class="metric">
        <dt><AppIcon name="tag" :size="16" /> Kategori</dt>
        <dd v-if="isLoading && !total" class="skeleton skeleton--num"></dd>
        <dd v-else>{{ formatNumber(jumlahKategori) }}</dd>
      </div>
      <div class="metric" :class="{ 'metric--alert': perluRestok > 0 }">
        <dt><AppIcon name="alert" :size="16" /> Perlu restok</dt>
        <dd v-if="isLoading && !total" class="skeleton skeleton--num"></dd>
        <dd v-else>
          {{ formatNumber(perluRestok) }}
          <small v-if="counts.habis">{{ formatNumber(counts.habis) }} habis</small>
        </dd>
      </div>
    </dl>
  </section>
</template>
