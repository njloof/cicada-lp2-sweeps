#!/usr/bin/env python3
"""Oracle queue #1 follow-up crops (owner answers 2026-11-16 requested them):
  1. p53 lines full-width (owner: crops too tight to certify lines 7-9 all-red)
  2. p27 pos-93: RE-ANCHORED crops (round-#1 crops were off by one line;
     see section 5) + same-line reference-glyph contact sheet
  3. p38 line-10 region (owner NEW observation: red 10-dot pattern at L10)
  4. digit comparison sheet: pp36-38 margin digits vs p10/p15 printed digits,
     plus a schematic Babylonian wedge reference (owner: can't tell wedge vs
     printed without examples)
Writes docs/img/oracle/*_v2.png (tracked). Reuse of make_checklist geometry.
"""
import os
import sys

import numpy as np
from PIL import Image, ImageDraw

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
sys.path.insert(0, os.path.join(ROOT, "scripts", "audit"))
import make_checklist as mc  # noqa: E402

IMGS = os.path.join(ROOT, "sources", "ibotpeaches", "liber_primus")
OUT = os.path.join(ROOT, "docs", "img", "oracle")


def page(n):
    return Image.open(os.path.join(IMGS, f"{n + 17:02d}.jpg")).convert("RGB")


def crop(im, x0, y0, x1, y1, path, zoom=2):
    W, H = im.size
    c = im.crop((max(0, x0), max(0, y0), min(W, x1), min(H, y1)))
    c = c.resize((c.width * zoom, c.height * zoom), Image.LANCZOS)
    c.save(os.path.join(OUT, path))
    print(path, c.size)


def bands(n):
    g = np.array(page(n).convert("L"))
    return mc.ink_bands(g), g


# 1. p53: full-width bands 0..11 (generous; owner maps to stream lines)
bd, _ = bands(53)
im = page(53)
for i, (y0, y1) in enumerate(bd[:12]):
    crop(im, 560, y0, 1900, y1, f"p53_band{i:02d}_full.png", zoom=1)

# 2. (SUPERSEDED 2026-11-16: this section cropped bd27[4] assuming band k =
#    line k; band 0 is the mayfly ornament and band 1 holds lines 0-2, so
#    bd27[4] was LINE 5. Correct cluster-anchored crops are in section 5.
#    p27_pos93_wide.png / p27_strip04_marked.png are NOT regenerated.)

# 3. p38: line-10 band full width + wider context (bands 8-11)
bd38, _ = bands(38)
im38 = page(38)
if len(bd38) >= 10:
    y0, y1 = bd38[9]
    crop(im38, 560, y0, 1900, y1, "p38_line10_full.png", zoom=2)
y0c = bd38[7][0] if len(bd38) > 7 else 0
y1c = bd38[min(11, len(bd38) - 1)][1]
crop(im38, 560, y0c, 1900, y1c, "p38_context_bands8-11.png", zoom=1)

# 4. digit comparison sheet
def load(p):
    return Image.open(os.path.join(OUT, p))

margins = [("p36 margin `1*`", "ADJ_p36_band7.png"),
           ("p37 margins `2* 3* 4*`", "p37_margins.png"),
           ("p38 margin `5*`", "p38_margins.png")]
printed = [("p10 inline `7` (black)", "p10_line8.png"),
           ("p15 groups (3299 red)", "p15_digits_LABELLED.png")]
H = 900
W = 1500
sheet = Image.new("RGB", (W, 2600), "white")
dr = ImageDraw.Draw(sheet)
y = 20
dr.text((20, y), "TOP: margin digits pp36-38 (our red-digit claim)", fill="black")
y += 30
for label, f in margins:
    c = load(f)
    sc = min(1.4, (W - 60) / c.width, (H / 3) / c.height)
    c = c.resize((int(c.width * sc), int(c.height * sc)), Image.LANCZOS)
    dr.text((20, y), label, fill="black")
    y += 20
    sheet.paste(c, (20, y))
    y += c.height + 24
