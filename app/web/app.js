// CMP-01 Web UI — SCR-01..SCR-06 (docs/04-design/UI_UX_design/README.md). Vanilla ES modules, no build (ADR-006).
import { api, setCsrf, setUnauthorizedHandler, uploadFile } from "./api.js";

const root = document.getElementById("app");
const STATUS = {
  processing: ["◌", "Đang xử lý"],
  ready: ["✓", "Sẵn sàng"],
  failed: ["✕", "Lỗi"],
  no_text: ["!", "Không trích xuất được văn bản"],
};
const DRAFT_KEY = "cwd.draft";
const CONV_KEY = "cwd.conversation";

const state = {
  config: null, me: null, docs: [], selected: new Set(), uploads: [],
  conversationId: null, turns: [], sending: false, lastError: null, pollTimer: null,
};

// ---------------------------------------------------------------- helpers
function h(tag, attrs = {}, ...children) {
  const el = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs)) {
    if (v === false || v == null) continue;
    if (k === "class") el.className = v;
    else if (k.startsWith("on")) el.addEventListener(k.slice(2), v);
    else el.setAttribute(k, v === true ? "" : v);
  }
  for (const c of children.flat()) if (c != null && c !== false) el.append(c instanceof Node ? c : String(c));
  return el;
}
const fmtDate = (iso) => new Date(iso).toLocaleString("vi-VN", { dateStyle: "short", timeStyle: "short" });
const session = {
  get: (k) => { try { return sessionStorage.getItem(k); } catch { return null; } },
  set: (k, v) => { try { v == null ? sessionStorage.removeItem(k) : sessionStorage.setItem(k, v); } catch { /* private mode */ } },
};

// ---------------------------------------------------------------- boot
async function boot() {
  setUnauthorizedHandler(() => { if (state.me) expireSession(); });
  try { state.config = await api.config(); } catch { state.config = { ai_mode: "local", max_file_mb: 20, max_question_chars: 2000 }; }
  try {
    state.me = await api.me();
    setCsrf(state.me.csrf_token);
    await showWorkspace();
  } catch {
    showLogin();
  }
}

// ---------------------------------------------------------------- SCR-01 / SCR-06
function showLogin(expired = false) {
  stopPolling();
  const error = h("div", { class: "banner banner-error hidden", role: "alert" });
  const user = h("input", { id: "username", name: "username", autocomplete: "username", required: true });
  const pass = h("input", { id: "password", name: "password", type: "password", autocomplete: "current-password", required: true });
  const submit = h("button", { class: "btn btn-primary", type: "submit" }, "Đăng nhập");
  const form = h("form", { class: "card", onsubmit: async (e) => {
    e.preventDefault();
    submit.disabled = true;
    error.classList.add("hidden");
    try {
      state.me = await api.login(user.value.trim(), pass.value);
      setCsrf(state.me.csrf_token);
      await showWorkspace();
    } catch (err) {
      error.textContent = err.message;
      error.classList.remove("hidden");
      submit.disabled = false;
      pass.value = "";
      pass.focus();
    }
  } },
    h("div", { class: "brand" }, h("span", { class: "logo", "aria-hidden": "true" }, "📄"), "Chat với tài liệu"),
    h("h1", {}, "Đăng nhập"),
    expired ? h("div", { class: "banner banner-warning", role: "status" }, "Phiên đăng nhập đã hết hạn. Vui lòng đăng nhập lại; câu hỏi đang soạn đã được giữ lại.") : null,
    error,
    h("div", { class: "field" }, h("label", { for: "username" }, "Tên đăng nhập"), user),
    h("div", { class: "field" }, h("label", { for: "password" }, "Mật khẩu"), pass),
    submit,
  );
  root.replaceChildren(h("main", { class: "center" }, form));
  user.focus();
}

function expireSession() {
  const draft = document.getElementById("question");
  if (draft && draft.value.trim()) session.set(DRAFT_KEY, draft.value);
  state.me = null;
  setCsrf(null);
  showLogin(true);
}

