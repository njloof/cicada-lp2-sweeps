#!/usr/bin/env python3
"""Campaign #17 — language triage (PREREG sweeps/2026-11-langtriage).

S1 word-length histogram, S2 short-word signature, S3 apostrophe position
class, S4 chi-square vs in-book English reference (solved p56/p57) under
a permutation null. Deterministic + one MC (D=20,000, seed 20261205).

Usage: python3 -I scripts/audit/lang_triage.py
"""
import os
import random
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
sys.path.insert(0, ROOT)
from insert_transcriptions import load_pages  # noqa: E402

MD = os.path.join(ROOT, "docs", "ORACLE_PAGES.md")
OUT = os.path.join(ROOT, "sweeps", "2026-11-langtriage", "results")
UNSOLVED = [p for p in range(58) if p not in (50, 56, 57)]
BINS = [(1, 1), (2, 2), (3, 3), (4, 6), (7, 99)]
SEED = 20261205
D = 20_000


def words_of(seg):
    """krisyotam segment -> words (split on - and . and /), stripped of
    owner marks; apostrophes kept inside words for S3."""
    seg = re.sub(r"◆\d+\*?|\*|⟦[^⟧]*⟧|/|///|//", "", seg)
    toks = re.split(r"[-.]", seg)
    return [t for t in toks if t.strip()]


def hist(ws):
    n = len(ws)
    return [sum(1 for w in ws if lo <= len(w) <= hi) / n for lo, hi in BINS], n


def main():
    os.makedirs(OUT, exist_ok=True)
    base = load_pages()
    md = open(MD).read()

    # unsolved words (baseline krisyotam + owner inline quotes/apostrophes
    # are in the doc blocks; S1/S2 ride the baseline separators; S3 uses
    # the owner blocks where ' appears)
    uw = []
    for p in UNSOLVED:
        for seg in base.get(p, []):
            if seg.strip() in ("&", "$", "§"):
                continue
            uw.extend(words_of(seg))
    # G1 cross-pin: campaign #11 separator geometry EXACT (its 2,928-word
    # count predates the tail relabel — pinned separators instead; amended
    # pre-output, see PREREG)
    dash = sum(s.count("-") for p in UNSOLVED for s in base.get(p, []))
    dots = sum(s.count(".") for p in UNSOLVED for s in base.get(p, []))
    assert dash == 2729 and dots == 173, f"G1: dash {dash} dots {dots}"
    from core.validate import flat
    assert sum(len(flat(n)) for n in range(56) if n != 50) == 12956, "G3"

    # reference: solved plaintext words from the Plaintext blocks
    ref = []
    for pat in (r"AN END\nWITHIN THE DEEP WEB THERE EXISTS A PAGE THAT "
                r"HASHES TO.*?SEEK OUT THIS PAGE",
                r"Parable : like the instar.*?emerge\."):
        m = re.search(pat, md, re.S)
        txt = m.group(0)
        txt = re.sub(r"\[the five hex lines[^\]]*\]", "", txt)
        txt = re.sub(r"[.:]", " ", txt)
        ref.extend(w for w in re.split(r"\s+", txt) if w.isalpha())
    assert len(ref) >= 40, f"G2: ref n={len(ref)}"

    hu, nu = hist(uw)
    hr, nr = hist(ref)
    f1 = sum(1 for w in uw if len(w) == 1) / nu
    f2 = sum(1 for w in uw if len(w) <= 2) / nu
    rf1 = sum(1 for w in ref if len(w) == 1) / nr
    rf2 = sum(1 for w in ref if len(w) <= 2) / nr

    # S3 apostrophe position class from owner blocks
    apos = {"initial": 0, "medial": 0, "final": 0}
    for p in range(58):
        img = f"![p{p}](img/oracle/pages/p{p:02d}.jpg)"
        i = md.find(img)
        if i < 0:
            continue
        o = md.find("```", md.find("**Ciphertext**", i))
        c = md.find("```", o + 3)
        for l in md[o:c].split("\n"):
            l = l.replace("⟦'⟧", "'")  # machine-confirmed annotation counts
            for w in re.findall(r"\S*'\S*", l):
                w2 = w.strip("'")
                if w.startswith("'") and w2:
                    apos["initial"] += 1
                elif w.endswith("'") and w2:
                    apos["final"] += 1
                elif "'" in w2:
                    apos["medial"] += 1

    # S4 permutation chi-square (pooled relabel)
    cu = [sum(1 for w in uw if lo <= len(w) <= hi) for lo, hi in BINS]
    cr = [sum(1 for w in ref if lo <= len(w) <= hi) for lo, hi in BINS]
    pooled = [a + b for a, b in zip(cu, cr)]
    N = nu + nr

    def chi(a, b):
        s = 0.0
        for k in range(5):
            e1 = pooled[k] * nu / N
            e2 = pooled[k] * nr / N
            if e1:
                s += (a[k] - e1) ** 2 / e1
            if e2:
                s += (b[k] - e2) ** 2 / e2
        return s

    obs = chi(cu, cr)
    rng = random.Random(SEED)
    labels = [0] * nu + [1] * nr
    wl = [next(k for k, (lo, hi) in enumerate(BINS) if lo <= len(w) <= hi)
          for w in uw + ref]
    ge = 0
    for _ in range(D):
        rng.shuffle(labels)
        a = [0] * 5
        b = [0] * 5
        for lab, k in zip(labels, wl):
            (a if lab == 0 else b)[k] += 1
        if chi(a, b) >= obs - 1e-12:
            ge += 1
    p = (ge + 1) / (D + 1)
    verdict = "CONSISTENT-English" if p > 0.05 else "DEVIANT"

    rep = [
        "# Campaign #17 report — language triage\n",
        f"\nG1 separators EXACT (2,729 '-', 173 '.'); unsolved words "
        f"n={nu}; G2 reference n={nr} solved-page English words; G3 PASS",
        f"\n## S1 word-length histogram bins 1/2/3/4-6/7+",
        f"\nunsolved: {[f'{x:.1%}' for x in hu]}  mean "
        f"{sum(len(w) for w in uw)/nu:.2f}",
        f"\nEnglish ref : {[f'{x:.1%}' for x in hr]}",
        f"\n## S2 short words: unsolved f1={f1:.1%} f2<=2={f2:.1%} | "
        f"English ref f1={rf1:.1%} f2<=2={rf2:.1%}",
        f"\n## S3 apostrophe class (owner-marked): {apos} — medial/final >0 "
        "refutes Latin (Latin has no apostrophes)",
        f"\n## S4 permutation chi-square: obs={obs:.2f} p={p:.4f} "
        f"(D={D}, seed {SEED}) → **{verdict}** (low-power disclosed: "
        f"reference n={nr})",
    ]
    with open(f"{OUT}/REPORT.md", "w") as f:
        f.write("\n".join(rep) + "\n")
    print("\n".join(rep))


if __name__ == "__main__":
    main()
