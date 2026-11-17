#!/usr/bin/env python3
"""Generate docs/SEGMENTS.md — the 58 original pages laid out under their
decoration-groups, v2 = 7 unsolved + solved (owner request 2026-11-17: "double-check all this by
preparing a document that shows the original pages divided into the 10
groups").

Deterministic; embeds the existing full-page images (no image binaries
written). Regenerate after any segmentation change:

    python3 scripts/audit/make_segments_doc.py

Segmentation data = v2, owner round-7 decoration pass (see GROUPS
below); v1 (10 groups, campaign #18, sweeps/2026-11-segments/) is
sealed as run.
"""
import os
import sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
sys.path.insert(0, os.path.abspath(ROOT))
sys.path.insert(0, os.path.join(ROOT, "scripts", "audit"))
from core.validate import flat  # noqa: E402

# v2 = owner round-7 full decoration pass (ORACLE_PAGES.md, committed
# 396e2c2). Three boundaries moved vs the #18-registered 10 groups:
# scrolls run pp3–7 (P2/P3 merge), cicadas include p26 (P5 extends),
# 3/5-dot mirrored scrolls are continuous pp40–55 (P8/P9 merge).
# #18 stays sealed as run; #19 re-test queued pending owner sign-off.
GROUPS = [
    ("Q1", [0, 1, 2], "vertical fence (mirrored + flipped) + small ∞ top/bottom on all three pages (owner r7)"),
    ("Q2", [3, 4, 5, 6, 7], "symmetric spiral-scrolls on ALL FIVE pages (owner r7 extends the family down to p3); p7-bottom 5-dot = vertical flip of p23-top — bracket opens here"),
    ("Q3", list(range(8, 23)), "interior of the p7↔p23 bracket: branching drawings alternate L/R pp8–14 (L,R,L,R,L,R,L); p15 numbers separated from runes by large ∞; p22 horizontal fence + body lying in repose (closing marker candidate); pp16–21 carry no decoration note — see question 2"),
    ("Q4", [23, 24, 25, 26], "p23 = HINGE: its top dots are simultaneously the flip-partner of p7-bottom and the mirror-partner of p56-bottom ('a beginning here, an ending on p56'); mirrored cicadas p24–26 (owner r7 adds p26; jbo mayfly group pp23–26, dukotah pp24–26)"),
    ("Q5", list(range(27, 33)), "gap; singletons only — p27 cicada wing at top, p32 blurry tree at bottom"),
    ("Q6", list(range(33, 40)), "owner r7: 'No scrolls; </Y patterns' on ALL SEVEN pages (independent of the machine finding: one pixel-identical black stamp ×7, campaign #12); 3-large-dot paragraph breaks at p33 and p39"),
    ("Q7", list(range(40, 56)), "'3 dot / 5 dot mirrored scrolls' on sides, CONTINUOUS pp40–55 (owner r7; includes runeless p50 and the whole base-60 stream pp49–51); p55 adds tree outline center + cicada bottom; p40↔p48 margin asymmetry (S8c) now reads as a sub-feature, not a boundary"),
    ("Q8", [56, 57], "solved closing pages; p56-bottom 5-dot pattern (groups of 3+2) = closing partner of the p23 hinge"),
]


def main():
    out = [
        "# SEGMENTS — LP2 divided into 7 decoration-groups (v2)\n",
        "\n**v2 = owner round-7 full decoration pass (2026-11-17).** Three "
        "boundaries moved vs the #18-registered 10 groups: spiral-scrolls "
        "run pp3–7 (old P2+P3 merge), mirrored cicadas include p26, and "
        "the 3/5-dot mirrored scrolls are continuous pp40–55 (old P8+P9 "
        "merge). Campaign #18's verdict stands as run on its registered "
        "segmentation; a #19 re-test on THIS partition is queued pending "
        "your sign-off. Pages are the original full-page scans "
        "(docs/img/oracle/pages/), book order within each group. Rune "
        "counts from core.validate; stream positions over pp00–55 (p50 "
        "runeless, excluded).\n",
        "\nEvidence and verdict panel (v1, 10 groups): "
        "sweeps/2026-11-segments/. Regenerate: "
        "`python3 scripts/audit/make_segments_doc.py`.\n",
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
        "\n## Review notes — what your round-7 notes left open\n"
        "\n1. **p23 hinge**: its top dots are (per your notes) both the "
        "flip-partner of p7-bottom AND the mirror-partner of p56-bottom. "
        "Palindrome hinge (house style) — shared by two brackets — or "
        "should p23 belong solely to the cicada group (jbo's mayfly "
        "group is pp23–26; dukotah's is pp24–26; your literal note puts "
        "mirrored cicadas on p24, p25, p26)?\n"
        "2. **pp16–21 carry no decoration note.** Are they plain interior "
        "of the bracketed passage pp8–22, or do p15 (large ∞ under the "
        "numbers) and p22 (fence + body in repose) delimit a sub-passage "
        "pp8–14 / pp15–21 / p22?\n"
        "3. **Q7 spans the base-60 token stream (pp49–51) and the "
        "runeless p50**, with the same mirrored scrolls throughout — one "
        "passage containing the tokens? If so the old P8/P9 split (my "
        "p40↔p48 margin-asymmetry bracket) is demoted to a sub-feature.\n"
        "4. **Q5 is a group by ABSENCE** (only the p27 wing and p32 tree "
        "singletons). Anything at its edges (p26/p27, p32/p33) that "
        "should merge or split it?\n"
        "5. **3-large-dot paragraph breaks on p33 and p39** (your note): "
        "both at Q6 edges — consistent with Q6 as a passage; same "
        "large-dot class as p7's `$` diamond and the 9 `$` pages (oracle "
        "round #6 S9 still live).\n")
    with open(os.path.join(ROOT, "docs", "SEGMENTS.md"), "w") as f:
        f.write("".join(out))
    print("wrote docs/SEGMENTS.md")


if __name__ == "__main__":
    main()
