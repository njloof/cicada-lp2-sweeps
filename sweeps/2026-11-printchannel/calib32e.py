#!/usr/bin/env python3
"""#32 PRE-OUTPUT calibration v5: DILATE-then-label.
v1-v4 findings: runes split into fragments (vertical strokes w~9, half
strokes h~58) 1-3 px apart; x-merging chains through ornaments. Fix:
binary_dilation(k) before labeling merges near-touching fragments into
one component while normal kerning (>=10 px) keeps runes separate.
Grid: k in {1,2,3}. Coverage = aligned runes / transcription runes on
sample pages (lines must match transcription count to count)."""
import os, sys
import numpy as np
from PIL import Image
from scipy import ndimage
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from calib32b import lines_of

def comps_dil(page, k):
    a = np.array(Image.open(
        f"{os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))}/work/images/{page}.jpg"
    ).convert("RGB"), dtype=np.int16)
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
    ink = (lum <= best[0]) & (redness < 45)
    if k: ink = ndimage.binary_dilation(ink, iterations=k)
    lab, n = ndimage.label(ink, structure=np.ones((3, 3)))
    objs = ndimage.find_objects(lab)
    # measure on ORIGINAL ink restricted to each dilated label
    lab0 = ndimage.label((lum <= best[0]) & (redness < 45),
                         structure=np.ones((3, 3)))[0]
    # count ORIGINAL-ink pixels per dilated label
    ink0 = (lab0 > 0)
    areas = np.bincount(lab[ink0], minlength=n + 1)[1:].astype(float) \
        if n else np.zeros(n)
    hs = np.array([o[0].stop - o[0].start for o in objs], dtype=float) - 2 * k
    ws = np.array([o[1].stop - o[1].start for o in objs], dtype=float) - 2 * k
    cys = np.array([(o[0].start + o[0].stop - 1) / 2 for o in objs])
    cxs = np.array([(o[1].start + o[1].stop - 1) / 2 for o in objs])
    return hs, ws, areas, cys, cxs

def report(page, k):
    hs, ws, areas, cys, cxs = comps_dil(page, k)
    good = (hs >= 85) & (hs <= 145) & (ws >= 8) & (ws <= 125) & (areas >= 350)
    tl = lines_of(page); want = [len(ln) for ln in tl]
    o = np.argsort(cys[good]); v = cys[good][o]
    cuts = np.where(np.diff(v) > 90)[0]
    cl = [np.sort(g) for g in np.split(o, cuts + 1)]
    cl = [c for c in cl if len(c) >= 3]
    gidx = np.where(good)[0]
    ok = 0; run = 0; miss = []
    for i, c in enumerate(cl):
        s = len(c); w = want[i] if i < len(want) else -1
        ok += s == w; run += min(s, max(w, 0))
        if s != w: miss.append((i, w, s))
    print(f"p{page} k={k}: clusters={len(cl)}/{len(want)} lines_ok={ok} "
          f"runes {run}/{sum(want)} ({100*run/sum(want):.1f}%) miss={miss}")
    return ok, len(cl), run, sum(want)

if __name__ == "__main__":
    for k in (1, 2, 3):
        T = [0, 0, 0, 0]
        for p in (0, 7, 15, 26, 40):
            for i, x in enumerate(report(p, k)): T[i] += x
        print(f"== k={k}: lines {T[0]}/{T[1]} runes {T[2]}/{T[3]} "
              f"({100*T[2]/T[3]:.1f}%)")
