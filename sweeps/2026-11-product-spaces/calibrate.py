#!/usr/bin/env python3
"""Campaign 2026-11-product-spaces — per-family MC null of the GLOBAL MAX.

20 in-page shuffles of all 55 targets (lengths/frequencies/F-density preserved;
pads stay real), seed 20261119, shared shuffle stream across families — run one
process per family in parallel; the stream is seed-identical either way.
Resumable: RNG state checkpointed after every shuffle (bit-identical stream).

The null needs only the family max, so chi2 is computed VECTORIZED across all
offsets (scan_max) instead of the observed run's per-window loop: identical
statistic, identical exclusions (min_len, straddle, trivial self-pair offsets),
~10-20x faster. Startup self-check asserts scan_max == the loop path
(mult_scan / pair_scan) on real-data streams before any shuffle runs.

  python3 sweeps/2026-11-product-spaces/calibrate.py --family K   (likewise L, M)

Output: results/null_<F>.csv (shuffle,max). At completion prints min/med/p95/max,
empirical p vs results/obs_maxima.csv, and the PREREG escalation check
(obs >= null median  =>  extend to >=200 draws before verdict).
"""
import argparse, json, os, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, ROOT)
sys.path.insert(0, HERE)
import numpy as np
from core import DATA, kernel
from run import (mult_scan, strided_ext, strided_all, strided_mirrors,
                 plain_mirrors, KS, Q)

def scan_max(A, B, mask="tgt", min_len=kernel.MIN_LEN, ks=(1,),
             straddle=None, trivial=None):
    """Max chi2 over all valid windows of one (A, B, ks) scan — vectorized
    equivalent of the run.py loop (same Valid geometry, same filters)."""
    m, n = len(A), len(B)
    if mask == "both":
        Valid = (A[:, None] != 0) & (B[None, :] != 0)
    else:
        Valid = np.repeat((A != 0)[:, None], n, axis=1)
    ii, jj = np.nonzero(Valid)
    d = (ii - jj) + (n - 1)
    n_off = m + n - 1
    Ai = A[ii].astype(np.int32); Bj = B[jj].astype(np.int32)
    offs = np.arange(n_off) - (n - 1)
    good = np.ones(n_off, bool)
    if straddle is not None:
        good &= (-straddle < offs) & (offs <= m - 1 - straddle)
    if trivial is not None and len(trivial):
        good &= ~np.isin(offs, np.fromiter(trivial, int))
    best = -1.0
    with np.errstate(divide="ignore", invalid="ignore"):
        for k in ks:
            vals = (Ai - k * Bj) % Q
            H = np.bincount(d * Q + vals, minlength=n_off * Q).reshape(n_off, Q)
            cnt = H.sum(1)
            chi2 = (Q / cnt) * (H * H).sum(1) - cnt     # cnt==0 rows masked below
            ok = good & (cnt >= min_len)
            if ok.any():
                c = float(chi2[ok].max())
                if c > best: best = c
    return best

def selfcheck(pages, targets):
    """Vectorized max must equal the loop path on real streams (run once)."""
    M = targets[0]; A = pages[M]
    N, w, W = next((N, w, W) for N, w, W in strided_all(pages) if len(W) >= kernel.MIN_LEN)
    loop = max(c for _, _, _, c, _, _ in mult_scan(A, W, ks=KS))
    vec = scan_max(A, W, ks=KS)
    assert abs(loop - vec) < 1e-6, (loop, vec)
    # mirror path (straddle + trivial), non-self and self pair
    for N2, orient, B, s in plain_mirrors(pages, {}):
        m = len(A)
        triv = ({0} if orient == "fwdrev" else {-s}) if N2 == M else None
        loop = max(c for k, off, _, c, _, _ in mult_scan(A, B, ks=KS)
                   if (triv is None or off not in triv) and (-s < off <= m - 1 - s))
        vec = scan_max(A, B, ks=KS, straddle=s, trivial=triv)
        assert abs(loop - vec) < 1e-6, ("mirror", N2, orient, loop, vec)
        if triv: break
    # K path (pair_scan geometry, straddle via scan_max)
    for N2, w2, W2 in strided_ext(pages):
        if len(W2) < kernel.MIN_LEN: continue
        loop = max(c for _, _, c, _, _ in kernel.pair_scan(A, W2))
        vec = scan_max(A, W2)
        assert abs(loop - vec) < 1e-6, ("K", loop, vec)
        break
    for N2, w2, W2, s in strided_mirrors(pages):
        m = len(A)
        loop = max(c for _, _, c, _, _ in kernel.pair_scan(A, W2, straddle=s))
        vec = scan_max(A, W2, straddle=s)
        assert abs(loop - vec) < 1e-6, ("Kmir", loop, vec)
        break
    print("selfcheck: vectorized max == loop path on real streams OK", flush=True)

def family_max(fam, sh, pages, pt, targets):
    """Global max chi2 for one family on (possibly shuffled) targets sh."""
    mx = -1.0
    for M in targets:
        A = sh[M]
        if fam == "K":
            for N, w, W in strided_ext(pages):
                if len(W) < kernel.MIN_LEN: continue
                c = scan_max(A, W)
                if c > mx: mx = c
            for N, w, W, s in strided_mirrors(pages):
                c = scan_max(A, W, straddle=s)
                if c > mx: mx = c
        elif fam == "L":
            for N, w, W in strided_all(pages):
                if len(W) < kernel.MIN_LEN: continue
                c = scan_max(A, W, ks=KS)
                if c > mx: mx = c
        elif fam == "M":
            for N, orient, B, s in plain_mirrors(pages, pt):
                triv = ({0} if orient == "fwdrev" else {-s}) if N == M else None
                c = scan_max(A, B, ks=KS, straddle=s, trivial=triv)
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
    selfcheck(pages, targets)

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
