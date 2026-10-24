"""Regression checks for offline provenance, split leakage and stale UI settings."""

import json
from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest
from test_foundation import dataset, sample

from endo.data import freeze, load_manifest
from endo.workspace import create, verify
from endo_contracts import Study, digest, png, sha


def workspace(tmp_path, *, public=False):
    study, source, probability = sample()
    research = None
    if public:
        value = study.model_dump()
        value.update(
            patient_alias="research-composite-test",
            input_kind="approved-public-research",
        )
        value["model"].update(
            name="UNetSmall",
            backend="onnx-cpu",
            evaluation_scope="positive-images-only",
        )
        study = Study.model_validate(value)
        research = {
            "dataset": "manufactured-test-image",
            "source_url": "https://example.org/research",
            "license": "manufactured-test-only",
            "research_subject_id": "unrelated-test-subject",
            "original_sha256": sha(png(source)),
            "composite_case": True,
        }
    output = tmp_path / "workspace"
    create(
        source,
        probability,
        study.model,
        output,
        patient_alias=study.patient_alias,
        study_id=study.study_id,
        input_kind=study.input_kind,
        research=research,
    )
    return output, study


@pytest.mark.parametrize("public", [False, True])
def test_historical_workspaces_remain_verifiable(tmp_path, public):
    output, study = workspace(tmp_path, public=public)
    provenance = json.loads((output / "provenance.json").read_text())
    provenance.pop("research_sha256")
    provenance.pop("bundle_sha256")
    (output / "provenance.json").write_text(json.dumps(provenance))
    assert verify(output) == study


@pytest.mark.parametrize("mutation", ["changed", "missing", "symlink"])
def test_public_workspace_provenance_is_bound_to_export(tmp_path, mutation):
    output, _ = workspace(tmp_path, public=True)
    file = output / "research.json"
    if mutation == "changed":
        research = json.loads(file.read_text())
        research["research_subject_id"] = "wrong-source"
        file.write_text(json.dumps(research))
    elif mutation == "missing":
        file.unlink()
    else:
        replacement = tmp_path / "research.json"
        replacement.write_bytes(file.read_bytes())
        file.unlink()
        try:
            file.symlink_to(replacement)
        except OSError:
            pytest.skip("Symlink creation unavailable on this platform")
    with pytest.raises(ValueError, match="provenance"):
        verify(output)


@pytest.mark.parametrize("public", [False, True])
@pytest.mark.parametrize("mutation", ["changed", "missing"])
def test_export_download_cannot_diverge_from_verified_workspace(
    tmp_path, public, mutation
):
    output, _ = workspace(tmp_path, public=public)
    file = output / "bundle.endo.zip"
    if mutation == "changed":
        file.write_bytes(b"invalid or substituted exported result")
    else:
        file.unlink()
    with pytest.raises(ValueError, match="bundle"):
        verify(output)


def test_original_byte_mismatch_leaves_no_partial_workspace(tmp_path):
    study, source, probability = sample()
    other_source = source.copy()
    other_source[0, 0] = [0, 0, 0]
    output = tmp_path / "not-created"
    with pytest.raises(ValueError, match="Original"):
        create(
            source,
            probability,
            study.model,
            output,
            patient_alias=study.patient_alias,
            study_id=study.study_id,
            input_kind=study.input_kind,
            original_bytes=png(other_source),
        )
    assert not output.exists()


def rewrite_manifest(file, body):
    body.pop("manifest_sha256")
    body["manifest_sha256"] = digest(body)
    file.write_text(json.dumps(body))


def test_rehashed_manifest_cannot_put_identical_pixels_in_a_new_test_group(tmp_path):
    root = dataset(tmp_path)
    manifest = root / "split.json"
    body = freeze(root, manifest)
    original = body["records"][0]
    duplicate = dict(original)
    duplicate.update(image="images/duplicate.png", mask="masks/duplicate.png")
    (root / duplicate["image"]).write_bytes((root / original["image"]).read_bytes())
    (root / duplicate["mask"]).write_bytes((root / original["mask"]).read_bytes())
    duplicate.update(
        group="new-group", split="test" if original["split"] != "test" else "train"
    )
    body["records"].append(duplicate)
    rewrite_manifest(manifest, body)
    with pytest.raises(ValueError, match="Related-image content"):
        load_manifest(manifest, root)


@pytest.mark.parametrize(
    "metadata", ["decoded_sha256", "dhash", "positive", "foreground_fraction"]
)
def test_rehashed_manifest_metadata_must_match_actual_pixels_and_masks(
    tmp_path, metadata
):
    root = dataset(tmp_path)
    manifest = root / "split.json"
    body = freeze(root, manifest)
    row = body["records"][0]
    row[metadata] = {
        "decoded_sha256": "0" * 64,
        "dhash": "0" * 16,
        "positive": not row["positive"],
        "foreground_fraction": 0.25,
    }[metadata]
    rewrite_manifest(manifest, body)
    with pytest.raises(ValueError, match="identity/fingerprint|Target metadata"):
        load_manifest(manifest, root)


@pytest.mark.parametrize(
    "path", ["images/../images/0.png", "images\\0.png", "/outside.png", "C:outside.png"]
)
def test_rehashed_manifest_rejects_noncanonical_paths(tmp_path, path):
    root = dataset(tmp_path)
    manifest = root / "split.json"
    body = freeze(root, manifest)
    body["records"][0]["image"] = path
    rewrite_manifest(manifest, body)
    with pytest.raises(ValueError, match="relative POSIX"):
        load_manifest(manifest, root)


@pytest.mark.parametrize("setting", ["model", "backend"])
def test_model_or_backend_change_cancels_and_hides_stale_result(setting):
    class Job:
        cancelled = False

        def status(self):
            return "running"

        def cancel(self):
            self.cancelled = True

    app = AppTest.from_file(str(Path(__file__).resolve().parents[1] / "app.py")).run()
    job = Job()
    app.session_state.job = job
    app.session_state.workspace = "old-model-result"
    app.session_state.reviewed_summary = {"report": "old-model-review"}
    if setting == "model":
        next(
            t for t in app.text_input if t.label == "Installed model directory"
        ).set_value("other-model").run()
    else:
        next(s for s in app.selectbox if s.label == "Local execution").set_value(
            "openvino-cpu"
        ).run()
    assert job.cancelled and "workspace" not in app.session_state
    assert "reviewed_summary" not in app.session_state
    assert not app.exception and not app.image


def test_worker_startup_errors_remain_visible_and_retryable(monkeypatch):
    def fail(*args, **kwargs):
        raise OSError("scripted local launch failure")

    monkeypatch.setattr("endo_contracts.worker.LocalJob", fail)
    app = AppTest.from_file(str(Path(__file__).resolve().parents[1] / "app.py")).run()
    next(b for b in app.button if b.label == "Analyze image").click().run()
    assert not app.exception
    assert any("scripted local launch failure" in e.value for e in app.error)
    assert not next(b for b in app.button if b.label == "Analyze image").disabled
