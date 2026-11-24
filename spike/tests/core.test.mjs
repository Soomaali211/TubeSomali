import assert from 'node:assert/strict';
import { test } from 'node:test';
import {
  TONE_A_HZ, TONE_B_HZ, clickScore, cueSchedule, driftSlope, goertzelPower, makeLogger, offsetMs, peakDbfs, percentToGain,
} from '../lib/core.js';

test('percentToGain maps 0..100 linearly and clamps', () => {
  assert.equal(percentToGain(0), 0);
  assert.equal(percentToGain(50), 0.5);
  assert.equal(percentToGain(100), 1);
  assert.equal(percentToGain(150), 1);
  assert.equal(percentToGain(-5), 0);
  assert.equal(percentToGain(50, 'perceptual'), 0.25);
  assert.throws(() => percentToGain('abc'), RangeError);
});

test('cueSchedule skips past cues, offsets in-progress cues, scales future by rate', () => {
  const cues = [{ id: 'a', start: 1, dur: 1 }, { id: 'b', start: 4, dur: 1 }, { id: 'c', start: 8, dur: 2 }];
  const s = cueSchedule(cues, 4.5, 1);
  assert.deepEqual(s.map((c) => c.id), ['b', 'c']);
  assert.equal(s[0].whenSec, 0);
  assert.equal(s[0].offsetSec, 0.5);
  assert.equal(s[1].whenSec, 3.5);
  assert.equal(cueSchedule(cues, 4.5, 2)[1].whenSec, 1.75);
  assert.deepEqual(cueSchedule(cues, 100, 1), []);
  assert.throws(() => cueSchedule(cues, 0, 0), RangeError);
});

test('offsetMs sign: positive when audio is ahead', () => {
  assert.ok(offsetMs(10, 10.05) > 49 && offsetMs(10, 10.05) < 51);
  assert.ok(offsetMs(10, 9.95) < 0);
});

test('driftSlope recovers a known slope and rejects degenerate input', () => {
  const series = [0, 10, 20, 30].map((t) => ({ t, offsetMs: 5 + 0.2 * t }));
  const r = driftSlope(series);
  assert.ok(Math.abs(r.slopeMsPerSec - 0.2) < 1e-9);
  assert.equal(r.n, 4);
  assert.equal(driftSlope([{ t: 1, offsetMs: 1 }]), null);
  assert.equal(driftSlope([{ t: 1, offsetMs: 1 }, { t: 1, offsetMs: 2 }]), null);
});

function sine(freq, sr, n, amp = 0.5) {
  return Float32Array.from({ length: n }, (_, i) => amp * Math.sin((2 * Math.PI * freq * i) / sr));
}

test('clickScore: smooth tone is low, an injected step is high', () => {
  const sr = 48000;
  const smooth = sine(440, sr, 4096);
  const stepped = smooth.slice();
  for (let i = 2048; i < stepped.length; i++) stepped[i] += 0.4;
  const a = clickScore(smooth, 2048);
  const b = clickScore(stepped, 2048);
  assert.ok(a < 2, `smooth score ${a}`);
  assert.ok(b > 10, `step score ${b}`);
});

test('goertzel finds the marker tone and distinguishes A from B', () => {
  const sr = 48000;
  const toneB = sine(TONE_B_HZ, sr, 4800);
  const pB = goertzelPower(toneB, sr, TONE_B_HZ);
  const pA = goertzelPower(toneB, sr, TONE_A_HZ);
  assert.ok(pB > 100 * pA, `B at B=${pB}, B at A=${pA}`);
});

test('peakDbfs', () => {
  assert.equal(peakDbfs([0, 0]), -Infinity);
  assert.ok(Math.abs(peakDbfs([0.5, -1]) - 0) < 1e-9);
  assert.ok(Math.abs(peakDbfs([0.5]) - -6.0206) < 1e-3);
});

test('logger is append-only, deterministic and labels the measurement tier', () => {
  let t = 0;
  const log = makeLogger(() => (t += 10));
  log.log('play', { videoT: 1 });
  log.log('pause');
  const ev = log.events();
  assert.deepEqual(ev.map((e) => [e.i, e.t, e.type]), [[0, 10, 'play'], [1, 20, 'pause']]);
  ev.pop();
  assert.equal(log.events().length, 2);
  const x = log.export({ device: 'unrecorded' });
  assert.equal(x.schema, 'tubesomali-spike-v0');
  assert.match(x.measurementTier, /software-level only/);
});
