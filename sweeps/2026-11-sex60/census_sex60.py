#!/usr/bin/env python3
"""Campaign #12 / F17 — sexagesimal-stamp CENSUS (descriptive, no gate).

The "Babylonian sexagesimal margin art" of book pp34-39 is ONE repeated
stamp (dukotah R44-W2-B2 correction: 7 instances, p33 bottom + tops of
p34-p39; p34-p39 bitwise identical). This script re-verifies placement +
identity independently of dukotah's numbers, prints the component table,
and cuts the oracle read sheets (wedge identification is a human-eye task;
machine wedge-counting is disclosed as failed below).

Usage: python3 census_sex60.py [--imgdir sources/ibotpeaches/liber_primus]
                               [--out docs/img/oracle]
"""
import argparse
import json
import os

import numpy as np
from PIL import Image, ImageDraw

_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
DUK = os.path.join(_ROOT, "sources", "dukotah", "liber-primus", "analysis",
                   "round44", "W2-B2-cuneiform")
# book page -> image file = page + 17
STAMP = (1029, 1391, 157, 546)          # x0,x1,y0,y1 on p34-p39 images
P33_Y = (3050, 3440)
PAGES = list(range(34, 40))


def load_geom():
    """Component boxes from dukotah's persisted census (geometry reuse, not
    recount - their census is the record; we re-verify pixels ourselves)."""
    c = json.load(open(os.path.join(DUK, "census.json")))
    comps = sorted(c["images"]["p34"]["unlogged_components"][:7],
                   key=lambda z: (z["y0"] // 120, z["x0"]))
    return comps


def verify(imgdir):
    """Bitwise identity of the stamp region across p34-p39 (independent)."""
    x0, x1, y0, y1 = STAMP
    ref = np.asarray(Image.open(os.path.join(imgdir, "51.jpg")).convert("L"))[y0:y1 + 1, x0:x1 + 1]
    ok = {}
    for n in PAGES:
        a = np.asarray(Image.open(os.path.join(imgdir, f"{n + 17:02d}.jpg")).convert("L"))[y0:y1 + 1, x0:x1 + 1]
        ok[n] = bool(np.array_equal(a, ref))
    return ok


def sheets(imgdir, outdir, comps):
    os.makedirs(outdir, exist_ok=True)
    x0, x1, y0, y1 = STAMP
    im = Image.open(os.path.join(imgdir, "51.jpg")).convert("RGB")

    # 1. stamp at 3x with G-labels
    stamp = im.crop((x0 - 25, y0 - 25, x1 + 25, y1 + 25))
    S = 3
    stamp = stamp.resize((stamp.width * S, stamp.height * S), Image.LANCZOS)
    d = ImageDraw.Draw(stamp)
    for i, g in enumerate(comps):
        cx = (g["x0"] + g["x1"]) // 2 - x0 + 25
        cy = g["y0"] - y0 + 25
        d.text((cx * S - 12, max(0, cy * S - 30)), f"G{i+1}", fill="red")
    stamp.save(os.path.join(outdir, "sex60_stamp_p34.png"))

    # 2. per-glyph tiles 4x
    tiles = []
    for g in comps:
        t = im.crop((g["x0"] - 15, g["y0"] - 15, g["x1"] + 15, g["y1"] + 15))
        t = t.resize((t.width * 4, t.height * 4), Image.LANCZOS)
        tiles.append(t)
    W = max(t.width for t in tiles)
    H = max(t.height for t in tiles) + 34
    sheet = Image.new("RGB", (W * 4 + 50, H * 2 + 30), "white")
    dr = ImageDraw.Draw(sheet)
    for i, t in enumerate(tiles):
        px, py = (i % 4) * (W + 10) + 10, (i // 4) * (H + 10) + 10
        sheet.paste(t, (px, py + 30))
        dr.text((px + 4, py + 4), f"G{i+1}", fill="red")
    sheet.save(os.path.join(outdir, "sex60_glyphs_p34.png"))

    # 3. synthetic wedge reference (schematic, drawn not cropped)
    ref = Image.new("RGB", (900, 240), "white")
    dr = ImageDraw.Draw(ref)

    def vdown(dr, x, y, n):
        """n vertical wedges (value 1 each)."""
        for k in range(n):
            xx = x + k * 46
            dr.polygon([(xx, y), (xx + 34, y), (xx + 17, y + 26)], fill="black")
            dr.line([(xx + 17, y + 26), (xx + 17, y + 66)], fill="black", width=5)

    def uleft(dr, x, y, n):
        """n corner wedges (value 10 each)."""
        for k in range(n):
            yy = y + k * 40
            dr.polygon([(x + 30, yy), (x + 30, yy + 30), (x, yy + 15)], fill="black")
            dr.line([(x + 30, yy + 15), (x + 66, yy + 15)], fill="black", width=5)

    vdown(dr, 30, 40, 3)
    dr.text((30, 130), "vertical wedge = 1\n(3 shown = 3)", fill="black")
    uleft(dr, 320, 30, 2)
    dr.text((320, 130), "corner wedge = 10\n(2 shown = 20)", fill="black")
    dr.polygon([(620, 70), (620, 104), (652, 87)], fill="black")
    dr.line([(652, 87), (740, 87)], fill="black", width=6)
    dr.text((600, 130), "horizontal wedge\n(not a number digit)", fill="black")
    ref.save(os.path.join(outdir, "sex60_wedge_ref.png"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--imgdir", default=os.path.join(_ROOT, "sources", "ibotpeaches", "liber_primus"))
    ap.add_argument("--out", default=os.path.join(_ROOT, "docs", "img", "oracle"))
    args = ap.parse_args()
    comps = load_geom()
    ok = verify(args.imgdir)
    print("stamp bitwise identical p34-p39:", ok)
    assert all(ok.values()), "identity check failed"
    print(f"{'glyph':6} {'x0':>5} {'y0':>5} {'w':>4} {'h':>4} {'area':>6}")
    for i, g in enumerate(comps):
        print(f"G{i+1:<5} {g['x0']:>5} {g['y0']:>5} {g['w']:>4} {g['h']:>4} {g['area']:>6}")
    sheets(args.imgdir, args.out, comps)
    print("wrote sheets to", args.out)


if __name__ == "__main__":
    main()
