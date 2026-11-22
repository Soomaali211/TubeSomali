import js from '@eslint/js';
import tseslint from 'typescript-eslint';

const audioAndAuthorized = [
  { group: ['**/modes/authorized/**', '**/authorized/**'], message: 'YouTube mode/core must not import Authorized Media code (ADR-013).' },
  { group: ['**/AudioMixer*', '**/AudioScheduler*', '**/SubtitleRenderer*', '**/MediaRights*', '**/AuthorizedMediaPlayer*', '**/tts/**'], message: 'Audio/TTS/subtitle-overlay modules are forbidden here (ADR-013).' },
];

export default tseslint.config(
  { ignores: ['dist', 'node_modules'] },
  js.configs.recommended,
  ...tseslint.configs.recommended,
  {
    files: ['src/modes/youtube/**/*.{ts,tsx}', 'src/core/**/*.{ts,tsx}'],
    rules: { 'no-restricted-imports': ['error', { patterns: audioAndAuthorized }] },
  },
);
