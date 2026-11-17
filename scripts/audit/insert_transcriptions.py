#!/usr/bin/env python3
"""Insert per-page ciphertext blocks into docs/ORACLE_PAGES.md (owner request
2026-11-17: full ciphertext with punctuation + '*' on red next to every page).

Edit-based and idempotent: replaces an existing **Ciphertext** block between
each page's image line and its **Notes:** line; never regenerates the file,
never touches owner notes.

Sources:
- runes: sources/dukotah/liber-primus/data/krisyotam_runes.txt (BOOK map)
- red spans: owner-confirmed lines (ORACLE_PAGES notes, F4, S-answers)
- punctuation: owner-confirmed image-only marks + work/scratch/punct_census_v2.json
- p50 table: scream314 compilation (via pinned dukotah clone)

Usage: python3 scripts/audit/insert_transcriptions.py

QUEUED (owner request 2026-11-17, DEFERRED until owner completes the full
annotation pass on all 58 pages): append to each runic line in the fenced
block its Romanization using the corpus Gematria table (core.validate TRANS:
0:F 1:U 2:TH 3:O 4:R 5:C 6:G 7:W 8:H 9:N 10:I 11:J 12:EO 13:P 14:X 15:S
16:T 17:B 18:E 19:M 20:L 21:NG 22:OE 23:D 24:A 25:AE 26:Y 27:IA 28:EA),
e.g. as a trailing "  = U TH ..." after the runes; non-runic symbols
(`-` `.` `/` `*` `◆N` `//` `///` quotes) pass through unchanged. Sync rule:
Romanization is derived from the rune text, so it must be regenerated
whenever a line changes — annotate-protected (◆) pages included, but only
the trailing roman segment may be rewritten, never the owner's runes/notes.
"""
import json
import os
import re

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
KRIS = os.path.join(ROOT, "sources", "dukotah", "liber-primus", "data",
                    "krisyotam_runes.txt")
MD = os.path.join(ROOT, "docs", "ORACLE_PAGES.md")
CENSUS = os.path.join(ROOT, "work", "scratch", "punct_census_v2.json")

BOOK = list(range(50)) + list(range(51, 56)) + [56, 57]

# owner-confirmed red head words: page -> [(1-based line, n_words or None=all)]
HEADS = {
    0: [(1, 1)], 3: [(1, 1), (7, 1)], 6: [(5, 4)], 8: [(1, 2)],
    15: [(1, 1), (6, 1)], 23: [(1, 1)], 27: [(1, 1)], 33: [(1, 1), (6, 2)],
    37: [(1, 1)], 39: [(7, 1)], 40: [(1, 2)], 54: [(1, 1)],
}
# red tail words (page -> [(line, n_words)])
TAILS = {7: [(10, 2)]}
# fully/last-red lines (page -> {line: 'all'|'last'})
RED_LINES = {53: {6: "last", 7: "all", 8: "all", 9: "all"}}
# owner-confirmed image-only punctuation (page -> [(line, sym, xfrac|None)])
PUNCT = {
    41: [(10, "'", 0.55)],
    42: [(3, '"', None), (6, '"', None)],
    43: [(1, '"', 0.41)],
    53: [(3, '"', None), (6, '"', None)],
}
# line-level ornament annotations (page -> [(line, text)])
LATT = {
    0: [(1, "red 13-dot lattice")],
    3: [(1, "red inline dot-matrix"), (7, "red 13-dot lattice")],
    6: [(4, "red 13-dot lattice ends L4"), (5, "terminating red 13-dot lattice")],
    7: [(10, "red 13-dot lattices bracket this line")],
    27: [(1, "terminating red 13-dot lattice")],
    33: [(5, "terminating red 13-dot lattice")],
    36: [(5, "red 10-dot lattice at end of L5"), (6, "red digit 1*")],
    37: [(1, "red digit 2*"), (5, "red digit 3*"), (9, "black 4-dot diamonds (owner)"),
         (10, "red digit 4*")],
    38: [(4, "red digit 5*"), (10, "red 10-dot lattice begins L10")],
    39: [(6, "red 13-dot lattice"), (12, "red 13-dot lattice")],
    53: [(6, "red arrow after L6")],
    57: [(1, "RED inline 13-dot matrix (S8b)")],
    10: [(8, "black inline digit 7")],
    15: [(1, "printed digits 3278/3299*/3298/2838 above")],
}
LATTICE_ONLY = {2, 14, 22, 26, 32, 49, 55}

