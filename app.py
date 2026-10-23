"""Standalone research-image UI; LOVISA provides the separate clinical workflow."""

import sys
from pathlib import Path
from uuid import uuid4

import streamlit as st

from endo.workspace import reviewed_report, verify
from endo_contracts import LIMITATION, Review, digest, sha
from endo_contracts.worker import LocalJob

ROOT = Path(__file__).resolve().parent


@st.fragment(run_every=1)
def progress(job):
    if job.status() != "running":
        st.rerun()
    st.info(job.progress())
    st.caption(
        f"{job.elapsed:.0f} seconds elapsed · automatic stop at {job.timeout:.0f} seconds"
    )
    if st.button("Cancel analysis"):
        job.cancel()
        st.rerun()


def main():
    st.set_page_config(
        page_title="LOVISA · Endoscopy research", page_icon="◈", layout="wide"
    )
    st.title("Endoscopy image review")
    st.caption("Local polyp candidate research assistant · " + LIMITATION)
    left, guide = st.columns([3, 1])
    with guide:
        st.subheader("Your next steps")
        st.write(
            "1. Choose an artificial example or permitted research image.\n\n2. Run local analysis.\n\n3. Inspect source and candidate outlines.\n\n4. Review every candidate.\n\n5. Include synthetic evidence in LOVISA, or save a separate research review."
        )
        st.info(
            "The non-ML fixture demonstrates the workflow. Installed models show their actual training/evaluation scope."
        )
    with left:
        mode = st.radio(
            "Image source",
            ["Artificial example", "Public research image"],
            horizontal=True,
        )
        upload = (
            st.file_uploader("Research image (PNG/JPEG)", type=["png", "jpg", "jpeg"])
            if mode == "Public research image"
            else None
        )
        permission = (
            st.checkbox(
                "I have permission to use this de-identified research image; it is not a clinical patient record."
            )
            if mode == "Public research image"
            else True
        )
        with st.expander("Local model settings"):
            model = st.text_input(
                "Installed model directory",
                value=str(ROOT / "artifacts/kvasir-model")
                if (ROOT / "artifacts/kvasir-model/registration.json").is_file()
                else "",
                help="Leave empty for the artificial non-ML fixture. Synthetic-only weights are not a clinical polyp detector.",
            )
            backend = st.selectbox(
                "Local execution", ["onnx-cpu", "openvino-cpu", "openvino-npu"]
            )
        source_token = mode + (sha(upload.getvalue()) if upload is not None else "")
        if st.session_state.get("source_token") != source_token:
            old = st.session_state.get("job")
            if old and old.status() == "running":
                old.cancel()
            for key in ("job", "workspace", "reviewed_summary"):
                st.session_state.pop(key, None)
            st.session_state.source_token = source_token
        job = st.session_state.get("job")
        running = job is not None and job.status() == "running"
        if st.button(
            "Analyze image",
            type="primary",
            disabled=running
            or not permission
            or (mode == "Public research image" and (upload is None or not model)),
        ):
            directory = ROOT / "artifacts/jobs" / uuid4().hex
            output = directory / "result"
            command = [
                sys.executable,
                "-m",
                "endo.cli",
                "demo" if mode == "Artificial example" else "infer",
                "--output",
                str(output),
                "--backend",
                backend,
            ]
            if model:
                command += ["--model-dir", model]
            if upload:
                raw = upload.getvalue()
                if len(raw) > 16 * 1024**2:
                    st.error("Image exceeds 16 MiB.")
                    return
                source = ROOT / "artifacts/uploads" / uuid4().hex
                source.parent.mkdir(parents=True, exist_ok=True)
                source.write_bytes(raw)
                command += ["--image", str(source), "--research-use-attested"]
            st.session_state.pop("workspace", None)
            st.session_state.pop("reviewed_summary", None)
            st.session_state.job = LocalJob(
                command, cwd=ROOT, directory=directory, output=output / "study.json"
            )
            st.rerun()
        if job:
            if job.status() == "running":
                progress(job)
            elif job.status() == "complete":
                st.session_state.workspace = job.bundle_path.parent
            else:
                st.warning(job.error)
        if "workspace" not in st.session_state:
            return
        output = st.session_state.workspace
        try:
            study = verify(output)
            st.subheader("Analysis results")
            st.write(
                f"{len(study.candidates)} candidate region(s) · {study.model.name} · {study.model.evaluation_scope}"
            )
            a, b = st.columns(2)
            a.image(
                str(output / "source.png"),
                caption="Original decoded image",
                width="stretch",
            )
            b.image(
                str(output / "overlay.png"),
                caption="Candidate outlines · not a diagnosis",
                width="stretch",
            )
            for c in study.candidates:
                st.write(
                    f"{c.candidate_id}: {c.area_px:,} pixels; {100 * c.area_px / (study.width * study.height):.2f}% of this image. Model score {c.mean_model_score:.3f}, not cancer probability."
                )
            with st.form("review"):
                decisions = [
                    {
                        "candidate_id": c.candidate_id,
                        "decision": st.selectbox(
                            "Review " + c.candidate_id,
                            ["uncertain", "accept", "reject"],
                            key=digest(study) + c.candidate_id,
                        ),
                    }
                    for c in study.candidates
                ]
                reviewer = st.text_input("Research reviewer name")
                attested = st.checkbox(
                    "I checked the source, every candidate and the research limitations."
                )
                submit = st.form_submit_button("Save research review")
            if submit:
                review = Review(
                    study_digest=digest(study),
                    reviewer=reviewer,
                    attested=attested,
                    decisions=decisions,
                )
                report = reviewed_report(output, review.model_dump())
                # Preserve decisions separately; do not overwrite earlier reviews.
                destination = output / ("review-" + uuid4().hex + ".json")
                destination.write_text(review.model_dump_json(indent=2))
                st.success(
                    "Research review saved. LOVISA requires its own authenticated image acceptance and final report approval."
                )
                st.session_state.reviewed_summary = {
                    "study_digest": digest(study),
                    "report": report,
                }
            summary = st.session_state.get("reviewed_summary")
            if summary and summary["study_digest"] == digest(study):
                st.download_button(
                    "Download research summary",
                    summary["report"],
                    file_name="endoscopy-research.md",
                )
            if study.input_kind == "generated-synthetic":
                st.download_button(
                    "Send to LOVISA: download synthetic bundle",
                    (output / "bundle.endo.zip").read_bytes(),
                    file_name="bundle.endo.zip",
                    mime="application/zip",
                )
            else:
                st.caption(
                    "Public research images remain in this standalone workspace; LOVISA accepts artificial studies only."
                )
        except (ValueError, OSError) as error:
            st.error(str(error))


if __name__ == "__main__":
    main()
