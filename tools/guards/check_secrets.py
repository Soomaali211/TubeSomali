#!/usr/bin/env python3
"""Guard (AT-SEC-05 scaffold level): fail on likely committed secrets. Heuristic pattern scan of
text files; it is NOT a replacement for a dedicated scanner (limitation recorded).
Usage: check_secrets.py [--root DIR]   exit 0 = clean, 1 = findings."""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

SKIP_DIRS = {".git", "node_modules", "dist", "__pycache__", ".venv", ".mypy_cache", ".ruff_cache"}
PATTERNS = {
    "private key block": re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    "GitHub token": re.compile(r"\bgh[pousr]_[A-Za-z0-9]{30,}\b"),
    "AWS access key id": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "API-style secret": re.compile(r"\bsk-[A-Za-z0-9]{24,}\b"),
    "assigned secret literal": re.compile(
        r"""(?i)\b(?:api[_-]?key|secret|token|password)\b\s*[:=]\s*['"][A-Za-z0-9/+_\-]{20,}['"]"""
    ),
}
ALLOW_FILES = {".env.example"}  # placeholders only; checked separately for non-placeholder values


def scan(root: Path) -> list[str]:
    out: list[str] = []
    for p in root.rglob("*"):
        if not p.is_file() or any(part in SKIP_DIRS for part in p.parts):
            continue
        if p.suffix in {".png", ".jpg", ".ico", ".woff", ".woff2", ".zip", ".lock"}:
            continue
        try:
            text = p.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for name, rx in PATTERNS.items():
            if rx.search(text):
                out.append(f"{p.relative_to(root)}: possible {name}")
    env_example = root / ".env.example"
    if env_example.is_file():
        for ln in env_example.read_text(encoding="utf-8").splitlines():
            if "=" in ln and not ln.lstrip().startswith("#"):
                key, _, val = ln.partition("=")
                if re.search(r"(?i)(secret|token|key|password)", key) and val.strip() not in (
                    "", "CHANGE_ME", "<placeholder>"
                ):
                    out.append(f".env.example: non-placeholder value for {key.strip()}")
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=str(Path(__file__).resolve().parents[2]))
    findings = scan(Path(ap.parse_args().root))
    for f in findings:
        print("FAIL:", f)
    print("secrets guard:", "FAIL" if findings else "PASS")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
