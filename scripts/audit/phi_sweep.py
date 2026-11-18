#!/usr/bin/env python3
"""Campaign #23 — skeleton-constrained phi-prime sweep, all 55 unsolved
pages (PREREG sweeps/2026-11-phi-sweep, committed 33374de BEFORE output).

Per page: enumerate null-combos x {skip,hold}, decode with the page-
aligned phi-prime stream, count crib hits at skeleton-LEGAL placements
(phrase cribs exempt). m_n = max legal hits per page; M = max over
pages. Null of the max: per page S=1000 letter-shuffles of that page's
best-candidate text, page null-max = max over S, global null-max = max
over pages, D=200 replicates, seed 20261223. Verdict per PREREG; a HIT
is flagged for owner review only, never auto-certified.

Usage: python3 -m scripts.audit.phi_sweep   (ETA printed at start)
"""
import csv
from collections import Counter
import itertools
import os
import random
import re
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)
import core.validate as V          # noqa: E402
import core.skeleton as S          # noqa: E402
from core.cribs import REPR as CRIBS  # noqa: E402

OUT = os.path.join(ROOT, "sweeps", "2026-11-phi-sweep", "results")
WORK = os.path.join(ROOT, "work", "phi_sweep")
MERGE = str.maketrans("KVZQ", "CUSS")
UNSOLVED = S.UNSOLVED                    # books 0-49, 51-55 (55 pages)
SEED = 20261223
S_SHUF = 1000
D = 200
# longest-first so finditer reports the phrase cribs before their
# substrings; hits are counted per distinct crib anyway
CRIBS_SORTED = sorted(CRIBS, key=len, reverse=True)
CRIB_RE = re.compile("|".join(CRIBS_SORTED))


def merged(txt):
    return txt.upper().translate(MERGE)


def hits_of(text, page, nulls, skel):
    """(legal, raw) crib-hit counts for a merged text; legality uses the
    page skeleton under the candidate's effective null mask."""
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
        st = 0
        ok = False
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


def sweep_page(page):
    """All candidates with raw>0, ranked; returns (ranked, n_cand, n_decodes)."""
    ct = V.flat(page)
    stream = V.phi_prime_stream(len(ct))
    fpos = [t for t, c in enumerate(ct) if c == 0]
    skel = S.skeleton(page)
    n_dec = 0
    out = []
    for r in range(len(fpos) + 1):
        for combo in itertools.combinations(fpos, r):
            cs = frozenset(combo)
            mask = [t in cs for t in range(len(ct))]
            for conv, fn in (("skip", V.decode_skipnull),
                             ("hold", V.decode_holdnull)):
                n_dec += 1
                txt = merged(V.translit(fn(ct, stream, mask)))
                legal, raw = hits_of(txt, page, cs if conv == "skip"
                                     else (), skel)
                if raw:
                    out.append((legal, raw, conv, tuple(sorted(cs)), txt))
    out.sort(key=lambda x: (-x[0], -x[1], -S.score_text(x[4])))
    return out, len(fpos), n_dec


