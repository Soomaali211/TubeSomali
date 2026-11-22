// Each guard must pass on the clean tree and FAIL on a deliberate violation (plan W6).
import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { mkdirSync, mkdtempSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join, resolve } from 'node:path';
import { test } from 'node:test';

const guard = resolve(import.meta.dirname, '../../tools/guards/check_boundaries.mjs');
const run = (root) => spawnSync('node', [guard, '--root', root], { encoding: 'utf8' }).status;

test('boundary guard passes on the clean tree', () => {
  assert.equal(run(resolve(import.meta.dirname, '../..')), 0);
});

function tree(file, content) {
  const root = mkdtempSync(join(tmpdir(), 'bg-'));
  const dir = join(root, 'frontend/src', file.dir);
  mkdirSync(dir, { recursive: true });
  writeFileSync(join(dir, file.name), content);
  return root;
}

test('fails when YouTube mode imports Authorized code', () => {
  assert.equal(run(tree({ dir: 'modes/youtube', name: 'x.ts' }, "import { a } from '../authorized/AudioMixer.ts';\n")), 1);
});
test('fails when YouTube mode uses AudioContext', () => {
  assert.equal(run(tree({ dir: 'modes/youtube', name: 'x.ts' }, 'const c = new AudioContext();\n')), 1);
});
test('fails when core imports TTS', () => {
  assert.equal(run(tree({ dir: 'core', name: 'x.ts' }, "import { t } from '../tts/voice.ts';\n")), 1);
});
