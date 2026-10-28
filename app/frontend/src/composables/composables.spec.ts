import { flushPromises, mount } from "@vue/test-utils";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

import type { DocumentInfo } from "@/api/types";

const apiMock = vi.hoisted(() => ({
  config: vi.fn(),
  me: vi.fn(),
  logout: vi.fn(),
  documents: vi.fn(),
  deleteDocument: vi.fn(),
  conversation: vi.fn(),
  chunk: vi.fn(),
}));
const uploadMock = vi.hoisted(() => vi.fn());
vi.mock("@/api/client", async (importOriginal) => ({
  ...(await importOriginal<typeof import("@/api/client")>()),
  api: apiMock,
  uploadFile: uploadMock,
}));

import AppHeader from "@/components/AppHeader.vue";
import WorkspaceView from "@/components/WorkspaceView.vue";

import { useChat } from "./useChat";
import { useDocuments } from "./useDocuments";
import { CONVERSATION_KEY, DRAFT_KEY, useSession } from "./useSession";

const doc = (id: string, status: DocumentInfo["status"]): DocumentInfo => ({
  id,
  filename: `${id}.pdf`,
  size_bytes: 1,
  status,
  created_at: "2026-10-28T09:00:00Z",
});

beforeEach(() => {
  Object.values(apiMock).forEach((fn) => fn.mockReset());
  uploadMock.mockReset();
  const docs = useDocuments();
  docs.state.docs = [];
  docs.state.selected.clear();
  docs.state.uploads = [];
  sessionStorage.clear();
});
afterEach(() => {
  useDocuments().stopPolling();
  vi.useRealTimers();
});

describe("useDocuments", () => {
  it("polls while a document is processing, then stops (AC-203.2)", async () => {
    vi.useFakeTimers();
    apiMock.documents
      .mockResolvedValueOnce({ documents: [doc("a", "processing")] })
      .mockResolvedValueOnce({ documents: [doc("a", "ready")] });
    const docs = useDocuments();
    await docs.load();
    expect(docs.state.docs[0]!.status).toBe("processing");
    await vi.advanceTimersByTimeAsync(2000);
    expect(docs.state.docs[0]!.status).toBe("ready");
    await vi.advanceTimersByTimeAsync(4000);
    expect(apiMock.documents).toHaveBeenCalledTimes(2);
  });

  it("drops a selection when the document is no longer ready", async () => {
    const docs = useDocuments();
    docs.toggle("gone", true);
    apiMock.documents.mockResolvedValue({ documents: [] });
    await docs.load();
    expect(docs.state.selected.size).toBe(0);
    docs.toggle("x", true);
    docs.toggle("x", false);
    expect(docs.state.selected.has("x")).toBe(false);
  });

  it("reports load errors", async () => {
    apiMock.documents.mockRejectedValue(new Error("Mất kết nối."));
    const docs = useDocuments();
    await docs.load();
    expect(docs.state.error).toBe("Mất kết nối.");
  });

  it("tracks per-file upload results, one bad file never blocks others (AC-201.2)", async () => {
    vi.useFakeTimers();
    uploadMock
      .mockImplementationOnce(async (_f: File, onProgress: (p: number) => void) => {
        onProgress(1);
        return { filename: "a.pdf", ok: true };
      })
      .mockResolvedValueOnce({ filename: "b.docx", ok: false, error: { code: "file.wrong_type", message: "Sai định dạng" } })
      .mockRejectedValueOnce(new Error("Mất kết nối khi tải lên."));
    apiMock.documents.mockResolvedValue({ documents: [doc("a", "ready")] });
    const docs = useDocuments();
    await docs.upload([new File(["1"], "a.pdf"), new File(["2"], "b.docx"), new File(["3"], "c.pdf")]);
    expect(docs.state.uploads.map((u) => [u.done, u.error])).toEqual([
      [true, null],
      [false, "Sai định dạng"],
      [false, "Mất kết nối khi tải lên."],
    ]);
    await vi.advanceTimersByTimeAsync(4000);
    expect(docs.state.uploads).toHaveLength(2); // successful uploads disappear, errors stay visible
    await docs.upload([]);
  });

  it("removes a document and its selection", async () => {
    apiMock.deleteDocument.mockResolvedValue(undefined);
    apiMock.documents.mockResolvedValue({ documents: [] });
    const docs = useDocuments();
    docs.toggle("a", true);
    await docs.remove(doc("a", "ready"));
    expect(apiMock.deleteDocument).toHaveBeenCalledWith("a");
    expect(docs.state.selected.size).toBe(0);
  });
});