// ---------------------------------------------------------------- SCR-02 workspace
async function showWorkspace() {
  root.replaceChildren(
    header(),
    h("main", { class: "workspace" },
      h("section", { class: "panel", "aria-labelledby": "docs-title", id: "docs-panel" }),
      h("section", { class: "panel", "aria-labelledby": "chat-title", id: "chat-panel" }),
    ),
    h("div", { id: "drawer-host" }),
    h("div", { id: "live", class: "sr-only", "aria-live": "polite" }),
  );
  await loadDocuments();
  state.conversationId = session.get(CONV_KEY);
  state.turns = [];
  if (state.conversationId) {
    try { state.turns = (await api.conversation(state.conversationId)).turns; } catch { state.conversationId = null; }
  }
  renderChat();
}

function header() {
  const menu = h("div", { class: "header-right" },
    h("span", { class: "badge badge-info", title: "Nơi xử lý nội dung tài liệu (FR-003)" },
      state.config.ai_mode === "local" ? "🔒 Xử lý cục bộ" : "☁ Dùng dịch vụ AI bên ngoài"),
    state.me.role === "manager" ? h("button", { class: "btn btn-ghost btn-sm", onclick: showDashboard }, "Số liệu sử dụng") : null,
    h("span", { class: "muted" }, state.me.username),
    h("button", { class: "btn btn-sm", onclick: async () => { try { await api.logout(); } finally { state.me = null; session.set(CONV_KEY, null); showLogin(); } } }, "Đăng xuất"),
  );
  return h("header", { class: "app-header" },
    h("button", { class: "brand btn-ghost btn", onclick: showWorkspace, "aria-label": "Về màn hình chính" },
      h("span", { class: "logo", "aria-hidden": "true" }, "📄"), "Chat với tài liệu"),
    menu);
}

// ---------------------------------------------------------------- documents
async function loadDocuments() {
  try { state.docs = (await api.documents()).documents; } catch (err) { announce(err.message); }
  for (const id of [...state.selected]) if (!state.docs.some((d) => d.id === id && d.status === "ready")) state.selected.delete(id);
  renderDocs();
  renderComposerState();
  schedulePolling();
}

function schedulePolling() {
  stopPolling();
  if (state.docs.some((d) => d.status === "processing")) state.pollTimer = setTimeout(loadDocuments, 2000);
}
function stopPolling() { if (state.pollTimer) clearTimeout(state.pollTimer); state.pollTimer = null; }

function renderDocs() {
  const panel = document.getElementById("docs-panel");
  if (!panel) return;
  const input = h("input", { type: "file", accept: "application/pdf,.pdf", multiple: true, class: "sr-only", id: "file-input",
    onchange: (e) => { startUploads([...e.target.files]); e.target.value = ""; } });
  const zone = h("div", { class: "dropzone",
    ondragover: (e) => { e.preventDefault(); zone.classList.add("drag"); },
    ondragleave: () => zone.classList.remove("drag"),
    ondrop: (e) => { e.preventDefault(); zone.classList.remove("drag"); startUploads([...e.dataTransfer.files]); } },
    h("button", { class: "btn btn-primary", onclick: () => input.click() }, "+ Tải lên PDF"),
    h("p", { class: "muted" }, `Kéo thả hoặc chọn nhiều file PDF, tối đa ${state.config.max_file_mb} MB mỗi file.`), input);

  const uploads = h("ul", { class: "upload-list", "aria-label": "Tiến độ tải lên" },
    state.uploads.map((u) => h("li", { class: "upload-item" },
      h("div", {}, u.name, " — ", u.error ? h("span", { class: "upload-error" }, u.error) : u.done ? "đã tải lên" : `${Math.round(u.progress * 100)}%`),
      u.done || u.error ? null : h("progress", { max: "1", value: String(u.progress), "aria-label": `Tiến độ ${u.name}` }))));

  const list = state.docs.length === 0
    ? h("div", { class: "empty" }, h("p", {}, "Chưa có tài liệu nào."), h("button", { class: "btn", onclick: () => input.click() }, "Tải tài liệu đầu tiên"))
    : h("ul", { class: "doc-list" }, state.docs.map(docItem));

  panel.replaceChildren(
    h("div", { class: "panel-head" }, h("h2", { id: "docs-title" }, `Tài liệu (${state.docs.length})`)),
    h("div", { class: "panel-body" }, zone, uploads, list),
  );
}

