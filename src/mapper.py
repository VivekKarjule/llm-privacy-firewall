"""
mapper.py - replaces sensitive spans with placeholders and remembers
which placeholder stands for which original value.

Key rule: the SAME entity always gets the SAME placeholder within a
session. If "John Doe" appears twice, both become [PERSON_1]. Otherwise
the LLM would think they are two different people.
"""
from src.detector import Span


class Mapper:
    def __init__(self):
        self.mapping: dict[str, str] = {}     # "[PERSON_1]" -> "John Doe"
        self._reverse: dict[tuple, str] = {}  # (label, normalised text) -> placeholder
        self._counters: dict[str, int] = {}   # label -> how many issued so far

    @staticmethod
    def _normalise(text: str) -> str:
        # "John Doe" and "john doe " should count as the same entity
        return " ".join(text.lower().split())

    def _placeholder_for(self, span: Span) -> str:
        key = (span.label, self._normalise(span.text))
        if key not in self._reverse:
            n = self._counters.get(span.label, 0) + 1
            self._counters[span.label] = n
            placeholder = f"[{span.label}_{n}]"
            self._reverse[key] = placeholder
            self.mapping[placeholder] = span.text   # keep first-seen spelling
        return self._reverse[key]

    def sanitize(self, text: str, spans: list[Span]) -> str:
        """Return text with every span replaced by its placeholder."""
        spans = sorted(spans, key=lambda s: s.start)
        # Number placeholders left-to-right so the output reads naturally
        placeholders = [self._placeholder_for(s) for s in spans]
        # Replace right-to-left so earlier character offsets stay valid
        out = text
        for s, ph in reversed(list(zip(spans, placeholders))):
            out = out[: s.start] + ph + out[s.end:]
        return out
