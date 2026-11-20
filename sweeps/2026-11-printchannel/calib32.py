#!/usr/bin/env python3
"""#32 PRE-OUTPUT calibration: inspect binarization + component structure on
sample pages so extraction rules get registered before any test. Engineering
diagnostics only — no statistic touches the corpus."""
import glob, json, os
import numpy as np
from PIL import Image
from scipy import ndimage

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
IMG = os.path.join(ROOT, "work", "images")

def lines_of(page):
    f = f"{ROOT}/data/pages/lp2_{page:02d}.txt"
    return [len(ln.split()) for ln in open(f).read().splitlines() if ln.strip()]

def page_report(page):
    a = np.array(Image.open(os.path.join(IMG, f"{page}.jpg")).convert("RGB"), dtype=np.int16)
    R, G, B = a[..., 0], a[..., 1], a[..., 2]
    lum = (a * (0.299, 0.587, 0.114)).sum(-1)
    redness = R - np.minimum(G, B)
    # Otsu on luminance
    hist, _ = np.histogram(lum, bins=256, range=(0, 256))
    tot = hist.sum(); best = (0, -1)
    w0 = 0.0; s0 = 0.0; muT = sum(i * hist[i] for i in range(256))
    for t in range(256):
        w0 += hist[t]
        if w0 == 0 or w0 == tot: continue
        s0 += t * hist[t]
        m0 = s0 / w0; m1 = (muT - s0) / (tot - w0)
        v = w0 * (tot - w0) * (m0 - m1) ** 2
        if v > best[1]: best = (t, v)
    T = best[0]
    ink = (lum <= T) & (redness < 45)          # dark, not red
    lab, n = ndimage.label(ink, structure=np.ones((3, 3)))
    objs = ndimage.find_objects(lab)
    areas = ndimage.sum(ink, lab, range(1, n + 1))
    hs = np.array([o[0].stop - o[0].start for o in objs])
    ws = np.array([o[1].stop - o[1].start for o in objs])
    ys = np.array([(o[0].start + o[0].stop) / 2 for o in objs])
    tl = lines_of(page)
    # y-projection line bands
    proj = ink.sum(1)
    bands = []; inb = False
    for y, v in enumerate(proj):
        if v > 2 and not inb: st = y; inb = True
        elif v <= 2 and inb:
            if y - st > 15: bands.append((st, y))
            inb = False
    print(f"--- page {page}: shape {a.shape[:2]} Otsu T={T} comps={n} "
          f"bands={len(bands)} transcr_lines={len(tl)} runes={sum(tl)}")
    for nm, arr in (("area", areas), ("height", hs), ("width", ws)):
        q = np.percentile(arr, [1, 5, 25, 50, 75, 95, 99])
        print(f"  {nm} pct(1,5,25,50,75,95,99) = {[int(x) for x in q]}")
    # per-band component counts vs line rune counts (first 8 lines)
    big = (hs >= 25)
    for bi, (s, e) in enumerate(bands[:8]):
        m = (ys >= s) & (ys < e)
        print(f"  band{bi} y[{s}:{e}] h={e-s} comps={int(m.sum())} big={int((m&big).sum())} "
              f"transcr={tl[bi] if bi < len(tl) else '?'}")
    return T

if __name__ == "__main__":
    for p in (0, 7, 15, 26, 40):
        page_report(p)
