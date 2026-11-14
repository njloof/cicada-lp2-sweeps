#!/usr/bin/env python3
"""Campaign 2026-11-p12-mirror — G+H null: 1000 in-page shuffles, seed 20261116.
Per shuffle (all 55 pages shuffled, lengths/frequencies/F-density preserved):
  maxG      = max page ratio (mirror_max / own-diff p99)   — campaign #3's F, sharp null
  maxH      = max page S, S = max over rev alignments of (h[1]+h[28])/n — prospective H_shift
  p12_chi2  = p12's rev-family chi2 max (sharpens #3's exploratory 0/200 anatomy null)
Resumable: RNG state checkpointed after every shuffle (bit-identical stream).
Run from repo root:  python3 sweeps/2026-11-p12-mirror/calibrate.py --n <cumulative>
Output: results/null_GH.csv  (shuffle,maxG,maxH,p12_chi2)
"""
import argparse, json, os, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, ROOT)
import numpy as np
from core import kernel
from run import page_ratio_stats, shift_stat

def shuffle_maxima(pages, targets):
    maxG = maxH = p12c = -1.0
    for M in targets:
        r = page_ratio_stats(pages[M])
        if r and r[0] / r[1] > maxG: maxG = r[0] / r[1]
        s, off, nn = shift_stat(pages[M])
        if s > maxH: maxH = s
        if M == 12:
            p12c = max(c for _, _, c, _, _ in kernel.pair_scan(pages[12], pages[12][::-1]))
    return maxG, maxH, p12c

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=1000)
    ap.add_argument("--seed", type=int, default=20261116)
    a = ap.parse_args()
    pages = kernel.load_pages()
    targets = [n for n in pages if n <= 54]

    ckpt_f = f"{HERE}/results/null_checkpoint.json"
    start, rows = 0, []
    if os.path.exists(ckpt_f):
        ck = json.load(open(ckpt_f))
        assert ck["seed"] == a.seed, "checkpoint/seed mismatch"
        rng = np.random.default_rng(0)
        rng.bit_generator.state = ck["rng_state"]
        rows = [tuple(r) for r in ck["rows"]]
        start = len(rows)
        print(f"resuming from checkpoint at shuffle {start}", flush=True)
    else:
        rng = np.random.default_rng(a.seed)

    def save():
        json.dump(dict(seed=a.seed, rng_state=rng.bit_generator.state, rows=rows),
                  open(ckpt_f, "w"))

    t0 = time.time()
    for it in range(start, a.n):
        sh = dict(pages)
        for M in targets:
            p = pages[M].copy(); rng.shuffle(p); sh[M] = p
        g, h, c12 = shuffle_maxima(sh, targets)
        rows.append((it, g, h, c12))
        if it % 10 == 9 or it == a.n - 1: save()
        if it % 100 == 0 or it == a.n - 1:
            print(f"shuffle {it}: maxG={g:.3f} maxH={h:.3f} p12_chi2={c12:.1f} "
                  f"({time.time()-t0:.0f}s)", flush=True)
    save()
    with open(f"{HERE}/results/null_GH.csv", "w") as f:
        f.write("shuffle,maxG,maxH,p12_chi2\n")
        for r in rows: f.write(f"{r[0]},{r[1]:.4f},{r[2]:.4f},{r[3]:.2f}\n")
    g = np.array([[r[1], r[2], r[3]] for r in rows])
    # observed values read from run.py's tables (p12 rows) — no hardcoded drift
    import csv
    obsG = float([r for r in csv.DictReader(open(f"{HERE}/results/obs_G_ratios.csv")) if r["page"] == "12"][0]["ratio"])
    obsH = float([r for r in csv.DictReader(open(f"{HERE}/results/obs_H_shift.csv")) if r["page"] == "12"][0]["S"])
    obsC = max(c for _, _, c, _, _ in kernel.pair_scan(kernel.load_pages()[12], kernel.load_pages()[12][::-1]))
    for i, (name, obs) in enumerate([("G_ratio", obsG), ("H_shift", obsH), ("p12_chi2", obsC)]):
        col = g[:, i]
        p = (1 + int((col >= obs).sum())) / (len(col) + 1)
        print(f"null {name}: min={col.min():.3f} med={np.median(col):.3f} "
              f"p95={np.percentile(col,95):.3f} max={col.max():.3f} | obs={obs} -> p={p:.4f}")

if __name__ == "__main__":
    main()
