"""
rehydrate.py - puts the original values back into the LLM's response.

Why not just str.replace? Because LLMs mangle placeholders:
    [PERSON_1]  ->  [PERSON_1]'s,  [person_1],  PERSON_1,  [PERSON 1]
This module tolerates those variants. Anything that does NOT match a
known placeholder is left untouched.
"""
import re

# Alternative 1: bracketed, case-insensitive, underscore or space  -> [PERSON_1] [person 1]
# Alternative 2: bare with underscore                              -> PERSON_1
_PATTERN = re.compile(
    r"\[\s*([A-Za-z]+)[_ ](\d+)\s*\]|\b([A-Za-z]+)_(\d+)\b"
)


def rehydrate(text: str, mapping: dict[str, str]) -> str:
    def _swap(m: re.Match) -> str:
        label = (m.group(1) or m.group(3)).upper()
        number = m.group(2) or m.group(4)
        key = f"[{label}_{number}]"
        return mapping.get(key, m.group(0))   # unknown -> leave as is

    return _PATTERN.sub(_swap, text)
