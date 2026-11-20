#!/usr/bin/env python3
"""Campaign #29 shared machinery — hint-grammar generators (PREREG + addenda).

Letter map = core.validate.LATIN2IDX (G3 gate). Scoring relaxation = #28
engine semantics EXACTLY (13 extra-states, each carrying its own best score
+ letter context; key advance 1..3 per rune; 3.0 nats per extra consumption;
initial context THE; quadgram log-probs with unigram fallback) — registered
in addendum 3. K1 (plaintext-autokey) runs in engine29.c (per-state plaintext
history — path-dependent key); K2/K3/K4 use the known-key-array screen here.
"""
import os, sys, zlib
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "sweeps/2026-11-tail"))
from core import validate as V                                    # noqa: E402
from core.cribs import REPR                                       # noqa: E402

SEED = 20261229
N = 29
L_CORP = 12_956
HEAD = 120            # scored head runes (window start = lag w for K1/K2)
NKS_HEAD = 140        # key values needed for head (119 + 12 + 1)
PEN = 3.0
MAXEXTRA = 12
QUAD = os.path.join(ROOT, "sources/dukotah/liber-primus/data/english_quadgrams.txt")
ARMADA = os.path.join(ROOT, "sources/dukotah/liber-primus/data/keys/armada18")
TRANS = V.TRANS
CTX_THE = (19 * 26 + 7) * 26 + 4
COLLAPSE = {"K": "C", "Q": "C", "V": "U", "Z": "S"}
PAGES = list(range(50)) + list(range(51, 56))

def rng_for(tag, d): return np.random.default_rng([SEED, zlib.crc32(tag.encode()) % 100000, d])

# ---------------------------------------------------------------- quadgram ll (engine load_quad mirror)
def build_ll(path=QUAD):
    wch = {}; csum = {}; tot = [0.0] * 26; T = 0.0
    for ln in open(path, encoding="utf-8"):
        q, c = ln.split(); n = int(c)
        a, b, d, e = (ord(x) - 65 for x in q)
        if min(a, b, d, e) < 0 or max(a, b, d, e) > 25: continue
        ctx = (a * 26 + b) * 26 + d
        wch[ctx * 26 + e] = wch.get(ctx * 26 + e, 0.0) + n
        csum[ctx] = csum.get(ctx, 0.0) + n
        tot[e] += n; T += n
    import math
    uni = [math.log(x / T) if x > 0 else math.log(1e-12) for x in tot]
    ll = [0.0] * (17576 * 26)
    for ctx in range(17576):
        s = csum.get(ctx, 0.0)
        base = ctx * 26
        for e in range(26):
            w = wch.get(base + e, 0.0)
            ll[base + e] = math.log(w / s) if (s > 0 and w > 0) else uni[e]
    return ll

LL = None  # built at import (workers inherit via fork)
LL = build_ll()

# ---------------------------------------------------------------- corpus
def corpus():
    s = bytes(x for p in PAGES for x in V.flat(p))
    assert len(s) == L_CORP
    return s

PAGE_RUNES = [len(V.flat(p)) for p in PAGES]

def surrogate_corpus(pages_perm):
    return bytes(x for p in pages_perm for x in V.flat(p))

# ---------------------------------------------------------------- screen (K2/K3/K4: known key array)
def screen(ks, cwin, sign, cap=MAXEXTRA):
    """#28 engine screen() semantics on a KNOWN key array. Returns best LL (nats)."""
    NEG = -1e30
    nks = len(ks); Lw = len(cwin)
    ds = [NEG] * (cap + 1); cs = [0] * (cap + 1)
    ds[0] = 0.0; cs[0] = CTX_THE
    ll = LL; tr = TRANS
    for t in range(Lw):
        ct = cwin[t]
        nds = [NEG] * (cap + 1); ncs = [0] * (cap + 1)
        any_live = False
        for e in range(cap + 1):
            s0 = ds[e]
            if s0 == NEG: continue
            kpos = t + e
            if kpos >= nks: continue
            p = (ct - sign * ks[kpos]) % N
            ctx = cs[e]
            lt = tr[p]
            s = s0
            o = ord(lt[0]) - 65
            s += ll[ctx * 26 + o]; ctx = (ctx % 676) * 26 + o
            if len(lt) > 1:
                o = ord(lt[1]) - 65
                s += ll[ctx * 26 + o]; ctx = (ctx % 676) * 26 + o
            if s > nds[e]: nds[e] = s; ncs[e] = ctx
            if e + 1 <= cap:
                s1 = s - PEN
                if s1 > nds[e + 1]: nds[e + 1] = s1; ncs[e + 1] = ctx
                if e + 2 <= cap:
                    s2 = s - 2 * PEN
                    if s2 > nds[e + 2]: nds[e + 2] = s2; ncs[e + 2] = ctx
            any_live = True
        if not any_live: return NEG
        ds, cs = nds, ncs
    return max(ds)

