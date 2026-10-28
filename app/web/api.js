// HTTP client for the CWD API (docs/04-design/openapi.yaml).
let csrfToken = null;
let onUnauthorized = () => {};

export class ApiError extends Error {
  constructor(status, problem) {
    super(problem.title || "Đã có lỗi xảy ra.");
    this.status = status;
    this.code = problem.code || "internal";
  }
}

export function setCsrf(token) { csrfToken = token; }
export function setUnauthorizedHandler(fn) { onUnauthorized = fn; }

async function parse(res) {
  if (res.status === 204) return null;
  const body = await res.json().catch(() => ({ title: "Không đọc được phản hồi từ máy chủ." }));
  if (!res.ok) {
    if (res.status === 401 && body.code === "auth.required") onUnauthorized();
    throw new ApiError(res.status, body);
  }
  return body;
}

export async function request(method, path, body) {
  const headers = {};
  if (body !== undefined) headers["Content-Type"] = "application/json";
  if (method !== "GET" && csrfToken) headers["X-CSRF-Token"] = csrfToken;
  let res;
  try {
    res = await fetch(path, { method, headers, body: body === undefined ? undefined : JSON.stringify(body), credentials: "same-origin" });
  } catch {
    throw new ApiError(0, { code: "network", title: "Mất kết nối. Vui lòng kiểm tra mạng và thử lại." });
  }
  return parse(res);
}

// Upload one file with progress (AC-201.3). Resolves with the UploadResult for that file.
export function uploadFile(file, onProgress) {
  return new Promise((resolve, reject) => {
    const xhr = new XMLHttpRequest();
    const form = new FormData();
    form.append("files", file, file.name);
    xhr.open("POST", "/api/documents");
    if (csrfToken) xhr.setRequestHeader("X-CSRF-Token", csrfToken);
    xhr.upload.onprogress = (e) => { if (e.lengthComputable) onProgress(e.loaded / e.total); };
    xhr.onerror = () => reject(new ApiError(0, { code: "network", title: "Mất kết nối khi tải lên." }));
    xhr.onload = () => {
      let body = {};
      try { body = JSON.parse(xhr.responseText); } catch { /* handled below */ }
      if (xhr.status === 200) return resolve(body.results[0]);
      if (xhr.status === 401) onUnauthorized();
      reject(new ApiError(xhr.status, body));
    };
    xhr.send(form);
  });
}

export const api = {
  config: () => request("GET", "/api/config"),
  me: () => request("GET", "/api/auth/me"),
  login: (username, password) => request("POST", "/api/auth/login", { username, password }),
  logout: () => request("POST", "/api/auth/logout"),
  documents: () => request("GET", "/api/documents"),
  deleteDocument: (id) => request("DELETE", `/api/documents/${encodeURIComponent(id)}`),
  chunk: (id) => request("GET", `/api/chunks/${encodeURIComponent(id)}`),
  newConversation: () => request("POST", "/api/conversations"),
  conversation: (id) => request("GET", `/api/conversations/${encodeURIComponent(id)}`),
  ask: (id, question, documentIds) =>
    request("POST", `/api/conversations/${encodeURIComponent(id)}/questions`,
      documentIds ? { question, document_ids: documentIds } : { question }),
  feedback: (turnId, rating, reason) => request("PUT", `/api/turns/${encodeURIComponent(turnId)}/feedback`, { rating, reason: reason || null }),
  weekly: () => request("GET", "/api/metrics/weekly?weeks=8"),
};
