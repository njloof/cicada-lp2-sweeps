#!/usr/bin/env python3
"""Transcription-audit harness (docs/TRANSCRIPTION_AUDIT.md item 1).

For each page: split the full-res published image (ibotpeaches N+17) into
horizontal INK STRIPS by projection profile, pair each strip with the
transcribed line from data/pages/, and emit a visual-pass checklist.
Band count vs transcribed line count is itself a first structural signal:
a mismatch means the transcription's line segmentation disagrees with the
page's visible layout (audit priority).

Output (gitignored work/): work/audit/page_NN/strip_XX.png + checklist.md
Usage: python3 scripts/audit/make_checklist.py [--pages 49,7,12,...]
"""
import argparse, hashlib, os, sys

import numpy as np
from PIL import Image

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
sys.path.insert(0, ROOT)
from core.validate import GEMATRIA, N as Q  # noqa: E402
from core.kernel import Q as _Q  # noqa: E402,F401

GLYPH = [g[0] for g in GEMATRIA]
PRIME = [g[2] for g in GEMATRIA]
GEMATRIA_D = set(GLYPH)
IMGS = os.path.join(ROOT, "sources", "ibotpeaches", "liber_primus")
OUT = os.path.join(ROOT, "work", "audit")

# Expected confusion families (audit doc + PARABLE pos-80 precedent) + full table
CONFUSION = [("ᚦ", "ᛈ"), ("ᚫ", "ᚪ"), ("ᛖ", "ᚣ"), ("ᚻ", "ᛁ"), ("ᛞ", "ᛏ"), ("ᛗ", "ᛖ")]


def is_prime(n):
    if n < 2:
        return False
    d = 2
    while d * d <= n:
        if n % d == 0:
            return False
        d += 1
    return True


def ink_profile(gray, min_ink_frac=0.002):
    med = np.median(gray)
    mad = np.median(np.abs(gray - med)) + 1.0
    ink = (gray < med - 3.5 * mad).mean(axis=1)
    rows = np.where(ink > min_ink_frac)[0]
    return ink, int(rows[0]), int(rows[-1])


def fft_period(prof):
    f = np.abs(np.fft.rfft(prof - prof.mean()))
    k = int(np.argmax(f[2:])) + 2
    return len(prof) / k


def valley_cuts(prof, H):
    """H-1 cut points: near each nominal k*h/H, take the deepest valley
    within +-0.4 step. Works on dense grids where lines never fully touch
    zero over wide gaps."""
    h = len(prof)
    step = h / H
    smooth = np.convolve(prof, np.ones(5) / 5, mode="same")
    cuts = []
    for k in range(1, H):
        lo = max(0, int(k * step - 0.4 * step))
        hi = min(h - 1, int(k * step + 0.4 * step))
        cuts.append(lo + int(np.argmin(smooth[lo:hi + 1])))
    return cuts


KRIS = os.path.join(ROOT, "sources", "dukotah", "liber-primus", "data", "krisyotam_runes.txt")


def seg_for_page(n):
    """Book page -> stream segment index. Confirmed 2026-11-15 (owner's p51
    read, exact pairing): the runes-only extraction into krisyotam dropped
    the root's empty-of-runes p50 slot (the rtkd master HAS a slot 50 -
    the token table, 0 runes), so segments 50-56 are book pages 51-57.
    Book p50 itself has no segment in the rune stream."""
    if n == 50:
        raise ValueError("book p50 has no stream segment (runeless token "
                         "page; its empty slot was dropped in extraction - "
                         "the +1 tail shift)")
    return n if n <= 49 else n - 1


def page_lines(n):
    """Rune indices per line for BOOK page n, read straight from the pinned
    krisyotam stream (data/pages/ names are off by one on the tail - the
    relabel there is a separate pending decision; the stream + seg_for_page
    is the authoritative book->segment map)."""
    seg = open(KRIS, encoding="utf-8").read().split("%")[seg_for_page(n)]
    idx = {g: i for i, (g, _, _) in enumerate(GEMATRIA)}
    return [[idx[c] for c in ln if c in idx]
            for ln in seg.split("/") if any(c in idx for c in ln)]


