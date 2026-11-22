export type ModeId = 'youtube' | 'authorized';

export const MODE_IDS: readonly ModeId[] = ['youtube', 'authorized'] as const;

export function isModeId(value: string): value is ModeId {
  return (MODE_IDS as readonly string[]).includes(value);
}
