#!/usr/bin/env python3
"""#32 tests32: registered tests T1 (value<->metric eta^2, within-line
permutation null) and T2 (Rayleigh of frac(cx)), plants FIRST, then
T_obs, then verdict applied verbatim (PREREG sections 2,3,5 + 1b
coverage escalation). Reads work/table32.jsonl (studio). Seed 20261232;
per-stream default_rng([SEED, stream]) — host-independent streams."""
import json, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
SEED = 20261232
METRICS = ("fx", "fy", "cx", "cy", "w", "h", "area", "gap")
D_NULL, D_MC = 2000, 20000
ALPHA = 0.025                      # Bonferroni x2 per PREREG

def rng_for(stream):
    return np.random.default_rng([SEED, stream])

def load_rows():
    rows = [json.loads(l) for l in
            open(os.path.join(ROOT, "work", "table32.jsonl"))]
    return rows

def build_matrix(rows):
    """within-line z per metric; NaN (pos-0 gaps) -> z=0 with mask off."""
    N = len(rows)
    Z = np.zeros((N, len(METRICS))); M = np.zeros((N, len(METRICS)))
    line_id = np.array([(r["page"], r["line"]) for r in rows], dtype=object)
    # group rows by line
    byl = {}
    for i, r in enumerate(rows):
        byl.setdefault((r["page"], r["line"]), []).append(i)
    for k, idx in byl.items():
        idx = np.array(idx)
        for mi, m in enumerate(METRICS):
            x = np.array([rows[i][m] for i in idx], dtype=float)
            ok = np.isfinite(x)
            if ok.sum() >= 3:
                mu = x[ok].mean(); sd = x[ok].std()
                if sd > 1e-12:
                    Z[np.ix_(idx[ok], [mi])] = ((x[ok] - mu) / sd)[:, None]
                    M[np.ix_(idx[ok], [mi])] = 1.0
    V = np.array([r["value"] for r in rows])
    keys = np.array([f"{r['page']}:{r['line']}" for r in rows])
    _, L = np.unique(keys, return_inverse=True)   # deterministic ids
    return Z, M, V, L, byl

def t1_all(Z, M, V):
    """pooled eta^2 per metric: sum_v acc[v]^2/nv[v] / SS."""
    out = np.zeros(Z.shape[1])
    for mi in range(Z.shape[1]):
        z = Z[:, mi]; keep = M[:, mi] > 0
        zz = np.where(keep, z, 0.0)
        acc = np.bincount(V, weights=zz, minlength=29)
        nv = np.bincount(V[keep], minlength=29).astype(float)
        SS = float((zz ** 2).sum())
        with np.errstate(divide="ignore", invalid="ignore"):
            terms = np.where(nv > 0, acc ** 2 / np.maximum(nv, 1), 0.0)
        out[mi] = terms.sum() / SS if SS > 0 else 0.0
    return out

