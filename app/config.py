"""CMP-13 Configuration — environment variables CWD_* (SAD §8.5)."""

import os
from dataclasses import dataclass, field
from pathlib import Path

TRUE_VALUES = {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class Settings:
    data_dir: Path = Path("data")
    max_file_mb: int = 20
    max_docs: int = 50
    max_question_chars: int = 2000
    min_relevance: float = 0.6
    top_k: int = 6
    per_doc_limit: int = 2
    session_idle_hours: float = 8
    allow_external_ai: bool = False
    anthropic_api_key: str | None = field(default=None, repr=False)
    anthropic_model: str = "claude-sonnet-5-5"
    answer_timeout_s: float = 15
    cookie_secure: bool = False

    @property
    def db_path(self) -> Path:
        return self.data_dir / "cwd.db"

    @property
    def files_dir(self) -> Path:
        return self.data_dir / "files"

    @property
    def max_file_bytes(self) -> int:
        return self.max_file_mb * 1024 * 1024

    @classmethod
    def from_env(cls, env=None) -> "Settings":
        env = os.environ if env is None else env

        def get(name, cast, default):
            raw = env.get(name)
            return default if raw is None or raw == "" else cast(raw)

        def as_bool(raw):
            return raw.strip().lower() in TRUE_VALUES

        d = cls()
        return cls(
            data_dir=get("CWD_DATA_DIR", Path, d.data_dir),
            max_file_mb=get("CWD_MAX_FILE_MB", int, d.max_file_mb),
            max_docs=get("CWD_MAX_DOCS", int, d.max_docs),
            max_question_chars=get("CWD_MAX_QUESTION_CHARS", int, d.max_question_chars),
            min_relevance=get("CWD_MIN_RELEVANCE", float, d.min_relevance),
            top_k=get("CWD_TOP_K", int, d.top_k),
            per_doc_limit=get("CWD_PER_DOC_LIMIT", int, d.per_doc_limit),
            session_idle_hours=get("CWD_SESSION_IDLE_HOURS", float, d.session_idle_hours),
            allow_external_ai=get("CWD_ALLOW_EXTERNAL_AI", as_bool, d.allow_external_ai),
            anthropic_api_key=get("ANTHROPIC_API_KEY", str, None),
            anthropic_model=get("CWD_ANTHROPIC_MODEL", str, d.anthropic_model),
            answer_timeout_s=get("CWD_ANSWER_TIMEOUT_S", float, d.answer_timeout_s),
            cookie_secure=get("CWD_COOKIE_SECURE", as_bool, d.cookie_secure),
        )
