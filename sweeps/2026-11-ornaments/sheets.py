#!/usr/bin/env python3
"""Campaign #13 oracle sheets for the O1 flag (round #4, tasks S4/S5).
S4: red-head pages WITHOUT any lattice in our census (8, 37, 40) — missed
lattice? S5: lattice-only unsolved pages (2,14,22,26,32,49,55) — missed red
head word? Book page N -> image {N+17}.jpg. Deterministic downscale only.
"""
import os

from PIL import Image

_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
IMG = os.path.join(_ROOT, "sources", "ibotpeaches", "liber_primus")
OUT = os.path.join(_ROOT, "docs", "img", "oracle")
S4 = [8, 37, 40]
S5 = [2, 14, 22, 26, 32, 49, 55]
os.makedirs(OUT, exist_ok=True)
for tag, pages, scale in (("S4", S4, 0.4), ("S5", S5, 0.3)):
    for p in pages:
        im = Image.open(os.path.join(IMG, f"{p + 17:02d}.jpg"))
        im = im.resize((int(im.width * scale), int(im.height * scale)))
        f = os.path.join(OUT, f"f7_{tag}_p{p:02d}.png")
        im.save(f)
        print(f, im.size)
