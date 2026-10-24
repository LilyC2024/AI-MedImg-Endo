# Validation and reproducible checks

[Overview](../README.md) · [Executed evidence](../EVALUATION.md) · [Review findings](REVIEW.md)

## Offline software checks

Run from this checkout in its existing environment:

```bash
.venv/bin/python -m pip check
.venv/bin/python -m compileall -q src tests app.py scripts
.venv/bin/python -m ruff check src tests app.py --select F,I
.venv/bin/python -m pytest -q
.venv/bin/python scripts/check_docs.py
.venv/bin/python scripts/check_publication.py
```

The suite uses artificial pixels, temporary outputs and scripted reviewer names.
Some tests actually train/export a tiny artificial CPU model; that is real model
execution on manufactured data, not a clinical performance experiment. Separate
contract tests manufacture probability maps to test exact reconstruction.

| Boundary | Examples covered |
| --- | --- |
| Source/exchange | Unsafe ZIPs, wrong modality/case, inconsistent pixels, masks, regions and overlays |
| Workspace | Original-byte mismatch, changed/deleted provenance or ZIP, historical compatibility |
| Data | Path traversal, changed source hashes, forged decoded fingerprints, group leakage and contradictory mask metadata |
| Model | Registration/checkpoint/config mismatch, non-boolean parity claims, missing probes, invalid numeric parameters |
| Review/UI | Uncertain candidates, missing attestations, source/settings change, cancellation, startup failure and stale results |

The documentation checker verifies local files and Markdown heading anchors,
including encoded paths, repeated headings and fenced examples. It does not fetch
external URLs or implement every Markdown construct.

## Actual installed-model checks

After explicit data permission, training and registration, `endo.cli infer`
executes the actual selected backend. `endo.cli evaluate` measures the frozen
partition; report positive overlap separately from negative-image false alarms.
[Commands and test-set restrictions](TRAINING.md). A model registration is
numerical compatibility evidence, not validated screening accuracy.

From the separate LOVISA checkout, run its endoscopy contract-sync and worker
smokes. Those exercise the actual producer/consumer without issuing approvals.
Use LOVISA's real-upload smoke for the prepared research kit. Its temporary DB
must never be confused with the application's actual clinician decisions.

## Hardware and hosted checks

Linux/Windows CI exercises CPU code and generated data. It neither verifies an
Intel NPU driver nor runs public patient images, Ollama or clinical approvals.
Unavailable hardware is recorded as untested. The current host's actual CPU/
OpenVINO checks and remaining warnings are recorded in [Evaluation](../EVALUATION.md).
