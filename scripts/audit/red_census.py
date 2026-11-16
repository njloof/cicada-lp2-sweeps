#!/usr/bin/env python3
"""Red-ink census over the published LP2 pages (descriptive tabulation, not a
hypothesis test - no PREREG needed; analytic verdicts belong to dukotah
redrune + our STREAM_TAIL_EVIDENCE.md red section).

Per book page (0-57, image N+17.jpg):
  1. strict red mask (R>150, R-max(G,B)>80)  [same rule as the evidence pack]
  2. connected components, classified:
       matrix  - grid of small dots (rubrication section markers): position +
                 grid rows x cols + dot count
       tall    - drop-cap / title-band glyph (h > 160 px)
       glyph   - text-size red component (h 40..160): red rune OR red digit -
                 disambiguation is the owner's visual pass; each gets a crop
  3. ink-profile bands; items tagged with band index. NOTE: on rubricated
     pages band 0 is tall (drop-cap spans lines) and merges the drop-cap with
     the first ~3 text lines - flagged as title band, not split.
  4. digit-channel watchlist pages (book 10/15/36/37/38): every band cropped
     for the owner, red or not.

Output (gitignored): work/red_census/census.csv + crops/ + console summary.
Usage: python3 scripts/audit/red_census.py [--pages 0,3,6,...]  (default all)
"""
import argparse, csv, os
from collections import deque

import numpy as np
from PIL import Image

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
IMGS = os.path.join(ROOT, "sources", "ibotpeaches", "liber_primus")
OUT = os.path.join(ROOT, "work", "red_census")
DIGIT_PAGES = {10, 15, 36, 37, 38}  # printed-number channel (SOURCES.md + p15 find)


def comps(mask, minsz=8):
    """8-connected components; returns (x0,x1,y0,y1,npix,cy,cx)."""
    H, W = mask.shape
    seen = np.zeros_like(mask)
    out = []
    ys, xs = np.where(mask)
    for y0, x0 in zip(ys, xs):
        if seen[y0, x0]:
            continue
        seen[y0, x0] = True
        q = deque([(y0, x0)])
        pix, sy, sx = 0, 0, 0
        X0 = X1 = x0
        Y0 = Y1 = y0
        while q:
            y, x = q.popleft()
            pix += 1
            sy += y
            sx += x
            X0 = min(X0, x); X1 = max(X1, x)
            Y0 = min(Y0, y); Y1 = max(Y1, y)
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    ny, nx = y + dy, x + dx
                    if 0 <= ny < H and 0 <= nx < W and mask[ny, nx] and not seen[ny, nx]:
                        seen[ny, nx] = True
                        q.append((ny, nx))
        if pix >= minsz:
            out.append((X0, X1, Y0, Y1, pix, sy / pix, sx / pix))
    return out


def bands_of(L, x0=620, x1=1800, thr=8, min_h=35):
    px = (L < 135)
    ink = px[:, x0:x1:3].sum(axis=1)
    out, s = [], None
    for y, v in enumerate(ink):
        if v > thr and s is None:
            s = y
        elif v <= thr and s is not None:
            if y - s > min_h:
                out.append((s, y))
            s = None
    if s is not None:
        out.append((s, len(ink)))
    return out


def cluster_dots(dots, link=70):
    """Union dots whose centroids are within `link` px (chaining)."""
    n = len(dots)
    par = list(range(n))

    def find(i):
        while par[i] != i:
            par[i] = par[par[i]]
            i = par[i]
        return i

    for i in range(n):
        for j in range(i + 1, n):
            if abs(dots[i][5] - dots[j][5]) < link and abs(dots[i][6] - dots[j][6]) < link:
                a, b = find(i), find(j)
                if a != b:
                    par[a] = b
    groups = {}
    for i in range(n):
        groups.setdefault(find(i), []).append(dots[i])
    return list(groups.values())


def grid_dims(cs):
    ys = sorted(c[5] for c in cs)
    xs = sorted(c[6] for c in cs)
    rows = 1 + sum(1 for a, b in zip(ys, ys[1:]) if b - a > 12)
    cols = 1 + sum(1 for a, b in zip(xs, xs[1:]) if b - a > 12)
    return rows, cols


def band_of(bands, y):
    for k, (b0, b1) in enumerate(bands):
        if b0 <= y <= b1:
            return k
    return -1


