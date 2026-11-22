/** Contract stub for Authorized Media mode (ARCHITECTURE §3). NOT IMPLEMENTED in Phase 1. */
export const MODULE_ID = 'tubesomali:authorized:subtitle-renderer';

export interface SubtitleRendererContract {
  readonly implemented: false;
}

export class SubtitleRendererStub implements SubtitleRendererContract {
  readonly implemented = false as const;
  notImplemented(): never {
    throw new Error('SubtitleRenderer: not implemented (later phase)');
  }
}
