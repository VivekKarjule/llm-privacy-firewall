import pytest
from src.detector import detect_regex, detect_spacy, detect_hybrid, resolve_overlaps, Span


def labels(spans):
    return {(s.label, s.text) for s in spans}


# ---------- regex ----------
def test_ssn():
    assert ("SSN", "123-45-6789") in labels(detect_regex("SSN is 123-45-6789."))


def test_email():
    assert ("EMAIL", "a.b@x.co.in") in labels(detect_regex("mail a.b@x.co.in now"))


def test_phone_plain_and_with_country_code():
    found = labels(detect_regex("call 9876543210 or +91 9123456789"))
    assert ("PHONE", "9876543210") in found
    assert ("PHONE", "+91 9123456789") in found


def test_aadhaar():
    assert ("AADHAAR", "2345 6789 0123") in labels(detect_regex("id 2345 6789 0123"))


def test_date():
    assert ("DATE", "12/03/2025") in labels(detect_regex("admitted 12/03/2025"))


def test_long_number_is_not_a_phone():
    # 12 digits glued together must NOT yield a 10-digit phone match
    assert all(s.label != "PHONE" for s in detect_regex("ref 987654321012"))


def test_no_false_positive_on_plain_text():
    assert detect_regex("The patient felt better after rest.") == []


def test_span_offsets_are_correct():
    text = "mail me at a@b.com please"
    for s in detect_regex(text):
        assert text[s.start:s.end] == s.text


# ---------- overlap resolution ----------
def test_overlap_keeps_longer_span():
    a = Span(0, 5, "X", "hello", "spacy")
    b = Span(0, 11, "Y", "hello world", "spacy")
    assert resolve_overlaps([a, b]) == [b]


def test_overlap_regex_wins_tie():
    a = Span(0, 5, "A", "12345", "spacy")
    b = Span(0, 5, "B", "12345", "regex")
    assert resolve_overlaps([a, b])[0].source == "regex"


# ---------- spaCy (skipped automatically if model not installed) ----------
try:
    import spacy
    spacy.load("en_core_web_sm")
    HAS_MODEL = True
except (ImportError, OSError):
    HAS_MODEL = False

needs_model = pytest.mark.skipif(not HAS_MODEL, reason="en_core_web_sm not installed")


@needs_model
def test_spacy_finds_person():
    found = labels(detect_spacy("Summarize the record for John Doe from Pune."))
    assert any(l == "PERSON" for l, _ in found)


@needs_model
def test_hybrid_catches_both_kinds():
    found = labels(detect_hybrid("John Doe, SSN 123-45-6789, lives in Pune."))
    kinds = {l for l, _ in found}
    assert "SSN" in kinds and "PERSON" in kinds
