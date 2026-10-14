"""
Local Privacy-Preserving LLM Firewall - Prototype v0.1
Pipeline: detect sensitive spans -> replace with placeholders -> (LLM) -> rehydrate

Run:  python firewall_prototype.py
Optional (better name/place detection):
    pip install spacy
    python -m spacy download en_core_web_sm
"""
import re

# ---------- 1. DETECTION ----------
# Layer A: regex for structured data (patterns are predictable)
REGEX_PATTERNS = {
    "SSN":   r"\b\d{3}-\d{2}-\d{4}\b",
    "EMAIL": r"\b[\w.+-]+@[\w-]+\.[\w.]+\b",
    "PHONE": r"\b(?:\+?\d{1,3}[ -]?)?\d{10}\b",
}

# Layer B: statistical NER for unstructured data (names, places, orgs)
try:
    import spacy
    nlp = spacy.load("en_core_web_sm")
    SPACY_LABELS = {"PERSON": "PERSON", "GPE": "LOCATION", "ORG": "ORG"}
except Exception:
    nlp = None
    print("[note] spaCy not available - running regex-only mode\n")


def detect(text):
    """Return list of (start, end, label, original_text)."""
    spans = []
    for label, pattern in REGEX_PATTERNS.items():
        for m in re.finditer(pattern, text):
            spans.append((m.start(), m.end(), label, m.group()))
    if nlp:
        for ent in nlp(text).ents:
            if ent.label_ in SPACY_LABELS:
                spans.append((ent.start_char, ent.end_char,
                              SPACY_LABELS[ent.label_], ent.text))
    # Resolve overlaps: sort by start, longer first; drop anything overlapping
    spans.sort(key=lambda s: (s[0], -(s[1] - s[0])))
    clean, last_end = [], -1
    for s in spans:
        if s[0] >= last_end:
            clean.append(s)
            last_end = s[1]
    return clean


# ---------- 2. SANITIZE (pseudonymize) ----------
def sanitize(text):
    """Replace sensitive spans with placeholders. Returns (safe_text, mapping)."""
    mapping = {}        # placeholder -> original
    reverse = {}        # original -> placeholder (consistency: same entity, same tag)
    counters = {}
    spans = detect(text)
    for start, end, label, original in reversed(spans):  # right-to-left keeps offsets valid
        pass
    # assign placeholders left-to-right so numbering reads naturally
    placeholders = []
    for start, end, label, original in spans:
        if original not in reverse:
            counters[label] = counters.get(label, 0) + 1
            ph = f"[{label}_{counters[label]}]"
            reverse[original] = ph
            mapping[ph] = original
        placeholders.append((start, end, reverse[original]))
    safe = text
    for start, end, ph in reversed(placeholders):
        safe = safe[:start] + ph + safe[end:]
    return safe, mapping


# ---------- 3. REHYDRATE ----------
def rehydrate(text, mapping):
    """Put original values back into the LLM's response."""
    for ph, original in mapping.items():
        text = text.replace(ph, original)
    return text


# ---------- 4. DEMO ----------
def fake_llm(prompt):
    """Stand-in for a cloud LLM so the demo needs no API key."""
    return f"Summary: The patient mentioned in the request ({prompt.split('for ')[1].split(',')[0]}) needs a follow-up visit."


if __name__ == "__main__":
    prompt = ("Summarize this medical record for John Doe, SSN 123-45-6789, "
              "email john.doe@example.com, phone 9876543210.")
    print("ORIGINAL :", prompt)

    safe, mapping = sanitize(prompt)
    print("SANITIZED:", safe)
    print("MAPPING  :", mapping)

    response = fake_llm(safe)
    print("LLM SEES/REPLIES:", response)
    print("REHYDRATED:", rehydrate(response, mapping))