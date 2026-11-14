#!/usr/bin/env python3
"""Campaign 2026-11-pad-transform MC null — 20 in-page shuffles of the full A+B space.
Per PREREG: seed 20261114; per-family maxima AND global max per shuffle.
Run from repo root:  python3 sweeps/2026-11-pad-transform/calibrate.py [--n 20]
Output: results/null_maxima.csv  (shuffle,max_A,max_B,max_global)
"""
import argparse, json, os, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, ROOT)
import numpy as np
from core import DATA, kernel
from run import page_pads, weave_pads   # same pad construction as the real sweep

def family_maxima(pages, targets, pt, mask):
    """Returns (maxA, maxB) over the full family A + B space for given page dict."""
    maxA = maxB = -1.0
    for M in targets:
        A = pages[M]
        padstreams = list(page_pads(pages)) + \
                     [(k, o, s if o == "fwd" else s[::-1], None)
                      for k, s in pt.items() for o in ("fwd", "rev")]
        for N, orient, B, straddle in padstreams:
            for _, _, chi2, _, _ in kernel.pair_scan(A, B, mask=mask, straddle=straddle, stat="sum"):
                if chi2 > maxA: maxA = chi2
        for N, wname, W in weave_pads(pages):
            for _, _, chi2, _, _ in kernel.pair_scan(A, W, mask=mask):
                if chi2 > maxB: maxB = chi2
    return maxA, maxB

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=20)
    ap.add_argument("--mask", default="tgt", choices=["tgt", "both"])
    ap.add_argument("--seed", type=int, default=20261114)
    a = ap.parse_args()

    pages = kernel.load_pages()
    targets = [n for n in pages if n <= 54]
    pt = {}
    sp = f"{DATA}/solved_plaintexts.json"
    if os.path.exists(sp):
        pt = {k: np.array(v, dtype=np.int8) for k, v in json.load(open(sp)).items()}

    # resumable: checkpoint RNG state after every shuffle so chunked foreground runs
    # are bit-identical to one continuous run of the registered seed
    ckpt_f = f"{HERE}/results/null_checkpoint.json"
    start, rows = 0, []
    if os.path.exists(ckpt_f):
        ck = json.load(open(ckpt_f))
        assert ck["seed"] == a.seed and ck["mask"] == a.mask, "checkpoint/args mismatch"
        rng = np.random.default_rng(0)
        rng.bit_generator.state = ck["rng_state"]
        rows = [tuple(r) for r in ck["rows"]]
        start = len(rows)
        print(f"resuming from checkpoint at shuffle {start}", flush=True)
    else:
        rng = np.random.default_rng(a.seed)

    def save():
        json.dump(dict(seed=a.seed, mask=a.mask, rng_state=rng.bit_generator.state, rows=rows),
                  open(ckpt_f, "w"))

    t0 = time.time()
    for it in range(start, a.n):
        sh = dict(pages)
        for M in targets:
            p = pages[M].copy(); rng.shuffle(p); sh[M] = p
        mA, mB = family_maxima(sh, targets, pt, a.mask)
        rows.append((it, mA, mB, max(mA, mB)))
        save()
        print(f"shuffle {it:2d}: maxA={mA:.1f} maxB={mB:.1f} global={max(mA,mB):.1f}  "
              f"({time.time()-t0:.0f}s)", flush=True)

    with open(f"{HERE}/results/null_maxima.csv", "w") as f:
        f.write("shuffle,max_A,max_B,max_global\n")
        for r in rows: f.write(f"{r[0]},{r[1]:.2f},{r[2]:.2f},{r[3]:.2f}\n")
    g = np.array([[r[1], r[2], r[3]] for r in rows])
    for i, name in enumerate(["A", "B", "global"]):
        print(f"null {name}: min={g[:,i].min():.1f} median={np.median(g[:,i]):.1f} "
              f"max={g[:,i].max():.1f}")

if __name__ == "__main__":
    main()