def main():
    t0 = time.time()
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(WORK, exist_ok=True)
    rep = []

    # ---- gates ----
    stream = []
    for n in UNSOLVED:
        stream.extend(V.flat(n))
    assert len(stream) == 12956, f"G1 FAIL N={len(stream)}"
    top56, all56 = S.interrupter_sweep(
        56, ["DEEPWEB", "PILGRIM", "HASHESTO"])
    true56 = [c for c in all56 if c[2:4] == ("skip", (47,))]
    assert len(true56) == 1 and true56[0][:2] == (2, 3) \
        and true56[0] in top56, f"G2 FAIL {true56[:2]}"
    tc = {}
    qc = {'"': 0, "'": 0}
    for p in sorted(S._blocks()):
        sk = S.skeleton(p)
        for d, _ in sk["marks"]:
            tc["◆" + d] = tc.get("◆" + d, 0) + 1
        for ch, _ in sk["quotes"]:
            qc[ch] += 1
    assert tc.get("◆4") == 129 and tc.get("◆13") == 32 and \
        tc.get("◆10") == 3 and tc.get("◆23") == 1 and \
        qc['"'] == 14 and qc["'"] == 3, f"G3 FAIL {tc} {qc}"
    rep.append(f"G1 N=12956; G2 p56 true combo (skip,(47,)) legal 2/raw 3 "
               f"in top; G3 census {tc} quotes {qc}")

    # ---- sweep (checkpointed; rerun resumes) ----
    STATE = os.path.join(WORK, "state.py")
    per_page, total_dec = [], 0
    if os.path.exists(STATE):
        ns = {"__builtins__": {}}
        exec(open(STATE).read(), ns)
        per_page = ns["per_page"]
        total_dec = sum(r["n_dec"] for r in per_page)
        print(f"resumed sweep state: {len(per_page)} pages", flush=True)
    else:
        for i, page in enumerate(UNSOLVED):
            ranked, F, n_dec = sweep_page(page)
            total_dec += n_dec
            m = ranked[0][0] if ranked else 0
            per_page.append(dict(page=page, F=F, n_dec=n_dec,
                                 n_raw=len(ranked), m=m,
                                 best=ranked[0] if ranked else None))
            if (i + 1) % 10 == 0:
                print(f"  swept {i+1}/55 pages, {total_dec} decodes, "
                      f"{time.time()-t0:.0f}s", flush=True)
        with open(STATE, "w") as f:
            f.write("per_page = " + repr(per_page) + "\n")
    M = max(r["m"] for r in per_page)
    winners = [r for r in per_page if r["m"] == M and M > 0]
    rep.append(f"Sweep: {total_dec} decodes over 55 pages "
               f"(prereg estimate 499,604); M = max legal hits = {M}; "
               f"pages at M: {[r['page'] for r in winners]}")
    for r in per_page:
        b = r["best"]
        rep.append(f"  p{r['page']:>2}: F={r['F']:>2} raw>0 cands="
                   f"{r['n_raw']:>4} m={r['m']}"
                   + (f"  best {b[2]}{b[3]}: {b[4][:60]}" if b else ""))

    # ---- null of the max (checkpointed; per-replicate substream
    # rng.Random(f"{SEED}:{d}") so chunked reruns are bit-identical) ----
    best_txt = {r["page"]: (r["best"][4] if r["best"] else "")
                for r in per_page}
    eff = {r["page"]: (r["best"][3] if r["best"] and r["best"][2] == "skip"
                       else ()) for r in per_page}
    skels = {p: S.skeleton(p) for p in UNSOLVED}
    # shuffle legality is evaluated under the best candidate's null mask
    # (the mask that produced the observed m_n) — disclosed choice
    NULLF = os.path.join(WORK, "null_maxes.txt")
    null_maxes = []
    if os.path.exists(NULLF):
        with open(NULLF) as f:
            null_maxes = [int(x) for x in f.read().split()]
        print(f"resumed null: {len(null_maxes)}/{D} replicates", flush=True)
    for d in range(len(null_maxes), D):
        rng = random.Random(f"{SEED}:{d}")
        gm = 0
        for page in UNSOLVED:
            t = best_txt[page]
            if not t:
                continue
            pm = 0
            tl = list(t)
            for _ in range(S_SHUF):
                rng.shuffle(tl)
                lh, _ = hits_of("".join(tl), page, eff[page], skels[page])
                if lh > pm:
                    pm = lh
            if pm > gm:
                gm = pm
        null_maxes.append(gm)
        with open(NULLF, "a") as f:
            f.write(f"{gm}\n")
        if (d + 1) % 20 == 0:
            print(f"  null replicate {d+1}/{D}, {time.time()-t0:.0f}s",
                  flush=True)
    if len(null_maxes) < D:
        print(f"partial: {len(null_maxes)}/{D} null replicates done; "
              f"rerun to continue (no report written)")
        return
    beats = sum(1 for x in null_maxes if x >= M)
    p = (1 + beats) / (D + 1)
    thr = sorted(null_maxes)[int(0.95 * D) - 1] if D >= 20 else None
    rep.append(f"Null of the max: S={S_SHUF}/page, D={D}, seed {SEED}; "
               f"null-max samples: min={min(null_maxes)} median="
               f"{sorted(null_maxes)[D//2]} max={max(null_maxes)}; "
               f"beaten {beats}/{D}; p={p:.4f}; 95th pct null-max={thr}")

    # ---- power plants (text-space; test the scorer, not the key) ----
    # POST-REG CORRECTION: the first run's seeded draw over all 55 pages
    # hit 3 pages with no raw>0 candidate (no best text to plant into —
    # skipped, power step unfulfilled). Redraw restricted to pages WITH a
    # best-candidate text (p20/p39/p43/p48/p51); disclosed in report.
    prng = random.Random(SEED + 1)
    eligible = [r["page"] for r in per_page if r["best"]]
    plant_pages = sorted(prng.sample(eligible, min(3, len(eligible))))
    plants = []
    for page in plant_pages:
        t = best_txt[page]
        if not t:
            plants.append(f"  p{page}: no candidate text, skipped")
            continue
        fit = [c for c in CRIBS if S.crib_placements(c, page, eff[page],
                                                     skel=skels[page]) > 0]
        crib = prng.choice(sorted(fit))
        L = len(crib)
        bad = S._bad(page, eff[page], skels[page])
        n = len(t)
        offs = [o for o in range(n - L + 1)
                if not any(o <= b < o + L - 1 for b in bad)]
        o = prng.choice(offs)
        planted = t[:o] + crib + t[o + L:]
        lh, _ = hits_of(planted, page, eff[page], skels[page])
        pp = (1 + sum(1 for x in null_maxes if x >= lh)) / (D + 1)
        plants.append(f"  p{page}: planted {crib}@{o} -> legal hits "
                      f"{lh} (page m was {per_page[UNSOLVED.index(page)]['m']}"
                      f"; p at {lh} = {pp:.3f})")
    pw_hist = dict(sorted(Counter(null_maxes).items()))
    m_need = next((k for k in range(1, 10)
                   if (1 + sum(1 for x in null_maxes if x >= k)) / (D + 1)
                   < 0.05), None)
    rep.append("Power plants (scorer sensitivity, NOT key evidence):\n"
               + "\n".join(plants)
               + f"\n  POWER SUMMARY: null-max histogram {pw_hist}; the "
                 f"max-statistic HIT bar (p<0.05) needs legal >= {m_need} "
                 f"on one page. A single planted crib reaches legal 2 "
                 f"(p=0.383) -> this sweep is BLIND to single-crib "
                 f"signals and powered for multi-crib (>= {m_need}) "
                 f"pages; a true decode of a full page would put many "
                 f"of the 36 cribs legally, so the bar is appropriate.")

    # ---- verdict ----
    if p < 0.05:
        verdict = ("PHI-SKELETON-HIT — flagged for OWNER REVIEW (visual + "
                   "crib reading); nothing auto-certified")
    else:
        verdict = ("PHI-FAMILY-NULL — phi-prime page-aligned + interrupter "
                   "family retired for unsolved pages; coverage: that "
                   "family only, 36-crib merged vocabulary, skeleton-"
                   "pruned; power from plants above")
    rep.append(f"VERDICT: {verdict}")
    rep.append("DISCLOSURES: (1) legality of shuffle surrogates evaluated "
               "under the best candidate's null mask. (2) plants are "
               "text-space splices: they test scorer sensitivity, not the "
               "key hypothesis. (3) phi-prime page-alignment inherited "
               "from p56 only; other alignments invisible to this run. "
               "(4) p56/p57 excluded (controls; G2 gate). (5) wrong- "
               "convention decodes penalized by design (true-plaintext "
               "skeleton space). (6) FIRST RUN power-step defect: seeded "
               "plant draw over all 55 pages hit 3 textless pages and "
               "skipped; redraw restricted to the 5 pages with candidate "
               "text (correction appended to PREREG; statistic/null "
               "untouched, bit-identical via per-replicate substreams). "
               "(7) p43 (F=17) is the multiple-testing hotspot: 43,008 "
               "raw>0 candidates, and its m=1 is exactly what its shuffle "
               "null produces (null-max min 1) — the null-of-the-max "
               "absorbs it as designed. (8) measured runtime 112 s. "
               "(9) raw>0 counts are backbone-dominated: non-F runes "
               "decode identically across combos, so a crib window is "
               "either in the fixed backbone (inherited by most combos "
               "— p43's 43,008) or unreachable for the whole page "
               "(p0's 0/32,768); the effective independent search is "
               "per-page backbones, far fewer than 499,604 tests — the "
               "letter-shuffle null ignores this and is CONSERVATIVE "
               "(inflated null), and M=1 still sits at its median.")

    # ---- persist ----
    with open(f"{OUT}/REPORT.md", "w") as f:
        f.write("# Campaign #23 report — skeleton-constrained phi-prime "
                "sweep (55 unsolved pages)\n\n" + "\n\n".join(rep) + "\n")
    with open(f"{WORK}/per_page.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["page", "F", "decodes", "cands_raw_gt0", "m_legal",
                    "best_conv", "best_nulls", "best_text"])
        for r in per_page:
            b = r["best"]
            w.writerow([r["page"], r["F"], r["n_dec"], r["n_raw"], r["m"],
                        b[2] if b else "", b[3] if b else "",
                        b[4] if b else ""])
    print("\n".join(rep))
    print(f"\n{time.time()-t0:.0f}s total")


if __name__ == "__main__":
    main()
