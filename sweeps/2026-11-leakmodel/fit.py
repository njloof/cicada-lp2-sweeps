#!/usr/bin/env python3
"""Campaign #26 — Track A: leak-model changepoint fit + key-consumption
identifiability. PREREG.md (registered 2026-11-19) precedes every output;
verdict rules are exactly as registered.

Lane A1 (local, minutes): flat-key idiom-equivalence simulation (key-skip vs
plaintext-redraw emit the same distribution -> key consumption NOT
identifiable; skip-tolerant decoder class adopted for power claims).
Lane A2 (studio): exact-DP piecewise-Bernoulli changepoint comparison on the
12,955-pair leak sequence; registered prediction T7-as-changepoint with
10,000-draw parametric-bootstrap calibration + page-block CV + plant power.

Run:  python3 sweeps/2026-11-leakmodel/fit.py gates
      python3 sweeps/2026-11-leakmodel/fit.py a1
      python3 sweeps/2026-11-leakmodel/fit.py a2          (fit+null+cv+hmm+power)
Seeding: PREREG's Random("20261226:{d}") notation implemented house-style as
default_rng([20261226, crc32(tag)%100000, d]) — deterministic per-draw
substreams, same intent, bit-identical reruns.
"""
import json, os, subprocess, sys, time, zlib
from multiprocessing import Pool
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, ROOT)
from core import validate as V                                    # noqa: E402

RES = os.path.join(HERE, "results")
SEED = 20261226
PAGES = list(range(50)) + list(range(51, 56))                     # book 0-49 + 51-55
EDGES = (2740, 4389)                                              # registered void windows
WIN = 150                                                         # +-150 runes
DMIN = 50                                                         # min segment span
D_BOOT, D_PLANT = 10_000, 20
NPLANT = 10

def rng_for(tag, d): return np.random.default_rng([SEED, zlib.crc32(tag.encode()) % 100000, d])

# ---------------------------------------------------------------- data + gates

def leak_stream():
    """(coords, ev): pair coords 1..12955 (0-based second-rune index) and the
    doublet indicator L_t = 1[C_t == C_{t-1}]."""
    s = np.array([r for p in PAGES for r in V.flat(p)], dtype=np.int8)
    assert len(s) == 12_956, f"corpus length {len(s)} != 12956"
    eq = s[1:] == s[:-1]
    return np.arange(1, len(s), dtype=np.int64), eq

def page_boundaries():
    lens = [len(V.flat(p)) for p in PAGES]
    assert sum(lens) == 12_956
    return list(np.cumsum(lens)[:-1])                             # 54 internal

