"""Typed contracts for later phases (ARCHITECTURE §3). NO behavior: every method raises."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


class NotImplementedInPhase(NotImplementedError):
    """Raised by every stub; the feature belongs to a later phase."""


@dataclass(frozen=True)
class Segment:
    id: str
    source_start: float
    source_end: float
    source_text: str
    translated_text: str | None = None


class CaptionProvider(ABC):  # Phase 3
    """Supplies caption text from a lawful source. Never receives or returns audio (no ASR)."""

    @abstractmethod
    def get_segments(self, source_ref: str) -> list[Segment]:
        raise NotImplementedInPhase("Phase 3")


class TranslationPipeline(ABC):  # Phase 4 — blocked until G24 passes with owner approval
    @abstractmethod
    def translate(self, segments: list[Segment]) -> list[Segment]:
        raise NotImplementedInPhase("Phase 4")


class TTSAdapter(ABC):  # Phase 5 — blocked until G24 passes with owner approval
    @abstractmethod
    def synthesize(self, text: str, voice_id: str) -> bytes:
        raise NotImplementedInPhase("Phase 5")
