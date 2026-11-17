#!/usr/bin/env python3
"""Mark machine-census finds on FULL-PAGE images.

OWNER POLICY 2026-11-17: audits use full pages, never crops ("so we don't
have to play games about whether cropping worked well"). OWNER RUNS THIS
(bulk image writes belong to the owner; the classifier blocks the agent):

    python3 scripts/audit/mark_full_pages.py

Outputs docs/img/oracle/audit/pNN_marked.png (+ pNN_markers.txt sidecar)
for the two live oracle questions:

  (b) the 19 residual plain dots (campaign #16 t4_residual.csv) —
      "help me find the unstarred plain dots": every black 4-dot diamond
      the machine census found on those pages is circled CYAN (D-numbered)
      so you can read off which one is the sentence dot you left plain.
  (a) the 9 krisyotam `$` pages — every red lattice cluster is boxed
      ORANGE (L-numbered, dot count in the label) so you can tell us what
      the `$` segment sits on.

Census CSVs use ibotpeaches scan pixel space; marks are drawn at source
resolution then the page is resized to the 850-px walkthrough width.
"""
import csv
import os

from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
SCAN = os.path.join(ROOT, "sources", "ibotpeaches", "liber_primus")
PAGES = os.path.join(ROOT, "docs", "img", "oracle", "pages")
OUTD = os.path.join(ROOT, "docs", "img", "oracle", "audit")
W = 850

RESIDUAL_PAGES = {7, 10, 17, 20, 26, 27, 29, 30, 34, 40, 41, 44, 47, 48, 52}
DOLLAR_PAGES = {2, 7, 15, 22, 26, 32, 39, 55, 56}


def main():
    os.makedirs(OUTD, exist_ok=True)
    four = {}
    with open(os.path.join(ROOT, "sweeps/2026-11-ornaments/fourdots.csv")) as f:
        for r in csv.DictReader(f):
            four.setdefault(int(r["page"]), []).append((int(r["x"]), int(r["y"])))
    lat = {}
    with open(os.path.join(ROOT, "sweeps/2026-11-ornaments/lattices.csv")) as f:
        for r in csv.DictReader(f):
            lat.setdefault(int(r["page"]), []).append(
                (int(r["x0"]), int(r["y0"]), int(r["x1"]), int(r["y1"]),
                 int(r["dots"])))
    resid = {}
    with open(os.path.join(ROOT, "sweeps/2026-11-diamonds/results/t4_residual.csv")) as f:
        for r in csv.DictReader(f):
            resid.setdefault(int(r["page"]), []).append(r)

    pages = sorted(RESIDUAL_PAGES | DOLLAR_PAGES)
    font = ImageFont.load_default(size=42)
    for p in pages:
        src = os.path.join(SCAN, f"{p + 17:02d}.jpg")
        im = Image.open(src).convert("RGB")
        d = ImageDraw.Draw(im)
        lines = [f"# p{p} markers (scan px; page {im.width}x{im.height})",
                 "# D = black 4-dot diamond census (cyan) — residual-dot question",
                 "# L = red lattice census (orange) — `$` question"]
        for k in resid.get(p, []):
            lines.append(f"# residual plain dot: krisyotam line {k['line']}, "
                         f"dot #{k['dot_k']} of {k['n_dots_line']} on that line"
                         + (", LINE-FINAL" if k["line_final"] == "True" else ""))
        for i, (x, y) in enumerate(sorted(four.get(p, [])), 1):
            r = 55
            d.ellipse([x - r, y - r, x + r, y + r], outline="cyan", width=8)
            d.text((x + r + 8, y - 20), f"D{i}", fill="cyan", font=font)
            lines.append(f"D{i} four-dot diamond at ({x},{y})")
        for i, (x0, y0, x1, y1, n) in enumerate(sorted(lat.get(p, []), key=lambda t: (t[1], t[0])), 1):
            pad = 20
            d.rectangle([x0 - pad, y0 - pad, x1 + pad, y1 + pad], outline="orange", width=8)
            d.text((x1 + pad + 8, y0 - 10), f"L{i}:{n}", fill="orange", font=font)
            lines.append(f"L{i} {n}-dot red lattice box ({x0},{y0})-({x1},{y1})")
        im = im.resize((W, int(im.height * W / im.width)), Image.LANCZOS)
        im.save(os.path.join(OUTD, f"p{p:02d}_marked.png"), optimize=True)
        with open(os.path.join(OUTD, f"p{p:02d}_markers.txt"), "w") as f:
            f.write("\n".join(lines) + "\n")
        print("marked p", p, flush=True)
    print(f"wrote {len(pages)} pages to {OUTD}")


if __name__ == "__main__":
    main()
