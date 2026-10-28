<script setup lang="ts">
// SCR-03 citation panel: original passage + page (AC-305.2); Esc closes and focus returns (WCAG 2.1.1).
import { onMounted, onUnmounted, ref, watch } from "vue";

import { api } from "@/api/client";
import type { Citation } from "@/api/types";

const props = defineProps<{ citation: Citation }>();
const emit = defineEmits<{ close: [] }>();

const text = ref<string | null>(null);
const failed = ref(false);
const closeButton = ref<HTMLButtonElement | null>(null);
const opener = document.activeElement as HTMLElement | null;

async function load(): Promise<void> {
  text.value = null;
  failed.value = false;
  if (props.citation.document_deleted) return;
  try {
    text.value = (await api.chunk(props.citation.chunk_id)).text;
  } catch {
    failed.value = true;
  }
}

function onKey(event: KeyboardEvent): void {
  if (event.key === "Escape") emit("close");
}

onMounted(() => {
  document.addEventListener("keydown", onKey);
  closeButton.value?.focus();
  void load();
});
onUnmounted(() => {
  document.removeEventListener("keydown", onKey);
  opener?.focus();
});
watch(() => props.citation, load);
</script>

<template>
  <aside class="drawer" role="dialog" aria-label="Nguồn trích dẫn">
    <div class="panel-head">
      <h2>Nguồn [{{ citation.index }}]</h2>
      <button ref="closeButton" class="btn btn-sm" aria-label="Đóng panel nguồn" @click="emit('close')">Đóng</button>
    </div>
    <div class="panel-body">
      <p><strong>{{ citation.document_name }}</strong> — trang {{ citation.page }}</p>
      <template v-if="citation.document_deleted">
        <div class="notice">Tài liệu đã bị xóa.</div>
        <div class="drawer-text">{{ citation.snippet }}</div>
      </template>
      <template v-else-if="failed">
        <div class="notice">Không tải được đoạn gốc; hiển thị đoạn trích đã lưu.</div>
        <div class="drawer-text">{{ citation.snippet }}</div>
      </template>
      <div v-else-if="text !== null" class="drawer-text">{{ text }}</div>
      <p v-else class="muted">Đang tải đoạn gốc…</p>
    </div>
  </aside>
</template>
