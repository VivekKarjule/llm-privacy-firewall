from src.datagen import Example
from src.detector import Span
from src.evaluate import score, summarize


def G(s, e, label, text="x"):
    return Span(s, e, label, text, "gold")


def P(s, e, label, text="x"):
    return Span(s, e, label, text, "test")


def run(preds, golds):
    ex = [Example("0123456789", golds)]
    counts, errors = score(lambda t: preds, ex)
    return summarize(counts), errors


def test_perfect_detector():
    rows, _ = run([P(0, 5, "A")], [G(0, 5, "A")])
    assert rows["ALL"]["sP"] == rows["ALL"]["sR"] == 1.0
    assert rows["ALL"]["leak"] == 0.0


def test_partial_overlap_is_lenient_hit_but_not_strict():
    rows, _ = run([P(0, 3, "A")], [G(0, 5, "A")])
    assert rows["ALL"]["sR"] == 0.0 and rows["ALL"]["lR"] == 1.0
    assert rows["ALL"]["leak"] == 0.0   # touched, so not totally unmasked


def test_wrong_label_counts_as_miss_but_not_leak():
    rows, _ = run([P(0, 5, "B")], [G(0, 5, "A")])
    assert rows["A"]["lR"] == 0.0
    assert rows["A"]["leak"] == 0.0     # still masked (just mislabeled)


def test_completely_missed_is_a_leak():
    rows, errors = run([], [G(0, 5, "A")])
    assert rows["ALL"]["leak"] == 1.0
    assert len(errors["missed"]) == 1


def test_false_positive_hurts_precision_only():
    rows, errors = run([P(0, 5, "A"), P(6, 9, "A")], [G(0, 5, "A")])
    assert rows["ALL"]["lR"] == 1.0
    assert rows["ALL"]["lP"] == 0.5
    assert len(errors["false_pos"]) == 1


def test_no_division_by_zero_on_empty():
    rows, _ = run([], [])
    assert rows["ALL"]["lP"] == 0.0 and rows["ALL"]["lR"] == 0.0
