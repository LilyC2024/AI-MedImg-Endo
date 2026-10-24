"""Local commands. Setup/training are explicit; runtime never fetches models/data."""

import argparse
import json
import os
from pathlib import Path
from uuid import uuid4

import numpy as np
from PIL import Image

from endo.fixture import fixture_probability, phantom
from endo_contracts import ModelInfo, sha


def main():
    """Dispatch explicit local workflow commands without automatic clinical decisions."""
    parser = argparse.ArgumentParser(
        description="Local polyp candidate research assistant"
    )
    sub = parser.add_subparsers(dest="command", required=True)
    split = sub.add_parser("split")
    split.add_argument("--data", required=True)
    split.add_argument("--output", required=True)
    split.add_argument("--negative-dir")
    split.add_argument("--seed", type=int, default=42)
    syn = sub.add_parser("synthetic-data")
    syn.add_argument("--output", required=True)
    syn.add_argument("--count", type=int, default=64)
    syn.add_argument("--size", type=int, default=64)
    train = sub.add_parser("train")
    train.add_argument("--data", required=True)
    train.add_argument("--manifest", required=True)
    train.add_argument("--output", required=True)
    train.add_argument("--epochs", type=int, default=10)
    train.add_argument("--size", type=int, default=256)
    train.add_argument("--base", type=int, default=16)
    train.add_argument("--threads", type=int, default=4)
    train.add_argument("--synthetic", action="store_true")
    export = sub.add_parser("export-model")
    export.add_argument("--model-dir", required=True)
    ev = sub.add_parser("evaluate")
    ev.add_argument("--model-dir", required=True)
    ev.add_argument("--data", required=True)
    ev.add_argument("--manifest", required=True)
    ev.add_argument("--output", required=True)
    ev.add_argument(
        "--backend",
        default="onnx-cpu",
        choices=["onnx-cpu", "openvino-cpu", "openvino-npu"],
    )
    keygen = sub.add_parser(
        "keygen", help="Create an Ed25519 signing key for review ZIPs; prints public key"
    )
    keygen.add_argument("--output", required=True, help="New private key file (0600)")
    for name in ("demo", "infer", "bridge"):
        item = sub.add_parser(name)
        item.add_argument("--output", required=True)
        item.add_argument(
            "--signing-key",
            default=os.environ.get("LOVISA_SIGNING_KEY_FILE"),
            help="Ed25519 key file; defaults to $LOVISA_SIGNING_KEY_FILE; unsigned if absent",
        )
        item.add_argument(
            "--evaluation",
            help="Explicit held-out evaluation for this exact model/configuration/backend; otherwise unmeasured",
        )
        item.add_argument("--patient-id", default="synthetic-checklist")
        item.add_argument("--study-id", default=None)
        item.add_argument("--model-dir")
        item.add_argument(
            "--backend",
            default="onnx-cpu",
            choices=["onnx-cpu", "openvino-cpu", "openvino-npu"],
        )
        if name == "infer":
            item.add_argument("--image", required=True)
            item.add_argument("--research-use-attested", action="store_true")
            item.add_argument(
                "--research-provenance",
                help="Public dataset/license/subject JSON for composite LOVISA export",
            )
    args = parser.parse_args()
    command = args.command
    if command == "keygen":
        from endo_contracts.producer_signature import generate_key

        print(json.dumps({"producer": "lovisa-endo", **generate_key(args.output)}, indent=2))
        return
    if command == "split":
        from endo.data import freeze

        result = freeze(
            args.data, args.output, negatives=args.negative_dir, seed=args.seed
        )
        print(
            json.dumps(
                {
                    "records": len(result["records"]),
                    "manifest_sha256": result["manifest_sha256"],
                }
            )
        )
        return
    if command == "synthetic-data":
        if not 12 <= args.count <= 1000 or args.size not in (64, 128, 256):
            raise ValueError("Synthetic dataset bounds exceeded")
        root = Path(args.output)
        root.mkdir(parents=True, exist_ok=False)
        for directory in ("images", "masks"):
            (root / directory).mkdir()
        for i in range(args.count):
            source, mask = phantom(i, args.size, positive=i % 4 != 0)
            Image.fromarray(source).save(root / "images" / f"{i:04d}.png")
            Image.fromarray(mask).save(root / "masks" / f"{i:04d}.png")
        return
    if command == "train":
        from endo.train import train

        train(
            args.data,
            args.manifest,
            args.output,
            epochs=args.epochs,
            size=args.size,
            base=args.base,
            threads=args.threads,
            synthetic=args.synthetic,
        )
        return
    if command == "export-model":
        from endo.deploy import export

        print(json.dumps(export(args.model_dir), indent=2))
        return
    if command == "evaluate":
        from endo.evaluate import evaluate

        report = evaluate(
            args.model_dir, args.data, args.manifest, args.output, backend=args.backend
        )
        print(json.dumps({k: v for k, v in report.items() if k != "results"}, indent=2))
        return
    from endo.workspace import create

    print("LOVISA_STAGE=source", flush=True)
    original = None
    if command == "infer":
        if not args.research_use_attested:
            raise ValueError(
                "Explicit public-research use attestation required; clinical records unsupported"
            )
        raw = Path(args.image).read_bytes()
        if len(raw) > 16 * 1024**2:
            raise ValueError("Input file exceeds 16 MiB")
        import io

        with Image.open(io.BytesIO(raw)) as image:
            if (
                image.format not in ("JPEG", "PNG")
                or not 16 <= min(image.size) <= max(image.size) <= 2048
                or getattr(image, "n_frames", 1) != 1
            ):
                raise ValueError("Single RGB image,16–2048 pixels per side, required")
            source = np.array(image.convert("RGB"))
        original = raw
        kind = "approved-public-research"
        if not args.model_dir:
            raise ValueError("Installed registered model required")
    else:
        source, _ = phantom(11)
        kind = "generated-synthetic"
    if args.model_dir:
        print("LOVISA_STAGE=model", flush=True)
        from endo.inference import Predictor

        predictor = Predictor(args.model_dir, args.backend)
        print("LOVISA_STAGE=detect", flush=True)
        if (
            kind == "approved-public-research"
            and predictor.config["evaluation_scope"] == "synthetic-only"
        ):
            raise ValueError(
                "Synthetic-only weights cannot analyse public research images"
            )
        p, model = predictor.predict(source)
        evaluation = args.evaluation
        from endo.evaluate import declared_performance

        performance = declared_performance(predictor.info, evaluation, backend=args.backend)
    else:
        if args.evaluation:
            raise ValueError("The non-ML fixture has no model evaluation")
        performance = None
        if args.backend != "onnx-cpu":
            raise ValueError("Fixture is CPU-only")
        p = fixture_probability(source)
        model = ModelInfo(
            name="synthetic-fixture",
            backend="fixture",
            checkpoint_sha256=sha(b"non-ML"),
            recipe_sha256=sha(b"fixture-v1"),
            threshold=0.5,
            min_area_px=8,
            evaluation_scope="software-fixture",
        )
    print("LOVISA_STAGE=export", flush=True)
    study = create(
        source,
        p,
        model,
        args.output,
        patient_alias=args.patient_id,
        study_id=args.study_id or "endo-" + uuid4().hex[:16],
        input_kind=kind,
        original_bytes=original,
        research=json.loads(Path(args.research_provenance).read_text())
        if command == "infer" and args.research_provenance
        else None,
        signing_key=args.signing_key,
        performance=performance,
    )
    print(
        json.dumps(
            {
                "study_id": study.study_id,
                "candidates": len(study.candidates),
                "input_kind": kind,
                "approval": "pending",
            }
        )
    )


if __name__ == "__main__":
    main()
