/** Contract stub for the OFFICIAL YouTube IFrame player (ARCHITECTURE §3). NOT IMPLEMENTED (Phase 7).
 *  Must never: mute/alter volume for dubbing, draw in front of the player, load TTS, touch media. */
export interface YouTubePlayerAdapterContract {
  readonly implemented: false;
}

export class YouTubePlayerAdapterStub implements YouTubePlayerAdapterContract {
  readonly implemented = false as const;
  notImplemented(): never {
    throw new Error('YouTubePlayerAdapter: not implemented (Phase 7)');
  }
}
