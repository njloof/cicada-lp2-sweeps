#!/usr/bin/env python3
"""Campaign #22 — p15 grid as 16 stream pointers (PREREG
sweeps/2026-11-grid16, committed a4eacf9 BEFORE output).

S1 doublet-site hits (primary, both conventions, Holm) + S2 phi-prime
aligned-window crib scan (secondary) + S3 report-only panel.

Usage: python3 -m scripts.audit.grid_pointers   (or direct path; <60 s)
"""
import math
import os
import random
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)
import core.validate as V          # noqa: E402
from core.cribs import REPR as CRIBS  # noqa: E402

OUT = os.path.join(ROOT, "sweeps", "2026-11-grid16", "results")
MERGE = str.maketrans("KVZQ", "CUSS")
BOOK = list(range(50)) + list(range(51, 56))
GRID = [3258, 3222, 3152, 3038, 3278, 3299, 3298, 2838,
        3288, 3294, 3296, 2472, 4516, 1206, 708, 1820]
SEED = 20261222
D = 20000
W = 12


def main():
    os.makedirs(OUT, exist_ok=True)
    rep = []
    stream = []
    for n in BOOK:
        stream.extend(V.flat(n))
    N = len(stream)
    assert N == 12956, f"G1 FAIL N={N}"
    # doublet sites (within pages, global index of FIRST rune)
    sites, base = set(), 0
    for n in BOOK:
        p = V.flat(n)
        for j in range(len(p) - 1):
            if p[j] == p[j + 1]:
                sites.add(base + j)
        base += len(p)
    assert len(sites) == 86, f"G2 FAIL sites={len(sites)}"
    assert len(GRID) == 16
    rep.append(f"G1 N={N}; G2 sites={len(sites)}; G3 grid=16 recorded")

    def hyper_tail(k, K, n):
        return sum(math.comb(K, i) * math.comb(N - K, n - i)
                   for i in range(k, min(n, K) + 1)) / math.comb(N, n)

    # ---- S1 ----
    k0 = sum(g in sites for g in GRID)
    k1 = sum(g - 1 in sites for g in GRID)
    p0 = hyper_tail(k0, len(sites), 16)
    p1 = hyper_tail(k1, len(sites), 16)
    rep.append(f"S1 0-based: k={k0}/16 p={p0:.4f} | 1-based: k={k1}/16 "
               f"p={p1:.4f} | expected 0.106; P(>=1)=0.101 P(>=2)=0.0050")

    # ---- S2 ----
    K = V.phi_prime_stream(N)

    def win_hits(g):
        idx = [(stream[g + i] - K[g + i]) % 29 for i in range(W)]
        t = V.translit(idx).upper().translate(MERGE)
        return sum(c in t for c in CRIBS), t

    obs, texts = 0, []
    for g in GRID:
        h, t = win_hits(g - 1)          # 0-based primary
        obs += h
        texts.append(f"  {g}: {t}")
    if obs == 0:
        p2, beats = 1.0, 0       # P(null_total >= 0) = 1 trivially
        rep.append("S2 aligned-window crib hits: obs=0/16 windows; "
                   "null P(>=0)=1 by construction, MC skipped")
    else:
        rng = random.Random(SEED)
        beats = 0
        for _ in range(D):
            pos = set()
            while len(pos) < 16:
                pos.add(rng.randrange(N - W))
            tot = sum(win_hits(g)[0] for g in pos)
            if tot >= obs:
                beats += 1
            if beats > D // 4:          # p will exceed any alpha
                break
        p2 = (1 + beats) / (D + 1)
        rep.append(f"S2 aligned-window crib hits: obs={obs}/16 windows, "
                   f"beaten by {beats}/{D} nulls, p={p2:.4f}")

    # ---- Holm ----
    tests = sorted([("S1-0b", p0), ("S1-1b", p1), ("S2", p2)],
                   key=lambda x: x[1])
    m = len(tests)
    holm = []
    for i, (nm, p) in enumerate(tests):
        holm.append((nm, p, min(1.0, (m - i) * p)))
    surv = [nm for nm, _, ph in holm if ph < 0.05]
    rep.append("Holm: " + ", ".join(f"{nm} adj_p={ph:.4f}"
                                    for nm, _, ph in holm))

    # ---- verdict ----
    if surv:
        verdict = f"GRID-SELECTS ({','.join(surv)})"
    elif obs == 0 and k0 == 0 and k1 == 0:
        verdict = ("GRID-NULL-WEAKLY-POWERED — all observed zeros; S1 "
                   "near-blind (exp 0.106); S2 blind unless global "
                   "alignment holds; pointer reading SUSPENDED, not "
                   "retired; option (b) ink-sweep remains")
    else:
        verdict = "GRID-NULL"
    rep.append(f"VERDICT: {verdict}")
    rep.append("S3 (report-only) 0-based window decodes:\n"
               + "\n".join(texts))
    rep.append("DISCLOSURES: (1) FIRST COMPLETED RUN INVALID (not "
               "retained): MC early-break capped beats at 101/20000 when "
               "obs=0, yielding p=0.0050 and a spurious GRID-SELECTS; "
               "true P(null>=0)=1. Fixed before this run. (2) grid seen "
               "pre-registration (owner S12 answer); pointer-semantics "
               "channel choice post-hoc to containment. (3) row-2 "
               "doublet contribution fixed at 0 by #20 glance. (4) S2 "
               "conditional on global keystream alignment (zero power "
               "under other alignments). (5) S3 shifted repeats at "
               "3288-3299 are window overlap, not signal.")
    with open(f"{OUT}/REPORT.md", "w") as f:
        f.write("# Campaign #22 report — p15 grid as 16 stream pointers\n\n"
                + "\n\n".join(rep) + "\n")
    print("\n".join(rep))


if __name__ == "__main__":
    main()
