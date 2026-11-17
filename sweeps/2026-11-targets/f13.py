#!/usr/bin/env python3
"""Campaign #14 / F13 — token table as TARGET. Registration: PREREG.md
(31c38c3), committed before any output. R1 = T2 re-power (canon-only affine
pad -> page, W=240/stride=120 long-window regime); R2 = blob-minus-page-pad
target scan (a 1..28 x o 0..255, n=256, sign folded into a). Seed 20261203,
alpha 0.025/family, escalation 20->200.

Usage: python3 f13.py [--stage 20] [--out results/f13_results.json]
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
from core.validate import N as Q, TRANS  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
BLOB = os.path.join(_ROOT, "sources", "dukotah", "liber-primus", "analysis",
                    "pp49_51", "canon_256.bin")
BLOB_SHA = "3b9b07d9a26e6d55c432d94d2661fdff3c2b348daed06821f2bdb23184a4b290"
PAGES = os.path.join(_ROOT, "data", "pages")
BOOK = list(range(50)) + list(range(51, 56))
SEED = 20261203
ALPHA = 0.025
W, STRIDE = 240, 120

# English letter frequencies over runes representable by single-letter TRANS
_L2V = {}
for v in range(Q):
    s = TRANS[v]
    if len(s) == 1:
        _L2V[s.upper()] = v
_FREQ = {"A": .0817, "B": .0149, "C": .0278, "D": .0425, "E": .1270, "F": .0223,
         "G": .0202, "H": .0609, "I": .0697, "J": .0015, "K": .0077, "L": .0403,
         "M": .0241, "N": .0675, "O": .0751, "P": .0193, "Q": .0010, "R": .0599,
         "S": .0633, "T": .0906, "U": .0276, "V": .0098, "W": .0236, "X": .0015,
         "Y": .0197, "Z": .0007}
_p = np.zeros(Q)
_unrep = []
for ch, f in _FREQ.items():
    if ch in _L2V:
        _p[_L2V[ch]] += f
    else:
        _unrep.append(ch)
ENG = _p / _p.sum()


def rng_for(tag, draw):
    return np.random.default_rng([SEED, zlib.crc32(tag.encode()) % 100000, draw])


def load():
    b = open(BLOB, "rb").read()
    assert hashlib.sha256(b).hexdigest() == BLOB_SHA, "G1 blob sha"
    assert len(b) == 256, "G1 blob len"
    pages = [(p, np.array([int(x) for x in
               open(os.path.join(PAGES, f"lp2_{p:02d}.txt")).read().split()]))
             for p in BOOK]
    assert sum(len(v) for _, v in pages) == 12956, "G1 corpus L"
    return (np.frombuffer(b, np.uint8).astype(np.int64)) % Q, pages


# ---------------- R1 ----------------

def r1_scan(pages, b29, W=W, stride=STRIDE):
    """max window chi2 of D = (v - a*(pad mod 29)) mod 29, a 2..28, o 0..255."""
    elig = [(p, v) for p, v in pages if len(v) >= W]
    best, arg, nwin_tot = -1.0, None, 0
    ar29 = np.arange(Q)
    for pnum, v in elig:
        Lp = len(v)
        OH = np.zeros((Lp, Q), np.int32)
        OH[np.arange(Lp), v] = 1
        st = np.arange(0, Lp - W + 1, stride)
        nwin_tot += len(st)
        lo, hi = st[0], st[-1] + W
        sub = OH[lo:hi]
        idx = (np.arange(256)[:, None] + np.arange(Lp)[None, :]) % 256
        for a in range(2, 29):
            cmat = (a * b29[idx]) % Q                      # (256, Lp)
            g = (ar29[None, None, :] + cmat[:, lo:hi, None]) % Q
            M = np.take_along_axis(np.broadcast_to(sub[None], (256, hi - lo, Q)), g, 2)
            Cs = np.concatenate([np.zeros((256, 1, Q), np.int64),
                                 np.cumsum(M, 1)], axis=1)
            Cw = Cs[:, st - lo + W] - Cs[:, st - lo]       # (256, nwin, 29)
            chi = (Q / W) * (Cw * Cw).sum(2) - W
            k = int(np.argmax(chi))
            if chi.flat[k] > best:
                o, wi = np.unravel_index(k, chi.shape)
                best, arg = float(chi[o, wi]), (pnum, a, int(o), int(st[wi]))
    return best, arg, nwin_tot, len(elig)


def r1_plant(pages, b29, draw):
    rng = rng_for("plant-R1", draw)
    elig = [i for i, (_, v) in enumerate(pages) if len(v) >= W]
    pi = int(rng.choice(elig))
    pnum, v = pages[pi]
    a = int(rng.integers(2, 29))
    o = int(rng.integers(256))
    st = np.arange(0, len(v) - W + 1, STRIDE)
    w0 = int(rng.choice(st))
    crib = rng.choice(Q, size=W, p=ENG)
    pad = (a * b29[(o + np.arange(w0, w0 + W)) % 256]) % Q
    vp = v.copy()
    vp[w0:w0 + W] = (crib + pad) % Q
    pages2 = list(pages)
    pages2[pi] = (pnum, vp)
    assert np.array_equal((vp[w0:w0 + W] - pad) % Q, crib), "plant self-check"
    return pages2


# ---------------- R2 ----------------

def r2_scan(pages, b29):
    """max chi2 of D[j] = (B[(j+o)%256] - a*v[j%Lp]) mod 29 over (page,a,o)."""
    bsh = b29[(np.arange(256)[:, None] + np.arange(256)[None, :]) % 256]  # (o, j)
    rows = np.repeat(np.arange(256), 256)
    best, arg, top = -1.0, None, []
    jmod = np.arange(256)
    for pnum, v in pages:
        vv = v[jmod % len(v)]
        for a in range(1, 29):
            D = (bsh - ((a * vv) % Q)[None, :]) % Q
            C = np.zeros((256, Q), np.int64)
            np.add.at(C, (rows, D.ravel()), 1)
            chi = (Q / 256.0) * (C * C).sum(1) - 256.0
            o = int(np.argmax(chi))
            top.append((float(chi[o]), pnum, a, o))
            if chi[o] > best:
                best, arg = float(chi[o]), (pnum, a, o)
    top.sort(reverse=True)
    return best, arg, top[:5]


def r2_plant(pages, b29, draw):
    rng = rng_for("plant-R2", draw)
    pi = int(rng.integers(len(pages)))
    pnum, v = pages[pi]
    a = int(rng.integers(1, 29))
    o = int(rng.integers(256))
    crib = rng.choice(Q, size=256, p=ENG)
    vv = v[np.arange(256) % len(v)]
    Bp = np.empty(256, np.int64)
    t = np.arange(256)
    Bp[(t + o) % 256] = (crib + (a * vv) % Q) % Q
    assert np.array_equal((Bp[(np.arange(256) + o) % 256] - (a * vv) % Q) % Q,
                          crib), "plant self-check"
    return Bp


# ---------------- pipeline ----------------

def fam_max(fam):
    return fam[0]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", type=int, default=20)
    ap.add_argument("--out", default=os.path.join(HERE, "results", "f13_results.json"))
    args = ap.parse_args()
    t0 = time.time()
    b29, pages = load()
    print(f"gates PASS (blob mod29, L=12956; unrepresented letters: {_unrep})",
          flush=True)

    obs1, arg1, nwin1, nelig1 = r1_scan(pages, b29)
    print(f"R1 obs {obs1:.2f} arg(page,a,o,win)={arg1} pages={nelig1} "
          f"windows/page-set={nwin1}", flush=True)
    obs2, arg2, top2 = r2_scan(pages, b29)
    print(f"R2 obs {obs2:.2f} arg(page,a,o)={arg2} family=394240", flush=True)

    res = {"seed": SEED, "alpha": ALPHA,
           "R1": {"obs": obs1, "arg": arg1, "pages_eligible": nelig1,
                  "windows_total": nwin1,
                  "family_size": int(nelig1 * 27 * 256 * max(nwin1 // nelig1, 1))},
           "R2": {"obs": obs2, "arg": arg2, "family_size": 55 * 28 * 256,
                  "top5": top2}}

    for fam, obsv, scan, plant, tag in (
            ("R1", obs1, lambda pg: r1_scan(pg, b29)[0],
             lambda d: r1_plant(pages, b29, d), "R1"),
            ("R2", obs2, lambda pg: r2_scan(pg, b29)[0],
             lambda d: r2_plant(pages, b29, d), "R2")):
        nulls = []
        for d in range(args.stage):
            rng = rng_for(tag, d)
            pg = [(p, rng.permutation(v)) for p, v in pages]
            nulls.append(scan(pg))
            if (d + 1) % 5 == 0:
                print(f"{fam} null {d+1}/{args.stage}", flush=True)
        arr = np.array(nulls)
        if obsv >= float(np.median(arr)) and args.stage == 20:
            print(f"{fam}: escalation fires -> 200", flush=True)
            for d in range(20, 200):
                rng = rng_for(tag, d)
                pg = [(p, rng.permutation(v)) for p, v in pages]
                nulls.append(scan(pg))
            arr = np.array(nulls)
        p = (1 + int((arr >= obsv).sum())) / (len(arr) + 1)
        p95 = float(np.percentile(arr, 95))
        hits = 0
        for d in range(20):
            pg = plant(d)
            if fam == "R2":
                sc = r2_scan(pages, pg)[0]
            else:
                sc = scan(pg)
            hits += sc > p95
        res[fam].update({"null_D": len(arr), "median": round(float(np.median(arr)), 2),
                         "p95": round(p95, 2), "max": round(float(arr.max()), 2),
                         "p": p, "plants_vs_p95": f"{hits}/20"})
        print(f"{fam}: obs {obsv:.2f} med {np.median(arr):.2f} p95 {p95:.2f} "
              f"p={p} plants {hits}/20", flush=True)

    res["flags"] = [f for f in ("R1", "R2") if res[f]["p"] <= ALPHA]
    if res["flags"]:
        from core.cribs import crib_hits
        hits = {}
        for f in res["flags"]:
            if f == "R2":
                pnum, a, o = arg2
                v = dict(pages)[pnum]
                D = (b29[(np.arange(256) + o) % 256] - (a * v[np.arange(256) % len(v)]) % Q) % Q
                dec = "".join(TRANS[x] for x in D)
                hits["R2_argmax"] = {"translit": dec, "cribs": crib_hits(dec)}
        res["cribs"] = hits
    res["runtime_s"] = round(time.time() - t0, 1)
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    json.dump(res, open(args.out, "w"), indent=1)
    print("wrote", args.out, res["runtime_s"], "s", flush=True)


if __name__ == "__main__":
    main()
