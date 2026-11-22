#!/usr/bin/env node
// Guard (AT-YT-03/04 scaffold level): YouTube mode and core must not import audio/TTS/authorized code.
// Usage: node check_boundaries.mjs [--root DIR]   exit 0 = clean, 1 = violation.
import { readdirSync, readFileSync, statSync, existsSync } from 'node:fs';
import { join, relative, resolve } from 'node:path';

const args = process.argv.slice(2);
const root = resolve(args.includes('--root') ? args[args.indexOf('--root') + 1] : new URL('../../', import.meta.url).pathname);
const FORBIDDEN_IMPORT = /(modes\/authorized|AudioMixer|AudioScheduler|SubtitleRenderer|MediaRights|AuthorizedMediaPlayer|\/tts|TTS)/;
const FORBIDDEN_API = /\b(AudioContext|webkitAudioContext|createMediaElementSource|SpeechSynthesis|speechSynthesis)\b/;

function walk(dir) {
  if (!existsSync(dir)) return [];
  return readdirSync(dir).flatMap((n) => {
    const p = join(dir, n);
    return statSync(p).isDirectory() ? walk(p) : /\.(ts|tsx|mjs|js)$/.test(n) ? [p] : [];
  });
}
const findings = [];
for (const sub of ['frontend/src/modes/youtube', 'frontend/src/core']) {
  for (const f of walk(join(root, sub))) {
    const text = readFileSync(f, 'utf8');
    if (/\.test\.[tj]s$/.test(f)) continue;
    for (const m of text.matchAll(/^\s*(?:import|export)\s[^;]*?from\s+['"]([^'"]+)['"]/gm)) {
      if (FORBIDDEN_IMPORT.test(m[1])) findings.push(`${relative(root, f)}: forbidden import '${m[1]}'`);
    }
    if (FORBIDDEN_API.test(text.replace(/\/\/.*$/gm, '').replace(/\/\*[\s\S]*?\*\//g, ''))) {
      findings.push(`${relative(root, f)}: forbidden audio API use`);
    }
  }
}
findings.forEach((f) => console.log('FAIL:', f));
console.log('boundary guard:', findings.length ? 'FAIL' : 'PASS');
process.exit(findings.length ? 1 : 0);
