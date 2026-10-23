"""Ensure the maintained publication contains no generated images/models/runtime data."""

import subprocess
from pathlib import Path

root = Path(__file__).resolve().parents[1]
files = subprocess.check_output(
    ["git", "ls-files", "--cached", "--others", "--exclude-standard"],
    cwd=root,
    text=True,
).splitlines()
for name in files:
    if (
        name.startswith((".venv/", "data/", "datasets/"))
        or (name.startswith("artifacts/") and name != "artifacts/.gitkeep")
        or Path(name).suffix in (".pt", ".pth", ".onnx", ".sqlite3", ".db")
    ):
        raise ValueError("Runtime/research artifact in publication: " + name)
print(
    f"Publication inventory checked: {len(set(files))} maintained files; no datasets, weights or runtime records"
)
