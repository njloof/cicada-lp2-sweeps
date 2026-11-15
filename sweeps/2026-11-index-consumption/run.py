#!/usr/bin/env python3
"""Campaign 2026-11-index-consumption — sweep CLI (implements PREREG.md exactly).

Families (registered 2026-11-14 before any output):
  P  drop-decimation pads S[b::a], a in 2..28, b in 0..a-1, kept when len>=50,
     orientations fwd+rev (surviving widths {2,3,4,5}; >=6 length-vacuous).
  W  cyclic decimation pads [S[(a*j+c) mod L] for j in range(L)], a in 2..28,
     gcd(a,L)=1, cut c in C(a) = {(a*floor(i*L/k)) mod L : i<k},
     k = ceil(L/(L-49)), orientations fwd+rev. Cut placement spread in the
     step-a coordinate => COMPLETE alignment coverage (PREREG guarantee 1);
     verified exhaustively at startup (coverage_check) before any scan.

Statistic: (A - B) mod 29, chi2 vs uniform over 29 bins (no k-scaling, no
mirrors this campaign — PREREG collapses 5-6). core/kernel.py UNCHANGED.

Memory policy: full CSVs stream to work/index-consumption/ (unsorted, sha256
recorded); results/ ships top 100k rows (repo size policy).

Run from repo root:  python3 sweeps/2026-11-index-consumption/run.py
                     [--mask tgt|both] [--floor 40] [--skip P,W]
"""
import argparse, hashlib, heapq, json, math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, ROOT)
import numpy as np
from core import DATA, kernel

Q = 29
TRACK_TOP = 100_000
WORK = f"{ROOT}/work/index-consumption"
HDR = "target,pad,orient,offset,n_valid,chi2,ioc,top_rune,top_frac"
CHI2_COL = 4                     # index in the row tuple (== HDR order)

def load_sources():
    pages = kernel.load_pages()
    targets = [n for n in pages if n <= 54]
    pt = {}
    sp = f"{DATA}/solved_plaintexts.json"
    if os.path.exists(sp):
        pt = {k: np.array(v, dtype=np.int8) for k, v in json.load(open(sp)).items()}
    return pages, targets, {**pages, **pt}

# ---- pad stream generators (PREREG geometry) --------------------------------
def drop_pads(sources):
    """Family P: S[b::a], all phases, fwd+rev. 1,210 pads."""
    for N, S in sources.items():
        for a in range(2, 29):
            for b in range(a):
                p = S[b::a]
                if len(p) < kernel.MIN_LEN: continue
                yield N, f"d{a}.{b}", p
                yield N, f"d{a}.{b}r", p[::-1]

def cyc_cuts(L):
    """Registered cut set C(a) = {(a*floor(i*L/k)) mod L : i=0..k-1}, k=ceil(L/(L-49)).
    Returns k; cuts computed per step in cyc_pads."""
    return math.ceil(L / (L - 49))

