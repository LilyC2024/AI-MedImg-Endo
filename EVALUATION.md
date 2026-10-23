# Evaluation — image-first endoscopy research assistant

[Overview](README.md) · [Reproduction](docs/TRAINING.md) · [Artifacts](reports/README.md)

## Actual research experiment — 23 October 2026

Official Kvasir-SEG archive: 46,227,172 bytes, SHA-256
`03b30e21d584e04facf49397a2576738fd626815771afbbf788f74a7153478f7`.
Download used verified HTTPS with the missing server intermediate certificate
supplied and verified against the system trust store; TLS validation was not
disabled. The hash matches the earlier data card, not a publisher-issued checksum.
No research image pixels, masks or trained weights are published in this repo.

The frozen manifest contains 1,000 pairs in 933 heuristic related-image groups:
682 training, 150 validation, 168 test. Exact decoded duplicates and dHash distance
<=4 remain in the same split. Patient independence is **not established**.
Manifest: `6d128ca97fb0a1a3df7dcf7bf9a0bac17d66b5bb64cded231f90b26d19daa78d`.

Actual CPU training used 12 epochs, input 128×128, base channels 8, batch 8,
seed 42, four threads, Adam 0.001, BCE+soft Dice, aligned training-only flips.
Lowest validation loss selected epoch 10. Threshold 0.5/minimum component area 8
were fixed before test evaluation. Training took 129.76 seconds in this run.
Defaults 256/base-16 remain available but were not benchmarked here.

| Actual held-out result | ONNX Runtime CPU | OpenVINO CPU (FP32 hint) |
| --- | --- | --- |
| Positive images / negative images | 168 / 0 | 168 / 0 |
| Mean positive Dice | 0.446343 | 0.446343 |
| Mean positive IoU | 0.315057 | 0.315057 |
| Box-connected-region recall proxy, IoU >=0.5 | 0.251256 | 0.251256 |
| Box-connected-region precision proxy | 0.165017 | 0.165017 |
| False candidates per negative image | Unavailable | Unavailable |
| Median image inference + region extraction | 0.11585s | 0.09782s |
| p95 image inference + region extraction | 0.26477s | 0.16562s |

These are exploratory, limited baseline results and are **insufficient for
clinical deployment**. Connected mask regions are not adjudicated individual
lesions. Kvasir is positive-only; no normal-examination specificity, cancer
classification, external generalisation or clinical time-saving result is claimed.
No training/test-set tuning was performed after reporting this baseline.

ONNX export compared three actual PyTorch/CPU probes at atol=rtol=1e-4; maximum
absolute logit difference was 3.8147e-6. OpenVINO additionally runs three live
ONNX-reference comparisons at atol=rtol=1e-3 before allowing output. Probe parity
is separate from the held-out evaluation above. Full artifacts are in `reports/`.

## Actual artificial-data experiment

An initial 8-epoch artificial model failed to produce positive masks (mean positive
Dice 0). A separately labelled 40-epoch artificial run took 24.291s and achieved
Dice 0.926209 on 17 artificial positive test images; 11 artificial negatives had
zero proposed candidates. Those coloured phantoms are software demonstrations,
not evidence of clinical detection or real negative-examination performance.
Their maximum ONNX logit difference was 0.00012207 and passed the documented
combined absolute/relative tolerance. [Artifact](reports/synthetic-test-v2.json).

## Software and integration checks

The automated suite covers adversarial archives/arrays, exact source/overlay
consistency, review completeness, immutable dataset splits, actual tiny artificial
CPU training/export/parity, registered artifact changes, Streamlit controls,
source switching, and subprocess deadlines/cancellation. Test reviewers and
clinical inference in LOVISA tests are scripted, never live clinicians/models.
Final counts and hosted outcomes are recorded at release completion below.

Actual producer → LOVISA validator smokes on artificial images passed:
non-ML fixture 1.04s; installed Kvasir model on CPU 1.08s. Each proposed one region
and validated all four artifacts. Both stop before image/clinical approval.
LOVISA also passed its real local `gemma4:e2b` smoke, stopping for final review.

Local environment: Linux, Python 3.12.15, torch 2.14.1+cpu, ONNX Runtime 1.31.0,
OpenVINO 2026.4.1. Only `CPU` was available to OpenVINO; no full-model NPU, Intel
Windows, GPU or live-video result is claimed. Historical Windows environment
snapshots are not new execution evidence. Exact installed versions are in
[the Linux snapshot](configs/environment-linux.snapshot.txt).

Browser verification on an isolated localhost test port was blocked by a saved
browser permission. No workaround was attempted. Streamlit AppTest verifies the
new UI and review controls; a live visual check of the new view remains a limitation.

## Release completion

Local final suite: **34 passed in 4.18s**, with two documented legacy ONNX-export deprecation warnings. This includes actual tiny artificial CPU training/export and optional OpenVINO CPU parity/unavailable-NPU checks. Documentation links (12 Markdown files), package consistency, source compilation, Ruff F/I and publication inventory checks passed.

The model was re-evaluated with the final editable installation and OpenVINO CPU numerical gate: maximum three-probe logit error 3.8147e-6. Final installed producer → LOVISA validation took 0.70s and left approval pending. Hosted CI/publication outcomes are appended after execution. No clinical report is automatically approved by release.
