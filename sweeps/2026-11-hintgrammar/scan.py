#!/usr/bin/env python3
"""Campaign #29 — Track C hint-grammar scan (PREREG b8c779a + addenda 1-3).

    python3 scan.py --gates      # G1 validate / G2 phi(p56) / G3 letter map
    python3 scan.py --plants     # synthetic power plants FIRST (no corpus)
    python3 scan.py --scan       # real-corpus grid maxima (studio, Pool 28)
    python3 scan.py --nulls      # family-matched MC surrogates (studio)
    python3 scan.py --verdict    # bars, gates, adjudication, verdicts

Cells: K1 plaintext-autokey (engine29.c; per-w verdicts; keyskip0 emission,
L9), K2 ciphertext-autokey (keyskip1 + causality leak), K3 running keys from
pinned hints, K4 math streams. Statistic = #28 skip-tolerant head LL
(addendum 3); flag bar B = plant_min - 2.0; CLOSED iff no candidate >= B and
20/20 plants >= null_max + 2.0; adjudication = full beam decode +
letter-space crib hits (>=2 distinct on one page -> oracle, never auto).
"""
import json, os, subprocess, sys, time
import numpy as np
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
import grammar as G                                               # noqa: E402

ENG = os.path.join(HERE, "engine29")
RES = os.path.join(HERE, "results")
WORK = os.path.join(HERE, "work")
NPLANT = 20
SCAN_HINTS = ["armfwd", "armrev", "scream", "anend", "parable"]
STREAMS = ["primes", "fib", "phi", "ratio", "pi", "e", "sqrt2", "p56hex"]
NEG = -1e31

# parent-side, built once, inherited by fork
HINTS = G.load_hints()
K4S = G.k4_streams()
EMERSON = G.text_vals(open(os.path.join(G.ARMADA, "emerson_essays_first_series.txt")).read())
SQRT3 = G.sqrt3_stream(2000)

def _run_k1(corp, tag, names=SCAN_HINTS, wmin=2, wmax=24, hintfile=None, lens=None):
    os.makedirs(WORK, exist_ok=True)
    cp = os.path.join(WORK, f"corp_{tag}.bin"); open(cp, "wb").write(corp)
    if hintfile is None:
        hintfile = os.path.join(WORK, f"hints_{tag}.bin")
        lens = ",".join(str(len(HINTS[h])) for h in names)
        open(hintfile, "wb").write(b"".join(bytes(HINTS[h]) for h in names))
    r = subprocess.run([ENG, "--k1", cp, G.QUAD, hintfile, lens, str(wmin), str(wmax)],
                       capture_output=True, text=True)
    if r.returncode: raise RuntimeError("engine29: " + r.stderr[:200])
    top, perw = [], {}
    for ln in r.stdout.splitlines():
        a = ln.split()
        if a[0] == "B": perw[int(a[1])] = [float(a[2]), int(a[3]), int(a[4]), int(a[5]), int(a[6])]
        else: top.append([float(a[0]), int(a[1]), int(a[2]), int(a[3]), int(a[4])])
    top.sort(reverse=True)
    return top, perw

