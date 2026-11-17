#!/usr/bin/env python3
"""Campaign #15 — F2/F9: red digits 1-5 (pp36-38) as selectors.
PREREG: PREREG.md (commit 2931ab0, registered before any output).

Registered families (statistic = coincidence pairs sum_r C(n_r,2) over the
5 selected rune values; alpha = 0.05/3; FIRE iff p<=alpha AND ceiling-p<alpha):
  D1 digit -> 1-based position in its own stream line (line[L][d-1])
  D2 digit -> 1-based line number on its page (last rune of line #d)
  D3 digit -> 1-based dash-word index in its line (first rune of word #d)
Nulls: MC D=20000 uniform positions over the registered populations;
ceilings exact (all-five-agree), ceiling p analytic under each null.

Usage: python3 f2.py [--stage 20000] [--out results/f2_results.json]
"""
import argparse
import json
import os
import sys
import time
import zlib
from collections import Counter

import numpy as np

_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
sys.path.insert(0, _ROOT)
from core.validate import N as Q, GEMATRIA, TRANS  # noqa: E402

RUNES = "".join(r for r, _t, _p in GEMATRIA)
R2V = {c: i for i, c in enumerate(RUNES)}
V2L = [TRANS[v] for v in range(Q)]
KRIS = os.path.join(_ROOT, "sources", "dukotah", "liber-primus", "data",
                    "krisyotam_runes.txt")
PAGES = os.path.join(_ROOT, "data", "pages")
BOOK = list(range(50)) + list(range(51, 56))
SEED = 20261204
ALPHA = 0.05 / 3
# (page, 0-based line carrying the digit, digit value) — owner-confirmed
# census (docs/RED_CENSUS.md; round #1 + F3 answers).
DIGITS = [(36, 6, 1), (37, 1, 2), (37, 5, 3), (37, 10, 4), (38, 4, 5)]
LINE_LENS = [25, 23, 20, 19, 23]  # campaign #12 E1 pin


def load_blocks():
    lines = open(KRIS).read().splitlines()
    blocks, cur = [], []
    for l in lines:
        if l.strip() == "%":
            blocks.append(cur)
            cur = []
        else:
            cur.append(l)
    blocks.append(cur)
    return blocks


def runevals(s):
    return np.array([R2V[c] for c in s if c in R2V], dtype=np.int64)


