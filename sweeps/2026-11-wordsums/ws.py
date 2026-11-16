#!/usr/bin/env python3
"""Campaign #11 — LP2 word-sum self-keys (F1). PREREG: PREREG.md (955c597),
registered before any output. Families WS1-WS4 per registration; null =
derive-from-shuffled; plants = English-strength forward pass.

Usage: python3 ws.py [--stage 20] [--out results/ws_results.json]
"""
import argparse
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
KRIS = os.path.join(_ROOT, "sources", "dukotah", "liber-primus", "data",
                    "krisyotam_runes.txt")
PAGES = os.path.join(_ROOT, "data", "pages")
BOOK = list(range(50)) + list(range(51, 56))          # 55 unsolved pages
SEGS = list(range(55))                                 # krisyotam segs (tail +1)
SEED = 20261130
FAMS = ("WS1", "WS2", "WS3", "WS4")


def load():
    """[(vals, wlens)] per unsolved page + separator counts."""
    lines = open(KRIS).read().splitlines()
    blocks, cur = [], []
    for l in lines:
        if l.strip() == "%":
            blocks.append(cur)
            cur = []
        else:
            cur.append(l)
    blocks.append(cur)
    pages, seps = [], {"-": 0, ".": 0}
    for s in SEGS:
        body = "\n".join(blocks[s])
        vals, wl, n = [], [], 0
        for c in body:
            if c in R2V:
                vals.append(R2V[c])
                n += 1
            elif c in "-.":
                seps[c] += 1
                if n:
                    wl.append(n)
                n = 0
        if n:
            wl.append(n)
        pages.append((np.array(vals, dtype=np.int64), wl))
    return pages, seps


def kill_gates(pages, seps):
    total = sum(len(v) for v, _ in pages)
    assert total == 12956, f"G1 runes {total}"
    for bi, b in enumerate(BOOK):
        tv = np.array([int(x) for x in open(os.path.join(PAGES, f"lp2_{b:02d}.txt")).read().split()])
        assert np.array_equal(pages[bi][0], tv), f"G1 bit-identical book {b}"
    assert seps == {"-": 2729, ".": 173}, f"G2 seps {seps}"
    nwords = sum(len(w) for _, w in pages)
    assert nwords == 2928, f"G2 words {nwords}"
    assert min(len(w) for _, w in pages) >= 17, "G3"
    return {"runes": total, "seps": seps, "words": nwords,
            "mean_len": round(sum(wl for _, ws_ in pages for wl in ws_) / nwords, 4)}


def keys(fam, vals, wlens):
    """Per-rune key array, page-local, self-derived from vals (the array
    under test) + fixed word geometry."""
    K = np.zeros(len(vals), dtype=np.int64)
    i = 0
    prev_sum = 0
    run = 0
    for w in wlens:
        seg = vals[i:i + w]
        s = int(seg.sum()) % Q
        if fam == "WS1":
            k = s
        elif fam == "WS2":
            k = prev_sum
        elif fam == "WS3":
            k = w % Q
        elif fam == "WS4":
            k = run
        K[i:i + w] = k
        prev_sum = s
        run = (run + s) % Q
        i += w
    return K


def mask(fam, vals, wlens):
    """WS1 excludes one-rune words (D==0 identically — registered)."""
    if fam != "WS1":
        return np.ones(len(vals), dtype=bool)
    m = np.ones(len(vals), dtype=bool)
    i = 0
    for w in wlens:
        if w == 1:
            m[i] = False
        i += w
    return m


def chi2(d):
    n = len(d)
    if n < 50:
        return -1.0
    h = np.bincount(d, minlength=Q).astype(np.float64)
    return (Q / n) * float((h * h).sum()) - n


def fam_max(fam, pages):
    """(max chi2, argmax page index) over the 55 pages."""
    best, arg = -1.0, -1
    for pi, (vals, wlens) in enumerate(pages):
        k = keys(fam, vals, wlens)
        d = (vals - k) % Q
        d = d[mask(fam, vals, wlens)]
        c = chi2(d)
        if c > best:
            best, arg = c, pi
    return best, arg


def rng_for(tag, draw):
    return np.random.default_rng([SEED, zlib.crc32(tag.encode()) % 100000, draw])


def null_draw(fam, pages, draw):
    """derive-from-shuffled: permute each page's values, re-derive keys."""
    rng = rng_for(fam, draw)
    best = -1.0
    for pi, (vals, wlens) in enumerate(pages):
        v = rng.permutation(vals)
        d = (v - keys(fam, v, wlens)) % Q
        d = d[mask(fam, v, wlens)]
        c = chi2(d)
        if c > best:
            best = c
    return best


