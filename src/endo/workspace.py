"""Immutable source/prediction workspaces and explicit separate research review."""

import io
import json
from pathlib import Path

import numpy as np
from PIL import Image

from endo.exchange import export_bundle, make_study
from endo_contracts import (
    LIMITATION,
    PublicResearchSource,
    Review,
    Study,
    _probability,
    digest,
    overlay_pixels,
    png,
    read_exchange,
    sha,
)


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
    research=None,
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
    canonical_source = png(source)
    original = original_bytes if original_bytes is not None else canonical_source
    # Reject inconsistent sources/provenance before creating a partial workspace.
    with Image.open(io.BytesIO(original)) as image:
        if (
            image.format not in ("PNG", "JPEG")
            or image.size != (study.width, study.height)
            or getattr(image, "n_frames", 1) != 1
            or not np.array_equal(np.array(image.convert("RGB")), source)
        ):
            raise ValueError("Original file does not match decoded source")
    if research is not None:
        research = PublicResearchSource.model_validate(research)
        if research.original_sha256 != sha(original):
            raise ValueError("Research provenance does not match original image bytes")
    bundle = (
        export_bundle(study, source, p, research=research)
        if input_kind == "generated-synthetic" or research is not None
        else None
    )
    output = Path(output)
    output.mkdir(parents=True, exist_ok=False)
    (output / "study.json").write_text(study.model_dump_json(indent=2))
    np.save(output / "probability.npy", p, allow_pickle=False)
    (output / "source.png").write_bytes(canonical_source)
    (output / "mask.png").write_bytes(png(mask))
    (output / "overlay.png").write_bytes(
        png(overlay_pixels(source, mask, study.candidates))
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
    # Explicit null distinguishes a standalone public workspace from a lost sidecar.
    provenance["research_sha256"] = digest(research) if research is not None else None
    provenance["bundle_sha256"] = sha(bundle) if bundle is not None else None
    (output / "provenance.json").write_text(json.dumps(provenance, indent=2))
    if research is not None:
        (output / "research.json").write_text(research.model_dump_json(indent=2))
    if bundle is not None:
        (output / "bundle.endo.zip").write_bytes(bundle)
    return study


def verify(output):
    """Recheck original-source association and every derived workspace annotation."""
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
    research_path = output / "research.json"
    research = None
    if research_path.exists():
        if research_path.is_symlink():
            raise ValueError("Research provenance must be a regular local file")
        research = PublicResearchSource.model_validate_json(research_path.read_text())
        if (
            study.input_kind != "approved-public-research"
            or research.original_sha256 != provenance["original_file_sha256"]
        ):
            raise ValueError("Research provenance does not match original image")
    if "research_sha256" in provenance and provenance["research_sha256"] != (
        digest(research) if research is not None else None
    ):
        raise ValueError("Research provenance changed or is missing")
    bundle_path = output / "bundle.endo.zip"
    requires_bundle = study.input_kind == "generated-synthetic" or research is not None
    if requires_bundle or bundle_path.exists() or provenance.get("bundle_sha256"):
        if bundle_path.is_symlink() or not bundle_path.is_file():
            raise ValueError("Exported bundle changed or is missing")
        payload = bundle_path.read_bytes()
        if "bundle_sha256" in provenance and provenance["bundle_sha256"] != sha(
            payload
        ):
            raise ValueError("Exported bundle changed")
        bundle, _, artifacts = read_exchange(payload, study.patient_alias)
        if (
            bundle.study != study
            or bundle.research != research
            or any(
                artifacts[a.path] != (output / a.path).read_bytes()
                for a in bundle.artifacts
            )
        ):
            raise ValueError("Exported bundle does not match workspace evidence")
    return study


def reviewed_report(output, review):
    """Compose a short research summary only for a complete matching human review."""
    study = verify(output)
    review = Review.model_validate(review)
    review.verify(study)
    accepted = sum(d.decision == "accept" for d in review.decisions)
    return f"# Endoscopy research summary\n\n{len(study.candidates)} candidate region(s) proposed; {accepted} accepted and {len(study.candidates) - accepted} rejected on review. Reviewed areas are in source-image pixels; physical size, histology and anatomical location are unavailable.\n\n{LIMITATION}\n\nStudy evidence: {digest(study)}\nReview evidence: {digest(review)}\n"