def cyc_pads(sources):
    """Family W: full-length cyclic reads, cuts spread in the step-a coordinate
    (PREREG guarantee 1), fwd+rev. 4,128 pads."""
    for N, S in sources.items():
        L = len(S); k = cyc_cuts(L)
        for a in range(2, 29):
            if math.gcd(a, L) != 1: continue
            j = np.arange(L)
            for i in range(k):
                c = (a * ((i * L) // k)) % L
                pad = S[(a * j + c) % L]
                yield N, f"c{a}.{i}", pad
                yield N, f"c{a}.{i}r", pad[::-1]

# ---- PREREG guarantee 1: exhaustive alignment-coverage verification ---------
def coverage_check(pages, targets, sources, verbose=True):
    """For every (source L, step a, alignment v, target m) verify some cut
    yields a window with >=50 valid (tgt-mask) positions. Direct steps 2..28
    use C(a); steps L-28..L-2 are covered by rev pads of step a'=L-a, whose
    induced cuts are {a(L-1)+c}. Vectorized over alignments: for usable offsets
    o (full list precomputed per (m, L)), the alignment covered by cut c is
    v = (c - a*o) mod L. Returns violation count (must be 0)."""
    bad = 0
    for N, S in sources.items():
        L = len(S); k = cyc_cuts(L)
        for M in targets:
            A = pages[M]; m = len(A)
            nz = np.concatenate([[False], (A != 0)])          # prefix helper
            pre = np.concatenate([[0], np.cumsum(A != 0)])
            # usable offsets: window [max(0,o), min(m,o+L)) with >=50 valid,
            # o in [50-L, m-50] (both representatives o0, o0-L fold into this)
            us = [o for o in range(50 - L, m - 49)
                  if pre[min(m, o + L)] - pre[max(0, o)] >= 50]
            if not us: return _fail(N, M)
            us = np.array(us)
            for a in range(2, 29):
                if math.gcd(a, L) != 1: continue
                cuts = [(a * ((i * L) // k)) % L for i in range(k)]
                sides = [(a, cuts), (L - a, [(a * (L - 1) + c) % L for c in cuts])]
                for ap, cs in sides:
                    if ap < 2 or ap > L - 2: continue
                    cov = np.zeros(L, bool)
                    for c in cs:
                        cov[(c - ap * us) % L] = True
                    nv = int((~cov).sum())
                    if nv:
                        bad += nv
                        print(f"  coverage gap: source {N} L={L} step {ap} "
                              f"target {M}: {nv} alignments", flush=True)
    if verbose:
        print(f"coverage check (PREREG guarantee 1): {bad} violations "
              f"{'— COMPLETE' if bad == 0 else '— ABORT'}", flush=True)
    assert bad == 0, f"alignment coverage violated {bad}x"
    return bad

def _fail(N, M):
    raise AssertionError(f"no usable offset for source {N} target {M}")

def window_stats(A, B, off, mask="both"):
    """Recompute one window (mask sensitivity for leaders)."""
    m, n = len(A), len(B)
    i = np.arange(max(0, off), min(m, off + n))
    j = i - off
    a, b = A[i], B[j]
    keep = (a != 0) & (b != 0) if mask == "both" else (a != 0)
    a, b = a[keep], b[keep]
    nn = len(a)
    if nn < kernel.MIN_LEN: return None
    vals = (a.astype(np.int32) - b.astype(np.int32)) % Q
    h = np.bincount(vals, minlength=Q)
    return nn, (Q / nn) * float((h * h).sum()) - nn

class Sink:
    """Streams full CSV to work/, keeps a bounded top-K heap for results/."""
    def __init__(self, fam, floor):
        os.makedirs(WORK, exist_ok=True)
        os.makedirs(f"{HERE}/results", exist_ok=True)
        self.fam, self.floor = fam, floor
        self.nwin, self.nrow, self.mx, self.seq = 0, 0, -1.0, 0
        self.heap = []                                   # (chi2, seq, row)
        self.f = open(f"{WORK}/sweep_{fam}.csv", "w")
        self.f.write(HDR + "\n")
    def add(self, chi2, row):
        self.nwin += 1
        if chi2 > self.mx: self.mx = chi2
        if chi2 < self.floor: return
        self.nrow += 1
        self.f.write(",".join(str(x) for x in row) + "\n")
        item = (chi2, self.seq, row); self.seq += 1
        if len(self.heap) < TRACK_TOP: heapq.heappush(self.heap, item)
        elif chi2 > self.heap[0][0]: heapq.heapreplace(self.heap, item)
    def finish(self):
        self.f.close()
        rows = sorted((r for _, _, r in self.heap), key=lambda r: -r[CHI2_COL])
        with open(f"{HERE}/results/sweep_{self.fam}.csv", "w") as f:
            f.write(HDR + "\n")
            for r in rows: f.write(",".join(str(x) for x in r) + "\n")
        sha = hashlib.sha256(open(f"{WORK}/sweep_{self.fam}.csv", "rb").read()).hexdigest()
        return dict(family=self.fam, windows=self.nwin, rows_ge_floor=self.nrow,
                    obs_max=round(self.mx, 2), tracked_rows=len(rows),
                    full_csv=f"work/index-consumption/sweep_{self.fam}.csv",
                    full_sha256=sha)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mask", default="tgt", choices=["tgt", "both"])
    ap.add_argument("--floor", type=float, default=40.0)
    ap.add_argument("--skip", default="", help="comma list of families to skip")
    a = ap.parse_args()
    skip = set(x for x in a.skip.split(",") if x)

    pages, targets, sources = load_sources()
    coverage_check(pages, targets, sources)

    sinks, leaders = {}, {}

    def record(fam, chi2, row, tgt, padname, orient, off, B):
        sk = sinks.get(fam) or sinks.setdefault(fam, Sink(fam, a.floor))
        sk.add(chi2, row)
        lb = leaders.setdefault(fam, [])
        lb.append((chi2, tgt, padname, orient, off, B))
        if len(lb) > 400:
            lb.sort(key=lambda t: -t[0]); del lb[400:]

    for M in targets:
        A = pages[M]
        if "P" not in skip:
            for N, w, W in drop_pads(sources):
                for off, nn, chi2, ioc, h in kernel.pair_scan(A, W, mask=a.mask):
                    top = int(np.argmax(h))
                    record("P", chi2, (M, f"{N}:{w}", "drop", off, nn,
                            round(chi2, 2), round(ioc, 5), top,
                            round(float(h[top]) / nn, 4)), M, f"{N}:{w}", "drop", off, W)
        if "W" not in skip:
            for N, w, W in cyc_pads(sources):
                for off, nn, chi2, ioc, h in kernel.pair_scan(A, W, mask=a.mask):
                    top = int(np.argmax(h))
                    record("W", chi2, (M, f"{N}:{w}", "cyc", off, nn,
                            round(chi2, 2), round(ioc, 5), top,
                            round(float(h[top]) / nn, 4)), M, f"{N}:{w}", "cyc", off, W)
        print(f"target {M} done: " + ", ".join(f"{f}={s.nwin}" for f, s in sinks.items()),
              flush=True)

    summary = [sinks[f].finish() for f in sorted(sinks)]
    with open(f"{HERE}/results/obs_maxima.csv", "w") as f:
        f.write("family,windows,rows_ge_floor,obs_max,tracked_rows,full_sha256\n")
        for s in summary:
            f.write(f"{s['family']},{s['windows']},{s['rows_ge_floor']},"
                    f"{s['obs_max']},{s['tracked_rows']},{s['full_sha256']}\n")
    # mask=both sensitivity for the 20 leaders of each family (decision prong)
    with open(f"{HERE}/results/leaders_both.csv", "w") as f:
        f.write("family,target,pad,orient,offset,chi2_tgt,n_both,chi2_both\n")
        for fam in sorted(leaders):
            lb = sorted(leaders[fam], key=lambda t: -t[0])
            seen, out = set(), 0
            for chi2, tgt, padname, orient, off, B in lb:
                key = (tgt, padname, off)
                if key in seen: continue
                seen.add(key)
                r = window_stats(pages[tgt], B, off, mask="both")
                nb, cb = (r if r else ("", ""))
                f.write(f"{fam},{tgt},{padname},{orient},{off},{round(chi2, 2)},"
                        f"{nb},{round(cb, 2) if cb != '' else ''}\n")
                out += 1
                if out >= 20: break
    wc = f"{HERE}/results/window_counts.json"
    all_counts = json.load(open(wc)) if os.path.exists(wc) else {}
    for s in summary:
        all_counts[f"{s['family']}_windows"] = s["windows"]
        all_counts[f"{s['family']}_rows_ge_floor"] = s["rows_ge_floor"]
    with open(wc, "w") as f: json.dump(all_counts, f, indent=1)
    for s in summary:
        print(f"{s['family']}: {s['windows']} windows, {s['rows_ge_floor']} rows "
              f">= {a.floor}, max={s['obs_max']} (full: {s['full_csv']}, "
              f"sha256 {s['full_sha256'][:16]}…)")

if __name__ == "__main__":
    main()
