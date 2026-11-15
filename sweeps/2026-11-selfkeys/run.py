#!/usr/bin/env python3
"""Campaign #8 observed sweep: self-derived value keys (LS/VT/CF).
PREREG registered 2026-11-15 before output. Streams full CSVs to
work/selfkeys/, keeps top-100k heap + sha256 (house policy)."""
import argparse, hashlib, heapq, json, os, sys, time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import selfkeys as SK  # noqa: E402
from core.kernel import Q  # noqa: E402
from core.validate import flat  # noqa: E402

WORK = os.path.join(HERE, "..", "..", "work", "selfkeys")
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
        self.f.write(s)
        self.sha.update(s.encode())
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


def recompute_both(fam, target, tag, off):
    """mask=both chi2 for a recorded row, from the REAL corpus page."""
    A = np.array(flat(target), dtype=np.int16)
    m = len(A)
    K = SK.pad_by_tag(tag, target, A)
    if K is None:
        return -1.0, 0
    if fam == "LS":
        keep = (A != 0) & (K != 0)
        vals = (A - K)[keep] % Q
        nn = int(keep.sum())
        return (SK.chi2_of(vals) if nn >= 50 else -1.0), nn
    o = off
    i0, i1 = max(0, o), min(m, len(K) + o)
    D = (A[i0:i1] - K[i0 - o:i1 - o]) % Q
    keep = (A[i0:i1] != 0) & (K[i0 - o:i1 - o] != 0)
    vals = D[keep]
    if len(vals) < 50:
        return -1.0, len(vals)
    return SK.chi2_of(vals), len(vals)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fams", default="LS,VT,CF")
    ap.add_argument("--floor", type=float, default=40.0)
    args = ap.parse_args()
    fams = args.fams.split(",")
    os.makedirs(RES, exist_ok=True)

    # Pre-output degeneracy check (PREREG): no unexplained zero-pileups.
    flags = SK.zero_check(SK.TARGETS)
    with open(os.path.join(RES, "zero_check.json"), "w") as f:
        json.dump(flags, f, indent=2)
    print(f"zero_check: {len(flags)} flagged (>0.15 D-zero, needs mechanism)", flush=True)
    for fl in flags[:10]:
        print("  FLAG", fl, flush=True)

    sinks = {}
    t0 = time.time()
    for fam, n, tag, off, nn, c2 in SK.iter_rows(fams, SK.TARGETS):
        s = sinks.get(fam)
        if s is None:
            s = sinks[fam] = Sink(fam, args.floor)
        s.add(n, tag, off, nn, c2)
        if s.windows % 1000000 < 1:
            print(f"[{time.time()-t0:5.1f}s] {fam} windows={s.windows:,} max={s.max[0]:.2f}", flush=True)
    obs_rows, leaders = [], []
    for fam in fams:
        if fam not in sinks:
            continue
        s = sinks[fam]
        sha = s.close()
        obs_rows.append((fam, s.windows, s.rows, s.max[0], s.max[1], sha))
        print(f"{fam}: windows={s.windows:,} rows>=floor={s.rows:,} max={s.max[0]:.2f} "
              f"argmax={s.max[1]} sha={sha[:12]} [{time.time()-t0:.0f}s]", flush=True)
        for c2, tg, tag, off, nn in sorted(s.heap, reverse=True)[:20]:
            c2b, nnb = recompute_both(fam, tg, tag, off)
            leaders.append((fam, tg, tag, off, c2, nn, c2b, nnb))
    with open(os.path.join(RES, "obs_maxima.csv"), "w") as f:
        f.write("family,windows,rows_ge_floor,chi2_max,target,key,offset,n_valid,full_csv_sha256\n")
        for fam, w, r, c2, am, sha in obs_rows:
            tg, tag, off, nn = am
            f.write(f"{fam},{w},{r},{c2:.4f},{tg},{tag},{off},{nn},{sha}\n")
    with open(os.path.join(RES, "leaders_both.csv"), "w") as f:
        f.write("family,target,key,offset,chi2_tgt,n_tgt,chi2_both,n_both\n")
        for row in leaders:
            f.write(f"{row[0]},{row[1]},{row[2]},{row[3]},{row[4]:.4f},{row[5]},{row[6]:.4f},{row[7]}\n")
    with open(os.path.join(RES, "window_counts.json"), "w") as f:
        json.dump({fam: {"windows": w, "rows_ge_floor": r} for fam, w, r, *_ in obs_rows}, f, indent=2)
    print(f"total {sum(w for _, w, *_ in obs_rows):,} windows in {time.time()-t0:.0f}s", flush=True)


if __name__ == "__main__":
    main()
