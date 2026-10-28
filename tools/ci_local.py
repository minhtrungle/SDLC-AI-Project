"""Run the L0 quality gate locally — same steps as .github/workflows/ci.yml.

Usage: python tools/ci_local.py [--log docs/07-verification/ci-log.txt] [--skip-frontend]
Exit code is non-zero if any step fails. Every step runs even if an earlier one fails.
Frontend/E2E steps need Node >= 22.12 and `npm ci` in app/frontend and app/e2e (E2E uses the
installed Google Chrome locally; CI installs Playwright's Chromium).
"""

import pathlib
import shutil
import subprocess
import sys
import time

ROOT = pathlib.Path(__file__).resolve().parent.parent
BACKEND = ROOT / "app" / "backend"
FRONTEND = ROOT / "app" / "frontend"
E2E = ROOT / "app" / "e2e"
PY = sys.executable
NPM = shutil.which("npm") or "npm"

PYTHON_STEPS = [
    ("py-format", [PY, "-m", "ruff", "format", "--check", "."], ROOT),
    ("py-lint", [PY, "-m", "ruff", "check", "."], ROOT),
    ("py-compile", [PY, "-m", "compileall", "-q", "app/backend/cwd", "tools"], ROOT),
    ("secret-scan", [PY, "tools/secret_scan.py"], ROOT),
    (
        "py-dependency-audit",
        [PY, "-m", "pip_audit", "-r", "app/backend/requirements.txt", "--progress-spinner", "off"],
        ROOT,
    ),
    ("cross-view-audit", [PY, "tools/cross_view_audit.py"], ROOT),
    ("traceability", [PY, "tools/trace_matrix.py"], ROOT),
    ("backend-tests+coverage", [PY, "-m", "pytest", "-p", "no:cacheprovider"], BACKEND),
]
FRONTEND_STEPS = [
    ("fe-api-contract", [NPM, "run", "check:api"], FRONTEND),
    ("fe-lint", [NPM, "run", "lint"], FRONTEND),
    ("fe-type-check", [NPM, "run", "type-check"], FRONTEND),
    ("fe-tests+coverage", [NPM, "test"], FRONTEND),
    ("fe-build", [NPM, "run", "build"], FRONTEND),
    ("fe-dependency-audit", [NPM, "audit", "--audit-level=high"], FRONTEND),
    # Playwright E2E against the real backend serving the build above (raw output: test_reports/.raw).
    ("e2e-type-check", [NPM, "run", "type-check"], E2E),
    ("e2e-playwright", [NPM, "test"], E2E),
    # Screenshots + mp4 videos + report.md in test_reports/ from the run above.
    ("e2e-report", [PY, "tools/e2e_report.py"], ROOT),
]


def main():
    log_path = ROOT / sys.argv[sys.argv.index("--log") + 1] if "--log" in sys.argv else None
    steps = PYTHON_STEPS + ([] if "--skip-frontend" in sys.argv else FRONTEND_STEPS)
    lines, failed = [], []
    total = time.perf_counter()
    for name, cmd, cwd in steps:
        start = time.perf_counter()
        proc = subprocess.run(
            cmd, cwd=cwd, capture_output=True, text=True, encoding="utf-8", errors="replace", check=False
        )
        secs = time.perf_counter() - start
        status = "PASS" if proc.returncode == 0 else "FAIL"
        if status == "FAIL":
            failed.append(name)
        header = f"=== [{status}] {name} ({secs:.1f}s): {pathlib.Path(cmd[0]).stem} {' '.join(cmd[1:])}"
        print(header)
        lines.append(header)
        output = (proc.stdout + proc.stderr).strip()
        tail = "\n".join(output.splitlines()[-40:])
        if tail:
            lines.append(tail)
            if status == "FAIL":
                print(tail)
    summary = f"L0 gate: {len(steps) - len(failed)}/{len(steps)} passed in {time.perf_counter() - total:.1f}s"
    summary += f"; failed: {', '.join(failed)}" if failed else ""
    print(summary)
    lines.append(summary)
    if log_path:
        log_path.parent.mkdir(parents=True, exist_ok=True)
        log_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