def gates():
    ok = True
    r = subprocess.run([sys.executable, "-m", "core.validate"], cwd=ROOT,
                       capture_output=True, text=True)
    print(f"G1 validate.py: {'PASS' if r.returncode == 0 else 'FAIL'}")
    ok &= r.returncode == 0
    coords, ev = leak_stream()
    sites = coords[ev]
    cond = (len(sites) == 86 and set(EDGES) | {3140, 3852} <= set(sites.tolist())
            and list(np.diff(sorted([2740, 3140, 3852, 4389]))) == [400, 712, 537])
    print(f"G2 doublets: {len(sites)} (86) sites incl {EDGES + (3140, 3852)}, "
          f"gaps 400/712/537: {'PASS' if cond else 'FAIL'}")
    ok &= cond
    b = page_boundaries()
    cond = len(b) == 54 and not any(abs(x - e) < 50 for x in b for e in EDGES)
    print(f"G3 54 page boundaries; void edges NOT near page edges "
          f"(min dist {min(min(abs(x-e) for x in b) for e in EDGES)}): {'PASS' if cond else 'FAIL'}")
    ok &= cond
    cond = True
    # G4a: DP == exhaustive brute force (optimizer exactness), PREREG addendum
    import itertools
    for k, N in [(1, 160), (2, 210), (3, 260)]:
        rng = np.random.default_rng([SEED, 998, k])
        evp = rng.random(N) < rng.uniform(0.01, 0.1)
        fit = dp_fit(np.arange(1, N + 1), evp, k)
        dp_b = sorted(fit["fits"][k]["bounds"])
        best, argb = np.inf, None
        for cuts in itertools.combinations(range(50, N - 49), k):
            cuts = sorted(cuts)
            if any(y - x < 50 for x, y in zip([0] + cuts, cuts + [N])):
                continue
            pcx = np.concatenate([[0], np.cumsum(evp)])
            segs = [0] + list(cuts) + [N]
            c = 0.0
            for i in range(k + 1):
                n_ = segs[i + 1] - segs[i]; kk_ = int(pcx[segs[i + 1]] - pcx[segs[i]])
                if kk_ == 0 or kk_ == n_:
                    continue
                c -= kk_ * np.log(kk_ / n_) + (n_ - kk_) * np.log1p(-kk_ / n_)
            if c < best:
                best, argb = c, [x + 1 for x in cuts]
        okk = dp_b == sorted(argb)
        cond &= okk
        print(f"G4a brute k={k} N={N}: DP {dp_b} == brute {sorted(argb)} "
              f"{'ok' if okk else 'MISMATCH'}")
    # G4b: recovery within registered +-150 resolution (addendum), exact reported
    for k, plant in [(1, [6000]), (2, [4000, 9000]), (3, [3000, 7000, 12000]),
                     (4, [2500, 5500, 9500, 14000])]:
        rng = np.random.default_rng([SEED, 999, k])
        N = 20_000
        rates = ([0.05, 0.005] * 3 + [0.05, 0.005])[:k + 1]
        cuts = [0] + plant + [N]
        evp = np.zeros(N, dtype=bool)
        for i in range(k + 1):
            a, b2 = cuts[i], cuts[i + 1]
            evp[a:b2] = rng.random(b2 - a) < rates[i]
        fit = dp_fit(np.arange(1, N + 1), evp, k)
        got = sorted(int(c) for c in fit["fits"][k]["bounds"])
        want = sorted(p + 1 for p in plant)                        # ev idx -> pair coord
        okk = all(abs(g - w) <= 150 for g, w in zip(got, want)) and len(got) == k
        cond &= okk
        print(f"G4b synthetic k={k}: planted {want} -> fitted {got} "
              f"(exact={got == want}) {'ok' if okk else 'MISMATCH'}")
    ok &= cond
    if not ok:
        sys.exit("GATES FAILED — no statistic may be touched.")
    print("ALL GATES PASS")

# ------------------------------------------------------------------- DP fitter

def _dp_layer(prev, pc, coords, cmax):
    """One DP layer: V[j] = min cost over cut a of prev[a] + cost(a, j).
    cost = -binomial LL over positions [a, j) (counts), min span DMIN coords."""
    N = len(coords)
    Vv = np.full(N + 1, np.inf)
    arg = np.zeros(N + 1, dtype=np.int64)
    for j in range(1, N + 1):
        hi = cmax[j - 1]                                          # last a with span>=DMIN
        if hi < 0 or not np.isfinite(prev[:hi + 1]).any():
            continue
        a = np.arange(0, hi + 1)
        nn = (j - a).astype(float)
        kk = (pc[j] - pc[a]).astype(float)
        with np.errstate(divide="ignore", invalid="ignore"):
            t1 = np.where(kk > 0, kk * np.log(kk / nn), 0.0)
            t2 = np.where(kk < nn, (nn - kk) * np.log1p(-np.minimum(kk / nn, 1.0)), 0.0)
        vals = prev[a] - (t1 + t2)
        i = int(np.argmin(vals))
        Vv[j], arg[j] = vals[i], a[i]
    return Vv, arg

