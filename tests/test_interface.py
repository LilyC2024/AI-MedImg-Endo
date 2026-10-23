"""Real Streamlit render and stdlib workers; artificial fixtures, no clinical approvals."""

import sys
import time
from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

from endo_contracts.worker import LocalJob


def test_standalone_ui_starts_with_clear_review_guide():
    app = AppTest.from_file(str(Path(__file__).resolve().parents[1] / "app.py")).run()
    assert not app.exception
    assert any("Endoscopy image review" in t.value for t in app.title)
    assert any(b.label == "Analyze image" for b in app.button)
    app.radio[0].set_value("Public research image").run()
    assert next(b for b in app.button if b.label == "Analyze image").disabled


def test_worker_completion_requires_expected_output(tmp_path):
    result = tmp_path / "job" / "result.txt"
    command = [
        sys.executable,
        "-c",
        'from pathlib import Path;import sys;Path(sys.argv[1]).write_text("scripted worker, no inference")',
        str(result),
    ]
    job = LocalJob(command, cwd=tmp_path, directory=tmp_path / "job", output=result)
    until = time.monotonic() + 5
    while job.status() == "running" and time.monotonic() < until:
        time.sleep(0.01)
    assert job.status() == "complete"


@pytest.mark.parametrize("cancel", [True, False])
def test_worker_timeout_cancellation_no_late_completion(tmp_path, cancel):
    job = LocalJob(
        [sys.executable, "-c", "import time;time.sleep(60)"],
        cwd=tmp_path,
        directory=tmp_path / "job",
        output=tmp_path / "missing",
        timeout=10 if cancel else 0.1,
    )
    if cancel:
        job.cancel()
    job.process.wait(timeout=5)
    assert job.status() == ("cancelled" if cancel else "timed_out")


@pytest.mark.parametrize("timeout", [0, float("inf"), float("nan")])
def test_invalid_deadline_rejected(tmp_path, timeout):
    with pytest.raises(ValueError):
        LocalJob(
            [],
            cwd=tmp_path,
            directory=tmp_path / "job",
            output=tmp_path / "missing",
            timeout=timeout,
        )


def test_changing_source_cancels_old_job_and_hides_old_result():
    class Job:
        cancelled = False

        def status(self):
            return "running"

        def cancel(self):
            self.cancelled = True

    app = AppTest.from_file(str(Path(__file__).resolve().parents[1] / "app.py")).run()
    job = Job()
    app.session_state.job = job
    app.session_state.workspace = "old image"
    app.session_state.reviewed_summary = {"report": "old"}
    app.radio[0].set_value("Public research image").run()
    assert (
        job.cancelled
        and "workspace" not in app.session_state
        and "reviewed_summary" not in app.session_state
    )
    assert not app.exception and not app.image
