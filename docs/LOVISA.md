# Connect endoscopy to LOVISA

[Overview](../README.md) · [Workflow](WORKFLOWS.md) · [Architecture](ARCHITECTURE.md)

LOVISA provides one patient workspace with separate history, CT and endoscopy
views. The endoscopy companion runs image inference in its own Python environment.
LOVISA accepts artificial-v1 or separately labelled public-research-v2 evidence.
Public images require a fictional `research-composite-` case and explicit
dataset/license/source provenance. Their research subjects are unrelated to the
fictional history and other imaging modalities. Clinical records remain unsupported.

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
review UI. Choose **Endoscopy review → Upload → Analyze**, then inspect candidates and resolve all decisions,
optionally add a note, retain the selected inspection confirmation, then explicitly include the study. Complete safety and final
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

## Export a permitted public image

Create a provenance JSON with `dataset`, HTTPS `source_url`, `license`,
`research_subject_id` (say unknown when only an image identifier is known),
`original_sha256` of the actual JPEG/PNG bytes and `composite_case: true`.
Then use the registered real-data model, never fixture/synthetic-only weights:

```bash
.venv/bin/python -m endo.cli infer --image /absolute/path/research.jpg --research-use-attested --research-provenance /absolute/path/provenance.json --model-dir artifacts/kvasir-research-v2 --patient-id research-composite-demo --study-id research-endo-01 --output artifacts/research-endo-01
```

The workspace preserves original bytes, canonical pixels and model predictions
separately and verifies their hashes before export. `bundle.endo.zip` is pending,
not a human-reviewed result. Research-v2 permits up to 2048 pixels per side and
keeps the same exact four derived artifacts/bounded probability reconstruction.
The consumer cannot verify original JPEG bytes absent from its canonical PNG
bundle; provenance is an operator declaration, not independent authentication.

In LOVISA, the fixed research kit recognises the exact three supplied Kvasir JPGs
for local re-analysis. Opening a prepared bundle avoids repeat inference. Notes
can be blank; candidate uncertainty still blocks inclusion. Clinical/safety/final
review rules remain independent of imaging. [Prepare files and terms](https://github.com/LilyC2024/Medical-AI/blob/main/docs/RESEARCH_IMAGES.md).

Research-v2 allows a bounded 64-MiB archive/expanded size and up to 16 MiB plus NPY header per artifact, supporting real large-image probability maps. Synthetic-v1 retains its original 16-MiB total and 4-MiB artifact limits.

## Receiver workflow and compatibility table

| Input | Analyze behavior | Required review |
| --- | --- | --- |
| Synthetic-v1 review ZIP | Independently validate included source and predictions | Every region, then authenticated image inclusion |
| Public-research-v2 ZIP | Validate public provenance and exact source-derived annotations in a fictional composite | Same image inclusion; no producer approval substitutes |
| One of LOVISA's exact prepared research JPG/PNG files | Run installed local model on those bytes; preserve dataset provenance | Inspect new regions and explicitly include |
| Arbitrary unprovenanced real image | Rejected by LOVISA; prepare a permitted standalone research workspace with provenance | No automatic relabelling |

ZIP analysis opens existing results, not fresh inference. Model/example selection
applies only without an upload. Uploads take precedence over generated examples.
Adding valid imaging after a clinical case starts releases the old active context;
new image inclusion and safety review precede another draft. Saved reports remain
unchanged. Invalid uploads keep the old context and show the actual bounded error.

Workspace verification now checks the exported ZIP against the same typed study,
provenance and source/mask/probability/overlay bytes. Old workspaces without the
additional provenance/ZIP hash fields still require these direct comparisons.
Exact shared-schema sync remains mandatory; no wire-format migration occurred in
the expert review. [Verification](VALIDATION.md) · [Repairs](REVIEW.md).

## Optional signed export

Generate a new private key (never commit it):

```bash
.venv/bin/python -m endo.cli keygen --output /private/local-exporter.key
```

Pin the returned public key in LOVISA using
`python -m medical_assistant.producer_trust --producer lovisa-endo --public-key <public_key_b64> --label <name>`.
Keys require a trusted local identity check. Add `--signing-key /private/local-exporter.key`
to the companion export/infer command, or set `LOVISA_SIGNING_KEY_FILE`. A private
PEM must have owner-only POSIX permissions. No private key is sent to LOVISA.

The shared module bounds archives, rejects ambiguous paths/JSON and binds all
manifest-listed artifact hashes. Signed proof identifies the exporter, not clinical
accuracy. Unknown signed keys are blocked by LOVISA; unsigned older examples stay
compatible unless its trust settings require signatures. Existing schema versions
are retained. See [branch review](BRANCH_REVIEW.md).

Evaluation claims require explicit `--evaluation path/to/evaluation.json`; they
must match the ONNX model, configuration, inference backend and test partition.
Older evaluation files without configuration identity must be regenerated to
attach metrics; omitting the flag preserves normal inference/export as unmeasured.
The signed unmatched-candidate fraction is a producer-declared precision proxy,
not screening specificity, histology or a cancer probability.
