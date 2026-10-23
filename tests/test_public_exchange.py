"""Manufactured probability tests, never a live public-image accuracy measurement."""

import pytest
from endo.exchange import export_bundle
from endo_contracts import Study, read_exchange
from test_foundation import sample


def test_public_provenance_is_required_without_synthetic_relabelling():
    fixture, source, probability = sample()
    value = fixture.model_dump()
    value.update(
        patient_alias="research-composite-demo", input_kind="approved-public-research"
    )
    value["model"].update(
        name="UNetSmall", backend="onnx-cpu", evaluation_scope="positive-images-only"
    )
    study = Study.model_validate(value)
    provenance = dict(
        dataset="test",
        source_url="https://example.org/test",
        license="test-only",
        research_subject_id="unrelated-subject",
        original_sha256="a" * 64,
        composite_case=True,
    )
    data = export_bundle(study, source, probability, research=provenance)
    bundle, _, _ = read_exchange(data, "research-composite-demo")
    assert bundle.synthetic is False and bundle.research.dataset == "test"
    with pytest.raises(ValueError):
        export_bundle(study, source, probability)


def test_research_probability_above_legacy_four_megabyte_limit():
    """Manufactured large RGB/map: actual Kvasir example dimensions need >4 MiB NPY."""
    import numpy as np
    from endo.exchange import make_study

    fixture, _, _ = sample()
    model = fixture.model.model_copy(
        update=dict(
            name="UNetSmall",
            backend="onnx-cpu",
            evaluation_scope="positive-images-only",
        )
    )
    source = np.zeros((1070, 1348, 3), np.uint8)
    p = np.zeros(source.shape[:2], np.float32)
    p[20:30, 20:30] = 0.9
    study, _ = make_study(
        source,
        p,
        model,
        patient_alias="research-composite-demo",
        study_id="large",
        input_kind="approved-public-research",
    )
    provenance = dict(
        dataset="manufactured",
        source_url="https://example.org/test",
        license="test-only",
        research_subject_id="unknown",
        original_sha256="a" * 64,
        composite_case=True,
    )
    bundle, _, _ = read_exchange(
        export_bundle(study, source, p, research=provenance), "research-composite-demo"
    )
    assert (
        next(a.size_bytes for a in bundle.artifacts if a.role == "probability")
        > 4 * 1024**2
    )