def dp_fit(coords, ev, kmax):
    """Exact piecewise-Bernoulli DP, k=0..kmax changepoints, BIC params 1+2k.
    Returns per-k BIC, boundaries (coords), rates, and dBIC vs k=0."""
    N = len(coords)
    pc = np.concatenate([[0], np.cumsum(ev)])
    cmax = np.searchsorted(coords, coords - DMIN + 1, side="right") - 1  # span guard
    bic, store, args = {}, {}, {}
    cost0 = -(pc[N] * np.log(pc[N] / N) + (N - pc[N]) * np.log1p(-pc[N] / N))
    bic[0] = 2 * cost0 + 1 * np.log(N)
    store[0] = ([], [pc[N] / N])
    # k=0 layer: cost of the single segment [0, a) for every legal end a
    prev = np.full(N + 1, np.inf)
    a_all = np.arange(1, N + 1)
    nn = a_all.astype(float); kk = pc[1:].astype(float)
    with np.errstate(divide="ignore", invalid="ignore"):
        t1 = np.where(kk > 0, kk * np.log(kk / nn), 0.0)
        t2 = np.where(kk < nn, (nn - kk) * np.log1p(-np.minimum(kk / nn, 1.0)), 0.0)
    span0 = coords - coords[0] + 1 >= DMIN                          # span of [0, a)
    prev[1:][span0] = -(t1 + t2)[span0]
    for k in range(1, kmax + 1):
        Vv, arg = _dp_layer(prev, pc, coords, cmax)
        if not np.isfinite(Vv[N]):
            break
        bic[k] = 2 * Vv[N] + (1 + 2 * k) * np.log(N)
        args[k] = arg
        j, cuts = N, []
        for m in range(k, 0, -1):                                   # per-layer backpointers
            a = int(args[m][j]); cuts.append(a); j = a
        cuts = sorted(cuts)
        segs = [0] + cuts + [N]
        rates = [(pc[segs[i + 1]] - pc[segs[i]]) / (segs[i + 1] - segs[i])
                 for i in range(k + 1)]
        store[k] = ([int(coords[c]) for c in cuts], rates)
        prev = Vv
    return {"N": int(N), "events": int(pc[N]),
            "dbic": {k: float(bic[0] - bic[k]) for k in bic if k >= 1},
            "bic": {k: float(v) for k, v in bic.items()},
            "fits": {k: {"bounds": b, "rates": [float(r) for r in rt]}
                     for k, (b, rt) in store.items()}}

def loc_clause(bounds, rates):
    """Registered P3: both changepoints within +-WIN of the fixed edges,
    middle segment rate below both outers."""
    if len(bounds) != 2 or len(rates) != 3:
        return False
    b = sorted(bounds)
    return (abs(b[0] - EDGES[0]) <= WIN and abs(b[1] - EDGES[1]) <= WIN
            and rates[1] < rates[0] and rates[1] < rates[2])

# --------------------------------------------------------------------- Lane A2

def _boot1(d):
    coords, _ = _BOOT["coords"], None
    N = _BOOT["N"]; p0 = _BOOT["p0"]
    ev = rng_for("boot", d).random(N) < p0
    f = dp_fit(coords, ev, 2)
    f2 = f["fits"].get(2) or {"bounds": [], "rates": []}
    return f["dbic"].get(2, 0.0), bool(loc_clause(f2["bounds"], f2["rates"]))

def a2_null(coords, ev, dbic_obs):
    ck_path = os.path.join(RES, "null_bootstrap_checkpoint.json")
    done, dbics, locs = [], [], []
    if os.path.exists(ck_path):
        ck = json.load(open(ck_path))
        done, dbics, locs = ck["done"], ck["dbic"], ck["loc"]
        print(f"[null] resuming at {len(done)} draws")
    global _BOOT
    _BOOT = {"coords": coords, "N": len(coords), "p0": ev.sum() / len(coords)}
    todo = [d for d in range(D_BOOT) if d not in set(done)]
    t0 = time.time()
    with Pool(min(28, os.cpu_count() or 4)) as pool:
        for i, (db, lc) in enumerate(pool.imap_unordered(_boot1, todo, chunksize=25)):
            done.append(todo[i]); dbics.append(float(db)); locs.append(bool(lc))
            if len(done) % 500 == 0:
                json.dump({"seed": SEED, "done": done, "dbic": dbics, "loc": locs},
                          open(ck_path, "w"))
                print(f"[null] {len(done)}/{D_BOOT} ({time.time()-t0:.0f}s)", flush=True)
    json.dump({"seed": SEED, "done": done, "dbic": dbics, "loc": locs}, open(ck_path, "w"))
    dbics = np.array(dbics); locs = np.array(locs)
    return {"D": len(done),
            "p_dbic": float((1 + np.sum(dbics >= dbic_obs)) / (len(done) + 1)),
            "p_loc": float((1 + np.sum(locs)) / (len(done) + 1)),
            "null_dbic_max": float(dbics.max()), "loc_hits": int(locs.sum())}

