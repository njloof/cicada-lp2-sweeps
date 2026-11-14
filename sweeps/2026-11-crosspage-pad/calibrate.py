#!/usr/bin/env python3
"""Campaign MC null calibration — 20 in-page shuffles of the full search space.
Run from repo root:  python3 sweeps/2026-11-crosspage-pad/calibrate.py [--n 20] [--mirror]
Output: results/null_maxima.csv
"""
import argparse, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, ROOT)
import numpy as np
from core import DATA, kernel, mc

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=20)
    ap.add_argument("--mirror", action="store_true")
    ap.add_argument("--mask", default="tgt", choices=["tgt", "both"])
    ap.add_argument("--seed", type=int, default=20261113)
    ap.add_argument("--out", default=f"{HERE}/results/null_maxima.csv")
    a = ap.parse_args()

    pages = kernel.load_pages()
    targets = [n for n in pages if n <= 54]
    pads = list(pages)
    extra = []
    sp = f"{DATA}/solved_plaintexts.json"
    if os.path.exists(sp):
        for k, v in json.load(open(sp)).items():
            extra.append((k, np.array(v, dtype=np.int8)))

    maxima = mc.null_maxima(pages, targets, pads, n=a.n, mask=a.mask,
                            mirror=a.mirror, seed=a.seed, extra_pads=extra)
    os.makedirs(os.path.dirname(a.out), exist_ok=True)
    with open(a.out, "w") as f:
        f.write("shuffle,max_chi2\n")
        for it, g in enumerate(maxima): f.write(f"{it},{g:.2f}\n")
    g = np.array(maxima)
    print(f"\nnull max: min={g.min():.1f} median={np.median(g):.1f} max={g.max():.1f} "
          f"(n={a.n}) -> decision threshold = observed > {g.max():.1f}")

if __name__ == "__main__":
    main()