# ---------------------------------------------------------------- beam adjudication (known key array)
def beam_decode(ks, cwin, sign, W=64, cap=1200):
    """Full-length skip-tolerant beam (engine --decode mirror): width 64,
    advance 1..3, 3.0 nats/extra, cap 1200. Carries the winning path's
    extras-chain and replays it, so the returned values are the exact decode.
    Adjudication-only (top candidates); returns decoded rune values."""
    NEG = -1e30
    nks = len(ks); Lw = len(cwin)
    cur = [(0.0, 0, CTX_THE, ())]      # score, extra, ctx, extras-chain (tuple of per-rune advances)
    tr = TRANS; ll = LL
    for t in range(Lw):
        ct = cwin[t]
        nxt = []
        for (s0, e, ctx0, chain) in cur:
            kpos = t + e
            if kpos >= nks: continue
            p = (ct - sign * ks[kpos]) % N
            ctx = ctx0
            s = s0
            lt = tr[p]
            o = ord(lt[0]) - 65
            s += ll[ctx * 26 + o]; ctx = (ctx % 676) * 26 + o
            if len(lt) > 1:
                o = ord(lt[1]) - 65
                s += ll[ctx * 26 + o]; ctx = (ctx % 676) * 26 + o
            for a in (1, 2, 3):
                e2 = e + a - 1
                if e2 > cap: continue
                nxt.append((s - PEN * (a - 1), e2, ctx, chain + (a,)))
        if not nxt: return []
        nxt.sort(key=lambda x: -x[0])
        cur = nxt[:W]
    best = min(cur, key=lambda x: -x[0])
    # replay best chain to get values
    vals = []
    e = 0
    for t, a in enumerate(best[3]):
        kpos = t + e
        if kpos >= nks: break
        vals.append((cwin[t] - sign * ks[kpos]) % N)
        e += a - 1
    return vals

# ---------------------------------------------------------------- crib statistic (letter space, per page)
def crib_stat(vals, r0=0):
    """vals: decoded rune values covering corpus runes [r0, r0+len(vals)).
    Returns (total distinct hits summed over pages, [(page_i, hits)...] >=2)."""
    letters = "".join(TRANS[v] for v in vals)
    lens = [len(TRANS[v]) for v in vals]
    csz = [0]
    for x in lens: csz.append(csz[-1] + x)
    vend = r0 + len(vals)
    out = []; rb = 0; total = 0
    for i, plen in enumerate(PAGE_RUNES):
        pe = rb + plen
        a = max(rb, r0); b = min(pe, vend)
        if b - a >= 3:
            seg = letters[csz[a - r0]:csz[b - r0]]
            hits = {c for c in REPR if c in seg}
            total += len(hits)
            if len(hits) >= 2: out.append((PAGES[i], sorted(hits)))
        rb = pe
    return total, out

def sqrt3_stream(n):
    return _digits(lambda D: D(3).sqrt(), n)

# ---------------------------------------------------------------- keys: text hints
def text_vals(s, a1=False):
    out = []
    for ch in s.upper():
        i = V.LATIN2IDX.get(ch)
        if i is not None:
            out.append((i + 1) % N if a1 else i)
    return out

def load_hints():
    """Pinned hint value streams (addendum 1 item 2)."""
    H = {}
    H["armfwd"] = text_vals(open(os.path.join(ARMADA, "lp1_english_forward.txt")).read())
    H["armrev"] = text_vals(open(os.path.join(ARMADA, "lp1_english_reversed.txt")).read())
    import f14_lp1
    pages = f14_lp1.lp1_pages()
    allc = [c for v in pages.values() for c in v]
    r2i = f14_lp1.R2I
    H["scream"] = [r2i[c] for c in allc if c in r2i]
    import json
    sp = json.load(open(os.path.join(ROOT, "data/solved_plaintexts.json")))
    H["anend"] = list(sp["ANEND56"]); H["parable"] = list(sp["PARABLE57"])
    return H

def hint_variants(vals, a1, rev, fskip):
    k = [(v + 1) % N for v in vals] if a1 else list(vals)
    if rev: k.reverse()
    if fskip: k = [v for v in k if v != 0]
    return k

# ---------------------------------------------------------------- keys: math streams (K4)
def _primes_mod29(n):
    out = []; cand = 2
    while len(out) < n:
        isp = True; d = 2
        while d * d <= cand:
            if cand % d == 0: isp = False; break
            d += 1
        if isp: out.append(cand % N)
        cand += 1
    return out

def _fib_mod29(n):
    out = []; a, b = 1, 1
    for _ in range(n):
        out.append(a % N); a, b = b, a + b
    return out

def _digits(xfn, n):
    from decimal import Decimal, getcontext
    getcontext().prec = n + 30
    s = xfn(Decimal)
    d = "".join(ch for ch in str(s) if ch.isdigit())
    return [int(c) for c in d[:n]]

