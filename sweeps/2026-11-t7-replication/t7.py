#!/usr/bin/env python3
"""Campaign #10 — T7 replication + smooth-heterogeneity power curve.

PREREG.md (commit d1d81a8) precedes every output. Statistics, nulls, plants,
thresholds and verdict rule are exactly as registered; changes only as dated
addenda before real-data scoring.

Run:  python3 sweeps/2026-11-t7-replication/t7.py [--stage 2000|10000]
"""
import glob, json, os, sys, time, zlib
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
SEED = 20261128
L = 12956
K = 86
MINGAP = 6
BLOCKS = np.array([1000]*12 + [956])
ALPHA = 0.0025                      # Bonferroni/4 over family alpha 0.01
PIN_PROFILE = [8, 3, 7, 2, 6, 9, 10, 8, 11, 2, 9, 6, 5]
PIN_AC1 = 0.3795

def stream():
    files = sorted(glob.glob('data/pages/lp2_*.txt'))
    unsolved = [f for f in files if 'lp2_50' not in f and 'lp2_56' not in f and 'lp2_57' not in f]
    assert len(unsolved) == 55
    s = []
    for f in unsolved:
        s += [int(t) for t in open(f).read().split()]
    return np.array(s)

def census():
    """Kill gate: reproduce the pinned premise exactly or stop."""
    s = stream()
    assert len(s) == L, "INSTRUMENT-INCOMPLETE: stream length"
    pos = np.where(s[:-1] == s[1:])[0]
    gaps = np.diff(pos)
    blocks = np.bincount(pos // 1000, minlength=13)
    assert len(pos) == K and gaps.min() == MINGAP, "INSTRUMENT-INCOMPLETE: sites"
    assert blocks.tolist() == PIN_PROFILE, "INSTRUMENT-INCOMPLETE: profile"
    return pos, gaps

def _rank_avg(x):
    """Tie-averaged ranks (scipy convention) for one row."""
    o = np.argsort(x, kind="stable"); s = x[o]
    r = np.empty(len(x)); i = 0
    while i < len(x):
        j = i
        while j + 1 < len(x) and s[j + 1] == s[i]:
            j += 1
        r[o[i:j + 1]] = (i + j) / 2.0
        i = j + 1
    return r

def stats(pos, gaps):
    """The four registered statistics. Called with single draws (D=1)."""
    pos = np.atleast_2d(pos); gaps = np.atleast_2d(gaps)
    assert pos.shape[0] == 1
    edges = np.cumsum(BLOCKS)[:-1]
    bid = np.searchsorted(edges, pos[0])
    blk = np.bincount(bid, minlength=13).astype(float)[None, :]
    e = K * BLOCKS / L
    s1 = (((blk - e) ** 2) / e).sum(axis=1)
    g = gaps[0] - gaps[0].mean()
    s2 = np.array([(g[:-1] * g[1:]).sum() / (g * g).sum()])
    r = _rank_avg(gaps[0]); rc = r - r.mean()
    s3 = np.array([(rc[:-1] * rc[1:]).sum() / (rc * rc).sum()])
    sign = (blk[0] > e).astype(int)
    s4 = np.array([1 + int((sign[1:] != sign[:-1]).sum())])
    return s1, s2, s3, s4

def draw_n2(rng, D):
    return np.sort(rng.choice(L - 1, size=(D, K), replace=False), axis=1)

def draw_n1(rng, D):
    """Hard-core gap>=6 via y_j = p_j - 5j on a uniform subset of 0..L-2-5(K-1)."""
    y = np.sort(rng.choice(L - 1 - 5 * (K - 1), size=(D, K), replace=False), axis=1)
    return y + 5 * np.arange(K)

def draw_plant(rng, D, kind, delta):
    """Smooth-heterogeneity plant: ordered sites of an inhomogeneous Poisson
    process conditioned on N=K == K iid draws from the normalized density
    (exact), taken greedily with the SAME gap>=6 hard-core as N1 (sequential
    greedy is a documented proxy for the constrained joint). One density
    (one phase) per draw."""
    assert D == 1
    phi = rng.uniform(0, 2 * np.pi)
    grid = np.arange(L - 1)
    if kind == "sin":
        w = 1 + delta * np.sin(2 * np.pi * grid / L + phi)
    else:  # step
        w = np.where(grid < L / 2, 1 + delta, 1 - delta)
    cdf = np.cumsum(w)
    pos = []
    while len(pos) < K:
        t = int(np.searchsorted(cdf, rng.random() * cdf[-1]))
        if all(abs(t - q) >= MINGAP for q in pos):
            pos.append(t)
    return np.array(sorted(pos))[None, :]

def rng_for(tag, draw):
    return np.random.default_rng([SEED, zlib.crc32(tag.encode()) % 100000, draw])

def battery(obs, nulls):
    """add-one p-values; two-sided = 2*min side capped at 1."""
    out = {}
    s1o, s2o, s3o, s4o = (x[0] for x in stats(*obs))
    names = ["S1_blockchi2", "S2_pearson_ac1", "S3_spearman_ac1", "S4_runs"]
    obs_v = [s1o, s2o, s3o, s4o]
    sides = ["one", "two", "two", "two"]
    for tag, (n1, n2, n3, n4) in nulls.items():
        nullmat = [n1, n2, n3, n4]
        for nm, ov, nv, side in zip(names, obs_v, nullmat, sides):
            D = len(nv)
            plo = (1 + (nv <= ov).sum()) / (D + 1)
            phi_ = (1 + (nv >= ov).sum()) / (D + 1)
            p = phi_ if side == "one" else min(1.0, 2 * min(plo, phi_))
            out.setdefault(nm, {})[tag] = {"obs": float(ov), "p": float(p),
                                           "null_mean": float(nv.mean()), "null_sd": float(nv.std())}
    return out

def main():
    t0 = time.time()
    stage = int(sys.argv[sys.argv.index("--stage") + 1]) if "--stage" in sys.argv else 2000
    os.makedirs(f"{HERE}/results", exist_ok=True)
    pos, gaps = census()
    obs = (pos[None, :], gaps[None, :])
    print(f"census gate PASS; obs stats = {[float(x[0]) for x in stats(*obs)]}")

    nulls = {}
    for tag, drawer in (("N1", draw_n1), ("N2", draw_n2)):
        acc = {i: [] for i in range(4)}
        for d in range(stage):
            p = drawer(rng_for(tag, d), 1)[0]
            st = stats(p[None, :], np.diff(p)[None, :])
            for i in range(4):
                acc[i].append(float(st[i][0]))
        nulls[tag] = tuple(np.array(acc[i]) for i in range(4))
        print(f"{tag}: {stage} draws done ({time.time()-t0:.1f}s)")

    res = battery(obs, nulls)
    for nm in res:
        print(nm, {t: round(v["p"], 5) for t, v in res[nm].items()})

    # escalation rule (PREREG): S1 or S2 on N1 <= 0.01 -> extend to 10,000
    esc = res["S1_blockchi2"]["N1"]["p"] <= 0.01 or res["S2_pearson_ac1"]["N1"]["p"] <= 0.01
    if esc and stage < 10000:
        print("escalation fired -> extending N1/N2 to 10,000")
        for tag, drawer in (("N1", draw_n1), ("N2", draw_n2)):
            more = {i: [] for i in range(4)}
            for d in range(stage, 10000):
                p = drawer(rng_for(tag, d), 1)[0]
                st = stats(p[None, :], np.diff(p)[None, :])
                for i in range(4):
                    more[i].append(float(st[i][0]))
            nulls[tag] = tuple(np.concatenate([nulls[tag][i], np.array(more[i])]) for i in range(4))
        res = battery(obs, nulls)
        for nm in res:
            print(nm, {t: round(v["p"], 5) for t, v in res[nm].items()})

    # critical values from N1 (primary null) for the power curve
    n1 = nulls["N1"]
    crit = {"S1_blockchi2": np.quantile(n1[0], 1 - ALPHA),
            "S2_pearson_ac1": np.quantile(n1[1], 1 - ALPHA / 2),
            "S3_spearman_ac1": np.quantile(n1[2], 1 - ALPHA / 2),
            "S4_runs": None}   # runs: two-sided discrete; use both tails below
    lo4 = np.quantile(n1[3], ALPHA / 2)

    plants = {}
    grid = [("sin", d) for d in (0.3, 0.5, 0.7, 0.9)] + [("step", d) for d in (0.35, 0.5)]
    for gi, (kind, delta) in enumerate(grid):
        tag = f"P-{kind}{delta}"
        s1s, s2s, s3s, s4s = [], [], [], []
        for d in range(200):
            p = draw_plant(rng_for(tag, d), 1, kind, delta)[0]
            st = stats(p[None, :], np.diff(p)[None, :])
            s1s.append(float(st[0][0])); s2s.append(float(st[1][0]))
            s3s.append(float(st[2][0])); s4s.append(float(st[3][0]))
        pw = {"S1": float(np.mean(np.array(s1s) >= crit["S1_blockchi2"])),
              "S2": float(np.mean(np.array(s2s) >= crit["S2_pearson_ac1"])),
              "S3": float(np.mean(np.array(s3s) >= crit["S3_spearman_ac1"])),
              "S4": float(np.mean((np.array(s4s) <= lo4) | (np.array(s4s) >= np.quantile(n1[3], 1 - ALPHA / 2))))}
        plants[tag] = {"power": pw, "ac1_mean": float(np.mean(s2s))}
        print(tag, pw)

    # observed-amplitude calibration: first-Fourier amplitude of block profile vs mean
    s1o = res["S1_blockchi2"]["N1"]["obs"]
    blk = np.array(PIN_PROFILE, dtype=float); e = K * BLOCKS / L
    k = np.arange(13)
    a = 2 * np.sum((blk - e) * np.cos(2 * np.pi * k / 13)) / 13
    b = 2 * np.sum((blk - e) * np.sin(2 * np.pi * k / 13)) / 13
    delta_fit = float(np.hypot(a, b) / e.mean())

    fired = [nm for nm in res if res[nm]["N1"]["p"] <= ALPHA]
    verdict = "REPLICATE" if fired else "NO-REPLICATE"
    out = {"seed": SEED, "stage": stage, "escalated": esc and stage < 10000,
           "draws": {t: len(v[0]) for t, v in nulls.items()},
           "battery": res, "critical": {k2: (float(v) if v is not None else None) for k2, v in crit.items()},
           "runs_lo": float(lo4), "plants": plants, "delta_fit": delta_fit,
           "fired": fired, "verdict": verdict, "runtime_s": time.time() - t0}
    json.dump(out, open(f"{HERE}/results/t7_battery.json", "w"), indent=1)
    print(f"VERDICT: {verdict} fired={fired} delta_fit={delta_fit:.3f} "
          f"({out['runtime_s']:.1f}s)")

if __name__ == "__main__":
    main()
