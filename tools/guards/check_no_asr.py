#!/usr/bin/env python3
"""Guard (AT-CAP-13 scaffold level): fail if an ASR / speech-recognition / transcription package
appears in dependency manifests or imports in application source. Manifest + source scan only; it
cannot see transitive dependencies (limitation, recorded in docs/PHASE1_REPORT.md).
Usage: check_no_asr.py [--root DIR]   exit 0 = clean, 1 = violation."""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

FORBIDDEN = [
    "whisper", "faster-whisper", "openai-whisper", "whisper-cpp", "vosk", "speechrecognition",
    "speech_recognition", "deepspeech", "pocketsphinx", "wav2vec", "assemblyai", "deepgram",
    "google-cloud-speech", "azure-cognitiveservices-speech", "amazon-transcribe",
    "transformers.js", "whisper-web", "nemo_toolkit", "stt",
]
# "stt" only matches as a whole token in manifests (see below) to avoid false positives.
MANIFESTS = ("requirements*.txt", "pyproject.toml", "package.json", "Pipfile")
SRC_DIRS = (("backend/app", "*.py"), ("frontend/src", "*.ts"), ("frontend/src", "*.tsx"))


def _tokens_in(text: str) -> set[str]:
    return {t.lower() for t in re.findall(r"[A-Za-z0-9_.\-]+", text)}


def scan(root: Path) -> list[str]:
    findings: list[str] = []
    forb = {f.lower() for f in FORBIDDEN}
    for pattern in MANIFESTS:
        for p in root.rglob(pattern):
            if any(part in ("node_modules", ".git") for part in p.parts):
                continue
            toks = _tokens_in(p.read_text(encoding="utf-8", errors="replace"))
            for hit in sorted(toks & forb):
                findings.append(f"{p.relative_to(root)}: forbidden ASR dependency '{hit}'")
    for sub, glob in SRC_DIRS:
        base = root / sub
        if not base.is_dir():
            continue
        for p in base.rglob(glob):
            text = p.read_text(encoding="utf-8", errors="replace")
            for m in re.finditer(r"^\s*(?:from|import)\s+['\"]?([A-Za-z0-9_.\-@/]+)", text, re.M):
                if m.group(1).split(".")[0].lower() in forb:
                    findings.append(f"{p.relative_to(root)}: imports ASR module '{m.group(1)}'")
    return findings


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=str(Path(__file__).resolve().parents[2]))
    args = ap.parse_args()
    findings = scan(Path(args.root))
    for f in findings:
        print("FAIL:", f)
    print("no-ASR guard:", "FAIL" if findings else "PASS")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
