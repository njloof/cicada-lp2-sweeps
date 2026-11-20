#!/usr/bin/env python3
"""#32 PRE-OUTPUT calibration v6: adjacency anatomy per line.
Question: are the dropped h~114 w~9 strokes fragments of neighbours
(small dx to an accepted body) or standalone narrow runes (dx ~ kerning)?
Prints the full left->right sequence per line: accepted as [w], dropped
with h/w, so the merge rule can be registered from observation."""
import os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from calib32b import components, cluster, lines_of

def page_report(page):
    hs, ws, areas, cys, cxs = components(page)
    cand = (hs >= 90) & (hs <= 135) & (ws >= 12) & (ws <= 120) & (areas >= 400)
    tl = lines_of(page); want = [len(ln) for ln in tl]
    cl = [c for c in cluster(cys[cand], 90) if len(c) >= 3]
    gidx = np.where(cand)[0]
    print(f"--- p{page}")
    for i, c in enumerate(cl[:4]):
        g = gidx[c]
        lo = cys[g].min() - 35; hi = cys[g].max() + 35
        band = np.where((cys >= lo) & (cys < hi) & (hs >= 25) & (hs <= 140)
                        & (areas >= 150) & (ws <= 130))[0]
        seq = []
        for j in band[np.argsort(cxs[band])]:
            if cand[j]:
                seq.append(f"[{ws[j]:.0f}]")
            else:
                seq.append(f"({hs[j]:.0f}x{ws[j]:.0f}:{areas[j]:.0f})")
        w = want[i] if i < len(want) else -1
        print(f" line{i} want={w} acc={int(cand[band].sum())} :: " + " ".join(seq))

if __name__ == "__main__":
    for p in (0, 7, 26):
        page_report(p)
