#!/usr/bin/env python3
"""Campaign 2026-11-pad-algebra — Phase 3 sweep CLI (implements PREREG.md exactly).

Families (registered 2026-11-14 before any output):
  D_mult    D = (C_M - k*C_N) mod 29, k in 2..27, all pairs, fwd+rev
  E_stride  difference stat vs strided pads C_N[g*t], C_N[n-1-g*t], g in {2,3}
  F_outlier per-page mirror-max / own-diff-p99 ratio (null: max-ratio across
            shuffled replicates — computed by calibrate.py)

core/kernel.py is deliberately UNCHANGED (PREREG): scaled/strided pads are
constructed here. mult_scan is a campaign-local helper that exploits the
k-invariance of the valid-position mask (k*0 = 0 keeps F positions fixed).

Run from repo root:  python3 sweeps/2026-11-pad-algebra/run.py [--mask tgt|both]
Outputs: results/sweep_D_mult.csv, sweep_E_stride.csv, audit_F_outlier.csv
"""
import argparse, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, ROOT)
import numpy as np
from core import DATA, kernel

KS = list(range(2, 28))          # k=0 trivial, k=1 campaign#1, k=28=campaign#2-A (PREREG collapses)
Q = 29

def mult_scan(A, B, mask="tgt", min_len=kernel.MIN_LEN, ks=KS, skip_off0=False):
    """k-scaled pad scan. Valid geometry computed once (k-invariant), then one
    bincount per k. skip_off0: exclude self-pair fwd o=0 — D=(1-k)*C_M is a symbol
    permutation of the page's own histogram, not a pad signal (trivial, disclosed)."""
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
            off = int(oi - (n - 1))
            if skip_off0 and off == 0: continue
            h = H[oi]; nn = int(cnt[oi])
            chi2 = (Q / nn) * float((h * h).sum()) - nn
            ioc = float((h * (h - 1)).sum()) / (nn * (nn - 1))
            yield k, off, nn, chi2, ioc, h

def stride_pads(pages):
    for N, p in pages.items():
        for g in (2, 3):
            yield N, f"s{g}",  p[::g]          # pad[t] = C_N[g*t]
            yield N, f"sr{g}", p[::-1][::g]    # pad[t] = C_N[n-1-g*t]

