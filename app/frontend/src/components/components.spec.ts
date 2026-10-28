import { flushPromises, mount } from "@vue/test-utils";
import { beforeEach, describe, expect, it, vi } from "vitest";

import type { Citation, DocumentInfo, Turn } from "@/api/types";

const apiMock = vi.hoisted(() => ({
  config: vi.fn(),
  me: vi.fn(),
  login: vi.fn(),
  logout: vi.fn(),
  documents: vi.fn(),
  deleteDocument: vi.fn(),
  chunk: vi.fn(),
  newConversation: vi.fn(),
  conversation: vi.fn(),
  ask: vi.fn(),
  feedback: vi.fn(),
  weekly: vi.fn(),
}));
vi.mock("@/api/client", async (importOriginal) => ({
  ...(await importOriginal<typeof import("@/api/client")>()),
  api: apiMock,
}));

import App from "@/App.vue";
import AnswerMessage from "@/components/AnswerMessage.vue";
import ChatPanel from "@/components/ChatPanel.vue";
import CitationDrawer from "@/components/CitationDrawer.vue";
import DocumentPanel from "@/components/DocumentPanel.vue";
import UsageDashboard from "@/components/UsageDashboard.vue";
import { useChat } from "@/composables/useChat";
import { useDocuments } from "@/composables/useDocuments";
import { useSession } from "@/composables/useSession";

const citation: Citation = {
  index: 1,
  chunk_id: 42,
  document_id: "d1",
  document_name: "HopDong_Alpha.pdf",
  page: 2,
  snippet: "Giá trị hợp đồng Alpha là 2,5 tỷ đồng.",
  document_deleted: false,
};
const turn = (over: Partial<Turn> = {}): Turn => ({
  id: "t1",
  question: "Giá trị hợp đồng Alpha?",
  answer: "Theo tài liệu đã tải lên:\n- Giá trị hợp đồng Alpha là 2,5 tỷ đồng. [1]",
  outcome: "answered",
  citations: [citation],
  latency_ms: 3,
  created_at: "2026-10-28T09:00:00Z",
  ...over,
});
const doc = (id: string, status: DocumentInfo["status"]): DocumentInfo => ({
  id,
  filename: `${id}.pdf`,
  size_bytes: 10,
  page_count: 3,
  status,
  created_at: "2026-10-28T09:00:00Z",
});

beforeEach(() => {
  Object.values(apiMock).forEach((fn) => fn.mockReset());
  const docs = useDocuments();
  docs.stopPolling();
  docs.state.docs = [];
  docs.state.selected.clear();
  docs.state.uploads = [];
  const chat = useChat();
  chat.state.turns = [];
  chat.state.conversationId = null;
  chat.state.error = null;
  sessionStorage.clear();
});

describe("App + LoginView (US-101)", () => {
  it("shows the login screen when not signed in, then the workspace after login", async () => {
    apiMock.config.mockResolvedValue({ ai_mode: "local", max_file_mb: 20, max_docs: 50, max_question_chars: 2000 });
    apiMock.me.mockRejectedValue(new Error("401"));
    apiMock.login.mockResolvedValue({ id: 1, username: "linh", role: "user", csrf_token: "t" });
    apiMock.documents.mockResolvedValue({ documents: [] });
    const wrapper = mount(App, { attachTo: document.body });
    await flushPromises();
    expect(wrapper.text()).toContain("Đăng nhập");
    await wrapper.get("#username").setValue("linh");
    await wrapper.get("#password").setValue("matkhau-123");
    await wrapper.get("form").trigger("submit");
    await flushPromises();
    expect(apiMock.login).toHaveBeenCalledWith("linh", "matkhau-123");
    expect(wrapper.text()).toContain("Tài liệu (0)");
    expect(wrapper.text()).toContain("Xử lý cục bộ");
    wrapper.unmount();
  });

  it("shows the server message on wrong credentials (AC-101.3)", async () => {
    apiMock.config.mockResolvedValue({ ai_mode: "local", max_file_mb: 20, max_docs: 50, max_question_chars: 2000 });
    apiMock.me.mockRejectedValue(new Error("401"));
    apiMock.login.mockRejectedValue(new Error("Tên đăng nhập hoặc mật khẩu không đúng."));
    useSession().state.view = "loading";
    const wrapper = mount(App);
    await flushPromises();
    await wrapper.get("form").trigger("submit");
    await flushPromises();
    expect(wrapper.get("[role=alert]").text()).toBe("Tên đăng nhập hoặc mật khẩu không đúng.");
  });
});

describe("DocumentPanel (US-203, US-204)", () => {
  it("renders the empty state (AC-204.2)", () => {
    expect(mount(DocumentPanel).text()).toContain("Tải tài liệu đầu tiên");
  });

  it("lists name, status label and pages; only ready documents can be scoped", async () => {
    useDocuments().state.docs = [doc("a", "ready"), doc("b", "processing"), doc("c", "no_text")];
    const wrapper = mount(DocumentPanel);
    expect(wrapper.text()).toContain("Sẵn sàng");
    expect(wrapper.text()).toContain("Đang xử lý");
    expect(wrapper.text()).toContain("Không trích xuất được văn bản");
    const boxes = wrapper.findAll("input[type=checkbox]");
    expect(boxes.map((b) => (b.element as HTMLInputElement).disabled)).toEqual([false, true, true]);
    await boxes[0]!.setValue(true);
    expect(useDocuments().state.selected.has("a")).toBe(true);
    await wrapper.get("[aria-label='Xóa a.pdf']").trigger("click");
    expect(wrapper.emitted("delete")?.[0]).toEqual([useDocuments().state.docs[0]]);
  });
});

