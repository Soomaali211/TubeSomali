// Phase 1b spike page. Graph: video -> MediaElementSource -> originalGain -> master -> destination;
// Somali source -> somaliGain -> master. Approach A: per-cue buffers. Approach B: second media element.
// Logs T1 data only. No network except same-origin fixture fetches. Nothing is stored or sent anywhere.
import { cueSchedule, makeLogger, offsetMs, percentToGain } from './lib/core.js';

const $ = (id) => document.getElementById(id);
const v = $('v');
const a = $('a');
const logger = makeLogger(() => Math.round(performance.now() * 100) / 100);
let ctx = null;
let nodes = null;
let cues = [];
let buffers = new Map();
let live = []; // {src, id} currently scheduled (approach A)
let approach = 'B';
let sampler = null;
const stats = { scheduled: 0, cancelled: 0, driftCorrections: 0 };

function show() {
  const ev = logger.events().slice(-12).map((e) => JSON.stringify(e)).join('\n');
  $('log').textContent = ev || '(log)';
}
function log(type, data) { logger.log(type, data); show(); }

function gainValue(id) { return percentToGain($(id).value, $('curve').value); }

function setGain(param, value) {
  const now = ctx.currentTime;
  const tc = Math.max(0.001, Number($('tc').value) || 0.02);
  const m = $('method').value;
  if (m === 'target') { param.cancelScheduledValues(now); param.setTargetAtTime(value, now, tc); }
  else if (m === 'ramp') { param.cancelScheduledValues(now); param.setValueAtTime(param.value, now); param.linearRampToValueAtTime(value, now + tc); }
  else { param.cancelScheduledValues(now); param.value = value; }
}
function applyGains() {
  if (!nodes) return;
  setGain(nodes.orig.gain, gainValue('g-orig'));
  setGain(nodes.som.gain, gainValue('g-som'));
  setGain(nodes.master.gain, gainValue('g-master'));
  log('gain', { orig: $('g-orig').value, som: $('g-som').value, master: $('g-master').value, method: $('method').value, curve: $('curve').value });
}

async function load(base) {
  const vf = $('vfile').value;
  v.src = `${base}/${vf}`;
  cues = (await (await fetch(`${base}/cues.json`)).json()).cues;
  if (approach === 'B') a.src = `${base}/fx-som-track.wav`;
  else {
    buffers = new Map();
    for (const c of cues) {
      const ab = await (await fetch(`${base}/${c.file}`)).arrayBuffer();
      buffers.set(c.id, await ctx.decodeAudioData(ab));
    }
  }
  // metadata may already have loaded while cues were being fetched/decoded: check readyState first
  if (v.readyState < 1) await new Promise((res, rej) => { v.onloadedmetadata = res; v.onerror = () => rej(new Error('video load failed')); });
}

function buildGraph() {
  ctx = new AudioContext();
  const master = ctx.createGain();
  const orig = ctx.createGain();
  const som = ctx.createGain();
  ctx.createMediaElementSource(v).connect(orig);
  orig.connect(master); som.connect(master); master.connect(ctx.destination);
  if (approach === 'B') ctx.createMediaElementSource(a).connect(som);
  nodes = { master, orig, som };
}

// Approach A
function cancelAll(reason) {
  for (const l of live) { try { l.src.stop(); } catch { /* already stopped */ } }
  if (live.length) { stats.cancelled += live.length; log('cancel', { reason, n: live.length }); }
  live = [];
}
function scheduleFrom(t) {
  const rate = v.playbackRate;
  for (const s of cueSchedule(cues, t, rate)) {
    const src = ctx.createBufferSource();
    src.buffer = buffers.get(s.id);
    src.playbackRate.value = rate; // pitch shifts at rate != 1 (F18): reported, not corrected
    src.connect(nodes.som);
    src.start(ctx.currentTime + s.whenSec, s.offsetSec);
    live.push({ src, id: s.id });
    stats.scheduled += 1;
  }
}

// Approach B sync controller
function syncB(reason) {
  a.playbackRate = v.playbackRate;
  const d = Math.abs(a.currentTime - v.currentTime);
  if (reason !== 'tick' || d > 0.05) {
    a.currentTime = v.currentTime;
    if (reason === 'tick') stats.driftCorrections += 1;
    log('syncB', { reason, driftBeforeMs: Math.round(d * 1000) });
  }
}

