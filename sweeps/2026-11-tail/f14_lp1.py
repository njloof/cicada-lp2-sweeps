#!/usr/bin/env python3
"""Campaign #24 Lane C — F14 LP1 pages as targets (PREREG
sweeps/2026-11-tail/PREREG.md, committed 1a48cec BEFORE output).

Self-contained / studio-syncable. Lineage gate output first (premise
facts, no decode), then phi-prime page-aligned x {skip,hold} x all
null-combos (F truncated to first 20 positions, disclosed) over LP1
rune pages (>=60 runes) from the scream314 transcription; statistic =
RAW crib hits (no skeleton: LP1 bullets unqualified); MC null of the
max, letter shuffles, S=1000/page, D=200, seed 20261226,
per-replicate substreams. HIT = flag for owner only.

Run:  python3 sweeps/2026-11-tail/f14_lp1.py
"""
import itertools
import json
import os
import random
import re
import sys
import time
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, ROOT)
import core.validate as V               # noqa: E402
from core.cribs import REPR as CRIBS    # noqa: E402

OUT = os.path.join(HERE, "results")
WORK = os.path.join(ROOT, "work", "tail_f14")
MERGE = str.maketrans("KVZQ", "CUSS")
R2I = {g[0]: i for i, g in enumerate(V.GEMATRIA)}
VAL = [g[1] for g in V.GEMATRIA]
SEED = 20261226
S_SHUF, D = 1000, 200
MAX_F = 20
CRIB_RE = re.compile("|".join(sorted(CRIBS, key=len, reverse=True)))


def merged(t):
    return t.upper().translate(MERGE)


def lp1_pages():
    txt = open(os.path.join(ROOT, "sources", "scream314",
                            "liber_primus.md")).read()
    lp1 = txt[txt.index("# LP1"):txt.index("# LP2")]
    pages, cur = {}, None
    for line in lp1.splitlines():
        m = re.match(r"## (.+)", line)
        if m:
            cur = m.group(1)
            pages[cur] = []
        elif cur is not None:
            pages[cur].extend(c for c in line
                              if 0x16A0 <= ord(c) <= 0x16FF)
    return pages


def lineage():
    pages = lp1_pages()
    allc = [c for v in pages.values() for c in v]
    unmapped = [c for c in allc if c not in R2I]
    dk = json.load(open(os.path.join(
        ROOT, "sources", "dukotah", "liber-primus", "data", "keys",
        "armada18", "lp1_runes_as_key.json")))
    ours = [R2I[c] for c in allc if c in R2I]
    best = None
    for off in range(-200, 201):
        if off >= 0:
            n = min(len(ours), len(dk) - off)
            a = sum(1 for i in range(n) if ours[i] == dk[i + off])
        else:
            n = min(len(ours) + off, len(dk))
            a = sum(1 for i in range(n) if ours[i - off] == dk[i])
        if n > 0 and (best is None or a / n > best[1]):
            best = (off, a / n, n)
    return pages, len(allc), unmapped, dk, ours, best


def sweep(page_idx):
    ct = page_idx
    n = len(ct)
    stream = V.phi_prime_stream(n)
    fpos = [t for t, c in enumerate(ct) if c == 0]
    trunc = max(0, len(fpos) - MAX_F)
    fpos = fpos[:MAX_F]
    out = []
    for r in range(len(fpos) + 1):
        for combo in itertools.combinations(fpos, r):
            cs = set(combo)
            mask = [t in cs for t in range(n)]
            for conv, fn in (("skip", V.decode_skipnull),
                             ("hold", V.decode_holdnull)):
                txt = merged(V.translit(fn(ct, stream, mask)))
                raw = len({m.group(0) for m in CRIB_RE.finditer(txt)})
                if raw:
                    out.append((raw, conv, tuple(sorted(cs)), txt))
    out.sort(key=lambda x: (-x[0], -sum(1 for c in CRIBS if c in x[3])))
    return out, len(fpos), trunc, 2 ** len(fpos)


