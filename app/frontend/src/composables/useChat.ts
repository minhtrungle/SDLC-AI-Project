import { reactive } from "vue";

import { api } from "@/api/client";
import type { Turn } from "@/api/types";
import { sessionStore } from "@/utils/format";

import { CONVERSATION_KEY } from "./keys";

const state = reactive({
  conversationId: null as string | null,
  turns: [] as Turn[],
  pending: null as string | null,
  error: null as string | null,
});

/** Restore the conversation of this browser session (US-403); a stale id is simply dropped. */
async function restore(): Promise<void> {
  state.conversationId = sessionStore.get(CONVERSATION_KEY);
  state.turns = [];
  if (!state.conversationId) return;
  try {
    state.turns = (await api.conversation(state.conversationId)).turns;
  } catch {
    state.conversationId = null;
    sessionStore.set(CONVERSATION_KEY, null);
  }
}

function startNew(): void {
  state.conversationId = null;
  state.turns = [];
  state.error = null;
  sessionStore.set(CONVERSATION_KEY, null);
}

/** Returns true when the question got an answer (so the caller can clear the input). */
async function ask(question: string, documentIds: string[] | null): Promise<boolean> {
  state.pending = question;
  state.error = null;
  try {
    if (!state.conversationId) {
      state.conversationId = (await api.newConversation()).id;
      sessionStore.set(CONVERSATION_KEY, state.conversationId);
    }
    state.turns.push(await api.ask(state.conversationId, question, documentIds));
    return true;
  } catch (err) {
    state.error = (err as Error).message; // EC-04/EC-05: keep the question, offer "Gửi lại"
    return false;
  } finally {
    state.pending = null;
  }
}

async function rate(turn: Turn, rating: "up" | "down", reason: string | null): Promise<void> {
  await api.feedback(turn.id, rating, reason);
  turn.feedback = rating;
}

/** Forget the previous user's conversation (logout / session expiry — NR-03). */
function reset(): void {
  startNew();
  state.pending = null;
}

export function useChat() {
  return { state, restore, startNew, ask, rate, reset };
}
