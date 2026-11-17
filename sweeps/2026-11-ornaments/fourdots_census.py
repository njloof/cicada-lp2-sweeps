import csv, time
import numpy as np
from PIL import Image

def _find(p, i):
    while p[i] != i:
        p[i] = p[p[i]]; i = p[i]
    return i

def cc_dots(black):
    H, W = black.shape
    parent = [0]
    lab = np.zeros((H, W), np.int32)
    prev = []
    for y in range(H):
        row = black[y]
        if not row.any():
            prev = []; continue
        d = np.flatnonzero(np.diff(np.concatenate(([0], row.view(np.int8), [0]))))
        starts, ends = d[0::2], d[1::2]
        cur = []
        for x0, x1 in zip(starts, ends):
            cands = {lb for px0, px1, lb in prev if x0 - 1 <= px1 and px0 <= x1}
            if cands:
                lb = min(_find(parent, c) for c in cands)
                for c in cands:
                    r1, r2 = _find(parent, lb), _find(parent, c)
                    if r1 != r2: parent[max(r1, r2)] = min(r1, r2)
            else:
                parent.append(len(parent)); lb = len(parent) - 1
            lab[y, x0:x1] = lb
            cur.append((int(x0), int(x1 - 1), lb))
        prev = cur
    ys, xs = np.nonzero(black)
    roots = np.array([_find(parent, i) for i in range(len(parent))], np.int32)
    lb = roots[lab[ys, xs]]
    keep = lb != 0
    ys, xs, lb = ys[keep], xs[keep], lb[keep]
    u, inv = np.unique(lb, return_inverse=True)
    n = len(u)
    area = np.bincount(inv)
    x0 = np.full(n, 1 << 30); x1 = np.full(n, -1); y0 = x0.copy(); y1 = x1.copy()
    np.minimum.at(x0, inv, xs); np.maximum.at(x1, inv, xs)
    np.minimum.at(y0, inv, ys); np.maximum.at(y1, inv, ys)
    w = x1 - x0 + 1; h = y1 - y0 + 1
    ok = (w >= 5) & (w <= 30) & (h >= 5) & (h <= 30) & (area >= 0.4 * w * h)
    cx = np.bincount(inv, weights=xs) / area
    cy = np.bincount(inv, weights=ys) / area
    return list(zip(cx[ok].tolist(), cy[ok].tolist()))

def clusters(dots):
    res, used = [], set()
    n = len(dots)
    for i in range(n):
        if i in used: continue
        grp = [j for j in range(n) if j not in used and abs(dots[j][0]-dots[i][0]) < 55 and abs(dots[j][1]-dots[i][1]) < 55]
        if len(grp) == 4:
            xs = [dots[j][0] for j in grp]; ys = [dots[j][1] for j in grp]
            if max(xs)-min(xs) >= 18 and max(ys)-min(ys) >= 18:
                res.append((int(sum(xs)/4), int(sum(ys)/4))); used.update(grp)
    return res

rows = []
for p in range(58):
    if p == 50: continue
    a = np.asarray(Image.open(f'sources/ibotpeaches/liber_primus/{p+17:02d}.jpg').convert('RGB')).astype(int)
    black = (a[:,:,0] < 120) & (a[:,:,1] < 120) & (a[:,:,2] < 120)
    for x, y in clusters(cc_dots(black)):
        rows.append((p, x, y))
    print(f'p{p} cum={len(rows)}', flush=True)
with open('work/scratch/fourdots.csv', 'w') as f:
    w = csv.writer(f); w.writerow(['page','x','y']); w.writerows(rows)
print('total', len(rows))
