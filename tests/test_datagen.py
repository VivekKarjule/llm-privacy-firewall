from src import datagen


def test_gold_offsets_are_exact():
    for kind in ("clean", "adversarial"):
        for ex in datagen.generate(kind, 200, seed=1):
            for s in ex.spans:
                assert ex.text[s.start:s.end] == s.text


def test_same_seed_same_dataset():
    a = datagen.generate("clean", 50, seed=7)
    b = datagen.generate("clean", 50, seed=7)
    assert [e.text for e in a] == [e.text for e in b]


def test_different_seed_differs():
    a = datagen.generate("clean", 50, seed=1)
    b = datagen.generate("clean", 50, seed=2)
    assert [e.text for e in a] != [e.text for e in b]


def test_clean_set_contains_negatives():
    exs = datagen.generate("clean", 150)
    assert any(len(e.spans) == 0 for e in exs)


def test_adversarial_variants_are_really_different():
    rng = datagen.random.Random(0)
    assert " " in datagen._value("SSN", "spaced", rng)
    assert "-" not in datagen._value("SSN", "plain", rng)
    v = datagen._value("PERSON", "lower", rng)
    assert v == v.lower()


def test_bad_kind_rejected():
    import pytest
    with pytest.raises(ValueError):
        datagen.generate("nope")