describe("AnswerMessage (US-305, US-501)", () => {
  it("renders [n] as a button that opens the citation", async () => {
    const wrapper = mount(AnswerMessage, { props: { turn: turn() } });
    await wrapper.get("button.cite").trigger("click");
    expect(wrapper.emitted("open-citation")?.[0]).toEqual([citation]);
    expect(wrapper.text()).toContain("HopDong_Alpha.pdf — tr. 2");
  });

  it("marks not-found answers, deleted sources and processing warnings", () => {
    const wrapper = mount(AnswerMessage, {
      props: {
        turn: turn({
          outcome: "not_found",
          citations: [{ ...citation, document_deleted: true }],
          warning: "docs_processing",
        }),
      },
    });
    expect(wrapper.classes()).toContain("not-found");
    expect(wrapper.text()).toContain("tài liệu đã bị xóa");
    expect(wrapper.text()).toContain("Một số tài liệu đang xử lý");
  });

  it("records feedback and reflects it with aria-pressed", async () => {
    apiMock.feedback.mockResolvedValue({});
    const t = turn();
    const wrapper = mount(AnswerMessage, { props: { turn: t } });
    await wrapper.get("[aria-label='Hữu ích']").trigger("click");
    await flushPromises();
    expect(apiMock.feedback).toHaveBeenCalledWith("t1", "up", null);
    expect(t.feedback).toBe("up");
  });
});

describe("ChatPanel (US-301, US-402, US-403)", () => {
  it("disables the question box without ready documents (AC-301.5)", () => {
    const wrapper = mount(ChatPanel);
    expect((wrapper.get("textarea").element as HTMLTextAreaElement).disabled).toBe(true);
    expect(wrapper.text()).toContain("Hãy tải tài liệu để bắt đầu hỏi.");
  });

  it("sends with Enter, scoped to selected documents, and shows the answer", async () => {
    useDocuments().state.docs = [doc("a", "ready")];
    useDocuments().state.selected.add("a");
    apiMock.newConversation.mockResolvedValue({ id: "c1", created_at: "x", turns: [] });
    apiMock.ask.mockResolvedValue(turn());
    const wrapper = mount(ChatPanel);
    expect(wrapper.text()).toContain("Phạm vi: 1 tài liệu đã chọn");
    await wrapper.get("textarea").setValue("Giá trị hợp đồng Alpha?");
    await wrapper.get("textarea").trigger("keydown", { key: "Enter" });
    await flushPromises();
    expect(apiMock.ask).toHaveBeenCalledWith("c1", "Giá trị hợp đồng Alpha?", ["a"]);
    expect(wrapper.text()).toContain("2,5 tỷ đồng");
    expect((wrapper.get("textarea").element as HTMLTextAreaElement).value).toBe("");
  });

  it("keeps the question and offers retry when sending fails (EC-04)", async () => {
    useDocuments().state.docs = [doc("a", "ready")];
    apiMock.newConversation.mockResolvedValue({ id: "c1", created_at: "x", turns: [] });
    apiMock.ask.mockRejectedValue(new Error("Mất kết nối."));
    const wrapper = mount(ChatPanel);
    await wrapper.get("textarea").setValue("Câu hỏi");
    await wrapper.get("button.btn-primary").trigger("click");
    await flushPromises();
    expect(wrapper.get("[role=alert]").text()).toContain("Mất kết nối.");
    expect((wrapper.get("textarea").element as HTMLTextAreaElement).value).toBe("Câu hỏi");
    await wrapper.get("[role=alert] button").trigger("click");
    expect(apiMock.ask).toHaveBeenCalledTimes(2);
  });

  it("starts a new, empty conversation (AC-403.2)", async () => {
    useChat().state.turns = [turn()];
    const wrapper = mount(ChatPanel);
    await wrapper.findAll("button").find((b) => b.text() === "Cuộc hội thoại mới")!.trigger("click");
    expect(useChat().state.turns).toEqual([]);
  });
});

describe("CitationDrawer (AC-305.2)", () => {
  it("loads the original passage and closes with Escape", async () => {
    apiMock.chunk.mockResolvedValue({ chunk_id: 42, document_id: "d1", document_name: "A", page: 2, text: "Đoạn gốc đầy đủ." });
    const wrapper = mount(CitationDrawer, { props: { citation } });
    await flushPromises();
    expect(wrapper.text()).toContain("Đoạn gốc đầy đủ.");
    document.dispatchEvent(new KeyboardEvent("keydown", { key: "Escape" }));
    expect(wrapper.emitted("close")).toBeTruthy();
  });

  it("falls back to the stored snippet for deleted documents (AC-205.4)", () => {
    const wrapper = mount(CitationDrawer, { props: { citation: { ...citation, document_deleted: true } } });
    expect(wrapper.text()).toContain("Tài liệu đã bị xóa.");
    expect(apiMock.chunk).not.toHaveBeenCalled();
  });
});

describe("UsageDashboard (US-502)", () => {
  it("renders weekly metrics", async () => {
    apiMock.weekly.mockResolvedValue({
      weeks: [{ week: "2026-W44", active_users: 2, questions: 3, not_found_rate: 0.3333, positive_feedback_rate: 1 }],
    });
    const wrapper = mount(UsageDashboard);
    await flushPromises();
    expect(wrapper.text()).toContain("2026-W44");
    expect(wrapper.text()).toContain("33%");
    expect(wrapper.text()).toContain("100%");
  });

  it("shows the error for non-managers (AC-502.2)", async () => {
    apiMock.weekly.mockRejectedValue(new Error("Bạn không có quyền thực hiện thao tác này."));
    const wrapper = mount(UsageDashboard);
    await flushPromises();
    expect(wrapper.get("[role=alert]").text()).toContain("không có quyền");
  });
});
