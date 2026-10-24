# Changelog

Notable changes to the endoscopy companion. Dated test outcomes live in
[EVALUATION.md](EVALUATION.md). Research software, not a diagnostic device.

## Unreleased

### Added
- Ed25519 producer signatures for review ZIPs (`endo.cli keygen`,
  `--signing-key`/`LOVISA_SIGNING_KEY_FILE`). Signed claims carry the measured
  false-positive share for the exact registered ONNX model when an evaluation is
  supplied, otherwise "not measured". New dependency: `cryptography`.

### Changed
- The shared endoscopy reader accepts one optional `signature.json` entry.
  Unsigned archives remain valid.

## 0.1.0 — 24 October 2026

Baseline before this changelog; see [EVALUATION.md](EVALUATION.md).
