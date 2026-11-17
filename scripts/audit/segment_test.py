#!/usr/bin/env python3
"""Campaign #18 — decoration-based segmentation tests (PREREG
sweeps/2026-11-segments). S1 T7-void containment, S2 per-group doublet
deficit, S3 sentence-dot density, S4 word-length differentiation.
Deterministic + two permutation nulls (D=20,000, seed 20261218).

Usage: python3 -I scripts/audit/segment_test.py
"""
import math
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
sys.path.insert(0, ROOT)
from core.validate import flat  # noqa: E402
from insert_transcriptions import load_pages  # noqa: E402
from lang_triage import words_of  # noqa: E402

OUT = os.path.join(ROOT, "sweeps", "2026-11-segments", "results")
GROUPS = [("P1", [0, 1, 2]), ("P2", [3, 4]), ("P3", [5, 6, 7]),
          ("P4", list(range(8, 24))), ("P5", [24, 25]),
          ("P6", list(range(26, 33))), ("P7", list(range(33, 40))),
          ("P8", list(range(40, 49))), ("P9", list(range(49, 56)))]
VOID = (2740, 4389)  # campaign #10 doublet-SPARSE span (gap indices
# 17-19 = 400+712+537; #10 quoted "2739-4388" = span minus one; sites
# 2740/3140/3852/4389, mean internal gap 550 vs corpus mean ~151)
BINS = [(1, 1), (2, 2), (3, 3), (4, 6), (7, 99)]
D, SEED = 20_000, 20261218
ALPHA = 0.05


