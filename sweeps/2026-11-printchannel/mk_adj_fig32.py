#!/usr/bin/env python3
"""#32 adjudication figures. OWNER POLICY: full pages, never crops —
every page figure is the complete page at w=850 with machine marks.
Inputs: work/table32.jsonl + work/images/{0,15}.jpg (pulled from
studio). Outputs: sweeps/2026-11-printchannel/figs/*.
"""
import json, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
FIG = os.path.join(HERE, "figs")
os.makedirs(FIG, exist_ok=True)
W_OUT = 850

def font(sz):
    for p in ("/System/Library/Fonts/Menlo.ttc",
              "/System/Library/Fonts/Helvetica.ttc"):
        try:
            return ImageFont.truetype(p, sz)
        except OSError:
            pass
    return ImageFont.load_default()

rows = [json.loads(l) for l in open(os.path.join(ROOT, "work", "table32.jsonl"))]
byl = {}
for r in rows:
    byl.setdefault((r["page"], r["line"]), []).append(r)

def want(page):
    f = f"{ROOT}/data/pages/lp2_{page:02d}.txt"
    return [len(ln.split()) for ln in open(f).read().splitlines() if ln.strip()]

def page_fig(page, name, note):
    im = Image.open(f"{ROOT}/work/images/{page}.jpg").convert("RGB")
    sc = W_OUT / im.width
    im = im.resize((W_OUT, int(im.height * sc)))
    d = ImageDraw.Draw(im)
    f = font(14); fs = font(11)
    wv = want(page)
    cys = {ln: np.median([r["cy"] for r in byl[(page, ln)]])
           for (pg, ln) in byl if pg == page}
    pitch = np.median(np.diff(sorted(cys.values()))) if len(cys) > 2 else 190
    # excluded lines: spread their labels across the margin REGION
    # bounded by the nearest aligned lines above/below (exact row is
    # unknown by construction — the line failed the count gate)
    aligned = sorted(cys)
    run = [i for i in range(len(wv)) if i not in cys]
    for i in run:
        above = max([j for j in aligned if j < i], default=None)
        below = min([j for j in aligned if j > i], default=None)
        seg = [k for k in run
               if (above is None or k > above) and (below is None or k < below)]
        ytop = cys[above] if above is not None else 40
        ybot = cys[below] if below is not None else im.height / sc - 40
        k = seg.index(i)
        y = ytop + (ybot - ytop) * (k + 1) / (len(seg) + 1)
        y = int(y * sc)
        d.rectangle([2, y - 3, 10, y + 3], outline=(230, 0, 0), width=2)
        d.text((14, y - 7), f"l{i} EXCL want={wv[i]}",
               fill=(255, 60, 60), font=fs)
    for i in aligned:
        y = int(cys[i] * sc)
        d.rectangle([2, y - 3, 10, y + 3], fill=(0, 200, 0))
        d.text((14, y - 7), f"l{i} {len(byl[(page,i)])}/{wv[i]}",
               fill=(0, 220, 0), font=fs)
        for r in byl[(page, i)]:
            x0 = (r["cx"] - r["w"] / 2) * sc; x1 = (r["cx"] + r["w"] / 2) * sc
            yb = (r["cy"] + r["h"] / 2 + 3) * sc
            d.line([x0, yb, x1, yb], fill=(0, 160, 255), width=1)
    d.rectangle([0, 0, W_OUT, 22], fill=(0, 0, 0))
    d.text((6, 3), f"p{page}: {note} | red-label rows approximate",
           fill=(255, 255, 0), font=f)
    im.save(os.path.join(FIG, name), quality=82)
    print(name, os.path.getsize(os.path.join(FIG, name)) // 1024, "KB")

def canvas(w, h, title):
    im = Image.new("RGB", (w, h), (250, 250, 250))
    d = ImageDraw.Draw(im)
    d.text((10, 8), title, fill=(20, 20, 20), font=font(16))
    return im, d

def area_fig():
    med, lo, hi = [], [], []
    for v in range(29):
        a = np.array([r["area"] for r in rows if r["value"] == v])
        med.append(np.median(a)); lo.append(np.percentile(a, 16))
        hi.append(np.percentile(a, 84))
    im, d = canvas(900, 480,
                   "Ink area by rune VALUE (9,640 aligned runes): median, 16-84 pct band")
    x0, y0, x1, y1 = 60, 50, 880, 420
    d.line([x0, y1, x1, y1], fill=(0, 0, 0))
    mx = max(hi) * 1.05
    bw = (x1 - x0) / 29
    for v in range(29):
        bx = x0 + v * bw
        def yy(a): return y1 - (a / mx) * (y1 - y0)
        d.rectangle([bx + 3, yy(med[v]), bx + bw - 3, y1], fill=(60, 90, 200))
        d.line([bx + bw / 2, yy(lo[v]), bx + bw / 2, yy(hi[v])],
               fill=(200, 30, 30), width=2)
        d.text((bx + bw / 2 - 5, y1 + 4), str(v), fill=(0, 0, 0), font=font(12))
    d.text((x0, 26), "error bars are the 16-84 percentile band: a few % wide "
                     "(JPEG noise), not a channel", fill=(120, 30, 30), font=font(13))
    im.save(os.path.join(FIG, "area_by_value.png"))
    print("area_by_value.png", os.path.getsize(os.path.join(FIG, "area_by_value.png")) // 1024, "KB")

def frac_fig():
    im, d = canvas(900, 460,
                   "frac(cx) per value: arrows = circular mean (angle) with "
                   "resultant R as length; bottom = global octogram")
    cx, cy, R = 230, 230, 150
    d.ellipse([cx - R, cy - R, cx + R, cy + R], outline=(150, 150, 150))
    for v in range(29):
        f = np.array([r["fx"] for r in rows if r["value"] == v])
        z = np.exp(2j * np.pi * f).mean()
        ang = np.angle(z); rr = abs(z)
        x = cx + R * rr * np.cos(ang); y = cy - R * rr * np.sin(ang)
        d.line([cx, cy, x, y], fill=(60, 90, 200), width=3)
        d.text((cx + (R + 8) * np.cos(ang) - 4, cy - (R + 8) * np.sin(ang)),
               str(v), fill=(0, 0, 0), font=font(12))
    d.text((60, 400), "per-value R = 0.8-0.9 for most values: the sub-pixel "
           "x-centroid is a GLYPH FINGERPRINT, not a code", fill=(120, 30, 30),
           font=font(13))
    g = np.histogram(np.array([r["fx"] for r in rows]), bins=8, range=(0, 1))[0]
    bx0, by1, bw = 520, 380, 40
    mx = max(g) * 1.1
    uni = len(rows) / 8
    for k in range(8):
        h = (g[k] / mx) * 280
        d.rectangle([bx0 + k * (bw + 4), by1 - h, bx0 + (k + 1) * bw + 0,
                     by1], fill=(60, 90, 200))
        d.text((bx0 + k * (bw + 4) + 8, by1 + 4), f"{k}/8", font=font(12))
    d.line([bx0, by1 - (uni / mx) * 280, bx0 + 8 * (bw + 4),
            by1 - (uni / mx) * 280], fill=(0, 160, 0), width=2)
    d.text((bx0, 60), "global octogram (green = uniform)",
           fill=(20, 20, 20), font=font(13))
    im.save(os.path.join(FIG, "frac_cx.png"))
    print("frac_cx.png", os.path.getsize(os.path.join(FIG, "frac_cx.png")) // 1024, "KB")

if __name__ == "__main__":
    page_fig(0, "p0_coverage.jpg",
             "p0: green=aligned red=EXCLUDED (l0 header is RED-ink print, "
             "excluded by the registered red-ink rule, not faded)")
    page_fig(15, "p15_coverage.jpg",
             "worst page (28%): grid + ornaments contaminate the count gate")
    area_fig()
    frac_fig()
