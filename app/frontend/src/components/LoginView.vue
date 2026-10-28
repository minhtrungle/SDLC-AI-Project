<script setup lang="ts">
// SCR-01 login, SCR-06 session expired (US-101, EC-15).
import { onMounted, ref } from "vue";

import { useSession } from "@/composables/useSession";

const session = useSession();
const username = ref("");
const password = ref("");
const error = ref<string | null>(null);
const busy = ref(false);
const userInput = ref<HTMLInputElement | null>(null);
const passwordInput = ref<HTMLInputElement | null>(null);

onMounted(() => userInput.value?.focus());

async function submit(): Promise<void> {
  busy.value = true;
  error.value = null;
  try {
    await session.login(username.value.trim(), password.value);
  } catch (err) {
    error.value = (err as Error).message;
    password.value = "";
    passwordInput.value?.focus();
  } finally {
    busy.value = false;
  }
}
</script>

<template>
  <main class="center">
    <form class="card" @submit.prevent="submit">
      <div class="brand"><span class="logo" aria-hidden="true">📄</span>Chat với tài liệu</div>
      <h1>Đăng nhập</h1>
      <div v-if="session.state.sessionExpired" class="banner banner-warning" role="status">
        Phiên đăng nhập đã hết hạn. Vui lòng đăng nhập lại; câu hỏi đang soạn đã được giữ lại.
      </div>
      <div v-if="error" class="banner banner-error" role="alert">{{ error }}</div>
      <div class="field">
        <label for="username">Tên đăng nhập</label>
        <input id="username" ref="userInput" v-model="username" autocomplete="username" required />
      </div>
      <div class="field">
        <label for="password">Mật khẩu</label>
        <input
          id="password"
          ref="passwordInput"
          v-model="password"
          type="password"
          autocomplete="current-password"
          required
        />
      </div>
      <button class="btn btn-primary" type="submit" :disabled="busy">Đăng nhập</button>
    </form>
  </main>
</template>