def page_lines_with_seps(n):
    """Raw krisyotam lines WITH word dividers '-' and sentence dots '.'
    preserved (the community stream carries them; data/pages tokenization
    drops them). The visual pass verifies divider fidelity — this is the
    only independent check on them (single-root caveat applies)."""
    seg = open(KRIS, encoding="utf-8").read().split("%")[seg_for_page(n)]
    out = []
    for ln in seg.split("/"):  # NB: split("/")[0] IS line 1 - a [1:] here
        #  silently paired every strip with the next line's separators (found
        #  2026-11-15 by owner's p51 read; every page was off by one line)
        s = "".join(c for c in ln.strip() if not c.isspace())
        if any(c in GEMATRIA_D for c in s):  # keep in lockstep with page_lines
            out.append(s)
    return out


# Mixed-content pages (verified by full-page inspection 2026-11-15): the FFT
# pitch pairing above assumes the page is all rune lines - false on the tail,
# where token tables interleave (owner's p51 pass caught this: transcriptions
# were paired to token rows from the top while the real rune lines sat
# unpaired at the bottom). Explicit per-row kinds, measured band-by-band.
ROW_LAYOUT = {
    49: ['rune'] * 3 + ['token'] * 10,          # 66.jpg: 3 rune lines, 10x8 table
    51: ['token'] * 9 + ['rune'] * 4,           # 68.jpg: 9x8 table, 4 rune lines
    55: ['rune'] * 4 + ['plate'],               # 72.jpg: 4 lines + matrix/tree/plate
}
KIND_NOTE = {'token': 'base-60 TOKEN row (pp49-51 payload; not in the rune stream)',
             'plate': 'ornament/plate (red matrix, tree diagram, cicada art)'}
VERIFIED = {  # book page -> note shown on every rune strip
    51: "VERIFIED 2026-11-15 by owner's from-scratch read == stream, "
        "92/92 runes + all dividers exact (work/audit/p51_runes/READ.md) "
        "- no re-read needed",
}


def ink_bands(gray, x0=620, x1=1800, thr=8, min_h=35):
    """Visible content row bands via horizontal-ink profile (central window)."""
    px = (gray > 120)
    ink = px[:, x0:x1:3].sum(axis=1)
    bands, start = [], None
    for y, s in enumerate(ink):
        if s > thr and start is None:
            start = y
        elif s <= thr and start is not None:
            if y - start > min_h:
                bands.append((start, y))
            start = None
    if start is not None:
        bands.append((start, len(ink)))
    return bands


