#!/usr/bin/env python3
"""Generate oracle visual assets from the pinned ibotpeaches scans:

1. docs/ORACLE_PAGES.md + docs/img/oracle/pages/pNN.jpg — full-page
   walkthrough with per-page Notes fields (owner fills by eye).
2. docs/img/oracle/f7_S8c_p{40,48}_margins_full.png — full-height margin
   strips (S8c re-ask: previous crops were too tight per owner).

Run from repo root:  python3 scripts/audit/make_oracle_visuals.py
"""
import os
import sys

from PIL import Image

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
IMG = os.path.join(ROOT, "sources", "ibotpeaches", "liber_primus")
OUTD = os.path.join(ROOT, "docs", "img", "oracle")
PAGE_DIR = os.path.join(OUTD, "pages")

RED_HEADS = {0, 3, 6, 7, 8, 15, 23, 27, 33, 37, 39, 40, 53, 54}
LATTICE_ONLY = {2, 14, 22, 26, 32, 49, 55}
EXTRA = {
    36: "red digit 1 (L6)",
    37: "red digits 2/3/4 (L1/L5/L10) + black 4-dot diamonds (owner L2/4/5/8/11)",
    38: "red digit 5 (L4) + black diamonds right edge (L3/8/9); margin asymmetry S8c",
    10: "black inline digit 7 (L8)",
    15: "printed digit group 3278/3299*(red)/3298/2838",
    53: "stream L7/L8/L9 entirely red + red arrow after L6 (owner F4)",
    8: "black 4-dot diamonds L3/L7/L11 (L6-left = noise per owner S7)",
    40: "red-opening sentence ENDED by mid-line-2 black diamond (S8a CONFIRMED); margin asymmetry S8c",
    48: "margin decoration asymmetry (S8c/d)",
    57: "23-dot lattice (book end) + RED inline matrix after red word (S8b CONFIRMED) + bottom decoration",
    3: "red inline dot-matrix after red word (seen 2026-11-16)",
    50: "token table page (0 runes)",
}


def known(p):
    ks = []
    if p in RED_HEADS:
        ks.append("red head word (line 1)")
    if p in LATTICE_ONLY:
        ks.append("red only via dot-lattice (section terminator)")
    if 33 <= p <= 39:
        ks.append("black stamp device (top; p33 footer)")
    if p in EXTRA:
        ks.append(EXTRA[p])
    if p in (56, 57):
        ks.append("SOLVED closing page")
    return "; ".join(ks) or "—"


RED_HEADS = {0, 3, 6, 7, 8, 15, 23, 27, 33, 37, 39, 40, 53, 54}
LATTICE_ONLY = {2, 14, 22, 26, 32, 49, 55}

HEADER = """# Oracle page walkthrough — all LP2 pages, open notes

Companion to ORACLE_QUEUE.md: the queue asks *specific* questions; this file
is for *anything you notice* on a page that we may have missed. You do not
have to fill every page — partial notes on any subset are gold. Skip a page
by leaving its Notes line empty.

Conventions: page numbers = BOOK numbers (0–57; p50 = runeless token page;
pp56–57 = solved closing pages). Red ink uses `*` per red glyph. "Known"
lists what the machine census + your previous answers already account for —
anything NOT in that list is news to us.

Broad questions worth a thought as you flip (answer inline anywhere):
- Do word-separator dots (·) ever differ in size/shape from page to page?
- Any pages where the margin decoration differs from the usual scroll motif?
- Do the 4-dot black diamonds and the red dot-matrices ever appear on the
  SAME page? Same line?
- Anything that repeats visually across pages but is not in the Known list?

---
"""


def walkthrough():
    os.makedirs(PAGE_DIR, exist_ok=True)
    out = [HEADER]
    for p in range(58):
        src = os.path.join(IMG, f"{p + 17:02d}.jpg")
        if not os.path.exists(src):
            print("missing", p)
            continue
        im = Image.open(src).convert("RGB")
        w = 850
        im = im.resize((w, int(im.height * w / im.width)), Image.LANCZOS)
        fn = f"pages/p{p:02d}.jpg"
        im.save(os.path.join(OUTD, fn), quality=74, optimize=True)
        status = "solved" if p in (50, 56, 57) else "unsolved"
        out.append(f"\n## p{p} ({status})\n\nKnown: {known(p)}\n\n"
                   f"![p{p}](img/oracle/{fn})\n\n**Notes:**\n\n\n")
        print("page", p, "ok", flush=True)
    out.append("\n---\n\n## Broad observations (anything not tied to one page)\n\n__\n\n__\n\n__\n")
    with open(os.path.join(ROOT, "docs", "ORACLE_PAGES.md"), "w") as fh:
        fh.write("".join(out))
    print("wrote docs/ORACLE_PAGES.md")


def margins():
    for pg, name in ((40, "p40"), (48, "p48")):
        im = Image.open(os.path.join(IMG, f"{pg + 17:02d}.jpg"))
        l = im.crop((0, 0, 520, 3600))
        r = im.crop((1880, 0, 2400, 3600))
        comb = Image.new("RGB", (l.width + r.width + 24, 3600), "white")
        comb.paste(l, (0, 0))
        comb.paste(r, (l.width + 24, 0))
        comb = comb.resize((int(comb.width * 0.22), int(comb.height * 0.22)), Image.LANCZOS)
        comb.save(os.path.join(OUTD, f"f7_S8c_{name}_margins_full.png"))
        print("margins", name, comb.size)


if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    if which in ("all", "margins"):
        margins()
    if which in ("all", "pages"):
        walkthrough()
