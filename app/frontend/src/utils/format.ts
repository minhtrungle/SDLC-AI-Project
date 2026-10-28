import type { DocumentStatus } from "@/api/types";

/** Status is shown with an icon AND text, never colour alone (UX-002). */
export const STATUS_LABELS: Record<DocumentStatus, { icon: string; label: string }> = {
  processing: { icon: "◌", label: "Đang xử lý" },
  ready: { icon: "✓", label: "Sẵn sàng" },
  failed: { icon: "✕", label: "Lỗi" },
  no_text: { icon: "!", label: "Không trích xuất được văn bản" },
};

export function formatDate(iso: string): string {
  return new Date(iso).toLocaleString("vi-VN", { dateStyle: "short", timeStyle: "short" });
}

export function percent(value: number | null | undefined): string {
  return value == null ? "—" : `${Math.round(value * 100)}%`;
}

/** sessionStorage can be unavailable (private mode); never let that break the app. */
export const sessionStore = {
  get(key: string): string | null {
    try {
      return sessionStorage.getItem(key);
    } catch {
      return null;
    }
  },
  set(key: string, value: string | null): void {
    try {
      if (value == null) sessionStorage.removeItem(key);
      else sessionStorage.setItem(key, value);
    } catch {
      /* ignore */
    }
  },
};
