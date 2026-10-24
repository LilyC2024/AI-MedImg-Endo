# Code reference

[Overview](../README.md) · [Architecture](ARCHITECTURE.md)

| Folder/module | Main functions/classes and purpose |
| --- | --- |
| `src/endo_contracts/__init__.py` | `Study`, `Candidate`, `ModelInfo`, `Review`, `Bundle`; `regions` derives 4-connected masks/boxes; `read_exchange` validates bounded source and annotation bytes |
| `src/endo_contracts/worker.py` | `LocalJob`: subprocess progress, deadline, cancellation and no late publication |
| `src/endo/data.py` | `inventory`, `fingerprint`, `freeze`, `load_manifest`, `arrays`: validate, group, split, recheck and preprocess research sources |
| `src/endo/fixture.py` | `phantom`, `fixture_probability`: explicitly artificial sources and non-ML finder |
| `src/endo/model.py` | `UNetSmall`, `block`, `loss`: RGB-to-logit network and BCE/soft-Dice objective |
| `src/endo/train.py` | `train`: seeded CPU training, aligned flips, validation selection and artifact records |
| `src/endo/deploy.py` | `export`: weights-only loading, fixed-shape ONNX export and numerical parity registration |
| `src/endo/inference.py` | `load_registration`, `Predictor`: hash checks and explicit ONNX/OpenVINO runtime |
| `src/endo/evaluate.py` | `iou`, `score`, `evaluate`: source-resolution test metrics and latency evidence |
| `src/endo/exchange.py` | `make_study`, `export_bundle`: derive typed observations and pending synthetic/public exchange |
| `src/endo/workspace.py` | `create`, `verify`, `reviewed_report`: separate original bytes, derived artifacts and explicit research review |
| `src/endo/cli.py` | `main`: split, synthetic-data, train, export-model, evaluate, infer, demo and bridge commands |
| `app.py` | Source/overlay viewer, bounded local analysis and explicit region review |
| `tests/` | Artificial adversarial contracts/data, actual tiny CPU train/export and Streamlit/worker checks |
| `reports/` | Frozen research split metadata and measured evaluations; no patient images or weights |
| `configs/` | Historical Windows and actual Linux environment evidence |
| `artifacts/`, `data/` | Ignored models, study workspaces, cache and artificial datasets |

Public callables carry module/function docstrings. This index explains boundaries;
[Training](TRAINING.md), [Workflow](WORKFLOWS.md) and [Integration](LOVISA.md)
contain command-level details and measurement limitations.

## Research evidence extension

`endo_contracts.PublicResearchSource` and `Bundle.consistent` keep public-v2 and
synthetic-v1 distinct. `exchange.export_bundle(research=...)` exports verified
public predictions; `workspace.create(research=...)` checks original byte hashes
and preserves source/probability/provenance. `cli infer --research-provenance`
exposes this path. Shared `worker.LocalJob(input_files=...)` stages only bounded
basename inputs before launching the local process. No review is generated.

## Public API and subfunction navigation

[Callable inventory](reference/CALLABLES.md) lists exact source signatures and
nested helpers with code-line links. Use the contracts below when extending code:

| API | Input → output; failure behavior |
| --- | --- |
| `data.freeze` | Image/mask inventory → new hashed grouped split; existing output is not overwritten |
| `data.load_manifest` | Manifest/root → rehashed decoded sources and target metadata; traversal/group leakage/contradiction fails |
| `train.train` | Verified split/config → CPU model/training evidence; validation loss selects checkpoint |
| `deploy.export` | Actual trained artifacts → ONNX/registration after three numerical probes |
| `inference.load_registration` | Local model directory → verified hashes/strict parity/config; invalid metadata fails before model runtime |
| `Predictor.predict` | Source RGB → source-resolution probabilities and typed model evidence; explicit selected backend |
| `exchange.make_study` | RGB/probabilities/model → derived regions and typed study |
| `workspace.create` | Exact original bytes/decoded source/provenance → immutable workspace; mismatches fail before creation |
| `workspace.verify` | Workspace → checked study only after source/region/mask/overlay/provenance/ZIP agreement |
| `workspace.reviewed_report` | Verified workspace and exact resolved review → short research summary |
| `LocalJob` | Fixed subprocess and staged basename inputs → bounded lifecycle; cancellation prevents late publication |

Keep type/coordinate semantics in the shared contracts and all ML imports outside
that package. UI state invalidation is a presentation/lifecycle concern; it cannot
change model evidence or issue LOVISA acceptance. [Detailed repairs](REVIEW.md).
