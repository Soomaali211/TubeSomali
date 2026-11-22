import { so } from '../../locales/so.ts';

/** Placeholder. No player is embedded in Phase 1 and there are no audio controls (G1). */
export default function YouTubeMode() {
  return (
    <section aria-labelledby="yt-title">
      <h2 id="yt-title">{so.modeYoutube}</h2>
      <p>{so.youtubeNoAudio}</p>
      <p>{so.notImplemented}</p>
    </section>
  );
}
