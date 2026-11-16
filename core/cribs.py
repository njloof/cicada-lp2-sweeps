#!/usr/bin/env python3
"""GO-prong-3 crib list — the "25-crib house list", VERSIONED at last.

Disclosed gap: campaigns #1-#8 quoted a "25-crib house list" in PREREGs and
REPORTs (e.g. "0/80 leaders decode fwd+rev vs 25 cribs") but the list itself
was never committed; it lived in ad-hoc session scripts. Two 25-word variants
were recovered from session transcripts on 2026-11-15. Campaign #9 (and every
campaign from here) uses the UNION below (36 words, 31 representable in the
29-rune alphabet — V/K/Q/Z absent, hence DIUINITY next to DIVINITY). This is
permissive relative to either historical list; it is a qualitative confirmation
gate, not a statistical one (prong 1 carries the multiplicity), and the
per-word hit is always reported for human review.

Usage: crib_hits(translit_text) -> list of hit words; decode_window() builds
the D/S letter string of a winning window (target order, tgt mask).
"""
from core.validate import translit

CRIBS = [
    # recovered variant A (transcript, 25 words)
    "DEEPWEB", "WITHIN", "PILGRIM", "ANEND", "WELCOME", "DIVINITY", "PARABLE",
    "SURFACE", "SHADOW", "CIRCUMFERENCE", "KNOWLEDGE", "WARNING", "LIBER",
    "PRIMUS", "CICADA", "THIRTY", "SELF", "MIRROR", "REVERSE", "EMERGE",
    "FIND", "SHED", "START", "TUNNEL", "DEEP",
    # recovered variant B adds (11 new)
    "PILGRIM", "HASHESTO", "TRUTH", "DIUINITY", "JOURNEY", "BELIEVE",
    "WISDOM", "OBSCURA", "MOBIUS", "THIRD", "ONION", "WEB",
]
# dedupe preserving order
seen = set()
CRIBS = [c for c in CRIBS if not (c in seen or seen.add(c))]
assert len(CRIBS) == 36, len(CRIBS)

from core.validate import TRANS                                   # noqa: E402
LETTERS = set(TRANS.values())      # 29-rune alphabet letters (no V/K/Q/Z)
REPR = [c for c in CRIBS if all(ch in LETTERS for ch in c)]       # encodable


def crib_hits(text):
    """Words present in the (already transliterated) letter string."""
    return [c for c in REPR if c in text]


def decode_window(A, B, op, off, mask="tgt"):
    """Letter string of the D/S window at `off` (i - j = off), positions in
    ascending target order, tgt/both mask as recorded. Returns (fwd, rev)."""
    m, n = len(A), len(B)
    vals = []
    for i in range(m):
        j = i - off
        if not (0 <= j < n):
            continue
        if mask == "tgt" and A[i] == 0:
            continue
        if mask == "both" and (A[i] == 0 or B[j] == 0):
            continue
        vals.append((int(A[i]) + int(B[j])) % 29 if op == "sum"
                    else (int(A[i]) - int(B[j])) % 29)
    s = translit(vals)
    return s, s[::-1]