dr.text((20, y), "MIDDLE: printed digits p10/p15 (Arabic-style reference)", fill="black")
y += 30
for label, f in printed:
    c = load(f)
    sc = min(1.0, (W - 60) / c.width, (H / 3) / c.height)
    c = c.resize((int(c.width * sc), int(c.height * sc)), Image.LANCZOS)
    dr.text((20, y), label, fill="black")
    y += 20
    sheet.paste(c, (20, y))
    y += c.height + 24
# schematic Babylonian wedges (NOT a scan - drawing): 1..5 vertical wedges, 10 angle wedge
dr.text((20, y), "BOTTOM: SCHEMATIC Babylonian sexagesimal (drawn, not a scan):", fill="black")
y += 26
x = 40
for val, n in ((1, 1), (2, 2), (3, 3), (4, 4), (5, 5)):
    for k in range(n):
        wx = x + k * 34
        dr.polygon([(wx, y + 60), (wx + 26, y + 30), (wx + 26, y + 90)], fill="black")
    dr.text((x, y + 100), str(val), fill="black")
    x += 34 * n + 70
# angle wedge for 10
dr.polygon([(x, y + 30), (x + 90, y + 60), (x, y + 90)], fill="black")
dr.polygon([(x, y + 30), (x + 30, y + 45), (x, y + 60)], fill="white")
dr.text((x, y + 100), "10", fill="black")
if y + 160 < sheet.height:
    sheet = sheet.crop((0, 0, W, y + 160))
sheet.save(os.path.join(OUT, "digit_style_sheet.png"))
print("digit_style_sheet.png", sheet.size)

# 5. p27 pos-93 RE-ANCHORED (round #2) — the round-#1 crops were off by one
#    line: p27 band 0 is the mayfly-wing ornament and band 1 holds THREE
#    stream lines (line 0 in RED + lines 1-2 black), so ink-band k != line k.
#    Verified by separator fingerprinting against krisyotam (cluster pattern
#    per visual row matches the rune/separator pattern per line exactly for
#    lines 1,2 and by tail-alignment for 3-10). Line y-ranges (image 44.jpg):
#      line0 RED ~913-1031 | line1 1105-1220 | line2 1293-1408 | line k>=3: bands[k-1]
#    Target: 0-based page position 93 = line 4 (0-based 77-97), rune idx 16.
#    Line 4 cluster pattern RRRRRRRRRRRsRRsRRsRRRs = the head run merged
#    (15 runes -> 11 clusters), so the target is anchored by separators:
#    rune 16 = cluster 12. Line 1 matched its pattern exactly (23 clusters,
#    no merges): rune idx p-20 -> cluster map below. Values (GEMATRIA_RUNES):
#    1=ᚢ 13=ᛈ 17=ᛒ — references on line 1 share the target's recorded value.
import numpy as _np  # noqa: E402

rgb27 = _np.array(page(27).convert("RGB")).astype(int)
redm = rgb27[:, :, 0] - (rgb27[:, :, 1] + rgb27[:, :, 2]) / 2 > 40
blk = (rgb27.sum(axis=2) < 400) & ~redm


def clusters(mask, y0, y1, x0=800, x1=1800):
    seg = mask[y0:y1, x0:x1]
    col = seg.sum(axis=0)
    out, inr = [], False
    for i, v in enumerate(col):
        if v > 0 and not inr:
            s, inr = i, True
        if v == 0 and inr:
            out.append((s + x0, i + x0))
            inr = False
    if inr:
        out.append((s + x0, x0 + len(col)))
    return [(a, b) for a, b in out if b - a > 3]


LINE1_Y = (1105, 1220)
LINE4_Y = (1670, 1784)
c1 = clusters(blk, *LINE1_Y)          # 23 clusters, pattern-exact
c4 = clusters(blk, *LINE4_Y)          # 21 clusters, head merged; sep-anchored
assert len(c1) == 23, f"line1 clusters {len(c1)}"
assert len(c4) == 21, f"line4 clusters {len(c4)}"
# rune idx -> cluster idx (line 1): pat RRRRRRsRRsRRRsRRRsRRsRs
L1 = {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 7, 7: 8, 8: 10, 9: 11,
      10: 12, 11: 14, 12: 15, 13: 16, 14: 18, 15: 19, 16: 21}