P50_TABLE = """    2M 0w 3L 3D 2r 0S 1p 15
    3V 3e 3I 0n 3u 1O 0u 0Z
    3g 2U 1C 0Y 1N 3n 0W 3Q
    22 13 0V 3c 0E 34 0W 1t
    1D 2N 3H 47 0s 2p 0Z 34
    0g 3v 1Q 0s 0D 0K 2h 3D
    3L 2x 1Q 20 2n 2L 1C 2p
    0A 29 3r 0D 45 0k 2e 2W
    25 3U 1W 2r 46 2s 2X 39
    3p 0X 0E 1q 0q 4B 49 48
    3r 3b 3C 1M 1j 0I 4A 48
    40 3m 4E 0s 2S 1v 3T 0I
    3t 2B 2k 2t 2O 0e 2l 1L"""

P51_TABLE = """    28 2a 0J 1L 0c 3C 2o 0X
    00 2Z 2d 1T 2u 1t 1j 0l
    1o 1E 3T 18 3E 1G 27 0L
    0v 2t 06 11 1A 2U 4B 1O
    2M 3d 2S 0x 0w 0q 0p 2V
    18 0q 1D 49 2O 00 1v 2t
    1k 3s 3G 21 3w 0W 29 2r
    2O 2L 0g 3Y 0M 0u 3I 3C
    1r 2c 2q 3o 30 0a 39 1K"""

P56_HEX = """    36367763ab73783c7af284446c
    59466b4cd653239a311cb7116
    d4618dee09a8425893dc7500b
    464fdaf1672d7bef5e891c6e227
    4568926a49fb4f45132c2a8b4"""


def load_pages():
    lines = open(KRIS).read().splitlines()
    blocks, cur = [], []
    for l in lines:
        if l.strip() == "%":
            blocks.append(cur)
            cur = []
        else:
            cur.append(l)
    blocks.append(cur)
    return {b: [s for s in blocks[bi] if s.strip()] for bi, b in enumerate(BOOK)}


def _rune(c):
    return 0x16A0 <= ord(c) <= 0x16FF


def star(s, n=None, mode="first"):
    """Suffix '*' on runes of the first (or last) n dash-words, or all/last rune.
    Only runic codepoints get '*'; '.' stays unmarked."""
    words = s.split("-")
    if mode == "all":
        return "-".join("".join(c + "*" if _rune(c) else c for c in w) for w in words)
    if mode == "lastrune":
        out = list(words)
        w = out[-1]
        last = max((j for j, c in enumerate(w) if _rune(c)), default=-1)
        if last >= 0:
            out[-1] = w[:last + 1] + "*" + w[last + 1:]
        return "-".join(out)
    k = n if n is not None else 1
    if mode == "first":
        return "-".join(
            "".join(c + "*" if _rune(c) else c for c in w) if i < k else w
            for i, w in enumerate(words))
    # "lastwords": last n words
    return "-".join(
        "".join(c + "*" if _rune(c) else c for c in w) if i >= len(words) - k else w
        for i, w in enumerate(words))


def word_slot(seg, xfrac):
    """Approximate dash-word index (1-based) at character fraction xfrac."""
    return max(1, min(len(seg.split("-")), int(xfrac * len(seg)) + 1))


def fence(table):
    """Dedent a 4-space-indented table constant into a fenced code block."""
    body = "\n".join(l[4:] if l.startswith("    ") else l
                     for l in table.splitlines())
    return "```\n" + body + "\n```"


