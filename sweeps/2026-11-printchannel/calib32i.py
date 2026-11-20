#!/usr/bin/env python3
"""#32 PRE-OUTPUT calibration v9: why do tail pages (47,48,49,51,53,55)
lose lines? Per-page glyph-height mode vs the fixed [90,135] band, and
per-line fail reasons (cluster count vs want, comp count vs want)."""
import os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from table32 import ink_and_mask, lines_of, cluster_cy
from scipy import ndimage

def diag(page):
    ink = ink_and_mask(page)
    lab, n = ndimage.label(ink, structure=np.ones((3, 3)))
    objs = ndimage.find_objects(lab)
    areas = np.bincount(lab.ravel(), minlength=n + 1)[1:].astype(float)
    hs = np.array([o[0].stop - o[0].start for o in objs], dtype=float)
    ws = np.array([o[1].stop - o[1].start for o in objs], dtype=float)
    cys = np.array([(o[0].start + o[0].stop - 1) / 2 for o in objs])
    big = areas >= 350
    q = np.percentile(hs[big], [5, 25, 50, 75, 95]) if big.any() else []
    dens = areas / np.maximum(hs * ws, 1)
    rune = ((hs >= 90) & (hs <= 135) & (areas >= 350) & (ws <= 120)
            & ((ws >= 12) | (dens >= 0.7)))
    tl = lines_of(page); want = [len(ln) for ln in tl]
    cl = cluster_cy(cys[rune])
    reasons = []
    gidx = np.where(rune)[0]
    for i, c in enumerate(cl):
        if i >= len(want): break
        s = len(c); w = want[i]
        reasons.append("OK" if s == w else f"l{i}:{s}/{w}")
    extra = len(want) - len(cl)
    print(f"p{page}: h[big] p5/25/50/75/95={[int(x) for x in q]} "
          f"clusters={len(cl)} want_k={len(want)} (missing {extra}) "
          + " ".join(reasons))

if __name__ == "__main__":
    for p in (47, 48, 49, 51, 53, 55, 44, 15, 40):
        diag(p)
