#!/usr/bin/env python3
"""Pytest cases: the rig must reproduce every known LP2/LP1 decryption, plus
kernel self-tests for the sweep machinery. Run: python3 -m pytest -q
"""
import numpy as np, pytest
from core import validate as V
from core import kernel as sweep

TRANS = V.translit

# ---------- known decodes ----------

def test_atbash_a_warning():
    sc = open(f"{V.SRC}/scream314/liber_primus.md", encoding="utf-8").read()
    sec = [s for s in sc.split("\n## ") if s.startswith("Runes - 01.jpg")][0]
    ct = [V.R2I[c] for c in sec.split("---")[0] if c in V.R2I]
    txt = TRANS([(29 - 1 - c) % 29 for c in ct])
    for w in ("BELIEUE", "FROMTHIS", "TRUE"):     # V->U: runes alphabet has no V
        assert w in txt

def test_welcome_vigenere():
    sc = open(f"{V.SRC}/scream314/liber_primus.md", encoding="utf-8").read()
    sec = [s for s in sc.split("\n## ") if s.startswith("03.jpg")][0]
    ct = [V.R2I[c] for c in sec.split("---")[0] if c in V.R2I]
    res = V.brute_interrupters(ct, V.keyword_stream("DIVINITY", len(ct)),
                               ["WELCOME", "PILGRIM", "JOURNEY"])
    assert res and res[1] == 3, res

def test_wisdom_identity():
    sc = open(f"{V.SRC}/scream314/liber_primus.md", encoding="utf-8").read()
    sec = [s for s in sc.split("\n## ") if s.startswith("05.jpg")][0]
    ct = [V.R2I[c] for c in sec.split("---")[0] if c in V.R2I]
    txt = TRANS(ct)                              # standard futhark, no layer
    for w in ("THEPRIMESARESACRED", "TOTIENT", "ENCRYPTED"):
        assert w in txt

def test_koan_atbash_shift3():
    sc = open(f"{V.SRC}/scream314/liber_primus.md", encoding="utf-8").read()
    sec = [s for s in sc.split("\n## ") if s.startswith("06.jpg")][0]
    ct = [V.R2I[c] for c in sec.split("---")[0] if c in V.R2I]
    txt = TRANS([(29 - 1 - c + 3) % 29 for c in ct])   # dukotah "atbash+shift+3"
    for w in ("ACOAN", "MASTER", "STUDENT"):
        assert w in txt

def test_circumference_vigenere():
    # public since 2017; mislabeled an open lead until the 2026-11-18 review
    sc = open(f"{V.SRC}/scream314/liber_primus.md", encoding="utf-8").read()
    sec = [s for s in sc.split("\n## ") if s.startswith("14.jpg")][0]
    ct = [V.R2I[c] for c in sec.split("---")[0] if c in V.R2I]
    res = V.brute_interrupters(ct, V.keyword_stream("FIRFUMFERENFE", len(ct)),
                               ["LESSON", "MASTER", "EXPLAINED", "STUDENT"])
    assert res and res[1] == 4, res

def test_p15_grid_closed_form():
    # external review 2026-11-18: recorded grid = |3301 - prime(F+1)| over
    # distinct Fibonacci F (16/16; dukotah round44's 14/16 missed the sign
    # flips 1206 = prime(611)-3301, 4516 = prime(988)-3301). Fibonacci order
    # is a square spiral from the red 3299. Containment readings retracted.
    def nth_prime(k):
        n, c = 1, 0
        while c < k:
            n += 1
            if V.is_prime(n):
                c += 1
        return n
    fibs = [0, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987]
    grid = [3258, 3222, 3152, 3038, 3278, 3299, 3298, 2838,
            3288, 3294, 3296, 2472, 4516, 1206, 708, 1820]
    assert sorted(abs(3301 - nth_prime(f + 1)) for f in fibs) == sorted(grid)
    assert 3301 - nth_prime(1) == 3299           # spiral origin = the red cell

def test_anend_phi_prime():
    ct = V.flat(56)
    res = V.brute_interrupters(ct, V.phi_prime_stream(len(ct)),
                               ["DEEPWEB", "PILGRIM", "HASHESTO"])
    assert res and res[1] == 3, res

def test_parable_translit():
    txt = TRANS(V.flat(57))
    assert "DIUINITY" in txt and "EMERGE" in txt

def test_phi_stream_values():
    # first primes 2,3,5,7,11 -> (p-1) mod 29
    assert V.phi_prime_stream(5) == [1, 2, 4, 6, 10]

def test_keyword_stream_wrap():
    # A=24, B=17 in gematria order; stream repeats the key
    assert V.keyword_stream("AB", 5) == [24, 17, 24, 17, 24]

# ---------- sweep kernel self-tests ----------

def test_pair_scan_recovers_planted_pad():
    """Synthetic round-trip (Appendix C style): plant C_M = P_M + C_N at offset o,
    kernel must peak at that (pad, offset)."""
    rng = np.random.default_rng(7)
    N = rng.integers(1, 29, size=200, dtype=np.int8)          # pad (no F to keep it clean)
    # skewed plaintext (English-like: a few frequent symbols) — a uniform "plaintext"
    # would be indistinguishable from the null, which is the whole point of the test
    probs = np.full(28, 1.0); probs[[3, 17, 9, 15, 18]] = 9.0   # R E I T M heavy (idx-1)
    probs /= probs.sum()
    P = rng.choice(np.arange(1, 29), size=120, p=probs).astype(np.int8)  # no F(0)
    o = 37
    C = np.zeros(len(P) + o, dtype=np.int8)
    C[o:] = (P + N[:len(P)]) % 29
    hits = {off: chi2 for off, n, chi2, ioc, h in sweep.pair_scan(C, N)}
    assert max(hits, key=hits.get) == o
    assert hits[o] > 5 * np.median(list(hits.values()))

def test_pair_scan_uniform_null():
    rng = np.random.default_rng(11)
    A = rng.integers(0, 29, size=250, dtype=np.int8)
    B = rng.integers(0, 29, size=250, dtype=np.int8)
    chis = [c for _, _, c, _, _ in sweep.pair_scan(A, B)]
    assert max(chis) < 120  # ~250 windows, Bonferroni-ish bound for uniform null

def test_trivial_self_excluded():
    p = np.array([3, 7, 1, 9, 4, 2, 12, 5], dtype=np.int8)
    hits = [c for off, n, c, i, h in sweep.pair_scan(p, p, min_len=1) if off == 0]
    # offset 0 of self-pair is all-zero D (chi2 enormous); run_sweep excludes it,
    # pair_scan itself still reports it (exclusion lives in run_sweep)
    # all-zero D on 8 valid positions: chi2 = (29/8)*8^2 - 8 = 224 exactly
    assert hits and hits[0] == pytest.approx(224.0)

def test_straddle_dedup():
    A = np.arange(1, 6, dtype=np.int8)
    B = np.arange(1, 11, dtype=np.int8)
    offs = [o for o, n, c, i, h in sweep.pair_scan(A, B, min_len=1, straddle=5)]
    assert offs == [-4, -3, -2, -1]

def test_mask_modes():
    A = np.array([5, 0, 7, 9, 3, 12, 1, 4], dtype=np.int8)
    B = np.array([2, 0, 8, 1, 6], dtype=np.int8)
    n_tgt = sum(n for _, n, *_ in sweep.pair_scan(A, B, mask="tgt", min_len=1))
    n_both = sum(n for _, n, *_ in sweep.pair_scan(A, B, mask="both", min_len=1))
    assert n_tgt > n_both  # target-only mask keeps pad-F positions
