<script setup lang="ts">
// SCR-02 workspace: documents (left) and conversation (right) — UX-001.
import { onMounted, onUnmounted, ref } from "vue";

import type { Citation, DocumentInfo } from "@/api/types";
import ChatPanel from "@/components/ChatPanel.vue";
import CitationDrawer from "@/components/CitationDrawer.vue";
import ConfirmDialog from "@/components/ConfirmDialog.vue";
import DocumentPanel from "@/components/DocumentPanel.vue";
import { useAnnouncer } from "@/composables/useAnnouncer";
import { useChat } from "@/composables/useChat";
import { useDocuments } from "@/composables/useDocuments";

const documents = useDocuments();
const chat = useChat();
const { announce } = useAnnouncer();
const citation = ref<Citation | null>(null);
const pendingDelete = ref<DocumentInfo | null>(null);

onMounted(async () => {
  await Promise.all([documents.load(), chat.restore()]);
});
onUnmounted(documents.stopPolling);

async function confirmDelete(): Promise<void> {
  const doc = pendingDelete.value;
  pendingDelete.value = null;
  if (!doc) return;
  try {
    await documents.remove(doc);
    announce(`Đã xóa ${doc.filename}`);
  } catch (err) {
    announce((err as Error).message);
  }
}
</script>

<template>
  <main class="workspace">
    <DocumentPanel @delete="pendingDelete = $event" />
    <ChatPanel @open-citation="citation = $event" />
  </main>
  <CitationDrawer v-if="citation" :citation="citation" @close="citation = null" />
  <ConfirmDialog
    v-if="pendingDelete"
    title="Xóa tài liệu?"
    :message="`&quot;${pendingDelete.filename}&quot; sẽ bị xóa vĩnh viễn và không còn được dùng để trả lời câu hỏi.`"
    confirm-label="Xóa"
    @confirm="confirmDelete"
    @cancel="pendingDelete = null"
  />
</template>
