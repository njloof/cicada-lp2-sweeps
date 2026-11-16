#!/usr/bin/env python3
"""Campaign #9 space — implements PREREG.md exactly (registered 2026-11-16,
commit ab28743, before any output).

Orientation group on the line grid (data/pages, lines preserved):
  id / rl (reverse line order) / rg (reverse glyphs within line) /
  r180 = rl+rg (bottom-right to top-left; = flat reversal).
Declared collapse (chi2 reversal-invariance; maximal windows map exactly at
q = n-m-o): (o_M,o_N) == (r180 o_M, r180 o_N) for diff/sum  =>  16 combos
= 8 classes (CLASSES below). Verified on synthetic grids at registration;
the real-corpus pilot (run.py --pilot) is output-blocking.

Families:
  O1 mirror pairs (k,55-k), 27 pairs (p50 runeless, excluded), 8 classes,
     {diff, sum} x both operand orders (sum order matters under tgt mask -
     the commute collapse was falsified by the registration pilot)
  O2 CONTROL: all ordered pairs id-only, diff + sum, both orders
  T1 token<->token: canon_256.bin tables p49/p51/p50 as byte streams mod 29,
     token-grid orientations, BOTH idx-246 variants (shipped canon 0xc6 /
     dissenting-witness 0xe0 - see token_tab docstring)
  T2 token->rune affine bridge: pad = a*(T mod 29), a in 2..28 (b excluded:
     constant shift, chi2-invariant), vs every unsolved rune page, id
Instrument: core.kernel.pair_scan UNCHANGED (mask tgt primary; both for
confirmation at leader stage).
"""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, ROOT)
from core import DATA  # noqa: E402
from core.kernel import pair_scan, Q, MIN_LEN  # noqa: E402,F401

CANON = f"{ROOT}/sources/dukotah/liber-primus/analysis/pp49_51/canon_256.bin"
UNSOLVED = [n for n in range(56) if n != 50]          # book 0-49 + 51-55

ORIENTS = ("id", "rl", "rg", "r180")
COMP = {"id": "r180", "r180": "id", "rl": "rg", "rg": "rl"}   # compose with r180
# canonical representatives of the 8 collapse classes (first of each pair)
CLASSES = [("id", "id"), ("id", "rl"), ("id", "rg"), ("id", "r180"),
           ("rl", "id"), ("rl", "rl"), ("rl", "rg"), ("rg", "id")]
# the full 16-combo pairing, for the pilot check
PAIRING = [(oM, oN, COMP[oM], COMP[oN]) for oM in ORIENTS for oN in ORIENTS]

MIRROR_PAIRS = [(k, 55 - k) for k in range(28) if k != 5]      # (5,50) drops
assert len(MIRROR_PAIRS) == 27 and all(m in UNSOLVED and n in UNSOLVED
                                       for m, n in MIRROR_PAIRS)


def load_grids():
    """book page -> (flat rune-index array, line lengths)."""
    grids = {}
    for n in range(58):
        p = f"{DATA}/pages/lp2_{n:02d}.txt"
        if not os.path.exists(p):
            continue
        lines = [[int(x) for x in ln.split()] for ln in open(p) if ln.split()]
        grids[n] = (np.array([v for ln in lines for v in ln], np.int8),
                    [len(l) for l in lines])
    return grids


def read(arr, lens, o):
    """Flat sequence of the page under orientation o (all four are
    involutions - self-inverse permutations)."""
    if o == "id":
        return arr
    if o == "r180":
        return arr[::-1]
    rows = np.split(arr, np.cumsum(lens)[:-1])
    if o == "rl":
        return np.concatenate(rows[::-1])
    if o == "rg":
        return np.concatenate([r[::-1] for r in rows])
    raise ValueError(o)


def perm_of(lens, o):
    """read(arange, lens, o) — oriented-index -> raw-index map."""
    n = int(sum(lens))
    return read(np.arange(n, dtype=np.int32), lens, o)


# ---- token streams (T1/T2) --------------------------------------------------
def token_tab(variant="canon"):
    """Canonical token bytes. Variant 'e0' = the dissenting-witness reading
    at idx 246 (root+relikd 3i = 0xe0); the pinned current canon_256.bin is
    0xc6 (3I) - matching our pixel adjudication and the owner read (the
    CAMPAIGN-VII doc hex / *_superseded.bin carry the old 0xe0)."""
    byts = np.frombuffer(open(CANON, "rb").read(), np.uint8).copy()
    if variant == "e0":
        assert byts[246] == 0xC6
        byts[246] = 0xE0
    return byts


def tok_read(tab, o):
    """Orientation at the TOKEN level on the 8-per-row grid (a token is a
    2-byte unit; byte order within a token is never reversed), then flat."""
    toks = tab.reshape(-1, 2)
    rows = [toks[i:i + 8] for i in range(0, len(toks), 8)]
    if o == "rl":
        rows = rows[::-1]
    elif o == "rg":
        rows = [r[::-1] for r in rows]
    elif o == "r180":
        rows = [r[::-1] for r in rows[::-1]]
    return np.concatenate([r.reshape(-1) for r in rows])


