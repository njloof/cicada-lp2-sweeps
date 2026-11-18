#!/usr/bin/env python3
"""Campaign #20 - p15 decimal grid selector battery (PREREG
sweeps/2026-11-decimals). B1/B2 analytic containment, B3 MC sums,
B4/B5 doublet hits. Usage: python3 -I scripts/audit/decimal_test.py
"""
import math
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, ROOT)
sys.path.insert(0, HERE)
from core.validate import flat, translit  # noqa: E402

OUT = os.path.join(ROOT, "sweeps", "2026-11-decimals", "results")
DECS = [3278, 3299, 3298, 2838]
VOID = (2740, 4389)
SPAN = (1874, 3602)
D, SEED = 200_000, 20261220


def main():
    os.makedirs(OUT, exist_ok=True)
    stream = [i for n in list(range(50)) + [51, 52, 53, 54, 55]
              for i in flat(n)]
    N = len(stream)
    assert N == 12956, f"G1 FAIL {N}"                      # G1
    assert DECS == [3278, 3299, 3298, 2838]                # G2 (owner record)
    assert VOID[1] - VOID[0] + 1 == 1650                   # G3
    rep = [f"G1-G3 PASS: N={N}; grid rows {DECS} (3299 marked); void span 1650"]
    dbl = set(i for i in range(1, N) if stream[i] == stream[i - 1])
    assert len(dbl) == 86

    p_b1 = math.comb(VOID[1] - VOID[0] + 1, 4) / math.comb(N, 4)
    p_b2 = math.comb(SPAN[1] - SPAN[0] + 1, 4) / math.comb(N, 4)
    rep.append(f"B1 void containment: all {DECS} in {VOID}; p = {p_b1:.2e}")
    rep.append(f"B2 pre-axis span containment: all in {SPAN}; "
               f"p = {p_b2:.2e}")

    sums = [sum(int(c) for c in str(d)) for d in DECS]
    rng = random.Random(SEED)
    hits = 0
    for _ in range(D):
        ss = [sum([rng.randint(1, 9)] + [rng.randint(0, 9) for _ in range(3)])
              for _ in range(4)]
        if len(set(ss)) == 4 and max(ss) - min(ss) == 3:
            hits += 1
    p_b3 = (hits + 1) / (D + 1)
    rep.append(f"B3 digit sums {sums} (distinct, range 3); MC p = {p_b3:.5f} "
               f"(D={D}, seed {SEED})")

    for nm, sel in [("B4 (0-based)", DECS), ("B5 (1-based)", [d - 1 for d in DECS])]:
        obs = sum(1 for s in sel if s in dbl)
        p_at_least_1 = 1 - math.comb(N - 86, 4) / math.comb(N, 4)
        rep.append(f"{nm}: doublet hits {obs}/4; P(>=1 | null) = "
                   f"{p_at_least_1:.4f} -> {'NULL' if obs == 0 else f'p={p_at_least_1:.4f}'}")

    p15s = sum(len(flat(n)) for n in range(15))
    tr = {
        "R1 0-based": translit([stream[d] for d in DECS]),
        "R2 1-based": translit([stream[d - 1] for d in DECS]),
        "R3 Q3a-local": translit([stream[d - 1874] for d in DECS]),
        "R4 sums-in-p15": translit([stream[p15s + s] for s in sums]),
    }
    rep.append(f"Descriptive transliterations: {tr}; 3299 prime (before "
               f"3301) + ink/red double-mark; 3298 = 2x1649 (#10 quoted "
               f"1649; exact span 1650 - caveat)")

    ps = sorted([("B1", p_b1), ("B2", p_b2), ("B3", p_b3)], key=lambda x: x[1])
    adj = {nm: min(1.0, (3 - i) * p) for i, (nm, p) in enumerate(ps)}
    ok = [nm for nm, a in adj.items() if a < 0.05]
    verdict = (f"DECIMALS-STRUCTURED ({','.join(ok)} survive Holm; FLAG "
               f"FOR CONFIRMATION - post-hoc origin, independent prediction "
               f"required before adoption)" if ok else
               "DECIMALS-NULL (position family retired; power: B1/B2 could "
               "detect full-containment-class effects; B4/B5 near-blind)")
    rep.append("Holm: " + ", ".join(f"{k} adj={v:.4f}" for k, v in adj.items())
               + f" -> VERDICT: {verdict}")
    rep.append("DISCLOSURES: B1-B3 post-hoc (design-pass origin); B4/B5 "
               "a priori but null; dukotah H9 ink-tone channel already in "
               "our records via owner red-asterisk; 1649-vs-1650 caveat on "
               "the 3298 numeric flag.")
    with open(f"{OUT}/REPORT.md", "w") as f:
        f.write("# Campaign #20 report - p15 decimal grid\n\n"
                + "\n\n".join(rep) + "\n")
    print("\n".join(rep))


if __name__ == "__main__":
    main()
