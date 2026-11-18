#!/usr/bin/env python3
"""Punctuation census on the TEXT channel (campaign #21 step 1; owner
direction 2026-11-17: "We shouldn't have to depend on the images, right?
We have dots noted for every page in our transcription.").

Source: the fenced **Ciphertext** blocks of docs/ORACLE_PAGES.md
(krisyotam verbatim + owner-confirmed marks). Descriptive tabulation, not
a hypothesis test - no PREREG (red_census precedent).

Per page line, rune segment only (before the roman `=`):
  * strip line number, `*` red markers, `◆N` lattice tokens (counted
    separately with the same position classes), `⟦'⟧`/`⟦"⟧` quote marks,
    trailing annotations, `/` line-end, `&$§` standalone ornament lines;
  * dash-split into words; classify every `.` / quote by position:
      medial   between two runes inside a dash-word  (apostrophe-like)
      final    end of a dash-word
      initial  start of a dash-word
      alone    a dash-word consisting of the mark alone (word slot)
      lineend  final mark of the line's last word
  * record dash-word lengths (crib-placement skeleton for #21).

Output (gitignored): work/punct_census/text_census.csv + console
summary. Image-side raised-vs-mid probing stays oracle-gated (round #6)
and is only needed for marks absent from the transcription.

Usage: python3 scripts/audit/punct_text_census.py
"""
import csv
import os
import re
from collections import Counter, defaultdict

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
MD = os.path.join(ROOT, "docs", "ORACLE_PAGES.md")
OUT = os.path.join(ROOT, "work", "punct_census")
BOOK = list(range(50)) + list(range(51, 58))


def rune_segment(line):
    """Strip line number and roman segment; return rune-side string or None."""
    m = re.match(r"\s*\d+\s+(.*)", line)
    if not m:
        return None
    s = m.group(1)
    s = re.split(r"\s{2,}=\s", s)[0]          # cut roman segment
    return s


def classify(words, mark):
    """Position classes of `mark` within dash-words (list of rune strings)."""
    cls = []
    for wi, w in enumerate(words):
        n = w.count(mark)
        for _ in range(n):
            if w == mark:
                cls.append("alone")
            elif w.startswith(mark) and w.endswith(mark) and len(w) > 1:
                cls.append("medial")
            elif w.startswith(mark):
                cls.append("initial")
            elif w.endswith(mark):
                cls.append("final")
            else:
                cls.append("medial")
    return cls


