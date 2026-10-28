"""
datagen.py - generates FAKE labeled sentences for evaluating the detector.

Each example = a sentence + the exact "gold" spans (what a perfect detector
should find). Everything is synthetic and seeded, so results are reproducible
and no real personal data is ever involved.

Two sets:
  clean       - normal formatting, plus sentences with NO sensitive data
                (to catch false positives)
  adversarial - the tricky cases: lowercase names, spaced/plain numbers,
                names that are also common words, dates written in words

Template slots look like {LABEL} or {LABEL:variant}, e.g. {SSN:spaced}.

Run   python -m src.datagen   to save both sets as JSON in data/ (for reading).
"""
import json
import random
import re
from dataclasses import dataclass
from pathlib import Path

from src.detector import Span


@dataclass
class Example:
    text: str
    spans: list  # list[Span], source="gold"


FIRST = ["Rahul", "Priya", "Amit", "Sneha", "John", "Maria", "David", "Anjali",
         "Rohan", "Emily", "Vikram", "Neha", "Michael", "Sara", "Arjun", "Kavya"]
LAST = ["Sharma", "Patel", "Deshmukh", "Iyer", "Smith", "Johnson", "Kulkarni",
        "Reddy", "Brown", "Singh", "Joshi", "Williams", "Nair", "Gupta", "Miller", "Rao"]
# first names that are also ordinary English words - hard for NER
TRICKY_FIRST = ["Rose", "Will", "Grace", "Hope", "April", "Mark", "Amber", "Joy"]
CITIES = ["Pune", "Mumbai", "Delhi", "Bengaluru", "Chennai", "Kolkata", "Hyderabad",
          "Nagpur", "Jaipur", "London", "Toronto", "Singapore", "New York"]
ORGS = ["Apollo Hospital", "Fortis Hospital", "Ruby Hall Clinic", "Mayo Clinic",
        "Max Healthcare", "Manipal Hospitals", "Sahyadri Hospital", "Cleveland Clinic"]
DOMAINS = ["example.com", "mail.org", "hospital.in", "clinic.net"]
MONTHS = ["January", "February", "March", "April", "May", "June", "July",
          "August", "September", "October", "November", "December"]


def _value(label: str, variant: str | None, rng: random.Random) -> str:
    """Produce one fake value for a slot."""
    if label == "PERSON":
        if variant == "tricky":
            return f"{rng.choice(TRICKY_FIRST)} {rng.choice(LAST)}"
        name = f"{rng.choice(FIRST)} {rng.choice(LAST)}"
        return name.lower() if variant == "lower" else name
    if label == "LOCATION":
        city = rng.choice(CITIES)
        return city.lower() if variant == "lower" else city
    if label == "ORG":
        return rng.choice(ORGS)
    if label == "SSN":
        a, b, c = rng.randint(100, 899), rng.randint(10, 99), rng.randint(1000, 9999)
        sep = {"spaced": " ", "plain": "", "dots": "."}.get(variant, "-")
        return f"{a}{sep}{b}{sep}{c}"
    if label == "EMAIL":
        return f"{rng.choice(FIRST).lower()}.{rng.choice(LAST).lower()}@{rng.choice(DOMAINS)}"
    if label == "PHONE":
        digits = str(rng.randint(6, 9)) + "".join(str(rng.randint(0, 9)) for _ in range(9))
        if variant == "spaced":
            return f"{digits[:5]} {digits[5:]}"
        if variant == "plus91":
            return f"+91 {digits}"
        return digits
    if label == "AADHAAR":
        digits = str(rng.randint(2, 9)) + "".join(str(rng.randint(0, 9)) for _ in range(11))
        if variant == "plain":
            return digits
        return f"{digits[:4]} {digits[4:8]} {digits[8:]}"
    if label == "DATE":
        d, m, y = rng.randint(1, 28), rng.randint(1, 12), rng.randint(2019, 2026)
        if variant == "written":
            return f"{d} {MONTHS[m - 1]} {y}"
        return f"{d:02d}/{m:02d}/{y}"
    raise ValueError(f"unknown slot label: {label}")