def a2_cv(coords, ev):
    """10-fold contiguous page-block CV; predictive LL on held-out pairs."""
    b = [0] + page_boundaries() + [12_956]
    pages = [(b[i] + 1, b[i + 1]) for i in range(len(b) - 1)]       # pair-coord blocks
    folds = [pages[i::10] for i in range(10)]
    out = {"M0": 0.0, "M2": 0.0}
    for hold in folds:
        mask = np.ones(12_955, dtype=bool)
        for a, c in hold:
            mask[a - 1:c - 1] = False                               # pair idx of coords a..c-1
        tr_c, tr_e = coords[mask], ev[mask]
        p0 = tr_e.mean()
        f2 = dp_fit(tr_c, tr_e, 2)
        fit2 = f2["fits"].get(2) or {"bounds": [], "rates": [p0, p0, p0]}
        bnds, rates = fit2["bounds"], fit2["rates"]
        bs = sorted(bnds) if len(bnds) == 2 else []
        te_c, te_e = coords[~mask], ev[~mask]
        eps = 1e-9
        r0 = min(max(float(p0), eps), 1 - eps)
        out["M0"] += float(te_e.sum() * np.log(r0) + (~te_e).sum() * np.log1p(-r0))
        if bs:
            seg = np.searchsorted(bs, te_c)                          # 0/1/2
            rr = np.array([max(min(x, 1 - eps), eps) for x in rates[:3]])
            pr = rr[seg]
            out["M2"] += float((te_e * np.log(pr) + (~te_e) * np.log1p(-pr)).sum())
        else:
            out["M2"] = -np.inf
    return out

def a2_hmm(coords, ev, iters=200):
    """Descriptive 2-state leak HMM by EM (rates free — PREREG disclosure)."""
    o = ev.astype(float)
    p = 0.01; a01 = a10 = 0.05; p_lo, p_hi = 0.002, 0.02
    N = len(o)
    for _ in range(iters):
        # forward-backward (2 states), scaled
        B = np.stack([np.where(o == 1, q, 1 - q) for q in (p_lo, p_hi)])   # 2 x N
        A = np.array([[1 - a01, a01], [a10, 1 - a10]])
        al = np.zeros((2, N)); sc = np.zeros(N); al[:, 0] = [1 - p, p] * B[:, 0]
        sc[0] = al[:, 0].sum(); al[:, 0] /= sc[0]
        for t in range(1, N):
            for s in range(2):
                al[s, t] = (al[0, t-1]*A[0, s] + al[1, t-1]*A[1, s]) * B[s, t]
            sc[t] = al[:, t].sum(); al[:, t] /= max(sc[t], 1e-300)
        be = np.zeros((2, N)); be[:, N-1] = 1.0
        for t in range(N - 2, -1, -1):
            for s in range(2):
                be[s, t] = be[s, t+1] * (A[s, 0]*B[0, t+1] + A[s, 1]*B[1, t+1])
            be[:, t] /= max(sc[t+1], 1e-300)
        g = al * be
        gsum = g.sum(0) + 1e-300; g /= gsum
        tr = np.zeros((2, 2))
        for s in range(2):
            for s2 in range(2):
                tr[s, s2] = np.sum(al[s, :N-1] * A[s, s2] * B[s2, 1:] * be[s2, 1:] / sc[1:])
        tr /= tr.sum(1, keepdims=True) + 1e-300
        p = float(g[1, 0]); a01, a10 = float(tr[0, 1]), float(tr[1, 0])
        p_lo = float((g[0] * o).sum() / g[0].sum()); p_hi = float((g[1] * o).sum() / g[1].sum())
        ll = float(np.log(sc).sum())
    bic = -2 * ll + 5 * np.log(N)
    return {"ll": ll, "p_lo": p_lo, "p_hi": p_hi, "a01": a01, "a10": a10,
            "pi": p, "bic": bic}

