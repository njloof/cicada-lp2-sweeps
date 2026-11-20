#!/usr/bin/env python3
"""#32 table32: extract per-rune print metrics for all unsolved pages.
Registered rules: PREREG.md sections 1 + 1b (RUNE component rule, cy-gap
clustering with sanity split, comp-count gate, one projection-split
attempt with marginalia filter, per-line EXCLUDE). Gates G1 (coverage),
G2 (brute-force machinery), G3 run separately (core.validate).
Full table -> work/table32.jsonl (studio, never git); summary ->
results/coverage32.json (small)."""
import json, os, sys
import numpy as np
from PIL import Image
from scipy import ndimage

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
IMG = os.path.join(ROOT, "work", "images")
UNSOLVED = [p for p in range(56) if p != 50 and os.path.exists(
    f"{ROOT}/data/pages/lp2_{p:02d}.txt")]
METRICS = ("fx", "fy", "cx", "cy", "w", "h", "area", "gap")

def lines_of(page):
    f = f"{ROOT}/data/pages/lp2_{page:02d}.txt"
    return [[int(x) for x in ln.split()] for ln in open(f).read().splitlines()
            if ln.strip()]

def ink_and_mask(page):
    a = np.array(Image.open(os.path.join(IMG, f"{page}.jpg")).convert("RGB"),
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

def cluster_cy(cy):
    """cy-gap clustering (>90) + one sanity split for spread>80."""
    if len(cy) == 0: return []
    o = np.argsort(cy); v = cy[o]
    parts = np.split(o, np.where(np.diff(v) > 90)[0] + 1)
    out = []
    for p in parts:
        s = p[np.argsort(cy[p])]
        if len(s) >= 3 and (cy[s].max() - cy[s].min()) > 80:
            g = np.diff(cy[s]); c = int(np.argmax(g))
            if g[c] > 60:
                out.append(np.sort(s[:c + 1])); out.append(np.sort(s[c + 1:]))
                continue
        out.append(np.sort(p))
    return [c for c in out if len(c) >= 3]

def seg_metrics(ink, lo, hi, sx, ex, lab=None, lid=0):
    sub = ink[lo:hi, sx:ex]
    if lab is not None:
        sub = lab[lo:hi, sx:ex] == lid
    ys, xs = np.nonzero(sub)
    if len(ys) == 0: return None
    return dict(area=float(len(ys)),
                cx=float(xs.mean() + sx), cy=float(ys.mean() + lo),
                w=float(xs.max() - xs.min() + 1),
                h=float(ys.max() - ys.min() + 1),
                x0=float(xs.min() + sx), x1=float(xs.max() + sx + 1))

def extract_page(page):
    """returns (rows, want_total). rows: dicts with page/line/pos/value +
    metrics + mode."""
    ink = ink_and_mask(page)
    lab, n = ndimage.label(ink, structure=np.ones((3, 3)))
    if n == 0: return [], 0
    objs = ndimage.find_objects(lab)
    areas = np.bincount(lab.ravel(), minlength=n + 1)[1:].astype(float)
    hs = np.array([o[0].stop - o[0].start for o in objs], dtype=float)
    ws = np.array([o[1].stop - o[1].start for o in objs], dtype=float)
    cys = np.array([(o[0].start + o[0].stop - 1) / 2 for o in objs])
    cxs = np.array([(o[1].start + o[1].stop - 1) / 2 for o in objs])
    dens = areas / np.maximum(hs * ws, 1)
    rune = ((hs >= 90) & (hs <= 135) & (areas >= 350) & (ws <= 120)
            & ((ws >= 12) | (dens >= 0.7)))
    tl = lines_of(page)
    want = [len(ln) for ln in tl]
    gidx = np.where(rune)[0]
    cl = cluster_cy(cys[rune])
    rows = []
    for i, c in enumerate(cl):
        if i >= len(tl): break
        g = gidx[c]
        w_i = want[i]
        lo = int(cys[g].min()) - 60; hi = int(cys[g].max()) + 61
        units = None; mode = None
        if len(g) == w_i:                                   # comp mode
            mode = "comp"
            units = []
            for j in g:
                o = objs[j]
                m = seg_metrics(ink, o[0].start, o[0].stop,
                                o[1].start, o[1].stop, lab=lab, lid=j + 1)
                if m: units.append(m)
        else:                                               # segment mode
            core = ink[lo:hi]
            col = core.sum(0)
            segs = []; inb = False
            for x, vv in enumerate(col):
                if vv > 0 and not inb: sx = x; inb = True
                elif vv == 0 and inb:
                    if x - sx >= 3: segs.append((sx, x))
                    inb = False
            keep = []
            for (sx, ex) in segs:
                m = seg_metrics(ink, lo, hi, sx, ex)
                if m is None or m["h"] < 60 or m["area"] < 350: continue
                if m["w"] >= 60 and m["area"] / (m["w"] * m["h"]) <= 0.25:
                    continue                                # marginalia
                keep.append(m)
            if len(keep) == w_i:
                mode = "seg"; units = keep
        if units is None: continue
        units.sort(key=lambda m: m["cx"])
        prev_x1 = None
        for pos, m in enumerate(units):
            gap = np.nan if prev_x1 is None else m["x0"] - prev_x1
            prev_x1 = m["x1"]
            rows.append(dict(page=page, line=i, pos=pos, value=tl[i][pos],
                             mode=mode, cx=m["cx"], cy=m["cy"],
                             fx=m["cx"] % 1.0, fy=m["cy"] % 1.0,
                             w=m["w"], h=m["h"], area=m["area"],
                             gap=float(gap)))
    return rows, sum(want)

def main():
    all_rows = []; cov = {}; tot = 0; aligned = 0
    for page in UNSOLVED:
        rows, want = extract_page(page)
        all_rows.extend(rows)
        cov[page] = {"want": want, "aligned": len(rows)}
        tot += want; aligned += len(rows)
        print(f"p{page}: {len(rows)}/{want}", flush=True)
    out = os.path.join(ROOT, "work", "table32.jsonl")
    with open(out, "w") as f:
        for r in all_rows:
            f.write(json.dumps(r) + "\n")
    cov["_total"] = {"want": tot, "aligned": aligned,
                     "pct": 100.0 * aligned / tot}
    json.dump(cov, open(os.path.join(HERE, "results", "coverage32.json"),
                        "w"), indent=1)
    g1 = aligned / tot >= 0.95
    print(f"G1: coverage {aligned}/{tot} = {100*aligned/tot:.2f}% "
          f"{'PASS' if g1 else 'FAIL (see escalation)'}")
    # ---- G2: brute-force machinery check on 3 random clean lines
    rng = np.random.default_rng(20261232)
    byl = {}
    for k, r in enumerate(all_rows):
        byl.setdefault((r["page"], r["line"], r["mode"]), []).append(k)
    keys = [k for k in byl if len(byl[k]) >= 5]
    picks = [keys[i] for i in rng.choice(len(keys), 3, replace=False)]
    worst = 0.0; n_checked = 0
    for (pg, ln, mode) in picks:
        ink = ink_and_mask(pg)
        lab, n = ndimage.label(ink, structure=np.ones((3, 3)))
        for k in byl[(pg, ln, mode)]:
            r = all_rows[k]
            cy0, cx0 = int(round(r["cy"])), int(round(r["cx"]))
            if mode == "comp":
                # brute force: component id at centroid (5x5 fallback),
                # pixel loop over its mask
                lid = 0
                for dy in range(-3, 4):
                    for dx in range(-3, 4):
                        lid = lab[cy0 + dy, cx0 + dx]
                        if lid: break
                    if lid: break
                assert lid, f"G2: no ink near centroid p{pg} l{ln}"
                ys, xs = np.nonzero(lab == lid)
            else:
                x0 = int(np.floor(r["cx"] - r["w"] / 2)) - 2
                x1 = int(np.ceil(r["cx"] + r["w"] / 2)) + 3
                y0 = int(np.floor(r["cy"] - r["h"] / 2)) - 2
                y1 = int(np.ceil(r["cy"] + r["h"] / 2)) + 3
                sub = ink[y0:y1, x0:x1]
                ys, xs = np.nonzero(sub)
                xs = xs + x0; ys = ys + y0
            e = max(abs(xs.mean() - r["cx"]), abs(ys.mean() - r["cy"]),
                    abs(len(ys) - r["area"]))
            worst = max(worst, e); n_checked += 1
    print(f"G2: {n_checked} runes checked on 3 lines; worst deviation "
          f"{worst:.2e} {'PASS' if worst < 0.5 else 'FAIL'} "
          f"(tol 0.5 px centroid / exact px count)")

if __name__ == "__main__":
    os.makedirs(os.path.join(HERE, "results"), exist_ok=True)
    main()
