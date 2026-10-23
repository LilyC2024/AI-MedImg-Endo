# Data Card: Kvasir-SEG

## Source

- Dataset page: https://datasets.simula.no/kvasir-seg/
- Download: https://datasets.simula.no/downloads/kvasir-seg.zip
- Downloaded archive size: 46,227,172 bytes.
- Archive SHA-256:
  03b30e21d584e04facf49397a2576738fd626815771afbbf788f74a7153478f7

The hash identifies the downloaded archive. It has not been compared
against a publisher-provided checksum.

Read the publisher's current terms before use or redistribution.
This repository does not grant rights to the dataset.
Dataset files are not committed to Git.

## Local Storage

Relative to the parent medical-ai working directory:

datasets/kvasir-seg/Kvasir-SEG/
- images/
- masks/

Future commands will accept a configurable dataset path.

## Initial Validation

- Images: 1,000.
- Masks: 1,000.
- Missing image/mask pairs: 0.
- Unreadable pairs or spatial-size mismatches: 0.
- Unique mask grayscale values: 19.
- Mask grayscale range: 0 to 255.
- Empty masks at threshold 128: 0.
- Full-foreground masks at threshold 128: 0.
- Foreground fraction, minimum/median/maximum:
  0.0047 / 0.1140 / 0.8118.
- Exact decoded-RGB image duplicate groups: 0.

Validation was performed locally during environment preparation.
A reusable validation script and machine-readable report are pending.

## Label Processing

The initial binary target is grayscale >= 128.
Masks must use nearest-neighbor interpolation for resizing.
Image and mask spatial transformations must remain aligned.

## Split Policy

No train/validation/test split has been frozen.

Before splitting:
- Check visually similar images and potential related frames.
- Keep identified related images in the same split.
- Record the split in a versioned manifest.
- Reserve the test split from model and threshold selection.

Patient independence has not been established. An image-level split
must not be described as a patient-independent evaluation.

## Limitations

This dataset supports polyp segmentation experiments.
It does not by itself establish malignancy diagnosis, screening
specificity, or performance on negative examinations.
Exact duplicate checking does not exclude near-duplicate leakage.

## Implemented image-first release — 23 October 2026

The earlier preparation notes above remain historical. This release adds reusable
inventory/split commands, a frozen near-duplicate-grouped manifest, actual CPU
training and test evaluation. The retrieved official archive matched the recorded
hash. New split: 933 heuristic groups; 682 training/150 validation/168 test images.
Patient independence remains unestablished and real negative-examination coverage
remains absent. Source hashes are rechecked by the loader; mask interpolation
remains nearest-neighbor. [Commands](TRAINING.md) · [Actual evidence](../EVALUATION.md).
