#!/usr/bin/env python3
"""Campaign #12 / F18 — in-document OTP consumption (PB1 page->blob reverse
scan). Registration: PREREG.md (d478ca9) as amended by PREREG2.md (60d2857)
BEFORE any output: windowed chi2 (W=60, stride=30), derive-from-shuffled
null, seed 20261201, escalation 20->200, plants 10, alpha 0.05.

Usage: python3 f18.py [--stage 20] [--out results/f18_results.json]
"""
import argparse
import hashlib
import json
import os
import sys
import time
import zlib

import numpy as np

_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
sys.path.insert(0, _ROOT)
from core.validate import N as Q, GEMATRIA, TRANS  # noqa: E402

RUNES = "".join(r for r, _t, _p in GEMATRIA)
R2V = {c: i for i, c in enumerate(RUNES)}
V2L = [TRANS[v] for v in range(Q)]
BLOB = os.path.join(_ROOT, "sources", "dukotah", "liber-primus", "analysis",
                    "pp49_51", "canon_256.bin")
BLOB_SHA = "3b9b07d9a26e6d55c432d94d2661fdff3c2b348daed06821f2bdb23184a4b290"
PAGES = os.path.join(_ROOT, "data", "pages")
KRIS = os.path.join(_ROOT, "sources", "dukotah", "liber-primus", "data",
                    "krisyotam_runes.txt")
BOOK = list(range(50)) + list(range(51, 56))
SEED = 20261201
W, STRIDE = 60, 30
SOFFS = list(range(228))               # window slide over the 256-byte table


def rng_for(tag, draw):
    return np.random.default_rng([SEED, zlib.crc32(tag.encode()) % 100000, draw])


def load():
    b = open(BLOB, "rb").read()
    assert hashlib.sha256(b).hexdigest() == BLOB_SHA, "G1 blob sha"
    assert len(b) == 256, "G1 blob len"
    B = np.frombuffer(b, np.uint8).astype(np.int64)
    pages = [np.array([int(x) for x in open(os.path.join(PAGES, f"lp2_{p:02d}.txt")).read().split()])
             for p in BOOK]
    assert sum(len(v) for v in pages) == 12956, "G3 corpus L"
    return B, pages


def gates(B):
    """G2: plant-feasibility image coverage per offset."""
    keep = []
    for s in SOFFS:
        img = {int(B[(r + s) % 256]) % Q for r in range(Q)}
        if len(img) >= 12:
            keep.append(s)
    assert len(keep) >= 50, "G2 too few offsets"
    return keep


def selection(B, soffs):
    """LUT[s][r] = B[(r+s)%256]%29 ; Mflat (29, S*29) one-hot for matmul."""
    LUT = np.array([[int(B[(r + s) % 256]) % Q for r in range(Q)] for s in soffs])
    M = np.zeros((len(soffs), Q, Q), np.float32)
    for si in range(len(soffs)):
        for r in range(Q):
            M[si, r, LUT[si, r]] = 1.0
    Mflat = np.transpose(M, (1, 0, 2)).reshape(Q, len(soffs) * Q)
    pre = [[ [r for r in range(Q) if LUT[si, r] == x] for x in range(Q)]
           for si in range(len(soffs))]
    return LUT, Mflat, pre


def win_counts(v):
    """(nwin,29) rune-value counts, windows W/STRIDE."""
    L = len(v)
    st = np.arange(0, L - W + 1, STRIDE)
    if len(st) == 0:
        return st, np.zeros((0, Q), np.float32)
    OH = np.zeros((L, Q), np.float32)
    OH[np.arange(L), v] = 1.0
    C = np.vstack([np.zeros(Q, np.float32), OH.cumsum(0)])
    return st, C[st + W] - C[st]


def chi2_grid(Cw, Mflat, S):
    if Cw.shape[0] == 0:
        return np.full((0, S), -1.0)
    H = (Cw @ Mflat).reshape(Cw.shape[0], S, Q)
    return (Q / W) * (H * H).sum(-1) - W


def fam_max(pages, Mflat, S):
    best, arg = -1.0, None
    for pi, v in enumerate(pages):
        st, Cw = win_counts(v)
        g = chi2_grid(Cw, Mflat, S)
        if g.size and g.max() > best:
            wi, si = np.unravel_index(g.argmax(), g.shape)
            best, arg = float(g[wi, si]), (pi, si, int(st[wi]))
    return best, arg


def null_draw(pages, Mflat, S, draw):
    rng = rng_for("PB1", draw)
    best = -1.0
    for v in pages:
        vp = rng.permutation(v)
        st, Cw = win_counts(vp)
        g = chi2_grid(Cw, Mflat, S)
        if g.size:
            best = max(best, float(g.max()))
    return best


