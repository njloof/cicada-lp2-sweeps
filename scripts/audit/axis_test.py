#!/usr/bin/env python3
"""Campaign #19 — p15 axis reading (PREREG sweeps/2026-11-axis).
V1 largest-gap-center vs junction (permutation), V1b fixed-span
(analytic), V4 v2-unit homogeneity (report-only). Deterministic +
permutation nulls (D=20,000, seed 20261219).

Usage: python3 -I scripts/audit/axis_test.py
"""
import math
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
sys.path.insert(0, ROOT)
from core.validate import flat, load_page  # noqa: E402
from insert_transcriptions import load_pages  # noqa: E402
from lang_triage import words_of  # noqa: E402

OUT = os.path.join(ROOT, "sweeps", "2026-11-axis", "results")
D, SEED, ALPHA = 20_000, 20261219, 0.05
# v2 partition (SEGMENTS.md) with terminator subsections
UNITS = [("Q1", [0, 1, 2]), ("Q2", [3, 4, 5, 6, 7]),
         ("Q3a", list(range(8, 15))), ("Q3ax", [15]),
         ("Q3b", list(range(16, 23))), ("Q4", [23, 24, 25, 26]),
         ("Q5", list(range(27, 33))), ("Q6", list(range(33, 40))),
         ("Q7a", list(range(40, 50))), ("Q7b", list(range(50, 54))),
         ("Q7c", [54, 55])]
VOID_SITES = [2740, 3140, 3852, 4389]
TERM_END = {2, 7, 14, 22, 26, 32, 39, 49, 53, 55, 56, 57}
V2_EDGES = [2, 7, 22, 26, 32, 39, 55]
BINS = [(1, 1), (2, 2), (3, 3), (4, 6), (7, 99)]


