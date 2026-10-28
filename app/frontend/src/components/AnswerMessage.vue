<script setup lang="ts">
// One answer: text with clickable [n] citations (US-305), sources list, warning, feedback (US-501).
import { computed } from "vue";

import type { Citation, Turn } from "@/api/types";
import { useAnnouncer } from "@/composables/useAnnouncer";
import { useChat } from "@/composables/useChat";
import { splitAnswer } from "@/utils/answer";

const props = defineProps<{ turn: Turn }>();
defineEmits<{ "open-citation": [citation: Citation] }>();

const chat = useChat();
const { announce } = useAnnouncer();
const parts = computed(() => splitAnswer(props.turn.answer, props.turn.citations));

async function rate(rating: "up" | "down"): Promise<void> {
  const reason = rating === "down" ? (window.prompt("Lý do (không bắt buộc, tối đa 500 ký tự):", "") ?? "").slice(0, 500) : "";
  try {
    await chat.rate(props.turn, rating, reason || null);
    announce("Đã ghi nhận đánh giá.");
  } catch (err) {
    announce((err as Error).message);
  }
}
</script>

<template>
  <div class="msg msg-a" :class="{ 'not-found': turn.outcome === 'not_found' }">
    <div class="answer-text">
      <template v-for="(part, i) in parts" :key="i">
        <button
          v-if="part.kind === 'cite'"
          class="cite"
          :aria-label="`Nguồn ${part.citation.index}: ${part.citation.document_name}, trang ${part.citation.page}`"
          @click="$emit('open-citation', part.citation)"
        >
          [{{ part.citation.index }}]
        </button>
        <template v-else>{{ part.text }}</template>
      </template>
    </div>
    <ol v-if="turn.citations.length" class="sources" aria-label="Nguồn">
      <li v-for="c in turn.citations" :key="c.index" :value="c.index">
        <button class="link" @click="$emit('open-citation', c)">{{ c.document_name }} — tr. {{ c.page }}</button>
        <span v-if="c.document_deleted"> (tài liệu đã bị xóa)</span>
      </li>
    </ol>
    <div v-if="turn.warning === 'docs_processing'" class="notice">
      Một số tài liệu đang xử lý chưa được dùng để trả lời; câu trả lời có thể chưa đầy đủ.
    </div>
    <div class="feedback">
      <button class="btn btn-sm" :aria-pressed="turn.feedback === 'up'" aria-label="Hữu ích" @click="rate('up')">
        👍 Hữu ích
      </button>
      <button class="btn btn-sm" :aria-pressed="turn.feedback === 'down'" aria-label="Không hữu ích" @click="rate('down')">
        👎 Không hữu ích
      </button>
    </div>
  </div>
</template>