describe("useSession", () => {
  it("keeps the draft question when the session expires (EC-15)", () => {
    const session = useSession();
    session.state.me = { id: 1, username: "linh", role: "user", csrf_token: "t" };
    const area = document.createElement("textarea");
    area.id = "question";
    area.value = "Câu hỏi đang soạn";
    document.body.append(area);
    session.expire();
    expect(JSON.parse(sessionStorage.getItem(DRAFT_KEY)!)).toEqual({ username: "linh", text: "Câu hỏi đang soạn" });
    expect(session.state).toMatchObject({ view: "login", sessionExpired: true, me: null });
    session.expire(); // no-op when already signed out
    area.remove();
  });

  it("logs out, forgets the conversation and falls back to default config", async () => {
    apiMock.config.mockRejectedValue(new Error("offline"));
    apiMock.me.mockRejectedValue(new Error("401"));
    const session = useSession();
    await session.boot();
    expect(session.state.config.max_question_chars).toBe(2000);
    sessionStorage.setItem(CONVERSATION_KEY, "c1");
    apiMock.logout.mockResolvedValue(undefined);
    await session.logout();
    expect(sessionStorage.getItem(CONVERSATION_KEY)).toBeNull();
    expect(session.state.view).toBe("login");
    session.show("dashboard");
    expect(session.state.view).toBe("dashboard");
  });
});

describe("useChat.restore", () => {
  it("drops a conversation id the server no longer knows", async () => {
    sessionStorage.setItem(CONVERSATION_KEY, "old");
    apiMock.conversation.mockRejectedValue(new Error("404"));
    const chat = useChat();
    await chat.restore();
    expect(chat.state.conversationId).toBeNull();
    expect(sessionStorage.getItem(CONVERSATION_KEY)).toBeNull();
  });
});

describe("AppHeader", () => {
  it("shows the dashboard link only to managers (US-502)", async () => {
    const session = useSession();
    session.state.me = { id: 1, username: "hung", role: "manager", csrf_token: "t" };
    const wrapper = mount(AppHeader);
    await wrapper.findAll("button").find((b) => b.text() === "Số liệu sử dụng")!.trigger("click");
    expect(session.state.view).toBe("dashboard");
    await wrapper.get("button[aria-label='Về màn hình chính']").trigger("click");
    expect(session.state.view).toBe("workspace");
    session.state.me = { id: 2, username: "linh", role: "user", csrf_token: "t" };
    await flushPromises();
    expect(wrapper.text()).not.toContain("Số liệu sử dụng");
  });
});

describe("WorkspaceView delete flow (US-205)", () => {
  it("asks for confirmation before deleting (AC-205.3)", async () => {
    apiMock.documents.mockResolvedValue({ documents: [doc("a", "ready")] });
    apiMock.deleteDocument.mockResolvedValue(undefined);
    const wrapper = mount(WorkspaceView, { attachTo: document.body });
    await flushPromises();
    await wrapper.get("[aria-label='Xóa a.pdf']").trigger("click");
    expect(document.body.textContent).toContain("Xóa tài liệu?");
    expect(apiMock.deleteDocument).not.toHaveBeenCalled();
    await wrapper.get("button.btn-danger").trigger("click");
    await flushPromises();
    expect(apiMock.deleteDocument).toHaveBeenCalledWith("a");
    wrapper.unmount();
  });

  it("cancel keeps the document", async () => {
    apiMock.documents.mockResolvedValue({ documents: [doc("a", "ready")] });
    const wrapper = mount(WorkspaceView, { attachTo: document.body });
    await flushPromises();
    await wrapper.get("[aria-label='Xóa a.pdf']").trigger("click");
    await wrapper.findAll("dialog button").find((b) => b.text() === "Hủy")!.trigger("click");
    expect(wrapper.find("dialog").exists()).toBe(false);
    expect(apiMock.deleteDocument).not.toHaveBeenCalled();
    wrapper.unmount();
  });
});
