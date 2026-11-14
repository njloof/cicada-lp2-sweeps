#!/usr/bin/env python3
"""Campaign 2026-11-product-spaces — Phase 5 sweep CLI (implements PREREG.md exactly).

Families (registered 2026-11-14 before any output):
  K  stride extension g in 4..8 fwd/rev (g>=6 vacuous by length — disclosed)
     + strided mirror pads g in 2..5 (both strided streams, both orderings,
       straddle-only)
  L  D = (C_M - k*W) mod 29, k in 2..27, W = strided pads C_N[::g], C_N[n-1-g*t],
     g in 2..5 (plaintext pads contribute no strided pads >= 50 — disclosed)
  M  D = (C_M - k*B) mod 29, k in 2..27, B = plain mirror pads (57 cipher + 2
     plaintext), straddle-only, trivial self-pair mirror identities excluded

core/kernel.py UNCHANGED (PREREG). mult_scan is a campaign-local copy of #3's
helper (k-invariant valid-mask geometry). Straddle as post-hoc offset test:
window crosses junction s  <=>  -s < off <= m-1-s  (identical to kernel.pair_scan's).

Memory policy: full CSVs stream to work/product-spaces/ (unsorted, sha256
recorded); results/ ships top 100k rows (repo size policy).

Run from repo root:  python3 sweeps/2026-11-product-spaces/run.py [--mask tgt|both]
                     [--skip K,L,M] [--floor 40]
"""
import argparse, hashlib, heapq, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, ROOT)
import numpy as np
from core import DATA, kernel

Q = 29
KS = list(range(2, 28))          # collapses exactly as campaign #3's PREREG
TRACK_TOP = 100_000
WORK = f"{ROOT}/work/product-spaces"
HDR = "target,pad,orient,k,offset,n_valid,chi2,ioc,top_rune,top_frac"
CHI2_COL = 6                     # index in the row tuple (== HDR order)

def mult_scan(A, B, mask="tgt", min_len=kernel.MIN_LEN, ks=KS):
    """k-scaled pad scan (campaign #3 helper, copied per campaign-local
    convention). Yields (k, off, n, chi2, ioc, hist)."""
    m, n = len(A), len(B)
    if mask == "both":
        Valid = (A[:, None] != 0) & (B[None, :] != 0)
    else:
        Valid = np.repeat((A != 0)[:, None], n, axis=1)
    ii, jj = np.nonzero(Valid)
    d = (ii - jj) + (n - 1)
    n_off = m + n - 1
    Ai = A[ii].astype(np.int32); Bj = B[jj].astype(np.int32)
    for k in ks:
        vals = (Ai - k * Bj) % Q
        H = np.bincount(d * Q + vals, minlength=n_off * Q).reshape(n_off, Q)
        cnt = H.sum(1)
        for oi in np.nonzero(cnt >= min_len)[0]:
            h = H[oi]; nn = int(cnt[oi])
            chi2 = (Q / nn) * float((h * h).sum()) - nn
            ioc = float((h * (h - 1)).sum()) / (nn * (nn - 1))
            yield k, int(oi - (n - 1)), nn, chi2, ioc, h

# ---- pad stream generators (PREREG geometry) --------------------------------
def strided_ext(pages, gs=(4, 5, 6, 7, 8)):
    for N, p in pages.items():
        for g in gs:
            yield N, f"s{g}",  p[::g]
            yield N, f"sr{g}", p[::-1][::g]

def strided_all(pages, gs=(2, 3, 4, 5)):
    for N, p in pages.items():
        for g in gs:
            yield N, f"s{g}",  p[::g]
            yield N, f"sr{g}", p[::-1][::g]

def strided_mirrors(pages, gs=(2, 3, 4, 5)):
    """Strided mirror pads: both strided streams, both orderings, junction=len(x)."""
    for N, p in pages.items():
        for g in gs:
            for tag, x in ((f"s{g}", p[::g]), (f"sr{g}", p[::-1][::g])):
                if len(x) < kernel.MIN_LEN: continue
                L = len(x)
                yield N, f"{tag}m",  np.concatenate([x, x[::-1]]), L
                yield N, f"{tag}rm", np.concatenate([x[::-1], x]), L

def plain_mirrors(pages, pt):
    for N, p in pages.items():
        rev = p[::-1]; n = len(p)
        yield N, "fwdrev", np.concatenate([p, rev]), n
        yield N, "revfwd", np.concatenate([rev, p]), n
    for name, s in pt.items():
        rev = s[::-1]; n = len(s)
        yield name, "fwdrev", np.concatenate([s, rev]), n
        yield name, "revfwd", np.concatenate([rev, s]), n

