#!/usr/bin/env python3
"""Campaign 2026-11-product-spaces — per-family MC null of the GLOBAL MAX.

20 in-page shuffles of all 55 targets (lengths/frequencies/F-density preserved;
pads stay real), seed 20261119, shared shuffle stream across families — run one
process per family in parallel; the stream is seed-identical either way.
Resumable: RNG state checkpointed after every shuffle (bit-identical stream).

  python3 sweeps/2026-11-product-spaces/calibrate.py --family K   (likewise L, M)

Output: results/null_<F>.csv (shuffle,max). At completion prints min/med/p95/max,
empirical p vs results/obs_maxima.csv, and the PREREG escalation check
(obs >= null median  =>  extend to >=200 draws before any verdict).
"""
import argparse, json, os, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, ROOT)
sys.path.insert(0, HERE)
import numpy as np
from core import DATA, kernel
from run import mult_scan, strided_ext, strided_all, strided_mirrors, plain_mirrors

def family_max(fam, sh, pages, pt, targets):
    """Global max chi2 for one family on (possibly shuffled) targets sh."""
    mx = -1.0
    for M in targets:
        A = sh[M]
        if fam == "K":
            for N, w, W in strided_ext(pages):
                if len(W) < kernel.MIN_LEN: continue
                for _, _, _, c, _, _ in kernel.pair_scan(A, W, mask="tgt"):
                    if c > mx: mx = c
            for N, w, W, s in strided_mirrors(pages):
                for _, _, _, c, _, _ in kernel.pair_scan(A, W, mask="tgt", straddle=s):
                    if c > mx: mx = c
        elif fam == "L":
            for N, w, W in strided_all(pages):
                if len(W) < kernel.MIN_LEN: continue
                for _, _, _, c, _, _ in mult_scan(A, W, mask="tgt"):
                    if c > mx: mx = c
        elif fam == "M":
            m = len(A)
            for N, orient, B, s in plain_mirrors(pages, pt):
                triv = set()
                if N == M:                    # exclusions applied identically to run.py
                    triv = {0} if orient == "fwdrev" else {-s}
                for k, off, _, c, _, _ in mult_scan(A, B, mask="tgt"):
                    if off in triv: continue
                    if not (-s < off <= m - 1 - s): continue
                    if c > mx: mx = c
        else:
            raise ValueError(fam)
    return mx

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--family", required=True, choices=["K", "L", "M"])
    ap.add_argument("--n", type=int, default=20)
    ap.add_argument("--seed", type=int, default=20261119)
    a = ap.parse_args()
    os.makedirs(f"{HERE}/results", exist_ok=True)
    pages = kernel.load_pages()
    targets = [n for n in pages if n <= 54]
    pt = {}
    sp = f"{DATA}/solved_plaintexts.json"
    if os.path.exists(sp):
        pt = {k: np.array(v, dtype=np.int8) for k, v in json.load(open(sp)).items()}

    ckpt_f = f"{HERE}/results/null_{a.family}_checkpoint.json"
    start, rows = 0, []
    if os.path.exists(ckpt_f):
        ck = json.load(open(ckpt_f))
        assert ck["seed"] == a.seed, "checkpoint/seed mismatch"
        rng = np.random.default_rng(0)
        rng.bit_generator.state = ck["rng_state"]
        rows = ck["rows"]
        start = len(rows)
        print(f"[{a.family}] resuming from checkpoint at shuffle {start}", flush=True)
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
        mx = family_max(a.family, sh, pages, pt, targets)
        rows.append([it, round(mx, 2)])
        save()
        print(f"[{a.family}] shuffle {it}: max={mx:.2f} ({time.time()-t0:.0f}s)", flush=True)

    with open(f"{HERE}/results/null_{a.family}.csv", "w") as f:
        f.write("shuffle,max\n")
        for r in rows: f.write(f"{r[0]},{r[1]}\n")
    col = np.array([r[1] for r in rows], dtype=float)
    obs = None
    om = f"{HERE}/results/obs_maxima.csv"
    if os.path.exists(om):
        import csv
        obs = float([r for r in csv.DictReader(open(om)) if r["family"] == a.family][0]["obs_max"])
    med = float(np.median(col))
    print(f"null {a.family}: n={len(col)} min={col.min():.2f} med={med:.2f} "
          f"p95={np.percentile(col, 95):.2f} max={col.max():.2f}")
    if obs is not None:
        p = (1 + int((col >= obs).sum())) / (len(col) + 1)
        print(f"obs={obs} -> p={p:.4f} | GO prong needs obs > 1.1 x {col.max():.2f} "
              f"= {1.1 * col.max():.2f}")
        print("ESCALATION: obs >= null median -> extend to >=200 draws before verdict"
              if obs >= med else "escalation rule: not triggered (obs < null median)")

if __name__ == "__main__":
    main()
