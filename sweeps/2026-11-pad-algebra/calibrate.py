#!/usr/bin/env python3
"""Campaign 2026-11-pad-algebra MC null — 20 in-page shuffles, seed 20261115.
Per shuffle: max chi2 over D space, max chi2 over E space, and max page RATIO
(over all 55 shuffled pages) for the F outlier test (max-vs-max null, PREREG).
Resumable: RNG state checkpointed after every shuffle (bit-identical stream).
Run from repo root:  python3 sweeps/2026-11-pad-algebra/calibrate.py --n <cumulative>
Output: results/null_maxima.csv  (shuffle,max_D,max_E,maxF_ratio)
"""
import argparse, json, os, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, ROOT)
import numpy as np
from core import DATA, kernel
from run import mult_scan, stride_pads, page_mirror_stats, KS   # identical space

def family_maxima(pages, targets, pt, mask):
    maxD = maxE = -1.0
    for M in targets:
        A = pages[M]
        streams = [(N, "fwd", p) for N, p in pages.items()] + \
                  [(N, "rev", p[::-1]) for N, p in pages.items()] + \
                  [(k, "fwd", s) for k, s in pt.items()] + \
                  [(k, "rev", s[::-1]) for k, s in pt.items()]
        for N, orient, B in streams:
            trivial = (M == N and orient == "fwd")
            for k, off, nn, chi2, ioc, h in mult_scan(A, B, mask=mask, skip_off0=trivial, ks=KS):
                if chi2 > maxD: maxD = chi2
        for N, wname, W in stride_pads(pages):
            if len(W) < kernel.MIN_LEN: continue
            for off, nn, chi2, ioc, h in kernel.pair_scan(A, W, mask=mask):
                if chi2 > maxE: maxE = chi2
    ratios = []
    for M in targets:
        st = page_mirror_stats(pages[M])
        if st: ratios.append(st[0] / st[1])
    return maxD, maxE, max(ratios)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=20)
    ap.add_argument("--mask", default="tgt", choices=["tgt", "both"])
    ap.add_argument("--seed", type=int, default=20261115)
    a = ap.parse_args()

    pages = kernel.load_pages()
    targets = [n for n in pages if n <= 54]
    pt = {}
    sp = f"{DATA}/solved_plaintexts.json"
    if os.path.exists(sp):
        pt = {k: np.array(v, dtype=np.int8) for k, v in json.load(open(sp)).items()}

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
        mD, mE, mF = family_maxima(sh, targets, pt, a.mask)
        rows.append((it, mD, mE, mF))
        save()
        print(f"shuffle {it:2d}: maxD={mD:.1f} maxE={mE:.1f} maxF_ratio={mF:.2f}  "
              f"({time.time()-t0:.0f}s)", flush=True)

    with open(f"{HERE}/results/null_maxima.csv", "w") as f:
        f.write("shuffle,max_D,max_E,maxF_ratio\n")
        for r in rows: f.write(f"{r[0]},{r[1]:.2f},{r[2]:.2f},{r[3]:.3f}\n")
    g = np.array([[r[1], r[2], r[3]] for r in rows])
    for i, name in enumerate(["D", "E", "F_ratio"]):
        print(f"null {name}: min={g[:,i].min():.2f} median={np.median(g[:,i]):.2f} max={g[:,i].max():.2f}")

if __name__ == "__main__":
    main()
