"""Separator-skeleton constraint machinery — the adopted payoff of
campaign #21 (SKELETON-QUALIFIED, LEDGER row 21, PREREG 2f8c015):
`-` sits at plaintext word boundaries and ◆4 at sentence ends
(p56: 15/15 aligned in verified regions, p=8.9e-13; p57: 16/16 + 3/3).

Turns the ORACLE_PAGES ciphertext blocks into per-page crib-placement
constraints for decode scoring. Marks are stored in RUNE index space
(CT index of the rune the mark follows, null-inclusive); mapping to
LETTER space needs a candidate null mask (digraphs TH/NG/EO are 1 rune
= 2 letters, skip-null-F runes advance the rune counter only), so
letter positions are computed per candidate:

    skeleton(page)               raw dashes/marks/quotes/wraps (runes)
    letter_boundaries(skel, ns)  dash boundaries in letter space
    word_slots(skel, ns)         dash-delimited slots + wrap merges
    crib_placements(crib, p, ns) legal placements for one crib
    score_text(text)             merged quadgram+crib scorer (V2)
    skeleton_penalty(cand, p, ns) crib hits straddling a dash
    payoff()                     search-space shrinkage report

Owner rules honored: stipulation (line-final ◆3 + next-line initial
'-' = one ◆4, both marks removed); roman layer ◆4='.', ◆13='¶',
◆23='§'; merged alphabet K->C, V->U, Z->S, Q->C on every English-side
comparison. Line wraps split words WITHOUT dashes (p57 ground truth),
so dash-slots are mergeable across wrap positions — cribs may span
them; cribs may NEVER straddle a dash.
"""
import functools
import math
import os
import re

import core.validate as V
from core.cribs import REPR as CRIBS

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MD = os.path.join(ROOT, "docs", "ORACLE_PAGES.md")
QG = os.path.join(ROOT, "sources", "dukotah", "liber-primus", "data",
                  "english_quadgrams.txt")
MERGE = str.maketrans("KVZQ", "CUSS")
VAL = [g[1] for g in V.GEMATRIA]  # positional romanization per rune index
UNSOLVED = list(range(50)) + list(range(51, 56))
# Phrase cribs (ground truth p56/p57): these straddle word dashes BY
# DESIGN (DEEP WEB / AN END / HASHES TO) — exempt from the no-straddle
# constraint. All other CRIBS entries are single words.
MULTIWORD = {"DEEPWEB", "ANEND", "HASHESTO"}


@functools.lru_cache(maxsize=1)
def _blocks():
    txt = open(MD).read()
    out = {}
    for m in re.finditer(r"## p(\d+).*?\*\*Ciphertext\*\*[^\n]*\n+"
                         r"```[a-zA-Z]*\n(.*?)```", txt, re.S):
        out[int(m.group(1))] = m.group(2)
    return out


def _rune_seg(line):
    m = re.match(r"\s*\d+\s+(.*)", line)
    if not m:
        return None
    return re.split(r"\s{2,}=\s", m.group(1))[0].strip()


def skeleton(page):
    """Per-page separator skeleton in rune index (CT) space.

    dashes  : letter-independent rune idx the '-' follows
    marks   : (digit-class, rune idx) for ◆N tokens
    quotes  : (char, rune idx) for bare " / '
    wraps   : rune idx ending a line with NO dash (word may continue)
    n_runes : rune count of the page
    """
    dashes, marks, quotes, wraps = [], [], [], []
    r = 0
    pending_d3 = False
    for raw in _blocks()[page].splitlines():
        s = _rune_seg(raw)
        if s is None or s in ("&", "$", "§") or \
                not any(0x16A0 <= ord(c) <= 0x16FF for c in s):
            continue
        s = re.sub(r"⟦['\"]⟧(?=\s*[A-Za-z])", "", s)   # annotations
        s = re.sub(r"⟦(['\"])⟧", r"\1", s)             # legacy wrap
        s = re.sub(r"[A-Za-z]+", "", s)
        s = re.sub(r"\s*†.*$", "", s)
        if pending_d3:                                 # owner stipulation
            s = s[1:] if s.startswith("-") else s
            pending_d3 = False
        if "◆3" in s:
            s = s.replace("◆3", "◆4")
            pending_d3 = True
        s = s.replace("*", "").rstrip()
        i = 0
        last = None                                    # last rune idx in line
        last_tok = None                                # rune/dash/mark
        while i < len(s):
            ch = s[i]
            if 0x16A0 <= ord(ch) <= 0x16FF:
                last, last_tok = r, "rune"
                r += 1
                i += 1
            elif ch == "-":
                dashes.append(r - 1)
                last_tok = "dash"
                i += 1
            elif ch == "◆":
                m = re.match(r"◆(\d+)", s[i:])
                marks.append((m.group(1), r - 1))
                last_tok = "mark"
                i += len(m.group(0))
            elif ch in "\"'":
                quotes.append((ch, r - 1))
                i += 1
            else:
                i += 1
        if last is not None and last_tok == "rune":
            wraps.append(last)   # line ends on a rune, no dash: word may
                                 # continue across the wrap (p57 ground truth)
    return {"dashes": dashes, "marks": marks, "quotes": quotes,
            "wraps": wraps, "n_runes": r}


