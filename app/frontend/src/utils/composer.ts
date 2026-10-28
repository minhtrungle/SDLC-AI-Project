import type { DocumentInfo } from "@/api/types";

export interface ComposerState {
  /** Canonical state name — blueprint §3.7. */
  state: "disabled_empty" | "disabled_processing" | "disabled_no_ready" | "sending" | "ready" | "ready_empty";
  inputDisabled: boolean;
  sendDisabled: boolean;
  hint: string;
}

/** Question box state from the document list (AC-204.2, AC-301.3, AC-301.5, EC-01/EC-02). */
export function composerState(
  docs: DocumentInfo[],
  draft: string,
  sending: boolean,
  maxChars: number,
): ComposerState {
  const ready = docs.filter((d) => d.status === "ready").length;
  const processing = docs.filter((d) => d.status === "processing").length;
  if (docs.length === 0) {
    return { state: "disabled_empty", inputDisabled: true, sendDisabled: true, hint: "Hãy tải tài liệu để bắt đầu hỏi." };
  }
  if (ready === 0 && processing > 0) {
    return {
      state: "disabled_processing",
      inputDisabled: true,
      sendDisabled: true,
      hint: `Đang xử lý ${processing} tài liệu, bạn có thể hỏi khi có ít nhất một tài liệu sẵn sàng.`,
    };
  }
  if (ready === 0) {
    return {
      state: "disabled_no_ready",
      inputDisabled: true,
      sendDisabled: true,
      hint: "Chưa có tài liệu nào sẵn sàng để hỏi.",
    };
  }
  if (sending) return { state: "sending", inputDisabled: false, sendDisabled: true, hint: "Đang trả lời…" };
  const empty = draft.trim().length === 0;
  return {
    state: empty ? "ready_empty" : "ready",
    inputDisabled: false,
    sendDisabled: empty,
    hint: `${draft.length}/${maxChars} ký tự`,
  };
}
