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
    ("Q3", list(range(8, 23)), "TERMINATOR CHANNEL CONFIRMS THE OWNER NESTING: p14 ENDS WITH & (branch segment pp8–14 = complete section, dragonfly close, partial page 7 lines / 1,729 runes) · AXIS p15 (& + $ sit MID-PAGE right after the decimal block — $ = the large ∞ graphic) · plain segment pp16–22 closes with $ (partial page 6 lines, fence + body in repose). Page symmetry 7|axis|7; core lines 72↔72; runes unequal (1,729 vs 1,903); LP1 line-sum palindrome REFUTED 0/72"),
    ("Q4", [23, 24, 25, 26], "p23 = MEMBER (owner r8): p23 carries NO page-end terminator (last line is runes) — it flows into the cicadas; the section closes only at p26's &/$. p23-top dots remain the flip/mirror partner of p7-bottom/p56-bottom (hinge decoration, but the text runs through it)"),
    ("Q5", list(range(27, 33)), "gap; singletons only — p27 cicada wing at top, p32 blurry tree at bottom"),
    ("Q6", list(range(33, 40)), "owner r7: 'No scrolls; </Y patterns' on ALL SEVEN pages (independent of the machine finding: one pixel-identical black stamp ×7, campaign #12); 3-large-dot paragraph breaks at p33 and p39"),
    ("Q7", list(range(40, 56)), "'3 dot / 5 dot mirrored scrolls' CONTINUOUS pp40–55 (owner r7), BUT terminators split it into three: [pp40–49]& (token page ENDS its section — & on p49's last line) · [pp50–53]& (p53's & sits right after the red-text block) · [pp54–55]$ (owner r8 nested unit: cicada after p53's red block → cicada at p55 bottom; boundary = p53's &). p55 tree center + cicada bottom; p40↔p48 asymmetry = sub-feature"),
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
        "\n1. **p23 hinge — RESOLVED by your r8 note + terminators:** p23 "
        "carries NO page-end terminator (last line is runes), so the text "
        "runs through it into the cicadas; the section closes only at "
        "p26's &/$. The hinge dots stay a decoration spanning two "
        "brackets; textually p23 ∈ Q4.\n"
        "2. **Q3 nesting (your 2026-11-17 hypothesis, measured):** "
        "branch-segment pp8–14 | axis p15 (decimals + ∞) | plain segment "
        "pp16–22. Page symmetry exact 7|axis|7, core line-counts 72↔72, "
        "both closers partial (p14: 7 lines/dragonfly, p22: 6 lines/fence"
        "+body) — but rune lengths unequal (1,729 vs 1,903) and the LP1 "
        "line-sum palindrome across the axis is REFUTED (0/72). Note: all "
        "four p15 decimals fall INSIDE the pre-axis segment's stream span "
        "(1874–3602), and 1,729 is the Hardy–Ramanujan number — logged, "
        "not evidence. UPDATE: terminators CONFIRM the nesting — p14 ends "
        "& (branch segment = closed section), p15's &+$ sit mid-page after "
        "the decimals, p22 closes $ — three units, not one passage.\n"
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
