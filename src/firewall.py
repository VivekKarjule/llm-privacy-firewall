"""
firewall.py - ties detect -> sanitize -> (LLM) -> rehydrate together.
One Firewall object = one session = one private mapping.
"""
from src import detector
from src.mapper import Mapper
from src.rehydrate import rehydrate

_STRATEGIES = {
    "regex": detector.detect_regex,
    "spacy": detector.detect_spacy,
    "hybrid": detector.detect_hybrid,
}


class Firewall:
    def __init__(self, strategy: str = "hybrid"):
        if strategy not in _STRATEGIES:
            raise ValueError(f"strategy must be one of {list(_STRATEGIES)}")
        self._detect = _STRATEGIES[strategy]
        self._mapper = Mapper()

    def sanitize(self, prompt: str) -> str:
        return self._mapper.sanitize(prompt, self._detect(prompt))

    def restore(self, llm_response: str) -> str:
        return rehydrate(llm_response, self._mapper.mapping)