function docItem(d) {
  const [icon, label] = STATUS[d.status];
  const ready = d.status === "ready";
  const box = h("input", { type: "checkbox", disabled: !ready, checked: state.selected.has(d.id),
    "aria-label": `Chọn ${d.filename} làm phạm vi câu hỏi`,
    onchange: (e) => { e.target.checked ? state.selected.add(d.id) : state.selected.delete(d.id); renderScope(); } });
  return h("li", { class: "doc" }, box,
    h("div", {},
      h("div", { class: "doc-name" }, d.filename),
      h("div", { class: `status status-${d.status}` }, h("span", { "aria-hidden": "true" }, icon), label),
      h("div", { class: "muted" }, fmtDate(d.created_at), d.page_count ? ` · ${d.page_count} trang` : ""),
      d.error_message ? h("div", { class: "muted" }, d.error_message) : null),
    h("button", { class: "btn btn-ghost btn-sm", "aria-label": `Xóa ${d.filename}`, onclick: () => confirmDelete(d) }, "🗑"));
}

async function startUploads(files) {
  if (!files.length) return;
  const items = files.map((f) => ({ name: f.name, progress: 0, done: false, error: null }));
  state.uploads = items;
  renderDocs();
  await Promise.all(files.map(async (file, i) => {
    try {
      const result = await uploadFile(file, (p) => { items[i].progress = p; renderDocs(); });
      if (result.ok) items[i].done = true; else items[i].error = result.error.message;
    } catch (err) { items[i].error = err.message; }
    renderDocs();
  }));
  await loadDocuments();
  setTimeout(() => { state.uploads = state.uploads.filter((u) => u.error); renderDocs(); }, 4000);
}

// SCR-04 confirm delete (native <dialog> traps focus and closes on Esc)
function confirmDelete(doc) {
  const dlg = h("dialog", { "aria-labelledby": "dlg-title" },
    h("h2", { id: "dlg-title" }, "Xóa tài liệu?"),
    h("p", {}, `"${doc.filename}" sẽ bị xóa vĩnh viễn và không còn được dùng để trả lời câu hỏi.`),
    h("div", { class: "dialog-actions" },
      h("button", { class: "btn", value: "cancel", onclick: () => dlg.close() }, "Hủy"),
      h("button", { class: "btn btn-danger", onclick: async () => {
        dlg.close();
        try { await api.deleteDocument(doc.id); state.selected.delete(doc.id); announce(`Đã xóa ${doc.filename}`); }
        catch (err) { announce(err.message); }
        await loadDocuments();
      } }, "Xóa")));
  dlg.addEventListener("close", () => dlg.remove());
  document.body.append(dlg);
  dlg.showModal();
}

// ---------------------------------------------------------------- chat
function renderChat() {
  const panel = document.getElementById("chat-panel");
  if (!panel) return;
  const textarea = h("textarea", { id: "question", "aria-label": "Câu hỏi", maxlength: String(state.config.max_question_chars),
    placeholder: "Nhập câu hỏi… (Enter để gửi, Shift+Enter xuống dòng)",
    oninput: renderComposerState,
    onkeydown: (e) => { if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); send(); } } });
  textarea.value = session.get(DRAFT_KEY) || "";
  session.set(DRAFT_KEY, null);
  panel.replaceChildren(
    h("div", { class: "panel-head" }, h("h2", { id: "chat-title" }, "Hội thoại"),
      h("button", { class: "btn btn-sm", onclick: newConversation }, "Cuộc hội thoại mới")),
    h("div", { class: "scope", id: "scope" }),
    h("div", { class: "messages", id: "messages", "aria-live": "polite" }),
    h("div", { class: "composer" }, textarea,
      h("div", { class: "composer-row" },
        h("span", { id: "composer-hint", class: "muted" }),
        h("button", { class: "btn btn-primary", id: "send", onclick: send }, "Gửi"))),
  );
  renderScope();
  renderMessages();
  renderComposerState();
}

function renderScope() {
  const el = document.getElementById("scope");
  if (el) el.textContent = state.selected.size ? `Phạm vi: ${state.selected.size} tài liệu đã chọn` : "Phạm vi: Tất cả tài liệu";
}

