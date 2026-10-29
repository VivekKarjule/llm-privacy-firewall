from src.detector import detect_regex, resolve_overlaps, _keep_entity, Span


def found(text):
    return {(s.label, s.text) for s in detect_regex(text)}


def test_ssn_separator_variants():
    assert ("SSN", "123 45 6789") in found("ssn 123 45 6789")
    assert ("SSN", "123.45.6789") in found("my ssn: 123.45.6789")


def test_plain_ssn_needs_context_and_masks_only_digits():
    assert ("SSN", "742307916") in found("SSN is 742307916 for Amit")
    assert found("order number 742307916") == set()      # no keyword -> not flagged


def test_spaced_phone_and_plus91():
    assert ("PHONE", "71819 60013") in found("Call 71819 60013 now")
    assert ("PHONE", "+91 9048281489") in found("Reach on +91 9048281489")


def test_plain_aadhaar():
    assert ("AADHAAR", "316155940781") in found("Aadhaar number 316155940781 ok")


def test_written_dates():
    assert ("DATE", "11 May 2021") in found("Admitted on 11 May 2021 at X")
    assert ("DATE", "March 5, 2024") in found("seen March 5, 2024.")


def test_regex_beats_overlapping_spacy_span():
    spacy_span = Span(0, 12, "PERSON", "Aadhaar 9871", "spacy")
    regex_span = Span(8, 22, "AADHAAR", "9871 3315 0983", "regex")
    assert resolve_overlaps([spacy_span, regex_span]) == [regex_span]


def test_noise_filter():
    assert not _keep_entity("SSN")
    assert not _keep_entity("Aadhaar 9871")
    assert not _keep_entity("a@b.com")
    assert _keep_entity("john doe")
