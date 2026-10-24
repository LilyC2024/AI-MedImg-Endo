"""Actual small CPU training/export tests use artificial pixels, not clinical data."""

import numpy as np
import pytest
from PIL import Image

from endo.data import freeze
from endo.deploy import export
from endo.evaluate import evaluate, score
from endo.fixture import phantom
from endo.inference import Predictor
from endo.train import train
from endo_contracts import regions


@pytest.fixture(scope="module")
def trained(tmp_path_factory):
    root = tmp_path_factory.mktemp("training")
    data = root / "data"
    for d in ("images", "masks"):
        (data / d).mkdir(parents=True)
    for i in range(20):
        source, mask = phantom(i, 64, positive=i % 3 != 0)
        Image.fromarray(source).save(data / "images" / f"{i}.png")
        Image.fromarray(mask).save(data / "masks" / f"{i}.png")
    manifest = root / "split.json"
    freeze(data, manifest, near_distance=0)
    model = root / "model"
    result = train(
        data, manifest, model, epochs=1, size=64, base=4, threads=1, synthetic=True
    )
    registration = export(model)
    return data, manifest, model, result, registration


def test_actual_cpu_training_and_export_parity(trained):
    data, manifest, model, result, registration = trained
    assert not result["test_used_for_selection"]
    assert (
        registration["onnx_parity_passed"]
        and registration["max_logit_absolute_error"] < 1e-4
    )
    predictor = Predictor(model)
    p, info = predictor.predict(phantom(7, 64)[0])
    assert p.shape == (64, 64) and np.isfinite(p).all()
    assert info.evaluation_scope == "synthetic-only"
    report = evaluate(model, data, manifest, model / "evaluation.json")
    assert report["images"] > 0 and report["partition"] == "test"


def test_changed_registered_weights_rejected(trained, tmp_path):
    import shutil

    model = tmp_path / "copy"
    shutil.copytree(trained[2], model)
    (model / "model.onnx").write_bytes(b"changed")
    with pytest.raises(ValueError, match="changed"):
        Predictor(model)


def test_backend_and_input_fail_without_silent_fallback(trained):
    with pytest.raises(ValueError):
        Predictor(trained[2], backend="cloud")
    predictor = Predictor(trained[2])
    with pytest.raises(ValueError):
        predictor.predict(np.zeros((64, 64), np.uint8))


def test_metrics_separate_negative_false_alarms_from_overlap():
    target = np.zeros((32, 32), np.uint8)
    p = np.zeros((32, 32), np.float32)
    p[8:16, 8:16] = 0.9
    mask, cs = regions(p, 0.5, 1)
    r = score(mask, target, cs)
    assert r["dice"] == 0 and r["candidate_count"] == 1 and not r["positive"]
    assert r["fp_proxy"] == 1


def test_optional_openvino_cpu_parity_and_npu_absence(trained):
    ov = pytest.importorskip("openvino")
    predictor = Predictor(trained[2], backend="openvino-cpu")
    assert predictor.backend_parity["probes"] == 3
    p, _ = predictor.predict(phantom(7, 64)[0])
    assert np.isfinite(p).all()
    if "NPU" not in ov.Core().available_devices:
        with pytest.raises(ValueError, match="unavailable"):
            Predictor(trained[2], backend="openvino-npu")


@pytest.mark.parametrize("artifact", ["model.pt", "config.json"])
def test_registration_rejects_changed_checkpoint_or_config(trained, tmp_path, artifact):
    import shutil

    from endo.inference import load_registration

    model = tmp_path / "copy"
    shutil.copytree(trained[2], model)
    (model / artifact).write_bytes(b"{}" if artifact.endswith("json") else b"changed")
    with pytest.raises(ValueError, match="changed|mismatch"):
        load_registration(model)


@pytest.mark.parametrize(
    "change",
    [
        {"onnx_parity_passed": "false"},
        {"onnx_parity_passed": 1},
        {"parity_probe_count": 0},
        {"max_logit_absolute_error": float("nan")},
    ],
)
def test_registration_requires_explicit_finite_parity_evidence(
    trained, tmp_path, change
):
    import json
    import shutil

    from endo.inference import load_registration

    model = tmp_path / "copy"
    shutil.copytree(trained[2], model)
    file = model / "registration.json"
    registration = json.loads(file.read_text())
    registration.update(change)
    file.write_text(json.dumps(registration))
    with pytest.raises(ValueError, match="parity"):
        load_registration(model)


@pytest.mark.parametrize(
    "change", [{"size": 64.0}, {"threshold": 1.1}, {"min_area_px": 0}]
)
def test_registered_invalid_postprocessing_fails_before_runtime_load(
    trained, tmp_path, change
):
    import json
    import shutil

    from endo.inference import load_registration
    from endo_contracts import digest

    model = tmp_path / "copy"
    shutil.copytree(trained[2], model)
    config_file = model / "config.json"
    config = json.loads(config_file.read_text())
    config.update(change)
    config_file.write_text(json.dumps(config))
    registration_file = model / "registration.json"
    registration = json.loads(registration_file.read_text())
    registration["config_sha256"] = digest(config)
    registration_file.write_text(json.dumps(registration))
    with pytest.raises(ValueError):
        load_registration(model)
