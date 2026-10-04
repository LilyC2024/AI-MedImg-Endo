# Endoscopy Polyp Segmentation

A research prototype for polyp segmentation in endoscopic images,
with reproducible training, ONNX export, and CPU/NPU deployment validation.

This project is under development. It is not intended for clinical use.
Polyp segmentation does not establish cancer diagnosis or performance
on examinations without polyps.

## Current Status

Completed:
- Windows development environment setup.
- PyTorch CPU forward/backward smoke test.
- Kvasir-SEG download and structural validation.
- Mask-value and exact decoded-image duplicate checks.
- OpenVINO CPU/NPU convolution smoke test.

Not yet completed:
- Similar-image analysis and a frozen dataset split.
- Segmentation model training and held-out evaluation.
- Full-model ONNX export and CPU/NPU parity testing.
- Latency benchmarking and an inference service.

## Planned Baseline

- Model: compact 2D U-Net, base channels 16.
- Input: RGB images, initially 256 x 256.
- Target: binary polyp mask.
- Loss: BCE with logits plus Dice loss.
- Training: PyTorch on CPU.
- Deployment: ONNX Runtime CPU and OpenVINO CPU/NPU.
- NPU inference: fixed input shape, batch size 1.

These choices will be confirmed through compatibility and runtime tests.

## Repository Layout

| Directory | Purpose |
| --- | --- |
| src/endo | Dataset, model, training, and inference modules |
| scripts | Command-line entry points |
| configs | Reproducible configurations |
| docs | Data, architecture, evaluation, and deployment documentation |
| tests | Tests for critical behavior |
| reports | Evaluation and benchmark evidence |
| artifacts | Local generated models; excluded from Git |

## Data

Kvasir-SEG is stored outside this repository.
See [the data card](docs/data_card.md) for acquisition details,
validation results, and limitations.

## Development Environment

Initial validation used:
- Windows 11 Pro, build 26200.
- Intel Core Ultra 7 155U; approximately 32 GB RAM.
- Intel AI Boost NPU, driver 32.0.100.5540.
- Python 3.12.1.
- PyTorch 2.14.1+cpu.
- OpenVINO 2026.3.1.

Training and inference use separate Python environments.
A successful small-model NPU test does not establish full U-Net support.

## Reproducibility

Runnable commands will be added after implementation and verification.
Reports must identify the dataset split, configuration, model checkpoint,
software versions, and execution device.
