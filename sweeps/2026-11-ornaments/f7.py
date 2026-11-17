#!/usr/bin/env python3
"""Campaign #13 / F7 — dot-lattices as data (language-agnostic structural
tests). Registration: PREREG.md (db6f467), committed before any output.
Families O1 (hypergeometric head alignment), O2 (count-vs-gap Spearman,
permutation null), O3 (counts-as-selectors coincidence, permutation null),
O4 (descriptive). Seed 20261202, alpha 0.05/3.

Disclosure (registered here, first executable line of the campaign): the O3
null set is finite and smaller than the registered MC stage
(C(30,3) = 4,060 assignments < D = 10,000), so the MC is replaced by
EXHAUSTIVE enumeration of the identical null set -> exact p. O2 keeps the
registered MC (its null set is 34!/(30!4!) = C(34,4) = 46,376 > 10,000).
Disclosed rerun: O2 PLANT construction bug fixed after the first run (see
o2() comment); obs and null streams are bit-identical across the rerun.

Usage: python3 f7.py [--out results/f7_results.json]
"""
import csv
import json
import math
import os
import sys
import time
import zlib
from collections import Counter
from itertools import combinations

import numpy as np

_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
sys.path.insert(0, _ROOT)
from core.validate import N as Q  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
PAGES = os.path.join(_ROOT, "data", "pages")
BOOK = list(range(50)) + list(range(51, 56))
HEADS = [0, 3, 6, 7, 8, 15, 23, 27, 33, 37, 39, 40, 53, 54]
UNIVERSE = [p for p in range(58) if p != 50]          # 57 pages
SEED = 20261202
ALPHA = 0.05 / 3
D_O2 = 10000
H = 3600


def rng_for(tag, draw):
    return np.random.default_rng([SEED, zlib.crc32(tag.encode()) % 100000, draw])


def load():
    lat = list(csv.DictReader(open(os.path.join(HERE, "lattices.csv"))))
    for r in lat:
        for k in ("page", "band", "y0", "y1", "x0", "x1", "dots"):
            r[k] = int(r[k])
    # G1
    assert len(lat) == 35, "G1 lattice count"
    assert Counter(r["dots"] for r in lat) == {13: 30, 10: 4, 23: 1}, "G1 size classes"
    stream, pstart, off = [], {}, 0
    for p in BOOK:
        pstart[p] = off
        vals = [int(x) for x in open(os.path.join(PAGES, f"lp2_{p:02d}.txt")).read().split()]
        stream.extend(vals)
        off += len(vals)
    assert len(stream) == 12956, "G2 corpus L"       # G2
    assert len(set(HEADS)) == 14 and set(HEADS) <= set(UNIVERSE), "G3 heads"
    return lat, np.array(stream), pstart


# ---------------- O1 ----------------

def hyper_p(ge, N, K, n):
    """P(X >= ge) hypergeometric."""
    num = sum(math.comb(K, k) * math.comb(N - K, n - k) for k in range(ge, min(K, n) + 1))
    den = math.comb(N, n)
    return num / den


def o1(lat):
    N, n, K = len(UNIVERSE), len(HEADS), len({r["page"] for r in lat})
    obs = len({r["page"] for r in lat} & set(HEADS))
    kmin = next(k for k in range(n + 1) if hyper_p(k, N, K, n) <= ALPHA)
    return {"N": N, "K_lattice_pages": K, "n_heads": n, "obs_overlap": obs,
            "expected": round(K * n / N, 2), "p": hyper_p(obs, N, K, n),
            "min_detectable_overlap": kmin, "alpha": round(ALPHA, 4)}


# ---------------- O2 ----------------

def avg_rank(x):
    order = np.argsort(x, kind="stable")
    r = np.empty(len(x), float)
    i = 0
    while i < len(x):
        j = i
        while j + 1 < len(x) and x[order[j + 1]] == x[order[i]]:
            j += 1
        r[order[i:j + 1]] = (i + j) / 2 + 1
        i = j + 1
    return r


def spearman(a, b):
    ra, rb = avg_rank(a), avg_rank(b)
    ra -= ra.mean()
    rb -= rb.mean()
    return float(ra @ rb / math.sqrt((ra @ ra) * (rb @ rb)))


def o2(lat):
    order = sorted(lat, key=lambda r: r["page"] * H + r["y0"])
    anch = np.array([r["page"] * H + r["y0"] for r in order])
    dots = np.array([r["dots"] for r in order])
    gaps = np.diff(anch)                       # paired with LEFT lattice (section opener)
    g, d = gaps, dots[:-1]                     # last lattice has no following gap
    obs = abs(spearman(g, d))
    multiset = Counter(d.tolist())
    nulls = np.empty(D_O2)
    for t in range(D_O2):
        nulls[t] = abs(spearman(g, rng_for("O2", t).permutation(d)))
    p = (1 + int((nulls >= obs).sum())) / (D_O2 + 1)
    p95 = float(np.percentile(nulls, 95))
    # plant: monotone rearrangement (rearrangement inequality maximizes |rho|
    # given the multiset); 20 random tie-breaks among equal gaps.
    # FIXED after first run (disclosed rerun): v1 permuted the gaps but built
    # the assignment in permuted space and scored it against the ORIGINAL gap
    # order -> scored a random assignment (0/20). obs/null streams untouched.
    hits = 0
    plant_ps = []
    for t in range(20):
        rng = rng_for("plant-O2", t)
        jit = rng.random(len(g)) * 1e-9 * (np.ptp(g) + 1)   # tie noise
        idx = np.argsort(g + jit, kind="stable")            # orig positions, small gaps first
        dp = np.empty(len(g), int)
        dp[idx] = np.sort(d)                                 # counts rise with gap
        rp = abs(spearman(g, dp))
        hits += rp > p95
        plant_ps.append((1 + int((nulls >= rp).sum())) / (D_O2 + 1))
    return {"n_lattices": len(order), "n_gaps": len(g),
            "effective_dots_multiset": dict(multiset),
            "obs_abs_rho": round(obs, 4), "null_median": round(float(np.median(nulls)), 4),
            "null_p95": round(p95, 4), "p": p, "D": D_O2,
            "plant_hits_vs_p95": f"{hits}/20", "plant_p_min": round(min(plant_ps), 5),
            "last_lattice": f"p{order[-1]['page']} band{order[-1]['band']} "
                            f"({order[-1]['dots']}-dot) - no following gap, excluded",
            "power_note": "plant is the max-|rho| assignment of the observed multiset "
                          "(rearrangement inequality); ties broken at random, 20 draws"}


