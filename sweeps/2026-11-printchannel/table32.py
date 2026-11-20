#!/usr/bin/env python3
"""#32 table32: extract per-rune print metrics for all unsolved pages.
Registered rules: PREREG.md sections 1 + 1b (RUNE component rule, cy-gap
clustering with sanity split, comp-count gate, one projection-split
attempt with marginalia filter, FRAGMENT merge into overlapping rune,
per-line EXCLUDE). Gates G1 (coverage), G2 (brute-force machinery,
tol 1e-6), G3 run separately (core.validate).
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

def metrics_from(ys, xs, lid, x0b, x1b, y0b, y1b, blo, bhi):
    return dict(area=float(len(ys)), cx=float(xs.mean()), cy=float(ys.mean()),
                w=float(xs.max() - xs.min() + 1),
                h=float(ys.max() - ys.min() + 1),
                x0=float(xs.min()), x1=float(xs.max() + 1),
                lid=lid, x0b=x0b, x1b=x1b, y0b=y0b, y1b=y1b,
                blo=blo, bhi=bhi)

def extract_page(page):
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
    frag = (hs >= 25) & (hs < 90) & (ws <= 30) & (areas >= 150)
    tl = lines_of(page)
    want = [len(ln) for ln in tl]
    gidx = np.where(rune)[0]
    fidx = np.where(frag)[0]
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
                y0, y1, x0, x1 = (o[0].start, o[0].stop,
                                  o[1].start, o[1].stop)
                ys, xs = np.nonzero(lab[y0:y1, x0:x1] == j + 1)
                ys = ys + y0; xs = xs + x0
                if len(ys) == 0: continue
                # registered FRAGMENT merge: frags whose bbox intersects
                # the band and whose x-range overlaps the rune bbox >=50%
                for fj in fidx:
                    fo = objs[fj]
                    fy0, fy1 = fo[0].start, fo[0].stop
                    fx0, fx1 = fo[1].start, fo[1].stop
                    if fy1 <= lo or fy0 >= hi: continue
                    if min(fx1, x1) - max(fx0, x0) < 0.5 * (fx1 - fx0):
                        continue
                    a2, b2 = np.nonzero(lab[fy0:fy1, fx0:fx1] == fj + 1)
                    ys = np.concatenate([ys, a2 + fy0])
                    xs = np.concatenate([xs, b2 + fx0])
                units.append(metrics_from(ys, xs, int(j) + 1, x0, x1, y0, y1,
                                          lo, hi))
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
                ys, xs = np.nonzero(ink[lo:hi, sx:ex])
                if len(ys) == 0: continue
                ys = ys + lo; xs = xs + sx
                m = metrics_from(ys, xs, 0, int(xs.min()),
                                 int(xs.max() + 1), int(ys.min()),
                                 int(ys.max() + 1), lo, hi)
                if m["h"] < 60 or m["area"] < 350: continue
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
                             gap=float(gap), lid=m["lid"],
                             x0b=m["x0b"], x1b=m["x1b"], y0b=m["y0b"],
                             y1b=m["y1b"], blo=m["blo"], bhi=m["bhi"]))
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
    # ---- G2: brute-force machinery (naive pixel loops, registered tol
    # 1e-6) on 3 random clean lines; re-implements the fragment rule
    # independently of the vectorized pipeline.
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
            x0, x1 = r["x0b"], r["x1b"]
            y0, y1 = r["y0b"], r["y1b"]
            sx = 0; sy = 0; cnt = 0
            if mode == "comp":
                # scan base bbox + fragment reach; naive loop per pixel
                pix = {}
                for y in range(max(y0 - 90, 0), min(y1 + 90, lab.shape[0])):
                    for x in range(max(x0 - 40, 0),
                                   min(x1 + 40, lab.shape[1])):
                        v = int(lab[y, x])
                        if v: pix.setdefault(v, []).append((y, x))
                sel = list(pix.get(r["lid"], []))
                for v, px in pix.items():
                    if v == r["lid"]: continue
                    fy = [p[0] for p in px]; fx = [p[1] for p in px]
                    fh = max(fy) - min(fy) + 1
                    fw = max(fx) - min(fx) + 1
                    if not (25 <= fh < 90 and fw <= 30 and len(px) >= 150):
                        continue
                    if max(fy) + 1 <= r["blo"] or min(fy) >= r["bhi"]:
                        continue
                    ov = min(max(fx) + 1, x1) - max(min(fx), x0)
                    if ov >= 0.5 * fw: sel.extend(px)
            else:
                sel = [(y, x) for y in range(y0, y1)
                       for x in range(x0, x1) if ink[y, x]]
            if not sel:
                worst = float("inf"); continue
            for (y, x) in sel:
                sy += y; sx += x; cnt += 1
            e = max(abs(sx / cnt - r["cx"]), abs(sy / cnt - r["cy"]),
                    abs(cnt - r["area"]))
            if e > 1e-6:
                print(f"  G2 dev p{pg} l{ln} {mode} k{k} "
                      f"stored(a={r['area']:.0f},cx={r['cx']:.4f},"
                      f"cy={r['cy']:.4f}) brute(a={cnt},cx={sx/cnt:.4f},"
                      f"cy={sy/cnt:.4f}) e={e:.3g}")
            worst = max(worst, e); n_checked += 1
    print(f"G2: {n_checked} runes on 3 lines; worst deviation {worst:.3g} "
          f"{'PASS' if worst <= 1e-6 else 'FAIL'} (registered tol 1e-6)")

if __name__ == "__main__":
    os.makedirs(os.path.join(HERE, "results"), exist_ok=True)
    main()
