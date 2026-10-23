# Architecture and data structures

[Overview](../README.md) · [Code reference](CODE_REFERENCE.md) · [LOVISA](LOVISA.md)

## Separation of concerns

| Layer | Responsibility |
| --- | --- |
| `endo_contracts` | Strict ML-free studies, candidate regions, review decisions, ZIP/pixel validation and bounded worker lifecycle |
| `endo.data` | Paired image/mask inventory, near-duplicate groups, immutable hashed split manifests |
| `endo.model` / `train` | Compact U-Net and offline CPU optimisation with validation-only checkpoint selection |
| `endo.deploy` / `inference` | Registered ONNX artifacts, explicit local backend, CPU/OpenVINO numerical checks |
| `endo.evaluate` | Held-out overlap, box-region proxies, negative-image false alarms and timings |
| `endo.workspace` / `exchange` | Original bytes, decoded sources, predictions and human review kept separate |
| `endo.cli` / `app.py` | Explicit commands and source-first Streamlit interface |
| LOVISA receiver | Patient-scoped storage, authenticated image acceptance, safety and clinical report approval |

## Core structures

`Study` binds source RGB pixel digest, width/height, input kind, unknown acquisition
date, patient/study aliases and model provenance. Each `Candidate` stores an ID,
half-open `(x0,y0,x1,y1)` box, predicted mask area in pixels and mean model score.
Candidate regions are recomputed from the actual probability array; they are not
invented by a language model or copied from dataset labels during inference.

`Review` refers to the exact study digest and contains one explicit decision per
candidate. Uncertain blocks completion. `Bundle` admits only generated-synthetic
input and exact artifacts. Original encoded research-image bytes are preserved in
standalone workspaces with hashes; decoded RGB and predictions are separate.
LOVISA archives original bundles and stores accepted snapshots/audit in SQLite.

## Agents versus models

U-Net performs computer vision; ONNX/OpenVINO execute that model locally. The
Endoscopy Agent is a bounded adapter in LOVISA that launches the companion. The
LangGraph orchestrator coordinates four existing specialist classes/nodes, of
which only clinical reasoning uses Ollama. Source extraction and safety remain
Python. A composed imaging paragraph is a reviewed observation, not new LLM
clinical reasoning. No image-model score becomes a diagnosis or medication order.

## Limits and trust

The standalone application is a loopback research workbench. LOVISA remains a
synthetic-only prototype. Archive hashes and reconstruction checks detect internal
tampering but do not authenticate the machine that produced them. Local operating
system/filesystem administrators are trusted. No model can approve its own output,
modify clinical facts, lower Python safety escalation or approve a final report.
