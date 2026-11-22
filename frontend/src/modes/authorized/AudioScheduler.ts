/** Contract stub for Authorized Media mode (ARCHITECTURE §3). NOT IMPLEMENTED in Phase 1. */
export const MODULE_ID = 'tubesomali:authorized:audio-scheduler';

export interface AudioSchedulerContract {
  readonly implemented: false;
}

export class AudioSchedulerStub implements AudioSchedulerContract {
  readonly implemented = false as const;
  notImplemented(): never {
    throw new Error('AudioScheduler: not implemented (later phase)');
  }
}