def page_mirror_stats(A):
    """Exact quantities of campaign #2 family C (registered definition of F)."""
    rev = A[::-1]
    diff = [c for off, _, c, _, _ in kernel.pair_scan(A, A) if off != 0]
    mir = [c for _, _, c, _, _ in kernel.pair_scan(A, rev)]
    n = len(A)
    for pad in (np.concatenate([A, rev]), np.concatenate([rev, A])):
        mir += [c for _, _, c, _, _ in kernel.pair_scan(A, pad, straddle=n)]
    if not diff or not mir: return None
    return max(mir), float(np.percentile(diff, 99))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mask", default="tgt", choices=["tgt", "both"])
    ap.add_argument("--floor", type=float, default=40.0)
    ap.add_argument("--skip", default="", help="comma list of families to skip, e.g. D,E")
    a = ap.parse_args()
    skip = set(x for x in a.skip.split(",") if x)

    pages = kernel.load_pages()
    targets = [n for n in pages if n <= 54]
    pt = {}
    sp = f"{DATA}/solved_plaintexts.json"
    if os.path.exists(sp):
        pt = {k: np.array(v, dtype=np.int8) for k, v in json.load(open(sp)).items()}
    os.makedirs(f"{HERE}/results", exist_ok=True)
    counts = {}

    # ---------- D: multiplicative pad scaling ----------
    if "D" not in skip:
        rows, nwin = [], 0
        for M in targets:
            A = pages[M]
            streams = [(N, "fwd", p) for N, p in pages.items()] + \
                      [(N, "rev", p[::-1]) for N, p in pages.items()] + \
                      [(k, "fwd", s) for k, s in pt.items()] + \
                      [(k, "rev", s[::-1]) for k, s in pt.items()]
            for N, orient, B in streams:
                trivial = (M == N and orient == "fwd")     # own-histogram window, see mult_scan
                for k, off, nn, chi2, ioc, h in mult_scan(A, B, mask=a.mask, skip_off0=trivial):
                    nwin += 1
                    if chi2 >= a.floor:
                        top = int(np.argmax(h))
                        rows.append(dict(target=M, pad=N, orient=orient, k=k, offset=off,
                                         n_valid=nn, chi2=round(chi2, 2), ioc=round(ioc, 5),
                                         top_rune=top, top_frac=round(float(h[top]) / nn, 4)))
            print(f"D: target {M} done ({nwin} windows)", flush=True)
        rows.sort(key=lambda r: -r["chi2"])
        with open(f"{HERE}/results/sweep_D_mult.csv", "w") as f:
            f.write("target,pad,orient,k,offset,n_valid,chi2,ioc,top_rune,top_frac\n")
            for r in rows:
                f.write(f"{r['target']},{r['pad']},{r['orient']},{r['k']},{r['offset']},"
                        f"{r['n_valid']},{r['chi2']},{r['ioc']},{r['top_rune']},{r['top_frac']}\n")
        counts["D_mult_windows"] = nwin
        print(f"D_mult: {nwin} windows, {len(rows)} rows >= {a.floor}, max={rows[0]['chi2'] if rows else None}")

    # ---------- E: stride/skip pads ----------
    if "E" not in skip:
        rows, nwin, npair = [], 0, 0
        for M in targets:
            A = pages[M]
            for N, wname, W in stride_pads(pages):
                if len(W) < kernel.MIN_LEN: continue
                npair += 1
                for off, nn, chi2, ioc, h in kernel.pair_scan(A, W, mask=a.mask):
                    nwin += 1
                    if chi2 >= a.floor:
                        top = int(np.argmax(h))
                        rows.append(dict(target=M, pad=f"{N}:{wname}", orient="stride",
                                         offset=off, n_valid=nn, chi2=round(chi2, 2),
                                         ioc=round(ioc, 5), top_rune=top,
                                         top_frac=round(float(h[top]) / nn, 4)))
        rows.sort(key=lambda r: -r["chi2"])
        with open(f"{HERE}/results/sweep_E_stride.csv", "w") as f:
            f.write("target,pad,orient,offset,n_valid,chi2,ioc,top_rune,top_frac\n")
            for r in rows:
                f.write(f"{r['target']},{r['pad']},{r['orient']},{r['offset']},{r['n_valid']},"
                        f"{r['chi2']},{r['ioc']},{r['top_rune']},{r['top_frac']}\n")
        counts["E_stride_windows"] = nwin; counts["E_pairs_participating"] = npair
        print(f"E_stride: {npair} pad-target pairs, {nwin} windows, {len(rows)} rows, "
              f"max={rows[0]['chi2'] if rows else None}")

    # ---------- F: page-level mirror-outlier ratios (observed side) ----------
    if "F" not in skip:
        out = []
        for M in targets:
            st = page_mirror_stats(pages[M])
            if st is None: continue
            mm, p99 = st
            out.append(dict(page=M, mirror_max=round(mm, 2), own_diff_p99=round(p99, 2),
                            ratio=round(mm / p99, 3)))
        out.sort(key=lambda r: -r["ratio"])
        with open(f"{HERE}/results/audit_F_outlier.csv", "w") as f:
            f.write("page,mirror_max,own_diff_p99,ratio\n")
            for r in out:
                f.write(f"{r['page']},{r['mirror_max']},{r['own_diff_p99']},{r['ratio']}\n")
        med = float(np.median([r["ratio"] for r in out]))
        print(f"F_outlier: {len(out)} pages, median ratio {med:.2f}, top: " +
              ", ".join(f"p{r['page']}={r['ratio']}" for r in out[:5]))

    with open(f"{HERE}/results/window_counts.json", "w") as f:
        json.dump(counts, f, indent=1)

if __name__ == "__main__":
    main()
