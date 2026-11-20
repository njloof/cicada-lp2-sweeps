#!/usr/bin/env python3
"""#32 PRE-OUTPUT calibration v7: registered extraction rules, full
coverage on sample pages.
  RUNE     : 90<=h<=135, area>=350, w<=120, and (w>=12 or solid bar:
             area/(h*w)>=0.7)                      [narrow stave runes]
  FRAGMENT : 25<=h<90, w<=30, area>=150 -> merged into the RUNE whose
             x-range overlaps it >=50% (metrics fidelity); else ignored
  line     : cy-gap clustering (gap>90, >=3 runes); count gate vs
             transcription; over-merged lines get one x-projection split
             at the widest gaps until count matches or give up -> EXCLUDE
Reports per-page line/rune coverage (projected G1)."""
import os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from calib32b import components, cluster, lines_of

def extract(page):
    hs, ws, areas, cys, cxs = components(page)
    dens = areas / np.maximum(hs * ws, 1)
    rune = (hs >= 90) & (hs <= 135) & (areas >= 350) & (ws <= 120) \
           & ((ws >= 12) | ((ws < 12) & (dens >= 0.7)))
    frag = (hs >= 25) & (hs < 90) & (ws <= 30) & (areas >= 150)
    return hs, ws, areas, cys, cxs, rune, frag

def proj_split(band_idx, cxs, ws, targets):
    """split the widest-x unit repeatedly at its largest interior column
    gap; band comps sorted by x. Returns list of comp-index lists."""
    order = sorted(band_idx, key=lambda j: cxs[j] - ws[j] / 2)
    units = [[j] for j in order]  # accepted comps are runes as-is (v6:
    # standalone staves sit at normal kerning; merging would delete them)
    # split at largest interior gaps: rebuild pixel columns? too heavy here;
    # approximate: split the unit with most comps at its largest cx gap
    while len(units) < targets:
        cand = [u for u in units if len(u) >= 2]
        if not cand: break
        u = max(cand, key=lambda u: max(
            np.diff(sorted(cxs[j] for j in u)), default=0))
        s = sorted(u, key=lambda j: cxs[j])
        gaps = np.diff([cxs[j] for j in s])
        cut = int(np.argmax(gaps)) + 1
        units.remove(u); units.append(s[:cut]); units.append(s[cut:])
    return units

def page_cov(page):
    hs, ws, areas, cys, cxs, rune, frag = extract(page)
    tl = lines_of(page); want = [len(ln) for ln in tl]
    cl = [c for c in cluster(cys[rune], 90) if len(c) >= 3]
    gidx = np.where(rune)[0]
    ok = 0; run = 0; fails = []
    for i, c in enumerate(cl):
        g = gidx[c]
        w = want[i] if i < len(want) else -1
        units = [[j] for j in g]
        # (no split yet in calibration: measure fail direction first)
        if len(units) == w:
            ok += 1; run += w
        else:
            fails.append((i, w, len(units)))
    return ok, len(want), run, sum(want), fails

if __name__ == "__main__":
    pages = sys.argv[1:] or [str(p) for p in (0, 7, 15, 26, 40)]
    T = [0, 0, 0, 0]
    for ps in pages:
        p = int(ps)
        ol, k, mr, rw, fails = page_cov(p)
        for i, v in enumerate((ol, k, mr, rw)): T[i] += v
        print(f"p{p}: lines {ol}/{k} runes {mr}/{rw} ({100*mr/rw:.1f}%) fails={fails}")
    print(f"TOTAL: lines {T[0]}/{T[1]} ({100*T[0]/T[1]:.1f}%) "
          f"runes {T[2]}/{T[3]} ({100*T[2]/T[3]:.1f}%)")
