"""L0 secret scan: fail if tracked files contain likely credentials.

Usage: python tools/secret_scan.py   (scans files tracked by git)
"""

import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

PATTERNS = {
    "Anthropic key": re.compile(r"sk-ant-[A-Za-z0-9_\-]{20,}"),
    "OpenAI-style key": re.compile(r"\bsk-[A-Za-z0-9]{32,}\b"),
    "AWS access key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "GitHub token": re.compile(r"\bgh[pousr]_[A-Za-z0-9]{36,}\b"),
    "Private key": re.compile(r"-----BEGIN (RSA |EC |OPENSSH |)PRIVATE KEY-----"),
    "Password assignment": re.compile(
        r"(?i)\b(password|passwd|secret|api_key)\s*=\s*['\"][^'\"\s]{12,}['\"]"
    ),
}
SKIP_SUFFIXES = {".png", ".jpg", ".xlsx", ".docx", ".pdf", ".ico"}
ALLOW_MARKER = "secret-scan: allow"


def tracked_files():
    out = subprocess.run(
        ["git", "ls-files", "-co", "--exclude-standard"], cwd=ROOT, capture_output=True, text=True, check=True
    ).stdout
    return [ROOT / p for p in out.splitlines() if p and (ROOT / p).is_file()]


def main():
    findings = []
    for path in tracked_files():
        if path.suffix.lower() in SKIP_SUFFIXES:
            continue
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except UnicodeDecodeError:
            continue
        for n, line in enumerate(lines, 1):
            if ALLOW_MARKER in line:
                continue
            for name, rx in PATTERNS.items():
                if rx.search(line):
                    findings.append(f"{path.relative_to(ROOT)}:{n}: {name}")
    for f in findings:
        print(f)
    print(f"secret scan: {len(findings)} finding(s)")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
