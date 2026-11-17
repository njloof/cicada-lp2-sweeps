#!/usr/bin/env python3
"""Generate docs/SEGMENTS.md — the 58 original pages laid out under their
10 decoration-groups (owner request 2026-11-17: "double-check all this by
preparing a document that shows the original pages divided into the 10
groups").

Deterministic; embeds the existing full-page images (no image binaries
written). Regenerate after any segmentation change:

    python3 scripts/audit/make_segments_doc.py

Segmentation data = campaign #18 (sweeps/2026-11-segments/PREREG.md),
owner-corrected 2026-11-17 (p0 joins the fence+inf family).
"""
import os
import sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
sys.path.insert(0, os.path.abspath(ROOT))
sys.path.insert(0, os.path.join(ROOT, "scripts", "audit"))
from core.validate import flat  # noqa: E402

GROUPS = [
    ("P1", [0, 1, 2], "fence + ∞ top/bottom margin family on all three pages (owner correction 2026-11-17)"),
    ("P2", [3, 4], "undecorated gap"),
    ("P3", [5, 6, 7], "symmetric spiral-scrolls on all three pages"),
    ("P4", list(range(8, 24)), "interior of the p7↔p23 bracket (p7-bottom 5-dot = vertical flip of p23-top). Owner round-7 notes: branching drawings alternate L/R across pp8–14 (split candidate); p23-top dots = mirror of p56-bottom dots, 'denote a beginning (here) and an ending (page 56)' — spanning-bracket candidate, see review notes below"),
    ("P5", [24, 25], "mirrored cicadas in margins (owner round-7 confirms; jbo 'mayfly' group pp23–26 agrees)"),
    ("P6", list(range(26, 33)), "gap between cicadas and stamp family (p27 cicada wing, p32 blurry tree — singletons)"),
    ("P7", list(range(33, 40)), "owner round-7: 'No scrolls; </Y patterns' on ALL SEVEN pages — independent confirmation; plus one pixel-identical black stamp ×7 (machine-verified, campaign #12); 3-large-dot paragraph breaks on p33+p39"),
    ("P8", list(range(40, 49)), "p40↔p48 margin-asymmetry bracket (S8c)"),
    ("P9", list(range(49, 56)), "gap; contains the entire base-60 token stream (pp49–51); owner round-7: p55 tree outline center + cicada bottom"),
    ("P10", [56, 57], "solved closing pages (different construction); p56-bottom 5-dot pattern (3+2) = mirror partner of p23-top per owner round-7"),
]


def main():
    out = [
        "# SEGMENTS — LP2 divided into 10 decoration-groups\n",
        "\nVisual double-check of the campaign #18 segmentation (owner "
        "hypothesis: decorations delimit passages, not pages). Pages are "
        "the original full-page scans (docs/img/oracle/pages/), in book "
        "order within each group. Rune counts from core.validate; stream "
        "positions over pp00–55 (p50 runeless, excluded).\n",
        "\nEvidence and verdict panel: sweeps/2026-11-segments/. "
        "Regenerate: `python3 scripts/audit/make_segments_doc.py`.\n",
    ]
    pos = 0
    for gid, pages, ev in GROUPS:
        runes = sum(len(flat(n)) for n in pages if n != 50)
        if pages[0] <= 55:
            rng = f"stream pos {pos}–{pos + runes - 1}"
            pos += runes
        else:
            rng = "solved (excluded from stream)"
        out.append(f"\n## {gid} — pp{pages[0]:02d}–{pages[-1]:02d} "
                   f"({len(pages)} pages, {runes} runes, {rng})\n")
        out.append(f"\n*{ev}*\n")
        for p in pages:
            n = 0 if p == 50 else len(flat(p))
            tag = " *(runeless token page)*" if p == 50 else f" *({n} runes)*"
            out.append(f"\n**p{p}**{tag}\n\n"
                       f"![p{p}](img/oracle/pages/p{p:02d}.jpg)\n")
    out.append(
        "\n## Review notes — open questions from your round-7 notes\n"
        "\n1. **p23-top ↔ p56-bottom mirror dots** ('a beginning here, an "
        "ending on p56'): as written this brackets pp23–56, which cuts "
        "across P4's end and P5–P9. Does it REPLACE the p7↔p23 bracket "
        "(making pp8–22 the passage and pp23–55 a second one), or is it a "
        "whole-book frame (p0-family opens, p56 closes) sitting above the "
        "per-passage decorations?\n"
        "2. **Branching drawings pp8–14 (alternating L/R)**: a family "
        "inside P4. Is P4 really one passage (pp8–23), or does the "
        "branching family delimit pp8–14 with a different decoration "
        "taking over at p15?\n"
        "3. **P2 / P6 / P9 are groups by ABSENCE of decoration** — the "
        "weakest rows. Anything at their edges (p2/p3, p25/p26, p32/p33, "
        "p48/p49) that should merge or split them?\n"
        "4. **3-large-dot paragraph breaks on p33 and p39** (your note): "
        "both sit at P7 edges — consistent with P7 as a passage; the same "
        "large-dot class appears at p7's `$` position (diamond) and the "
        "9 `$` pages (oracle round #6 S9).\n")
    with open(os.path.join(ROOT, "docs", "SEGMENTS.md"), "w") as f:
        f.write("".join(out))
    print("wrote docs/SEGMENTS.md")


if __name__ == "__main__":
    main()
