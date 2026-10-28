from src.firewall import Firewall


def test_roundtrip_regex_only():
    fw = Firewall(strategy="regex")
    safe = fw.sanitize("SSN 123-45-6789 email a@b.com")
    assert "123-45-6789" not in safe and "a@b.com" not in safe
    # Pretend the LLM echoed the placeholders back
    assert fw.restore(safe) == "SSN 123-45-6789 email a@b.com"


def test_bad_strategy_rejected():
    import pytest
    with pytest.raises(ValueError):
        Firewall(strategy="magic")
