# LLM Privacy Firewall

A local middleware that detects sensitive data (PII) in a prompt, replaces it with
placeholders **before** the prompt leaves the machine, and restores the original
values in the LLM's reply.

```
user prompt -> [detect] -> [mask: John Doe -> [PERSON_1]] -> cloud LLM
user answer <- [restore: [PERSON_1] -> John Doe] <-----------'
          (mapping stays in local memory only)
```

## Project structure
| Path | Purpose |
|---|---|
| `src/detector.py` | Finds sensitive spans: regex, spaCy NER, or hybrid |
| `src/mapper.py` | Placeholders + consistent per-session mapping |
| `src/rehydrate.py` | Restores originals, tolerating mangled placeholders |
| `src/firewall.py` | One session = detect -> mask -> restore |
| `src/llm.py` | Backends: `mock` (default), `ollama`, `anthropic` |
| `src/proxy.py` | FastAPI service exposing `/chat` |
| `src/datagen.py` | Synthetic labeled test data (clean + adversarial) |
| `src/evaluate.py` | Precision / recall / leak-rate comparison |
| `tests/` | pytest suite |
| `docs/threat_model.md` | What is protected, from whom, what is out of scope |

## Setup
```bash
python -m venv venv
venv\Scripts\activate            # Windows
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

## Run
```bash
python -m pytest -v                      # tests
python -m src.evaluate --show-errors     # compare regex / spaCy / hybrid
uvicorn src.proxy:app --reload           # then open http://127.0.0.1:8000/docs
```
Try `POST /chat` with
`{"prompt": "Summarize the record for John Doe, SSN 123-45-6789", "strategy": "hybrid", "backend": "mock"}`.
`sanitized_prompt` shows exactly what would leave the machine.

## Results (lenient precision / recall / leak%)
"Leak%" = sensitive items no detector span touched at all (the key privacy metric).
Synthetic data only; 150 clean + 100 adversarial sentences, fixed seed.

| Strategy | Dataset | Baseline (Step 2) | After hardening (Step 3) |
|---|---|---|---|
| regex | clean | 1.00 / 0.41 / 59% | 1.00 / 0.41 / 59% |
| regex | adversarial | 1.00 / 0.13 / 87% | 1.00 / 0.41 / 59% |
| spaCy | clean | 0.61 / 0.46 / 41% | *fill in after running* |
| spaCy | adversarial | 0.81 / 0.40 / 57% | *fill in after running* |
| hybrid | clean | 0.76 / 0.86 / 3% | *fill in after running* |
| hybrid | adversarial | 0.86 / 0.54 / 44% | *fill in after running* |

Key findings: regex is precise but blind to names; spaCy finds names but misses all
structured IDs; the hybrid cuts clean-data leakage from 59% (regex) to 3%.
Step 2 also exposed a bug (a spaCy span swallowed a regex-detected Aadhaar number),
fixed in Step 3 by giving regex priority on overlaps.

## Limitations (stated honestly)
- No NER model has 100% recall; anything missed is sent to the provider.
- Masking is **pseudonymization** (reversible), still personal data under GDPR.
  This project does **not** claim legal compliance.
- Quasi-identifiers (age + postcode + rare disease) are not handled.
- Plain 9-digit SSNs are detected only with a keyword like "SSN" nearby.
- The spaCy noise-word list was tuned on the synthetic set, so held-out scores
  would likely be lower. English only.
- The `ollama` and `anthropic` backends are implemented but only `mock` is tested.
- Sessions are in memory and not thread-safe; this is a prototype, not a hardened service.

## Roadmap
- [x] Setup, core modules, tests
- [x] Evaluation harness (clean + adversarial)
- [x] Hardening and re-measurement
- [x] FastAPI proxy
- [ ] Phase 2: synthetic data generator (Llama 3 via Ollama), future work
est data is synthetic. No real personal data is used.