"""CMP-02 API Gateway — application factory, middleware, routing, static files."""

import json
import logging
import time
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app import auth, documents
from app.config import Settings
from app.db import init_schema
from app.errors import install_handlers
from app.ingestion import recover_pending
from app.security import LoginLimiter

WEB_DIR = Path(__file__).with_name("web")
access_log = logging.getLogger("cwd.access")

SECURITY_HEADERS = {
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "Referrer-Policy": "no-referrer",
    "Content-Security-Policy": "default-src 'self'; img-src 'self' data:; frame-ancestors 'none'",
}


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
    app.state.login_limiter = LoginLimiter()
    install_handlers(app)
    app.include_router(auth.router)
    app.include_router(documents.router)

    @app.middleware("http")
    async def headers_and_access_log(request: Request, call_next):
        start = time.perf_counter()
        response = await call_next(request)
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
            "ai_mode": "local",
            "max_file_mb": settings.max_file_mb,
            "max_docs": settings.max_docs,
            "max_question_chars": settings.max_question_chars,
        }

    @app.get("/", include_in_schema=False)
    def index():
        return FileResponse(WEB_DIR / "index.html")

    app.mount("/static", StaticFiles(directory=WEB_DIR), name="static")
    return app


def __getattr__(name):
    # `uvicorn app.main:app` — build the app lazily so importing this module has no side effects.
    if name == "app":
        return create_app()
    raise AttributeError(name)
