"""Offline CPU training; validation selects checkpoint, held-out test is never used."""

import json
import random
import time
from pathlib import Path

import numpy as np
import torch

from endo.data import arrays, load_manifest
from endo.model import UNetSmall, loss
from endo_contracts import digest, sha


def train(
    root,
    manifest,
    output,
    *,
    epochs=10,
    size=256,
    base=16,
    batch_size=8,
    seed=42,
    threads=4,
    synthetic=False,
):
    """Train deterministically on CPU; select by validation loss without test selection."""
    if (
        epochs < 1
        or size not in (64, 128, 256, 512)
        or base not in (4, 8, 16)
        or not 1 <= batch_size <= 32
        or not 1 <= threads <= 16
    ):
        raise ValueError("Invalid bounded training configuration")
    output = Path(output)
    output.mkdir(parents=True, exist_ok=False)
    split = load_manifest(manifest, root)
    partitions = {
        name: [r for r in split["records"] if r["split"] == name]
        for name in ("train", "validation", "test")
    }
    if any(not rows for rows in partitions.values()):
        raise ValueError("All three splits are required")
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.set_num_threads(threads)
    torch.use_deterministic_algorithms(True)
    model = UNetSmall(base)
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
    # Cache only resized training/validation arrays; never load test pixels for selection.
    cache = {
        name: [arrays(r, root, size) for r in partitions[name]]
        for name in ("train", "validation")
    }
    config = {
        "model": "UNetSmall",
        "size": size,
        "base": base,
        "batch_size": batch_size,
        "seed": seed,
        "threads": threads,
        "epochs": epochs,
        "learning_rate": 0.001,
        "loss": "BCEWithLogits+softDice",
        "preprocess": "RGB/255; bilinear image resize; nearest mask >=128",
        "manifest_sha256": split["manifest_sha256"],
        "threshold": 0.5,
        "min_area_px": 8,
        "evaluation_scope": "synthetic-only"
        if synthetic
        else "positive-images-only"
        if all(r["positive"] for r in split["records"])
        else "includes-negative-images",
    }
    best = float("inf")
    history = []
    started = time.monotonic()
    rng = random.Random(seed)
    for epoch in range(epochs):
        model.train()
        order = list(range(len(cache["train"])))
        rng.shuffle(order)
        train_loss = 0
        for offset in range(0, len(order), batch_size):
            items = [cache["train"][i] for i in order[offset : offset + batch_size]]
            x = torch.from_numpy(np.stack([i[0] for i in items]))
            y = torch.from_numpy(np.stack([i[1] for i in items]))
            # Deterministic aligned flips are training-only.
            if rng.random() < 0.5:
                x = x.flip(-1)
                y = y.flip(-1)
            optimizer.zero_grad(set_to_none=True)
            value = loss(model(x), y)
            value.backward()
            optimizer.step()
            train_loss += float(value.detach()) * len(items)
        model.eval()
        validation = 0
        with torch.inference_mode():
            for x, y in cache["validation"]:
                validation += float(
                    loss(model(torch.from_numpy(x[None])), torch.from_numpy(y[None]))
                )
        validation /= len(cache["validation"])
        history.append(
            {
                "epoch": epoch + 1,
                "training_loss": train_loss / len(cache["train"]),
                "validation_loss": validation,
            }
        )
        print(json.dumps(history[-1]), flush=True)
        if validation < best:
            best = validation
            torch.save(model.state_dict(), output / "model.pt")
    (output / "config.json").write_text(json.dumps(config, indent=2))
    result = {
        "config": config,
        "config_sha256": digest(config),
        "checkpoint_sha256": sha((output / "model.pt").read_bytes()),
        "history": history,
        "elapsed_seconds": round(time.monotonic() - started, 3),
        "torch_version": torch.__version__,
        "device": "cpu",
        "test_used_for_selection": False,
    }
    (output / "training.json").write_text(json.dumps(result, indent=2))
    (output / "split.json").write_text(Path(manifest).read_text())
    return result