def plant(pages, LUT, Mflat, pre, S, draw):
    """35-rune English-strength window at a random (page, s*, aligned
    window); crib from p56/57 distribution restricted to the image."""
    rng = rng_for("plant-PB1", draw)
    solved = np.array([int(x) for x in
                       (open(os.path.join(PAGES, "lp2_56.txt")).read().split() +
                        open(os.path.join(PAGES, "lp2_57.txt")).read().split())])
    dist = np.bincount(solved, minlength=Q).astype(float)
    pi = int(rng.integers(len(pages)))
    si = int(rng.integers(S))
    v = pages[pi].copy()
    st, _ = win_counts(v)
    if len(st) == 0:
        return None
    w0 = int(rng.choice(st))
    img = [x for x in range(Q) if any(pre[si][x])]
    d = np.zeros(Q)
    for x in img:
        d[x] = dist[x]
    d /= d.sum()
    crib = rng.choice(Q, size=35, p=d)
    for k, x in enumerate(crib):
        v[w0 + k] = pre[si][x][0]
    # self-check
    dec = LUT[si][v[w0:w0 + 35]]
    assert np.array_equal(dec, crib), "plant self-check"
    st2, Cw = win_counts(v)
    g = chi2_grid(Cw, Mflat, S)
    wi = int(np.where(st2 == w0)[0][0])
    return float(g[wi, si]), v, pi, si, w0


def e1_lines():
    """Selected-line enumeration (no verdict): krisyotam lines of pp36-38,
    stream-line indices from RED_CENSUS; p10 line 8 for the black 7."""
    lines = open(KRIS).read().splitlines()
    blocks, cur = [], []
    for l in lines:
        if l.strip() == "%":
            blocks.append(cur)
            cur = []
        else:
            cur.append(l)
    blocks.append(cur)
    want = {36: 6, 37: 1, 38: 4, 10: 8}
    extra = {37: [5, 10]}
    out = {}
    for pg in (10, 36, 37, 38):
        body = "\n".join(blocks[pg])
        ls = [seg for seg in body.split("/")]
        idxs = [want[pg]] + extra.get(pg, [])
        for li in idxs:
            runes = [R2V[c] for c in ls[li] if c in R2V] if li < len(ls) else []
            out[f"p{pg}L{li}"] = {"n": len(runes),
                                  "first": V2L[runes[0]] if runes else None,
                                  "nlines_page": len(ls)}
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", type=int, default=20)
    ap.add_argument("--out", default=os.path.join(os.path.dirname(__file__), "results", "f18_results.json"))
    args = ap.parse_args()
    t0 = time.time()
    B, pages = load()
    soffs = gates(B)
    LUT, Mflat, pre = selection(B, soffs)
    S = len(soffs)
    print(f"gates PASS (offsets kept {S}/228)", flush=True)

    obs, arg = fam_max(pages, Mflat, S)
    pi, si, w0 = arg
    print(f"obs PB1 chi2={obs:.2f} page={BOOK[pi]} s={soffs[si]} win={w0}", flush=True)

    nulls = [null_draw(pages, Mflat, S, d) for d in range(args.stage)]
    D = len(nulls)
    if obs >= float(np.median(nulls)) and args.stage == 20:
        print("escalation fires -> 200", flush=True)
        nulls += [null_draw(pages, Mflat, S, d) for d in range(20, 200)]
        D = len(nulls)
    arr = np.array(nulls)
    p = (1 + int((arr >= obs).sum())) / (D + 1)
    p95 = float(np.percentile(arr, 95))
    print(f"PB1: obs {obs:.2f} vs null med {np.median(arr):.2f} p95 {p95:.2f} "
          f"max {arr.max():.2f}  p={p} (D={D})", flush=True)

    hits = 0
    for d in range(10):
        r = plant(pages, LUT, Mflat, pre, S, d)
        if r is None:
            continue
        hits += r[0] > p95
    power = hits / 10
    print(f"power: {power:.1f}", flush=True)

    res = {"seed": SEED, "offsets": S, "obs": {"chi2": obs, "page_book": BOOK[pi],
            "s": soffs[si], "win": w0},
           "null": {"D": D, "median": round(float(np.median(arr)), 3),
                    "p95": round(p95, 3), "max": round(float(arr.max()), 3), "p": p},
           "power_plants_vs_p95": power,
           "E1_lines": e1_lines(),
           "E2_placement": {"bracket": list(range(33, 40)), "header": [34, 35, 36, 37, 38, 39],
                            "footer": [33], "constant_per_page": True}}
    if p <= 0.05:
        from core.cribs import crib_hits
        dec = "".join(V2L[x] for x in LUT[si][pages[pi][w0:w0 + W]])
        res["cribs"] = crib_hits(dec)
        res["best_decode"] = dec
    res["runtime_s"] = round(time.time() - t0, 2)
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    json.dump(res, open(args.out, "w"), indent=1)
    print("wrote", args.out, res["runtime_s"], "s", flush=True)


if __name__ == "__main__":
    main()
