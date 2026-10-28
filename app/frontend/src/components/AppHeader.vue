<script setup lang="ts">
import { useSession } from "@/composables/useSession";

const session = useSession();
</script>

<template>
  <header class="app-header">
    <button class="brand btn btn-ghost" aria-label="Về màn hình chính" @click="session.show('workspace')">
      <span class="logo" aria-hidden="true">📄</span>Chat với tài liệu
    </button>
    <div class="header-right">
      <span class="badge badge-info" title="Nơi xử lý nội dung tài liệu (FR-003)">
        {{ session.state.config.ai_mode === "local" ? "🔒 Xử lý cục bộ" : "☁ Dùng dịch vụ AI bên ngoài" }}
      </span>
      <button
        v-if="session.state.me?.role === 'manager'"
        class="btn btn-ghost btn-sm"
        @click="session.show('dashboard')"
      >
        Số liệu sử dụng
      </button>
      <span class="muted">{{ session.state.me?.username }}</span>
      <button class="btn btn-sm" @click="session.logout">Đăng xuất</button>
    </div>
  </header>
</template>