function renderComposerState() {
  const ta = document.getElementById("question");
  const btn = document.getElementById("send");
  const hint = document.getElementById("composer-hint");
  if (!ta) return;
  const ready = state.docs.filter((d) => d.status === "ready").length;
  const processing = state.docs.filter((d) => d.status === "processing").length;
  let message = `${ta.value.length}/${state.config.max_question_chars} ký tự`;
  let disabled = false;
  if (state.docs.length === 0) { disabled = true; message = "Hãy tải tài liệu để bắt đầu hỏi."; }
  else if (ready === 0 && processing > 0) { disabled = true; message = `Đang xử lý ${processing} tài liệu, bạn có thể hỏi khi có ít nhất một tài liệu sẵn sàng.`; }
  else if (ready === 0) { disabled = true; message = "Chưa có tài liệu nào sẵn sàng để hỏi."; }
  if (state.sending) message = "Đang trả lời…";
  ta.disabled = disabled;
  btn.disabled = disabled || state.sending || !ta.value.trim();
  hint.textContent = message;
}

async function newConversation() {
  state.conversationId = null;
  state.turns = [];
  session.set(CONV_KEY, null);
  renderMessages();
  document.getElementById("question")?.focus();
}

async function send() {
  const ta = document.getElementById("question");
  const question = ta.value.trim();
  if (!question || state.sending || ta.disabled) return;
  state.sending = true;
  state.lastError = null;
  renderMessages(question);
  renderComposerState();
  try {
    if (!state.conversationId) {
      state.conversationId = (await api.newConversation()).id;
      session.set(CONV_KEY, state.conversationId);
    }
    const turn = await api.ask(state.conversationId, question, state.selected.size ? [...state.selected] : null);
    state.turns.push(turn);
    ta.value = "";
    announce(turn.outcome === "not_found" ? "Không tìm thấy thông tin trong tài liệu." : "Đã có câu trả lời.");
  } catch (err) {
    state.lastError = err.message;
  } finally {
    state.sending = false;
    renderMessages();
    renderComposerState();
    ta.focus();
  }
}

function renderMessages(pendingQuestion) {
  const box = document.getElementById("messages");
  if (!box) return;
  const items = state.turns.flatMap((t) => [h("div", { class: "msg msg-q" }, t.question), answerView(t)]);
  if (!state.turns.length && !pendingQuestion) {
    items.push(h("div", { class: "empty" }, "Hãy đặt câu hỏi về nội dung các tài liệu đã tải lên. Mỗi câu trả lời kèm nguồn để bạn kiểm chứng."));
  }
  if (pendingQuestion) items.push(h("div", { class: "msg msg-q" }, pendingQuestion), h("div", { class: "msg msg-a muted" }, "Đang trả lời…"));
  if (state.lastError) {
    items.push(h("div", { class: "msg msg-a", role: "alert" }, h("span", { class: "error-text" }, state.lastError), " ",
      h("button", { class: "btn btn-sm", onclick: send }, "Gửi lại")));
  }
  box.replaceChildren(...items);
  box.scrollTop = box.scrollHeight;
}

function answerView(turn) {
  const byIndex = new Map(turn.citations.map((c) => [c.index, c]));
  const text = h("div", { class: "answer-text" });
  for (const part of turn.answer.split(/(\[\d+\])/)) {
    const m = part.match(/^\[(\d+)\]$/);
    const c = m && byIndex.get(Number(m[1]));
    text.append(c ? h("button", { class: "cite", "aria-label": `Nguồn ${c.index}: ${c.document_name}, trang ${c.page}`, onclick: () => openCitation(c) }, `[${c.index}]`) : part);
  }
  const sources = turn.citations.length
    ? h("ol", { class: "sources", "aria-label": "Nguồn" }, turn.citations.map((c) => h("li", { value: String(c.index) },
      h("button", { class: "link", onclick: () => openCitation(c) }, `${c.document_name} — tr. ${c.page}`),
      c.document_deleted ? " (tài liệu đã bị xóa)" : "")))
    : null;
  const warning = turn.warning === "docs_processing"
    ? h("div", { class: "notice" }, "Một số tài liệu đang xử lý chưa được dùng để trả lời; câu trả lời có thể chưa đầy đủ.") : null;
  return h("div", { class: `msg msg-a${turn.outcome === "not_found" ? " not-found" : ""}` }, text, sources, warning, feedbackView(turn));
}

