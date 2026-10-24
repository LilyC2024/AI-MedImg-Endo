"""Research-only dataset inventory and immutable, related-image-grouped split manifests."""

import json
import math
import random
from pathlib import Path

import numpy as np
from PIL import Image

from endo_contracts import digest, sha

EXTENSIONS = {".png", ".jpg", ".jpeg"}


def _files(directory):
    """List regular supported image files and reject ambiguous duplicate stems."""
    paths = sorted(
        p for p in Path(directory).iterdir() if p.suffix.lower() in EXTENSIONS
    )
    if any(p.is_symlink() or not p.is_file() for p in paths):
        raise ValueError("Dataset images must be regular files")
    if len({p.stem for p in paths}) != len(paths):
        raise ValueError("Duplicate image stem")
    return paths


def fingerprint(rgb):
    """Compute a small difference hash for heuristic related-image grouping."""
    small = np.array(
        Image.fromarray(rgb).convert("L").resize((9, 8), Image.Resampling.BILINEAR)
    )
    return int.from_bytes(np.packbits(small[:, 1:] > small[:, :-1]).tobytes(), "big")


def inventory(root, negatives=None):
    """Validate paired research sources and record immutable content hashes."""
    root = Path(root).resolve()
    images, masks = _files(root / "images"), {p.stem: p for p in _files(root / "masks")}
    if not images or set(p.stem for p in images) != set(masks):
        raise ValueError("Missing/duplicated image-mask pairs")
    records = []
    for image in images:
        mask = masks[image.stem]
        with Image.open(image) as handle:
            rgb = np.array(handle.convert("RGB"))
        with Image.open(mask) as handle:
            target = np.array(handle.convert("L")) >= 128
        if rgb.shape[:2] != target.shape:
            raise ValueError("Image/mask dimensions differ")
        records.append(
            {
                "image": image.relative_to(root).as_posix(),
                "mask": mask.relative_to(root).as_posix(),
                "image_sha256": sha(image.read_bytes()),
                "mask_sha256": sha(mask.read_bytes()),
                "decoded_sha256": sha(rgb.tobytes()),
                "dhash": f"{fingerprint(rgb):016x}",
                "positive": bool(target.any()),
                "foreground_fraction": float(target.mean()),
                "group": None,
            }
        )
    if negatives:
        for image in _files(negatives):
            # Negative images live under the same declared dataset root.
            relative = image.resolve().relative_to(root)
            with Image.open(image) as handle:
                rgb = np.array(handle.convert("RGB"))
            records.append(
                {
                    "image": relative.as_posix(),
                    "mask": None,
                    "image_sha256": sha(image.read_bytes()),
                    "mask_sha256": None,
                    "decoded_sha256": sha(rgb.tobytes()),
                    "dhash": f"{fingerprint(rgb):016x}",
                    "positive": False,
                    "foreground_fraction": 0.0,
                    "group": None,
                }
            )
    if len({r["image"] for r in records}) != len(records):
        raise ValueError("Duplicate source path")
    return records


def freeze(root, output, *, negatives=None, seed=42, near_distance=4):
    """Write a new grouped split manifest without overwriting prior experiments."""
    if not 0 <= near_distance <= 16:
        raise ValueError("Invalid near-duplicate threshold")
    rows = inventory(root, negatives)
    parent = list(range(len(rows)))

    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    for i, row in enumerate(rows):
        for j in range(i):
            other = rows[j]
            if (
                row["decoded_sha256"] == other["decoded_sha256"]
                or (int(row["dhash"], 16) ^ int(other["dhash"], 16)).bit_count()
                <= near_distance
            ):
                parent[find(i)] = find(j)
    groups = sorted({find(i) for i in range(len(rows))})
    if len(groups) < 3:
        raise ValueError("Need at least three independent image groups")
    random.Random(seed).shuffle(groups)
    n = len(groups)
    # Keep complete related-image groups in one partition; no patient independence claim.
    val_count, test_count = max(1, round(n * 0.15)), max(1, round(n * 0.15))
    assignments = {
        g: (
            "test"
            if i < test_count
            else "validation"
            if i < test_count + val_count
            else "train"
        )
        for i, g in enumerate(groups)
    }
    for i, row in enumerate(rows):
        row["group"] = f"group-{find(i):05d}"
        row["split"] = assignments[find(i)]
    body = {
        "schema_version": "endo-split-v1",
        "seed": seed,
        "near_distance": near_distance,
        "patient_independence": "not-established",
        "records": rows,
    }
    body["manifest_sha256"] = digest(body)
    Path(output).parent.mkdir(parents=True, exist_ok=True)
    with Path(output).open("x", encoding="utf-8") as handle:
        json.dump(body, handle, indent=2)
    return body


