# LLM Privacy Firewall

A local middleware that detects and masks sensitive data (PII) in prompts
before they reach a cloud LLM, and restores it in the response.

## Status
Work in progress (mini project, AI lab).

## Roadmap
- [x] Project setup
- [ ] Threat model
- [ ] Detector (regex / spaCy / hybrid)
- [ ] Mapper and rehydration
- [ ] FastAPI proxy
- [ ] Evaluation
- [ ] Phase 2: synthetic data generator

## Note
All test data is synthetic. No real personal data is used.