def block(p, segs):
    if p == 50:
        return ("**Ciphertext** (token page — 0 runes; the page IS key material; "
                "tokens as printed, community base60 reading):\n\n" + fence(P50_TABLE) + "\n")
    if not segs:
        return None
    heads = dict((l, n) for l, n in HEADS.get(p, []))
    tails = dict((l, n) for l, n in TAILS.get(p, []))
    redl = RED_LINES.get(p, {})
    punct = {}
    for l, sym, xf in PUNCT.get(p, []):
        punct.setdefault(l, []).append((sym, xf))
    latt = {}
    for l, txt in LATT.get(p, []):
        latt.setdefault(l, []).append(txt)
    if p in LATTICE_ONLY:
        latt.setdefault(len(segs), []).append("red 13-dot lattice (section terminator)")
    out = ["**Ciphertext** (krisyotam verbatim; `-` word separator, `.` = "
           "sentence dot (see p56 L1 `END.`), `/` = line end; standalone `&` "
           "(18×) / `$` (9×) / `§` (1×, book end p57) are krisyotam's "
           "transcription of the red dot-matrix ornaments — cipher-stream "
           "content, size mapping unconfirmed; `*` = red ink on owner-confirmed "
           "spans; `⟦'⟧`/`⟦\"⟧` = image-only punctuation absent from the "
           "transcription, ≈word slot estimated. Line numbers = krisyotam "
           "lines (≠ image lines on solved pages, which wrap mid-word); printed "
           "Roman/Arabic content is omitted by krisyotam and appended below "
           "where known):", "", "```"]
    for i, seg in enumerate(segs, 1):
        s = seg
        if i in heads:
            s = star(s, heads[i], "first")
        if i in tails:
            s = star(s, tails[i] or 1, "lastwords")
        if i in redl:
            s = star(s, mode="lastrune" if redl[i] == "last" else "all")
        ann = []
        for sym, xf in punct.get(i, []):
            pos = f"≈w{word_slot(seg, xf)}" if xf is not None else "pos TBD"
            ann.append(f"⟦{sym}⟧{pos}")
        ann += latt.get(i, [])
        # wrap at dash-word boundaries for readability (owner request);
        # continuation lines align under the first rune
        head = f"{i:>2}  "
        indent = " " * len(head)
        parts = s.split("-")
        rows, cur = [], ""
        for j, w in enumerate(parts):
            piece = w + ("-" if j < len(parts) - 1 else "")
            if cur and len(cur) + len(piece) > 72:
                rows.append(cur)
                cur = piece
            else:
                cur += piece
        rows.append(cur)
        out.append(head + rows[0] + (("   " + "; ".join(ann)) if ann else ""))
        out.extend(indent + r for r in rows[1:])
    out.append("```")
    if p == 51:
        out.append("\nPrinted token table on this page (Roman/Arabic, omitted by "
                   "krisyotam; idx246 = r8c7 `3I` pixel-confirmed 0xc6; community "
                   "base60 reading):\n\n" + fence(P51_TABLE))
    if p == 56:
        out.append("\nPrinted hex lines (omitted by krisyotam — runes-only "
                   "extraction; the onion address):\n\n" + fence(P56_HEX))
    return "\n".join(out) + "\n"


def main():
    pages = load_pages()
    md = open(MD).read()
    n = 0
    for p in range(58):
        blk = block(p, pages.get(p, []))
        if blk is None:
            continue
        img = f"![p{p}](img/oracle/pages/p{p:02d}.jpg)"
        i = md.find(img)
        if i < 0:
            print("missing image line", p)
            continue
        j = md.find("**Notes:", i)  # prefix anchor: owner writes
        # "**Notes:**" (empty) AND "**Notes: text**" (bold-wrapped) — matching
        # only "**Notes:**" makes the insert swallow the next sections
        if j < 0:
            print("missing Notes", p)
            continue
        seg = md[i + len(img):j]
        if "◆" in seg or "///" in seg:
            # owner-annotated block (diamond lattices / break marks):
            # never regenerate — owner edits are ground truth here
            print("skipping owner-annotated p", p)
            continue
        new_seg = "\n\n" + blk + "\n"
        if "**Ciphertext**" in seg:
            k = seg.find("**Ciphertext**")
            md = md[:i + len(img)] + seg[:k] + blk + "\n" + md[j:]
        else:
            md = md[:i + len(img)] + new_seg + md[j:]
        n += 1
    open(MD, "w").write(md)
    print(f"inserted/refreshed ciphertext blocks for {n} pages")


if __name__ == "__main__":
    main()
