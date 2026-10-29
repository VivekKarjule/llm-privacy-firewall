# Threat Model: LLM Privacy Firewall

## 1. System overview
A user's prompt passes through a local firewall that masks sensitive values with
placeholders, sends only the masked prompt to a third-party LLM, and restores the
originals in the reply. The placeholder-to-original mapping never leaves local memory.

## 2. Assets
| Entity | Examples | Detection | In scope (v1) |
|---|---|---|---|
| PERSON | John Doe | spaCy NER | Yes |
| LOCATION / ORG | Pune, Apollo Hospital | spaCy NER | Yes |
| SSN, AADHAAR | 123-45-6789 | Regex | Yes |
| PHONE, EMAIL, DATE | 9876543210 | Regex | Yes |
| Diagnoses, medications | diabetes | none | No |

## 3. Trust boundaries
- **Trusted:** the user's machine, the firewall process, its in-memory mapping.
- **Untrusted:** the LLM provider and everything after the network boundary.

## 4. Adversaries
1. **LLM provider:** may log, retain, or train on prompts. Mitigated by masking.
2. **Insider reading logs:** mitigated by logging only sanitized prompts.
3. **Another local user/process:** can read memory; out of scope (see section 7).

## 5. Failure modes
| Failure | Impact | Mitigation / status |
|---|---|---|
| Detector misses an entity | Direct leak | Hybrid detection; measure leak% on clean and adversarial sets |
| Unusual formatting (spaced SSN, lowercase name) | Leak | Hardened regexes + lowercase pass; adversarial test set |
| Quasi-identifiers (age + zip + rare disease) | Re-identification | Not handled; documented |
| Context leak ("the CEO of Tesla") | Re-identification | Not handled; documented |
| Over-masking / wrong labels | Worse LLM answers | Noise filter; precision tracked |
| LLM rewrites a placeholder | Failed restore | Tolerant rehydration, tested |
| Mapping or raw prompt leaks locally | Exposure of originals | Memory only; never logged or returned; sessions deletable |

## 6. Assumptions
- The local machine and the firewall process are not compromised.
- Input is English text.
- TLS protects the connection to the provider.

## 7. Out of scope
- Malicious users deliberately evading detection
- Legal compliance certification (HIPAA / GDPR)
- Images, PDFs, audio, non-English text
- LLM hallucination or output safety
- Memory or disk forensics on the local machine

## 8. Known limitations
- Pseudonymization is reversible, so masked data is still personal data under GDPR.
- No NER model guarantees full recall.
- Evaluation uses synthetic data only; real-world performance will differ.