def _div_1033_3301(n):
    from decimal import Decimal, getcontext
    getcontext().prec = n + 30
    q = Decimal(1033) / Decimal(3301)
    d = "".join(ch for ch in str(q) if ch.isdigit())
    return [int(c) for c in d[:n]]

def k4_streams():
    S = {}
    S["primes"] = _primes_mod29(1140)
    S["fib"] = _fib_mod29(1140)
    S["phi"] = list(V.phi_prime_stream(1140))
    S["ratio"] = _div_1033_3301(3000)
    S["pi"] = _pi_stream(2000)
    S["e"] = _digits(lambda D: sum(D(1) / _fact(D, k) for k in range(1000)), 2000)
    S["sqrt2"] = _digits(lambda D: D(2).sqrt(), 2000)
    S["p56hex"] = _p56hex()
    return S

def _fact(D, k):
    r = D(1)
    for i in range(2, k + 1): r *= i
    return r

def _pi_stream(n):
    from decimal import Decimal, getcontext
    getcontext().prec = n + 30
    D = Decimal
    # Machin: pi/4 = 4*arctan(1/5) - arctan(1/239); direct alternating series
    eps = D(10) ** (-(n + 25))
    def arctan_inv(m):
        m2 = D(m * m); mk = D(m); s = 1 / mk; sign = -1; k = 1
        while True:
            mk *= m2
            term = 1 / (D(2 * k + 1) * mk)
            if term <= eps: break
            s += sign * term
            sign = -sign; k += 1
        return s
    pi = 4 * (4 * arctan_inv(5) - arctan_inv(239))
    d = "".join(ch for ch in str(pi) if ch.isdigit())
    return [int(c) for c in d[:n]]

def _p56hex():
    txt = open(os.path.join(ROOT, "docs/ORACLE_PAGES.md")).read()
    i = txt.index("Printed hex lines")
    j = txt.index("```", i) + 3
    blk = txt[j:txt.index("```", j)]
    hx = "".join(ch for ch in blk if ch in "0123456789abcdefABCDEF")
    return [int(c, 16) for c in hx]

# ---------------------------------------------------------------- encoders (plants)
def load_quad(path=QUAD):   # bit-identical to #26-A1 / #27 / #28
    ctx = {}
    for ln in open(path, encoding="utf-8"):
        q, c = ln.split()
        ctx.setdefault(q[:3], [[], []])
        ctx[q[:3]][0].append(q[3]); ctx[q[:3]][1].append(int(c))
    out = {}
    for k, (chs, ws) in ctx.items():
        cw = np.cumsum(ws); out[k] = (chs, cw / cw[-1])
    return out

def sampler(Q, rng, n):     # bit-identical to #26-A1
    AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    st = "THE"; out = []
    for _ in range(n):
        e = Q.get(st)
        ch = AZ[rng.integers(26)] if e is None else e[0][int(np.searchsorted(e[1], rng.random()))]
        out.append(V.LATIN2IDX[ch]); st = st[1:] + ch
    return out

def encode_keyskip1(P, K, sign, L):
    out, prev, pi, ki = [], -1, 0, 0
    while len(out) < L:
        p, k = P[pi], K[ki]
        c = (p + sign * k) % N
        while c == prev:
            ki += 1
            c = (p + sign * K[ki]) % N
        out.append(c); prev = c; pi += 1; ki += 1
    return bytes(out)

def encode_k1(P, seed, sign, L):
    """plaintext-autokey, keyskip0 (addendum 3 / L9): key = seed[t] for t<w
    else P[t-w]; no reject loop (keyskip1 autokey is not causally decodable —
    the key runs ahead of the emission once cumulative rejects exceed w)."""
    w = len(seed)
    return bytes((P[t] + sign * (seed[t] if t < w else P[t - w])) % N for t in range(L))

def encode_k2(P, w, sign, L, fs=0):
    """ciphertext-autokey, keyskip1 with causality leak (addendum 3): rejects
    consume key k[t-w+e] while e < w; when the causal key window is exhausted
    the doublet is emitted (leak). Key stream k = c (fs=0) or the nonzero
    values of c — the F-skip variant, LP1 rule; the decoder screens the same
    stream over the full corpus (ciphertext is known). t<w emitted with key 0
    (untested region). Decoder DP cap min(12, w-1) matches this policy."""
    c = []; nz = []; prev = -1
    for t in range(L):
        if t < w:
            cc = P[t] % N
        else:
            e = 0
            while True:
                ki = t - w + e
                k = (nz if fs else c)[ki] if ki < len(nz if fs else c) else 0
                cc = (P[t] + sign * k) % N
                if cc != prev or e + 1 >= w: break   # leak when causality exhausted
                e += 1
        c.append(cc)
        if cc: nz.append(cc)
        prev = cc
    return bytes(c)
