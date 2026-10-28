<script setup lang="ts">
import { onMounted } from "vue";

import AppHeader from "@/components/AppHeader.vue";
import LoginView from "@/components/LoginView.vue";
import UsageDashboard from "@/components/UsageDashboard.vue";
import WorkspaceView from "@/components/WorkspaceView.vue";
import { useAnnouncer } from "@/composables/useAnnouncer";
import { useSession } from "@/composables/useSession";

const session = useSession();
const { message } = useAnnouncer();

onMounted(session.boot);
</script>

<template>
  <p v-if="session.state.view === 'loading'" class="center muted">Đang tải…</p>
  <LoginView v-else-if="session.state.view === 'login'" />
  <template v-else>
    <AppHeader />
    <WorkspaceView v-if="session.state.view === 'workspace'" />
    <UsageDashboard v-else />
  </template>
  <div class="sr-only" aria-live="polite">{{ message }}</div>
</template>
