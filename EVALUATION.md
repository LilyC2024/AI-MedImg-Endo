# Evaluation — image-first endoscopy research assistant

## Expert source review — 24 October 2026

The independent reviewer repaired provenance/ZIP association, frozen-source group/
target validation, ambiguous model-registration evidence and stale model/backend/
permission UI state. Shared wire contracts, dependencies, installed models and
research datasets were unchanged. [Defects and repairs](docs/REVIEW.md).

| Executed check | Actual outcome |
| --- | --- |
| Final full regression | **72 passed in 5.76s**, including 31 new runtime and four documentation regressions |
| Source-repair phase | 72 passed in 9.39s before documentation changes; applicable Ruff passed |
| Historical workspace compatibility | Artificial fixture and all three existing public kit workspaces verified unchanged, with 1 / 5 / 2 / 2 candidates |
| Actual original frozen-manifest reload | All 1,000 images verified in **14.732s**; same manifest identity/group split retained |
| Actual registered model, endoscopy-03 source | ONNX CPU **0.085s**, OpenVINO CPU **0.389s** for predictor setup/prediction; not full-workflow latency |
| Runtime OpenVINO CPU parity | Three actual probes; maximum absolute logit error **9.36×10⁻⁶** |
| LOVISA actual installed artificial producer/receiver | **0.91s**, one region, four artifacts, review pending |
| LOVISA real upload workflow | Endoscopy ZIP **0.51s** to results; actual raw JPG inference **2.74s**, two regions, no acceptance issued |
| Supporting checks | 17 maintained Markdown files/anchors, generated API freshness, compilation, pip consistency, applicable Ruff and publication inventory passed |

Two warnings are existing TorchScript ONNX-export deprecations. Automated tests
use artificial sources/scripted reviews; some genuinely train/export a tiny
artificial model and are labelled accordingly. Actual public-workspace and
registered-model checks above are separate and issue no clinician approval.

Original bytes, canonical pixels, provenance and exported ZIP must agree; older
workspaces without new hash fields undergo the same direct evidence comparison.
Unsigned local hashes still prove consistency, not authenticity or permission.
The existing 24-epoch Kvasir results below were not retrained or newly validated.
Patient independence, negative-examination performance and clinical validity remain
unproven. NPU hardware was unavailable and is not marked tested.

Root documentation is concise; linked guides explain schemas, functions, data,
training, deployment, review and LOVISA. The editable system sketch contains no
research image pixels. Publication/hosted outcomes are recorded after execution below.

## Public research-image extension — 23 October 2026

- Final local regression: **37 passed in 5.15s**, with two existing ONNX-export deprecation warnings.
- Actual Kvasir CPU repeat: 24 epochs, input 128×128/base8/batch8/seed42/four threads, same frozen 682/150/168 grouped split. Training took **365.949s** under concurrent CT load. Best validation loss **0.8189604**, epoch23; test pixels were not used for checkpoint selection.
- Actual ONNX export parity passed; maximum logit absolute error **4.76837158203125e-06** on three probes. Registered checkpoint `23012881743e29bb1d5a5f3afa5f38598749770491504ca58a86bdb24452e5cc`.
- Frozen positive test repeat: **168 images; Dice 0.5439824, IoU 0.4131187**; box-region recall/precision proxies 0.3869347/0.2150838. Median inference-plus-region extraction 0.2294s, p95 0.4379s. No negative examinations; no established patient independence. The test set had already been inspected in the initial baseline, so this is **exploratory**, not independent external validation. [Machine-readable results](reports/kvasir-research-v2-evaluation.json).
- Three fixed real test JPEGs (first three manifest test rows, not selected by accuracy) produced 5/2/2 candidate regions. The first is 1348×1070, requiring >4-MiB probability storage: research-v2 now has a bounded 64-MiB archive/expanded limit and 16-MiB-plus-header artifacts. Synthetic-v1 retains its original smaller limits.
- Actual first raw JPEG -> LOVISA local worker -> byte/pixel validator: **3.16s**, 5 candidates, 4 verified artifacts, all approvals pending. Dataset originals, masks, predictions and weights remain local and excluded from Git.
- Combined real CT/endoscopy + actual local `gemma4:e2b` report smoke passed in **34.32s**, with four embedded evidence images and a 170-word report. Reviews were **scripted only in a disposable database**, never clinical approval in the actual app.

CT imagery belongs to LIDC-IDRI-0002; Kvasir subject identity is unknown. The LOVISA history is fictional, and no cross-subject diagnosis is inferred. New public exports require separate research-v2 provenance and a fictional composite alias. Source/checkpoint hashes prove consistency, not inference authenticity or clinical validity. Real NPU execution and external clinical validation remain unperformed.

Hosted checks exposed cwd-dependent first-party import classification. An explicit Ruff first-party package setting and canonical imports fix the Linux/Windows lint mismatch without changing inference. Local full suite was rerun; hosted outcomes follow.

The sections below record earlier releases and their then-current scope.

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

Local final suite: **35 passed in 4.22s**, with two documented legacy ONNX-export deprecation warnings. This includes actual tiny artificial CPU training/export and optional OpenVINO CPU parity/unavailable-NPU checks. Documentation links (12 Markdown files), package consistency, source compilation, Ruff F/I and publication inventory checks passed.

The model was re-evaluated with the final editable installation and OpenVINO CPU numerical gate: maximum three-probe logit error 3.8147e-6. Final installed producer → LOVISA validation took 0.70s and left approval pending. Hosted CI/publication outcomes are recorded below. No clinical report is automatically approved by release.

Initial hosted Linux checks passed. The first Windows run found platform-native backslashes in generated split manifests. The loader/writer now require canonical relative POSIX paths, with a cross-platform regression. The frozen Linux research split and model/checkpoint results are unchanged. Windows verification is rerun before release completion.


### Hosted verification and publication completed

[Hosted run 40002316931](https://github.com/LilyC2024/AI-MedImg-Endo/actions/runs/40002316931)
passed Linux and Windows checks on source `bff92c23dd9e2679d38a7dcd4274b1cb5035a35f`.
Each hosted environment passed 34 tests and skipped the optional OpenVINO test
because that extra is not installed there; the local environment passed all 35.
The Windows result includes actual tiny artificial CPU training, ONNX export,
Streamlit and worker checks, not Intel NPU hardware validation. The initial
Windows path failure is fixed; no test or validation was removed to hide it.

[LOVISA hosted run 40002402873](https://github.com/LilyC2024/Medical-AI/actions/runs/40002402873)
passed Python 3.10/3.12 regressions plus actual artificial endoscopy fixture and
trained-model producer/receiver checks, alongside all retained CT integrations.
Local trees were synchronized with published source. Final documentation-only
commits do not alter the tested implementation or frozen experiment artifacts.

## Final public-research publication checks

Tested producer `81ff9f53a0baa9b40ff396283ef1dd9f430bf170` passed its [hosted workflow](https://github.com/LilyC2024/AI-MedImg-Endo/actions/runs/40015138472). Both Linux and Windows jobs passed after the explicit import-classification fix; OpenVINO remains an optional local check. The follow-up changes in this section and PLAN.md are documentation only. No datasets, weights, accounts or generated research-image reports were published.
