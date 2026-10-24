# Training and evaluation

[Overview](../README.md) · [Data card](data_card.md) · [Actual evaluation](../EVALUATION.md)

## Prepare public research data

Read the publisher's [current terms](https://datasets.simula.no/kvasir-seg/)
before acquisition. Keep the official Kvasir-SEG archive and extracted data outside
Git. Expected layout is `DATA/images/` and `DATA/masks/`, with matching stems.
The recorded archive SHA-256 is in the data card; it is not a publisher-issued
checksum. No training or inference command automatically downloads data.

```bash
.venv/bin/python -m endo.cli split --data /absolute/path/Kvasir-SEG --output reports/my-split.json
```

The command rejects missing pairs/duplicate stems, validates masks and dimensions,
groups identical decoded images and related dHash images, and writes a manifest
with source hashes, seed and train/validation/test assignments. It never overwrites
an existing manifest. Related groups remain within one split. dHash is a heuristic,
not proof of patient independence; this release has no patient identifiers.

Masks are grayscale >=128; resizing uses nearest-neighbor interpolation. RGB
images are divided by 255 and resized bilinearly. Keep spatial transforms aligned.
Aligned random horizontal flips apply to training only. No training augmentation
is applied before splitting. The test set never selects checkpoints/thresholds.

To include reviewed negative research images, place them under `DATA/negatives/`
and add `--negative-dir /absolute/path/DATA/negatives` to `split`. Their supplied
negative status is an operator assumption, not a model finding. They receive empty
masks. Confirm negatives in every evaluation partition; the split is grouped,
not guaranteed class-stratified. Source files are rehashed before use. Reload also checks canonical relative
paths, exact decoded hashes/dHash, dimensions and actual mask-derived positive/
foreground metadata. Related decoded content cannot cross declared groups or
partitions even if someone recalculates the manifest hash after editing it.
These checks do not establish patient independence.

## Reproduce the initial baseline

```bash
.venv/bin/python -m endo.cli train --data /absolute/path/Kvasir-SEG --manifest reports/kvasir-split-v1.json --output artifacts/kvasir-model --epochs 12 --size 128 --base 8 --threads 4
.venv/bin/python -m endo.cli export-model --model-dir artifacts/kvasir-model
.venv/bin/python -m endo.cli evaluate --model-dir artifacts/kvasir-model --data /absolute/path/Kvasir-SEG --manifest reports/kvasir-split-v1.json --output artifacts/kvasir-model/test-evaluation.json
```

Use a fresh output directory. Defaults remain the planned 256×256/base-16 model;
the measured first baseline uses 128×128/base-8 to fit CPU development. U-Net has
three encoder levels, a bottleneck, skip connections and raw binary logits. Loss
is BCE-with-logits plus soft Dice; Adam uses 0.001. Lowest validation loss selects
the checkpoint. Fixed threshold 0.5/minimum connected area 8 pixels were set before
evaluation. Training is offline and is not subject to the UI's 110-second budget.

Registration binds checkpoint, configuration and ONNX hashes after three actual
PyTorch/ONNX CPU comparisons (`atol=rtol=1e-4`); it does not certify accuracy.
PyTorch state dictionaries load with `weights_only=True`. Inference accepts only
installed registered artifacts. No automatic model download/fallback occurs.

Evaluation uses the frozen test partition at source-image resolution. Report mean
positive Dice/IoU separately from false candidates per negative image. Box matches
at IoU >=0.5 against connected ground-truth mask regions are **proxies**, not
clinically adjudicated lesion detection. Kvasir has no negative examinations;
that false-alarm metric is therefore null, not zero. Test results are exploratory,
not patient-independent or external validation. Do not tune on this test set.

## Artificial software demonstration

```bash
.venv/bin/python -m endo.cli synthetic-data --output data/synthetic --count 80 --size 64
.venv/bin/python -m endo.cli split --data data/synthetic --output data/synthetic-split.json
.venv/bin/python -m endo.cli train --data data/synthetic --manifest data/synthetic-split.json --output artifacts/synthetic-model-v2 --epochs 40 --size 64 --base 8 --threads 2 --synthetic
.venv/bin/python -m endo.cli export-model --model-dir artifacts/synthetic-model-v2
```

These are simple coloured phantoms, not simulated clinical accuracy evidence.
Synthetic-only weights must not be presented as a trained clinical polyp detector.

## Next evaluation gate

Add permitted negative images and independent multi-centre research data, such as
[PolypGen](https://www.nature.com/articles/s41597-023-01981-y), after checking terms
and duplicate overlap. Where IDs exist, group by patient/procedure; otherwise keep
centre/video independence explicit and do not claim patient independence. Reserve
external data before experiments. Publish negative-image false alarms and
small/flat-region failure examples alongside overlap metrics. This release does
not include or claim those results.

## 24-epoch real-data repeat

Use the same frozen Kvasir split and commands above with
`--output artifacts/kvasir-research-v2 --epochs 24 --size 128 --base 8 --threads 4`.
Export before inference/evaluation. The checkpoint is selected by validation loss;
the previously examined test partition is exploratory, not an independent external
benchmark. Current repeat: Dice 0.544, IoU 0.413 on 168 positives, no negatives.
[Full measured outcomes](../EVALUATION.md). Never tune on or advertise the three
fixed display examples as an accuracy benchmark.

## Artifact and parameter contract

| Output | Purpose |
| --- | --- |
| `config.json` | Architecture, image size, base width, seed, training recipe, threshold and frozen-manifest identity |
| `model.pt` | Validation-selected tensor state dictionary |
| `training.json` | Epoch losses/timing, configuration and checkpoint hashes |
| `model.onnx` | Fixed `[1,3,size,size]` input, binary logits; opset 18 |
| `registration.json` | Graph/checkpoint/config identities and actual CPU parity evidence |
| Evaluation JSON | Test manifest/model/backend identities, individual results and aggregate metrics |

The Python training API additionally bounds batch size 1–32 and thread count 1–16.
Source identity/group verification reads all referenced files; optimizer updates
and checkpoint selection use only the training/validation partitions. RGB resizing
is bilinear, mask resizing nearest-neighbor, and predictions are returned to source
resolution for evaluation. Test data never choose thresholds/checkpoints.

Hash/shape/parity registration checks are validated before runtime initialization.
Ambiguous strings such as `"false"`, missing probes and nonfinite configuration
values fail closed. Existing registered models are reused; this code review did
not retrain a model or change its recorded research results.
