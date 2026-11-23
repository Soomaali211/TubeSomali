import { cleanup, fireEvent, render, screen } from '@testing-library/react';
import { afterEach, describe, expect, it } from 'vitest';
import App from '../src/app/App.tsx';
import { so } from '../src/locales/so.ts';

describe('App shell (Phase 1)', () => {
  afterEach(cleanup);

  it('shows the Somali home with two mode cards', () => {
    render(<App />);
    expect(screen.getByText(so.homeTitle)).toBeTruthy();
    expect(screen.getByRole('button', { name: new RegExp(so.modeYoutube) })).toBeTruthy();
    expect(screen.getByRole('button', { name: new RegExp(so.modeAuthorized) })).toBeTruthy();
  });

  it('YouTube mode shows the no-audio note and embeds no player or audio element', async () => {
    const { container } = render(<App />);
    fireEvent.click(screen.getByRole('button', { name: new RegExp(so.modeYoutube) }));
    expect(await screen.findByText(so.youtubeNoAudio)).toBeTruthy();
    expect(container.querySelector('iframe, audio, video, input[type=range]')).toBeNull();
  });

  it('Authorized mode shows an explicit not-implemented placeholder', async () => {
    render(<App />);
    fireEvent.click(screen.getByRole('button', { name: new RegExp(so.modeAuthorized) }));
    expect(await screen.findByText(so.notImplemented)).toBeTruthy();
  });
});
