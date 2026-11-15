"""Shared key construction for campaign #7 (number channels as additive keys).
PREREG: PREREG.md — registered 2026-11-15 before any output.
All sequences are computed from the pinned corpus (or the md-printed A WARNING
values, PREREG item 2) so the whole space regenerates deterministically."""
import math, os, re, sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
from core.validate import flat, R2I, GEMATRIA, N as Q, translit  # noqa: E402
from core.kernel import pair_scan  # noqa: E402
from core.plaintexts import an_end_plain, parable_plain  # noqa: E402

PRIME = {i: p for i, (_r, _t, p) in enumerate(GEMATRIA)}
SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "sources")
MD = os.path.join(SRC, "scream314", "liber_primus.md")


def phi(n):
    if n <= 1:
        return n
    r, d, nn = n, 2, n
    while d * d <= nn:
        if nn % d == 0:
            while nn % d == 0:
                nn //= d
            r -= r // d
        d += 1
    if nn > 1:
        r -= r // nn
    return r


def digitsum(v):
    return sum(int(c) for c in str(abs(v)))


def md_lines(label):
    """Per-line rune-index lists of a scream314 section (md line-wrapping)."""
    sc = open(MD, encoding="utf-8").read()
    sec = [s for s in re.split(r"^## ", sc, flags=re.M) if s.startswith(label)][0]
    out = []
    for ln in sec.split("---")[0].splitlines():
        idx = [R2I[c] for c in ln if c in R2I]
        if idx:
            out.append(idx)
    return out


def _line_sums(idxs_per_line):
    return [sum(PRIME[i] for i in ln) for ln in idxs_per_line]


def _page_lines(n):
    p = f"{os.path.dirname(os.path.abspath(__file__))}/../../data/pages/lp2_{n:02d}.txt"
    return [[int(x) for x in ln.split()] for ln in open(p) if ln.strip()]