def window_stats(A, B, k, off, mask="both"):
    """Recompute one window (mask sensitivity for leaders)."""
    m, n = len(A), len(B)
    i = np.arange(max(0, off), min(m, off + n))
    j = i - off
    a, b = A[i], B[j]
    keep = (a != 0) & (b != 0) if mask == "both" else (a != 0)
    a, b = a[keep], b[keep]
    nn = len(a)
    if nn < kernel.MIN_LEN: return None
    vals = (a.astype(np.int32) - k * b.astype(np.int32)) % Q
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
                    full_csv=f"work/product-spaces/sweep_{self.fam}.csv",
                    full_sha256=sha)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mask", default="tgt", choices=["tgt", "both"])
    ap.add_argument("--floor", type=float, default=40.0)
    ap.add_argument("--skip", default="", help="comma list of families to skip")
    a = ap.parse_args()
    skip = set(x for x in a.skip.split(",") if x)

    pages = kernel.load_pages()
    targets = [n for n in pages if n <= 54]
    pt = {}
    sp = f"{DATA}/solved_plaintexts.json"
    if os.path.exists(sp):
        pt = {k: np.array(v, dtype=np.int8) for k, v in json.load(open(sp)).items()}

    sinks, leaders = {}, {}

    def record(fam, chi2, row, tgt, padname, orient, k, off, B):
        sk = sinks.get(fam) or sinks.setdefault(fam, Sink(fam, a.floor))
        sk.add(chi2, row)
        lb = leaders.setdefault(fam, [])
        lb.append((chi2, tgt, padname, orient, k, off, B))
        if len(lb) > 400:
            lb.sort(key=lambda t: -t[0]); del lb[400:]

    for M in targets:
        A = pages[M]
        # ---------- K: stride extension + strided mirrors ----------
        if "K" not in skip:
            for N, w, W in strided_ext(pages):
                if len(W) < kernel.MIN_LEN: continue
                for off, nn, chi2, ioc, h in kernel.pair_scan(A, W, mask=a.mask):
                    top = int(np.argmax(h))
                    record("K", chi2, (M, f"{N}:{w}", "stride", 1, off, nn,
                            round(chi2, 2), round(ioc, 5), top,
                            round(float(h[top]) / nn, 4)), M, f"{N}:{w}", "stride", 1, off, W)
            for N, w, W, s in strided_mirrors(pages):
                for off, nn, chi2, ioc, h in kernel.pair_scan(A, W, mask=a.mask, straddle=s):
                    top = int(np.argmax(h))
                    record("K", chi2, (M, f"{N}:{w}", "smirror", 1, off, nn,
                            round(chi2, 2), round(ioc, 5), top,
                            round(float(h[top]) / nn, 4)), M, f"{N}:{w}", "smirror", 1, off, W)
        # ---------- L: scaling x stride ----------
        if "L" not in skip:
            for N, w, W in strided_all(pages):
                if len(W) < kernel.MIN_LEN: continue
                for k, off, nn, chi2, ioc, h in mult_scan(A, W, mask=a.mask):
                    top = int(np.argmax(h))
                    record("L", chi2, (M, f"{N}:{w}", "stride", k, off, nn,
                            round(chi2, 2), round(ioc, 5), top,
                            round(float(h[top]) / nn, 4)), M, f"{N}:{w}", "stride", k, off, W)
        # ---------- M: scaling x plain mirror junction ----------
        if "M" not in skip:
            m = len(A)
            for N, orient, B, s in plain_mirrors(pages, pt):
                triv = set()
                if N == M:                       # pad window == target (all-zero D)
                    triv = {0} if orient == "fwdrev" else {-s}
                for k, off, nn, chi2, ioc, h in mult_scan(A, B, mask=a.mask):
                    if off in triv: continue
                    if not (-s < off <= m - 1 - s): continue   # straddle (PREREG)
                    top = int(np.argmax(h))
                    record("M", chi2, (M, f"{N}:{orient}", "mirror", k, off, nn,
                            round(chi2, 2), round(ioc, 5), top,
                            round(float(h[top]) / nn, 4)), M, f"{N}:{orient}", "mirror", k, off, B)
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
        f.write("family,target,pad,orient,k,offset,chi2_tgt,n_both,chi2_both\n")
        for fam in sorted(leaders):
            lb = sorted(leaders[fam], key=lambda t: -t[0])
            seen, out = set(), 0
            for chi2, tgt, padname, orient, k, off, B in lb:
                key = (tgt, padname, k, off)
                if key in seen: continue
                seen.add(key)
                r = window_stats(pages[tgt], B, k, off, mask="both")
                nb, cb = (r if r else ("", ""))
                f.write(f"{fam},{tgt},{padname},{orient},{k},{off},{round(chi2, 2)},"
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
