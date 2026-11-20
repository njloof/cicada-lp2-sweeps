#!/usr/bin/env python3
"""#32 PRE-OUTPUT calibration v4: x-merge fragments into rune UNITS.
Findings so far: dots h~10 (inter-word, correctly excluded); runes often
split into vertical fragments (h~114 w~9 strokes; h~58 half-strokes at
cy+28). Within each line band: take comps with h>=30 (kills dots), sane
size (kills background blobs), merge comps whose x-ranges are within
MG px, count units vs transcription. Also report unit width distribution
(bimodal tail = merged pairs) and dx to nearest neighbor."""
import os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from calib32b import components, cluster, lines_of

def units_in_band(ix, cxs, ws, hs, areas, MG):
    """merge comps (indices ix within band) by x-proximity; return list of
    (cx_weighted, x0, x1, h_max, area_sum, n_frag)."""
    order = np.argsort(cxs[ix] - ws[ix] / 2)  # by left edge
    out = []
    for j in order:
        x0 = cxs[j] - ws[j] / 2; x1 = cxs[j] + ws[j] / 2
        if out and x0 - out[-1][2] <= MG:
            u = out[-1]
            n, sx, xa, xb, hm, ar = u
            out[-1] = (n + 1, sx + cxs[j] * areas[j], min(xa, x0),
                       max(xb, x1), max(hm, hs[j]), ar + areas[j])
        else:
            out.append((1, cxs[j] * areas[j], x0, x1, hs[j], areas[j]))
    return [(sx / ar, xa, xb, hm, ar, n) for (n, sx, xa, xb, hm, ar) in out]

def page_report(page, MG=6):
    hs, ws, areas, cys, cxs = components(page)
    cand = (hs >= 90) & (hs <= 135) & (ws >= 12) & (ws <= 120) & (areas >= 400)
    tl = lines_of(page); want = [len(ln) for ln in tl]
    cl = [c for c in cluster(cys[cand], 90) if len(c) >= 3]
    gidx = np.where(cand)[0]
    ok = 0; run = 0
    uw = []; nh = []
    for i, c in enumerate(cl):
        g = gidx[c]
        lo = cys[g].min() - 35; hi = cys[g].max() + 35
        band = np.where((cys >= lo) & (cys < hi) & (hs >= 30) & (hs <= 140)
                        & (areas >= 200) & (ws <= 130))[0]
        u = units_in_band(band, cxs, ws, hs, areas, MG)
        w = want[i] if i < len(want) else -1
        m = "OK " if len(u) == w else "MISS"
        ok += len(u) == w; run += min(len(u), max(w, 0))
        for (cx, x0, x1, hm, ar, nfr) in u:
            uw.append(x1 - x0); nh.append(nfr)
        if len(u) != w:
            print(f" p{page} line{i} {m}: want={w} units={len(u)} "
                  f"widths={[round(x[2]-x[1]) for x in u]}")
    uw = np.array(uw)
    print(f"p{page}: lines {ok}/{len(cl)} units-runes {run}/{sum(want)} "
          f"unitw pct(5,50,95,99,max)={[int(q) for q in np.percentile(uw,[5,50,95,99])],int(uw.max())} "
          f"frags/unit pct(50,95,max)={[int(q) for q in np.percentile(nh,[50,95])],int(max(nh))}")
    return ok, len(cl), run, sum(want)

if __name__ == "__main__":
    T = [0, 0, 0, 0]
    for p in (0, 7, 15, 26, 40):
        for i, v in enumerate(page_report(p)):
            T[i] += v
    print(f"TOTAL: lines {T[0]}/{T[1]} runes {T[2]}/{T[3]} ({100*T[2]/T[3]:.1f}%)")
