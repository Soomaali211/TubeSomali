import { so } from '../../locales/so.ts';
import { MODULE_ID as PLAYER } from './AuthorizedMediaPlayer.ts';
import { MODULE_ID as MIXER } from './AudioMixer.ts';
import { MODULE_ID as SCHED } from './AudioScheduler.ts';
import { MODULE_ID as SUBS } from './SubtitleRenderer.ts';
import { MODULE_ID as RIGHTS } from './MediaRights.ts';

/** Placeholder. Module ids are referenced so the bundle check can prove they live only in this chunk. */
export default function AuthorizedMode() {
  return (
    <section aria-labelledby="am-title" data-modules={[PLAYER, MIXER, SCHED, SUBS, RIGHTS].join(' ')}>
      <h2 id="am-title">{so.modeAuthorized}</h2>
      <p>{so.notImplemented}</p>
    </section>
  );
}