def main():
    rows = load_rows()
    Z, M, V, L, byl = build_matrix(rows)
    N = len(rows)
    print(f"table: {N} aligned runes, {len(byl)} lines, "
          f"{len(set(r['page'] for r in rows))} pages", flush=True)

    # ---- timing probe (owner rule: ETA stated before the long part)
    import time
    t0 = time.time()
    _null_draw(V, L, Z, M, rng_for(999))
    est = (time.time() - t0) * (D_NULL + 20 * 4 + 20 * 3 + 1)
    print(f"timing probe: ETA for nulls+plants ~{est:.0f}s", flush=True)

    # ---- PLANTS FIRST (PREREG section 3)
    t1_obs_pre = t1_all(Z, M, V)
    mstar = int(np.argmax(t1_obs_pre))
    print(f"plant(i) metric = argmax T1_obs = {METRICS[mstar]}", flush=True)
    power_i = {}
    for ei, eps in enumerate((0.02, 0.05, 0.10, 0.20)):
        rng = rng_for(2 + ei)
        hits = 0
        Zp = Z.copy(); Mp = M
        for _ in range(20):
            inj = eps * (V - 14) / 14.0
            Zp[:, mstar] = np.where(Mp[:, mstar] > 0, Z[:, mstar] + inj, 0.0)
            t1p = t1_all(Zp, Mp, V)[mstar]
            power_i.setdefault("raw_" + str(eps), []).append(t1p)
        power_i[eps] = power_i.pop("raw_" + str(eps))
    power_ii = {}
    fcx = np.array([r["fx"] for r in rows])   # fx = frac(cx) per table32
    for ji, jit in enumerate((0.1, 0.3, 1.0)):
        rng = rng_for(6 + ji)
        ps = []
        for _ in range(20):
            f = (V / 29.0 + jit * rng.random(N)) % 1.0
            ps.append(rayleigh_p(f))
        power_ii[jit] = ps

    # ---- NULLS
    nulls = np.zeros(D_NULL)
    rng = rng_for(1)
    for d in range(D_NULL):
        nulls[d] = _null_draw(line_start, bounds, V, Z, M, rng)
        if (d + 1) % 500 == 0: print(f"null {d+1}/{D_NULL} "
                                     f"({time.time()-t0:.0f}s)", flush=True)
    # ---- T_obs
    t1_obs = t1_all(Z, M, V)
    T1_obs = float(t1_obs.max())
    p_T1 = (1 + int((nulls >= T1_obs).sum())) / (D_NULL + 1)
    T2_R, p_T2 = rayleigh_stats(fcx)
    # MC cross-check: n*R^2 ~ Exp(1) under uniform (large-n)
    rm = rng_for(9).exponential(1.0, D_MC)
    p_T2_mc = float((rm >= N * T2_R ** 2).mean())

    # ---- power at registered alpha against the SAME null draws
    def p_from_null(t1v):
        return (1 + (nulls >= t1v).sum()) / (D_NULL + 1)
    pw_i = {e: float(np.mean([p_from_null(t) <= ALPHA for t in ts]))
            for e, ts in power_i.items() if not isinstance(e, str)}
    pw_ii = {j: float(np.mean([p <= ALPHA for p in ps]))
             for j, ps in power_ii.items()}
    gate_T1 = pw_i.get(0.10, 0) >= 0.95
    gate_T2 = pw_ii.get(0.3, 0) >= 0.95
    print(f"plant(i) power {pw_i}")
    print(f"plant(ii) power {pw_ii}")
    print(f"T1_obs={T1_obs:.4f} (metric {METRICS[int(np.argmax(t1_obs))]}) "
          f"null_med={np.median(nulls):.4f} c95={np.quantile(nulls,0.95):.4f} "
          f"p_T1={p_T1:.4g}")
    print(f"T2: R={T2_R:.5f} n={N} p_analytic={p_T2:.4g} p_mc={p_T2_mc:.4g}")
    print(f"gates: T1-power {gate_T1}, T2-power {gate_T2}")

    # ---- verdict (PREREG section 5 + 1b escalation), applied verbatim
    cov = json.load(open(os.path.join(HERE, "results", "coverage32.json")))
    pct = cov["_total"]["pct"]
    prefix = "" if pct >= 95 else ("PARTIAL-COVERAGE-" if pct >= 70
                                   else "INSTRUMENT-FAIL-")
    if prefix == "INSTRUMENT-FAIL-":
        verdict = "INSTRUMENT-FAIL"
    elif min(p_T1, p_T2) <= ALPHA:
        verdict = prefix + "FLAGGED"
    elif gate_T1 and gate_T2:
        verdict = prefix + "CLOSED-PRINTNULL"
    else:
        verdict = prefix + "UNPOWERED-NULL"
    print(f"VERDICT: {verdict} (coverage {pct:.1f}%)")

    out = dict(seed=SEED, n_runes=N, n_lines=len(byl),
               metrics=list(METRICS), T1_obs=T1_obs,
               T1_per_metric={METRICS[i]: float(t1_obs[i])
                              for i in range(len(METRICS))},
               null_median=float(np.median(nulls)),
               null_c95=float(np.quantile(nulls, 0.95)), p_T1=p_T1,
               T2_R=float(T2_R), p_T2_analytic=float(p_T2),
               p_T2_mc=p_T2_mc, D_null=D_NULL,
               plant_i_power=pw_i, plant_ii_power=pw_ii,
               gate_T1=bool(gate_T1), gate_T2=bool(gate_T2),
               plant_metric=METRICS[mstar], coverage_pct=pct,
               verdict=verdict)
    json.dump(out, open(os.path.join(HERE, "results", "tests32.json"), "w"),
              indent=1)

def rayleigh_p(f):
    R, p = rayleigh_stats(f)
    return p

def rayleigh_stats(f):
    z = np.exp(2j * np.pi * f)
    R = float(abs(z.sum()) / len(f))
    p = float(np.exp(-len(f) * R * R))
    return R, min(p, 1.0)

def _null_draw(V, L, Z, M, rng):
    """permute values within each line (lexsort by (random, line):
    positions keep their line, values reshuffle inside it); return max
    eta^2 over metrics."""
    N = len(V)
    # two independent random orders within each line block: position
    # order1[k] (line l) receives value of order2[k] (same line l)
    o1 = np.lexsort((rng.random(N), L))
    o2 = np.lexsort((rng.random(N), L))
    Vp = np.empty(N, dtype=V.dtype)
    Vp[o1] = V[o2]
    return float(t1_all(Z, M, Vp).max())

if __name__ == "__main__":
    main()