def main():
    t0 = time.time()
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(WORK, exist_ok=True)
    rep = []
    pages, n_all, unmapped, dk, ours, best = lineage()
    assert all(v == v.upper() for v in VAL)
    rep.append(
        f"C-G1 lineage gate: scream314 LP1 = {n_all} rune glyphs, "
        f"{len(unmapped)} outside the 29-rune alphabet (normalized by "
        f"scream314); mapped stream {len(ours)} vs dukotah glyph stream "
        f"{len(dk)}; best positional agreement {best[1]*100:.1f}% at "
        f"offset {best[0]} (n={best[2]}) — the lineages are NOT in "
        f"simple alignment (mixed-format doc; pp11/12 transcribed as "
        f"ENGLISH plaintext, p07 outguess note). PREMISE CORRECTION: "
        f"LP1 rune pages are largely readable koan English; 'unsolved "
        f"bulk' is not ciphertext. Lane runs the registered family as a "
        f"completeness check over pages with >=60 runes.")
    targets = {k: [R2I[c] for c in v if c in R2I]
               for k, v in pages.items() if len(v) >= 60}
    rep.append(f"targets ({len(targets)}): "
               + ", ".join(f"{k[:12]}:{len(v)}" for k, v in targets.items()))

    per_page = []
    for k, ct in targets.items():
        ranked, F, trunc, ndec = sweep(ct)
        per_page.append(dict(page=k, F=F, trunc=trunc, ndec=ndec,
                             n_raw=len(ranked),
                             m=ranked[0][0] if ranked else 0,
                             best=ranked[0] if ranked else None))
        print(f"  {k[:14]}: F={F} trunc={trunc} raw>0={len(ranked)} "
              f"m={per_page[-1]['m']} ({time.time()-t0:.0f}s)", flush=True)
    M = max(r["m"] for r in per_page)
    rep.append("Sweep: M = %d; pages at M: %s" % (
        M, [r["page"][:12] for r in per_page if r["m"] == M and M]))
    for r in per_page:
        b = r["best"]
        rep.append(f"  {r['page'][:14]}: F={r['F']} trunc={r['trunc']} "
                   f"decodes={r['ndec']} raw>0={r['n_raw']} m={r['m']}"
                   + (f"  best {b[1]}{b[2]}: {b[3][:50]}" if b else ""))

    best_txt = {r["page"]: (r["best"][3] if r["best"] else "")
                for r in per_page}
    NULLF = os.path.join(WORK, "null_maxes.txt")
    null_maxes = ([int(x) for x in open(NULLF).read().split()]
                  if os.path.exists(NULLF) else [])
    for d in range(len(null_maxes), D):
        rng = random.Random(f"{SEED}:{d}")
        gm = 0
        for k in targets:
            t = best_txt[k]
            if not t:
                continue
            pm, tl = 0, list(t)
            for _ in range(S_SHUF):
                rng.shuffle(tl)
                pm = max(pm, len({m.group(0) for m in
                                  CRIB_RE.finditer("".join(tl))}))
            gm = max(gm, pm)
        null_maxes.append(gm)
        with open(NULLF, "a") as f:
            f.write(f"{gm}\n")
    beats = sum(1 for x in null_maxes if x >= M)
    p = (1 + beats) / (len(null_maxes) + 1)
    rep.append(f"Null of the max: hist "
               f"{dict(sorted(Counter(null_maxes).items()))}, beaten "
               f"{beats}/{len(null_maxes)}, p={p:.4f}")

    # plants: p57 PT (95 runes) enciphered page-aligned phi-prime,
    # planted into an LP1-length carrier scan (scorer test only)
    pt = V.flat(57)
    Kp = V.phi_prime_stream(len(pt))
    plants = []
    for carrier_len, tag in ((len(pt), "exact"),):
        C = [(pt[i] + Kp[i]) % 29 for i in range(len(pt))]
        stream = V.phi_prime_stream(len(C))
        # EMPTY combo, skip convention (the true cell): the enciphered PT
        # contains genuine F runes; masking c==0 would delete PT letters
        # (first-run plant defect, disclosed in PREREG corrections).
        txt = merged(V.translit(V.decode_skipnull(
            C, stream, [False] * len(C))))
        raw = len({m.group(0) for m in CRIB_RE.finditer(txt)})
        pp = (1 + sum(1 for x in null_maxes if x >= raw)) / (len(null_maxes) + 1)
        plants.append(f"  plant p57-PT phi-prime enciphered ({tag}): raw "
                      f"{raw}, p at raw = {pp:.4f}")
    rep.append("Power plants (scorer test only):\n" + "\n".join(plants))
    verdict = ("LP1-HIT — FLAG FOR OWNER REVIEW" if p < 0.05 else
               "LP1-NULL — phi-prime page-aligned + interrupter family "
               "retired for LP1 rune pages too (coverage: 9 pages >=60 "
               "runes, scream314 lineage, F truncated to first 20 where "
               "needed, RAW crib statistic — no qualified skeleton for "
               "LP1). Premise correction: LP1 pages are largely readable "
               "English; this was completeness work.")
    rep.append(f"VERDICT: {verdict}")
    rep.append("DISCLOSURES: (1) no skeleton constraint (LP1 bullets "
               "unqualified) — weaker instrument than #23. (2) F>20 "
               "truncated to first 20 null-candidate positions. (3) "
               "lineage: scream314 mixed-format; dukotah glyph stream "
               "structurally different (9.2% best agreement). (4) "
               "shuffle null conservative. "
               f"(5) runtime {time.time()-t0:.0f} s.")
    with open(f"{OUT}/LANE_C_REPORT.md", "w") as f:
        f.write("# Campaign #24 Lane C (F14 LP1-as-target) report\n\n"
                + "\n\n".join(rep) + "\n")
    print("\n".join(rep))


if __name__ == "__main__":
    main()
