# Image-first polyp research assistant

Complete and test each phase before starting the next. Real-world clinical use,
malignancy classification and calibrated millimetre measurement are out of scope.

1. **Foundation** — strict source/candidate/review structures, RGB/mask/overlay
   exchange validation, synthetic fixtures, dataset inventory, near-duplicate
   grouping and immutable train/validation/test manifest. Status: passed — 15 foundation tests before inference implementation.
2. **Model/deployment** — compact U-Net, CPU training, held-out evaluation,
   registered local checkpoints, ONNX CPU parity, optional OpenVINO CPU/NPU,
   runnable CLI and standalone image UI. Status: passed — 26 tests; actual artificial CPU training/export/parity and UI checks.
3. **LOVISA** — synthetic-only bridge, human review, report/evidence integration,
   source binding, local watchdog, patient isolation and regression checks.
   Status: passed — 227 LOVISA tests; actual fixture and installed-model exchanges, with approvals pending.
4. **Release** — actual training/inference evidence, honest limitations, full
   tests, docs and CI, publication in both repositories. Local checks passed: 35 companion/231 LOVISA tests, actual Kvasir training/evaluation, CPU/ONNX/OpenVINO parity and producer-consumer smokes. Complete: both repositories published; Linux/Windows standalone CI and LOVISA Python 3.10/3.12 plus actual endoscopy/CT integration jobs passed. See EVALUATION.md.

## Public research exchange

Extend synthetic-v1 with separate research-v2 evidence and original-byte provenance;
public RGB inference exports only to explicitly fictional composite cases, without
issuing human approval. Re-run actual Kvasir training/evaluation as an exploratory
repeat, preserve frozen groups and state that the previously viewed test set is
not an independent prospective validation.

Status: implemented and tested locally — 37 endoscopy tests, actual 24-epoch real-image CPU training and 168-image evaluation. Hosted checks passed: https://github.com/LilyC2024/AI-MedImg-Endo/actions/runs/40015138472. Compatible LOVISA receiver is published; final receiver checks follow.

## Systematic three-project review — 24 October 2026

5. **Review/repair** — expert source audit, reproduced defects, focused regressions
   and full suite before documentation changes. Status: passed — 72 tests in 9.39s,
   actual historical workspace/model/split checks and focused Ruff passed.
6. **Documentation** — concise root README and detailed linked architecture/data/
   training/operation/API/security guides, aligned with LOVISA. Status: passed —
   17 documents/anchors and generated API references checked; specialist audit
   corrected an overstated test-coverage phrase.
7. **Joint release** — actual local inference/producer-consumer checks, evidence,
   explicitly synchronized contracts and tested publication. Status: complete — 72 local tests, actual registered model/workspace/data
   checks and receiver transfers passed. Source published as 9391192; hosted
   40099084727 passed Linux/Windows. No new clinical/NPU validation claimed.

## Claude branch integration — current review

8. **Branch/runtime foundation** — inspect every remote branch, adopt useful signed
   exchange and quality checks with adversarial regression repairs; preserve
   unsigned legacy evidence and synchronize shared signature code with LOVISA/CT.
   Status: passed; no inherited branch test claim is treated as a current result.
9. **Documentation and release preparation** — explain licensing, AI coding-agent
   self-audits, signed versus trusted evidence and actual validation, then regenerate
   source references and run full checks. Status: pending phase 8.
