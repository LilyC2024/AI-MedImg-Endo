# Kvasir-SEG data card

[Overview](../README.md) · [Training](TRAINING.md) · [Measured outcomes](../EVALUATION.md)

Source: [Simula Kvasir-SEG](https://datasets.simula.no/kvasir-seg/).
Publisher terms permit research/education; commercial use requires permission.
Dataset pixels are not committed, and this repository grants no dataset rights.

The downloaded archive has 46,227,172 bytes, SHA-256
`03b30e21d584e04facf49397a2576738fd626815771afbbf788f74a7153478f7`.
This identifies the local copy; it was not compared with a publisher checksum.
Use an explicit `--data /absolute/path/Kvasir-SEG` directory containing `images/`
and `masks/`. No hardcoded personal directory or runtime download is required.

## Structure and split

There are 1,000 positive-image/mask pairs. Manifest preparation checks files,
decoded pixels, matching dimensions, mask values and content hashes. Masks are
thresholded at 128. Exact decoded duplicates and dHash Hamming distance <=4
are grouped before partitioning. The frozen split has 933 related-image groups:
682 training images, 150 validation and 168 test. Patient identities and patient
independence are **not established** by this grouping.

The data contain no negative examinations. Segmentation overlap therefore cannot
establish screening specificity or missed-polyp rates. Connected mask regions
are not adjudicated lesion identities; pixel area is not millimetre size or
histology. Acquisition date and anatomical segment are not inferred.

## Current use

The 24-epoch CPU repeat selects its checkpoint using validation loss. Its already
examined test split is exploratory, not independent validation: mean Dice 0.544,
IoU 0.413 on 168 positives. No new test-set tuning or best-image display selection
is used. The LOVISA kit uses the first three frozen test-manifest rows, retaining
original bytes, reference masks and predictions separately.

LOVISA's patient history is fictional. Its Kvasir subject is recorded as unknown
with the public source image identifier; its CT comes from a different dataset
subject. Research-v2 provenance never asserts that these are one real patient.

## Reload and audit guarantees

A frozen manifest is both hashed and rechecked against local source content.
Canonical relative POSIX paths cannot escape through traversal or symlinks.
Decoded RGB/dHash and mask-derived positive/foreground fractions are recomputed;
related images cannot be separated by relabelling groups and rehashing the JSON.
All train/validation/test partitions must remain present. The stronger checker
verified the original 1,000-image frozen manifest without changing its identity.

These are data-engineering consistency checks. Permission, completeness of labels,
patient identity and external independence remain separate research responsibilities.
The 2026-10-24 review added no source images, test-set tuning or model promotion.
