#!/usr/bin/env python3
"""Campaign #25 Lane D — F3' affine canon-as-key at ARBITRARY key
offsets (PREREG sweeps/2026-11-tail2/PREREG.md, committed 86f6755 BEFORE
output). Crib-anchored slot inversion (see PREREG for the algebra and
the disclosed anchor shrink). Verdict per PREREG; a HIT is a flag for
the owner, never auto-certified.

Run (studio):  python3 sweeps/2026-11-tail2/f3prime_affine.py
"""
import json
import multiprocessing as mp
import os
import random
import re
import sys
import time
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, ROOT)
import numpy as np                      # noqa: E402
import core.validate as V               # noqa: E402
import core.skeleton as S               # noqa: E402
from core.cribs import REPR as CRIBS    # noqa: E402

OUT = os.path.join(HERE, "results")
WORK = os.path.join(ROOT, "work", "tail2_d")
MERGE = str.maketrans("KVZQ", "CUSS")
VAL = [g[1] for g in V.GEMATRIA]
BOOK58 = list(range(50)) + list(range(51, 58))
UNSOLVED = S.UNSOLVED
SEED = 20261227
S_SHUF, D = 1000, 200
CRIB_RE = re.compile("|".join(sorted(CRIBS, key=len, reverse=True)))
MULTIWORD = S.MULTIWORD
MIN_WIN = 60

# merged single-letter rune map + digraph map (preimage enumeration)
LET1 = {}
DIG = {}
for i, l in enumerate(VAL):
    m = l.translate(MERGE)
    if len(m) == 1:
        LET1.setdefault(m, []).append(i)
    else:
        DIG[m] = i


def merged(t):
    return t.upper().translate(MERGE)


def preimages(crib):
    """All rune-index sequences whose merged transliteration == crib."""
    out = []

    def rec(i, acc):
        if i == len(crib):
            out.append(tuple(acc))
            return
        for r in LET1.get(crib[i], []):
            rec(i + 1, acc + [r])
        d = DIG.get(crib[i:i + 2])
        if d is not None:
            rec(i + 2, acc + [d])
    rec(0, [])
    return out


def hits_of(text, page, nulls, skel):
    raw = {m.group(0) for m in CRIB_RE.finditer(text)}
    if not raw:
        return 0, 0
    bad = S._bad(page, nulls, skel)
    legal = 0
    for crib in raw:
        if crib in MULTIWORD:
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


PRE = {}                      # crib -> [rune tuples]
CRIBS_BY_LEN = defaultdict(list)
for _c in CRIBS:
    PRE[_c] = preimages(_c)
    if _c not in MULTIWORD:
        CRIBS_BY_LEN[len(_c)].append(_c)


def build_index(K, lengths):
    """r -> {window bytes: [offsets]} over the canon."""
    idx = {}
    for r in lengths:
        d = defaultdict(list)
        Kb = K.astype(np.uint8)
        for o in range(len(Kb) - r + 1):
            d[Kb[o:o + r].tobytes()].append(o)
        idx[r] = d
    return idx


def anchors_for(page):
    """[(t, crib, multi)] slot-aligned anchors in rune space."""
    runes = np.array(V.flat(page), dtype=np.int64)
    skel = S.skeleton(page)
    slots, _ = S.word_slots(skel, page)
    cum = S._cum(page, ())          # cum[t] = letters THROUGH rune i (INCLUSIVE)
    lens = [len(VAL[i]) for i in V.flat(page)]
    L2R = {int(cum[t]) - lens[t]: t for t in range(len(lens))}  # start letter -> rune
    out = []
    for ls, ln in slots:
        t = L2R.get(ls)
        if t is None:
            continue
        for c in CRIBS_BY_LEN.get(ln, []):
            out.append((t, c, False))
        for c in MULTIWORD:
            out.append((t, c, True))
    return runes, skel, out


