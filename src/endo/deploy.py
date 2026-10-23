"""Export local state dictionaries; register only after actual CPU numerical parity."""

import json
from pathlib import Path

import numpy as np
import onnxruntime as ort
import torch

from endo.model import UNetSmall
from endo_contracts import digest, sha


def export(directory):
    """Export a fixed-shape ONNX graph and register hashes after actual CPU parity."""
    directory = Path(directory)
    config = json.loads((directory / "config.json").read_text())
    training = json.loads((directory / "training.json").read_text())
    if training["config_sha256"] != digest(config) or training[
        "checkpoint_sha256"
    ] != sha((directory / "model.pt").read_bytes()):
        raise ValueError("Training artifacts changed")
    model = UNetSmall(config["base"])
    model.load_state_dict(
        torch.load(directory / "model.pt", map_location="cpu", weights_only=True)
    )
    model.eval()
    torch.set_num_threads(2)
    size = config["size"]
    rng = np.random.default_rng(177)
    probes = [
        np.zeros((1, 3, size, size), np.float32),
        np.ones((1, 3, size, size), np.float32),
        rng.random((1, 3, size, size), dtype=np.float32),
    ]
    torch.onnx.export(
        model,
        torch.from_numpy(probes[0]),
        str(directory / "model.onnx"),
        input_names=["image"],
        output_names=["logits"],
        opset_version=18,
        dynamo=False,
    )
    options = ort.SessionOptions()
    options.intra_op_num_threads = 2
    session = ort.InferenceSession(
        str(directory / "model.onnx"),
        sess_options=options,
        providers=["CPUExecutionProvider"],
    )
    errors = []
    with torch.inference_mode():
        for value in probes:
            expected = model(torch.from_numpy(value)).numpy()
            actual = session.run(None, {"image": value})[0]
            errors.append(float(np.max(np.abs(expected - actual))))
            if not np.allclose(actual, expected, atol=1e-4, rtol=1e-4):
                raise ValueError("ONNX CPU numerical parity failed")
    registration = {
        "schema_version": "endo-model-v1",
        "checkpoint_sha256": training["checkpoint_sha256"],
        "onnx_sha256": sha((directory / "model.onnx").read_bytes()),
        "config_sha256": digest(config),
        "onnx_parity_passed": True,
        "max_logit_absolute_error": max(errors),
        "parity_probe_count": len(probes),
        "torch_version": torch.__version__,
        "onnxruntime_version": ort.__version__,
    }
    (directory / "registration.json").write_text(json.dumps(registration, indent=2))
    return registration
