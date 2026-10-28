// Regression tests for L1 review round 2 (docs/07-verification/code-review-L1-round2.md).
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

import type { DocumentInfo } from "@/api/types";

const apiMock = vi.hoisted(() => ({ documents: vi.fn(), deleteDocument: vi.fn(), logout: vi.fn() }));
const uploadMock = vi.hoisted(() => vi.fn());
vi.mock("@/api/client", async (importOriginal) => ({
  ...(await importOriginal<typeof import("@/api/client")>()),
  api: apiMock,
  uploadFile: uploadMock,
}));

import { ApiError } from "@/api/client";

import { saveDraft, takeDraft } from "./keys";
import { useAnnouncer } from "./useAnnouncer";
import { useChat } from "./useChat";
import { useDocuments } from "./useDocuments";
import { useSession } from "./useSession";

const doc = (id: string, status: DocumentInfo["status"]): DocumentInfo => ({
  id,
  filename: `${id}.pdf`,
  size_bytes: 1,
  status,
  created_at: "2026-10-28T09:00:00Z",
});
const deferred = <T>() => {
  let resolve!: (v: T) => void;
  const promise = new Promise<T>((r) => (resolve = r));
  return { promise, resolve };
};

beforeEach(() => {
  Object.values(apiMock).forEach((fn) => fn.mockReset());
  uploadMock.mockReset();
  useDocuments().reset();
  sessionStorage.clear();
});
afterEach(() => vi.useRealTimers());

describe("NR-03 no data of the previous user after logout / expiry", () => {
  it("logout clears documents, selection and conversation", async () => {
    const session = useSession();
    session.state.me = { id: 1, username: "linh", role: "user", csrf_token: "t" };
    useDocuments().state.docs = [doc("a", "ready")];
    useDocuments().state.selected.add("a");
    useChat().state.turns = [{ id: "t", question: "q", answer: "a", outcome: "answered", citations: [], latency_ms: 1, created_at: "x" }];
    useChat().state.error = "Mất kết nối.";
    apiMock.logout.mockResolvedValue(undefined);
    await session.logout();
    expect(useDocuments().state.docs).toEqual([]);
    expect(useDocuments().state.selected.size).toBe(0);
    expect(useChat().state.turns).toEqual([]);
    expect(useChat().state.error).toBeNull();
  });

  it("session expiry clears data too, and the saved draft is offered only to the same user", () => {
    const session = useSession();
    session.state.me = { id: 1, username: "linh", role: "user", csrf_token: "t" };
    useDocuments().state.docs = [doc("a", "ready")];
    session.expire();
    expect(useDocuments().state.docs).toEqual([]);
    saveDraft("linh", "câu hỏi của Linh");
    expect(takeDraft("mai")).toBe(""); // another user never sees it…
    saveDraft("linh", "câu hỏi của Linh");
    expect(takeDraft("linh")).toBe("câu hỏi của Linh"); // …the same user gets it back once
    expect(takeDraft("linh")).toBe("");
  });
});

describe("NR-12 logout failure", () => {
  it("stays signed in and tells the user when the server cannot end the session", async () => {
    const session = useSession();
    session.state.me = { id: 1, username: "linh", role: "user", csrf_token: "t" };
    session.state.view = "workspace";
    apiMock.logout.mockRejectedValue(new ApiError(0, { code: "network", title: "Mất kết nối." }));
    await session.logout();
    expect(session.state.view).toBe("workspace");
    expect(useAnnouncer().message.value).toContain("Không đăng xuất được");
  });
});

describe("NR-04 / NR-06 polling", () => {
  it("does not start polling again after stopPolling (unmount) while a request is in flight", async () => {
    vi.useFakeTimers();
    const pending = deferred<{ documents: DocumentInfo[] }>();
    apiMock.documents.mockReturnValueOnce(pending.promise).mockResolvedValue({ documents: [doc("a", "processing")] });
    const docs = useDocuments();
    const loading = docs.load();
    docs.stopPolling(); // component unmounted / user logged out
    pending.resolve({ documents: [doc("a", "processing")] });
    await loading;
    await vi.advanceTimersByTimeAsync(10_000);
    expect(apiMock.documents).toHaveBeenCalledTimes(1);
  });

  it("ignores a stale poll response that arrives after a newer load (deleted document stays gone)", async () => {
    const stale = deferred<{ documents: DocumentInfo[] }>();
    apiMock.documents.mockReturnValueOnce(stale.promise).mockResolvedValueOnce({ documents: [doc("b", "ready")] });
    apiMock.deleteDocument.mockResolvedValue(undefined);
    const docs = useDocuments();
    const poll = docs.load(); // old poll, still in flight
    await docs.remove(doc("a", "ready")); // newer load after delete: only "b"
    stale.resolve({ documents: [doc("a", "ready"), doc("b", "ready")] });
    await poll;
    expect(docs.state.docs.map((d) => d.id)).toEqual(["b"]);
  });
});

describe("NR-05 upload batches", () => {
  it("clearing a finished batch never removes rows of a newer batch", async () => {
    vi.useFakeTimers();
    apiMock.documents.mockResolvedValue({ documents: [] });
    uploadMock.mockResolvedValueOnce({ filename: "a.pdf", ok: true });
    const docs = useDocuments();
    await docs.upload([new File(["1"], "a.pdf")]);
    const second = deferred<{ filename: string; ok: boolean }>();
    uploadMock.mockReturnValueOnce(second.promise);
    const running = docs.upload([new File(["2"], "b.pdf")]);
    await vi.advanceTimersByTimeAsync(4000); // first batch's cleanup fires while b.pdf is uploading
    expect(docs.state.uploads.map((u) => u.name)).toEqual(["b.pdf"]);
    second.resolve({ filename: "b.pdf", ok: false, error: { code: "file.too_large", message: "Tệp vượt dung lượng" } } as never);
    await running;
    await vi.advanceTimersByTimeAsync(4000);
    expect(docs.state.uploads.map((u) => [u.name, u.error])).toEqual([["b.pdf", "Tệp vượt dung lượng"]]);
  });
});