function onPlay() {
  if (approach === 'A') { cancelAll('play'); scheduleFrom(v.currentTime); }
  else { syncB('play'); a.play().catch((e) => log('audioPlayError', { msg: String(e) })); }
}
function onStop(reason) {
  if (approach === 'A') cancelAll(reason); else { a.pause(); syncB(reason); }
}
function onSeeked() {
  if (approach === 'A') { cancelAll('seek'); if (!v.paused) scheduleFrom(v.currentTime); }
  else { syncB('seeked'); if (!v.paused) a.play().catch(() => {}); }
}
function onRate() {
  log('ratechange', { rate: v.playbackRate });
  if (approach === 'A') { cancelAll('rate'); if (!v.paused) scheduleFrom(v.currentTime); } else syncB('rate');
}

function startSampler() {
  clearInterval(sampler);
  sampler = setInterval(() => {
    const row = {
      videoT: v.currentTime, ctxT: ctx.currentTime, ctxState: ctx.state, paused: v.paused,
      baseLatency: ctx.baseLatency, outputLatency: ctx.outputLatency, // estimates; may be undefined on Android [U]
    };
    if (approach === 'B') { row.audioT = a.currentTime; row.offsetMs = offsetMs(v.currentTime, a.currentTime); if (!v.paused) syncB('tick'); }
    log('sample', row);
  }, 500);
}

$('start').addEventListener('click', async () => {
  try {
    approach = $('approach').value;
    if (!ctx) buildGraph();
    await ctx.resume();
    await load($('fx').value.replace(/\/$/, ''));
    applyGains();
    for (const e of ['seeking', 'waiting', 'stalled', 'ended']) v.addEventListener(e, () => log(e, { videoT: v.currentTime }));
    v.addEventListener('play', () => { log('play', { videoT: v.currentTime }); onPlay(); });
    v.addEventListener('pause', () => { log('pause', { videoT: v.currentTime }); onStop('pause'); });
    v.addEventListener('seeking', () => { onStop('seeking'); });
    v.addEventListener('seeked', () => { log('seeked', { videoT: v.currentTime }); onSeeked(); });
    v.addEventListener('ratechange', onRate);
    document.addEventListener('visibilitychange', () => log('visibility', { state: document.visibilityState, ctxState: ctx.state }));
    document.addEventListener('fullscreenchange', () => log('fullscreen', { on: Boolean(document.fullscreenElement) }));
    startSampler();
    $('state').textContent = `ready (approach ${approach}, ctx ${ctx.state})`;
    window.__spike = { ctx, nodes, stats, logger, get live() { return live; }, v, a, applyGains };
    log('ready', { approach, ctxState: ctx.state, sampleRate: ctx.sampleRate });
  } catch (err) {
    $('state').textContent = `error: ${err.message}`;
    log('error', { msg: String(err) });
  }
});

for (const id of ['g-orig', 'g-som', 'g-master']) $(id).addEventListener('input', applyGains);
$('play').addEventListener('click', () => v.play());
$('pause').addEventListener('click', () => v.pause());
$('back10').addEventListener('click', () => { v.currentTime = Math.max(0, v.currentTime - 10); });
$('fwd10').addEventListener('click', () => { v.currentTime = Math.min(v.duration, v.currentTime + 10); });
$('rnd').addEventListener('click', () => { v.currentTime = Math.random() * v.duration; });
$('rate').addEventListener('change', () => { v.playbackRate = Number($('rate').value); });
$('fs').addEventListener('click', () => { const s = $('stage'); document.fullscreenElement ? document.exitFullscreen() : s.requestFullscreen(); });
$('export').addEventListener('click', () => {
  const env = Object.fromEntries(['tester', 'device', 'android', 'browser', 'route', 'power', 'tiers', 'notes'].map((k) => [k, $(`e-${k}`).value]));
  env.userAgent = navigator.userAgent;
  env.approach = approach;
  env.commit = new URLSearchParams(location.search).get('commit') || 'unrecorded';
  env.stats = stats;
  const blob = new Blob([JSON.stringify(logger.export(env), null, 2)], { type: 'application/json' });
  const el = document.createElement('a');
  el.href = URL.createObjectURL(blob);
  el.download = `spike-${approach}-${Date.now()}.json`;
  el.click();
});