def tok_streams(tab):
    """{'p49': {orient: stream}, ...} for the three tables. Streams are
    reduced mod 29 at build time (PREREG: "mod 29 into the 29-bin space").
    NB: this is NOT the same as the kernel's mod-29 of D — the F mask tests
    the raw operand value, so pre-reducing also fixes which positions count
    as F (residue 0). Doing it here keeps the scan faithful to the PREREG."""
    out = {}
    for name, sl in (("p49", slice(0, 80)), ("p50", slice(80, 184)),
                     ("p51", slice(184, 256))):
        t = tab[sl]
        out[name] = {o: (tok_read(t, o).astype(np.int32) % Q).astype(np.int8)
                     for o in ORIENTS}
    return out


# ---- family iterators: yield (key, A, B, op) --------------------------------
def iter_fam(fam, grids, variants=("canon", "e0")):
    if fam == "O1":
        for M, N in MIRROR_PAIRS:
            for oM, oN in CLASSES:
                A = read(*grids[M], oM)
                B = read(*grids[N], oN)
                tag = f"{M}-{N}|{oM}.{oN}"
                yield f"{tag}|dMN", A, B, "diff"
                yield f"{tag}|dNM", B, A, "diff"
                yield f"{tag}|sMN", A, B, "sum"
                yield f"{tag}|sNM", B, A, "sum"
    elif fam == "O2":
        for M in UNSOLVED:
            A = grids[M][0]
            for N in UNSOLVED:
                if M == N:
                    continue
                yield f"{M}>{N}|d", A, grids[N][0], "diff"
                yield f"{M}>{N}|s", A, grids[N][0], "sum"
    elif fam == "T1":
        for var in variants:
            S = tok_streams(token_tab(var))
            for oM, oN in CLASSES:
                A, B = S["p49"][oM], S["p51"][oN]
                tag = f"{var}:49-51|{oM}.{oN}"
                yield f"{tag}|dMN", A, B, "diff"
                yield f"{tag}|dNM", B, A, "diff"
                yield f"{tag}|sMN", A, B, "sum"
                yield f"{tag}|sNM", B, A, "sum"
                for T in ("p49", "p51"):                       # p50 as pad
                    for op in ("diff", "sum"):
                        yield (f"{var}:{T}-p50|{oM}.{oN}|{op}",
                               S[T][oM], S["p50"][oN], op)
    elif fam == "T2":
        for var in variants:
            S = tok_streams(token_tab(var))
            for T in ("p49", "p50", "p51"):
                base = S[T]["id"].astype(np.int32) % Q
                for a in range(2, Q):
                    pad = ((a * base) % Q).astype(np.int8)
                    for M in UNSOLVED:
                        yield f"{var}:{T}|a{a}|{M}", grids[M][0], pad, "diff"
    else:
        raise ValueError(fam)


FAMS = ("O1", "O2", "T1", "T2")


def scan_max(A, B, op, mask="tgt"):
    """Family-max helper: (chi2, offset, n) over all offsets."""
    best = (-1.0, None, 0)
    for off, nn, c2, ioc, h in pair_scan(A, B, mask=mask, stat=op):
        if c2 > best[0]:
            best = (c2, off, nn)
    return best


def scan_rows(fam, grids, variants=("canon", "e0")):
    """Yield (key, offset, n_valid, chi2) for every window of the family."""
    for key, A, B, op in iter_fam(fam, grids, variants):
        for off, nn, c2, ioc, h in pair_scan(A, B, mask="tgt", stat=op):
            yield key, off, nn, c2


def shuffled(grids, rng):
    """Null draw: permute each page's VALUES, line lengths fixed (house
    pattern from #8); token tables permuted by the same stream in
    scan_null_draw."""
    return {n: (rng.permutation(arr).astype(np.int8), lens)
            for n, (arr, lens) in grids.items()}


def scan_null_draw(fam, grids, rng):
    """One null draw of a family: shuffle operands, rerun the FULL family
    scan (all pairs, classes, ops, offsets), return the family max.
    Orientation and pairing choices are inside the max by construction."""
    g2 = shuffled(grids, rng)
    variants = ("canon", "e0")
    if fam in ("T1", "T2"):
        # permute token byte values too (operand streams of T families)
        orig = token_tab
        def shuffled_tab(variant="canon", _o=orig, _r=rng):
            t = _o(variant)
            return _r.permutation(t)
        globals()["token_tab"] = shuffled_tab
        try:
            rows = scan_rows(fam, g2, variants)
            mx = max((c2 for _, _, _, c2 in rows), default=-1.0)
        finally:
            globals()["token_tab"] = orig
        return mx
    return max((c2 for _, _, _, c2 in scan_rows(fam, g2, variants)),
               default=-1.0)
