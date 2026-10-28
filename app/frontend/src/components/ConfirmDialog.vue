<script setup lang="ts">
// SCR-04 confirmation (AC-205.3). Native <dialog> traps focus and closes on Esc.
import { onMounted, ref } from "vue";

defineProps<{ title: string; message: string; confirmLabel: string }>();
const emit = defineEmits<{ confirm: []; cancel: [] }>();

const dialog = ref<HTMLDialogElement | null>(null);

onMounted(() => dialog.value?.showModal?.());
</script>

<template>
  <dialog ref="dialog" aria-labelledby="dialog-title" @cancel.prevent="emit('cancel')">
    <h2 id="dialog-title">{{ title }}</h2>
    <p>{{ message }}</p>
    <div class="dialog-actions">
      <button class="btn" @click="emit('cancel')">Hủy</button>
      <button class="btn btn-danger" @click="emit('confirm')">{{ confirmLabel }}</button>
    </div>
  </dialog>
</template>
