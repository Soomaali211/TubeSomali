"""AST/static checks that need no web framework (AT-YT-09 skeleton: research never wired in)."""

import ast
from pathlib import Path

APP = Path(__file__).resolve().parents[1] / "app"


def _imports(path: Path) -> list[str]:
    out: list[str] = []
    for n in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
        if isinstance(n, ast.Import):
            out += [a.name for a in n.names]
        elif isinstance(n, ast.ImportFrom) and n.module:
            out.append(n.module)
    return out


def test_nothing_outside_research_imports_research() -> None:
    offenders = [
        str(p.relative_to(APP))
        for p in APP.rglob("*.py")
        if "research" not in p.relative_to(APP).parts
        and any(i == "app.research" or i.startswith("app.research.") for i in _imports(p))
    ]
    assert offenders == []


def test_research_package_is_empty_skeleton() -> None:
    mods = [p.name for p in (APP / "research").glob("*.py")]
    assert mods == ["__init__.py"]


def test_no_asr_or_media_download_imports_in_app() -> None:
    banned = {
        "whisper",
        "faster_whisper",
        "vosk",
        "speech_recognition",
        "yt_dlp",
        "youtube_transcript_api",
    }
    seen = {i.split(".")[0] for p in APP.rglob("*.py") for i in _imports(p)}
    assert not (seen & banned)
