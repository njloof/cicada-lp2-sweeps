#!/usr/bin/env python3
"""Campaign #27 — key-consumption discriminator scan (PREREG c0ec6ca, owner
approval 2026-11-19; escalation branch of #26-A1 SEPARATES).

Directional one-sided score test: do the 12,869 nonzero consecutive
differences of the unsolved stream contain an excess along the English
letter-difference direction (plaintext-redraw-with-held-key must inject
~2.9% of pairs from pi_E) or not (key-skip => EXACT uniform null)?

Run: python3 sweeps/2026-11-discriminator/scan.py   (seconds, local)
Verdict rules, gates, variants, power bar: exactly as registered.
"""
import itertools, json, os, subprocess, sys, zlib
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, ROOT)
from core import validate as V                                     # noqa: E402

RES = os.path.join(HERE, "results")
SEED = 20261227
NSYM = 29
PAGES = list(range(50)) + list(range(51, 56))
FLAG = 0.025                                                      # Bonferroni 2
D_BOOT, D_PLANT = 10_000, 20

def rng_for(tag, d): return np.random.default_rng([SEED, zlib.crc32(tag.encode()) % 100000, d])

# ------------------------------------------------------------------ pi_E streams

def lp1_plaintexts():
    """V1: solved-LP English, each section decoded with ITS OWN verified
    method (validate machinery), hold convention (interrupter F's kept —
    LEDGER C7). Returns list of per-section plaintext rune-index streams."""
    sc = open(V.SCREAM, encoding="utf-8").read()
    g = lambda s: V.scream_runes(s, sc)
    out = []
    out.append([(V.N - 1 - c) % V.N for c in g("Runes - 01.jpg")])                 # atbash
    both = g("03.jpg") + g("04.jpg")                                               # WELCOME join
    SK = {48, 74, 84, 132, 159, 160, 250, 421, 443, 465, 514}
    out.append(V.decode_holdnull(both, V.keyword_stream("DIVINITY", len(both)),
                                 [t in SK for t in range(len(both))]))
    out.append(g("05.jpg"))                                                        # identity
    out.append([(V.N - 1 - c + 3) % V.N for c in g("06.jpg")])                     # atbash+3
    out.append([(V.N - 1 - c + 3) % V.N for c in g("09.jpg")])                     # atbash+3
    for lab in ("10.jpg", "13.jpg", "16.jpg"):
        out.append(g(lab))                                                         # identity
    ci = g("14.jpg")                                                               # FIRFUMFERENFE hold
    res = V.brute_interrupters(ci, V.keyword_stream("FIRFUMFERENFE", len(ci)),
                               ["LESSON", "MASTER", "EXPLAINED", "STUDENT"])
    assert res and res[1] == 4 and res[2] == "hold", f"14.jpg decode failed: {res[:3]}"
    fpos = [t for t, c in enumerate(ci) if c == 0]
    for r in range(len(fpos) + 1):
        for combo in itertools.combinations(fpos, r):
            cs = set(combo)
            idx = V.decode_holdnull(ci, V.keyword_stream("FIRFUMFERENFE", len(ci)),
                                    [t in cs for t in range(len(ci))])
            if V.translit(idx) == res[0]:
                out.append(idx); break
        else:
            continue
        break
    return out

def load_quad(path):
    """Bit-identical to #26 A1 load_quad (file order, NO sorting)."""
    ctx = {}
    for ln in open(path, encoding="utf-8"):
        q, c = ln.split()
        ctx.setdefault(q[:3], [[], []])
        ctx[q[:3]][0].append(q[3]); ctx[q[:3]][1].append(int(c))
    out = {}
    for k, (chs, ws) in ctx.items():
        cw = np.cumsum(ws); out[k] = (chs, cw / cw[-1])
    return out

QUAD = lambda: load_quad(os.path.join(ROOT, "sources/dukotah/liber-primus/data/"
                                            "english_quadgrams.txt"))

def sampler(Q, rng, n):
    """Bit-identical to #26 A1 sampler."""
    AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    st = "THE"; out = []
    for _ in range(n):
        e = Q.get(st)
        ch = AZ[rng.integers(26)] if e is None else e[0][int(np.searchsorted(e[1], rng.random()))]
        out.append(V.LATIN2IDX[ch]); st = st[1:] + ch
    return out

def quadgram_stream(L):
    """V2: A1's stream 0 plaintext, bit-identical (same seed path + sampler)."""
    rng = np.random.default_rng([20261226, zlib.crc32(b"a1") % 100000, 0])  # A1 sim(0) rng
    return sampler(QUAD(), rng, L)

def diffdist(streams_or_stream, per_stream=True):
    """nonzero within-stream diff counts over 1..28 -> pi (normalized)."""
    streams = streams_or_stream if per_stream else [streams_or_stream]
    cnt = np.zeros(NSYM)
    for s in streams:
        d = (np.asarray(s[1:]) - np.asarray(s[:-1])) % NSYM
        d = d[d != 0]
        cnt += np.bincount(d, minlength=NSYM)
    return cnt / cnt.sum(), int(cnt.sum())

# ------------------------------------------------------------------ statistic

