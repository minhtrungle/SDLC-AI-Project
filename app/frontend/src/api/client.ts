// HTTP client for the CWD API — contract: app/api-contract/openapi.yaml.
import type {
  Chunk,
  Conversation,
  DocumentInfo,
  Me,
  PublicConfig,
  Turn,
  UploadResult,
  WeeklyMetric,
} from "./types";

export class ApiError extends Error {
  readonly status: number;
  readonly code: string;

  constructor(status: number, problem: { title?: string; code?: string }) {
    super(problem.title || "Đã có lỗi xảy ra.");
    this.status = status;
    this.code = problem.code || "internal";
  }
}

let csrfToken: string | null = null;
let onUnauthorized: () => void = () => {};

export function setCsrf(token: string | null): void {
  csrfToken = token;
}

export function setUnauthorizedHandler(fn: () => void): void {
  onUnauthorized = fn;
}

async function parse<T>(res: Response): Promise<T> {
  if (res.status === 204) return undefined as T;
  const body = await res.json().catch(() => ({ title: "Không đọc được phản hồi từ máy chủ." }));
  if (!res.ok) {
    if (res.status === 401 && body.code === "auth.required") onUnauthorized();
    throw new ApiError(res.status, body);
  }
  return body as T;
}

export async function request<T>(method: string, path: string, body?: unknown): Promise<T> {
  const headers: Record<string, string> = {};
  if (body !== undefined) headers["Content-Type"] = "application/json";
  if (method !== "GET" && csrfToken) headers["X-CSRF-Token"] = csrfToken;
  let res: Response;
  try {
    res = await fetch(path, {
      method,
      headers,
      body: body === undefined ? undefined : JSON.stringify(body),
      credentials: "same-origin",
    });
  } catch {
    throw new ApiError(0, { code: "network", title: "Mất kết nối. Vui lòng kiểm tra mạng và thử lại." });
  }
  return parse<T>(res);
}

/** Upload one file with progress events (AC-201.3); resolves with that file's UploadResult. */
export function uploadFile(file: File, onProgress: (ratio: number) => void): Promise<UploadResult> {
  return new Promise((resolve, reject) => {
    const xhr = new XMLHttpRequest();
    const form = new FormData();
    form.append("files", file, file.name);
    xhr.open("POST", "/api/documents");
    if (csrfToken) xhr.setRequestHeader("X-CSRF-Token", csrfToken);
    xhr.upload.onprogress = (e) => {
      if (e.lengthComputable) onProgress(e.loaded / e.total);
    };
    xhr.onerror = () => reject(new ApiError(0, { code: "network", title: "Mất kết nối khi tải lên." }));
    xhr.onload = () => {
      let body: { results?: UploadResult[]; title?: string; code?: string } = {};
      try {
        body = JSON.parse(xhr.responseText);
      } catch {
        /* handled below */
      }
      if (xhr.status === 200 && body.results?.[0]) return resolve(body.results[0]);
      if (xhr.status === 401) onUnauthorized();
      reject(new ApiError(xhr.status, body));
    };
    xhr.send(form);
  });
}

const id = encodeURIComponent;

export const api = {
  config: () => request<PublicConfig>("GET", "/api/config"),
  me: () => request<Me>("GET", "/api/auth/me"),
  login: (username: string, password: string) => request<Me>("POST", "/api/auth/login", { username, password }),
  logout: () => request<void>("POST", "/api/auth/logout"),
  documents: () => request<{ documents: DocumentInfo[] }>("GET", "/api/documents"),
  deleteDocument: (docId: string) => request<void>("DELETE", `/api/documents/${id(docId)}`),
  chunk: (chunkId: number) => request<Chunk>("GET", `/api/chunks/${chunkId}`),
  newConversation: () => request<Conversation>("POST", "/api/conversations"),
  conversation: (convId: string) => request<Conversation>("GET", `/api/conversations/${id(convId)}`),
  ask: (convId: string, question: string, documentIds: string[] | null) =>
    request<Turn>(
      "POST",
      `/api/conversations/${id(convId)}/questions`,
      documentIds ? { question, document_ids: documentIds } : { question },
    ),
  feedback: (turnId: string, rating: "up" | "down", reason: string | null) =>
    request<{ turn_id: string; rating: string }>("PUT", `/api/turns/${id(turnId)}/feedback`, { rating, reason }),
  weekly: () => request<{ weeks: WeeklyMetric[] }>("GET", "/api/metrics/weekly?weeks=8"),
};
