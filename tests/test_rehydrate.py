from src.rehydrate import rehydrate

M = {"[PERSON_1]": "John Doe", "[SSN_1]": "123-45-6789", "[PERSON_10]": "Zed"}


def test_exact_placeholder():
    assert rehydrate("Hi [PERSON_1]!", M) == "Hi John Doe!"


def test_possessive():
    assert rehydrate("[PERSON_1]'s record", M) == "John Doe's record"


def test_lowercase_variant():
    assert rehydrate("see [person_1]", M) == "see John Doe"


def test_space_variant():
    assert rehydrate("see [PERSON 1]", M) == "see John Doe"


def test_bare_variant():
    assert rehydrate("see PERSON_1 now", M) == "see John Doe now"


def test_person_1_does_not_swallow_person_10():
    assert rehydrate("[PERSON_10] and [PERSON_1]", M) == "Zed and John Doe"


def test_unknown_placeholder_left_alone():
    assert rehydrate("[PERSON_9]", M) == "[PERSON_9]"


def test_unrelated_text_untouched():
    assert rehydrate("Section 2 of snake_case_name", M) == "Section 2 of snake_case_name"


def test_multiple_in_one_string():
    assert rehydrate("[PERSON_1] / [SSN_1]", M) == "John Doe / 123-45-6789"