# line 4 anchor: image pat RRRRRRRRRRRsRRsRRsRRRs (widths show seps at
# clusters 10,13,16,20; head c0-c9 = runes 0-13 with 4 merges). Expected
# 2+12+2+2+3: seps after runes 1,13,15,17,20 -> image s1..s4 = after 13,15,17,20.
# Target rune idx 16 (pos 93) = cluster 14.
TARGET_C = 14
a, b = c4[TARGET_C]
assert (b - a) > 20, "target cluster should be a full rune, not a separator"
refs = [(22, "v1 @22"), (25, "v1 @25"), (30, "v1 @30"),
        (26, "v17(B) @26"), (31, "v17(B) @31"), (36, "v13(P) @36")]
tiles, lab = [], []
for pos, lb in refs:
    a, b = c1[L1[pos - 20]]
    cx = (a + b) // 2
    tiles.append(page(27).crop((cx - 45, LINE1_Y[0] - 15, cx + 45, LINE1_Y[1] + 15)))
    lab.append(lb)
tcx = (c4[TARGET_C][0] + c4[TARGET_C][1]) // 2
tiles.append(page(27).crop((tcx - 45, LINE4_Y[0] - 15, tcx + 45, LINE4_Y[1] + 15)))
lab.append("TARGET @93 (v1)")
Z = 4
tiles = [t.resize((t.width * Z, t.height * Z), Image.LANCZOS) for t in tiles]
tw, th = tiles[0].size
cs = Image.new("RGB", (4 * tw + 100, 2 * th + 120), "white")
d2 = ImageDraw.Draw(cs)
for i, (t, lb) in enumerate(zip(tiles, lab)):
    r, c = divmod(i, 4)
    cs.paste(t, (20 + c * (tw + 20), 30 + r * (th + 60)))
    d2.text((20 + c * (tw + 20), 10 + r * (th + 60)), lb, fill="black")
cs.save(os.path.join(OUT, "p27_glyph_compare.png"))
print("p27_glyph_compare.png", cs.size, "target cx:", tcx)

# corrected line-4 strip (the true pos-77-97 line) + tick under the target
strip = page(27).crop((620, LINE4_Y[0] - 25, 1800, LINE4_Y[1] + 25))
strip = strip.resize((strip.width * 2, strip.height * 2), Image.LANCZOS)
d3 = ImageDraw.Draw(strip)
tx = (tcx - 620) * 2
d3.polygon([(tx - 14, strip.height - 4), (tx + 14, strip.height - 4),
            (tx, strip.height - 34)], fill=(255, 0, 0))
strip.save(os.path.join(OUT, "p27_line04_marked.png"))
print("p27_line04_marked.png", strip.size)

# 6. p38 "10 dots" (owner round #1 observation) = left-margin red lattice,
#    band 11 = owner line numbering L10 (band5 = their L4). 10 red components,
#    diamond layout: centre column x~620 (4 dots), side columns x~605/634 (3+3).
crop(page(38), 560, 2480, 720, 2660, "p38_l10_red_dots_v2.png", zoom=3)
crop(page(38), 1650, 2052, 1960, 2226, "p38_l10_rightedge_v2.png", zoom=3)
full38 = page(38)
fz = full38.resize((full38.width // 2, full38.height // 2), Image.LANCZOS)
dz = ImageDraw.Draw(fz)
dz.rectangle([602 // 2, 2542 // 2, 637 // 2, 2599 // 2], outline=(255, 0, 0), width=3)
dz.rectangle([603 // 2, 1316 // 2, 664 // 2, 1409 // 2], outline=(0, 0, 255), width=3)
fz.save(os.path.join(OUT, "p38_full_marked.png"))
print("p38_full_marked.png", fz.size)

# 7. p49 lattice — same 10-dot diamond motif (right margin y1076-1135)
crop(page(49), 1650, 1030, 1770, 1180, "p49_lattice_v2.png", zoom=3)
