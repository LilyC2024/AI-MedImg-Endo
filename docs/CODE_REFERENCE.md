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
| `src/endo/exchange.py` | `make_study`, `export_bundle`: derive typed observations and pending synthetic exchange |
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
