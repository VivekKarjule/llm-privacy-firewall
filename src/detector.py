"""
detector.py - finds sensitive spans in text.   (v2: hardened in Step 3)

Strategies compared in evaluation:
  detect_regex  - rules for structured data (SSN, email, phone, ...)
  detect_spacy  - statistical NER for names, places, organisations
  detect_hybrid - both, with REGEX ALWAYS WINNING on overlaps

Step 3 changes (each motivated by a measured failure in Step 2):
  1. resolve_overlaps: regex spans beat spaCy spans (fixed the 'Aadhaar 9871' bug)
  2. broader regexes: SSN separators, context-based plain SSN, spaced phones,
     plain Aadhaar, dates written in words
  3. lowercase names: second spaCy pass on a capitalised copy of the text
  4. spaCy noise filter: drop entities containing digits/@ or label-words like 'SSN'
"""
import re
from dataclasses import dataclass


@dataclass(frozen=True)
class Span:
    start: int      # index of first character
    end: int        # index AFTER last character (slice style)
    label: str      # e.g. "PERSON", "SSN"
    text: str       # text[start:end]
    source: str     # "regex", "spacy" or "gold"


_MONTH = (r"(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|June?|July?|"
          r"Aug(?:ust)?|Sep(?:t(?:ember)?)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)")

# label -> list of patterns. A named group (?P<val>...) means "only mask the group"
# (used when a keyword like 'SSN' gives context but must not be masked itself).
# (?<!\d) / (?!\d) = "not glued to other digits".
REGEX_PATTERNS = {
    "SSN": [
        r"(?<!\d)\d{3}[- .]\d{2}[- .]\d{4}(?!\d)",
        r"(?i:\b(?:ssn|social security(?: number)?)\b[\s:#-]*(?:is\s*)?(?P<val>\d{9}))(?!\d)",
    ],
    "EMAIL": [r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+"],
    "AADHAAR": [r"(?<!\d)[2-9]\d{3}[ -]?\d{4}[ -]?\d{4}(?!\d)"],
    "PHONE": [r"(?<!\d)(?:\+91[ -]?)?[6-9]\d{4}[ -]?\d{5}(?!\d)"],
    "DATE": [
        r"(?<!\d)\d{1,2}[/-]\d{1,2}[/-]\d{2,4}(?!\d)",
        rf"(?i:(?<!\d)\d{{1,2}}(?:st|nd|rd|th)?\s+{_MONTH}\.?,?\s+\d{{4}})(?!\d)",
        rf"(?i:\b{_MONTH}\.?\s+\d{{1,2}}(?:st|nd|rd|th)?,?\s+\d{{4}})(?!\d)",
    ],
}


def detect_regex(text: str) -> list[Span]:
    spans = []
    for label, patterns in REGEX_PATTERNS.items():
        for pat in patterns:
            for m in re.finditer(pat, text):
                if m.groupdict().get("val"):
                    s, e = m.start("val"), m.end("val")
                else:
                    s, e = m.start(), m.end()
                spans.append(Span(s, e, label, text[s:e], "regex"))
    return resolve_overlaps(spans)


# ---------- spaCy NER ----------
SPACY_LABEL_MAP = {"PERSON": "PERSON", "GPE": "LOCATION", "LOC": "LOCATION",
                   "FAC": "LOCATION", "ORG": "ORG"}
# Words spaCy wrongly treats as entities (seen in Step 2 error lists).
# NOTE: tuned on my synthetic data, so a held-out set would likely score lower.
NOISE_WORDS = {"ssn", "aadhaar", "email", "reach", "refer", "call", "phone",
               "patient", "summarize", "mobile", "contact", "dob"}
_LOWERCASE_PASS_LABELS = {"PERSON", "GPE", "LOC"}

_nlp = None


def _get_nlp(model: str = "en_core_web_sm"):
    global _nlp
    if _nlp is None:
        import spacy
        _nlp = spacy.load(model)
    return _nlp


def _keep_entity(text: str) -> bool:
    """False for spaCy entities that are really regex territory or label words."""
    t = text.strip().lower()
    if any(ch.isdigit() for ch in t) or "@" in t:
        return False
    return t not in NOISE_WORDS


def detect_spacy(text: str, model: str = "en_core_web_sm") -> list[Span]:
    nlp = _get_nlp(model)
    spans = [
        Span(e.start_char, e.end_char, SPACY_LABEL_MAP[e.label_], e.text, "spacy")
        for e in nlp(text).ents
        if e.label_ in SPACY_LABEL_MAP and _keep_entity(e.text)
    ]
    # Second pass: spaCy leans on capital letters, so re-run on a copy with every
    # word capitalised (same length -> offsets stay valid). Accept only PERSON /
    # LOCATION hits whose ORIGINAL text was all-lowercase.
    fixed = re.sub(r"\b[a-z]", lambda m: m.group().upper(), text)
    if fixed != text:
        for e in nlp(fixed).ents:
            orig = text[e.start_char:e.end_char]
            if (e.label_ in _LOWERCASE_PASS_LABELS and orig == orig.lower()
                    and _keep_entity(orig)):
                spans.append(Span(e.start_char, e.end_char,
                                  SPACY_LABEL_MAP[e.label_], orig, "spacy"))
    return resolve_overlaps(spans)


def detect_hybrid(text: str, model: str = "en_core_web_sm") -> list[Span]:
    return resolve_overlaps(detect_regex(text) + detect_spacy(text, model))


def resolve_overlaps(spans: list[Span]) -> list[Span]:
    """Keep one span per region. Priority: regex > spacy, then longer, then earlier."""
    ranked = sorted(spans, key=lambda s: (s.source != "regex", -(s.end - s.start), s.start))
    kept = []
    for s in ranked:
        if all(s.end <= k.start or s.start >= k.end for k in kept):
            kept.append(s)
    return sorted(kept, key=lambda s: s.start)
