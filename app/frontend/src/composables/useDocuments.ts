import { reactive } from "vue";

import { api, uploadFile } from "@/api/client";
import type { DocumentInfo } from "@/api/types";

export interface UploadItem {
  id: number;
  batch: number;
  name: string;
  progress: number;
  done: boolean;
  error: string | null;
}

const POLL_MS = 2000;
const CLEAR_DONE_MS = 4000;

const state = reactive({
  docs: [] as DocumentInfo[],
  selected: new Set<string>(),
  uploads: [] as UploadItem[],
  error: null as string | null,
});
let pollTimer: ReturnType<typeof setTimeout> | null = null;
let polling = false; // false after stopPolling()/reset(): late responses must not restart polling (NR-04)
let latestRequest = 0; // only the newest list response may update state (NR-06)
let nextUploadId = 0;
let nextBatch = 0;

function stopPolling(): void {
  polling = false;
  if (pollTimer) clearTimeout(pollTimer);
  pollTimer = null;
}

async function load(): Promise<void> {
  const request = ++latestRequest;
  polling = true;
  let documents: DocumentInfo[];
  try {
    documents = (await api.documents()).documents;
  } catch (err) {
    if (request === latestRequest) state.error = (err as Error).message;
    return; // e.g. 401: the session handler takes over; never keep polling a failing endpoint
  }
  if (request !== latestRequest) return; // a newer load (e.g. after delete) already ran
  // Replace only when something changed so polling does not re-render the list (CR-11).
  if (JSON.stringify(documents) !== JSON.stringify(state.docs)) state.docs = documents;
  state.error = null;
  for (const id of [...state.selected]) {
    if (!state.docs.some((d) => d.id === id && d.status === "ready")) state.selected.delete(id);
  }
  if (pollTimer) clearTimeout(pollTimer);
  pollTimer = null;
  // AC-203.2: status updates without reloading the page.
  if (polling && state.docs.some((d) => d.status === "processing")) pollTimer = setTimeout(load, POLL_MS);
}

async function upload(files: File[]): Promise<void> {
  if (!files.length) return;
  const batch = ++nextBatch;
  const items = files.map((f) => ({ id: ++nextUploadId, batch, name: f.name, progress: 0, done: false, error: null }));
  state.uploads.push(...items);
  await Promise.all(
    files.map(async (file, i) => {
      // Mutate through the reactive array so progress renders.
      const item = state.uploads.find((u) => u.id === items[i]!.id);
      if (!item) return;
      try {
        const result = await uploadFile(file, (p) => (item.progress = p));
        if (result.ok) item.done = true;
        else item.error = result.error?.message ?? "Tải lên thất bại.";
      } catch (err) {
        item.error = (err as Error).message;
      }
    }),
  );
  await load();
  // Clear only this batch's successful rows; errors and newer batches stay visible (NR-05).
  setTimeout(() => (state.uploads = state.uploads.filter((u) => u.batch !== batch || u.error)), CLEAR_DONE_MS);
}

async function remove(doc: DocumentInfo): Promise<void> {
  await api.deleteDocument(doc.id);
  state.selected.delete(doc.id);
  await load();
}

function toggle(id: string, on: boolean): void {
  if (on) state.selected.add(id);
  else state.selected.delete(id);
}

/** Forget everything of the previous user (logout / session expiry — NR-03). */
function reset(): void {
  stopPolling();
  latestRequest++;
  state.docs = [];
  state.selected.clear();
  state.uploads = [];
  state.error = null;
}

export function useDocuments() {
  return { state, load, upload, remove, toggle, stopPolling, reset };
}