def decode_page(fam, vals, wlens):
    d = (vals - keys(fam, vals, wlens)) % Q
    return "".join(V2L[x] for x in d)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", type=int, default=20)
    ap.add_argument("--out", default=os.path.join(os.path.dirname(__file__), "results", "ws_results.json"))
    args = ap.parse_args()
    t0 = time.time()
    pages, seps = load()
    census = kill_gates(pages, seps)
    print("kill gates PASS:", census, flush=True)

    obs = {}
    for fam in FAMS:
        fam_g = fam
        obs[fam] = fam_max(fam, pages)
        print(f"obs {fam}: chi2={obs[fam][0]:.2f} page={obs[fam][1]}", flush=True)

    nulls = {f: [] for f in FAMS}
    for draw in range(args.stage):
        for fam in FAMS:
            nulls[fam].append(null_draw(fam, pages, draw))

    escalated = [f for f in FAMS if obs[f][0] >= float(np.median(nulls[f]))]
    if escalated and args.stage == 20:
        print("escalation fires:", escalated, flush=True)
        for draw in range(20, 200):
            for fam in escalated:
                nulls[fam].append(null_draw(fam, pages, draw))

    res = {"census": census, "seed": SEED, "obs": {f: {"chi2": obs[f][0], "page_book": BOOK[obs[f][1]]} for f in FAMS},
           "null": {}, "escalated": escalated}
    for fam in FAMS:
        arr = np.array(nulls[fam])
        D = len(arr)
        p = (1 + int((arr >= obs[fam][0]).sum())) / (D + 1)
        res["null"][fam] = {"D": D, "median": round(float(np.median(arr)), 3),
                            "p95": round(float(np.percentile(arr, 95)), 3),
                            "max": round(float(arr.max()), 3), "p": p}
        print(f"{fam}: obs {obs[fam][0]:.2f} vs null med {np.median(arr):.2f} "
              f"max {arr.max():.2f}  p={p}  (D={D})", flush=True)

    # ---- plants (power) ----
    plants = {}
    for fam in FAMS:
        p95 = res["null"][fam]["p95"]
        hits = 0
        for draw in range(10):
            rng = rng_for("plant-" + fam, draw)
            ok = plant(fam, pages, rng)
            if ok is None:
                continue
            c, planted = ok
            assert planted, f"plant self-check {fam} draw {draw}"
            hits += c > p95
        plants[fam] = hits / 10
        print(f"power {fam}: {plants[fam]:.1f}", flush=True)
    res["power_plants_vs_p95"] = plants

    # ---- crib gate for firing families ----
    from core.cribs import crib_hits
    res["cribs"] = {}
    for fam in FAMS:
        if res["null"][fam]["p"] <= 0.0125:
            pi = obs[fam][1]
            vals, wlens = pages[pi]
            txt = decode_page(fam, vals, wlens)
            res["cribs"][fam] = crib_hits(txt)

    res["runtime_s"] = round(time.time() - t0, 2)
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    json.dump(res, open(args.out, "w"), indent=1)
    print("wrote", args.out, res["runtime_s"], "s", flush=True)


def plant(fam, pages, rng):
    """English-strength forward plant on a random page: window = 8
    consecutive words (WS1: all len>=2). Returns (page chi2 after plant,
    self-check decode==crib)."""
    pi = int(rng.integers(len(pages)))
    vals, wlens = pages[pi]
    idx = np.where(np.array(wlens) >= (2 if fam == "WS1" else 1))[0]
    # find 8 consecutive word indices satisfying the length rule
    starts = []
    for a in range(len(wlens) - 8):
        seg = wlens[a:a + 8]
        if fam == "WS1" and min(seg) < 2:
            continue
        starts.append(a)
    if not starts:
        return None
    a = int(rng.choice(starts))
    # crib from solved p56/p57 plaintext value distribution
    solved = np.array([int(x) for x in
                       (open(os.path.join(PAGES, "lp2_56.txt")).read().split() +
                        open(os.path.join(PAGES, "lp2_57.txt")).read().split())])
    dist = np.bincount(solved, minlength=Q).astype(float)
    dist /= dist.sum()
    V = vals.copy()
    # word start offsets
    off = np.cumsum([0] + list(wlens))
    # crib values for the window runes
    nwin = int(sum(wlens[a:a + 8]))
    crib = rng.choice(Q, size=nwin, p=dist)
    # forward pass
    pos = off[a]
    wi = a
    ci = 0
    while wi < a + 8:
        w = wlens[wi]
        k = int(keys(fam, V, wlens)[pos])  # key from current (modified) copy
        cw = crib[ci:ci + w]
        if fam == "WS1":
            # closed form: word sum S must satisfy S = sum(crib + S) -> S=(1-w)^-1 * sum(crib)
            inv = pow(1 - w, Q - 2, Q)
            S = (int(cw.sum()) * inv) % Q
            V[pos:pos + w] = (cw + S) % Q
        else:
            V[pos:pos + w] = (cw + k) % Q
        pos += w
        ci += w
        wi += 1
    # self-check + score
    d = (V - keys(fam, V, wlens)) % Q
    win = np.zeros(len(V), dtype=bool)
    win[off[a]:off[a + 8]] = True
    ok = bool(np.array_equal(d[win & mask(fam, V, wlens)], crib[win[win & mask(fam, V, wlens)]]))
    dm = d[mask(fam, V, wlens)]
    return chi2(dm), ok


if __name__ == "__main__":
    main()