# ---------------------------------------------------------------- gates
def gates():
    ok = True
    r = subprocess.run([sys.executable, "-m", "core.validate"], capture_output=True, text=True, cwd=ROOT)
    g1 = r.returncode == 0
    print(("PASS" if g1 else "FAIL"), "G1 core.validate")
    ok &= g1
    ae = G.V.flat(56)
    res = G.V.brute_interrupters(ae, G.V.phi_prime_stream(len(ae)), ["DEEPWEB", "PILGRIM", "HASHESTO"])
    g2 = bool(res) and res[1] == 3 and "phi" in K4S
    print(("PASS" if g2 else "FAIL"), f"G2 phi(prime) recovers p56 blind: {res[2] if res else None}")
    ok &= g2
    g3 = all(G.TRANS[G.V.LATIN2IDX[ch]][0] == G.COLLAPSE.get(ch, ch)
             for ch in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" if ch in G.V.LATIN2IDX)
    print(("PASS" if g3 else "FAIL"), "G3 letter-map round-trip (collapses V->U,K->C,Q->C,Z->S)")
    ok &= g3
    print("GATES:", "PASS" if ok else "FAIL")
    return 0 if ok else 1

# ---------------------------------------------------------------- plants (synthetic only)
def plants():
    os.makedirs(RES, exist_ok=True); os.makedirs(WORK, exist_ok=True)
    Q = G.load_quad()
    out = {"seed": G.SEED, "n_plants": NPLANT,
           "note": "K1 seeds = Emerson substrings (held-out hint); K3 key = Emerson; K4 stream = sqrt3 (held-out)"}
    t0 = time.time()
    # ---- K1: 20 per lag w (per-w gate, addendum 3)
    perw = {}
    for w in range(2, 25):
        rows = []
        for d in range(NPLANT):
            rng = G.rng_for(f"plant-K1-w{w}", d)
            off = int(rng.integers(0, len(EMERSON) - w + 1))
            sign = 1 if rng.random() < 0.5 else -1
            rows.append((EMERSON[off:off + w], sign))
        hp = os.path.join(WORK, f"pseed_{w}.bin")
        open(hp, "wb").write(b"".join(bytes(s) for s, _ in rows))
        lens = ",".join([str(w)] * NPLANT)
        scores = []
        for d, (seed, sign) in enumerate(rows):
            rng = G.rng_for(f"plant-K1-w{w}", d)
            _ = int(rng.integers(0, len(EMERSON) - w + 1)); _ = 1 if rng.random() < 0.5 else -1
            P = G.sampler(Q, rng, 400)
            c = G.encode_k1(P, seed, sign, 200)
            top, _ = _run_k1(c, f"p{w}_{d}", hintfile=hp, lens=lens, wmin=w, wmax=w)
            scores.append(max((x[0] for x in top if x[1] == d and x[4] == sign), default=NEG))
        perw[str(w)] = [round(x, 4) for x in scores]
        print(f"K1 w={w:2d}: min={min(scores):.1f} med={sorted(scores)[10]:.1f}", flush=True)
    out["K1"] = perw
    # ---- K2
    sc = []
    for d in range(NPLANT):
        rng = G.rng_for("plant-K2", d)
        w = int(rng.integers(2, 65)); sign = 1 if rng.random() < 0.5 else -1; fs = int(rng.random() < 0.5)
        P = G.sampler(Q, rng, 400)
        c = G.encode_k2(P, w, sign, 200, fs)
        ks = c if not fs else bytes(v for v in c if v)
        sc.append(G.screen(ks, c[w:w + 120], sign, cap=min(12, w - 1)))
    out["K2"] = [round(x, 4) for x in sc]; print(f"K2: min={min(sc):.1f} med={sorted(sc)[10]:.1f}", flush=True)
    # ---- K3 (Emerson = held-out hint)
    sc = []
    for d in range(NPLANT):
        rng = G.rng_for("plant-K3", d)
        t0i = int(rng.integers(0, len(EMERSON) - 200 + 1))
        a1 = int(rng.random() < 0.5); rev = int(rng.random() < 0.5); fs = int(rng.random() < 0.5)
        sign = 1 if rng.random() < 0.5 else -1
        k = G.hint_variants(EMERSON, a1, rev, fs)
        P = G.sampler(Q, rng, 400)
        c = G.encode_keyskip1(P, k[t0i:], sign, 200)
        sc.append(G.screen(bytes(k[t0i:t0i + 140]), c[:120], sign))
    out["K3"] = [round(x, 4) for x in sc]; print(f"K3: min={min(sc):.1f} med={sorted(sc)[10]:.1f}", flush=True)
    # ---- K4 (sqrt3 = held-out stream)
    sc = []
    for d in range(NPLANT):
        rng = G.rng_for("plant-K4", d)
        off = int(rng.integers(0, 1000)); fs = int(rng.random() < 0.5)
        sign = 1 if rng.random() < 0.5 else -1
        k = SQRT3 if not fs else [v for v in SQRT3 if v]
        P = G.sampler(Q, rng, 400)
        c = G.encode_keyskip1(P, k[off:], sign, 200)
        sc.append(G.screen(bytes(k[off:off + 140]), c[:120], sign))
    out["K4"] = [round(x, 4) for x in sc]; print(f"K4: min={min(sc):.1f} med={sorted(sc)[10]:.1f}", flush=True)
    out["seconds"] = round(time.time() - t0, 1)
    json.dump(out, open(os.path.join(RES, "plants.json"), "w"), indent=1)
    print("plants.json written")
    return 0

# ---------------------------------------------------------------- grids
def _k2_task(corp):
    best = (NEG, None)
    ksf = bytes(v for v in corp if v)
    for w in range(2, 65):
        for sign in (1, -1):
            for fs in (0, 1):
                ks = corp if not fs else ksf
                s = G.screen(ks, corp[w:w + 120], sign, cap=min(12, w - 1))
                if s > best[0]: best = (s, ["K2", w, sign, fs])
    return best

def _k3_combo(corp, combo, hintvals):
    h, a1, rev, fs = combo
    k = G.hint_variants(hintvals, a1, rev, fs)
    n = len(k)
    if n < 132: return (NEG, None)          # head(120)+cap(12) key values needed (L11)
    kb = bytes(k); hi = n - 200
    cwin = corp[:120]
    best = (NEG, None)
    for t0 in range(hi + 1):
        ks = kb[t0:t0 + 140]
        for sign in (1, -1):
            s = G.screen(ks, cwin, sign)
            if s > best[0]: best = (s, [h, a1, rev, fs, t0, sign])
    return best

def _k3_task(arg):
    corp, combo = arg
    return _k3_combo(corp, combo, HINTS[combo[0]])

def _k4_task(arg):
    corp, sname, fs = arg
    k = K4S[sname]
    if fs: k = [v for v in k if v]
    n = len(k)
    if n < 132: return (NEG, None)
    kb = bytes(k)
    hi = min(999, n - 140)
    cwin = corp[:120]
    best = (NEG, None)
    for off in range(hi + 1):
        ks = kb[off:off + 140]
        for sign in (1, -1):
            s = G.screen(ks, cwin, sign)
            if s > best[0]: best = (s, [sname, fs, off, sign])
    return best

def _k3_combos():
    return [(h, a1, rev, fs) for h in SCAN_HINTS for a1 in (0, 1) for rev in (0, 1) for fs in (0, 1)]

def _grid_max(corp, cells=("K2", "K3", "K4"), pool=None):
    r = {}
    if "K2" in cells: r["K2"] = _k2_task(corp)
    if "K3" in cells: r["K3"] = max(pool.map(_k3_task, [(corp, c) for c in _k3_combos()]))
    if "K4" in cells: r["K4"] = max(pool.map(_k4_task, [(corp, s, fs) for s in STREAMS for fs in (0, 1)]))
    return r

def scan():
    os.makedirs(RES, exist_ok=True)
    corp = G.corpus()
    t0 = time.time()
    out = {"corpus_len": len(corp), "hint_lens": {k: len(v) for k, v in HINTS.items()},
           "k4_lens": {k: len(v) for k, v in K4S.items()}}
    with Pool(28) as pool:
        m = _grid_max(corp, pool=pool)
    k1top, k1perw = _run_k1(corp, "real")
    for cell in ("K2", "K3", "K4"):
        out[cell] = {"max": round(m[cell][0], 4), "arg": m[cell][1]}
    out["K1"] = {"max": round(k1top[0][0], 4) if k1top else None,
                 "top": k1top[:16], "perw": {str(k): v for k, v in k1perw.items()}}
    out["seconds"] = round(time.time() - t0, 1)
    json.dump(out, open(os.path.join(RES, "scan.json"), "w"), indent=1)
    print(json.dumps({k: (v["max"] if isinstance(v, dict) else v) for k, v in out.items() if k in ("K1", "K2", "K3", "K4")}))
    return 0

# ---------------------------------------------------------------- nulls
def _null_task(arg):
    cell, d = arg
    corp = G.corpus()
    if cell in ("K1", "K2", "K4"):
        rng = G.rng_for(f"null-{cell}", d)
        corp = G.surrogate_corpus(rng.permutation(len(G.PAGE_RUNES)))
    if cell == "K2":
        return _k2_task(corp)[0]
    if cell == "K4":
        return max(_k4_task((corp, s, fs))[0] for s in STREAMS for fs in (0, 1))
    if cell == "K1":
        top, _ = _run_k1(corp, f"n{d}")
        return top[0][0] if top else NEG
    if cell == "K3":
        rng = G.rng_for("null-K3", d)
        perm = {h: [int(x) for x in rng.permutation(HINTS[h])] for h in SCAN_HINTS}
        return max(_k3_combo(corp, c, perm[c[0]])[0] for c in _k3_combos())
    raise ValueError(cell)

def nulls():
    """Draw-level resume (studio ssh doctrine): progress checkpointed per draw
    batch into results/null_partial.json; completed draws are skipped."""
    os.makedirs(RES, exist_ok=True)
    PP = os.path.join(RES, "null_partial.json")
    try:
        prog = json.load(open(PP))
    except Exception:
        prog = {}
    D = {"K1": 20, "K2": 200, "K3": 200, "K4": 200}
    try:
        k1obs = json.load(open(os.path.join(RES, "scan.json")))["K1"]["max"]
    except Exception:
        k1obs = None
    out = {}
    with Pool(28) as pool:
        for cell in ("K1", "K2", "K3", "K4"):
            t0 = time.time()
            done = prog.setdefault(cell, {})
            todo = [d for d in range(D[cell]) if str(d) not in done]
            for i in range(0, len(todo), 28):
                batch = todo[i:i + 28]
                for d, sc in zip(batch, pool.map(_null_task, [(cell, d) for d in batch])):
                    done[str(d)] = round(sc, 4)
                json.dump(prog, open(PP, "w"))
                print(f"{cell}: {len(done)}/{D[cell]}", flush=True)
            rows = [done[str(d)] for d in range(D[cell])]
            esc = 0
            if cell == "K1" and k1obs is not None and k1obs >= float(np.median(rows)):
                print("K1 escalation: observed >= null median -> +30 draws", flush=True)
                extra = pool.map(_null_task, [(cell, 1000 + d) for d in range(30)])
                rows += extra
                esc = 30
            out[cell] = {"D": len(rows), "null_max": round(max(rows), 4),
                         "median": round(float(np.median(rows)), 4),
                         "draws": rows, "escalated": esc,
                         "seconds": round(time.time() - t0, 1)}
            print(cell, out[cell]["null_max"], f"({out[cell]['seconds']}s)", flush=True)
            json.dump(out, open(os.path.join(RES, "nulls.json"), "w"), indent=1)
    return 0

# ---------------------------------------------------------------- verdict
def _adjudicate(cell, arg, corp):
    """Full-length skip-tolerant decode + per-page letter-space crib hits."""
    if cell == "K1":
        _, h, off, w, sign = arg
        sp = os.path.join(WORK, "adj_seed.bin"); open(sp, "wb").write(bytes(HINTS[SCAN_HINTS[h]][off:off + w]))
        cp = os.path.join(WORK, "adj_corp.bin"); open(cp, "wb").write(corp)
        vp = os.path.join(WORK, "adj_vals.bin")
        subprocess.run([ENG, "--k1decode", cp, G.QUAD, sp, str(w), str(sign), vp],
                       capture_output=True)
        vals = list(open(vp, "rb").read())
        return G.crib_stat(vals, r0=w)
    if cell == "K2":
        _, w, sign, fs = arg
        ks = corp if not fs else bytes(v for v in corp if v)
        vals = G.beam_decode(ks, corp[w:], sign)
        return G.crib_stat(vals, r0=w)
    if cell in ("K3", "K4"):
        if cell == "K3":
            h, a1, rev, fs, t0, sign = arg
            k = G.hint_variants(HINTS[h], a1, rev, fs)
            ks = bytes(k[t0:])
        else:
            sname, fs, off, sign = arg
            k = K4S[sname]
            if fs: k = [v for v in k if v]
            ks = bytes(k[off:])
        vals = G.beam_decode(ks, corp, sign)
        return G.crib_stat(vals, r0=0)

def verdict():
    os.makedirs(RES, exist_ok=True)
    pl = json.load(open(os.path.join(RES, "plants.json")))
    sc = json.load(open(os.path.join(RES, "scan.json")))
    nl = json.load(open(os.path.join(RES, "nulls.json")))
    corp = G.corpus()
    out = {"rules": "B=plant_min-2.0; CLOSED iff no cand>=B and 20/20 plants>=null_max+2.0"}
    adj = {}
    for cell in ("K2", "K3", "K4"):
        pmin = min(pl[cell]); B = pmin - 2.0
        obs = sc[cell]["max"]; nm = nl[cell]["null_max"]
        flag = obs >= B
        gate = pmin >= nm + 2.0
        v = "FLAGGED" if flag else ("CLOSED-NO-GRAMMAR" if gate else "UNPOWERED-NULL")
        out[cell] = {"plant_min": round(pmin, 2), "B": round(B, 2), "obs_max": obs,
                     "null_max": nm, "plant_gate": gate, "verdict": v}
        if flag: adj[cell] = _adjudicate(cell, tuple(sc[cell]["arg"]), corp)
    kw = {}
    allclosed = True; flagged = []
    for w in range(2, 25):
        pmin = min(pl["K1"][str(w)]); B = pmin - 2.0
        e = sc["K1"]["perw"].get(str(w))
        obs = e[0] if e else None
        nm = nl["K1"]["null_max"]          # conservative: global null max applied per-w
        gate = pmin >= nm + 2.0
        v = "FLAGGED" if (obs is not None and obs >= B) else ("CLOSED-NO-GRAMMAR" if gate else "UNPOWERED-NULL")
        kw[str(w)] = {"plant_min": round(pmin, 2), "B": round(B, 2), "obs": obs, "verdict": v}
        if v == "FLAGGED": flagged.append(w)
        if v != "CLOSED-NO-GRAMMAR": allclosed = False
    out["K1"] = {"null_max": nl["K1"]["null_max"], "perw": kw,
                 "verdict": "CLOSED-NO-GRAMMAR" if allclosed else
                 ("FLAGGED" if flagged else "UNPOWERED-NULL (per-w coverage in perw)")}
    for w in flagged:
        e = sc["K1"]["perw"][str(w)]
        adj[f"K1@{w}"] = _adjudicate("K1", (0, e[1], e[2], e[3], e[4]), corp)
    json.dump(out, open(os.path.join(RES, "verdict.json"), "w"), indent=1)
    json.dump({k: {"crib_total": t, "pages": [[int(p) if isinstance(p, (int, float)) else p, h] for p, h in pg]}
               for k, (t, pg) in adj.items()},
              open(os.path.join(RES, "adjudication.json"), "w"), indent=1)
    print(json.dumps(out, indent=1))
    return 0

if __name__ == "__main__":
    a = sys.argv[1] if len(sys.argv) > 1 else ""
    sys.exit({"--gates": gates, "--plants": plants, "--scan": scan,
              "--nulls": nulls, "--verdict": verdict}.get(a, lambda: 1)())
