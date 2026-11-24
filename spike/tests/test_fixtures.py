"""Fixture generator tests. With REQUIRE_FFMPEG=1 a missing ffmpeg FAILS instead of skipping (CI)."""

import json
import os
import shutil
import subprocess
import sys
import wave
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "fixtures"))
import generate

HAS_FFMPEG = shutil.which("ffmpeg") and shutil.which("ffprobe")


@pytest.fixture(scope="module")
def out(tmp_path_factory):
    d = tmp_path_factory.mktemp("fx")
    if not HAS_FFMPEG and os.environ.get("REQUIRE_FFMPEG") == "1":
        pytest.fail("ffmpeg/ffprobe required but missing")
    generate.generate(d, minutes=0.1, sr=48000)
    return d


def test_audio_fixtures_have_expected_shape(out):
    m = json.loads((out / "manifest.json").read_text())
    assert m["sampleRate"] == 48000 and m["durationSec"] == 6.0
    with wave.open(str(out / "fx-som-track.wav")) as w:
        assert w.getframerate() == 48000 and w.getnchannels() == 1
        assert abs(w.getnframes() / 48000 - 6.0) < 0.01
    cues = json.loads((out / "cues.json").read_text())["cues"]
    assert len(cues) >= 1 and m["cueCount"] == len(cues)
    for c in cues:
        assert (out / c["file"]).exists() and c["start"] >= 1.0
    lv = json.loads((out / "fx-level.json").read_text())["tones"]
    assert [t["dbfs"] for t in lv] == sorted(t["dbfs"] for t in lv)


def test_level_fixture_peak_matches_spec(out):
    import struct

    with wave.open(str(out / "fx-level.wav")) as w:
        raw = w.readframes(w.getnframes())
    vals = struct.unpack("<" + "h" * (len(raw) // 2), raw)
    peak = max(abs(v) for v in vals) / 32767
    assert abs(20 * __import__("math").log10(peak) - -0.1) < 0.05


def test_manifest_hashes_match(out):
    m = json.loads((out / "manifest.json").read_text())
    for rel, info in m["files"].items():
        assert generate._sha(out / rel) == info["sha256"]


@pytest.mark.skipif(not HAS_FFMPEG, reason="ffmpeg not installed here (CI sets REQUIRE_FFMPEG=1)")
def test_video_fixture_has_video_and_audio_streams(out):
    m = json.loads((out / "manifest.json").read_text())
    assert isinstance(m["video"], dict) and "mp4_h264_aac" in m["video"]
    r = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "stream=codec_type,codec_name,duration",
            "-of",
            "json",
            str(out / "fx-vid.mp4"),
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    streams = {s["codec_type"]: s for s in json.loads(r.stdout)["streams"]}
    assert streams["video"]["codec_name"] == "h264" and streams["audio"]["codec_name"] == "aac"
    assert abs(float(streams["video"]["duration"]) - 6.0) < 0.5