def _plant1(args):
    w_i, d = args
    coords, N, p0 = _BOOT["coords"], _BOOT["N"], _BOOT["p0"]
    w = _BOOT["plants"][w_i]
    ev = rng_for(f"plant{w_i}", d).random(N) < p0
    lo, hi = w - EDGES[0], w - EDGES[0] + 1648                      # same length as void
    ev[lo:hi + 1] &= rng_for(f"thin{w_i}", d).random(hi - lo + 1) < 0.5
    f = dp_fit(coords, ev, 2)
    f2 = f["fits"].get(2) or {"bounds": [], "rates": []}
    return w_i, f["dbic"].get(2, 0.0), bool(loc_clause(f2["bounds"], f2["rates"]))

def a2_power(coords):
    rng = np.random.default_rng([SEED, zlib.crc32(b"plantpos") % 100000, 0])
    plants = sorted(int(x) for x in rng.choice(np.arange(300, 11_000, 800), NPLANT, replace=False))
    global _BOOT
    _BOOT = {"coords": coords, "N": len(coords), "p0": 86 / len(coords), "plants": plants}
    with Pool(min(28, os.cpu_count() or 4)) as pool:
        res = pool.map(_plant1, [(i, d) for i in range(NPLANT) for d in range(D_PLANT)])
    det = {}
    for w_i, db, lc in res:
        det.setdefault(w_i, []).append(db > 10 and lc)
    per = {plants[i]: float(np.mean(v)) for i, v in det.items()}
    return {"plants": plants, "detect_rate": per,
            "positions_pass_8of10": int(sum(v >= 0.8 for v in per.values())),
            "n_positions": NPLANT}

def a2():
    os.makedirs(RES, exist_ok=True)
    gates()
    coords, ev = leak_stream()
    f = dp_fit(coords, ev, 4)
    print(json.dumps({k: f[k] for k in ("dbic", "fits")}, indent=1))
    obs_dbic2 = f["dbic"].get(2, 0.0)
    fit2 = f["fits"].get(2) or {"bounds": [], "rates": []}
    p3 = loc_clause(fit2["bounds"], fit2["rates"])
    null = a2_null(coords, ev, obs_dbic2)
    cv = a2_cv(coords, ev)
    hmm = a2_hmm(coords, ev)
    pw = a2_power(coords)
    P1, P2 = obs_dbic2 > 10, null["p_dbic"] < 0.05
    csign = cv["M2"] > cv["M0"]
    verdict = "QUALIFIES" if (P1 and P2 and p3 and csign) else "NULL-RETIRE"
    out = {"seed": SEED, "obs": {"dbic_k": f["dbic"], "bic_k": f["bic"],
                                 "fits": f["fits"], "P1_dBIC2_gt10": P1,
                                 "P3_location": p3},
           "null": null, "P2_p_lt_005": P2, "cv": cv, "cv_sign_ok": bool(csign),
           "hmm_descriptive": hmm, "power": pw, "VERDICT": verdict,
           "stopping_rule": "P1&P2&P3&CVsign else retire changepoint lane (PREREG)"}
    json.dump(out, open(os.path.join(RES, "a2_fit.json"), "w"), indent=1)
    print("VERDICT:", verdict)

# --------------------------------------------------------------------- Lane A1

def load_quad(path):
    ctx = {}
    for ln in open(path, encoding="utf-8"):
        q, c = ln.split()
        ctx.setdefault(q[:3], [[], []])
        ctx[q[:3]][0].append(q[3]); ctx[q[:3]][1].append(int(c))
    out = {}
    for k, (chs, ws) in ctx.items():
        cw = np.cumsum(ws); out[k] = (chs, cw / cw[-1])
    return out

