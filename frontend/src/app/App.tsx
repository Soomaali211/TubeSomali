import { Suspense, lazy, useState } from 'react';
import type { ModeId } from '../core/modes.ts';
import { so } from '../locales/so.ts';

const YouTubeMode = lazy(() => import('../modes/youtube/YouTubeMode.tsx'));
const AuthorizedMode = lazy(() => import('../modes/authorized/AuthorizedMode.tsx'));

export default function App() {
  const [mode, setMode] = useState<ModeId | null>(null);

  if (mode === null) {
    return (
      <main>
        <h1>{so.appName}</h1>
        <h2>{so.homeTitle}</h2>
        <button type="button" onClick={() => setMode('youtube')}>
          {so.modeYoutube}
          <small>{so.modeYoutubeHint}</small>
        </button>
        <button type="button" onClick={() => setMode('authorized')}>
          {so.modeAuthorized}
          <small>{so.modeAuthorizedHint}</small>
        </button>
      </main>
    );
  }
  return (
    <main>
      <button type="button" onClick={() => setMode(null)}>
        {so.back}
      </button>
      <Suspense fallback={null}>{mode === 'youtube' ? <YouTubeMode /> : <AuthorizedMode />}</Suspense>
    </main>
  );
}
