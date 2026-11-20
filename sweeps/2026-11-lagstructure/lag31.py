#!/usr/bin/env python3
"""Campaign #31 — full-lag key-reuse/structure scan (PREREG F24).

PREREG.md (commit 17185d8) precedes every output. Statistic, null, plants,
gates, verdict rule exactly as registered. Order: gates -> plants (power,
needs null c95 -> nulls first among computations, but no real-data T until
plants+nulls done) -> T_obs -> verdict.

Run:  python3 sweeps/2026-11-lagstructure/lag31.py [--nulls N]
"""
import glob, json, os, sys, time, zlib
import numpy as np
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, "sweeps/2026-11-hintgrammar"))

SEED = 20261231
L = 12956
N = 29
LO, HI = 41, 12823                 # registered lag band (n_ell >= 132)
D_NULL = 2000
NPLANT = 20
NPROC = min(12, os.cpu_count() or 4)
NFFT = 1 << (2 * L - 1).bit_length()

# lag axis for irfft outputs: C_ab[ell] = #{t: s[t+ell]=a, s[t]=b}, ell=0..L-1
LAGS = slice(LO, HI + 1)

def rng_for(tag, d):
    return np.random.default_rng([SEED, zlib.crc32(tag.encode()) % 100000, d])

def stream():
    files = sorted(glob.glob(f'{ROOT}/data/pages/lp2_*.txt'))
    unsolved = [f for f in files if 'lp2_50' not in f and 'lp2_56' not in f and 'lp2_57' not in f]
    assert len(unsolved) == 55
    s = []
    for f in unsolved:
        s += [int(t) for t in open(f).read().split()]
    s = np.array(s, dtype=np.int64)
    assert len(s) == L
    return s

# ---------------------------------------------------------------- statistic machinery
def T_of(s):
    """Registered T: max chi2-vs-uniform over lags [LO,HI], diff and sum families."""
    n_ell = (L - np.arange(LO, HI + 1)).astype(float)
    F = [np.fft.rfft((s == a).astype(np.float64), n=NFFT) for a in range(N)]
    # accumulate chi2 over bins per lag
    chi2 = np.zeros(HI - LO + 1)
    # counts per (bin d, lag): build via grouping C_ab
    # diff bin d: pairs (a,b) with (a-b)%29==d ; sum bin d: (a+b)%29==d
    dc = np.zeros((N, HI - LO + 1)); sc = np.zeros((N, HI - LO + 1))
    for a in range(N):
        for b in range(N):
            c = np.fft.irfft(F[a] * np.conj(F[b]), n=NFFT)[:L][LO:HI + 1]
            dc[(a - b) % N] += c
            sc[(a + b) % N] += c
    e = n_ell / N
    # registered T = max over lags of max(family chi2); families kept separate
    xd = ((dc - e) ** 2 / e).sum(axis=0)
    xs = ((sc - e) ** 2 / e).sum(axis=0)
    i = int(np.argmax(np.maximum(xd, xs)))
    return float(max(xd[i], xs[i])), int(LO + i), ("diff" if xd[i] >= xs[i] else "sum")

# ---------------------------------------------------------------- gates
def gates(s):
    assert np.sum(s[1:] == s[:-1]) == 86, "G2 FAIL: doublet count"
    cnt = np.bincount(s, minlength=N)
    chi_u = float(((cnt - L / N) ** 2 / (L / N)).sum())
    assert chi_u < 100, f"G2 FAIL: unigram chi2 {chi_u}"
    # G3: FFT counts == brute force on random cells
    rng = rng_for("G3", 0)
    F = [np.fft.rfft((s == a).astype(np.float64), n=NFFT) for a in range(N)]
    for _ in range(200):
        a, b = rng.integers(0, N, 2); ell = int(rng.integers(1, L))
        fftv = np.fft.irfft(F[a] * np.conj(F[b]), n=NFFT)[:L][ell]
        brute = np.sum((s[ell:] == a) & (s[:L - ell] == b))
        assert abs(fftv - brute) < 0.5, f"G3 FAIL: a{a} b{b} ell{ell} fft={fftv} brute={brute}"
    return chi_u

