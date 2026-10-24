# Evaluation artifacts

[Actual results](../EVALUATION.md) · [Reproduction](../docs/TRAINING.md)

`kvasir-split-v1.json` freezes related-image groups and source hashes for 1,000
paired images (682 training, 150 validation, 168 test). It contains dataset
filenames/metadata, not image pixels, patient identifiers or masks. Patient
independence is unknown.

`kvasir-test-v1.json` and `kvasir-openvino-cpu-v1.json` record actual CPU test
predictions/metrics, separately from `synthetic-test-v2.json` (artificial data).
Model/checkpoint hashes and environment versions bind the experiment. This is
exploratory single-dataset research; no negative-examination, external, NPU or
clinical performance is established. Weights and workspaces remain ignored.

`kvasir-research-v2-evaluation.json` records the later 24-epoch repeat on the same
already-viewed test split (positive Dice 0.544, IoU 0.413). It is an exploratory
repeat, not a new independent benchmark. Current code-review tests and actual
workspace/registration checks are documented in [Review](../docs/REVIEW.md) and
[EVALUATION](../EVALUATION.md); they do not replace the dataset evaluation.

Before adding evidence, state input, model/config/manifest identities, backend,
timing scope, truth limitations and whether reviews were scripted. Commit permitted
aggregate metadata only, never real pixels, clinician decisions or model weights.