def _letter_lens(page):
    return [len(VAL[i]) for i in V.flat(page)]


def _cum(page, nulls=()):
    """cum[i] = letters emitted through rune i (skip-null)."""
    ns = set(nulls)
    out, t = [], 0
    for k, ln in enumerate(_letter_lens(page)):
        if k not in ns:
            t += ln
        out.append(t)
    return out


def letter_boundaries(skel, page, nulls=()):
    """Letter positions (last letter before the mark) for dashes and
    wraps under a candidate null mask."""
    cum = _cum(page, nulls)
    return ({cum[b] - 1 for b in skel["dashes"]},
            {cum[b] - 1 for b in skel["wraps"]})


def word_slots(skel, page, nulls=()):
    """Dash-delimited slots [(start_letter, length)] plus the wrap
    positions where adjacent slots may merge into one word."""
    bounds, wraps = letter_boundaries(skel, page, nulls)
    n = _cum(page, nulls)[-1]
    cuts = sorted(bounds | {n - 1})
    slots, start = [], 0
    for c in cuts:
        if c + 1 > start:
            slots.append((start, c + 1 - start))
        start = c + 1
    return slots, wraps


def crib_placements(crib, page, nulls=(), skel=None):
    """Count placements of `crib` (English, will be merged) that never
    straddle a dash except at wrap-mergeable positions. Phrase cribs
    (MULTIWORD) are exempt — no pruning for them."""
    skel = skel or skeleton(page)
    bounds, wraps = letter_boundaries(skel, page, nulls)
    n = _cum(page, nulls)[-1]
    c = crib.upper().translate(MERGE)
    L = len(c)
    if c in MULTIWORD:
        return max(0, n - L + 1)
    if L > n:
        return 0
    bad = bounds - wraps
    cnt = 0
    for o in range(n - L + 1):
        if not any(o <= b < o + L - 1 for b in bad):
            cnt += 1
    return cnt


@functools.lru_cache(maxsize=1)
def _qg():
    qg, tot = {}, 0
    with open(QG) as f:
        for line in f:
            w, c = line.split()
            qg[w] = int(c)
            tot += int(c)
    return qg, tot


def score_text(text):
    """Merged-alphabet quadgram + crib score (the #21-V2 gate scorer)."""
    qg, tot = _qg()
    floor = math.log10(0.01 / tot)
    t = re.sub(r"[^A-Z]", "", text.translate(MERGE))
    s = sum(math.log10(qg[t[i:i + 4]] / tot) if t[i:i + 4] in qg else floor
            for i in range(len(t) - 3))
    s /= max(1, len(t) - 3)
    merged = t.translate(MERGE)
    crib_hits = sum(1 for c in CRIBS if c in merged)
    return s + 0.5 * crib_hits / max(1, len(t)) * 100


def skeleton_penalty(candidate, page, nulls=(), skel=None):
    """Fraction of crib hits in `candidate` (merged) that straddle a
    non-mergeable dash boundary — 0.0 = skeleton-consistent decode."""
    skel = skel or skeleton(page)
    bounds, wraps = letter_boundaries(skel, page, nulls)
    bad = bounds - wraps
    c = candidate.upper().translate(MERGE)
    tot = ill = 0
    for crib in CRIBS:
        if crib in MULTIWORD:
            continue
        st = 0
        while True:
            o = c.find(crib, st)
            if o < 0:
                break
            tot += 1
            if any(o <= b < o + len(crib) - 1 for b in bad):
                ill += 1
            st = o + 1
    return ill / tot if tot else 0.0