function feedbackView(turn) {
  const make = (rating, label, icon) => h("button", { class: "btn btn-sm", "aria-pressed": String(turn.feedback === rating), "aria-label": label,
    onclick: async () => {
      let reason = null;
      if (rating === "down") reason = window.prompt("Lý do (không bắt buộc, tối đa 500 ký tự):", "")?.slice(0, 500) || null;
      try { await api.feedback(turn.id, rating, reason); turn.feedback = rating; renderMessages(); announce("Đã ghi nhận đánh giá."); }
      catch (err) { announce(err.message); }
    } }, icon, " ", label);
  return h("div", { class: "feedback" }, make("up", "Hữu ích", "👍"), make("down", "Không hữu ích", "👎"));
}

// SCR-03 citation drawer
async function openCitation(c) {
  const host = document.getElementById("drawer-host");
  const opener = document.activeElement;
  const close = () => { host.replaceChildren(); document.removeEventListener("keydown", onKey); opener?.focus(); };
  const onKey = (e) => { if (e.key === "Escape") close(); };
  document.addEventListener("keydown", onKey);
  const body = h("div", { class: "panel-body" }, h("p", { class: "muted" }, "Đang tải đoạn gốc…"));
  const closeBtn = h("button", { class: "btn btn-sm", onclick: close, "aria-label": "Đóng panel nguồn" }, "Đóng");
  host.replaceChildren(h("aside", { class: "drawer", role: "dialog", "aria-label": "Nguồn trích dẫn" },
    h("div", { class: "panel-head" }, h("h2", {}, `Nguồn [${c.index}]`), closeBtn), body));
  closeBtn.focus();
  const meta = h("p", {}, h("strong", {}, c.document_name), ` — trang ${c.page}`);
  if (c.document_deleted) { body.replaceChildren(meta, h("div", { class: "notice" }, "Tài liệu đã bị xóa."), h("div", { class: "drawer-text" }, c.snippet)); return; }
  try {
    const chunk = await api.chunk(c.chunk_id);
    body.replaceChildren(meta, h("div", { class: "drawer-text" }, chunk.text));
  } catch {
    body.replaceChildren(meta, h("div", { class: "notice" }, "Không tải được đoạn gốc; hiển thị đoạn trích đã lưu."), h("div", { class: "drawer-text" }, c.snippet));
  }
}

// ---------------------------------------------------------------- SCR-05 dashboard
async function showDashboard() {
  stopPolling();
  const content = h("div", {}, h("p", { class: "muted" }, "Đang tải…"));
  root.replaceChildren(header(), h("main", { class: "dashboard" }, h("h1", {}, "Số liệu sử dụng theo tuần"), content));
  try {
    const { weeks } = await api.weekly();
    const max = Math.max(1, ...weeks.map((w) => w.questions));
    const pct = (x) => (x == null ? "—" : `${Math.round(x * 100)}%`);
    content.replaceChildren(h("table", {},
      h("caption", { class: "sr-only" }, "Người dùng hoạt động, số câu hỏi, tỷ lệ không tìm thấy và tỷ lệ đánh giá tích cực theo tuần"),
      h("thead", {}, h("tr", {}, ["Tuần", "Người dùng hoạt động", "Số câu hỏi", "", "Không tìm thấy", "Đánh giá tích cực"].map((t) => h("th", { scope: "col" }, t)))),
      h("tbody", {}, weeks.map((w) => h("tr", {},
        h("td", {}, w.week), h("td", {}, w.active_users), h("td", {}, w.questions),
        h("td", { "aria-hidden": "true", class: "bar-cell" }, bar(w.questions / max)),
        h("td", {}, pct(w.not_found_rate)), h("td", {}, pct(w.positive_feedback_rate)))))));
  } catch (err) {
    content.replaceChildren(h("div", { class: "banner banner-error", role: "alert" }, err.message));
  }
}

function bar(ratio) {
  const el = h("div", { class: "bar" });
  el.style.width = `${Math.round(ratio * 100)}%`; // CSSOM is allowed under CSP, inline style attributes are not
  return el;
}

function announce(text) {
  const live = document.getElementById("live");
  if (live) live.textContent = text;
}

boot();
