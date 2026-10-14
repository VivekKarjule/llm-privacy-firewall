# Threat Model: LLM Privacy Firewall

## 1. System overview
[2-3 sentences: user -> firewall -> cloud LLM -> firewall -> user]

## 2. Assets (what we protect)
| Entity type | Examples | Detection method | In scope for v1? |
|---|---|---|---|
| PERSON | ... | spaCy NER | Yes |
| SSN | ... | Regex | Yes |
| ... | | | |

## 3. Trust boundaries
- Trusted: [user's machine, the firewall, the local mapping]
- Untrusted: [cloud LLM provider and anything past it]

## 4. Adversaries
1. [Cloud LLM provider: what could they do with the data?]
2. [Insider reading logs]

## 5. Failure modes
| Failure | Impact | Mitigation |
|---|---|---|
| Detector misses a name | Leak to provider | Measure recall, hybrid detection |
| ... | | |

## 6. Assumptions
- [e.g. The local machine is not compromised]
- [e.g. Input is English text]

## 7. Out of scope
- [list]

## 8. Known limitations
- Pseudonymization is reversible and is still personal data under GDPR.
- No NER model has 100% recall.
- Quasi-identifiers can still re-identify individuals.