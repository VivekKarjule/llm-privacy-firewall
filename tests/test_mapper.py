from src.detector import Span
from src.mapper import Mapper


def span(text_full, target, label):
    i = text_full.index(target)
    return Span(i, i + len(target), label, target, "test")


def test_basic_replacement():
    t = "Record for John Doe."
    m = Mapper()
    out = m.sanitize(t, [span(t, "John Doe", "PERSON")])
    assert out == "Record for [PERSON_1]."
    assert m.mapping == {"[PERSON_1]": "John Doe"}


def test_same_entity_same_placeholder():
    t = "John Doe met john doe."
    m = Mapper()
    spans = [Span(0, 8, "PERSON", "John Doe", "t"), Span(13, 21, "PERSON", "john doe", "t")]
    out = m.sanitize(t, spans)
    assert out == "[PERSON_1] met [PERSON_1]."
    assert len(m.mapping) == 1


def test_different_entities_get_different_numbers():
    t = "Alice and Bob"
    m = Mapper()
    out = m.sanitize(t, [Span(0, 5, "PERSON", "Alice", "t"), Span(10, 13, "PERSON", "Bob", "t")])
    assert out == "[PERSON_1] and [PERSON_2]"


def test_mixed_labels_count_separately():
    t = "Alice 123-45-6789"
    m = Mapper()
    out = m.sanitize(t, [Span(0, 5, "PERSON", "Alice", "t"), Span(6, 17, "SSN", "123-45-6789", "t")])
    assert out == "[PERSON_1] [SSN_1]"


def test_mapping_persists_across_calls():
    m = Mapper()
    t1 = "Alice"
    m.sanitize(t1, [Span(0, 5, "PERSON", "Alice", "t")])
    out = m.sanitize("Alice again", [Span(0, 5, "PERSON", "Alice", "t")])
    assert out == "[PERSON_1] again"


def test_no_spans_returns_text_unchanged():
    assert Mapper().sanitize("nothing here", []) == "nothing here"
