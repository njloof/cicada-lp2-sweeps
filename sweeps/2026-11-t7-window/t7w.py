#!/usr/bin/env python3
"""Campaign #30 — T7 fixed-window rate-ratio certification (PREREG F23).

PREREG.md (commit d326090) precedes every output. Statistic, nulls, plants,
gates and verdict rule exactly as registered; changes only as dated addenda.
Order enforced: kill gates -> nulls -> G3 -> plants (power curve) -> X_obs.

Run:  python3 sweeps/2026-11-t7-window/t7w.py
"""
import glob, json, math, os, sys, time, zlib
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
SEED = 20261230
L = 12956                 # runes
NS = L - 1                # doublet site positions 0..12954
K = 86
MINGAP = 6
BLOCKS = np.array([1000] * 12 + [956])
PIN_PROFILE = [8, 3, 7, 2, 6, 9, 10, 8, 11, 2, 9, 6, 5]
PIN_AC1 = 0.3795
J = 3611.5                # registered junction (#19 G4)
HALF = 825                # W* = [J-825, J+825] -> sites 2787..4436
WLO, WHI = 2787, 4436     # inclusive integer site bounds (1,650 sites)
D_NULL = 10_000
NPLANT = 200
RHOS = (0.0, 0.25, 0.5, 0.75, 1.0)
ALPHA = 0.05

def rng_for(tag, d):
    return np.random.default_rng([SEED, zlib.crc32(tag.encode()) % 100000, d])

