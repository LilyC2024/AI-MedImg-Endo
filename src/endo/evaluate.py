"""Held-out research metrics; mask-region box matches are detection proxies only."""

import json
import time
from pathlib import Path

import numpy as np
from PIL import Image

from endo.data import load_manifest
from endo.inference import Predictor
from endo_contracts import regions


def iou(a, b):
    """Calculate overlap between two half-open source-image boxes."""
    x0, y0 = max(a[0], b[0]), max(a[1], b[1])
    x1, y1 = min(a[2], b[2]), min(a[3], b[3])
    intersection = max(0, x1 - x0) * max(0, y1 - y0)
    return intersection / (
        (a[2] - a[0]) * (a[3] - a[1]) + (b[2] - b[0]) * (b[3] - b[1]) - intersection
    )


def score(mask, target, candidates):
    """Separate positive overlap, negative false candidates and box-region proxies."""
    pred = mask > 0
    truth = target > 0
    intersection = int((pred & truth).sum())
    union = int((pred | truth).sum())
    _, gt = regions(truth.astype(np.float32), 0.5, 1)
    used = set()
    tp = 0
    for c in sorted(candidates, key=lambda c: c.mean_model_score, reverse=True):
        possible = [
            (iou(c.box_xyxy, g.box_xyxy), i) for i, g in enumerate(gt) if i not in used
        ]
        best = max(possible, default=(0, -1))
        if best[0] >= 0.5:
            used.add(best[1])
            tp += 1
    return {
        "dice": 2 * intersection / (int(pred.sum() + truth.sum()))
        if pred.any() or truth.any()
        else 1.0,
        "iou": intersection / union if union else 1.0,
        "tp_proxy": tp,
        "fp_proxy": len(candidates) - tp,
        "fn_proxy": len(gt) - tp,
        "positive": bool(truth.any()),
        "candidate_count": len(candidates),
    }


def evaluate(directory, root, manifest, output, *, backend="onnx-cpu"):
    """Evaluate the frozen test partition and record measured local runtime evidence."""
    split = load_manifest(manifest, root)
    predictor = Predictor(directory, backend)
    if split["manifest_sha256"] != predictor.config["manifest_sha256"]:
        raise ValueError(
            "Use the frozen training manifest for held-out test evaluation"
        )
    results = []
    for row in split["records"]:
        if row["split"] != "test":
            continue
        with Image.open(Path(root) / row["image"]) as image:
            source = np.array(image.convert("RGB"))
        if row["mask"] is None:
            target = np.zeros(source.shape[:2], np.uint8)
        else:
            with Image.open(Path(root) / row["mask"]) as image:
                target = (np.array(image.convert("L")) >= 128).astype(np.uint8)
        start = time.perf_counter()
        p, model = predictor.predict(source)
        mask, candidates = regions(p, model.threshold, model.min_area_px)
        results.append(
            {
                "image": row["image"],
                "seconds": time.perf_counter() - start,
                **score(mask, target, candidates),
            }
        )
    positives = [r for r in results if r["positive"]]
    negatives = [r for r in results if not r["positive"]]
    tp, fp, fn = (
        sum(r[k] for r in results) for k in ("tp_proxy", "fp_proxy", "fn_proxy")
    )
    report = {
        "schema_version": "endo-evaluation-v1",
        "model_onnx_sha256": predictor.info["onnx_sha256"],
        "manifest_sha256": split["manifest_sha256"],
        "partition": "test",
        "backend": backend,
        "backend_parity": getattr(predictor, "backend_parity", None),
        "images": len(results),
        "positive_images": len(positives),
        "negative_images": len(negatives),
        "mean_positive_dice": float(np.mean([r["dice"] for r in positives]))
        if positives
        else None,
        "mean_positive_iou": float(np.mean([r["iou"] for r in positives]))
        if positives
        else None,
        "box_region_recall_proxy": tp / (tp + fn) if tp + fn else None,
        "box_region_precision_proxy": tp / (tp + fp) if tp + fp else None,
        "false_candidates_per_negative_image": sum(
            r["candidate_count"] for r in negatives
        )
        / len(negatives)
        if negatives
        else None,
        "latency_median_seconds": float(np.median([r["seconds"] for r in results]))
        if results
        else None,
        "latency_p95_seconds": float(np.percentile([r["seconds"] for r in results], 95))
        if results
        else None,
        "patient_independence": "not-established",
        "limitations": [
            "Connected ground-truth mask regions are not adjudicated lesion identities.",
            "No screening specificity can be established without negative examination data.",
            "No cancer, histology or millimetre estimate.",
        ],
        "results": results,
    }
    report["backend_parity"] = getattr(predictor, "backend_parity", None)
    with Path(output).open("x") as handle:
        json.dump(report, handle, indent=2)
    return report