def stat(vals):
    c = Counter(vals)
    return sum(n * (n - 1) // 2 for n in c.values())


def ceiling_p(dists):
    """P(all five selected values agree) under independent nulls;
    dists = list of length-29 probability vectors."""
    prod = np.ones(Q)
    for p in dists:
        prod *= p
    return float(prod.sum())


def mc_p(obs, dists, tag, D, rng_of):
    """Null draws: selection i takes a uniform index over its population
    (dists[i] comes from pop[i] value arrays). Returns (p, nulls)."""
    nulls = np.empty(D, dtype=np.int64)
    for d in range(D):
        rng = rng_of(d)
        vals = []
        for i in range(5):
            vals.append(int(dists[i]["pop"][rng.integers(0, len(dists[i]["pop"]))]))
        nulls[d] = stat(vals)
    p = (float((nulls >= obs).sum()) + 1.0) / (D + 1.0)
    return p, nulls


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", type=int, default=20000)
    ap.add_argument("--out", default=os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                  "results", "f2_results.json"))
    args = ap.parse_args()
    t0 = time.time()
    blocks = load_blocks()

    # ---- gates -------------------------------------------------------------
    assert len(blocks) == 57, f"G1 blocks {len(blocks)}"
    # block index = position in BOOK (krisyotam dropped the empty p50 slot;
    # tail +1 shift - f18.py p51tail convention). DIGITS pages (<50) unaffected.
    pages = {b: "\n".join(blocks[bi]).split("/") for bi, b in enumerate(BOOK)}
    total = sum(len(runevals(s)) for b in BOOK for s in pages[b])
    assert total == 12956, f"G3 runes {total}"
    for bi, b in enumerate(BOOK):
        tv = np.array(open(os.path.join(PAGES, f"lp2_{b:02d}.txt")).read().split(), dtype=np.int64)
        mine = np.concatenate([runevals(s) for s in pages[b]]) if pages[b] else np.array([], dtype=np.int64)
        assert np.array_equal(mine, tv), f"G3 bit-identical book {b}"
    line_vals = {}
    for pg, li, d in DIGITS:
        v = runevals(pages[pg][li])
        line_vals[(pg, li)] = v
        assert len(v) == LINE_LENS[DIGITS.index((pg, li, d))], f"G1 p{pg}L{li} len {len(v)}"
    nlines = {pg: sum(1 for s in pages[pg] if len(runevals(s))) for pg in (36, 37, 38)}
    assert nlines[36] >= 1 and nlines[37] >= 10 and nlines[38] >= 5, f"G2 line counts {nlines}"
    gates = {"blocks": 57, "L": total, "line_lens": LINE_LENS,
             "stream_lines": nlines, "bit_identical": True}
    print(f"gates PASS {gates}", flush=True)

    # ---- populations & observations ----------------------------------------
    # D1: position in own line (1-based)
    d1_pops = [line_vals[(pg, li)] for pg, li, _ in DIGITS]
    d1_obs = [int(line_vals[(pg, li)][d - 1]) for pg, li, d in DIGITS]
    # D2: 1-based line number on own page -> last rune (1-based over
    # rune-bearing lines; segment idx 11 is empty on all pages, verified)
    d2_pops = []
    for pg in (36, 37, 38):
        last = [int(runevals(s)[-1]) for s in pages[pg] if len(runevals(s))]
        d2_pops.append(np.array(last))
    page_pop = {36: d2_pops[0], 37: d2_pops[1], 38: d2_pops[2]}
    d2_obs = [int(page_pop[pg][d - 1]) for pg, _li, d in DIGITS]
    # D3: 1-based dash-word index -> first rune; empty (trailing) words are
    # positions with no rune -> excluded from populations (declared; observed
    # selections land on non-empty words, asserted)
    d3_pops = []
    for pg, li, d in DIGITS:
        words = pages[pg][li].split("-")
        firsts = [int(runevals(w)[0]) for w in words if len(runevals(w))]
        assert d <= len(firsts), f"G2 p{pg}L{li} word {d} empty/absent"
        d3_pops.append(np.array(firsts))

    d3_obs = [int(d3_pops[i][DIGITS[i][2] - 1]) for i in range(5)]
    # D2 has 5 selections over 3 page populations (p37 serves digits 2,3,4):
    sel_pops_d2 = [page_pop[pg] for pg, _li, _d in DIGITS]
    fams = {"D1": (d1_obs, d1_pops), "D2": (d2_obs, sel_pops_d2), "D3": (d3_obs, d3_pops)}
    results, flags = {}, []
    for fam in ("D1", "D2", "D3"):
        obs_vals, pops = fams[fam]
        obs = stat(obs_vals)
        dists = []
        for pop in pops:
            cnt = np.bincount(pop, minlength=Q).astype(float)
            dists.append({"pop": pop, "p": cnt / cnt.sum()})
        cp = ceiling_p([dd["p"] for dd in dists])
        p, nulls = mc_p(obs, dists, fam, args.stage,
                        lambda d, f=fam: np.random.default_rng(
                            [SEED, zlib.crc32(f.encode()) % 100000, d]))
        unpowered = cp >= ALPHA
        fire = (p <= ALPHA) and (cp < ALPHA)
        verdict = "FIRE" if fire else ("STRUCTURALLY-UNPOWERED" if unpowered else "NEGATIVE")
        if fire:
            flags.append(fam)
        results[fam] = {
            "obs_stat": obs,
            "selected": [{"page": pg, "digit": d, "value": int(v),
                          "letter": V2L[int(v)]}
                         for (pg, _li, d), v in zip(DIGITS, obs_vals)],
            "null": {"D": args.stage, "median": float(np.median(nulls)),
                     "mean": round(float(nulls.mean()), 4),
                     "p95": float(np.percentile(nulls, 95)), "max": int(nulls.max())},
            "p": p, "ceiling_p": cp, "alpha": ALPHA,
            # descriptive (disclosed): smallest p any observation could get
            # under this MC null; registered ceiling 10 is unreachable when
            # ceiling_p == 0 (no value shared by all five populations)
            "min_achievable_p": (float((nulls >= nulls.max()).sum()) + 1.0) / (args.stage + 1.0),
            "verdict": verdict,
        }
        print(f"{fam}: obs={obs} sel={[V2L[int(v)] for v in obs_vals]} "
              f"med={np.median(nulls):.1f} p={p:.5f} ceil_p={cp:.2e} -> {verdict}", flush=True)

    # D1 secondary (enumeration, no verdict): 0-based index d
    sec = [int(line_vals[(pg, li)][d]) for pg, li, d in DIGITS]
    out = {
        "campaign": "2026-11-redselect", "date_run": "2026-11-16",
        "prereg_commit": "2931ab0", "seed": SEED, "alpha": ALPHA,
        "gates": gates,
        "families": results,
        "d1_secondary_0based": [{"page": pg, "digit": d, "value": int(v),
                                 "letter": V2L[int(v)]}
                                for (pg, _li, d), v in zip(DIGITS, sec)],
        "flags": flags,
        "runtime_s": round(time.time() - t0, 2),
    }
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "w") as fh:
        json.dump(out, fh, indent=2)
    print(f"wrote {args.out} ({out['runtime_s']}s)", flush=True)


if __name__ == "__main__":
    main()
