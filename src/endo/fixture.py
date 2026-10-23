"""Clearly artificial RGB phantom; known labels are used only by tests/training."""

import numpy as np


def phantom(seed=0, size=256, *, positive=True):
    """Generate clearly artificial coloured regions and their known test masks."""
    rng = np.random.default_rng(seed)
    y, x = np.mgrid[:size, :size]
    texture = rng.normal(0, 5, (size, size))
    rgb = np.stack(
        [
            100 + 12 * np.sin(x / 13) + texture,
            46 + 8 * np.cos(y / 17) + texture,
            50 + texture,
        ],
        axis=-1,
    )
    mask = np.zeros((size, size), bool)
    if positive:
        for _ in range(1 + seed % 2):
            cx, cy = rng.integers(size // 4, 3 * size // 4, 2)
            rx, ry = rng.integers(max(4, size // 14), max(5, size // 6), 2)
            mask |= ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= 1
        rgb[mask] = (
            np.stack(
                [
                    np.full(mask.sum(), 205),
                    np.full(mask.sum(), 95),
                    np.full(mask.sum(), 105),
                ],
                axis=-1,
            )
            + texture[mask, None]
        )
    return np.clip(rgb, 0, 255).astype(np.uint8), mask.astype(np.uint8) * 255


def fixture_probability(source):
    # Non-ML finder of artificial red regions; no clinical detection claim.
    """Find artificial red regions with a declared non-ML rule."""
    return np.where(source[:, :, 0] > 165, 0.95, 0.02).astype(np.float32)
