"""Compact 3-level U-Net; raw logits, fixed multiples-of-eight RGB input."""

import torch
from torch import nn


def block(a, b):
    """Build two convolution/ReLU layers for one U-Net resolution level."""
    return nn.Sequential(
        nn.Conv2d(a, b, 3, padding=1),
        nn.ReLU(),
        nn.Conv2d(b, b, 3, padding=1),
        nn.ReLU(),
    )


class UNetSmall(nn.Module):
    def __init__(self, base=16):
        """Initialise the explicit local model or bounded worker without remote fallback."""
        super().__init__()
        self.enc1, self.enc2, self.enc3 = (
            block(3, base),
            block(base, base * 2),
            block(base * 2, base * 4),
        )
        self.mid = block(base * 4, base * 8)
        self.pool = nn.MaxPool2d(2)
        self.up3, self.up2, self.up1 = (
            nn.ConvTranspose2d(base * 8, base * 4, 2, 2),
            nn.ConvTranspose2d(base * 4, base * 2, 2, 2),
            nn.ConvTranspose2d(base * 2, base, 2, 2),
        )
        self.dec3, self.dec2, self.dec1 = (
            block(base * 8, base * 4),
            block(base * 4, base * 2),
            block(base * 2, base),
        )
        self.out = nn.Conv2d(base, 1, 1)

    def forward(self, x):
        """Return raw segmentation logits from RGB tensors using skip connections."""
        a = self.enc1(x)
        b = self.enc2(self.pool(a))
        c = self.enc3(self.pool(b))
        x = self.mid(self.pool(c))
        x = self.dec3(torch.cat([self.up3(x), c], 1))
        x = self.dec2(torch.cat([self.up2(x), b], 1))
        return self.out(self.dec1(torch.cat([self.up1(x), a], 1)))


def loss(logits, target):
    """Combine binary logit cross entropy and per-image soft Dice loss."""
    bce = nn.functional.binary_cross_entropy_with_logits(logits, target)
    probability = torch.sigmoid(logits)
    dims = (1, 2, 3)
    dice = (2 * (probability * target).sum(dims) + 1) / (
        probability.sum(dims) + target.sum(dims) + 1
    )
    return bce + (1 - dice).mean()
