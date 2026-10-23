"""Immutable source/prediction workspaces and explicit separate research review."""

import json
from pathlib import Path

from endo.exchange import export_bundle, make_study
from endo_contracts import LIMITATION, Review, digest, overlay_pixels, png, sha


def create(
    source,
    p,
    model,
    output,
    *,
    patient_alias,
    study_id,
    input_kind,
    original_bytes=None,
):
    """Persist original bytes, decoded source and immutable predictions separately."""
    study, mask = make_study(
        source,
        p,
        model,
        patient_alias=patient_alias,
        study_id=study_id,
        input_kind=input_kind,
    )
    output = Path(output)
    output.mkdir(parents=True, exist_ok=False)
    (output / "study.json").write_text(study.model_dump_json(indent=2))
    import numpy as np

    np.save(output / "probability.npy", p, allow_pickle=False)
    (output / "source.png").write_bytes(png(source))
    (output / "mask.png").write_bytes(png(mask))
    (output / "overlay.png").write_bytes(
        png(overlay_pixels(source, mask, study.candidates))
    )
    original = (
        original_bytes
        if original_bytes is not None
        else (output / "source.png").read_bytes()
    )
    (output / "source.original").write_bytes(original)
    provenance = {
        "original_file_sha256": sha(original),
        "canonical_source_sha256": study.source_sha256,
        "study_digest": digest(study),
        "artifacts": {
            name: sha((output / name).read_bytes())
            for name in (
                "source.png",
                "source.original",
                "probability.npy",
                "mask.png",
                "overlay.png",
            )
        },
    }
    (output / "provenance.json").write_text(json.dumps(provenance, indent=2))
    if input_kind == "generated-synthetic":
        (output / "bundle.endo.zip").write_bytes(export_bundle(study, source, p))
    return study


def verify(output):
    """Recheck original-source association and every derived workspace annotation."""
    import numpy as np
    from PIL import Image

    from endo_contracts import Study

    output = Path(output)
    study = Study.model_validate_json((output / "study.json").read_text())
    provenance = json.loads((output / "provenance.json").read_text())
    if provenance["study_digest"] != digest(study):
        raise ValueError("Study changed")
    expected = {
        "source.png",
        "source.original",
        "probability.npy",
        "mask.png",
        "overlay.png",
    }
    if (
        set(provenance["artifacts"]) != expected
        or provenance["original_file_sha256"]
        != provenance["artifacts"]["source.original"]
        or provenance["canonical_source_sha256"] != study.source_sha256
    ):
        raise ValueError("Missing or conflicting source provenance")
    for name, value in provenance["artifacts"].items():
        if (
            name
            not in (
                "source.png",
                "source.original",
                "probability.npy",
                "mask.png",
                "overlay.png",
            )
            or (output / name).is_symlink()
            or sha((output / name).read_bytes()) != value
        ):
            raise ValueError("Workspace artifact changed")
    with Image.open(output / "source.png") as image:
        source = np.array(image)
    with Image.open(output / "source.original") as original:
        if not np.array_equal(np.array(original.convert("RGB")), source):
            raise ValueError("Original file does not match decoded source")
    from endo_contracts import _probability

    p = _probability(
        (output / "probability.npy").read_bytes(), (study.height, study.width)
    )
    checked, mask = make_study(
        source,
        p,
        study.model,
        patient_alias=study.patient_alias,
        study_id=study.study_id,
        input_kind=study.input_kind,
    )
    if (
        checked != study
        or (output / "mask.png").read_bytes() != png(mask)
        or (output / "overlay.png").read_bytes()
        != png(overlay_pixels(source, mask, study.candidates))
    ):
        raise ValueError("Derived annotations changed")
    return study


def reviewed_report(output, review):
    """Compose a short research summary only for a complete matching human review."""
    study = verify(output)
    review = Review.model_validate(review)
    review.verify(study)
    accepted = sum(d.decision == "accept" for d in review.decisions)
    return f"# Endoscopy research summary\n\n{len(study.candidates)} candidate region(s) proposed; {accepted} accepted and {len(study.candidates) - accepted} rejected on review. Reviewed areas are in source-image pixels; physical size, histology and anatomical location are unavailable.\n\n{LIMITATION}\n\nStudy evidence: {digest(study)}\nReview evidence: {digest(review)}\n"