# ---------------------------------------------------------------- plants/nulls workers
def plant_stream(kind, ell, sign, rng, P):
    if kind == "per":
        K = rng.integers(0, N, ell)
        return (P + np.tile(K, (L + ell) // ell)[:L]) % N
    c = P.copy()
    if kind == "cta":
        prev_src = lambda t: c[t - ell]
    else:  # pta
        prev_src = lambda t: P[t - ell]
    for t in range(ell, L):
        c[t] = (P[t] + sign * prev_src(t)) % N
    return c

def _null_job(d):
    s = stream()
    perm = rng_for("null", d).permutation(L)
    return T_of(s[perm])[0]

def _plant_job(arg):
    kind, ell, sign, d, P = arg
    return T_of(plant_stream(kind, ell, sign, rng_for(f"P-{kind}-{ell}-{sign}", d), P))[0]

# ---------------------------------------------------------------- main
def main():
    t0 = time.time()
    nd = int(sys.argv[sys.argv.index("--nulls") + 1]) if "--nulls" in sys.argv else D_NULL
    os.makedirs(f"{HERE}/results", exist_ok=True)
    s = stream()
    chi_u = gates(s)
    print(f"G1 pass (external), G2 PASS (86 doublets, unigram chi2={chi_u:.1f}), G3 PASS (200/200 exact)")

    import grammar
    P = np.array(grammar.text_vals(open(os.path.join(
        grammar.ARMADA, "emerson_essays_first_series.txt")).read())[:L], dtype=np.int64)
    assert len(P) == L, "plant plaintext short"

    cells = ([("per", e, sg) for e in (41, 100, 400, 1000, 2000, 4000, 6400, 8000, 10000, 11781, 12400, 12823) for sg in (1, -1)]
             + [("cta", e, sg) for e in (41, 100, 400, 1000, 2000, 4000, 6400, 8000, 10000, 11781, 12400, 12823) for sg in (1, -1)]
             + [("pta", e, sg) for e in (41, 100, 400, 1000, 2000, 4000, 6400) for sg in (1, -1)])

    with Pool(NPROC) as pool:
        # timing probe -> ETA (memory rule: ETA at launch/after observation)
        probe = pool.map(_plant_job, [("per", 1000, 1, d, P) for d in range(NPROC)])
        tp = (time.time() - t0) / NPROC
        total_units = nd + len(cells) * NPLANT + NPROC
        print(f"timing probe: {tp:.2f}s/stream on {NPROC} workers -> "
              f"ETA ~{total_units * tp / NPROC / 60:.1f} min")

        tperm = np.array(pool.map(_null_job, range(nd), chunksize=4))
        print(f"nulls done ({nd} draws, {time.time()-t0:.0f}s): "
              f"T_perm median {np.median(tperm):.1f} max {tperm.max():.1f}")
        c95 = float(np.quantile(tperm, 0.95))

        jobs = [(k, e, sg, d, P) for (k, e, sg) in cells for d in range(NPLANT)]
        res = pool.map(_plant_job, jobs, chunksize=8)
    powers = {}
    for ci, (k, e, sg) in enumerate(cells):
        vals = np.array(res[ci * NPLANT:(ci + 1) * NPLANT])
        powers[f"{k}-{e}-s{sg}"] = float((vals >= c95).mean())

    # ---- observed statistic (after gates/nulls/plants) ----
    T_obs, ell_star, fam_star = T_of(s)
    p_obs = (1 + int((tperm >= T_obs).sum())) / (nd + 1)

    # detectability gates (registered wording)
    weak = [k for k, v in powers.items()
            if (k.startswith(("per", "cta")) and int(k.split("-")[1]) <= 12400 and v < 0.95)
            or (k.startswith("pta") and int(k.split("-")[1]) <= 4000 and v < 0.95)]
    if T_obs >= c95:
        verdict = "FLAGGED"
    elif not weak:
        verdict = "CLOSED-NOLAGSTRUCTURE"
    else:
        verdict = "UNPOWERED-NULL"

    out = {"seed": SEED, "prereg_commit": "17185d8", "band": [LO, HI],
           "null": {"D": nd, "median": float(np.median(tperm)), "max": float(tperm.max()),
                    "c95": c95},
           "powers": powers, "weak_cells": weak,
           "T_obs": T_obs, "ell_star": ell_star, "fam_star": fam_star,
           "p_obs": p_obs, "verdict": verdict, "runtime_s": time.time() - t0}
    json.dump(out, open(f"{HERE}/results/lag31.json", "w"), indent=1)
    print(f"T_obs={T_obs:.1f} at ell*={ell_star} ({fam_star})  c95={c95:.1f}  "
          f"p={p_obs:.4f}  weak_cells={weak}")
    print(f"VERDICT: {verdict}  ({out['runtime_s']:.0f}s)")

if __name__ == "__main__":
    main()