def crop(im, x0, y0, x1, y1, path, pad=30, zoom=2):
    W, H = im.size
    c = im.crop((max(0, x0 - pad), max(0, y0 - pad), min(W, x1 + pad), min(H, y1 + pad)))
    c = c.resize((c.width * zoom, c.height * zoom), Image.LANCZOS)
    c.save(path)


def do_page(n, w):
    path = f"{IMGS}/{n + 17}.jpg"
    im = Image.open(path).convert("RGB")
    a = np.asarray(im)
    R, G, B = a[:, :, 0].astype(int), a[:, :, 1].astype(int), a[:, :, 2].astype(int)
    red = (R > 150) & (R - np.maximum(G, B) > 80)
    total_red = int(red.sum())
    L = np.asarray(im.convert("L"), np.uint8)
    bands = bands_of(L)
    rows = []
    if total_red == 0 and n not in DIGIT_PAGES:
        return rows, 0, bands
    cs = comps(red)
    dots = [c for c in cs if (c[1] - c[0]) <= 30 and (c[3] - c[2]) <= 30]
    big = [c for c in cs if not ((c[1] - c[0]) <= 30 and (c[3] - c[2]) <= 30)]

    mi = 0
    for g in cluster_dots(dots):
        if len(g) < 6:
            continue  # stray specks / antialiasing, not an ornament matrix
        x0 = min(c[0] for c in g); x1 = max(c[1] for c in g)
        y0 = min(c[2] for c in g); y1 = max(c[3] for c in g)
        r, cld = grid_dims(g)
        mi += 1
        rows.append(dict(page=n, kind="matrix", y0=y0, y1=y1, x0=x0, x1=x1,
                         dots=len(g), rows=r, cols=cld,
                         band=band_of(bands, (y0 + y1) // 2), note=""))
        crop(im, x0, y0, x1, y1, f"{OUT}/crops/p{n:02d}_matrix{mi}.png")
    bi = 0
    for c in big:
        x0, x1, y0, y1, pix = c[0], c[1], c[2], c[3], c[4]
        h = y1 - y0
        kind = "tall" if h > 160 else "glyph"
        bi += 1
        rows.append(dict(page=n, kind=kind, y0=y0, y1=y1, x0=x0, x1=x1, dots="",
                         rows="", cols="", band=band_of(bands, (y0 + y1) // 2),
                         note="title-band drop-cap" if kind == "tall" else "red rune OR digit - owner crop check"))
        crop(im, x0, y0, x1, y1, f"{OUT}/crops/p{n:02d}_{kind}{bi}.png")
    if n in DIGIT_PAGES:
        for k, (b0, b1) in enumerate(bands):
            rp = int(red[b0:b1].sum())
            crop(im, 560, b0, 1900, b1, f"{OUT}/crops/p{n:02d}_digitband{k}.png", pad=6, zoom=1)
            rows.append(dict(page=n, kind="digit_band", y0=b0, y1=b1, x0=560, x1=1900,
                             dots="", rows="", cols="", band=k,
                             note=f"red_px={rp} (owner reads digits)"))
    return rows, total_red, bands


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pages", default=",".join(str(i) for i in range(58)))
    args = ap.parse_args()
    os.makedirs(f"{OUT}/crops", exist_ok=True)
    allrows = []
    for n in [int(x) for x in args.pages.split(",")]:
        rows, rpx, bands = do_page(n, w=None)
        nb = len(bands)
        tall0 = nb and bands and (bands[0][1] - bands[0][0]) > 200
        items = [r["kind"] for r in rows]
        if rpx or n in DIGIT_PAGES:
            print(f"p{n:02d}: red {rpx:6d}px  bands {nb}{' (tall title band)' if tall0 else ''}  "
                  f"matrix x{items.count('matrix')}  tall x{items.count('tall')}  "
                  f"glyph x{items.count('glyph')}  digit_bands x{items.count('digit_band')}")
        allrows += rows
    with open(f"{OUT}/census.csv", "w", newline="") as f:
        wr = csv.DictWriter(f, fieldnames=["page", "kind", "y0", "y1", "x0", "x1",
                                           "dots", "rows", "cols", "band", "note"])
        wr.writeheader()
        wr.writerows(allrows)
    print(f"\nwrote {OUT}/census.csv ({len(allrows)} rows) + crops/ ({len(os.listdir(f'{OUT}/crops'))} files)")


if __name__ == "__main__":
    main()