def build_sequences():
    """(name, raw integer sequence) — PREREG items 1-6 + digit expansions."""
    seqs = []
    seqs.append(("SW5", _line_sums(md_lines("05.jpg"))))                    # item 1
    seqs.append(("AWp", [757, 1009, 691, 353, 769]))                        # item 2 (printed)
    seqs.append(("WE5", _line_sums(md_lines("03.jpg"))))                    # item 3
    seqs.append(("DIV", [6, 19, 28, 19, 20, 19, 13, 3]))                    # item 4
    # item 5: per-line sums of solved plaintexts (line structure = page images'
    # 5-line layout for 56/57; md wrapping for LP1; WELCOME key-subtract is
    # plain periodic, no interrupter removal — disclosed simplification)
    ae, pa = an_end_plain(), parable_plain()
    def plain_line_sums(plain, lines):
        # ANEND plaintext is 84 vs 85 ct runes (one interrupter consumed):
        # consume line-lengths from the plain stream, clamped at its end.
        out, j = [], 0
        for ln in lines:
            hi = min(j + len(ln), len(plain))
            if hi > j:
                out.append(sum(PRIME[plain[t]] for t in range(j, hi)))
            j += len(ln)
        return out
    seqs.append(("PT56", plain_line_sums(ae, _page_lines(56))))
    seqs.append(("PT57", plain_line_sums(pa, _page_lines(57))))
    aw_lines = md_lines("Runes - 01.jpg")
    seqs.append(("PTAW", [sum(PRIME[(Q - 1 - c) % Q] for c in ln) for ln in aw_lines]))
    key = np.array([6, 19, 28, 19, 20, 19, 13, 3])
    we_lines, j, acc = md_lines("03.jpg"), 0, []
    for ln in we_lines:
        k = np.array(ln)
        ks = key[j:j + len(ln)] if j + len(ln) <= len(key) else np.tile(key, 1 + (j + len(ln)) // len(key))[j:j + len(ln)]
        acc.append(sum(PRIME[int(x)] for x in (k - ks) % Q))
        j += len(ln)
    seqs.append(("PTWE", acc))
    # item 6: digit expansions of the matrix constants (constants alone are
    # chi2-invariant and excluded; expansions are length-4 keys)
    seqs.append(("D1033", [1, 0, 3, 3]))
    seqs.append(("D3301", [3, 3, 0, 1]))
    return seqs


def build_variants(seqs=None):
    """Deduped additive keys: {id, phi, digitsum} x {direct, cumulative} x
    {sign} x {direction}; constant and length<2 keys excluded (chi2-invariant)."""
    seqs = seqs or build_sequences()
    seen, out = {}, []
    for name, raw in seqs:
        for tname, tf in (("v", lambda v: v), ("p", phi), ("d", digitsum)):
            base = [tf(v) for v in raw]
            for cname in ("", "c"):
                vals = base if cname == "" else np.cumsum(base)
                for sgn in (1, -1):
                    for dname, arr in (("", list(vals)), ("r", list(vals)[::-1])):
                        key = tuple((sgn * int(x)) % Q for x in arr)
                        if len(key) < 2 or len(set(key)) == 1:
                            continue
                        if key in seen:
                            continue
                        kid = f"v:{name}:{tname}{cname}{dname}"
                        seen[key] = kid
                        out.append((kid, key))
    return out


def key_from_id(keyid, variants):
    if keyid.startswith("v:"):
        for kid, key in variants:
            if kid == keyid:
                return np.array(key, dtype=np.int16)
    if keyid.startswith("r"):
        c, b = map(int, keyid[1:].split("."))
        return None  # ramps are length-dependent; use ramp_pad()
    if keyid == "dig37":
        return np.array([2, 3, 4], dtype=np.int16)
    raise KeyError(keyid)


def ramp_pad(c, b, m):
    return ((c * np.arange(m)) + b) % Q


def tiled(key, m):
    reps = 2 * (m // len(key) + 2)
    return np.tile(np.array(key, dtype=np.int16), reps)


def chi2_page(A, K, mask_both=False):
    """Whole-page chi2 under page-aligned key K (len == len(A))."""
    keep = A != 0
    if mask_both:
        keep &= K != 0
    vals = (A[keep] - K[keep]) % Q
    if len(vals) < 50:
        return -1.0, len(vals)
    h = np.bincount(vals, minlength=Q).astype(np.float64)
    nn = float(len(vals))
    return (Q / nn) * float((h * h).sum()) - nn, len(vals)


def variants_and_targets():
    variants = build_variants()
    targets = [n for n in range(55)]  # LP2 0-54 unsolved (p55 absent)
    return variants, targets


def iter_rows(fams, variants, targets, arrays=None):
    """Yield (fam, target, keyid, offset, n_valid, chi2) for every window.
    fams: subset of {"Vp","Vs","R","D"}. arrays: optional {page: np.array}
    (for shuffled nulls); default = corpus flat streams."""
    arrays = arrays or {n: np.array(flat(n), dtype=np.int16) for n in targets}
    for n in targets:
        A = arrays[n]
        m = len(A)
        if "Vp" in fams:
            for kid, key in variants:
                p = len(key)
                ka = np.array(key, dtype=np.int16)
                for o in range(p):
                    K = ka[(np.arange(m) - o) % p]  # page-aligned phase o
                    c2, nn = chi2_page(A, K)
                    if nn >= 50:
                        yield ("Vp", n, kid, o, nn, c2)
        if "Vs" in fams:
            for kid, key in variants:
                pad = tiled(key, m)
                for off, nn, c2, _ioc, _h in pair_scan(A, pad, mask="tgt", min_len=50):
                    yield ("Vs", n, kid, int(off), nn, float(c2))
        if "R" in fams:
            for c in range(1, Q):
                for b in range(Q):
                    pad = ramp_pad(c, b, m)
                    for off, nn, c2, _ioc, _h in pair_scan(A, pad, mask="tgt", min_len=50):
                        yield ("R", n, f"r{c}.{b}", int(off), nn, float(c2))
        if "D" in fams and 37 in arrays:
            A37 = arrays[37]
            pad = tiled((2, 3, 4), len(A37))
            for off, nn, c2, _ioc, _h in pair_scan(A37, pad, mask="tgt", min_len=50):
                yield ("D", 37, "dig37", int(off), nn, float(c2))


def family_max(fams, variants, targets, arrays):
    best = {}
    for fam, n, kid, off, nn, c2 in iter_rows(fams, variants, targets, arrays=arrays):
        if fam not in best or c2 > best[fam][0]:
            best[fam] = (c2, n, kid, off, nn)
    return best