def a1():
    """Flat-key idiom equivalence: key-skip vs plaintext-redraw emissions."""
    Q = load_quad(os.path.join(ROOT, "sources/dukotah/liber-primus/data/english_quadgrams.txt"))
    AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    L = 12_956
    def sampler(rng, n):
        st = "THE"; out = []
        for _ in range(n):
            e = Q.get(st)
            ch = AZ[rng.integers(26)] if e is None else e[0][int(np.searchsorted(e[1], rng.random()))]
            out.append(V.LATIN2IDX[ch]); st = st[1:] + ch
        return out
    def sim(seed, idiom):
        rng = np.random.default_rng([SEED, zlib.crc32(b"a1") % 100000, seed])
        pt = sampler(rng, L * 2)                                   # headroom for redraws
        keys = rng.integers(0, 29, L * 2)
        out, pi, ki, prev = [], 0, 0, -1
        while len(out) < L:
            p, k = pt[pi % len(pt)], int(keys[ki % len(keys)])
            c = (p + k) % 29
            while c == prev:                                        # filter rejects
                if idiom == "skip": ki += 1                         # key advances, P held
                else: pi += 1; p = pt[pi % len(pt)]                 # plaintext redrawn
                k = int(keys[ki % len(keys)]); c = (p + k) % 29
            out.append(c); prev = c; pi += 1; ki += 1
        return np.array(out, dtype=np.int8)
    def stats(s):
        d = (s[1:] - s[:-1]) % 29
        dc = np.bincount(d[1:], minlength=29)[1:29].astype(float)  # exclude the forced-nonzero first
        dc_chi2 = float(((dc - dc.sum()/28)**2 / (dc.sum()/28)).sum())
        x = s.astype(float); ac1 = float(np.corrcoef(x[:-1], x[1:])[0, 1])
        blocks = s[:len(s)//100*100].reshape(-1, 100)
        cnt = np.stack([np.bincount(b, minlength=29) for b in blocks]).astype(float)
        exp = cnt.sum(1, keepdims=True) / 29
        blk = float((((cnt - exp)**2 / np.maximum(exp, 1e-9)).sum(1)).mean())
        bg = (s[:-1].astype(int) * 29 + s[1:])
        hist = np.bincount(bg, minlength=29*29).reshape(29, 29).astype(float)
        np.fill_diagonal(hist, np.nan)
        tot = np.nansum(hist); dev = hist - tot / (29*28)
        big = float(np.nansum(dev**2 / (tot / (29*28))))
        return (dc_chi2, ac1, blk, big)
    N = 2000
    A = np.array([stats(sim(d, "skip")) for d in range(N)], dtype=float)
    B = np.array([stats(sim(d, "redraw")) for d in range(N)], dtype=float)
    names = ["dc_chi2", "sym_ac1", "block_chi2", "bigram_chi2"]
    res = {}
    from math import erfc, sqrt
    for i, nm in enumerate(names):
        a, b = np.sort(A[:, i]), np.sort(B[:, i])
        allv = np.concatenate([a, b]); ks = max(abs(np.searchsorted(a, allv, "right")
                                                   - np.searchsorted(b, allv, "right"))) / len(allv)
        # two-sided two-sample KS p ( asymptotic, n large )
        en = np.sqrt(len(a) * len(b) / (len(a) + len(b)))
        lam = (en + 0.12 + 0.11 / en) * ks
        p = 2 * sum((-1)**(j-1) * erfc(j * lam) for j in range(1, 60))
        t = (a.mean() - b.mean()) / sqrt(a.var()/len(a) + b.var()/len(b) + 1e-30)
        ptwo = erfc(abs(t) / sqrt(2))
        res[nm] = {"ks": float(ks), "p_ks": float(min(max(p, 0.0), 1.0)),
                   "t": float(t), "p_t": float(ptwo)}
    worst = max(min(r["p_ks"], r["p_t"]) for r in res.values())
    bonf = 8
    equiv = worst * bonf > 0.05                                    # no separation after Bonferroni
    out = {"N_per_idiom": N, "L": L, "per_stream_stats": res,
           "min_p": float(worst), "bonferroni_tests": bonf,
           "VERDICT": "MEMO-EQUIV" if equiv else "SEPARATES",
           "decision": ("key consumption NOT identifiable from corpus; adopt "
                        "skip-tolerant decoder class for power claims (I2 "
                        "with-skip 0.62-0.66)" if equiv else
                        "report separating statistic to owner BEFORE any scan")}
    os.makedirs(RES, exist_ok=True)
    json.dump(out, open(os.path.join(RES, "a1_equiv.json"), "w"), indent=1)
    print(json.dumps(out, indent=1))

if __name__ == "__main__":
    {"gates": gates, "a1": a1, "a2": a2}.get(sys.argv[1] if len(sys.argv) > 1 else "",
                                             gates)()