# ---------------------------------------------------------------- gates
def census():
    """G1: reproduce #10 census exactly or stop (INSTRUMENT-INCOMPLETE)."""
    files = sorted(glob.glob(f'{ROOT}/data/pages/lp2_*.txt'))
    unsolved = [f for f in files if 'lp2_50' not in f and 'lp2_56' not in f and 'lp2_57' not in f]
    assert len(unsolved) == 55
    s = []
    for f in unsolved:
        s += [int(t) for t in open(f).read().split()]
    s = np.array(s)
    assert len(s) == L, "G1 FAIL: stream length"
    pos = np.where(s[:-1] == s[1:])[0]
    gaps = np.diff(pos)
    blocks = np.bincount(pos // 1000, minlength=13)
    assert len(pos) == K and gaps.min() == MINGAP, "G1 FAIL: sites"
    assert blocks.tolist() == PIN_PROFILE, "G1 FAIL: profile"
    g = gaps - gaps.mean()
    ac1 = float((g[:-1] * g[1:]).sum() / (g * g).sum())
    assert abs(ac1 - PIN_AC1) <= 1e-3, "G1 FAIL: ac1"
    return pos, gaps, ac1

def junction():
    """G2: J recomputed from page/line structure (no doublets involved)."""
    files = sorted(glob.glob(f'{ROOT}/data/pages/lp2_*.txt'))
    unsolved = [f for f in files if 'lp2_50' not in f and 'lp2_56' not in f and 'lp2_57' not in f]
    tot = 0
    for f in unsolved:
        lines = [ln for ln in open(f).read().splitlines() if ln.strip()]
        if 'lp2_15' in f:
            j = tot + len(lines[0].split()) - 1 + 0.5
        tot += sum(len(ln.split()) for ln in lines)
    assert abs(j - J) <= 0.5, "G2 FAIL: junction"
    return j

# ---------------------------------------------------------------- draws (#10 mechanics verbatim)
def draw_n1(rng):
    """Hard-core gap>=6 via y_j = p_j - 5j on a uniform subset of 0..NS-1-5(K-1)."""
    y = np.sort(rng.choice(NS - 5 * (K - 1), size=K, replace=False))
    return y + 5 * np.arange(K)

def ac1_of(gaps):
    g = gaps - gaps.mean()
    return float((g[:-1] * g[1:]).sum() / (g * g).sum())

def draw_plant_win(rng, rho):
    """Window plant: density rho inside W*, 1 outside; K=86 greedy with the
    same gap>=6 hard-core as N1 (#10 draw_plant mechanics, window indicator)."""
    w = np.ones(NS)
    w[WLO:WHI + 1] = rho
    cdf = np.cumsum(w)
    pos = []
    while len(pos) < K:
        t = int(np.searchsorted(cdf, rng.random() * cdf[-1]))
        if all(abs(t - q) >= MINGAP for q in pos):
            pos.append(t)
    return np.array(sorted(pos))

def xcount(pos, lo=WLO, hi=WHI):
    return int(((pos >= lo) & (pos <= hi)).sum())

# ---------------------------------------------------------------- exact hypergeometric sanity
def hyper_p_le(k, N=NS, Kk=K, n=WHI - WLO + 1):
    """P(X <= k) exact, X ~ Hypergeom(N, Kk, n), log-space products."""
    def logC(a, b):
        return sum(math.log(a - i) - math.log(i + 1) for i in range(b))
    lcN = logC(N, Kk)
    tot = 0.0
    for i in range(0, k + 1):
        if i > n or Kk - i > N - n: continue
        lp = logC(n, i) + logC(N - n, Kk - i) - lcN
        tot += math.exp(lp)
    return tot

def main():
    t0 = time.time()
    os.makedirs(f"{HERE}/results", exist_ok=True)
    pos, gaps, ac1 = census()
    j = junction()
    print(f"G1 PASS (86 sites, profile, ac1={ac1:.4f}); G2 PASS (J={j})")

    # ---- nulls (N1 primary) ----
    xs = np.empty(D_NULL, dtype=int); a1s = np.empty(D_NULL)
    for d in range(D_NULL):
        p = draw_n1(rng_for("N1", d))
        xs[d] = xcount(p)
        a1s[d] = ac1_of(np.diff(p))
    # G3: null calibration vs #10 recorded ac1 null mean/SD (-0.009 +/- 0.104)
    assert abs(a1s.mean() + 0.009) <= 0.01 and abs(a1s.std() - 0.104) <= 0.01, \
        f"G3 FAIL: ac1 null {a1s.mean():.3f} +/- {a1s.std():.3f}"
    print(f"G3 PASS (ac1 null {a1s.mean():.3f} +/- {a1s.std():.3f}); "
          f"N1 X null mean {xs.mean():.2f} sd {xs.std():.2f}")

    # critical value: largest t with add-one P(X <= t) <= ALPHA
    D = D_NULL
    tcrit = max(t for t in range(int(xs.max()) + 1)
                if (1 + (xs <= t).sum()) / (D + 1) <= ALPHA)
    print(f"critical value tcrit={tcrit} (add-one P(X<=tcrit)="
          f"{(1 + (xs <= tcrit).sum()) / (D + 1):.4f})")

    # ---- plants (power curve) BEFORE observed statistic ----
    plants = {}
    for rho in RHOS:
        hit = 0
        for d in range(NPLANT):
            if xcount(draw_plant_win(rng_for(f"plant{rho}", d), rho)) <= tcrit:
                hit += 1
        plants[str(rho)] = hit / NPLANT
        print(f"plant rho={rho}: power={hit / NPLANT:.3f}")
    assert plants["0.0"] >= 0.99, "DETECTABILITY GATE FAIL -> INSTRUMENT-FAIL"

    # ---- observed statistic (first computation, post-gates/plants) ----
    x_obs = xcount(pos)
    p_n1 = (1 + (xs <= x_obs).sum()) / (D + 1)
    p_h = hyper_p_le(x_obs)
    jitter = {s: xcount(pos, WLO + s, WHI + s) for s in (-100, -50, 0, 50, 100)}

    verdict = "CERTIFIED-NONSTATIONARY" if p_n1 <= ALPHA else "LOCALIZATION-RETIRE"
    out = {"seed": SEED, "prereg_commit": "d326090",
           "window": {"J": J, "lo": WLO, "hi": WHI, "width": WHI - WLO + 1},
           "gates": {"G1": "PASS", "G2": "PASS", "G3": "PASS",
                     "ac1_obs": ac1, "ac1_null": [float(a1s.mean()), float(a1s.std())]},
           "null": {"D": D, "mean": float(xs.mean()), "sd": float(xs.std()),
                    "tcrit": int(tcrit)},
           "plants": plants, "x_obs": x_obs,
           "p_N1": float(p_n1), "p_hypergeom": float(p_h),
           "rate_ratio": x_obs / (K * (WHI - WLO + 1) / NS),
           "jitter_report_only": jitter,
           "verdict": verdict, "runtime_s": time.time() - t0}
    json.dump(out, open(f"{HERE}/results/t7w.json", "w"), indent=1)
    print(f"X_obs={x_obs} (null mean {xs.mean():.2f})  p_N1={p_n1:.5f}  "
          f"p_hyper={p_h:.5f}  ratio={out['rate_ratio']:.3f}")
    print(f"VERDICT: {verdict}  ({out['runtime_s']:.1f}s)")

if __name__ == "__main__":
    main()
