# AI coding-agent code review — 24 October 2026

[Overview](../README.md) · [Validation](VALIDATION.md) · [Evidence](../EVALUATION.md)

An AI coding-agent reviewer (a separate session) inspected data, model
registration, inference, workspaces, exchanges, UI state and tests. The primary
agent checked joint compatibility and documentation. This is an AI-assisted
self-audit under the single author, not independent human review, security review
or clinician review.

| Finding | Reproduction and repair |
| --- | --- |
| P1: public evidence could diverge from a reviewed workspace | Mutate `research.json` or substitute the ZIP. Verification now binds provenance/original bytes and compares typed study, source and predictions with the same workspace. New invalid sources fail before output creation. |
| P2: a rehashed split could misstate related-image groups or masks | Alter group/fingerprint/positive metadata. Loading now recomputes decoded fingerprints and mask content, rejects cross-group/split related images, malformed rows and noncanonical paths. |
| P2: registration accepted ambiguous parity/numeric values | Supply truthy strings, absent probes or nonfinite/invalid values. Registration now requires strict parity evidence and valid numeric dimensions/postprocessing. |
| P2: model/backend/permission changes retained stale results | Change settings while work/results exist. The UI cancels and clears prior work/review, prefers the current installed research model and displays retryable launch errors. |

Runtime changes are in `workspace.py`, `data.py`, `inference.py` and `app.py`.
`tests/test_review_regressions.py` and model tests cover failures and compatibility.
Shared wire schemas, dependencies, installed weights and datasets were unchanged.

Historical synthetic/public workspaces were verified unchanged. Stronger frozen-
manifest loading retained the existing 1,000-image split identity. Actual local
ONNX/OpenVINO checks are recorded separately in [Evaluation](../EVALUATION.md).
Unsigned local hashes still establish consistency, not authenticity. Patient
independence, negative-examination performance, clinical validity and NPU execution
remain unproven.