def scan_page(page, K, idx, C=None, skel=None, anchors=None):
    """Inversion scan; C/skel/anchors overridable for plants."""
    if anchors is None:
        runes, skel, anchors = anchors_for(page)
        C = runes
    else:
        runes = C
    n = len(C)
    cells = {}                                # (o,a,s,eps) -> True
    for (t, crib, multi) in anchors:
        for R in PRE[crib]:
            r = len(R)
            if t + r > n:
                continue
            Rv = np.array(R, dtype=np.int64)
            Cw = C[t:t + r]
            us = np.arange(1, 29)
            for eps in (1, -1):
                A = (us[:, None] * Rv[None, :] - eps * Cw[None, :]) % 29
                need = (A[:, None, :]
                        - (us[:, None] * np.arange(29)[None, :])[:, :, None]
                        ) % 29
                rows = need.astype(np.uint8)
                for ui in range(28):
                    for si in range(29):
                        # index returns the ABSOLUTE canon offset of the
                        # anchor window = page key start o + anchor t
                        for oo in idx[r].get(rows[ui, si].tobytes(), ()):
                            o = oo - t
                            if o < 0:
                                continue
                            if min(n, len(K) - o) < MIN_WIN:
                                continue
                            a = (eps * pow(ui + 1, 27, 29)) % 29
                            if a < 2:
                                continue        # a=1: dukotah additive
                            cells[(o, a, si, eps)] = True
    best = None
    for (o, a, s, eps) in cells:
        L = min(n, len(K) - o)
        X = (a * ((C[:L] + eps * K[o:o + L]) % 29) + s) % 29
        txt = merged("".join([VAL[x] for x in X.tolist()]))
        legal, raw = hits_of(txt, page, (), skel)
        if best is None or (legal, raw, S.score_text(txt)) > \
                (best[0], best[1], best[3]):
            best = (legal, raw, (o, a, s, eps), S.score_text(txt), txt)
    return best, len(cells)


def plant(K, starts):
    """p56+p57 PT enciphered at NON-page-start key offsets; recovered
    through the identical inversion path. Pass: legal >= 3."""
    res = []
    # carrier p57 (PT == CT in V.flat). p56 rejected as plant carrier:
    # its CT is phi-prime ciphertext with skip-convention PT 84 != CT 85
    # runes — positional anchors would misalign (disclosed).
    for carrier, cells in (
            (57, ((starts[20] + 31, 7, 1, 13), (starts[33] + 7, 15, -1, 5),
                  (starts[5] + 13, 23, 1, 20))),):
        A = np.array(V.flat(57), dtype=np.int64)
        skel = S.skeleton(carrier)
        _, _, anchors = anchors_for(carrier)
        for (o, a, eps, s) in cells:
            L = min(len(A), len(K) - o)
            ainv = pow(a, 27, 29)
            C = (ainv * (A - s) - eps * K[o:o + L]) % 29
            best, ncells = scan_page(carrier, K, G["idx"], C=C.copy(),
                                     skel=skel, anchors=anchors)
            legal = best[0] if best else 0
            found = best and best[2] == (o, a, s, eps)
            res.append(f"  plant p{carrier} o={o} a={a} eps={eps:+d} "
                       f"s={s}: legal {legal} cell-recovered "
                       f"{bool(found)} ({'PASS >=3' if legal >= 3 else 'FAIL'})")
    return res


G = {}


def sweep_one(page):
    K = G["K"]
    idx = G["idx"]
    best, ncells = scan_page(page, K, idx)
    return dict(page=page, ncells=ncells,
                m=best[0] if best else 0,
                cell=best[2] if best else None,
                raw=best[1] if best else 0,
                txt=best[4] if best else "")   # FULL text: null shuffles it


