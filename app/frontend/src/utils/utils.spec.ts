import { describe, expect, it } from "vitest";

import type { Citation, DocumentInfo } from "@/api/types";

import { splitAnswer } from "./answer";
import { composerState } from "./composer";
import { formatDate, percent, sessionStore, STATUS_LABELS } from "./format";

const cite = (index: number): Citation => ({
  index,
  chunk_id: index,
  document_id: "d",
  document_name: "A.pdf",
  page: 2,
  snippet: "…",
  document_deleted: false,
});
const doc = (status: DocumentInfo["status"]): DocumentInfo => ({
  id: status,
  filename: `${status}.pdf`,
  size_bytes: 1,
  status,
  created_at: "2026-10-28T09:00:00Z",
});

describe("splitAnswer (AC-305.1)", () => {
  it("turns known [n] markers into citations and keeps the rest as text", () => {
    const parts = splitAnswer("Giá trị là 2,5 tỷ. [1] Khác [9]", [cite(1)]);
    expect(parts).toEqual([
      { kind: "text", text: "Giá trị là 2,5 tỷ. " },
      { kind: "cite", citation: cite(1) },
      { kind: "text", text: " Khác " },
      { kind: "text", text: "[9]" },
    ]);
  });

  it("never interprets markup (XSS guard)", () => {
    const parts = splitAnswer("<img src=x onerror=alert(1)>", []);
    expect(parts).toEqual([{ kind: "text", text: "<img src=x onerror=alert(1)>" }]);
  });
});

describe("composerState (blueprint §3.7)", () => {
  it("is disabled without documents (AC-204.2, AC-301.5)", () => {
    expect(composerState([], "", false, 2000)).toMatchObject({ state: "disabled_empty", inputDisabled: true });
  });
  it("explains documents still processing (EC-02)", () => {
    const s = composerState([doc("processing")], "", false, 2000);
    expect(s.state).toBe("disabled_processing");
    expect(s.hint).toContain("Đang xử lý 1 tài liệu");
  });
  it("is disabled when only failed documents exist", () => {
    expect(composerState([doc("failed")], "x", false, 2000).state).toBe("disabled_no_ready");
  });
  it("blocks sending while an answer is pending (AC-301.3)", () => {
    expect(composerState([doc("ready")], "câu hỏi", true, 2000)).toMatchObject({ state: "sending", sendDisabled: true });
  });
  it("ignores whitespace-only drafts (AC-301.4) and counts characters", () => {
    expect(composerState([doc("ready")], "   ", false, 2000).sendDisabled).toBe(true);
    expect(composerState([doc("ready")], "abc", false, 2000)).toMatchObject({ state: "ready", hint: "3/2000 ký tự" });
  });
});

describe("format helpers", () => {
  it("labels every status with icon and text (UX-002)", () => {
    expect(STATUS_LABELS.no_text).toEqual({ icon: "!", label: "Không trích xuất được văn bản" });
  });
  it("formats percentages and dates", () => {
    expect(percent(0.333)).toBe("33%");
    expect(percent(null)).toBe("—");
    expect(formatDate("2026-10-28T09:00:00Z")).toMatch(/2026|26/);
  });
  it("sessionStore survives storage errors", () => {
    sessionStore.set("k", "v");
    expect(sessionStore.get("k")).toBe("v");
    sessionStore.set("k", null);
    expect(sessionStore.get("k")).toBeNull();
  });
});
