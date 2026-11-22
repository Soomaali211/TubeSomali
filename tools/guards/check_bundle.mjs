#!/usr/bin/env node
// Guard (AT-YT-03 scaffold level): after `vite build`, the YouTube chunk must not contain Authorized
// module ids, and those ids must appear ONLY in the authorized chunk. Fails if chunks are missing
// (never passes vacuously). Usage: node check_bundle.mjs [--dist DIR]
import { existsSync, readdirSync, readFileSync } from 'node:fs';
import { join, resolve } from 'node:path';

const a = process.argv.slice(2);
const dist = resolve(a.includes('--dist') ? a[a.indexOf('--dist') + 1] : 'dist');
const assets = join(dist, 'assets');
const MARK = 'tubesomali:authorized:';
const fail = (m) => { console.log('FAIL:', m); console.log('bundle guard: FAIL'); process.exit(1); };

if (!existsSync(assets)) fail(`no build output at ${assets} (run the build first)`);
const js = readdirSync(assets).filter((f) => f.endsWith('.js'));
const yt = js.filter((f) => f.startsWith('mode-youtube'));
const am = js.filter((f) => f.startsWith('mode-authorized'));
if (yt.length !== 1) fail(`expected exactly 1 mode-youtube chunk, found ${yt.length}`);
if (am.length !== 1) fail(`expected exactly 1 mode-authorized chunk, found ${am.length}`);
for (const f of js) {
  const has = readFileSync(join(assets, f), 'utf8').includes(MARK);
  if (f === am[0] && !has) fail('authorized chunk lacks its module ids (check is not meaningful)');
  if (f !== am[0] && has) fail(`authorized module ids leaked into ${f}`);
}
console.log('bundle guard: PASS');
