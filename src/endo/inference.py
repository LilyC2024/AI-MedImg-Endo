"""Local installed-model inference; no network/download/fallback or untrusted pickle."""

import json
from pathlib import Path

import numpy as np
from PIL import Image

from endo_contracts import ModelInfo, digest, sha


def load_registration(directory):
    """Reject mismatched local weights, graph or configuration before inference."""
    directory = Path(directory)
    info = json.loads((directory / "registration.json").read_text())
    config = json.loads((directory / "config.json").read_text())
    if info.get("schema_version") != "endo-model-v1" or info["config_sha256"] != digest(
        config
    ):
        raise ValueError("Model registration/config mismatch")
    for file, key in (("model.pt", "checkpoint_sha256"), ("model.onnx", "onnx_sha256")):
        path = directory / file
        if path.is_symlink() or sha(path.read_bytes()) != info[key]:
            raise ValueError("Registered model artifact changed")
    if not info.get("onnx_parity_passed"):
        raise ValueError("ONNX parity validation required")
    if (
        config.get("model") != "UNetSmall"
        or config.get("size") not in (64, 128, 256, 512)
        or config.get("base") not in (4, 8, 16)
    ):
        raise ValueError("Unsupported registered model configuration")
    return info, config


class Predictor:
    def __init__(self, directory, backend="onnx-cpu", threads=2):
        """Initialise the explicit local model or bounded worker without remote fallback."""
        if (
            backend not in ("onnx-cpu", "openvino-cpu", "openvino-npu")
            or not 1 <= threads <= 16
        ):
            raise ValueError("Unsupported explicit inference backend/threads")
        self.directory = Path(directory)
        self.info, self.config = load_registration(directory)
        self.backend = backend
        if backend == "onnx-cpu":
            import onnxruntime as ort

            options = ort.SessionOptions()
            options.intra_op_num_threads = threads
            options.inter_op_num_threads = 1
            self.session = ort.InferenceSession(
                str(self.directory / "model.onnx"),
                sess_options=options,
                providers=["CPUExecutionProvider"],
            )
        else:
            import openvino as ov

            core = ov.Core()
            device = "NPU" if backend == "openvino-npu" else "CPU"
            if device not in core.available_devices:
                raise ValueError(f"{device} is unavailable; select CPU explicitly")
            properties = {"CACHE_DIR": str(self.directory / "ov-cache")}
            if device == "CPU":
                properties["INFERENCE_PRECISION_HINT"] = "f32"
            self.session = core.compile_model(
                str(self.directory / "model.onnx"), device, properties
            )
            # Reject numerical drift before returning any image finding; never silently fallback.
            import onnxruntime as ort

            options = ort.SessionOptions()
            options.intra_op_num_threads = threads
            reference = ort.InferenceSession(
                str(self.directory / "model.onnx"),
                sess_options=options,
                providers=["CPUExecutionProvider"],
            )
            size = self.config["size"]
            probes = [
                np.zeros((1, 3, size, size), np.float32),
                np.ones((1, 3, size, size), np.float32),
                np.random.default_rng(177).random((1, 3, size, size), dtype=np.float32),
            ]
            errors = []
            for x in probes:
                expected = reference.run(None, {"image": x})[0]
                actual = self.session(x)[self.session.output(0)]
                errors.append(float(np.max(np.abs(actual - expected))))
                if not np.allclose(actual, expected, atol=1e-3, rtol=1e-3):
                    raise ValueError(
                        "OpenVINO numerical parity failed; no result is accepted"
                    )
            self.backend_parity = {
                "probes": len(probes),
                "max_absolute_logit_error": max(errors),
                "rtol": 1e-3,
                "atol": 1e-3,
                "openvino_version": ov.__version__,
            }

    def predict(self, source):
        """Return a source-resolution prediction map and declared local model provenance."""
        if (
            source.dtype != np.uint8
            or source.ndim != 3
            or source.shape[2] != 3
            or not 16 <= min(source.shape[:2]) <= max(source.shape[:2]) <= 2048
        ):
            raise ValueError("Expected RGB image, 16–2048 pixels per side")
        size = self.config["size"]
        x = (
            np.asarray(
                Image.fromarray(source).resize((size, size), Image.Resampling.BILINEAR),
                dtype=np.float32,
            ).transpose(2, 0, 1)[None]
            / 255
        )
        if self.backend == "onnx-cpu":
            logits = self.session.run(None, {"image": x})[0]
        else:
            logits = self.session(x)[self.session.output(0)]
        if logits.shape != (1, 1, size, size) or not np.isfinite(logits).all():
            raise ValueError("Invalid model output")
        p = (1 / (1 + np.exp(-np.clip(logits[0, 0], -80, 80)))).astype(np.float32)
        p = np.array(
            Image.fromarray(p).resize(
                (source.shape[1], source.shape[0]), Image.Resampling.BILINEAR
            ),
            dtype=np.float32,
        )
        return p, ModelInfo(
            name="UNetSmall",
            backend=self.backend,
            checkpoint_sha256=self.info["checkpoint_sha256"],
            recipe_sha256=digest(self.config),
            threshold=self.config["threshold"],
            min_area_px=self.config["min_area_px"],
            evaluation_scope=self.config["evaluation_scope"],
        )
