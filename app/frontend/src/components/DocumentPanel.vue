<script setup lang="ts">
// Documents panel: upload with progress (US-201..203), list (US-204), scope selection (US-402).
import { ref } from "vue";

import type { DocumentInfo } from "@/api/types";
import { useDocuments } from "@/composables/useDocuments";
import { useSession } from "@/composables/useSession";
import { formatDate, STATUS_LABELS } from "@/utils/format";

defineEmits<{ delete: [doc: DocumentInfo] }>();

const { state, upload, toggle } = useDocuments();
const session = useSession();
const fileInput = ref<HTMLInputElement | null>(null);
const dragging = ref(false);

function pick(event: Event): void {
  const input = event.target as HTMLInputElement;
  void upload([...(input.files ?? [])]);
  input.value = "";
}

function drop(event: DragEvent): void {
  dragging.value = false;
  void upload([...(event.dataTransfer?.files ?? [])]);
}
</script>

<template>
  <section class="panel" aria-labelledby="docs-title">
    <div class="panel-head">
      <h2 id="docs-title">Tài liệu ({{ state.docs.length }})</h2>
    </div>
    <div class="panel-body">
      <div
        class="dropzone"
        :class="{ drag: dragging }"
        @dragover.prevent="dragging = true"
        @dragleave="dragging = false"
        @drop.prevent="drop"
      >
        <button class="btn btn-primary" @click="fileInput?.click()">+ Tải lên PDF</button>
        <p class="muted">
          Kéo thả hoặc chọn nhiều file PDF, tối đa {{ session.state.config.max_file_mb }} MB mỗi file.
        </p>
        <input
          ref="fileInput"
          class="sr-only"
          type="file"
          accept="application/pdf,.pdf"
          multiple
          data-testid="file-input"
          @change="pick"
        />
      </div>

      <ul class="upload-list" aria-label="Tiến độ tải lên">
        <li v-for="u in state.uploads" :key="u.name" class="upload-item">
          <div>
            {{ u.name }} —
            <span v-if="u.error" class="upload-error">{{ u.error }}</span>
            <template v-else>{{ u.done ? "đã tải lên" : `${Math.round(u.progress * 100)}%` }}</template>
          </div>
          <progress v-if="!u.done && !u.error" max="1" :value="u.progress" :aria-label="`Tiến độ ${u.name}`" />
        </li>
      </ul>

      <p v-if="state.error" class="error-text" role="alert">{{ state.error }}</p>
      <div v-if="state.docs.length === 0" class="empty">
        <p>Chưa có tài liệu nào.</p>
        <button class="btn" @click="fileInput?.click()">Tải tài liệu đầu tiên</button>
      </div>
      <ul v-else class="doc-list">
        <li v-for="d in state.docs" :key="d.id" class="doc">
          <input
            type="checkbox"
            :disabled="d.status !== 'ready'"
            :checked="state.selected.has(d.id)"
            :aria-label="`Chọn ${d.filename} làm phạm vi câu hỏi`"
            @change="toggle(d.id, ($event.target as HTMLInputElement).checked)"
          />
          <div>
            <div class="doc-name">{{ d.filename }}</div>
            <div :class="`status status-${d.status}`">
              <span aria-hidden="true">{{ STATUS_LABELS[d.status].icon }}</span>{{ STATUS_LABELS[d.status].label }}
            </div>
            <div class="muted">{{ formatDate(d.created_at) }}{{ d.page_count ? ` · ${d.page_count} trang` : "" }}</div>
            <div v-if="d.error_message" class="muted">{{ d.error_message }}</div>
          </div>
          <button class="btn btn-ghost btn-sm" :aria-label="`Xóa ${d.filename}`" @click="$emit('delete', d)">🗑</button>
        </li>
      </ul>
    </div>
  </section>
</template>
