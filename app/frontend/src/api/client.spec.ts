import { afterEach, describe, expect, it, vi } from "vitest";

import { api, ApiError, request, setCsrf, setUnauthorizedHandler, uploadFile } from "./client";

function mockFetch(status: number, body: unknown) {
  const fn = vi.fn().mockResolvedValue(new Response(status === 204 ? null : JSON.stringify(body), { status }));
  vi.stubGlobal("fetch", fn);
  return fn;
}

afterEach(() => {
  vi.unstubAllGlobals();
  setCsrf(null);
  setUnauthorizedHandler(() => {});
});

describe("request", () => {
  it("sends the CSRF header on writes only (AC-NFR-010)", async () => {
    setCsrf("tok");
    const fetchFn = mockFetch(200, { id: "c1", created_at: "x", turns: [] });
    await api.newConversation();
    expect(fetchFn.mock.calls[0]![1].headers["X-CSRF-Token"]).toBe("tok");
    await api.documents();
    expect(fetchFn.mock.calls[1]![1].headers["X-CSRF-Token"]).toBeUndefined();
  });

  it("raises ApiError with the problem code and Vietnamese title", async () => {
    mockFetch(422, { code: "chat.invalid_question", title: "Câu hỏi không hợp lệ" });
    await expect(api.ask("c1", "x", null)).rejects.toMatchObject({ status: 422, code: "chat.invalid_question" });
  });

  it("calls the unauthorized handler on 401 auth.required (EC-15)", async () => {
    const handler = vi.fn();
    setUnauthorizedHandler(handler);
    mockFetch(401, { code: "auth.required", title: "Bạn cần đăng nhập" });
    await expect(api.me()).rejects.toBeInstanceOf(ApiError);
    expect(handler).toHaveBeenCalledOnce();
  });

  it("maps network failures to a readable error (EC-04)", async () => {
    vi.stubGlobal("fetch", vi.fn().mockRejectedValue(new TypeError("Failed to fetch")));
    await expect(request("GET", "/api/health")).rejects.toMatchObject({ status: 0, code: "network" });
  });

  it("handles 204 and sends scope only when given (FR-015)", async () => {
    const fetchFn = mockFetch(204, null);
    await expect(api.logout()).resolves.toBeUndefined();
    mockFetch(200, {});
    await api.ask("c1", "q", ["d1"]);
    const sent = JSON.parse((vi.mocked(fetch).mock.calls[0]![1] as RequestInit).body as string);
    expect(sent).toEqual({ question: "q", document_ids: ["d1"] });
    expect(fetchFn).toHaveBeenCalledOnce();
  });
});

class FakeXHR {
  static last: FakeXHR;
  status = 200;
  responseText = "";
  headers: Record<string, string> = {};
  upload: { onprogress?: (e: { lengthComputable: boolean; loaded: number; total: number }) => void } = {};
  onload?: () => void;
  onerror?: () => void;
  constructor() {
    FakeXHR.last = this;
  }
  open() {}
  setRequestHeader(k: string, v: string) {
    this.headers[k] = v;
  }
  send() {}
}

describe("uploadFile (AC-201.3)", () => {
  it("reports progress and resolves with the file result", async () => {
    vi.stubGlobal("XMLHttpRequest", FakeXHR);
    setCsrf("tok");
    const progress = vi.fn();
    const pending = uploadFile(new File(["%PDF"], "a.pdf"), progress);
    const xhr = FakeXHR.last;
    xhr.upload.onprogress?.({ lengthComputable: true, loaded: 1, total: 2 });
    xhr.responseText = JSON.stringify({ results: [{ filename: "a.pdf", ok: true }] });
    xhr.onload?.();
    await expect(pending).resolves.toEqual({ filename: "a.pdf", ok: true });
    expect(progress).toHaveBeenCalledWith(0.5);
    expect(xhr.headers["X-CSRF-Token"]).toBe("tok");
  });

  it("rejects on HTTP errors and network failures", async () => {
    vi.stubGlobal("XMLHttpRequest", FakeXHR);
    const failing = uploadFile(new File(["x"], "a.pdf"), () => {});
    FakeXHR.last.status = 413;
    FakeXHR.last.responseText = JSON.stringify({ code: "request.too_large", title: "Quá lớn" });
    FakeXHR.last.onload?.();
    await expect(failing).rejects.toMatchObject({ status: 413, code: "request.too_large" });
    const offline = uploadFile(new File(["x"], "a.pdf"), () => {});
    FakeXHR.last.onerror?.();
    await expect(offline).rejects.toMatchObject({ code: "network" });
  });
});
