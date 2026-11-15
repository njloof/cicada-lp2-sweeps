#!/usr/bin/env python3
"""Campaign 2026-11-index-consumption — planted-signal power probe (PREREG).

Coverage alone is not citable: plant 10 synthetic true pads into 10 distinct
targets simultaneously — A' = (A + pad_window) mod 29 over the full maximal
window at a random (pad geometry, orientation, offset) drawn from the family's
own pad list — then run the unmodified family scan and record, for each plant,
whether the true window's chi2 reaches the family null median (the threshold a
real hit would have to clear). Recovery rate = power at threshold.

  python3 sweeps/2026-11-index-consumption/power.py --family P --median 97.4
  (median from results/null_<F>.csv; pass --median to pin, else it is read)

Output: results/power.csv (per-plant rows + recovery rate printed).
"""
import argparse, csv, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, ROOT)
sys.path.insert(0, HERE)
import numpy as np
from core import kernel
from run import drop_pads, cyc_pads, load_sources, window_stats, Q
from calibrate import scan_max

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--family", required=True, choices=["P", "W"])
    ap.add_argument("--median", type=float, default=None)
    ap.add_argument("--seed", type=int, default=20261121)
    ap.add_argument("--plants", type=int, default=10)
    a = ap.parse_args()
    med = a.median
    nf = f"{HERE}/results/null_{a.family}.csv"
    if med is None:
        if not os.path.exists(nf):
            sys.exit("no null file and no --median: run calibrate.py first")
        col = [float(r["max"]) for r in csv.DictReader(open(nf))]
        med = float(np.median(col))

    pages, targets, sources = load_sources()
    pads = list(drop_pads(sources) if a.family == "P" else cyc_pads(sources))
    rng = np.random.default_rng(a.seed)
    mods = dict(pages)
    chosen = rng.choice(targets, size=a.plants, replace=False)
    plants = []
    for M in chosen:
        A = pages[M]
        while True:
            N, w, W = pads[int(rng.integers(len(pads)))]
            if N != M: break
        m, n = len(A), len(W)
        offs = [o for o in range(-(n - 1), m)
                if int((A[max(0, o):min(m, o + n)] != 0).sum()) >= kernel.MIN_LEN]
        o = offs[int(rng.integers(len(offs)))]
        i0, i1 = max(0, o), min(m, o + n)
        A2 = A.copy()
        A2[i0:i1] = (A[i0:i1].astype(np.int32) + W[i0 - o:i1 - o].astype(np.int32)) % Q
        mods[M] = A2
        plants.append((M, N, w, o, W))

    # unmodified family scan on the planted corpus
    fmax = -1.0
    for M in targets:
        A = mods[M]
        for N, w, W in pads:
            c = scan_max(A, W)
            if c > fmax: fmax = c

    os.makedirs(f"{HERE}/results", exist_ok=True)
    nrec = 0
    with open(f"{HERE}/results/power.csv", "w") as f:
        f.write("family,plant,target,source,pad,offset,n_valid,chi2_true_window,"
                "null_median,recovered\n")
        for j, (M, N, w, o, W) in enumerate(plants):
            r = window_stats(mods[M], W, o, mask="tgt")
            nn, chi2 = r
            rec = chi2 >= med
            nrec += rec
            f.write(f"{a.family},{j},{M},{N},{w},{o},{nn},{round(chi2, 2)},"
                    f"{med},{rec}\n")
    print(f"power {a.family}: {nrec}/{a.plants} planted windows reach the null "
          f"median {med:.2f} (planted-corpus family max {fmax:.2f})")

if __name__ == "__main__":
    main()
