#!/usr/bin/env python3
"""Campaign #7 observed sweep: number channels as additive keys.
PREREG registered 2026-11-15 before output. Streams full CSVs to
work/number-channels/, keeps top-100k heap + sha256 (house policy)."""
import argparse, hashlib, heapq, json, os, sys, time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
import numkeys as NK  # noqa: E402
from core.kernel import Q  # noqa: E402
from core.validate import flat  # noqa: E402

WORK = os.path.join(HERE, "..", "..", "work", "number-channels")
RES = os.path.join(HERE, "results")
HDR = "family,target,key,offset,n_valid,chi2"


class Sink:
    def __init__(self, fam, floor):
        os.makedirs(WORK, exist_ok=True)
        self.path = os.path.join(WORK, f"sweep_{fam}.csv")
        self.f = open(self.path, "w")
        self.f.write(HDR + "\n")
        self.sha = hashlib.sha256((HDR + "\n").encode())
        self.heap, self.floor, self.rows, self.windows = [], floor, 0, 0
        self.max = (-1.0, None)

    def add(self, target, key, off, nn, c2):
        self.windows += 1
        if c2 < self.floor:
            return
        self.rows += 1
        s = f"{target},{key},{off},{nn},{c2:.4f}\n"
        b = s.encode()
        self.f.write(s)
        self.sha.update(b)
        item = (c2, target, key, off, nn)
        if len(self.heap) < 100000:
            heapq.heappush(self.heap, item)
        elif item > self.heap[0]:
            heapq.heapreplace(self.heap, item)
        if c2 > self.max[0]:
            self.max = (c2, (target, key, off, nn))

    def close(self):
        self.f.close()
        return self.sha.hexdigest()


def recompute_both(fam, target, keyid, off, variants):
    """mask=both chi2 for a recorded row."""
    A = np.array(NK.flat(target), dtype=np.int16)
    m = len(A)
    if fam == "Vp":
        key = NK.key_from_id(keyid, variants)
        K = key[(np.arange(m) - off) % len(key)]
        return NK.chi2_page(A, K, mask_both=True)
    if fam == "R":
        c, b = map(int, keyid[1:].split("."))
        pad = NK.ramp_pad(c, b, m)
    else:
        pad = NK.tiled(NK.key_from_id(keyid, variants), m)
    o = off
    i0, i1 = max(0, o), min(m, len(pad) + o)
    D = (A[i0:i1] - pad[i0 - o:i1 - o]) % Q
    keep = (A[i0:i1] != 0) & (pad[i0 - o:i1 - o] != 0)
    vals = D[keep]
    if len(vals) < 50:
        return -1.0, len(vals)
    h = np.bincount(vals, minlength=Q).astype(np.float64)
    nn = float(len(vals))
    return (Q / nn) * float((h * h).sum()) - nn, len(vals)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fams", default="Vp,Vs,R,D")
    ap.add_argument("--floor", type=float, default=40.0)
    args = ap.parse_args()
    fams = args.fams.split(",")
    variants, targets = NK.variants_and_targets()
    os.makedirs(RES, exist_ok=True)
    print(f"variants={len(variants)} targets={len(targets)} fams={fams}", flush=True)
    sinks, counts = {}, {}
    t0 = time.time()
    for fam, n, kid, off, nn, c2 in NK.iter_rows(fams, variants, targets):
        s = sinks.get(fam)
        if s is None:
            s = sinks[fam] = Sink(fam, args.floor)
        s.add(n, kid, off, nn, c2)
        done = time.time() - t0
        if s.windows % 2000000 < 1:
            print(f"[{done:6.1f}s] {fam} windows={s.windows:,} rows={s.rows:,} max={s.max[0]:.2f}", flush=True)
    obs_rows, leaders = [], []
    for fam in fams:
        s = sinks[fam]
        sha = s.close()
        obs_rows.append((fam, s.windows, s.rows, s.max[0], s.max[1], sha))
        print(f"{fam}: windows={s.windows:,} rows>=floor={s.rows:,} max={s.max[0]:.2f} "
              f"argmax={s.max[1]} sha={sha[:12]} [{time.time()-t0:.0f}s]", flush=True)
        top = sorted(s.heap, reverse=True)[:20]
        for c2, tg, kid, off, nn in top:
            c2b, nnb = recompute_both(fam, tg, kid, off, variants)
            leaders.append((fam, tg, kid, off, c2, nn, c2b, nnb))
    with open(os.path.join(RES, "obs_maxima.csv"), "w") as f:
        f.write("family,windows,rows_ge_floor,chi2_max,target,key,offset,n_valid,full_csv_sha256\n")
        for fam, w, r, c2, am, sha in obs_rows:
            tg, kid, off, nn = am
            f.write(f"{fam},{w},{r},{c2:.4f},{tg},{kid},{off},{nn},{sha}\n")
    with open(os.path.join(RES, "leaders_both.csv"), "w") as f:
        f.write("family,target,key,offset,chi2_tgt,n_tgt,chi2_both,n_both\n")
        for row in leaders:
            fam, tg, kid, off, c2, nn, c2b, nnb = row
            f.write(f"{fam},{tg},{kid},{off},{c2:.4f},{nn},{c2b:.4f},{nnb}\n")
    with open(os.path.join(RES, "window_counts.json"), "w") as f:
        json.dump({fam: {"windows": w, "rows_ge_floor": r} for fam, w, r, *_ in obs_rows}, f, indent=2)
    print(f"total {sum(w for _, w, *_ in obs_rows):,} windows in {time.time()-t0:.0f}s", flush=True)


if __name__ == "__main__":
    main()
