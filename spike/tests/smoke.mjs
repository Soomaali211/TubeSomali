// LOCAL software smoke test of the spike page in headless Chromium. NOT an AT-SP execution and NOT device evidence.
import { createRequire } from 'node:module';
import { createServer } from 'node:http';
import { readFileSync, existsSync } from 'node:fs';
import { extname, join, normalize, resolve } from 'node:path';

// playwright is a sandbox/CI-provided dependency, not declared in this repo; resolved via require so NODE_PATH works.
const { chromium } = createRequire(import.meta.url)('playwright');

const root = resolve(import.meta.dirname, '..');
const types = { '.html': 'text/html', '.js': 'text/javascript', '.json': 'application/json', '.wav': 'audio/wav', '.mp4': 'video/mp4', '.webm': 'video/webm' };
const server = createServer((req, res) => {
  const p = normalize(decodeURIComponent(new URL(req.url, 'http://x').pathname));
  const f = join(root, p === '/' ? 'index.html' : p);
  if (!f.startsWith(root) || !existsSync(f)) { res.writeHead(404).end(); return; }
  const buf = readFileSync(f);
  const m = /bytes=(\d+)-(\d*)/.exec(req.headers.range || '');
  if (m) { const s = +m[1]; const e = m[2] ? +m[2] : buf.length - 1; res.writeHead(206, { 'content-type': types[extname(f)] || 'application/octet-stream', 'content-range': `bytes ${s}-${e}/${buf.length}`, 'accept-ranges': 'bytes' }).end(buf.subarray(s, e + 1)); return; }
  res.writeHead(200, { 'content-type': types[extname(f)] || 'application/octet-stream', 'accept-ranges': 'bytes' }).end(buf);
});
await new Promise((r) => server.listen(0, '127.0.0.1', r));
const port = server.address().port;
const results = [];
const check = (name, ok, info = '') => { results.push({ name, ok }); console.log(`${ok ? 'PASS' : 'FAIL'}: ${name} ${info}`); };

const browser = await chromium.launch({ args: ['--autoplay-policy=no-user-gesture-required'] });
for (const ap of ['B', 'A']) {
  const page = await browser.newPage();
  page.on('pageerror', (e) => console.log('pageerror', e.message));
  page.on('console', (m) => { if (m.type() === 'error') console.log('console.error', m.text()); });
  await page.goto(`http://127.0.0.1:${port}/index.html`);
  await page.fill('#fx', 'fixtures/out');
  await page.selectOption('#vfile', 'fx-vid.mp4');
  await page.selectOption('#approach', ap);
  await page.click('#start');
  try {
    await page.waitForFunction(() => window.__spike && window.__spike.logger.events().some((e) => e.type === 'ready'), null, { timeout: 20000 });
  } catch (e) {
    console.log(`FAIL: [${ap}] page never became ready; state text =`, await page.textContent('#state'));
    process.exit(1);
  }
  const st = await page.evaluate(() => ({ state: window.__spike.ctx.state, sr: window.__spike.ctx.sampleRate }));
  check(`[${ap}] audio context created and running`, st.state === 'running', JSON.stringify(st));
  await page.evaluate(() => { document.getElementById('g-som').value = '30'; document.getElementById('g-som').dispatchEvent(new Event('input')); document.getElementById('g-orig').value = '0'; document.getElementById('g-orig').dispatchEvent(new Event('input')); });
  const g = await page.evaluate(() => ({ som: window.__spike.nodes.som.gain.value, orig: window.__spike.nodes.orig.gain.value, master: window.__spike.nodes.master.gain.value }));
  check(`[${ap}] independent gains applied (som 0.3, orig 0, master 1)`, Math.abs(g.som - 0.3) < 1e-6 && g.orig === 0 && g.master === 1, JSON.stringify(g));
  await page.evaluate(() => window.__spike.v.play());
  await page.waitForTimeout(2500);
  const mid = await page.evaluate(() => ({ t: window.__spike.v.currentTime, live: window.__spike.live.length, sched: window.__spike.stats.scheduled, aT: window.__spike.a.currentTime, paused: window.__spike.v.paused }));
  check(`[${ap}] video advanced while playing`, mid.t > 1.0 && !mid.paused, JSON.stringify(mid));
  if (ap === 'A') check('[A] cues scheduled', mid.sched > 0, `scheduled=${mid.sched}`);
  else check('[B] audio element tracks video within 0.25 s', Math.abs(mid.aT - mid.t) < 0.25, `|a-v|=${Math.abs(mid.aT - mid.t).toFixed(3)}`);
  await page.evaluate(() => window.__spike.v.pause());
  await page.waitForTimeout(300);
  const after = await page.evaluate(() => ({ live: window.__spike.live.length, cancelled: window.__spike.stats.cancelled, apaused: window.__spike.a.paused }));
  check(`[${ap}] pause cancels/pauses Somali audio`, ap === 'A' ? after.live === 0 : after.apaused, JSON.stringify(after));
  const ev = await page.evaluate(() => window.__spike.logger.events().map((e) => e.type));
  check(`[${ap}] event log has play, pause and samples`, ['play', 'pause', 'sample'].every((t) => ev.includes(t)));
  await page.close();
}
await browser.close();
server.close();
const failed = results.filter((r) => !r.ok).length;
console.log(`smoke: ${results.length - failed}/${results.length} passed`);
process.exit(failed ? 1 : 0);
