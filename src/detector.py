"""
detector.py - finds sensitive spans in text.

Three detection strategies (we compare them in Stage 3 evaluation):
  1. detect_regex   - rules for structured data (SSN, email, phone ...)
  2. detect_spacy   - statistical NER for names, places, organisations
  3. detect_hybrid  - both combined, overlaps resolved

A "span" is just: where a sensitive piece of text starts and ends.
"""
import re
from dataclasses import dataclass


@dataclass(frozen=True)
class Span:
    start: int      # index of first character
    end: int        # index AFTER last character (Python slice style)
    label: str      # e.g. "PERSON", "SSN"
    text: str       # the original text, text[start:end]
    source: str     # "regex" or "spacy"  (useful when debugging)


# ---------- Layer A: regex rules ----------
# (?<!\d) and (?!\d) mean "not glued to other digits", which stops us
# from matching 10 digits in the middle of a longer number.
REGEX_PATTERNS = {
    "SSN":     r"(?<!\d)\d{3}-\d{2}-\d{4}(?!\d)",
    "EMAIL":   r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+",
    "AADHAAR": r"(?<!\d)\d{4}[ -]\d{4}[ -]\d{4}(?!\d)",
    "PHONE":   r"(?<!\d)(?:\+91[ -]?)?[6-9]\d{9}(?!\d)",
    "DATE":    r"(?<!\d)\d{1,2}[/-]\d{1,2}[/-]\d{2,4}(?!\d)",
}


def detect_regex(text: str) -> list[Span]:
    spans = []
    for label, pattern in REGEX_PATTERNS.items():
        for m in re.finditer(pattern, text):
            spans.append(Span(m.start(), m.end(), label, m.group(), "regex"))
    return resolve_overlaps(spans)


# ---------- Layer B: spaCy NER ----------
# spaCy label -> our label. We ignore labels we don't care about.
SPACY_LABEL_MAP = {
    "PERSON": "PERSON",
    "GPE": "LOCATION",   # countries, cities, states
    "LOC": "LOCATION",
    "FAC": "LOCATION",   # buildings, hospitals
    "ORG": "ORG",
}

_nlp = None  # loaded lazily so importing this file stays fast


def _get_nlp(model: str = "en_core_web_sm"):
    global _nlp
    if _nlp is None:
        import spacy
        _nlp = spacy.load(model)
    return _nlp


def detect_spacy(text: str, model: str = "en_core_web_sm") -> list[Span]:
    doc = _get_nlp(model)(text)
    spans = [
        Span(e.start_char, e.end_char, SPACY_LABEL_MAP[e.label_], e.text, "spacy")
        for e in doc.ents
        if e.label_ in SPACY_LABEL_MAP
    ]
    return resolve_overlaps(spans)


# ---------- Layer C: hybrid ----------
def detect_hybrid(text: str, model: str = "en_core_web_sm") -> list[Span]:
    # regex is listed first so it wins ties against spaCy
    return resolve_overlaps(detect_regex(text) + detect_spacy(text, model))


# ---------- helper ----------
def resolve_overlaps(spans: list[Span]) -> list[Span]:
    """
    Two detectors may flag the same text. Keep one span per region:
    the one that starts first; on a tie the longer one; on a further tie
    regex beats spacy (regex is more precise on structured data).
    """
    ordered = sorted(
        spans,
        key=lambda s: (s.start, -(s.end - s.start), s.source != "regex"),
    )
    kept, last_end = [], -1
    for s in ordered:
        if s.start >= last_end:
            kept.append(s)
            last_end = s.end
    return kept
