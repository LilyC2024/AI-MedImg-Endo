"""Build pending synthetic evidence; never supplies reviewer approval."""

import io
import json
import zipfile
from datetime import datetime, timezone
from uuid import uuid4

import numpy as np

from endo_contracts import (
    Artifact,
    Bundle,
    Study,
    array_bytes,
    overlay_pixels,
    png,
    read_exchange,
    regions,
    sha,
)


def make_study(source, probability, model, *, patient_alias, study_id, input_kind):
    """Derive source-bound candidate observations from the supplied prediction map."""
    if (
        source.dtype != np.uint8
        or source.ndim != 3
        or source.shape[2] != 3
        or probability.shape != source.shape[:2]
        or probability.dtype != np.float32
        or not np.isfinite(probability).all()
        or np.any(probability < 0)
        or np.any(probability > 1)
    ):
        raise ValueError("Invalid source/probability shape, type or range")
    mask, candidates = regions(probability, model.threshold, model.min_area_px)
    study = Study(
        study_id=study_id,
        patient_alias=patient_alias,
        input_kind=input_kind,
        source_sha256=sha(source.tobytes()),
        width=source.shape[1],
        height=source.shape[0],
        model=model,
        candidates=candidates,
    )
    return study, mask


def export_bundle(study, source, probability, *, job_id=None):
    """Export only synthetic pending evidence, then validate the complete archive."""
    mask, candidates = regions(
        probability, study.model.threshold, study.model.min_area_px
    )
    artifacts = {
        "source.png": ("source_preview", png(source)),
        "probability.npy": ("probability", array_bytes(probability)),
        "mask.png": ("mask", png(mask)),
        "overlay.png": (
            "overlay_preview",
            png(overlay_pixels(source, mask, candidates)),
        ),
    }
    bundle = Bundle(
        synthetic=True,
        patient_id=study.patient_alias,
        study_id=study.study_id,
        job_id=job_id or uuid4().hex,
        processed_at=datetime.now(timezone.utc),
        study=study,
        artifacts=[
            Artifact(path=path, role=role, sha256=sha(data), size_bytes=len(data))
            for path, (role, data) in artifacts.items()
        ],
    )
    stream = io.BytesIO()
    with zipfile.ZipFile(stream, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr(
            "bundle.json", json.dumps(bundle.model_dump(mode="json"), sort_keys=True)
        )
        for path, (_, data) in artifacts.items():
            archive.writestr(path, data)
    payload = stream.getvalue()
    read_exchange(payload, study.patient_alias)
    return payload
