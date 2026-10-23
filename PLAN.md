# Image-first polyp research assistant

Complete and test each phase before starting the next. Real-world clinical use,
malignancy classification and calibrated millimetre measurement are out of scope.

1. **Foundation** — strict source/candidate/review structures, RGB/mask/overlay
   exchange validation, synthetic fixtures, dataset inventory, near-duplicate
   grouping and immutable train/validation/test manifest. Status: in progress.
2. **Model/deployment** — compact U-Net, CPU training, held-out evaluation,
   registered local checkpoints, ONNX CPU parity, optional OpenVINO CPU/NPU,
   runnable CLI and standalone image UI. Status: passed — 26 tests; actual artificial CPU training/export/parity and UI checks.
3. **LOVISA** — synthetic-only bridge, human review, report/evidence integration,
   source binding, local watchdog, patient isolation and regression checks.
   Status: passed — 227 LOVISA tests; actual fixture and installed-model exchanges, with approvals pending.
4. **Release** — actual training/inference evidence, honest limitations, full
   tests, docs and CI, publication in both repositories. Local checks passed: 34 companion/231 LOVISA tests, actual Kvasir training/evaluation, CPU/ONNX/OpenVINO parity and producer-consumer smokes. Publication/hosted CI pending.
