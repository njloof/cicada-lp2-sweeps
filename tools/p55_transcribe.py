#!/usr/bin/env python3
"""LP2 page 55 — template-matching transcription (EXPERIMENTAL).

Builds glyph templates from the 55 VERIFIED pages (image + known rune labels),
validates the classifier by cross-validation on held-out known pages, and only
then classifies page 55 (72.jpg). Output carries per-glyph confidence; the
transcription is usable ONLY as an auxiliary pad candidate, never as a target,
and only if held-out accuracy is high enough to trust.

Pipeline: grayscale -> threshold -> line bands (row projection, central window)
-> connected components per band -> drop word-dots (small) -> merge split glyphs
-> normalize to 48x48 -> nearest-template by centered correlation.
Run: python3 p55_transcribe.py
"""
import numpy as np, os, sys
from PIL import Image
from collections import deque

HERE = os.path.dirname(os.path.abspath(__file__))          # tools/
ROOT = os.path.dirname(HERE)
IBOT = f"{ROOT}/sources/ibotpeaches/liber_primus"
Q = 29
RUNES = "ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛄᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛟᛞᚪᚫᚣᛡᛠ"
SZ = 48

def load_bands(path, x0=560, x1=1830, thr=40):
    im = np.array(Image.open(path).convert("L"))
    dark = im < 128
    rp = dark[:, x0:x1].sum(1)
    bands, y, inb = [], 0, False
    for i, v in enumerate(rp):
        if v > thr and not inb: inb, y = True, i
        elif v <= thr and inb:
            inb = False
            if i - y > 20: bands.append((y, i))
    return im, bands

def components(mask):
    """4-connected CC labels; returns list of (ys, xs) boxes."""
    lab = np.zeros(mask.shape, dtype=np.int32); cur = 0; out = []
    H, W = mask.shape
    for r in range(H):
        for c in range(W):
            if mask[r, c] and lab[r, c] == 0:
                cur += 1; q = deque([(r, c)]); lab[r, c] = cur
                pix = [(r, c)]
                while q:
                    y, x = q.popleft()
                    for dy, dx in ((1,0),(-1,0),(0,1),(0,-1)):
                        ny, nx = y+dy, x+dx
                        if 0 <= ny < H and 0 <= nx < W and mask[ny, nx] and lab[ny, nx] == 0:
                            lab[ny, nx] = cur; q.append((ny, nx)); pix.append((ny, nx))
                ys = np.array([p[0] for p in pix]); xs = np.array([p[1] for p in pix])
                out.append((ys.min(), ys.max(), xs.min(), xs.max(), len(pix)))
    return out

def glyphs_from_band(im, band, expected=None):
    """Return ordered glyph masks for one line band; None if count can't be reconciled."""
    y0, y1 = band
    sub = im[y0:y1, :] < 128
    comps = components(sub)
    big = [c for c in comps if (c[1]-c[0]) >= 28]          # drop word-dots
    big.sort(key=lambda c: c[2])
    # merge components whose x-ranges overlap (split glyphs like ᛄ two diamonds)
    merged = []
    for c in big:
        if merged and c[2] <= merged[-1][3] + 3:
            p = merged[-1]
            merged[-1] = (min(p[0],c[0]), max(p[1],c[1]), min(p[2],c[2]), max(p[3],c[3]), p[4]+c[4])
        else: merged.append(list(c) if isinstance(c, tuple) else c)
    if expected is not None and len(merged) != expected:
        return None
    out = []
    for (r0, r1, c0, c1, _) in merged:
        g = sub[r0:r1+1, c0:c1+1]
        out.append(normalize(g))
    return out

def normalize(g):
    h, w = g.shape
    s = SZ / max(h, w)
    im = Image.fromarray((g*255).astype(np.uint8)).resize((max(1,int(w*s)), max(1,int(h*s))))
    a = np.array(im) > 100
    out = np.zeros((SZ, SZ))
    oh, ow = a.shape
    r0, c0 = (SZ-oh)//2, (SZ-ow)//2
    out[r0:r0+oh, c0:c0+ow] = a
    v = out.ravel(); v = v - v.mean()
    n = np.linalg.norm(v)
    return v / n if n > 0 else v

