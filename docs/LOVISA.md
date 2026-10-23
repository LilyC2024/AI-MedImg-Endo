# Connect endoscopy to LOVISA

[Overview](../README.md) · [Workflow](WORKFLOWS.md) · [Architecture](ARCHITECTURE.md)

LOVISA provides one patient workspace with separate history, CT and endoscopy
views. The endoscopy companion runs image inference in its own Python environment.
LOVISA accepts only generated-synthetic image evidence, never public research
patient images. Model training/evaluation data remain in this standalone project.

## Produce a pending artificial study

```bash
.venv/bin/python -m endo.cli bridge --patient-id synthetic-checklist --study-id endo-example --output artifacts/bridge-example
```

Output: `artifacts/bridge-example/bundle.endo.zip`. No approvals are supplied.
Add `--model-dir artifacts/kvasir-model --backend onnx-cpu` for actual installed
model inference on the artificial source. The default is an explicitly non-ML
fixture, never a fallback for failed inference. Use a fresh study/output each run.

LOVISA discovers the sibling `AI-MedImg-Endo/.venv`. Otherwise configure
`LOVISA_ENDO_ROOT`, `LOVISA_ENDO_MODEL_DIR` and `LOVISA_ENDO_BACKEND` outside the
review UI. Choose Endoscopy review, inspect candidates, resolve all decisions,
add a note, attest inspection, then include the study. Complete safety and final
clinical review separately. [Receiver guide](https://github.com/LilyC2024/Medical-AI/blob/main/docs/ENDOSCOPY.md).

## Contract

`endo_contracts` is ML-free and copied exactly into LOVISA; a sync check detects
drift. `lovisa-endo-image-v1` contains `bundle.json` and four artifacts: source RGB
PNG, float32 probability NPY, binary mask PNG and annotation PNG. Receiver checks
safe ZIP paths, exact members/byte limits/hashes, source pixels, derived connected
regions, mask and overlay. No source is inferred from a screenshot alone.

The bundle binds synthetic patient/study aliases, unknown acquisition date,
processing timestamp, model/checkpoint/recipe provenance and typed candidate
regions. Endoscopy uses RGB pixels and half-open `xyxy` coordinates; it does not
reuse CT HU, voxel spacing, three-dimensional boxes or millimetre calipers.

Review decisions bind the exact study digest and authenticated reviewer. Uncertain,
missing or duplicate decisions block acceptance. Accepted source artifacts are
immutable. Final report approval covers both CT and endoscopy content; changing
a source, review or image invalidates export. Hashes prove consistency, not
independent synthetic origin, producer authenticity or diagnostic truth.

## Agent and LLM responsibilities

The Endoscopy Agent is LOVISA's explicit `LocalEndoscopyJob` CV adapter, launched
by the image-review action. It is not an extra LLM or an autonomous tool user.
The existing LangGraph orchestrator still coordinates history, medication,
reasoning and Python safety specialists. Only bounded history reasoning calls
local Ollama. Accepted endoscopy evidence is composed deterministically after
reasoning; images, scores and imaging notes do not enter the LLM or expand its
hypothesis catalog. No cloud inference or remote model API is used.