def main():
    os.makedirs(OUT, exist_ok=True)
    rep = []
    stream, pstart, linelen = [], {}, {}
    for n in list(range(50)) + [51, 52, 53, 54, 55]:
        pstart[n] = len(stream)
        stream.extend(flat(n))
    N = len(stream)
    assert N == 12956, f"G1 FAIL {N}"
    seen = sorted(p for _, pg in UNITS for p in pg if p != 50)
    assert seen == [p for p in range(56) if p != 50], "G1 partition FAIL"

    # G2: terminators + doublets + void
    base = load_pages()
    ends = set()
    for p, lines in base.items():
        ls = [s.strip() for s in lines]
        if ls and ls[-1] in ("&", "$", "§"):
            ends.add(p)
    assert ends == TERM_END, f"G2 terminator FAIL {sorted(ends)}"
    p15m = [s.strip() for s in base[15]]
    assert "&" in p15m[:3] and "$" in p15m[:3], "G2 p15 mid-page FAIL"
    dbl = [i for i in range(1, N) if stream[i] == stream[i - 1]]
    assert len(dbl) == 86, f"G2 doublets FAIL {len(dbl)}"
    v = [d for d in dbl if 2740 <= d <= 4389]
    assert v == VOID_SITES, f"G2 void FAIL {v}"

    # G4: junction J = midpoint after p15 L0 (L0 = runes above '&')
    amp = p15m.index("&")
    # rune count above &: index stream (krisyotam lines may be raw strings)
    l0 = sum(len(load_page(15)[k]) for k in range(amp))
    J = pstart[15] + l0 - 0.5
    assert abs(J - 3611.5) <= 0.5, f"G4 FAIL J={J}"
    rep.append(f"G1-G4 PASS: N={N}; terminators {sorted(ends)}; void "
               f"{v} gaps {[b-a for a,b in zip(v,v[1:])]}; J={J} "
               f"(p15 starts {pstart[15]}, L0={l0} runes); G3 boundary "
               f"agreement {sum(e in ends for e in V2_EDGES)}/7 "
               f"(disclosed: same ornament channel, fidelity test only)")

    # V1: largest inter-doublet gap midpoint vs J (permutation)
    def lgc(sites):
        s = sorted(sites)
        gaps = [(b - a, (a + b) / 2) for a, b in zip(s, s[1:])]
        return max(gaps)
    (g_obs, c_obs), d1 = lgc(dbl), None
    d1 = abs(c_obs - J)
    rng = random.Random(SEED)
    ge = 0
    for _ in range(D):
        perm = rng.sample(range(1, N), 86)
        g, c = lgc(perm)
        if abs(c - J) <= d1 + 1e-9:
            ge += 1
    p_v1 = (ge + 1) / (D + 1)
    rep.append(f"V1 largest gap {g_obs} center {c_obs}; d1 = |{c_obs} - "
               f"{J}| = {d1:.1f}; permutation p = {p_v1:.4f} (D={D}, "
               f"seed {SEED})")

    # V1b: fixed #10 span center vs J (analytic)
    L = VOID_SITES[-1] - VOID_SITES[0] + 1
    c2 = (VOID_SITES[0] + VOID_SITES[-1]) / 2
    d2 = abs(c2 - J)
    lo, hi = L / 2, N - 1 - L / 2
    p_v1b = min(1.0, (2 * d2 + 1) / (hi - lo + 1))
    rep.append(f"V1b span [{VOID_SITES[0]},{VOID_SITES[-1]}] center {c2}; "
               f"d2 = {d2:.1f}; analytic p = {p_v1b:.4f} (span {L})")

    # V4: homogeneity of dots + word-lengths across 11 units
    upos, ulen = {}, {}
    for uid, pg in UNITS:
        pos = [i for n in pg if n != 50 for i in range(pstart[n],
               pstart[n] + len(flat(n)))]
        upos[uid] = pos
        ulen[uid] = len(pos)
    NTOT = sum(ulen.values())
    dots = sum(s.count(".") for _, pg in UNITS for p in pg
               for s in base.get(p, []))
    gdot = {uid: sum(s.count(".") for p in pg for s in base.get(p, []))
            for uid, pg in UNITS}
    pos2u = [ui for ui, (uid, _) in enumerate(UNITS) for _ in upos[uid]]
    assert len(pos2u) == N

    def chi_dots(cnt):
        return sum((cnt[uid] - dots * ulen[uid] / NTOT) ** 2
                   / (dots * ulen[uid] / NTOT) for uid, _ in UNITS)
    obs_d = chi_dots(gdot)
    rng2 = random.Random(SEED)
    ge_d = 0
    for _ in range(D):
        c = [0] * len(UNITS)
        for _ in range(dots):
            c[pos2u[rng2.randrange(N)]] += 1
        s = sum((c[i] - dots * ulen[UNITS[i][0]] / NTOT) ** 2
                / (dots * ulen[UNITS[i][0]] / NTOT) for i in range(len(UNITS)))
        if s >= obs_d - 1e-12:
            ge_d += 1
    p_v4a = (ge_d + 1) / (D + 1)

    wlen = {uid: [len(w) for p in pg for s in base.get(p, [])
                  for w in words_of(s) if s.strip() not in ("&", "$", "§")]
            for uid, pg in UNITS}
    tot = [sum(1 for uid, _ in UNITS for Lw in wlen[uid] if lo2 <= Lw <= hi2)
           for lo2, hi2 in BINS]
    ntot = sum(len(x) for x in wlen.values())
    obs_w = 0.0
    for uid, _ in UNITS:
        for k, (lo2, hi2) in enumerate(BINS):
            e = tot[k] * len(wlen[uid]) / ntot
            if e:
                obs_w += (sum(1 for Lw in wlen[uid] if lo2 <= Lw <= hi2)
                          - e) ** 2 / e
    allw = [next(k for k, (lo2, hi2) in enumerate(BINS) if lo2 <= Lw <= hi2)
            for uid, _ in UNITS for Lw in wlen[uid]]
    labels = [i for i, (uid, _) in enumerate(UNITS) for _ in wlen[uid]]
    ge_w = 0
    for _ in range(D):
        rng2.shuffle(labels)
        cnt = [[0] * 5 for _ in range(len(UNITS))]
        size = [0] * len(UNITS)
        for lb, k in zip(labels, allw):
            cnt[lb][k] += 1
            size[lb] += 1
        s = 0.0
        for i in range(len(UNITS)):
            for bi in range(5):
                e = tot[bi] * size[i] / ntot
                if e:
                    s += (cnt[i][bi] - e) ** 2 / e
        if s >= obs_w - 1e-12:
            ge_w += 1
    p_v4b = (ge_w + 1) / (D + 1)
    rep.append(f"V4 (report-only): dots {dots} chi2={obs_d:.2f} "
               f"p={p_v4a:.4f}; word-lengths n={ntot} chi2={obs_w:.2f} "
               f"p={p_v4b:.4f} across 11 v2 units")

    # Holm over {V1, V1b}; verdict per PREREG S3
    ps = sorted([("V1", p_v1), ("V1b", p_v1b)], key=lambda x: x[1])
    adj = {nm: min(1.0, (2 - i) * p) for i, (nm, p) in enumerate(ps)}
    verdict = ("AXIS-ALIGNED (void centering stands; axis = tracked "
               "structural feature; no pipeline re-keying)"
               if min(adj.values()) < ALPHA else
               "NO-AXIS-EVIDENCE (axis stays a presentation frame only)")
    rep.append(f"Holm: " + ", ".join(f"{k} adj p={v2:.4f}"
               for k, v2 in adj.items()) + f" -> VERDICT: {verdict}")
    rep.append("DISCLOSURES: void localized in #10 BEFORE the axis "
               "existed (new prediction vs old data); exploratory "
               "per-unit panel (4d44c21) preceded registration and is "
               "descriptive only; V1/V1b correlated (same 4 sites) - "
               "Holm conservative; G3 agreement not independent "
               "evidence; V4 non-falsifying per #18 rule.")
    with open(f"{OUT}/REPORT.md", "w") as f:
        f.write("# Campaign #19 report — p15 axis reading\n\n"
                + "\n\n".join(rep) + "\n")
    print("\n".join(rep))


if __name__ == "__main__":
    main()
