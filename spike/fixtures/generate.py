"""Generate synthetic Phase 1b fixtures (FX-VID, FX-SOM-CUES, FX-SOM-TRACK, FX-LEVEL, FX-FMT).

Only generated tones and test patterns: no personal or third-party media, no network, no models.
Requires ffmpeg/ffprobe on PATH for the video fixtures. Output is git-ignored.
Usage: python3 generate.py [--out DIR] [--minutes 1.0] [--sr 48000]
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import shutil
import struct
import subprocess
import wave
from pathlib import Path

TONE_A_HZ = 1000.0  # original-audio marker, aligned to flash frames
TONE_B_HZ = 1600.0  # Somali stand-in marker
FLASH_PERIOD = 2.0  # seconds between flash frames / tone-A beeps
FLASH_LEN = 0.10
BEEP_LEN = 0.15
CUE_DURS = (0.4, 0.8, 1.2, 0.6)
CUE_SPACING = 5.0


def _tone(freq: float, dur: float, sr: int, amp: float = 0.5, fade: float = 0.005) -> list[float]:
    n = int(dur * sr)
    f = max(1, int(fade * sr))
    out = []
    for i in range(n):
        env = min(1.0, i / f, (n - 1 - i) / f)
        out.append(amp * env * math.sin(2 * math.pi * freq * i / sr))
    return out


def _write_wav(path: Path, samples: list[float], sr: int) -> None:
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes(
            b"".join(struct.pack("<h", int(max(-1.0, min(1.0, s)) * 32767)) for s in samples)
        )


def _place(total: float, sr: int, bursts: list[tuple[float, list[float]]]) -> list[float]:
    buf = [0.0] * int(total * sr)
    for start, data in bursts:
        i0 = int(start * sr)
        for k, v in enumerate(data):
            if i0 + k < len(buf):
                buf[i0 + k] += v
    return buf


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True, capture_output=True)


def _encoders() -> str:
    return subprocess.run(
        ["ffmpeg", "-hide_banner", "-encoders"], capture_output=True, text=True, check=True
    ).stdout


def generate(out: Path, minutes: float, sr: int) -> dict:
    total = max(6.0, minutes * 60.0)
    out.mkdir(parents=True, exist_ok=True)
    (out / "cues").mkdir(exist_ok=True)
    manifest: dict = {
        "schema": "tubesomali-spike-fixtures-v0",
        "durationSec": total,
        "sampleRate": sr,
        "files": {},
    }

    # FX-VID audio: tone A beeps aligned to flash frames
    beeps = [(t, _tone(TONE_A_HZ, BEEP_LEN, sr)) for t in _times(0.0, FLASH_PERIOD, total - 1)]
    a_wav = out / "fx-orig-audio.wav"
    _write_wav(a_wav, _place(total, sr, beeps), sr)

    # FX-SOM-CUES + FX-SOM-TRACK: identical content, two shapes
    cues, bursts = [], []
    for i, start in enumerate(_times(1.0, CUE_SPACING, total - 2)):
        dur = CUE_DURS[i % len(CUE_DURS)]
        f = out / "cues" / f"cue_{i:03d}.wav"
        data = _tone(TONE_B_HZ, dur, sr)
        _write_wav(f, data, sr)
        cues.append({"id": f"cue_{i:03d}", "start": start, "dur": dur, "file": f"cues/{f.name}"})
        bursts.append((start, data))
    (out / "cues.json").write_text(json.dumps({"cues": cues}, indent=2))
    track = out / "fx-som-track.wav"
    _write_wav(track, _place(total, sr, bursts), sr)

    # FX-LEVEL: calibration tones at known dBFS
    levels = [-20.0, -12.0, -6.0, -3.0, -1.0, -0.1]
    lv, t0, spec = [], 0.0, []
    for db in levels:
        amp = 10 ** (db / 20)
        spec.append({"dbfs": db, "start": t0, "dur": 1.0})
        lv.append((t0, _tone(1000.0, 1.0, sr, amp=amp)))
        t0 += 1.5
    lev = out / "fx-level.wav"
    _write_wav(lev, _place(t0, sr, lv), sr)
    (out / "fx-level.json").write_text(json.dumps({"tones": spec}, indent=2))

    # FX-VID / FX-FMT (needs ffmpeg)
    if shutil.which("ffmpeg") is None:
        manifest["video"] = "SKIPPED: ffmpeg not found"
    else:
        enc = _encoders()
        flash = f"drawbox=x=0:y=0:w=iw:h=ih:color=white@1:t=fill:enable='lt(mod(t\\,{FLASH_PERIOD})\\,{FLASH_LEN})'"
        src = [
            "-f",
            "lavfi",
            "-i",
            f"testsrc2=size=640x360:rate=30:duration={total}",
            "-i",
            str(a_wav),
        ]
        vf = ["-vf", flash, "-shortest"]
        formats = {}
        if "libx264" in enc and "aac" in enc:
            _run(
                [
                    "ffmpeg",
                    "-y",
                    *src,
                    *vf,
                    "-c:v",
                    "libx264",
                    "-pix_fmt",
                    "yuv420p",
                    "-c:a",
                    "aac",
                    str(out / "fx-vid.mp4"),
                ]
            )
            formats["mp4_h264_aac"] = "fx-vid.mp4"
        if "libvpx-vp9" in enc and "libopus" in enc:
            _run(
                [
                    "ffmpeg",
                    "-y",
                    *src,
                    *vf,
                    "-c:v",
                    "libvpx-vp9",
                    "-b:v",
                    "500k",
                    "-deadline",
                    "realtime",
                    "-c:a",
                    "libopus",
                    str(out / "fx-vid.webm"),
                ]
            )
            formats["webm_vp9_opus"] = "fx-vid.webm"
        manifest["video"] = formats or "SKIPPED: no usable encoders"

    for p in sorted(out.rglob("*")):
        if p.is_file() and p.name != "manifest.json":
            manifest["files"][str(p.relative_to(out))] = {
                "sha256": _sha(p),
                "bytes": p.stat().st_size,
            }
    manifest["cueCount"] = len(cues)
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2))
    return manifest


def _times(start: float, step: float, stop: float) -> list[float]:
    out, t = [], start
    while t < stop:
        out.append(round(t, 3))
        t += step
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", default=str(Path(__file__).parent / "out"))
    ap.add_argument(
        "--minutes",
        type=float,
        default=1.0,
        help="fixture length; the plan wants >= 20 for long-run drift",
    )
    ap.add_argument("--sr", type=int, default=48000)
    a = ap.parse_args()
    m = generate(Path(a.out), a.minutes, a.sr)
    print(f"generated {len(m['files'])} files, cues={m['cueCount']}, video={m['video']}")


if __name__ == "__main__":
    main()