def legal_occurrence(crib, candidate, page, nulls=(), skel=None):
    """True iff `crib` occurs in `candidate` at >=1 skeleton-legal
    placement (phrase cribs exempt — always legal)."""
    skel = skel or skeleton(page)
    c = candidate.upper().translate(MERGE)
    k = crib.upper().translate(MERGE)
    if k in MULTIWORD:
        return k in c
    st = 0
    while True:
        o = c.find(k, st)
        if o < 0:
            return False
        if not any(o <= b < o + len(k) - 1
                   for b in _bad(page, nulls, skel)):
            return True
        st = o + 1


@functools.lru_cache(maxsize=None)
def _bad_cached(page, nulls):
    skel = skeleton(page)
    bounds, wraps = letter_boundaries(skel, page, nulls)
    return frozenset(bounds - wraps)


def _bad(page, nulls, skel=None):
    return _bad_cached(page, tuple(sorted(nulls)))


def interrupter_sweep(page, expect, top=5):
    """Skeleton-pruned mirror of core.validate.brute_interrupters:
    enumerate null-combos x conventions, but rank candidates by crib
    hits counted ONLY at legal placements (legal_hits), then raw hits,
    then quadgram score. Returns ranked tuples
    (legal_hits, raw_hits, conv, nulls, text)."""
    import itertools
    import core.validate as V2
    ct = V2.flat(page)
    stream = V2.phi_prime_stream(len(ct))
    fpos = [t for t, c in enumerate(ct) if c == 0]
    skel = skeleton(page)
    out = []
    for r in range(len(fpos) + 1):
        for combo in itertools.combinations(fpos, r):
            cs = set(combo)
            for conv, fn in (("skip", V2.decode_skipnull),
                             ("hold", V2.decode_holdnull)):
                txt = V2.translit(
                    fn(ct, stream, [t in cs for t in range(len(ct))]))
                raw = sum(w in txt for w in expect)
                if raw == 0:
                    continue
                # hold convention emits a letter at nulls -> letter
                # space spans ALL runes (no skipped positions)
                eff = cs if conv == "skip" else ()
                legal = sum(
                    1 for w in expect
                    if legal_occurrence(w, txt, page, eff, skel))
                out.append((legal, raw, conv, tuple(sorted(cs)), txt))
    out.sort(key=lambda x: (-x[0], -x[1], -score_text(x[4])))
    return out[:top], out


def payoff(pages=None, out_csv=None):
    """Report-only: crib-placement search space, unconstrained vs
    skeleton-constrained, per crib x page. Returns median shrinkage."""
    import csv
    pages = pages or UNSOLVED
    rows, ratios = [], []
    for p in pages:
        skel = skeleton(p)
        n = _cum(p, ())[-1]
        for crib in CRIBS:
            if crib in MULTIWORD:
                continue
            L = len(crib)
            free = max(0, n - L + 1)
            fit = crib_placements(crib, p, (), skel=skel)
            if free:
                ratios.append(fit / free)
                rows.append(dict(page=p, crib=crib, free=free,
                                 constrained=fit, ratio=fit / free))
    if out_csv:
        os.makedirs(os.path.dirname(out_csv), exist_ok=True)
        with open(out_csv, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=["page", "crib", "free",
                                              "constrained", "ratio"])
            w.writeheader()
            w.writerows(rows)
    ratios.sort()
    return {"cells": len(ratios),
            "median_ratio": ratios[len(ratios) // 2] if ratios else None,
            "mean_ratio": sum(ratios) / len(ratios) if ratios else None,
            "zero_fraction": sum(1 for x in ratios if x == 0) / len(ratios)
            if ratios else None}


if __name__ == "__main__":
    r = payoff(out_csv=os.path.join(ROOT, "work", "skeleton_payoff",
                                    "payoff.csv"))
    print(f"cribs x unsolved pages: {r['cells']} cells; median "
          f"constrained/free = {r['median_ratio']:.3f}; mean "
          f"{r['mean_ratio']:.3f}; zero-placement fraction "
          f"{r['zero_fraction']:.3f} -> work/skeleton_payoff/payoff.csv")
