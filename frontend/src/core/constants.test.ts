import assert from 'node:assert/strict';
import { test } from 'node:test';
import { APP_PHASE, YOUTUBE_MODE_AUDIO_ALLOWED } from './constants.ts';
import { isModeId, MODE_IDS } from './modes.ts';

test('YOUTUBE_MODE_AUDIO_ALLOWED is false (AT-YT-04 skeleton)', () => {
  assert.equal(YOUTUBE_MODE_AUDIO_ALLOWED, false);
});

test('there are exactly two hard-separated modes', () => {
  assert.deepEqual([...MODE_IDS], ['youtube', 'authorized']);
  assert.equal(isModeId('youtube'), true);
  assert.equal(isModeId('both'), false);
});

test('scaffold reports phase 1', () => {
  assert.equal(APP_PHASE, 1);
});
