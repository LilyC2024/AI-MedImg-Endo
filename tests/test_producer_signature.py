"""Producer signatures and model-bound false-positive claims; artificial data only."""

import json

import pytest
from test_foundation import rewrite, sample

from endo.evaluate import declared_performance
from endo.exchange import export_bundle
from endo_contracts import read_exchange
from endo_contracts.producer_signature import (
    NOT_MEASURED,
    SIGNATURE_ENTRY,
    check_archive,
    generate_key,
)


@pytest.fixture
def key(tmp_path):
    path = tmp_path / "endo.key"
    info = generate_key(path)
    return path, {info["key_id"]: dict(info, producer="lovisa-endo", label="test endo")}


def evaluation(tmp_path, onnx="a" * 64, precision=0.25, negatives=0):
    path = tmp_path / "evaluation.json"
    path.write_text(
        json.dumps(
            {
                "schema_version": "endo-evaluation-v1",
                "model_onnx_sha256": onnx,
                "partition": "test",
                "model_config_sha256": "c" * 64,
                "backend": "onnx-cpu",
                "images": 40,
                "negative_images": negatives,
                "box_region_precision_proxy": precision,
                "patient_independence": "not-established",
            }
        )
    )
    return path


def test_signed_bundle_carries_verified_model_bound_false_positive_rate(tmp_path, key):
    path, trusted = key
    performance = declared_performance({"onnx_sha256": "a" * 64, "config_sha256": "c" * 64}, evaluation(tmp_path))
    payload = export_bundle(*sample(), signing_key=path, performance=performance)
    read_exchange(payload, "synthetic-test")
    check = check_archive(payload, trusted)
    assert check.status == "verified" and check.producer == "lovisa-endo"
    assert check.performance.false_positive_fraction == pytest.approx(0.75)
    assert check.performance.test_images == 40
    assert "no negative images" in check.performance.limitations


def test_evaluation_of_another_model_is_rejected_and_absence_is_unmeasured(tmp_path):
    with pytest.raises(ValueError, match="different model"):
        declared_performance({"onnx_sha256": "b" * 64, "config_sha256": "c" * 64}, evaluation(tmp_path))
    assert declared_performance({"onnx_sha256": "a" * 64, "config_sha256": "c" * 64}, None) == NOT_MEASURED
    unmeasurable = evaluation(tmp_path, precision=None)
    assert declared_performance({"onnx_sha256": "a" * 64, "config_sha256": "c" * 64}, unmeasurable) == NOT_MEASURED


def test_unsigned_default_and_unlisted_extra_entry_still_fail_closed(tmp_path, key):
    payload = export_bundle(*sample())
    assert check_archive(payload, key[1]).status == "unsigned"
    signed = export_bundle(*sample(), signing_key=key[0])

    def extra(files):
        files["notes.txt"] = b"unlisted"

    with pytest.raises(ValueError):
        read_exchange(rewrite(signed, extra), "synthetic-test")

    def drop(files):
        files.pop(SIGNATURE_ENTRY)

    assert check_archive(rewrite(signed, drop), key[1]).status == "unsigned"


@pytest.mark.parametrize("change", [{"backend": "openvino-npu"}, {"partition": "train"}, {"model_config_sha256": "d"*64}, {"negative_images": 41}, {"box_region_precision_proxy": True}])
def test_performance_mismatches_fail_closed(tmp_path, change):
    path = evaluation(tmp_path)
    body = json.loads(path.read_text())
    body.update(change)
    path.write_text(json.dumps(body))
    with pytest.raises(ValueError):
        declared_performance({"onnx_sha256": "a"*64, "config_sha256": "c"*64}, path)
