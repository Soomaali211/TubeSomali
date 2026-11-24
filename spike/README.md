# Phase 1b spike harness (test tool, not the app)
Implements the tooling for `docs/DUAL_AUDIO_SPIKE_PLAN.md`. **No AT-SP test has been executed on a device.** Nothing here is evidence for G11 or G24.

- `index.html`, `app.js`: page with the planned graph (`video -> originalGain -> master`, `Somali -> somaliGain -> master`), Approach A (per-cue buffers) and Approach B (second media element with drift correction), 0-100 % controls with three transition methods, T1 event/sample logging and JSON export with the section-8 environment form.
- `lib/core.js`: pure helpers (gain mapping, cue scheduling, drift slope, click score, Goertzel tone detection, logger). Unit-tested in Node.
- `fixtures/generate.py`: synthetic tones, flash-frame video and format variants (needs ffmpeg). Output goes to `fixtures/out/` (git-ignored). Default is 1 minute; the plan wants >= 20 minutes for long-run drift: `--minutes 20`.
- Not built: Approach A' (time-stretch) and C (native), T2 recording analysis scripts, delivery to the phone.

## Run locally (desktop, for development only)
```
python3 spike/fixtures/generate.py --minutes 1
cd spike && python3 -m http.server 8080      # then open http://localhost:8080/ (localhost is a secure context)
```
## Run on the phone
Delivery is **undecided** (SPIKE_PLAN section 11, ADR-025 PROPOSED, Q13/Q16): USB forwarding needs a PC; the phone-only route needs a separate static harness published over HTTPS, which is **not created and not authorized**. Do not publish this folder without owner authorization.
