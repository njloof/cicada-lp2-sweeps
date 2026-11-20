#!/usr/bin/env python3
"""#32 PRE-OUTPUT calibration v2 (engineering only, no statistic).

v1 finding: y-projection bands merge/split lines badly (inter-line ink
never drops below threshold; ornaments create spurious bands). But glyph
height is near-constant (~114-115 px, uniform print), so line structure
is recoverable from component y-CENTROIDS instead.

v2 rules under calibration:
  candidate = dark, non-red component with h in [90,135], 12<=w<=120,
              area>=400                      (kills dots, separators,
                                              merged blobs, ornaments)
  lines     = cluster candidate cy values, split at consecutive gaps > G
              (G grid {70, 90, 110}); expect k == transcription line count
  match     = cluster size == that line's rune count (in order)
Reports per-page cluster/line agreement + projected G1 coverage.
"""
import json, os
import numpy as np
from PIL import Image
from scipy import ndimage

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
IMG = os.path.join(ROOT, "work", "images")

def lines_of(page):
    f = f"{ROOT}/data/pages/lp2_{page:02d}.txt"
    return [ln.split() for ln in open(f).read().splitlines() if ln.strip()]

def components(page):
    a = np.array(Image.open(os.path.join(IMG, f"{page}.jpg")).convert("RGB"),
                 dtype=np.int16)
    R, G, B = a[..., 0], a[..., 1], a[..., 2]
    lum = (a * (0.299, 0.587, 0.114)).sum(-1)
    redness = R - np.minimum(G, B)
    hist, _ = np.histogram(lum, bins=256, range=(0, 256))
    tot = hist.sum(); best = (0, -1.0)
    w0 = 0.0; s0 = 0.0
    muT = sum(i * hist[i] for i in range(256))
    for t in range(256):
        w0 += hist[t]
        if w0 == 0 or w0 == tot: continue
        s0 += t * hist[t]
        m0 = s0 / w0; m1 = (muT - s0) / (tot - w0)
        v = w0 * (tot - w0) * (m0 - m1) ** 2
        if v > best[1]: best = (t, v)
    ink = (lum <= best[0]) & (redness < 45)
    lab, n = ndimage.label(ink, structure=np.ones((3, 3)))
    objs = ndimage.find_objects(lab)
    areas = np.array(ndimage.sum(ink, lab, range(1, n + 1)))
    hs = np.array([o[0].stop - o[0].start for o in objs], dtype=float)
    ws = np.array([o[1].stop - o[1].start for o in objs], dtype=float)
    cys = np.array([(o[0].start + o[0].stop - 1) / 2 for o in objs])
    cxs = np.array([(o[1].start + o[1].stop - 1) / 2 for o in objs])
    return hs, ws, areas, cys, cxs

def cluster(cy, gaps):
    o = np.argsort(cy); v = cy[o]
    cuts = np.where(np.diff(v) > gaps)[0]
    parts = np.split(o, cuts + 1)
    return [np.sort(p) for p in parts]

def page_report(page, G):
    hs, ws, areas, cys, cxs = components(page)
    cand = (hs >= 90) & (hs <= 135) & (ws >= 12) & (ws <= 120) & (areas >= 400)
    tl = lines_of(page)
    k = len(tl); want = [len(ln) for ln in tl]
    cl = cluster(cys[cand], G)
    sizes = [len(c) for c in cl]
    # trim tiny clusters (<3 comps) = stray marks
    cl = [c for c in cl if len(c) >= 3]; sizes = [len(c) for c in cl]
    ok_lines = sum(1 for i, s in enumerate(sizes)
                   if i < k and s == want[i])
    matched_runes = sum(min(s, want[i]) if i < k else 0
                        for i, s in enumerate(sizes))
    print(f"p{page} G={G}: cand={int(cand.sum())}/{len(hs)} clusters={len(cl)} "
          f"(k={k}) exact-line-match={ok_lines}/{k} runes~{matched_runes}/{sum(want)}")
    print(f"   sizes={sizes}")
    print(f"   want={want}")
    return ok_lines, k, matched_runes, sum(want)

if __name__ == "__main__":
    tot = {G: [0, 0, 0, 0] for G in (70, 90, 110)}
    for p in (0, 7, 15, 26, 40):
        for G in (70, 90, 110):
            ol, k, mr, rw = page_report(p, G)
            tot[G][0] += ol; tot[G][1] += k; tot[G][2] += mr; tot[G][3] += rw
    for G in (70, 90, 110):
        ol, k, mr, rw = tot[G]
        print(f"G={G}: lines {ol}/{k} ({100*ol/max(k,1):.0f}%) "
              f"runes {mr}/{rw} ({100*mr/max(rw,1):.0f}%)")
