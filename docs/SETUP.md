# Setup

[Overview](../README.md) · [Training](TRAINING.md) · [LOVISA](LOVISA.md)

Validated on Linux/Python 3.12 with CPU PyTorch and ONNX Runtime. The original
Windows 11/Core Ultra 7 155U environment snapshots remain historical preparation
records; the new full model has not been run on that Windows/NPU device here.
Hosted Windows Server CI now passes actual tiny artificial CPU training/export and UI checks. This is separate from the user's Intel NPU/driver. Do not assume a convolution smoke establishes full-model NPU compatibility.

## Environment

Linux: use the root README commands. On macOS, select a PyTorch build available
for that platform rather than the Linux/Windows CPU-wheel index. On Windows:

```powershell
py -3.12 -m venv .venv
.venv\Scripts\python.exe -m pip install torch==2.14.1+cpu --index-url https://download.pytorch.org/whl/cpu
.venv\Scripts\python.exe -m pip install -e ".[ml,ui,dev]"
.venv\Scripts\python.exe -m pip check
.venv\Scripts\python.exe -m streamlit run app.py --server.address=127.0.0.1 --server.port=8503
```

CPU training is supported; no NVIDIA device is required. Keep this environment
separate from LOVISA and the CT companion. `configs/environment-linux.snapshot.txt`
records the actual new environment, including optional OpenVINO. It is evidence,
not a portable Windows lock file. The package uses bounded dependency ranges;
inspect versions and `pip check` before changing an existing environment.

## Optional Intel acceleration

```bash
.venv/bin/python -m pip install -e '.[npu]'
.venv/bin/python -c "import openvino as ov; print(ov.Core().available_devices)"
```

First register an ONNX model using [Training](TRAINING.md). Select `openvino-cpu`
or `openvino-npu` explicitly. There is no silent NPU-to-CPU fallback. Missing
hardware, compilation failure or failed numerical parity stops inference. Start
with a fixed input shape and batch one. Compiled-model cache stays in the ignored
model directory; first compilation may be much slower than warm inference.

Run held-out evaluation again for the selected backend. Probe parity is not a
clinical accuracy result or a substitute for dataset evaluation. INT8 quantisation,
GPU training, full-model NPU results and real-time video are not validated here.
[OpenVINO NPU reference](https://docs.openvino.ai/2026/openvino-workflow/running-inference/inference-devices-and-modes/npu-device.html).

## Runtime scope

Bind Streamlit to loopback. The standalone app is an unauthenticated local
research tool, not a clinical records portal. LOVISA requires its own local login
and separate review approvals. No automatic public hosting, cloud inference,
telemetry service, model download or paid API is configured.

## Models, inputs and recoverable errors

The standalone UI prefers a registered `artifacts/kvasir-research-v2` directory
when present, otherwise the earlier `artifacts/kvasir-model`. LOVISA uses its own
matching discovery or `LOVISA_ENDO_MODEL_DIR`. A registration must agree with
checkpoint/graph/config bytes, contain at least three actual parity probes, and
have strict boolean/finite numerical evidence. Replacing a hash is not a repair;
re-export/register the actual model.

Public JPG/PNG input requires explicit research-use permission. A synthetic-only
model cannot process public research images. Missing model/backend and worker
startup errors stay visible; correct them and retry. Changing model/backend or
permission cancels old work and clears stale results/review controls. Keep training
and large experiments outside the interactive 110-second workflow.
