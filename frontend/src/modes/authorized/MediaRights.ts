/** Contract stub for Authorized Media mode (ARCHITECTURE §3). NOT IMPLEMENTED in Phase 1. */
export const MODULE_ID = 'tubesomali:authorized:media-rights';

export interface MediaRightsContract {
  readonly implemented: false;
}

export class MediaRightsStub implements MediaRightsContract {
  readonly implemented = false as const;
  notImplemented(): never {
    throw new Error('MediaRights: not implemented (later phase)');
  }
}