def score(counts, pi):
    N = counts.sum()
    u = np.full(28, 1.0 / 28)
    w = pi[1:29] - u
    T = float(((counts[1:29] - N * u) * w / u).sum())
    # Var(T) under multinomial-uniform null = N*sum(w^2/u) (the covariance term
    # collapses because sum(w)=0); the PREREG's sqrt(N*sum(u*w^2)) dropped it —
    # 28x too small. Corrected pre-verdict, addendum 2026-11-19; bootstrap
    # (registered exact-null calibration) agrees with this sd.
    sd = float(np.sqrt(N * (w * w / u).sum()))
    from math import erfc, sqrt
    Z = T / sd
    p = 0.5 * erfc(Z / sqrt(2))
    alpha = T / (N * (w * w / u).sum())
    alpha_sd = 1.0 / np.sqrt(N * (w * w / u).sum())
    return Z, p, alpha, alpha_sd, T

# ------------------------------------------------------------------ gates

def gates():
    ok = True
    r = subprocess.run([sys.executable, "-m", "core.validate"], cwd=ROOT,
                       capture_output=True, text=True)
    g1 = r.returncode == 0
    print(f"G1 validate.py: {'PASS' if g1 else 'FAIL'}")
    ok &= g1
    s = np.array([x for p in PAGES for x in V.flat(p)], dtype=np.int8)
    d = (s[1:].astype(int) - s[:-1].astype(int)) % NSYM
    nz = int((d != 0).sum())
    g2 = (len(s) == 12_956) and int((d == 0).sum()) == 86 and nz == 12_869
    print(f"G2 corpus: L={len(s)} zeros={int((d==0).sum())} nonzero={nz}: "
          f"{'PASS' if g2 else 'FAIL'}")
    ok &= g2
    v1 = lp1_plaintexts()
    n1 = sum(len(x) for x in v1)
    q = quadgram_stream(50)
    g3 = (n1 == 2798) and len(q) == 50
    print(f"G3 pi_E: V1 runes={n1} (want 2798), V2 sampler head OK={len(q)==50}: "
          f"{'PASS' if g3 else 'FAIL'}")
    ok &= g3
    if not ok:
        raise SystemExit("GATES FAILED — no statistic may be touched.")
    return s, v1

# ------------------------------------------------------------------ plants

def plant_redraw(d, Q):
    """A1 redraw-idiom emission stream (key held across rejects), A1 loop
    semantics, #27 house seeding."""
    rng = rng_for("plant", d)
    L = 12_956
    pt = sampler(Q, rng, L * 2)
    keys = rng.integers(0, 29, L * 2)
    out, pi_, ki, prev = [], 0, 0, -1
    while len(out) < L:
        p, k = pt[pi_ % len(pt)], int(keys[ki % len(keys)])
        c = (p + k) % 29
        while c == prev:
            pi_ += 1; p = pt[pi_ % len(pt)]
            k = int(keys[ki % len(keys)]); c = (p + k) % 29
        out.append(c); prev = c; pi_ += 1; ki += 1
    return np.array(out, dtype=np.int8)

# ------------------------------------------------------------------ main

def main():
    os.makedirs(RES, exist_ok=True)
    s, v1_streams = gates()
    d = (s[1:].astype(int) - s[:-1].astype(int)) % NSYM
    counts = np.bincount(d[d != 0], minlength=NSYM).astype(float)

    pi1, m1 = diffdist(v1_streams, per_stream=True)
    pi2, m2 = diffdist([quadgram_stream(12_956)], per_stream=True)

    out = {"seed": SEED, "variants": {}}
    for name, pi in (("V1_solvedLP", pi1), ("V2_quadgram", pi2)):
        Z, p, a, a_sd, T = score(counts, pi)
        # bootstrap consistency check (registered as descriptive)
        N = int(counts.sum())
        Ts = []
        for i in range(D_BOOT):
            b = rng_for("boot", i).multinomial(N, np.full(28, 1/28.0))
            c2 = np.zeros(NSYM); c2[1:29] = b
            Ts.append(score(c2, pi)[4])
        p_boot = (1 + sum(t >= T for t in Ts)) / (D_BOOT + 1)
        out["variants"][name] = {"Z": Z, "p_normal": p, "p_bootstrap": p_boot,
                                 "alpha_hat": a, "alpha_sd": a_sd,
                                 "piE_diffs_used": int(m1 if name.startswith("V1") else m2)}
        print(f"{name}: Z={Z:+.2f} p={p:.4g} p_boot={p_boot:.4g} "
              f"alpha_hat={a:+.4f}+-{a_sd:.4f}")

    # power: 20 redraw plants per variant, bar 19/20
    power = {}
    QP = QUAD()
    for name, pi in (("V1_solvedLP", pi1), ("V2_quadgram", pi2)):
        hits = 0
        for i in range(D_PLANT):
            st = plant_redraw(i, QP)
            dd = (st[1:].astype(int) - st[:-1].astype(int)) % NSYM
            cc = np.bincount(dd[dd != 0], minlength=NSYM).astype(float)
            _, p, *_ = score(cc, pi)
            hits += p < FLAG
        power[name] = {"detected": hits, "draws": D_PLANT, "bar": 19,
                       "pass": hits >= 19}
        print(f"power {name}: {hits}/{D_PLANT} (bar 19)")
    out["power"] = power

    sig = [n for n, v in out["variants"].items() if v["p_normal"] < FLAG]
    allpass = all(v["pass"] for v in power.values())
    if sig:
        verdict = "REDRAW-EXCESS"
    elif allpass:
        verdict = "NO-EXCESS"
    else:
        verdict = "UNINFORMATIVE"
    out["VERDICT"] = verdict
    out["flag_alpha"] = FLAG
    json.dump(out, open(os.path.join(RES, "discriminator.json"), "w"), indent=1)
    print("VERDICT:", verdict)

if __name__ == "__main__":
    main()