def load_manifest(path, root):
    """Recheck manifest identity, group separation and every referenced source."""
    body = json.loads(Path(path).read_text())
    if not isinstance(body, dict):
        raise ValueError("Split manifest must be a JSON object")
    expected = body.pop("manifest_sha256", None)
    if digest(body) != expected or body.get("schema_version") != "endo-split-v1":
        raise ValueError("Split manifest changed/unsupported")
    root = Path(root).resolve()
    rows = body.get("records")
    near_distance = body.get("near_distance")
    if (
        not isinstance(rows, list)
        or not rows
        or type(near_distance) is not int
        or not 0 <= near_distance <= 16
    ):
        raise ValueError("Invalid split manifest records/near-duplicate threshold")
    required = {
        "image",
        "mask",
        "image_sha256",
        "mask_sha256",
        "decoded_sha256",
        "dhash",
        "positive",
        "foreground_fraction",
        "group",
        "split",
    }
    if any(not isinstance(r, dict) or set(r) != required for r in rows):
        raise ValueError("Invalid split manifest record fields")
    if len({r["image"] for r in rows}) != len(rows):
        raise ValueError("Duplicate manifest image")
    groups = {}
    decoded = []
    for row in rows:
        if (
            not isinstance(row["group"], str)
            or not row["group"]
            or type(row["positive"]) is not bool
            or type(row["foreground_fraction"]) not in (int, float)
            or not math.isfinite(row["foreground_fraction"])
            or not 0 <= row["foreground_fraction"] <= 1
        ):
            raise ValueError("Invalid image group/target metadata")
        if row["split"] not in ("train", "validation", "test"):
            raise ValueError("Unknown split")
        if row["group"] in groups and groups[row["group"]] != row["split"]:
            raise ValueError("Related-image leakage")
        groups[row["group"]] = row["split"]
        for key in ("image", "mask"):
            if row[key] is None:
                if key == "image" or row["positive"]:
                    raise ValueError("Missing required source")
                continue
            if (
                not isinstance(row[key], str)
                or "\\" in row[key]
                or ":" in row[key]
                or Path(row[key]).is_absolute()
                or any(p in ("", ".", "..") for p in row[key].split("/"))
            ):
                raise ValueError("Dataset manifest paths must be relative POSIX paths")
            file = root / row[key]
            if (
                file.is_symlink()
                or not file.is_file()
                or not file.resolve().is_relative_to(root)
                or sha(file.read_bytes()) != row[key + "_sha256"]
            ):
                raise ValueError("Dataset source changed or escapes root")
        with Image.open(root / row["image"]) as image:
            rgb = np.array(image.convert("RGB"))
        image_digest = sha(rgb.tobytes())
        image_hash = fingerprint(rgb)
        if (
            row["decoded_sha256"] != image_digest
            or row["dhash"] != f"{image_hash:016x}"
        ):
            raise ValueError("Decoded image identity/fingerprint changed")
        if row["mask"] is None:
            positive, fraction = False, 0.0
            if row["mask_sha256"] is not None:
                raise ValueError("Negative image has conflicting mask metadata")
        else:
            with Image.open(root / row["mask"]) as image:
                target = np.array(image.convert("L")) >= 128
            if target.shape != rgb.shape[:2]:
                raise ValueError("Image/mask dimensions differ")
            positive, fraction = bool(target.any()), float(target.mean())
        if row["positive"] != positive or row["foreground_fraction"] != fraction:
            raise ValueError("Target metadata does not match source mask")
        for other_digest, other_hash, other_group, other_split in decoded:
            related = (
                image_digest == other_digest
                or (image_hash ^ other_hash).bit_count() <= near_distance
            )
            if related and (row["group"], row["split"]) != (other_group, other_split):
                raise ValueError("Related-image content crosses groups or splits")
        decoded.append((image_digest, image_hash, row["group"], row["split"]))
    if {row["split"] for row in rows} != {"train", "validation", "test"}:
        raise ValueError("All three splits are required")
    body["manifest_sha256"] = expected
    return body


def arrays(row, root, size):
    """Load aligned fixed-size RGB inputs and binary mask targets."""
    with Image.open(Path(root) / row["image"]) as image:
        rgb = (
            np.array(
                image.convert("RGB").resize((size, size), Image.Resampling.BILINEAR),
                dtype=np.float32,
            )
            / 255
        )
    if row["mask"] is None:
        mask = np.zeros((size, size), dtype=np.float32)
    else:
        with Image.open(Path(root) / row["mask"]) as image:
            mask = (
                np.array(
                    image.convert("L").resize((size, size), Image.Resampling.NEAREST)
                )
                >= 128
            ).astype(np.float32)
    return rgb.transpose(2, 0, 1), mask[None]
