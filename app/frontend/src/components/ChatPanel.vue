<script setup lang="ts">
// Conversation panel: ask (US-301..304), scope (US-402), history (US-403), new conversation.
import { computed, nextTick, ref, watch } from "vue";

import type { Citation } from "@/api/types";
import AnswerMessage from "@/components/AnswerMessage.vue";
import { useAnnouncer } from "@/composables/useAnnouncer";
import { useChat } from "@/composables/useChat";
import { useDocuments } from "@/composables/useDocuments";
import { takeDraft } from "@/composables/keys";
import { useSession } from "@/composables/useSession";
import { composerState } from "@/utils/composer";

defineEmits<{ "open-citation": [citation: Citation] }>();

const session = useSession();
const documents = useDocuments();
const chat = useChat();
const { announce } = useAnnouncer();

const draft = ref(takeDraft(session.state.me?.username)); // only this user's own draft (NR-03)
const textarea = ref<HTMLTextAreaElement | null>(null);
const messages = ref<HTMLElement | null>(null);

const maxChars = computed(() => session.state.config.max_question_chars);
const composer = computed(() => composerState(documents.state.docs, draft.value, chat.state.pending !== null, maxChars.value));
const scopeLabel = computed(() =>
  documents.state.selected.size ? `Phạm vi: ${documents.state.selected.size} tài liệu đã chọn` : "Phạm vi: Tất cả tài liệu",
);

watch(
  () => [chat.state.turns.length, chat.state.pending, chat.state.error],
  async () => {
    await nextTick();
    if (messages.value) messages.value.scrollTop = messages.value.scrollHeight;
  },
);

async function send(): Promise<void> {
  const question = draft.value.trim();
  if (!question || composer.value.sendDisabled || composer.value.inputDisabled) return;
  const scope = documents.state.selected.size ? [...documents.state.selected] : null;
  if (await chat.ask(question, scope)) {
    draft.value = "";
    const last = chat.state.turns[chat.state.turns.length - 1];
    announce(last?.outcome === "not_found" ? "Không tìm thấy thông tin trong tài liệu." : "Đã có câu trả lời.");
  }
  textarea.value?.focus();
}

function onKeydown(event: KeyboardEvent): void {
  // UX-009: Enter sends, Shift+Enter inserts a newline.
  if (event.key === "Enter" && !event.shiftKey) {
    event.preventDefault();
    void send();
  }
}

function newConversation(): void {
  chat.startNew();
  textarea.value?.focus();
}
</script>

<template>
  <section class="panel" aria-labelledby="chat-title">
    <div class="panel-head">
      <h2 id="chat-title">Hội thoại</h2>
      <button class="btn btn-sm" @click="newConversation">Cuộc hội thoại mới</button>
    </div>
    <div class="scope">{{ scopeLabel }}</div>
    <div ref="messages" class="messages" aria-live="polite">
      <div v-if="!chat.state.turns.length && !chat.state.pending" class="empty">
        Hãy đặt câu hỏi về nội dung các tài liệu đã tải lên. Mỗi câu trả lời kèm nguồn để bạn kiểm chứng.
      </div>
      <template v-for="turn in chat.state.turns" :key="turn.id">
        <div class="msg msg-q">{{ turn.question }}</div>
        <AnswerMessage :turn="turn" @open-citation="$emit('open-citation', $event)" />
      </template>
      <template v-if="chat.state.pending">
        <div class="msg msg-q">{{ chat.state.pending }}</div>
        <div class="msg msg-a muted">Đang trả lời…</div>
      </template>
      <div v-if="chat.state.error" class="msg msg-a" role="alert">
        <span class="error-text">{{ chat.state.error }}</span>
        <button class="btn btn-sm" @click="send">Gửi lại</button>
      </div>
    </div>
    <div class="composer">
      <textarea
        id="question"
        ref="textarea"
        v-model="draft"
        aria-label="Câu hỏi"
        :maxlength="maxChars"
        :disabled="composer.inputDisabled"
        placeholder="Nhập câu hỏi… (Enter để gửi, Shift+Enter xuống dòng)"
        @keydown="onKeydown"
      ></textarea>
      <div class="composer-row">
        <span class="muted">{{ composer.hint }}</span>
        <button class="btn btn-primary" :disabled="composer.sendDisabled || composer.inputDisabled" @click="send">
          Gửi
        </button>
      </div>
    </div>
  </section>
</template>
