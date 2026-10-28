"""
demo.py - run from the project root:  python demo.py
Shows the full round trip with a FAKE LLM (no API key needed yet).
"""
from src.firewall import Firewall


def fake_llm(prompt: str) -> str:
    # Mimics an LLM that rewrites placeholders a little, as real ones do.
    return f"Here is a summary. The record concerns {prompt.split('for ')[1].split(',')[0].lower()}."


prompt = ("Summarize this medical record for john doe, SSN 123 45 6789, "
          "email john.doe@example.com, phone 9876543210.")

for strategy in ("regex", "hybrid"):   # hybrid needs spaCy + en_core_web_sm
    try:
        fw = Firewall(strategy)
        safe = fw.sanitize(prompt)
    except Exception as e:
        print(f"[{strategy}] skipped: {e}\n")
        continue
    print(f"=== strategy: {strategy} ===")
    print("Original :", prompt)
    print("Sent out :", safe)          # <- this is all the cloud ever sees
    reply = fake_llm(safe)
    print("LLM reply:", reply)
    print("Restored :", fw.restore(reply), "\n")
