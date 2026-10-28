"""Problem+json errors (RFC 9457) with stable codes and Vietnamese titles (SAD §8.2)."""

import logging

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

log = logging.getLogger("cwd.error")

MESSAGES = {
    "auth.invalid_credentials": "Tên đăng nhập hoặc mật khẩu không đúng.",
    "auth.required": "Bạn cần đăng nhập để tiếp tục.",
    "auth.too_many_attempts": "Bạn đã nhập sai quá nhiều lần. Vui lòng thử lại sau 5 phút.",
    "auth.forbidden": "Bạn không có quyền thực hiện thao tác này.",
    "csrf.invalid": "Phiên làm việc không hợp lệ. Vui lòng tải lại trang.",
    "not_found": "Không tìm thấy dữ liệu yêu cầu.",
    "file.wrong_type": "Sai định dạng, chỉ chấp nhận PDF.",
    "file.too_large": "Tệp vượt dung lượng cho phép.",
    "docs.limit_reached": "Đã đạt số lượng tài liệu tối đa của workspace.",
    "chat.invalid_question": "Câu hỏi phải có từ 1 đến 2000 ký tự.",
    "chat.no_ready_documents": "Chưa có tài liệu nào sẵn sàng để hỏi.",
    "chat.ai_unavailable": "Dịch vụ trả lời đang gặp sự cố. Vui lòng thử lại.",
    "feedback.invalid": "Đánh giá không hợp lệ.",
    "validation.error": "Dữ liệu gửi lên không hợp lệ.",
    "internal": "Đã có lỗi xảy ra. Vui lòng thử lại sau.",
}


class ProblemError(Exception):
    def __init__(self, status: int, code: str, detail: str | None = None):
        super().__init__(code)
        self.status = status
        self.code = code
        self.detail = detail


def problem(status: int, code: str, detail: str | None = None) -> JSONResponse:
    body = {"type": "about:blank", "title": MESSAGES[code], "status": status, "code": code}
    if detail:
        body["detail"] = detail
    return JSONResponse(body, status_code=status, media_type="application/problem+json")


def install_handlers(app: FastAPI) -> None:
    @app.exception_handler(ProblemError)
    async def _problem(_: Request, exc: ProblemError):
        return problem(exc.status, exc.code, exc.detail)

    @app.exception_handler(RequestValidationError)
    async def _validation(_: Request, exc: RequestValidationError):
        fields = ", ".join(".".join(str(p) for p in e["loc"][1:]) for e in exc.errors())
        return problem(422, "validation.error", f"Trường không hợp lệ: {fields}" if fields else None)

    @app.exception_handler(StarletteHTTPException)
    async def _http(_: Request, exc: StarletteHTTPException):
        if exc.status_code == 404:
            return problem(404, "not_found")
        if exc.status_code == 405:
            return problem(405, "validation.error", "Phương thức không được hỗ trợ.")
        return problem(exc.status_code, "internal")

    @app.exception_handler(Exception)
    async def _unexpected(request: Request, exc: Exception):
        log.error("unhandled error on %s %s: %s", request.method, request.url.path, type(exc).__name__)
        return problem(500, "internal")
