"""Run the L0 quality gate locally — same steps as .github/workflows/ci.yml.

Usage: python tools/ci_local.py [--log docs/07-verification/ci-log.txt]
Exit code is non-zero if any step fails. Every step runs even if an earlier one fails.
"""

import pathlib
import subprocess
import sys
import time

ROOT = pathlib.Path(__file__).resolve().parent.parent
PY = sys.executable

STEPS = [
    ("format", [PY, "-m", "ruff", "format", "--check", "."]),
    ("lint", [PY, "-m", "ruff", "check", "."]),
    ("compile", [PY, "-m", "compileall", "-q", "app", "tools"]),
    ("secret-scan", [PY, "tools/secret_scan.py"]),
    ("dependency-audit", [PY, "-m", "pip_audit", "-r", "requirements.txt", "--progress-spinner", "off"]),
    ("cross-view-audit", [PY, "tools/cross_view_audit.py"]),
    ("traceability", [PY, "tools/trace_matrix.py"]),
    (
        "tests+coverage",
        [PY, "-m", "pytest", "-p", "no:cacheprovider", "--junitxml=docs/07-verification/junit.xml"],
    ),
]


def main():
    log_path = None
    if "--log" in sys.argv:
        log_path = ROOT / sys.argv[sys.argv.index("--log") + 1]
    lines, failed = [], []
    total = time.perf_counter()
    for name, cmd in STEPS:
        start = time.perf_counter()
        proc = subprocess.run(
            cmd, cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace", check=False
        )
        secs = time.perf_counter() - start
        status = "PASS" if proc.returncode == 0 else "FAIL"
        if status == "FAIL":
            failed.append(name)
        header = f"=== [{status}] {name} ({secs:.1f}s): {' '.join(cmd[1:])}"
        print(header)
        lines.append(header)
        output = (proc.stdout + proc.stderr).strip()
        tail = "\n".join(output.splitlines()[-40:])
        if tail:
            lines.append(tail)
            if status == "FAIL":
                print(tail)
    summary = f"L0 gate: {len(STEPS) - len(failed)}/{len(STEPS)} passed in {time.perf_counter() - total:.1f}s"
    summary += f"; failed: {', '.join(failed)}" if failed else ""
    print(summary)
    lines.append(summary)
    if log_path:
        log_path.parent.mkdir(parents=True, exist_ok=True)
        log_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
