<script setup>
import AppIcon from './AppIcon.vue';
import { toasts, dismissToast } from '../composables/useFeedback';
</script>

<template>
  <Teleport to="body">
    <div class="toasts" role="status" aria-live="polite">
      <TransitionGroup name="toast">
        <div v-for="t in toasts" :key="t.id" class="toast" :class="`toast--${t.type}`">
          <AppIcon :name="t.type === 'error' ? 'alert' : 'check'" :size="18" />
          <span class="toast__msg">{{ t.message }}</span>
          <button type="button" class="toast__close" aria-label="Tutup pesan" @click="dismissToast(t.id)">
            <AppIcon name="x" :size="16" />
          </button>
        </div>
      </TransitionGroup>
    </div>
  </Teleport>
</template>
