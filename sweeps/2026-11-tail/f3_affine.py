#!/usr/bin/env python3
"""Campaign #24 Lane A — F3 affine canon-as-key residual (PREREG
sweeps/2026-11-tail/PREREG.md, committed 1a48cec BEFORE output).

Self-contained (studio-syncable: lives under sweeps/, imports only
core/). p[m] = a*(C_j[m] + eps*K[o+m]) + s (mod 29); key = our 13,136-
rune canon (gate: equals dukotah's canon length exactly); offsets =
canon page starts (shrunk family, disclosed); statistic = skeleton-
legal crib hits; MC null of the max = letter shuffles of best texts
(S=1000/page, D=200, seed 20261224, per-replicate substreams,
resumable via work/tail_f3/null_maxes.txt). Verdict per PREREG; a HIT
is a flag for the owner, never auto-certified.

Run:  python3 sweeps/2026-11-tail/f3_affine.py   (local or studio)
"""
import os
import random
import re
import sys
import time
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, ROOT)
import numpy as np                      # noqa: E402
import core.validate as V               # noqa: E402
import core.skeleton as S               # noqa: E402
from core.cribs import REPR as CRIBS    # noqa: E402

OUT = os.path.join(HERE, "results")
WORK = os.path.join(ROOT, "work", "tail_f3")
MERGE = str.maketrans("KVZQ", "CUSS")
VAL = [g[1] for g in V.GEMATRIA]
BOOK58 = list(range(50)) + list(range(51, 58))
UNSOLVED = S.UNSOLVED
SEED = 20261224
S_SHUF, D = 1000, 200
CRIB_RE = re.compile("|".join(sorted(CRIBS, key=len, reverse=True)))


def merged(txt):
    return txt.upper().translate(MERGE)


def hits_of(text, page, nulls, skel):
    raw = {m.group(0) for m in CRIB_RE.finditer(text)}
    if not raw:
        return 0, 0
    bad = S._bad(page, nulls, skel)
    legal = 0
    for crib in raw:
        if crib in S.MULTIWORD:
            legal += 1
            continue
        L = len(crib)
        st, ok = 0, False
        while True:
            o = text.find(crib, st)
            if o < 0:
                break
            if not any(o <= b < o + L - 1 for b in bad):
                ok = True
                break
            st = o + 1
        legal += ok
    return legal, len(raw)


def canon():
    k, starts, t = [], [], 0
    for n in BOOK58:
        starts.append(t)
        f = V.flat(n)
        k.extend(f)
        t += len(f)
    return np.array(k, dtype=np.int64), starts


def scan_page(j, K, starts):
    C = np.array(V.flat(j), dtype=np.int64)
    skel = S.skeleton(j)
    Lc = len(C)
    out = []
    for o in starts:
        L = min(Lc, len(K) - o)
        if L < 60:
            continue
        Ks = K[o:o + L]
        for eps in (1, -1):
            base = (C[:L] + eps * Ks) % 29
            for a in range(2, 29):
                X = (a * base) % 29
                for s in range(29):
                    Dm = (X + s) % 29
                    txt = merged("".join([VAL[x] for x in Dm.tolist()]))
                    if not CRIB_RE.search(txt):
                        continue
                    legal, raw = hits_of(txt, j, (), skel)
                    if raw:
                        out.append((legal, raw, eps, a, s, o, txt))
    out.sort(key=lambda x: (-x[0], -x[1], -S.score_text(x[6])))
    return out


def plants(K, starts):
    A = np.array(V.flat(57), dtype=np.int64)   # p57 PT == CT
    skel = S.skeleton(57)
    res = []
    for (a, eps, s, osrc) in ((7, -1, 13, 12), (15, 1, 5, 30), (23, -1, 20, 0)):
        o = starts[osrc]
        L = min(len(A), len(K) - o)
        ainv = pow(a, 27, 29)
        C = (ainv * (A - s) - eps * K[o:o + L]) % 29
        base = (C + eps * K[o:o + L]) % 29
        txt = merged("".join([VAL[x] for x in ((a * base + s) % 29).tolist()]))
        legal, raw = hits_of(txt, 57, (), skel)
        res.append(f"  plant a={a} eps={eps:+d} s={s} key@p{osrc}: legal "
                   f"{legal}/raw {raw} ({'PASS >=3' if legal >= 3 else 'FAIL'})")
    return res


