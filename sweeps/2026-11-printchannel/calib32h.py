#!/usr/bin/env python3
"""#32 PRE-OUTPUT calibration v8: anatomy of v7's FAILED lines.
For each failed line: accepted comp widths, pixel x-projection segments
(zero-ink columns) within the line's core rows, segment heights/widths.
Decides whether projection-split can fix unders and what overs are."""
import os, sys
import numpy as np
from PIL import Image
from scipy import ndimage
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from calib32b import components, cluster, lines_of
from calib32g import extract

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def ink_mask(page):
    a = np.array(Image.open(f"{ROOT}/work/images/{page}.jpg").convert("RGB"),
                 dtype=np.int16)
    R, G, B = a[..., 0], a[..., 1], a[..., 2]
    lum = (a * (0.299, 0.587, 0.114)).sum(-1)
    redness = R - np.minimum(G, B)
    hist, _ = np.histogram(lum, bins=256, range=(0, 256))
    tot = hist.sum(); best = (0, -1.0); w0 = 0.0; s0 = 0.0
    muT = sum(i * hist[i] for i in range(256))
    for t in range(256):
        w0 += hist[t]
        if w0 == 0 or w0 == tot: continue
        s0 += t * hist[t]
        m0 = s0 / w0; m1 = (muT - s0) / (tot - w0)
        v = w0 * (tot - w0) * (m0 - m1) ** 2
        if v > best[1]: best = (t, v)
    return (lum <= best[0]) & (redness < 45)

def page_fails(page):
    hs, ws, areas, cys, cxs, rune, frag = extract(page)
    ink = ink_mask(page)
    tl = lines_of(page); want = [len(ln) for ln in tl]
    cl = [c for c in cluster(cys[rune], 90) if len(c) >= 3]
    gidx = np.where(rune)[0]
    for i, c in enumerate(cl):
        g = gidx[c]; w = want[i] if i < len(want) else -1
        if len(g) == w: continue
        lo = int(cys[g].min()) - 35; hi = int(cys[g].max()) + 35
        core = ink[lo:hi]
        col = core.sum(0)
        segs = []; inb = False
        for x, v in enumerate(col):
            if v > 0 and not inb: sx = x; inb = True
            elif v == 0 and inb:
                if x - sx >= 3: segs.append((sx, x))
                inb = False
        seginfo = []
        for (sx, ex) in segs:
            sub = core[:, sx:ex]
            rows = np.where(sub.sum(1) > 0)[0]
            h = rows.max() - rows.min() + 1 if len(rows) else 0
            seginfo.append((ex - sx, h, int(sub.sum())))
        big = [s for s in seginfo if s[1] >= 60]
        print(f"p{page} l{i}: want={w} comps={len(g)} segs={len(segs)} "
              f"bigsegs(h>=60)={len(big)}")
        print(f"   comp_w={sorted(int(ws[j]) for j in g)}")
        print(f"   segs(w,h,area)={seginfo}")

if __name__ == "__main__":
    for p in (0, 7, 26, 40, 15):
        page_fails(p)
