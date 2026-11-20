#!/usr/bin/env python3
"""#32 PRE-OUTPUT calibration v3: what does the v2 filter DROP?
Anchor lines with v2 candidates, then for each line list ALL components
whose cy falls in the line's y-range, split accepted/dropped, and show
the dropped ones' h/w/area so the filter can be fixed before any test."""
import os
import numpy as np
from PIL import Image
from scipy import ndimage
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from calib32b import components, cluster, lines_of

def page_report(page, G=90):
    hs, ws, areas, cys, cxs = components(page)
    cand = (hs >= 90) & (hs <= 135) & (ws >= 12) & (ws <= 120) & (areas >= 400)
    tl = lines_of(page); want = [len(ln) for ln in tl]
    cl = cluster(cys[cand], G)
    cl = [c for c in cl if len(c) >= 3]
    # map candidate indices back to global comp indices
    gidx = np.where(cand)[0]
    print(f"--- p{page}: {len(cl)} anchor clusters, want k={len(want)}")
    for i, c in enumerate(cl[:12]):
        g = gidx[c]
        lo = cys[g].min() - 35; hi = cys[g].max() + 35
        inband = np.where((cys >= lo) & (cys < hi))[0]
        acc = inband[cand[inband]]; drp = inband[~cand[inband]]
        w = want[i] if i < len(want) else -1
        flag = "" if len(acc) == w else "  <<< MISMATCH"
        print(f" line{i}: want={w} acc={len(acc)} drop={len(drp)}{flag}")
        for j in drp[:10]:
            print(f"   DROP id={j} h={hs[j]:.0f} w={ws[j]:.0f} area={areas[j]:.0f} "
                  f"cx={cxs[j]:.0f} cy={cys[j]:.0f}")

if __name__ == "__main__":
    for p in (0, 15, 7):
        page_report(p)
