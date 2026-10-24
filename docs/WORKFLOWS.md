# Analyze, inspect and review one image

[Overview](../README.md) · [Setup](SETUP.md) · [LOVISA transfer](LOVISA.md)

## Standalone UI

1. Start the loopback interface and select an artificial example or explicitly
   permitted public research image. Upload one JPG/PNG, 16–2048 pixels per side,
   at most 16 MiB; animated/multiframe sources are rejected.
2. Select the installed model directory and backend. Fixture mode is explicitly
   non-ML and cannot be used to relabel real research images as synthetic.
3. Attest research permission when required and start analysis. The worker reports
   progress, supports cancellation and stops at its 110-second deadline.
4. Inspect source and candidate overlay. Resolve every region as accept/reject;
   uncertainty blocks completion. Optional commentary is not a new source fact.
5. Supply the actual local reviewer identifier and explicit review attestation,
   then submit. Download the research summary only after evidence verification.

Changing model, backend or permission invalidates prior UI analysis/review state.
Startup/processing errors remain visible; correct the cause and retry. A local
reviewer name is an attestation, not verified clinician identity.

## Command-line paths

```bash
# Non-ML generated pixels; leaves review pending
.venv/bin/python -m endo.cli demo --output artifacts/demo
# Real installed inference; standalone research workspace
.venv/bin/python -m endo.cli infer --image /absolute/path/research.jpg --model-dir artifacts/kvasir-research-v2 --output artifacts/research-study --research-use-attested
# Artificial pending exchange bound to the LOVISA alias
.venv/bin/python -m endo.cli bridge --patient-id synthetic-checklist --study-id endo-example --output artifacts/bridge-example
```

Use a fresh output directory for every study. The optional public-provenance JSON
and a `research-composite-` alias enable a public research ZIP; without it a public
image remains a standalone workspace. [Provenance fields and command](LOVISA.md).
No command fabricates a reviewer decision or changes clinical records.

## Workspace contents

| File | Responsibility |
| --- | --- |
| `source.original` | Exact original encoded bytes |
| `source.png` | Canonical source-grid RGB, not an enhanced or annotated source |
| `probability.npy` | Float32 predicted probabilities at source resolution |
| `mask.png`, `overlay.png` | Deterministic threshold/region-derived annotations |
| `study.json` | Typed candidates, aliases, model and source identity |
| `provenance.json` | Source/study/artifact hashes and optional research/ZIP identity |
| `research.json` | Explicit public dataset/license/subject declaration when supplied |
| `bundle.endo.zip` | Pending exchange, only for eligible synthetic/public-composite studies |
| Review JSON | Separate explicit local review; does not overwrite predictions |

Before review/export, original bytes must decode to the canonical source; predicted
mask, regions and overlay must reconstruct exactly; public provenance and bundle
must match the same evidence. Incorrect input fails before reserving a workspace
where possible. A blank/failed result never establishes a normal examination.

## LOVISA UI

Use **Endoscopy review → Upload → Analyze**. Review ZIPs open existing results;
permitted research-kit JPG/PNG files run the installed model. Include the inspected
study, complete safety, then generate and separately approve the clinical report.
Adding imaging after report preparation starts a fresh unreviewed context; saved
reports stay intact. [Receiver operating guide](https://github.com/LilyC2024/Medical-AI/blob/main/docs/ENDOSCOPY.md).
