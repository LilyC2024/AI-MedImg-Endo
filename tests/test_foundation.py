"""Software fixtures only: no clinical inference or real reviewer approvals."""

import io
import json
import zipfile

import numpy as np
import pytest
from PIL import Image

from endo.data import freeze, load_manifest
from endo.exchange import export_bundle, make_study
from endo.fixture import fixture_probability, phantom
from endo_contracts import ModelInfo, Review, digest, read_exchange, sha


def sample(*, positive=True):
    source, _ = phantom(3, 64, positive=positive)
    probability = fixture_probability(source)
    model = ModelInfo(
        name="synthetic-fixture",
        backend="fixture",
        checkpoint_sha256=sha(b"non-ML"),
        recipe_sha256=sha(b"fixture-v1"),
        threshold=0.5,
        min_area_px=8,
        evaluation_scope="software-fixture",
    )
    study, _ = make_study(
        source,
        probability,
        model,
        patient_alias="synthetic-test",
        study_id="endo-test",
        input_kind="generated-synthetic",
    )
    return study, source, probability


def rewrite(payload, edit):
    with zipfile.ZipFile(io.BytesIO(payload)) as archive:
        files = {name: archive.read(name) for name in archive.namelist()}
    edit(files)
    stream = io.BytesIO()
    with zipfile.ZipFile(stream, "w") as archive:
        for path, data in files.items():
            archive.writestr(path, data)
    return stream.getvalue()


@pytest.mark.parametrize("positive", [True, False])
def test_roundtrip_pending_source_and_mask(positive):
    study, source, p = sample(positive=positive)
    bundle, _, artifacts = read_exchange(
        export_bundle(study, source, p), "synthetic-test"
    )
    assert len(bundle.study.candidates) == len(study.candidates)
    assert len(artifacts) == 4
    assert not hasattr(bundle, "review")


def test_patient_mismatch():
    with pytest.raises(ValueError, match="patient"):
        read_exchange(export_bundle(*sample()), "other")


@pytest.mark.parametrize(
    "what",
    [
        "pixels",
        "extra",
        "traversal",
        "nonfinite",
        "candidate",
        "public",
        "date",
        "synthetic",
    ],
)
def test_tampering_fails_closed(what):
    payload = export_bundle(*sample())

    def edit(files):
        manifest = json.loads(files["bundle.json"])
        if what == "pixels":
            files["source.png"] = files["overlay.png"]
        if what == "extra":
            files["extra.txt"] = b"bad"
        if what == "traversal":
            manifest["artifacts"][0]["path"] = "../escape.png"
        if what == "nonfinite":
            manifest["study"]["model"]["threshold"] = float("nan")
        if what == "candidate":
            manifest["study"]["candidates"][0]["area_px"] += 1
        if what == "public":
            manifest["study"]["input_kind"] = "approved-public-research"
        if what == "date":
            manifest["acquisition_date"] = "2020-01-01"
        if what == "synthetic":
            manifest["synthetic"] = 1
        files["bundle.json"] = json.dumps(manifest).encode()

    with pytest.raises(ValueError):
        read_exchange(rewrite(payload, edit), "synthetic-test")


def test_overlay_rehash_still_fails_pixel_validation():
    payload = export_bundle(*sample())

    def edit(files):
        files["overlay.png"] = files["source.png"]
        m = json.loads(files["bundle.json"])
        a = next(a for a in m["artifacts"] if a["role"] == "overlay_preview")
        a.update(sha256=sha(files["overlay.png"]), size_bytes=len(files["overlay.png"]))
        files["bundle.json"] = json.dumps(m).encode()

    with pytest.raises(ValueError, match="Overlay"):
        read_exchange(rewrite(payload, edit), "synthetic-test")


def test_review_cannot_omit_duplicate_or_leave_uncertain():
    study, _, _ = sample()
    decisions = [
        {"candidate_id": c.candidate_id, "decision": "accept"} for c in study.candidates
    ]

    def review(ds):
        return Review(
            study_digest=digest(study),
            reviewer="scripted-test",
            attested=True,
            decisions=ds,
        )

    review(decisions).verify(study)
    for ds in (
        [],
        decisions + decisions,
        [{**d, "decision": "uncertain"} for d in decisions],
    ):
        with pytest.raises(ValueError):
            review(ds).verify(study)
    with pytest.raises(ValueError):
        Review(
            study_digest=digest(study), reviewer="test", attested=1, decisions=decisions
        )


