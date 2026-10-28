<script setup lang="ts">
// SCR-05 weekly usage for managers (US-502).
import { computed, onMounted, ref } from "vue";

import { api } from "@/api/client";
import type { WeeklyMetric } from "@/api/types";
import { percent } from "@/utils/format";

const weeks = ref<WeeklyMetric[] | null>(null);
const error = ref<string | null>(null);
const maxQuestions = computed(() => Math.max(1, ...(weeks.value ?? []).map((w) => w.questions)));

onMounted(async () => {
  try {
    weeks.value = (await api.weekly()).weeks;
  } catch (err) {
    error.value = (err as Error).message;
  }
});
</script>

<template>
  <main class="dashboard">
    <h1>Số liệu sử dụng theo tuần</h1>
    <div v-if="error" class="banner banner-error" role="alert">{{ error }}</div>
    <p v-else-if="!weeks" class="muted">Đang tải…</p>
    <table v-else>
      <caption class="sr-only">
        Người dùng hoạt động, số câu hỏi, tỷ lệ không tìm thấy và tỷ lệ đánh giá tích cực theo tuần
      </caption>
      <thead>
        <tr>
          <th scope="col">Tuần</th>
          <th scope="col">Người dùng hoạt động</th>
          <th scope="col">Số câu hỏi</th>
          <th scope="col"><span class="sr-only">Biểu đồ</span></th>
          <th scope="col">Không tìm thấy</th>
          <th scope="col">Đánh giá tích cực</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="w in weeks" :key="w.week">
          <td>{{ w.week }}</td>
          <td>{{ w.active_users }}</td>
          <td>{{ w.questions }}</td>
          <td class="bar-cell" aria-hidden="true">
            <div class="bar" :style="{ width: `${Math.round((w.questions / maxQuestions) * 100)}%` }"></div>
          </td>
          <td>{{ percent(w.not_found_rate) }}</td>
          <td>{{ percent(w.positive_feedback_rate) }}</td>
        </tr>
      </tbody>
    </table>
  </main>
</template>