def page_lines(n):
    return [l.split() for l in open(f"{ROOT}/data/pages/lp2_{n:02d}.txt") if l.strip()]

def build_templates(pages, skip=()):
    X, Y = [], []
    for n in pages:
        if n in skip: continue
        im, bands = load_bands(f"{IBOT}/{n+17:02d}.jpg")
        lines = page_lines(n)
        if len(bands) < len(lines): continue
        # take the LAST len(lines) bands before the art: text bands are contiguous
        # find the contiguous run of bands matching line count with plausible heights
        best = None
        for s in range(len(bands)-len(lines)+1):
            seg = bands[s:s+len(lines)]
            gaps = [seg[i+1][0]-seg[i][1] for i in range(len(seg)-1)]
            if all(0 <= g < 140 for g in gaps) and all(b[1]-b[0] > 60 for b in seg):
                best = seg; break
        if best is None: continue
        for band, line in zip(best, lines):
            gs = glyphs_from_band(im, band, expected=len(line))
            if gs is None: continue
            for g, idx in zip(gs, line):
                X.append(g); Y.append(int(idx))
    return np.array(X), np.array(Y)

def classify(q, X, Y, k=5):
    sims = X @ q
    order = np.argsort(-sims)
    votes = {}
    for i in order[:k]: votes[Y[i]] = votes.get(Y[i], 0) + sims[i]
    best = max(votes, key=votes.get)
    top1, top2 = sims[order[0]], sims[order[1]]
    return best, float(sims[order[0]]), float(top1 - top2)

def main():
    known = [n for n in range(55) if os.path.exists(f"{ROOT}/data/pages/lp2_{n:02d}.txt")]
    print(f"building templates from {len(known)} verified pages ...")
    X, Y = build_templates(known)
    print(f"templates: {len(X)} glyphs, coverage per rune: "
          f"{np.bincount(Y, minlength=Q).min()}..{np.bincount(Y, minlength=Q).max()}")

    # 2-fold CV on known pages
    rng = np.random.default_rng(1); perm = rng.permutation(known)
    half = set(perm[:len(known)//2])
    Xa, Ya = build_templates(known, skip=half)
    Xb, Yb = build_templates(sorted(half))
    correct = tot = 0; accs = []
    for g, y in zip(Xb, Yb):
        pred, sim, marg = classify(g, Xa, Ya)
        correct += (pred == y); tot += 1
    print(f"held-out glyph accuracy: {correct}/{tot} = {correct/tot:.3f}")

    if correct/tot < 0.95:
        print("ACCURACY TOO LOW — page 55 transcription ABANDONED (stays excluded).")
        return

    # classify page 55
    im, bands = load_bands(f"{IBOT}/72.jpg")
    text_bands = [b for b in bands if b[1]-b[0] > 60][:4]
    print("p55 bands:", text_bands)
    out, confs = [], []
    for band in text_bands:
        gs = glyphs_from_band(im, band)
        line = []
        for g in gs:
            pred, sim, marg = classify(g, X, Y)
            line.append((pred, sim, marg))
        out.append(line)
        print(f" line {len(line)} glyphs: " +
              "".join(RUNES[p] if m > 0.05 else "?" for p, s, m in line))
    conf = [m for ln in out for _, _, m in ln]
    print(f"total glyphs: {len(conf)}, median margin {np.median(conf):.3f}, "
          f"low-confidence (<0.05): {sum(m < 0.05 for m in conf)}")
    with open(f"{ROOT}/work/p55/transcription.txt", "w") as f:
        for ln in out:
            f.write(" ".join(f"{RUNES[p]}{i}" for i, (p, s, m) in enumerate(ln)) + "\n")
    print("wrote work/p55/transcription.txt (EXPERIMENTAL — see REPORT.md)")

if __name__ == "__main__":
    main()
