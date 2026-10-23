# Image workflow

[Overview](../README.md) · [Training](TRAINING.md) · [LOVISA](LOVISA.md)

## Standalone interface

Launch Streamlit using the README commands. Select an artificial example or
explicitly permitted public research image. The original bytes and decoded RGB
source remain separate from predictions. Supported input: one JPEG/PNG, 16–2048
pixels per side, at most 16 MiB. Animated/multiframe/oversized images are rejected.

Artificial fixture mode requires no model. Public research mode requires a local
registered model and explicit permission attestation. Inspect source and amber
candidate outlines; model scores are not cancer probabilities. Regions use source
pixels and image-area percentages, not physical size or anatomical segment.

Resolve every candidate. The research-review form defaults to uncertain, requires
a reviewer name and explicit attestation, and writes a new review JSON without
overwriting predictions or earlier reviews. Download the concise research summary.
This local name/attestation is not verified professional identity.

## CLI

```bash
# Non-ML artificial demonstration; no automatic review
.venv/bin/python -m endo.cli demo --output artifacts/demo
# Actual installed inference, preserving the original research image
.venv/bin/python -m endo.cli infer --image /absolute/path/research-image.jpg --model-dir artifacts/kvasir-model --output artifacts/research-study --research-use-attested
```

Output contains immutable `study.json`, original/source/prediction artifacts and
provenance hashes. Pixel findings come from the model, never ground-truth masks.
Only generated-synthetic studies receive a LOVISA exchange ZIP. Public research
images cannot be relabelled as artificial through the CLI.

LOVISA has its own authenticated image review and independent final clinician
approval. A standalone research review cannot approve a LOVISA report. The worker
shows progress immediately, supports cancellation and stops after 110 seconds.
Training, evaluation and arbitrary-size image batches are separate offline jobs.
