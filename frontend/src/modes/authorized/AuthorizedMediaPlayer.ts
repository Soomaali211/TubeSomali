/** Contract stub for Authorized Media mode (ARCHITECTURE §3). NOT IMPLEMENTED in Phase 1. */
export const MODULE_ID = 'tubesomali:authorized:authorized-media-player';

export interface AuthorizedMediaPlayerContract {
  readonly implemented: false;
}

export class AuthorizedMediaPlayerStub implements AuthorizedMediaPlayerContract {
  readonly implemented = false as const;
  notImplemented(): never {
    throw new Error('AuthorizedMediaPlayer: not implemented (later phase)');
  }
}
