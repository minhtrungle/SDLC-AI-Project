"""CMP-02 API Gateway — application factory, middleware, routing, static files."""

import json
import logging
import time
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles

from cwd import auth, chat, documents, metrics
from cwd.config import Settings
from cwd.db import init_schema
from cwd.errors import install_handlers, log_unhandled, problem
from cwd.generation import build_generator
from cwd.ingestion import recover_pending
from cwd.security import LoginLimiter

access_log = logging.getLogger("cwd.access")

SECURITY_HEADERS = {
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "Referrer-Policy": "no-referrer",
    "Content-Security-Policy": "default-src 'self'; img-src 'self' data:; frame-ancestors 'none'",
}


class _BodyTooLarge(Exception):
    pass


class BodyLimitMiddleware:
    """Reject oversized request bodies with 413 before they are parsed or spooled (CR-04).

    Checks Content-Length up front and also counts streamed bytes, so chunked uploads are bounded too.
    """

    JSON_LIMIT = 64 * 1024

    def __init__(self, app, settings: Settings):
        self.app = app
        self.upload_limit = settings.max_file_bytes * documents.MAX_FILES_PER_REQUEST + 1024 * 1024

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http" or scope["method"] not in {"POST", "PUT", "PATCH"}:
            return await self.app(scope, receive, send)
        limit = self.upload_limit if scope["path"] == "/api/documents" else self.JSON_LIMIT
        declared = dict(scope["headers"]).get(b"content-length")
        if declared is not None and declared.isdigit() and int(declared) > limit:
            return await self._reject(scope, receive, send)
        seen, exceeded, replaced = 0, False, False

        async def counting_receive():
            nonlocal seen, exceeded
            message = await receive()
            seen += len(message.get("body", b""))
            if seen > limit:
                exceeded = True
                raise _BodyTooLarge  # stop parsing; FastAPI may turn this into its own error response
            return message

        async def guarded_send(message):
            nonlocal replaced
            if not exceeded:
                return await send(message)
            if not replaced:  # swap whatever error the app produced for a single 413
                replaced = True
                await self._reject(scope, receive, send)

        try:
            await self.app(scope, counting_receive, guarded_send)
        except _BodyTooLarge:
            if not replaced:
                await self._reject(scope, receive, send)

    @staticmethod
    async def _reject(scope, receive, send):
        response = problem(413, "request.too_large")
        response.headers.update(SECURITY_HEADERS)
        await response(scope, receive, send)


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or Settings.from_env()

    @asynccontextmanager
    async def lifespan(_: FastAPI):
        init_schema(settings)
        recover_pending(settings)
        yield

    app = FastAPI(
        title="Chat với tài liệu",
        lifespan=lifespan,
        docs_url=None,
        redoc_url=None,
        openapi_url=None,
    )
    app.state.settings = settings
    app.add_middleware(BodyLimitMiddleware, settings=settings)
    app.state.login_limiter = LoginLimiter()
    app.state.generator = build_generator(settings)
    install_handlers(app)
    app.include_router(auth.router)
    app.include_router(documents.router)
    app.include_router(chat.router)
    app.include_router(metrics.router)

    @app.middleware("http")
    async def headers_and_access_log(request: Request, call_next):
        start = time.perf_counter()
        try:
            response = await call_next(request)
        except Exception as exc:  # noqa: BLE001 — keep headers + access log on 500s too (CR-06)
            log_unhandled(request, exc)
            response = problem(500, "internal")
        response.headers.update(SECURITY_HEADERS)
        # NFR-008: metadata only — never bodies, query strings or cookies.
        access_log.info(
            json.dumps(
                {
                    "method": request.method,
                    "path": request.url.path,
                    "status": response.status_code,
                    "latency_ms": round((time.perf_counter() - start) * 1000),
                }
            )
        )
        return response

    @app.get("/api/health")
    def health():
        return {"status": "ok"}

    @app.get("/api/config")
    def get_config():
        return {
            "ai_mode": app.state.generator.mode,
            "max_file_mb": settings.max_file_mb,
            "max_docs": settings.max_docs,
            "max_question_chars": settings.max_question_chars,
        }

    mount_frontend(app, settings.frontend_dist)
    return app


NOT_BUILT_PAGE = """<!doctype html><html lang="vi"><meta charset="utf-8"><title>Chat với tài liệu</title>
<body><h1>Chat với tài liệu</h1><p>Giao diện chưa được build. Chạy <code>npm run build</code> trong
<code>frontend/</code>, hoặc dùng <code>npm run dev</code> khi phát triển.</p></body></html>"""


def mount_frontend(app: FastAPI, dist: Path) -> None:
    """Serve the Vue build (frontend/dist) at /, assets under /assets (ADR-009)."""
    index_html = dist / "index.html"

    @app.get("/", include_in_schema=False)
    def index():
        if index_html.is_file():
            return FileResponse(index_html)
        return HTMLResponse(NOT_BUILT_PAGE)

    if (dist / "assets").is_dir():
        app.mount("/assets", StaticFiles(directory=dist / "assets"), name="assets")


def __getattr__(name):
    # `uvicorn cwd.main:app` — build the app lazily so importing this module has no side effects.
    if name == "app":
        return create_app()
    raise AttributeError(name)