def main():
    os.makedirs(OUT, exist_ok=True)
    txt = open(MD).read()
    blocks = {}
    for m in re.finditer(r"## p(\d+).*?\*\*Ciphertext\*\*[^\n]*\n+```[a-zA-Z]*"
                         r"\n(.*?)```", txt, re.S):
        blocks[int(m.group(1))] = m.group(2)
    assert sorted(blocks) == list(range(58)), f"block set mismatch: " \
        f"{len(blocks)} (p50 table block parsed but skipped below)"

    rows = []
    tot = Counter()
    per_page = defaultdict(Counter)
    plain_dots = Counter()
    latt_page = Counter()
    wlen = Counter()
    for p in BOOK:
        pending_d3 = False
        for ln, raw in enumerate(blocks[p].splitlines()):
            if not raw.strip():
                continue
            s = rune_segment(raw)
            if s is None:
                continue
            s = s.strip()
            if s in ("&", "$", "§"):
                continue
            if not any(0x16A0 <= ord(c) <= 0x16FF for c in s):
                continue  # annotation/decimal-block lines, no runes
            # quote marks: BARE " and ' in the rune segment (owner p53
            # example 2026-11-17: bare marks on p6/7/21/22/35/40/41/42/43/53)
            # plus legacy ⟦⟧-wrapped ones; drop ⟦⟧ ANNOTATIONS (followed by
            # Latin letters, e.g. p42 '⟦"⟧pos TBD' which duplicates the
            # bare mark on the same line), then strip Latin annotation text.
            s = re.sub(r"⟦['\"]⟧(?=\s*[A-Za-z])", "", s)
            s = re.sub(r"⟦(['\"])⟧", r"\1", s)
            s = re.sub(r"[A-Za-z]+", "", s)
            quotes = re.findall(r"['\"]", s)
            plain_dots[p] += s.count(".")        # krisyotam verbatim dots
            # OWNER STIPULATION 2026-11-17 (clarified): line-final ◆3 + the
            # NEXT line's initial '-' TOGETHER render one ◆4: BOTH marks
            # are removed and replaced by a single sentence dot. (p5 L5->L6,
            # p11 L11->L12; roman already shows '.'). Stipulated, not
            # measured.
            if pending_d3:
                s = s[1:] if s.startswith("-") else s
                pending_d3 = False
            if "◆3" in s:
                s = s.replace("◆3", "◆4")
                pending_d3 = True
            latt = Counter(re.findall(r"◆(\d+)", s))
            # roman-layer mapping (ORACLE note): ◆4->'.' (#16 T1),
            # ◆13->¶, ◆23->§; other ◆N keep their own class
            s = re.sub(r"◆4(?!\d)", ".", s)
            s = re.sub(r"◆13(?!\d)", "¶", s)
            s = re.sub(r"◆23(?!\d)", "§", s)
            s = re.sub(r"◆\d+", "◈", s)
            s = s.replace("*", "")               # red marker
            s = re.sub(r"\s*†.*$", "", s)        # trailing dagger annotations
            s = s.replace("/", "").strip()
            if not s:
                continue
            words = s.split("-")
            for w in words:
                clean = re.sub(r"[.'\"0-9]", "", w)
                if clean:
                    wlen[len(clean)] += 1
            for mark, cnt in ((".", s.count(".")), ("'", s.count("'")),
                              ('"', s.count('"'))):
                if not cnt:
                    continue
                for c in classify(words, mark):
                    rows.append(dict(page=p, line=ln + 1, mark=mark, pos=c))
                    tot[f"{mark}:{c}"] += 1
                    per_page[p][f"{mark}:{c}"] += 1
            latt_page[p] += sum(latt.values())
            for d, k in sorted(latt.items()):
                rows.append(dict(page=p, line=ln + 1, mark=f"◆{d}",
                                 pos=f"lattice-token x{k}"))
                tot[f"◆{d}"] += k
            for q in quotes:
                tot[f"quote{q}"] += 1

    with open(f"{OUT}/text_census.csv", "w", newline="") as f:
        wr = csv.DictWriter(f, fieldnames=["page", "line", "mark", "pos"])
        wr.writeheader()
        wr.writerows(rows)

    print(f"pages: {len(BOOK)}  marks+tokens: {len(rows)}  "
          f"-> work/punct_census/text_census.csv\n")
    # cross-check: krisyotam verbatim file. The owner's ◆-pass REPLACED
    # krisyotam `.` per cluster class (p3: 3 file dots -> 3 ◆13), so the
    # accounting is file_dots = plain + all ◆N tokens; residual = dots the
    # block neither kept plain nor ◆-marked (channel incompleteness).
    kris = open(os.path.join(ROOT, "sources", "dukotah", "liber-primus",
                             "data", "krisyotam_runes.txt")).read()
    kblocks = [b for b in kris.split("%")]
    kdot = {BOOK[bi]: b.count(".") for bi, b in enumerate(kblocks)
            if bi < len(BOOK)}
    lat_tot = Counter({int(k[1:]): v for k, v in tot.items() if k.startswith("◆")})
    n_lat = sum(lat_tot.values())
    resid = {p: kdot[p] - plain_dots[p] - latt_page[p] for p in BOOK
             if kdot[p] - plain_dots[p] - latt_page[p] != 0}
    print(f"◆ tokens by class: {dict(sorted(lat_tot.items()))}")
    print(f"krisyotam file dots: {sum(kdot.values())} = block plain "
          f"{sum(plain_dots.values())} + ◆ tokens {n_lat} + residual "
          f"{sum(resid.values())}; residual per page: "
          f"{resid if resid else 'none'}")
    print("dot/quote/◆ position classes (◆4 folded to '.':",
          "krisyotam-verbatim + ◆4):")
    for k in sorted(tot):
        print(f"  {k:14s} {tot[k]}")
    print("\nper-page dot totals (page: dots medial/final/initial/alone):")
    for p in BOOK:
        d = per_page[p]
        n = sum(v for k, v in d.items() if k.startswith("."))
        if n:
            print(f"  p{p:02d}: {n:3d}  " + " ".join(
                f"{k.split(':')[1][:4]}={v}" for k, v in sorted(d.items())
                if k.startswith(".")))
    ndot = sum(v for k, v in tot.items() if k.startswith("."))
    pages_with = sum(1 for p in BOOK if any(k.startswith(".")
                                            for k in per_page[p]))
    print(f"\ntotal inline dots (rune segments, ◆4->'.' folded): {ndot} on "
          f"{pages_with}/{len(BOOK)} pages")
    print("dash-word length histogram:", dict(sorted(wlen.items())))


if __name__ == "__main__":
    main()
