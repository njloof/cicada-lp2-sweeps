#!/usr/bin/env python3
"""Campaign 2026-11-index-consumption — per-family MC null of the GLOBAL MAX.

20 in-page shuffles of all 55 targets (lengths/frequencies/F-density preserved;
pads stay real), seed 20261120, shared shuffle stream across families — run one
process per family in parallel; the stream is seed-identical either way.
Resumable: RNG state checkpointed after every shuffle (bit-identical stream).

The null needs only the family max, so chi2 is computed VECTORIZED across all
offsets (scan_max) instead of the observed run's per-window loop: identical
statistic, identical filters (min_len; no straddle/trivial geometry this
campaign), ~10x faster. Startup self-check asserts scan_max == the pair_scan
loop path on real streams, and re-runs the PREREG guarantee-1 exhaustive
alignment-coverage check, before any shuffle runs.

  python3 sweeps/2026-11-index-consumption/calibrate.py --family P   (likewise W)

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
from core import kernel
from run import drop_pads, cyc_pads, coverage_check, load_sources, Q

def scan_max(A, B, mask="tgt", min_len=kernel.MIN_LEN):
    """Max chi2 over all valid windows of one (A, B) scan — vectorized
    equivalent of the run.py pair_scan loop (same Valid geometry, same floor)."""
    m, n = len(A), len(B)
    if mask == "both":
        Valid = (A[:, None] != 0) & (B[None, :] != 0)
    else:
        Valid = np.repeat((A != 0)[:, None], n, axis=1)
    ii, jj = np.nonzero(Valid)
    d = (ii - jj) + (n - 1)
    n_off = m + n - 1
    vals = (A[ii].astype(np.int32) - B[jj].astype(np.int32)) % Q
    H = np.bincount(d * Q + vals, minlength=n_off * Q).reshape(n_off, Q)
    cnt = H.sum(1)
    ok = cnt >= min_len
    if not ok.any(): return -1.0
    with np.errstate(divide="ignore", invalid="ignore"):
        chi2 = (Q / cnt) * (H * H).sum(1) - cnt
    return float(chi2[ok].max())

def selfcheck(pages, targets, sources):
    """Vectorized max must equal the loop path on real streams (run once)."""
    M = targets[0]; A = pages[M]
    for gen, tag in ((drop_pads(sources), "P"), (cyc_pads(sources), "W")):
        for N, w, W in gen:
            loop = max(c for _, _, c, _, _ in kernel.pair_scan(A, W))
            vec = scan_max(A, W)
            assert abs(loop - vec) < 1e-6, (tag, N, w, loop, vec)
            break
    print("selfcheck: vectorized max == pair_scan loop path on real streams OK",
          flush=True)

def family_max(fam, sh, pages, sources, targets, exclude_self=False):
    """Global max chi2 for one family on (possibly shuffled) targets sh.
    exclude_self: AMENDED geometry (self-pair cyclic pads carry gcd(a±1,L)
    permutation fixed points -> un-calibratable D=0 pileups; PREREG AMENDMENT)."""
    mx = -1.0
    gen = drop_pads(sources) if fam == "P" else cyc_pads(sources)
    pads = list(gen)
    for M in targets:
        A = sh[M]
        for N, w, W in pads:
            if exclude_self and N == M: continue
            c = scan_max(A, W)
            if c > mx: mx = c
    return mx

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--family", required=True, choices=["P", "W"])
    ap.add_argument("--n", type=int, default=20)
    ap.add_argument("--seed", type=int, default=20261120)
    ap.add_argument("--exclude-self", action="store_true",
                    help="AMENDED geometry: skip self-pair pads (matches run.py "
                         "--exclude-self); writes null_<F>_noself.csv")
    ap.add_argument("--obs", type=float, default=None,
                    help="override observed max (use with --exclude-self: pass the "
                         "max of the filtered full sweep CSV)")
    a = ap.parse_args()
    os.makedirs(f"{HERE}/results", exist_ok=True)
    pages, targets, sources = load_sources()
    selfcheck(pages, targets, sources)
    coverage_check(pages, targets, sources)

    sfx = "_noself" if a.exclude_self else ""
    ckpt_f = f"{HERE}/results/null_{a.family}{sfx}_checkpoint.json"
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
        mx = family_max(a.family, sh, pages, sources, targets,
                        exclude_self=a.exclude_self)
        rows.append([it, round(mx, 2)])
        save()
        print(f"[{a.family}{sfx}] shuffle {it}: max={mx:.2f} ({time.time()-t0:.0f}s)", flush=True)

    with open(f"{HERE}/results/null_{a.family}{sfx}.csv", "w") as f:
        f.write("shuffle,max\n")
        for r in rows: f.write(f"{r[0]},{r[1]}\n")
    col = np.array([r[1] for r in rows], dtype=float)
    obs = a.obs
    om = f"{HERE}/results/obs_maxima.csv"
    if obs is None and os.path.exists(om):
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