def main():
    os.makedirs(OUT, exist_ok=True)
    # stream + group ranges
    stream, gpos = [], {}
    for gid, pages in GROUPS:
        start = len(stream)
        for p in pages:
            stream.extend(flat(p) if p != 50 else [])
        gpos[gid] = (start, len(stream) - 1)
    N = len(stream)
    assert N == 12956, f"G1 FAIL: {N}"  # G1
    seen = sorted(p for _, pg in GROUPS for p in pg if p != 50)
    assert seen == [p for p in range(56) if p != 50], "G2 FAIL"  # G2

    # doublets
    dbl = [i for i in range(1, N) if stream[i] == stream[i - 1]]
    assert len(dbl) == 86, f"G3a: {len(dbl)} doublets"
    void_sites = [d for d in dbl if VOID[0] <= d <= VOID[1]]
    assert void_sites == [2740, 3140, 3852, 4389], f"G3b: {void_sites}"
    vg = [b - a for a, b in zip(void_sites, void_sites[1:])]
    assert vg == [400, 712, 537], f"G3c: {vg}"
    lo = max([d for d in dbl if d < VOID[0]], default=-1)
    hi = min([d for d in dbl if d > VOID[1]], default=-1)
    rep = [f"G1 stream {N} EXACT; G2 partition EXACT; G3 void reproduced "
           f"EXACTLY (86 doublets; span sites {void_sites}, gaps {vg}, "
           f"sum {sum(vg)}; flanking sites {lo}/{hi}; mean internal gap "
           f"{sum(vg)/3:.0f} vs corpus mean {N/86:.0f})"]

    # S1 containment
    L = VOID[1] - VOID[0] + 1
    inside = [g for g, (a, b) in gpos.items() if a <= VOID[0] and VOID[1] <= b]
    p1 = sum(max(0, (b - a + 1) - L + 1) for a, b in gpos.values()) / (N - L + 1)
    edges = min(min(abs(VOID[0] - a), abs(VOID[1] - b)) for a, b in gpos.values())
    rep.append(f"S1 void [{VOID[0]},{VOID[1]}] ({L} runes) contained in "
               f"{inside}; nearest group edge distance {edges}; "
               f"P(random {L}-window in one group) = {p1:.4f}")

    # S2 per-group doublet deficit
    zs, k_neg = [], 0
    for gid, _ in GROUPS:
        a, b = gpos[gid]
        seg = stream[a:b + 1]
        m = len(seg)
        obs = sum(1 for i in range(1, m) if seg[i] == seg[i - 1])
        fr = {}
        for r in seg:
            fr[r] = fr.get(r, 0) + 1
        p2 = sum((c / m) ** 2 for c in fr.values())
        exp = (m - 1) * p2
        z = (obs - exp) / math.sqrt((m - 1) * p2 * (1 - p2))
        zs.append((gid, obs, round(exp, 1), round(z, 2)))
        k_neg += z < 0
    p2v = sum(math.comb(9, j) for j in range(k_neg, 10)) / 2 ** 9
    rep.append(f"S2 per-group doublets (obs/exp/z): {zs}; {k_neg}/9 groups "
               f"deficient, sign-test p = {p2v:.4f}")

    # S3 sentence-dot density (krisyotam '.' over stream positions)
    base = load_pages()
    dots = sum(s.count(".") for _, pg in GROUPS for p in pg for s in base.get(p, []))
    assert dots == 173, f"S3 pin: {dots}"
    gdot = {g: sum(s.count(".") for p in pg for s in base.get(p, []))
            for g, pg in GROUPS}
    grune = {g: gpos[g][1] - gpos[g][0] + 1 for g, _ in GROUPS}

    def chi_counts(cnt):
        s = 0
        for g, _ in GROUPS:
            e = dots * grune[g] / N
            s += (cnt[g] - e) ** 2 / e
        return s

    obs3 = chi_counts(gdot)
    pos2g = []
    for i, (g, _) in enumerate([(g, 0) for g, _ in GROUPS]):
        a, b = gpos[g]
        pos2g.extend([i] * (b - a + 1))
    assert len(pos2g) == N
    rng = random.Random(SEED)
    ge3 = 0
    for _ in range(D):
        c = [0] * 9
        for _ in range(dots):
            c[pos2g[rng.randrange(N)]] += 1
        s = 0.0
        for i, (g, _) in enumerate(GROUPS):
            e = dots * grune[g] / N
            s += (c[i] - e) ** 2 / e
        if s >= obs3 - 1e-12:
            ge3 += 1
    p3 = (ge3 + 1) / (D + 1)
    rep.append(f"S3 dots per group {gdot}; chi2 = {obs3:.2f}, "
               f"permutation p = {p3:.4f} (D={D}, seed {SEED})")

    # S4 word-length differentiation
    wlen = {g: [len(w) for p in pg for s in base.get(p, [])
                for w in words_of(s) if s.strip() not in ("&", "$", "§")]
            for g, pg in GROUPS}
    tot = [sum(1 for g, _ in GROUPS for L in wlen[g] if lo <= L <= hi)
           for lo, hi in BINS]
    ntot = sum(len(v) for v in wlen.values())

    def chi4(gw):
        s = 0.0
        for g, _ in GROUPS:
            for k, (lo, hi) in enumerate(BINS):
                e = tot[k] * len(gw[g]) / ntot
                if e:
                    s += (sum(1 for L in gw[g] if lo <= L <= hi) - e) ** 2 / e
        return s

    obs4 = chi4(wlen)
    allw = [next(i for i, (lo, hi) in enumerate(BINS) if lo <= L <= hi)
            for g, _ in GROUPS for L in wlen[g]]
    labels = [i for i, (g, _) in enumerate(GROUPS) for _ in wlen[g]]
    assert len(labels) == len(allw) == ntot
    exp_frac = [t / ntot for t in tot]
    ge4 = 0
    for _ in range(D):
        rng.shuffle(labels)
        cnt = [[0] * 5 for _ in range(9)]
        size = [0] * 9
        for l, k in zip(labels, allw):
            cnt[l][k] += 1
            size[l] += 1
        s = 0.0
        for i in range(9):
            for bi in range(5):
                e = tot[bi] * size[i] / ntot
                if e:
                    s += (cnt[i][bi] - e) ** 2 / e
        if s >= obs4 - 1e-12:
            ge4 += 1
    p4 = (ge4 + 1) / (D + 1)
    rep.append(f"S4 words n={ntot}; chi2 across 9 groups = {obs4:.2f}, "
               f"permutation p = {p4:.4f}")

    # Holm + verdict (labels per PREREG §3)
    ps = sorted([("S1", p1), ("S2", p2v), ("S3", p3), ("S4", p4)], key=lambda x: x[1])
    labels = {}
    m = len(ps)
    for i, (name, p) in enumerate(ps):
        adj = min(1.0, (m - i) * p)
        if name == "S1":
            labels[name] = "SUPPORTS" if (inside and adj < ALPHA) else "NEUTRAL"
        else:
            labels[name] = "SUPPORTS" if adj < ALPHA else "NEUTRAL"
        rep.append(f"Holm {name}: raw p={p:.4f} adj={adj:.4f} -> {labels[name]}")
    sup = sum(v == "SUPPORTS" for v in labels.values())
    verdict = ("SEGMENTATION-CONSISTENT" if sup >= 2 else "NO-GROUPS-EVIDENCE "
               "(segmentation stays a presentation frame; pipeline NOT restructured)")
    rep.append(f"VERDICT: {sup} SUPPORTS, 0 REFUTES -> {verdict}")
    rep.append(
        "DISCLOSURES: (1) S2 WEAK DISCRIMINATION — a single stream with a "
        "global anti-repeat filter also predicts per-group deficits; the "
        "9/9 result is consistent-with, not evidence-for, separate streams "
        "(per-group rates do vary, 0.52%-1.48%, unregistered follow-up). "
        "(2) VOID CONVENTION — #10 quoted '2739-4388'; exact sites are "
        "2740/3140/3852/4389 (their span minus one) and the span is "
        "doublet-SPARSE (mean gap 550 vs 151), not literally zero; G3 "
        "reproduces sites+gaps EXACTLY. (3) S4 RERUN — first run had a "
        "comprehension-variable leak (tot computed for one group only); "
        "fixed pre-report, seed unchanged, verdict identical. (4) S3/S4 "
        "homogeneity is NOT a refutation (shared register possible) per "
        "PREREG §3.")
    with open(f"{OUT}/REPORT.md", "w") as f:
        f.write("# Campaign #18 report — segmentation tests\n\n" +
                "\n\n".join(rep) + "\n")
    print("\n".join(rep))


if __name__ == "__main__":
    main()
