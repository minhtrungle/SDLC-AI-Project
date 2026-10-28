import { reactive } from "vue";

import { api, setCsrf, setUnauthorizedHandler } from "@/api/client";
import type { Me, PublicConfig } from "@/api/types";

import { saveDraft } from "./keys";
import { useAnnouncer } from "./useAnnouncer";
import { useChat } from "./useChat";
import { useDocuments } from "./useDocuments";

export { CONVERSATION_KEY, DRAFT_KEY } from "./keys";

type View = "loading" | "login" | "workspace" | "dashboard";

const DEFAULT_CONFIG: PublicConfig = { ai_mode: "local", max_file_mb: 20, max_docs: 50, max_question_chars: 2000 };

const state = reactive({
  view: "loading" as View,
  config: DEFAULT_CONFIG as PublicConfig,
  me: null as Me | null,
  sessionExpired: false,
});

function signedIn(me: Me): void {
  state.me = me;
  state.sessionExpired = false;
  setCsrf(me.csrf_token);
  state.view = "workspace";
}

/** Drop the signed-in user and everything shown for them, so the next login starts clean (NR-03). */
function signOutLocally(expired: boolean): void {
  useDocuments().reset();
  useChat().reset();
  state.me = null;
  state.sessionExpired = expired;
  setCsrf(null);
  state.view = "login";
}

/** EC-15: a 401 while signed in keeps this user's draft question and returns to the login screen (SCR-06). */
function expire(): void {
  if (!state.me) return;
  const draft = document.getElementById("question") as HTMLTextAreaElement | null;
  if (draft?.value.trim()) saveDraft(state.me.username, draft.value);
  signOutLocally(true);
}

export function useSession() {
  async function boot(): Promise<void> {
    setUnauthorizedHandler(expire);
    try {
      state.config = await api.config();
    } catch {
      state.config = DEFAULT_CONFIG;
    }
    try {
      signedIn(await api.me());
    } catch {
      state.view = "login";
    }
  }

  async function login(username: string, password: string): Promise<void> {
    signedIn(await api.login(username, password));
  }

  /** NR-12: if the server cannot end the session, say so and stay signed in instead of pretending. */
  async function logout(): Promise<void> {
    try {
      await api.logout();
    } catch (err) {
      useAnnouncer().announce(`Không đăng xuất được: ${(err as Error).message}`);
      if ((err as { status?: number }).status !== 401) return;
    }
    signOutLocally(false);
  }

  function show(view: "workspace" | "dashboard"): void {
    state.view = view;
  }

  return { state, boot, login, logout, show, expire };
}