def dataset(tmp_path):
    for d in ("images", "masks"):
        (tmp_path / d).mkdir()
    for i in range(12):
        rng = np.random.default_rng(i)
        Image.fromarray(rng.integers(0, 255, (32, 32, 3), dtype=np.uint8)).save(
            tmp_path / "images" / f"{i}.png"
        )
        Image.fromarray(np.full((32, 32), 255 if i % 2 else 0, dtype=np.uint8)).save(
            tmp_path / "masks" / f"{i}.png"
        )
    return tmp_path


def test_manifest_frozen_and_sources_rechecked(tmp_path):
    root = dataset(tmp_path)
    manifest = root / "split.json"
    body = freeze(root, manifest)
    assert len(load_manifest(manifest, root)["records"]) == 12
    assert {r["split"] for r in body["records"]} == {"train", "validation", "test"}
    with pytest.raises(FileExistsError):
        freeze(root, manifest)
    (root / "images/1.png").write_bytes(b"changed")
    with pytest.raises(ValueError, match="changed"):
        load_manifest(manifest, root)


def test_related_decoded_images_never_cross_splits(tmp_path):
    root = dataset(tmp_path)
    (root / "images/12.png").write_bytes((root / "images/1.png").read_bytes())
    (root / "masks/12.png").write_bytes((root / "masks/1.png").read_bytes())
    rows = freeze(root, root / "split.json")["records"]
    a = next(r for r in rows if r["image"] == "images/1.png")
    b = next(r for r in rows if r["image"] == "images/12.png")
    assert a["group"] == b["group"] and a["split"] == b["split"]


@pytest.mark.parametrize(
    "kind",
    [
        "huge-array",
        "nan-probability",
        "missing-source",
        "reserved-path",
        "json-duplicate",
    ],
)
def test_adversarial_artifacts_cannot_reach_allocation_or_acceptance(kind):
    from endo_contracts import array_bytes

    def edit(files):
        m = json.loads(files["bundle.json"])
        if kind == "huge-array":
            stream = io.BytesIO()
            np.lib.format.write_array_header_1_0(
                stream,
                {
                    "descr": "<f4",
                    "fortran_order": False,
                    "shape": (1000000000, 1000000000),
                },
            )
            files["probability.npy"] = stream.getvalue()
        elif kind == "nan-probability":
            files["probability.npy"] = array_bytes(
                np.full((64, 64), np.nan, np.float32)
            )
        elif kind == "missing-source":
            files.pop("source.png")
        elif kind == "reserved-path":
            m["artifacts"][0]["path"] = "source.mhcra.zip"
        elif kind == "json-duplicate":
            files["bundle.json"] = files["bundle.json"].replace(
                b'"synthetic": true', b'"synthetic": true, "synthetic": true'
            )
            return
        for a in m["artifacts"]:
            if a["path"] in files:
                a.update(sha256=sha(files[a["path"]]), size_bytes=len(files[a["path"]]))
        files["bundle.json"] = json.dumps(m).encode()

    with pytest.raises(ValueError):
        read_exchange(rewrite(export_bundle(*sample()), edit), "synthetic-test")


def test_original_source_bytes_and_prediction_are_separate_and_verified(tmp_path):
    from endo.workspace import create, verify

    study, source, p = sample()
    output = tmp_path / "study"
    create(
        source,
        p,
        study.model,
        output,
        patient_alias=study.patient_alias,
        study_id=study.study_id,
        input_kind=study.input_kind,
    )
    assert verify(output) == study
    provenance = json.loads((output / "provenance.json").read_text())
    provenance["artifacts"].pop("source.original")
    (output / "provenance.json").write_text(json.dumps(provenance))
    with pytest.raises(ValueError, match="provenance"):
        verify(output)


def test_split_manifest_uses_portable_relative_posix_paths(tmp_path):
    root = dataset(tmp_path)
    manifest = freeze(root, root / "split.json")
    assert all(
        "\\" not in row["image"] and "\\" not in row["mask"]
        for row in manifest["records"]
    )
    row = manifest["records"][0]
    row["image"] = row["image"].replace("/", "\\")
    manifest.pop("manifest_sha256")
    manifest["manifest_sha256"] = digest(manifest)
    (root / "split.json").write_text(json.dumps(manifest))
    with pytest.raises(ValueError, match="POSIX"):
        load_manifest(root / "split.json", root)