# ---------------- O3 ----------------

def o3(lat, stream, pstart):
    sub = [r for r in lat if r["page"] in pstart]
    n = len(sub)
    base = np.array([pstart[r["page"]] for r in sub])
    sel13 = stream[(base + 13 - 1) % 12956]
    sel10 = stream[(base + 10 - 1) % 12956]
    n10 = int(sum(r["dots"] == 10 for r in sub))
    assert n10 == 3 and n == 30, "O3 scope"

    def coinc(tens):
        v = sel13.copy()
        v[list(tens)] = sel10[list(tens)]
        c = Counter(v.tolist())
        return sum(x * (x - 1) // 2 for x in c.values())

    obs = coinc(tuple(i for i, r in enumerate(sub) if r["dots"] == 10))
    # EXHAUSTIVE null: all C(30,3) = 4060 placements of the three 10-counts
    allc = np.array([coinc(t) for t in combinations(range(n), 3)])
    p = (1 + int((allc >= obs).sum())) / (len(allc) + 1)
    p95 = float(np.percentile(allc, 95))
    ceiling = int(allc.max())
    sel = sel13.copy()
    tpos = tuple(i for i, r in enumerate(sub) if r["dots"] == 10)
    sel[list(tpos)] = sel10[list(tpos)]
    return {"n": n, "excluded_solved_pages": [r["page"] for r in lat if r["page"] not in pstart],
            "obs_coincidence": obs, "null_D": int(len(allc)),
            "null_median": float(np.median(allc)), "null_p95": p95,
            "null_max": int(allc.max()), "p": p,
            "ceiling_plant": ceiling, "ceiling_p": (1 + int((allc >= ceiling).sum())) / (len(allc) + 1),
            "power": "CEILING > p95" if ceiling > p95 else "STRUCTURALLY WEAKLY POWERED (declared)",
            "selected_values": sel.tolist(),
            "selected_letters": None}   # letters filled by caller (TRANS)


# ---------------- O4 ----------------

def o4(lat):
    ys = sorted({r["y0"] for r in lat})
    diffs = Counter(b - a for a, b in zip(ys, ys[1:]))
    return {"distinct_y": ys, "consecutive_y_diffs_histogram": dict(sorted(diffs.items())),
            "band0_lattices": sum(1 for r in lat if r["band"] == 0),
            "per_page_counts": dict(sorted(Counter(r["page"] for r in lat).items())),
            "x_range": [min(r["x0"] for r in lat), max(r["x1"] for r in lat)],
            "height_by_size": {s: sorted({r["y1"] - r["y0"] for r in lat if r["dots"] == s})
                               for s in (13, 10, 23)}}


def main():
    t0 = time.time()
    lat, stream, pstart = load()
    print("gates G1/G2/G3 PASS", flush=True)
    r1 = o1(lat)
    print(f"O1: overlap {r1['obs_overlap']} (exp {r1['expected']}) p={r1['p']:.5f}", flush=True)
    r2 = o2(lat)
    print(f"O2: |rho| {r2['obs_abs_rho']} p={r2['p']} plants {r2['plant_hits_vs_p95']}", flush=True)
    r3 = o3(lat, stream, pstart)
    print(f"O3: coinc {r3['obs_coincidence']} vs med {r3['null_median']} p95 {r3['null_p95']} "
          f"ceiling {r3['ceiling_plant']} p={r3['p']}", flush=True)
    from core.validate import TRANS
    r3["selected_letters"] = [TRANS[v] for v in r3["selected_values"]]
    r4 = o4(lat)
    res = {"seed": SEED, "alpha_per_family": round(ALPHA, 5),
           "O1_head_alignment": r1, "O2_count_vs_gap": r2,
           "O3_counts_as_selectors": r3, "O4_descriptive": r4,
           "flags": [k for k, r, pv in (("O1", r1, r1["p"]), ("O2", r2, r2["p"]),
                                        ("O3", r3, r3["p"])) if pv <= ALPHA]}
    res["runtime_s"] = round(time.time() - t0, 2)
    out = os.path.join(HERE, "results", "f7_results.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    json.dump(res, open(out, "w"), indent=1)
    print("wrote", out, res["runtime_s"], "s", flush=True)


if __name__ == "__main__":
    main()