CLEAN_TEMPLATES = [
    "Summarize the medical record for {PERSON}, SSN {SSN}.",
    "Patient {PERSON} can be reached at {PHONE} or {EMAIL}.",
    "{PERSON} was admitted to {ORG} in {LOCATION} on {DATE}.",
    "Please draft a discharge note for {PERSON}, Aadhaar {AADHAAR}.",
    "Email {EMAIL} about the appointment of {PERSON} on {DATE}.",
    "{PERSON} from {LOCATION} reported chest pain; contact {PHONE}.",
    "Insurance claim for {PERSON} (SSN {SSN}) at {ORG}.",
    "Refer {PERSON} to {ORG}, {LOCATION}. Callback: {PHONE}.",
]

# No sensitive data at all. Anything detected here is a FALSE POSITIVE.
NEGATIVE_TEMPLATES = [
    "The patient reported mild fever and a persistent headache.",
    "Prescribed Metformin 500mg twice daily after meals.",
    "Summarize the key findings of the clinical trial in simple terms.",
    "Explain how blood pressure medication works.",
    "What are common side effects of Ibuprofen and Paracetamol?",
    "The lab results show elevated cholesterol levels.",
    "Take 2 tablets 3 times a day for 10 days.",
    "Diabetes and hypertension are common chronic conditions.",
]

ADVERSARIAL_TEMPLATES = [
    "summarize the record for {PERSON:lower}, ssn {SSN:spaced}.",
    "Patient {PERSON:tricky} lives in {LOCATION:lower}.",
    "SSN is {SSN:plain} for {PERSON}.",
    "Call {PHONE:spaced} or write to {EMAIL}.",
    "Reach {PERSON:lower} on {PHONE:plus91}.",
    "Aadhaar number {AADHAAR:plain} belongs to {PERSON}.",
    "Admitted on {DATE:written} at {ORG}.",
    "{PERSON:tricky} met {PERSON:lower} in {LOCATION}.",
    "my ssn: {SSN:dots}",
    "refer {PERSON:lower} to {ORG}, {LOCATION:lower}.",
]

_SLOT = re.compile(r"\{(\w+)(?::(\w+))?\}")


def _fill(template: str, rng: random.Random) -> Example:
    text, spans, pos = "", [], 0
    for m in _SLOT.finditer(template):
        text += template[pos:m.start()]
        label, variant = m.group(1), m.group(2)
        value = _value(label, variant, rng)
        spans.append(Span(len(text), len(text) + len(value), label, value, "gold"))
        text += value
        pos = m.end()
    text += template[pos:]
    return Example(text, spans)


def generate(kind: str = "clean", n: int = 150, seed: int = 42) -> list[Example]:
    """kind: 'clean' or 'adversarial'. Same seed -> identical dataset."""
    rng = random.Random(seed)
    if kind == "clean":
        pool = CLEAN_TEMPLATES * 4 + NEGATIVE_TEMPLATES * 2   # ~20% negatives
    elif kind == "adversarial":
        pool = ADVERSARIAL_TEMPLATES
    else:
        raise ValueError("kind must be 'clean' or 'adversarial'")
    return [_fill(rng.choice(pool), rng) for _ in range(n)]


def save(examples: list[Example], path: Path) -> None:
    data = [{"text": e.text,
             "spans": [{"start": s.start, "end": s.end, "label": s.label, "text": s.text}
                       for s in e.spans]} for e in examples]
    path.parent.mkdir(exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


if __name__ == "__main__":
    for kind, n in (("clean", 150), ("adversarial", 100)):
        out = Path("data") / f"eval_{kind}.json"
        save(generate(kind, n), out)
        print(f"saved {n} {kind} examples -> {out}")