def main():
    t0 = time.time()
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(WORK, exist_ok=True)
    rep = []
    assert all(v == v.upper() for v in VAL), "VAL must be uppercase"
    K, starts = canon()
    assert len(K) == 13136, f"A-G1 FAIL len={len(K)}"
    N = sum(len(V.flat(n)) for n in UNSOLVED)
    assert N == 12956, f"G1 FAIL N={N}"
    tc = {}
    for p in sorted(S._blocks()):
        for d, _ in S.skeleton(p)["marks"]:
            tc["◆" + d] = tc.get("◆" + d, 0) + 1
    assert tc.get("◆4") == 129, f"G3 FAIL {tc}"
    rep.append(f"Gates: canon 13,136 (58 starts; EXACTLY dukotah's canon "
               f"length — lineage concern resolved; PREREG's 13,141 was an "
               f"arithmetic slip, see corrections); N=12,956; census ◆4=129. "
               f"Family 55 x {len(starts)} x 27 x 29 x 2 decodes.")

    per_page = []
    for i, j in enumerate(UNSOLVED):
        ranked = scan_page(j, K, starts)
        per_page.append(dict(page=j, n_raw=len(ranked),
                             m=ranked[0][0] if ranked else 0,
                             best=ranked[0] if ranked else None))
        if (i + 1) % 10 == 0:
            print(f"  {i+1}/55 pages, {time.time()-t0:.0f}s", flush=True)
    M = max(r["m"] for r in per_page)
    rep.append(f"Sweep: M = {M}; pages at M: "
               f"{[r['page'] for r in per_page if r['m'] == M and M]}")
    for r in per_page:
        b = r["best"]
        rep.append(f"  p{r['page']:>2}: raw>0={r['n_raw']:>3} m={r['m']}"
                   + (f"  best eps{b[2]:+d} a={b[3]} s={b[4]} key@{b[5]}: "
                      f"{b[6][:50]}" if b else ""))

    best_txt = {r["page"]: (r["best"][6] if r["best"] else "")
                for r in per_page}
    skels = {p: S.skeleton(p) for p in UNSOLVED}
    NULLF = os.path.join(WORK, "null_maxes.txt")
    null_maxes = []
    if os.path.exists(NULLF):
        null_maxes = [int(x) for x in open(NULLF).read().split()]
    for d in range(len(null_maxes), D):
        rng = random.Random(f"{SEED}:{d}")
        gm = 0
        for page in UNSOLVED:
            t = best_txt[page]
            if not t:
                continue
            pm, tl = 0, list(t)
            for _ in range(S_SHUF):
                rng.shuffle(tl)
                lh, _ = hits_of("".join(tl), page, (), skels[page])
                pm = max(pm, lh)
            gm = max(gm, pm)
        null_maxes.append(gm)
        with open(NULLF, "a") as f:
            f.write(f"{gm}\n")
    beats = sum(1 for x in null_maxes if x >= M)
    p = (1 + beats) / (len(null_maxes) + 1)
    rep.append(f"Null of the max: hist {dict(sorted(Counter(null_maxes).items()))}"
               f", beaten {beats}/{len(null_maxes)}, p={p:.4f}")
    rep.append("Power plants (p57 carrier, scorer test only):\n"
               + "\n".join(plants(K, starts)))
    verdict = ("AFFINE-HIT — FLAG FOR OWNER REVIEW (nothing auto-certified)"
               if p < 0.05 else
               "AFFINE-NULL — affine canon-as-key residual closed at "
               "page-start coverage (a in 2..28, s in 0..28, eps +-1); "
               "arbitrary-offset affine NOT covered (dukotah's additive "
               "all-offset negative is the only coverage there)")
    rep.append(f"VERDICT: {verdict}")
    rep.append("DISCLOSURES: (1) offsets shrunk to canon page starts "
               "(F13 lesson); non-page-start affine alignments invisible. "
               "(2) no interrupter/skip model in this family. (3) canon "
               "length 13,136 verified EQUAL to dukotah's canon. (4) "
               "shuffle surrogates conservative (break digraph structure). "
               f"(5) runtime {time.time()-t0:.0f} s.")
    with open(f"{OUT}/LANE_A_REPORT.md", "w") as f:
        f.write("# Campaign #24 Lane A (F3 affine residual) report\n\n"
                + "\n\n".join(rep) + "\n")
    print("\n".join(rep))


if __name__ == "__main__":
    main()
