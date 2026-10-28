import { sessionStore } from "@/utils/format";

export const DRAFT_KEY = "cwd.draft";
export const CONVERSATION_KEY = "cwd.conversation";

/** A draft is kept per user so it is never offered to someone else on a shared machine (NR-03). */
export function saveDraft(username: string, text: string): void {
  sessionStore.set(DRAFT_KEY, JSON.stringify({ username, text }));
}

export function takeDraft(username: string | undefined): string {
  const raw = sessionStore.get(DRAFT_KEY);
  sessionStore.set(DRAFT_KEY, null);
  if (!raw || !username) return "";
  try {
    const draft = JSON.parse(raw) as { username?: string; text?: string };
    return draft.username === username ? (draft.text ?? "") : "";
  } catch {
    return "";
  }
}
