// Pure helpers for the Phase 1b dual-audio spike. No DOM, no Web Audio: testable in Node.
// Nothing here is a measurement of a device. These are the formulas the page and offline analysis use.

export const TONE_A_HZ = 1000; // original-audio marker (FX-VID)
export const TONE_B_HZ = 1600; // Somali stand-in marker (FX-SOM-*)

/** Map a 0-100 % control to a linear gain. 'perceptual' (squared) is optional per AT-SP-02; neither is recommended here. */
export function percentToGain(percent, curve = 'linear') {
  const p = Math.min(100, Math.max(0, Number(percent))) / 100;
  if (Number.isNaN(p)) throw new RangeError('percent must be a number');
  return curve === 'perceptual' ? p * p : p;
}

/**
 * Approach A scheduling: which cues to (re)start from media time t at playback rate `rate`.
 * Cues are {id,start,dur} in media seconds. A cue already in progress starts now with an offset into the buffer.
 * Per-buffer playbackRate changes pitch (F18); the spike only reports this, it does not fix it (that is A').
 */
export function cueSchedule(cues, t, rate = 1) {
  if (!(rate > 0)) throw new RangeError('rate must be > 0');
  const out = [];
  for (const c of cues) {
    const end = c.start + c.dur;
    if (end <= t) continue;
    if (c.start <= t) out.push({ id: c.id, whenSec: 0, offsetSec: t - c.start });
    else out.push({ id: c.id, whenSec: (c.start - t) / rate, offsetSec: 0 });
  }
  return out;
}

/** Signed offset in ms: positive means the audio clock is ahead of the video clock. */
export function offsetMs(videoTimeSec, audioTimeSec) {
  return (audioTimeSec - videoTimeSec) * 1000;
}

/** Least-squares slope of offset vs time, in ms per second of media time. Needs >= 2 points with distinct t. */
export function driftSlope(series) {
  const n = series.length;
  if (n < 2) return null;
  const mt = series.reduce((s, p) => s + p.t, 0) / n;
  const mo = series.reduce((s, p) => s + p.offsetMs, 0) / n;
  let num = 0;
  let den = 0;
  for (const p of series) {
    num += (p.t - mt) * (p.offsetMs - mo);
    den += (p.t - mt) ** 2;
  }
  return den === 0 ? null : { slopeMsPerSec: num / den, n };
}

/**
 * Click score around index `center` of a sampled waveform: max |first difference| in the window divided by the
 * median |first difference| in the same window. A smooth signal scores near 1; a step scores far higher.
 * The threshold is NOT defined here: it must be proposed from real recordings (SPIKE_PLAN section 6).
 */
export function clickScore(samples, center, halfWindow = 256) {
  const lo = Math.max(1, center - halfWindow);
  const hi = Math.min(samples.length - 1, center + halfWindow);
  const d = [];
  for (let i = lo; i <= hi; i++) d.push(Math.abs(samples[i] - samples[i - 1]));
  if (d.length === 0) return null;
  const sorted = [...d].sort((a, b) => a - b);
  const median = sorted[Math.floor(sorted.length / 2)];
  const max = sorted[sorted.length - 1];
  return median === 0 ? (max === 0 ? 1 : Infinity) : max / median;
}

/** Goertzel power of `freq` in `samples` (offline analysis of recordings, tier T2). */
export function goertzelPower(samples, sampleRate, freq) {
  const w = (2 * Math.PI * freq) / sampleRate;
  const coeff = 2 * Math.cos(w);
  let s1 = 0;
  let s2 = 0;
  for (let i = 0; i < samples.length; i++) {
    const s0 = samples[i] + coeff * s1 - s2;
    s2 = s1;
    s1 = s0;
  }
  return (s1 * s1 + s2 * s2 - coeff * s1 * s2) / samples.length;
}

/** Peak in dBFS of a sample array in [-1, 1]; -Infinity for silence. */
export function peakDbfs(samples) {
  let m = 0;
  for (const v of samples) m = Math.max(m, Math.abs(v));
  return m === 0 ? -Infinity : 20 * Math.log10(m);
}

/** Append-only event log with a monotonic index. `now` is injected so tests are deterministic. */
export function makeLogger(now) {
  const events = [];
  return {
    log(type, data = {}) {
      events.push({ i: events.length, t: now(), type, ...data });
    },
    events: () => events.slice(),
    export(env) {
      return {
        schema: 'tubesomali-spike-v0',
        measurementTier: 'T1 software-level only (not acoustic sync, not real Bluetooth latency)',
        env,
        events: events.slice(),
      };
    },
  };
}
