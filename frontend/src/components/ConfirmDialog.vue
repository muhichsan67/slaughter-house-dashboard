<script setup>
import { ref, watch, nextTick, onBeforeUnmount } from 'vue';
import AppIcon from './AppIcon.vue';
import { confirmState, answerConfirm } from '../composables/useFeedback';

const cancelBtn = ref(null);
let lastFocused = null;

const onKey = (e) => {
  if (e.key === 'Escape') answerConfirm(false);
};

watch(
  () => confirmState.open,
  async (open) => {
    if (open) {
      lastFocused = document.activeElement;
      document.addEventListener('keydown', onKey);
      await nextTick();
      cancelBtn.value?.focus();
    } else {
      document.removeEventListener('keydown', onKey);
      lastFocused?.focus?.();
    }
  }
);

onBeforeUnmount(() => document.removeEventListener('keydown', onKey));
</script>

<template>
  <Teleport to="body">
    <Transition name="overlay">
      <div v-if="confirmState.open" class="overlay overlay--center" @mousedown.self="answerConfirm(false)">
        <div
          class="dialog dialog--small"
          role="alertdialog"
          aria-modal="true"
          aria-labelledby="confirm-title"
          aria-describedby="confirm-desc"
        >
          <div class="dialog__icon" :class="{ 'dialog__icon--danger': confirmState.danger }">
            <AppIcon :name="confirmState.danger ? 'trash' : 'alert'" :size="22" />
          </div>
          <h2 id="confirm-title" class="dialog__title">{{ confirmState.title }}</h2>
          <p id="confirm-desc" class="dialog__text">{{ confirmState.message }}</p>
          <div class="dialog__actions">
            <button ref="cancelBtn" type="button" class="btn btn--ghost" @click="answerConfirm(false)">
              {{ confirmState.cancelLabel }}
            </button>
            <button
              type="button"
              class="btn"
              :class="confirmState.danger ? 'btn--danger' : 'btn--primary'"
              @click="answerConfirm(true)"
            >
              {{ confirmState.confirmLabel }}
            </button>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>
