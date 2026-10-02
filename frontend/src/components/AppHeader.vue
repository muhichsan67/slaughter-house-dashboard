<script setup>
import AppIcon from './AppIcon.vue';
import { useTheme } from '../composables/useTheme';

defineEmits(['add']);
const { theme, toggle } = useTheme();
</script>

<template>
  <header class="topbar">
    <div class="topbar__inner">
      <div class="brand">
        <span class="brand__mark"><AppIcon name="snow" :size="20" /></span>
        <div class="brand__text">
          <strong>Gudang RPA</strong>
          <span>Karkas &amp; daging</span>
        </div>
      </div>

      <div class="topbar__actions">
        <button
          type="button"
          class="btn btn--icon"
          :aria-label="theme === 'dark' ? 'Ganti ke tema terang' : 'Ganti ke tema gelap'"
          :title="theme === 'dark' ? 'Tema terang' : 'Tema gelap'"
          @click="toggle"
        >
          <AppIcon :name="theme === 'dark' ? 'sun' : 'moon'" />
        </button>
        <button type="button" class="btn btn--primary" @click="$emit('add')">
          <AppIcon name="plus" />
          <span class="hide-xs">Tambah barang</span>
          <span class="show-xs">Tambah</span>
        </button>
      </div>
    </div>
  </header>
</template>
