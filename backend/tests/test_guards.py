"""Each guard must PASS on the clean tree and FAIL on a deliberate violation (plan W6/W7)."""

import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
G = ROOT / "tools" / "guards"


def run_py(script: str, root: Path) -> int:
    return subprocess.run(
        [sys.executable, "-I", str(G / script), "--root", str(root)],
        capture_output=True,
        text=True,
        check=False,
    ).returncode


def test_no_asr_clean_tree() -> None:
    assert run_py("check_no_asr.py", ROOT) == 0


def test_no_asr_fails_on_manifest_violation(tmp_path: Path) -> None:
    (tmp_path / "backend").mkdir()
    (tmp_path / "backend" / "requirements.txt").write_text("fastapi\nopenai-whisper\n")
    assert run_py("check_no_asr.py", tmp_path) == 1


def test_no_asr_fails_on_import_violation(tmp_path: Path) -> None:
    d = tmp_path / "backend" / "app"
    d.mkdir(parents=True)
    (d / "x.py").write_text("import vosk\n")
    assert run_py("check_no_asr.py", tmp_path) == 1


def test_secrets_clean_tree() -> None:
    assert run_py("check_secrets.py", ROOT) == 0


@pytest.mark.parametrize(
    "content",
    [
        "-----BEGIN "
        + "RSA PRIVATE KEY-----\n",  # built from fragments so this file is not flagged
        "API_" + 'KEY = "' + 'abcdefghijklmnopqrstuvwxyz123456"\n',
    ],
)
def test_secrets_fails_on_violation(tmp_path: Path, content: str) -> None:
    (tmp_path / "a.txt").write_text(content)
    assert run_py("check_secrets.py", tmp_path) == 1


def test_secrets_flags_non_placeholder_env_example(tmp_path: Path) -> None:
    (tmp_path / ".env.example").write_text("TUBESOMALI_SOME_TOKEN=realvalue123\n")
    assert run_py("check_secrets.py", tmp_path) == 1
