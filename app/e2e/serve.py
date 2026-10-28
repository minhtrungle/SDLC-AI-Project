"""Start the backend for Playwright: fresh data dir, seeded users, PDF fixtures, built frontend.

Usage (Playwright webServer): python serve.py --port 8799
Requires app/frontend/dist (run `npm run build` in app/frontend first).
"""

import argparse
import os
import pathlib
import shutil
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
BACKEND = HERE.parent / "backend"
DIST = HERE.parent / "frontend" / "dist"
DATA = HERE / ".data"
PASSWORD = "e2e-pass-123"  # secret-scan: allow (throwaway test account)
# One account per spec file so scenarios never see each other's documents.
USERS = [
    ("auth_user", "user"),
    ("doc_user", "user"),
    ("chat_user", "user"),
    ("iso_a", "user"),
    ("iso_b", "user"),
    ("dash_user", "user"),
    ("hung", "manager"),
]


def make_fixtures(target: pathlib.Path) -> None:
    """Text PDFs built from the backend's synthetic corpus (same generator the backend tests use)."""
    sys.path.insert(0, str(BACKEND))
    from tests import corpus  # noqa: PLC0415
    from tests.conftest import make_pdf  # noqa: PLC0415

    target.mkdir(parents=True, exist_ok=True)
    (target / "HopDong_Alpha.pdf").write_bytes(make_pdf(corpus.ALPHA))
    (target / "DuAn_Beta.pdf").write_bytes(make_pdf(corpus.BETA))
    (target / "BangGia_2026.pdf").write_bytes(make_pdf(corpus.PRICING))
    (target / "ghi-chu.docx").write_bytes(b"PK\x03\x04 not a pdf")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8799)
    args = parser.parse_args()
    if not (DIST / "index.html").exists():
        print("app/frontend/dist is missing: run `npm run build` in app/frontend first.", file=sys.stderr)
        return 1
    shutil.rmtree(DATA, ignore_errors=True)
    env = {**os.environ, "CWD_DATA_DIR": str(DATA / "db"), "CWD_FRONTEND_DIST": str(DIST)}
    for username, role in USERS:
        subprocess.run(
            [
                sys.executable,
                "-m",
                "cwd.cli",
                "create-user",
                "--username",
                username,
                "--role",
                role,
                "--password",
                PASSWORD,
            ],
            cwd=BACKEND,
            env=env,
            check=True,
            stdout=subprocess.DEVNULL,
        )
    make_fixtures(DATA / "pdfs")
    # Run uvicorn in this process (os.exec* on Windows spawns a new process and exits, which
    # Playwright would read as "server died"). Playwright stops this process after the run.
    os.environ.update(env)
    os.chdir(BACKEND)
    import uvicorn  # noqa: PLC0415

    uvicorn.run("cwd.main:app", host="127.0.0.1", port=args.port, log_level="warning")
    return 0


if __name__ == "__main__":
    sys.exit(main())