def main():
    try:
        mp.set_start_method("fork")
    except RuntimeError:
        pass
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--budget", type=int, default=480)
    a = ap.parse_args()
    t0 = time.time()
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(WORK, exist_ok=True)
    rep = []
    K, starts = canon()
    assert len(K) == 13136, f"G2 FAIL len={len(K)}"
    N = sum(len(V.flat(n)) for n in UNSOLVED)
    assert N == 12956, f"G1 FAIL N={N}"
    tc = Counter()
    for p in sorted(S._blocks()):
        for d, _ in S.skeleton(p)["marks"]:
            tc["◆" + d] = tc.get("◆" + d, 0) + 1
    assert tc.get("◆4") == 129, f"G3 FAIL {tc}"
    assert sum(len(v) for v in PRE.values()) == 37, f"G4 FAIL {sum(len(v) for v in PRE.values())}"
    lengths = sorted({len(R) for v in PRE.values() for R in v})
    idx = build_index(K, lengths)
    G.update(K=K, idx=idx)
    nanch = sum(len(anchors_for(p)[2]) for p in UNSOLVED)
    rep.append(f"Gates PASS (canon 13,136; N=12,956; ◆4=129; preimages 37). "
               f"Anchors {nanch}; window lengths {lengths[0]}..{lengths[-1]}.")

    PF = os.path.join(WORK, "pages.jsonl")
    done = {}
    if os.path.exists(PF):
        for line in open(PF):
            r = json.loads(line)
            done[r["page"]] = r
    todo = [p for p in UNSOLVED if p not in done]
    if todo:
        with mp.Pool() as pool:
            with open(PF, "a") as f:
                for r in pool.imap_unordered(sweep_one, todo):
                    done[r["page"]] = r
                    f.write(json.dumps(r) + "\n")
                    f.flush()
                    print(f"  p{r['page']:>2}: cells {r['ncells']} "
                          f"m {r['m']} ({time.time()-t0:.0f}s)", flush=True)
    per_page = [done[p] for p in UNSOLVED]
    M = max(r["m"] for r in per_page)
    tot_cells = sum(r["ncells"] for r in per_page)
    rep.append(f"Inversion: {tot_cells} survivor cells; M = {M}; pages at "
               f"M: {[r['page'] for r in per_page if r['m'] == M and M]}")
    for r in per_page:
        if r["m"]:
            rep.append(f"  p{r['page']:>2}: m={r['m']} raw={r['raw']} "
                       f"cell(o,a,s,eps)={r['cell']}: {r['txt'][:50]}")

    best_txt = {r["page"]: r["txt"] for r in per_page}
    skels = {p: S.skeleton(p) for p in UNSOLVED}
    NULLF = os.path.join(WORK, "null_maxes.txt")
    null_maxes = ([int(x) for x in open(NULLF).read().split()]
                  if os.path.exists(NULLF) else [])
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
        if (d + 1) % 20 == 0:
            print(f"  null {d+1}/{D} ({time.time()-t0:.0f}s)", flush=True)
        if time.time() - t0 > a.budget:
            print(f"PARTIAL (null {len(null_maxes)}/{D}) — rerun",
                  flush=True)
            return
    beats = sum(1 for x in null_maxes if x >= M)
    p = (1 + beats) / (len(null_maxes) + 1)
    rep.append(f"Null of the max: hist "
               f"{dict(sorted(Counter(null_maxes).items()))}, beaten "
               f"{beats}/{len(null_maxes)}, p={p:.4f}")
    rep.append("Power plants (non-page-start offsets, scorer+inversion "
               "test):\n" + "\n".join(plant(K, starts)))
    verdict = ("AFFINE2-HIT — FLAG FOR OWNER REVIEW (nothing auto-certified)"
               if p < 0.05 else
               "AFFINE2-NULL — arbitrary-offset affine (a in 2..28, s in "
               "0..28, eps +-1, any key start) closed under the slot-"
               "aligned anchor shrink")
    rep.append(f"VERDICT: {verdict}")
    rep.append("DISCLOSURES: (1) anchor shrink: single-word cribs must "
               "fill a slot, MULTIWORD start at slot starts; mid-slot / "
               "mid-digraph occurrences invisible. (2) no interrupter/skip "
               "model; window >= 60; key = canon. (3) shuffle surrogates "
               "conservative. (4) length-3 anchors expect ~3.6e5 spurious "
               "survivors — null built on the same survivor-max structure. "
               f"(5) runtime {time.time()-t0:.0f} s.")
    with open(f"{OUT}/LANE_D_REPORT.md", "w") as f:
        f.write("# Campaign #25 Lane D (F3' arbitrary-offset affine) report\n\n"
                + "\n\n".join(rep) + "\n")
    print("\n".join(rep))


if __name__ == "__main__":
    main()