def do_page(n, pad=24):
    img_path = os.path.join(IMGS, f"{n + 17}.jpg")
    lines = page_lines(n)
    H = len(lines)
    im = Image.open(img_path)  # keep RGB: red-ink glyphs are an open
    #  channel (dukotah 4/6) - strips must show color, profile uses L
    a = np.asarray(im.convert("L"), dtype=np.float32)
    sha1 = hashlib.sha1(open(img_path, "rb").read()).hexdigest()[:12]
    d = os.path.join(OUT, f"page_{n:02d}")
    os.makedirs(d, exist_ok=True)
    rows = []
    if n in ROW_LAYOUT:  # explicit layout: pair only 'rune' rows with stream lines
        bands = ink_bands(np.asarray(im.convert("L"), dtype=np.uint8))
        kinds = ROW_LAYOUT[n]
        if len(bands) != len(kinds):
            raise RuntimeError(f"p{n}: measured {len(bands)} bands, layout says "
                               f"{len(kinds)} - re-inspect the page before trusting this")
        per = step = float('nan')
        ok = True
        li = 0
        for s, ((a0, a1), kind) in enumerate(zip(bands, kinds)):
            im.crop((0, max(0, a0 - pad), a.shape[1], min(a.shape[0], a1 + pad))) \
              .save(os.path.join(d, f"strip_{s:02d}.png"))
            if kind == 'rune':
                rows.append((s, lines[li], a1 - a0, f"measured band; stream line {li + 1}"))
                li += 1
            else:
                rows.append((s, None, a1 - a0, KIND_NOTE[kind]))
        assert li == H, f"p{n}: {H} stream lines but {li} rune bands"
    else:
        ink, y0c, y1c = ink_profile(a)
        prof = ink[y0c:y1c + 1]
        per = fft_period(prof)
        step = (y1c - y0c) / H
        ok = abs(per - step) / step < 0.05  # visible line pitch agrees with H
        Hi = max(1, round((y1c - y0c) / per))  # visible line count
        ns = H if ok else Hi  # cut by visible rows when they disagree
        cuts = valley_cuts(prof, ns)
        edges = [0] + cuts + [len(prof)]
        for s in range(ns):
            a0, a1 = y0c + edges[s], y0c + edges[s + 1]
            im.crop((0, max(0, a0 - pad), a.shape[1], min(a.shape[0], a1 + pad))) \
              .save(os.path.join(d, f"strip_{s:02d}.png"))
            if s < H:
                rows.append((s, lines[s], a1 - a0, "valley-cut"))
            else:
                rows.append((s, None, a1 - a0, "**NO TRANSCRIBED LINE — record glyphs**"))
    with open(os.path.join(d, "checklist.md"), "w") as f:
        f.write(f"# Visual audit checklist — LP2 page {n}\n\n")
        f.write(f"Image: `{os.path.relpath(img_path, ROOT)}` (sha1 {sha1}…)\n\n")
        if n in ROW_LAYOUT:
            f.write(f"Layout: **explicit measured bands** (mixed-content page: "
                    f"{ROW_LAYOUT[n].count('rune')} rune lines + non-rune rows; "
                    f"FFT pitch pairing does not apply)\n\n")
        else:
            f.write(f"Visible line pitch (FFT): **{per:.1f}px** vs content-height/{H} = "
                    f"**{step:.1f}px** → {'MATCH' if ok else f'**MISMATCH — visible rows ≈ {Hi}, transcribed {H}: top priority**'}\n\n")
        f.write(f"Runes: {sum(len(l) for l in lines)}; line sums primality: "
                f"{sum(1 for l in lines if is_prime(sum(PRIME[v] for v in l)))}/{H} prime\n\n")
        f.write("For each strip: read the runes off the image, compare to the "
                "transcription, mark OK or list (position, seen-vs-recorded).\n\n")
        if n in VERIFIED:
            f.write(f"> **{VERIFIED[n]}**\n\n")
        pos = 0
        for s, ln, bh, how in rows:
            if ln is None:
                f.write(f"## strip {s:02d} — {how}\n\n")
                f.write(f"![strip](strip_{s:02d}.png)\n\n")
                if "NO TRANSCRIBED LINE" in how:
                    f.write(f"recorded glyphs: ____________\n\n")
                continue
            seps = page_lines_with_seps(n)
            txt = seps[s] if s < len(seps) else "".join(GLYPH[v] for v in ln)
            nd = txt.count("-") + txt.count(".")
            ssum = sum(PRIME[v] for v in ln)
            f.write(f"## strip {s:02d} — positions {pos}–{pos + len(ln) - 1} "
                    f"(len {len(ln)}, sum {ssum}{' PRIME' if is_prime(ssum) else ''}) [{how}]\n\n")
            f.write(f"![strip](strip_{s:02d}.png)\n\n")
            f.write(f"`{txt}`\n\n")
            f.write(f"verdict: ☐ OK   ☐ diffs: ____________\n\n")
            pos += len(ln)
    return n, per, H, ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pages", default="49,7,12,4,6,10,32,35,45")
    args = ap.parse_args()
    print("confusion-pair legend:",
          " ".join(f"{a}/{b}" for a, b in CONFUSION), "\n")
    mism = []
    for n in [int(x) for x in args.pages.split(",")]:
        n, per, H, ok = do_page(n)
        print(f"page {n:2d}: pitch {per:6.1f}px vs h/H (lines {H:2d})  {'ok' if ok else 'MISMATCH'}"
              f"  -> work/audit/page_{n:02d}/checklist.md")
        if not ok:
            mism.append(n)
    print(f"\nband/line agreement: {len(args.pages.split(',')) - len(mism)}"
          f"/{len(args.pages.split(','))}; mismatches (audit priority): {mism or 'none'}")


if __name__ == "__main__":
    main()
