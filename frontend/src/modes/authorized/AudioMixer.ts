/** Contract stub for Authorized Media mode (ARCHITECTURE §3). NOT IMPLEMENTED in Phase 1. */
export const MODULE_ID = 'tubesomali:authorized:audio-mixer';

export interface AudioMixerContract {
  readonly implemented: false;
}

export class AudioMixerStub implements AudioMixerContract {
  readonly implemented = false as const;
  notImplemented(): never {
    throw new Error('AudioMixer: not implemented (later phase)');
  }
}
