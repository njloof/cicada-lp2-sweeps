#!/usr/bin/env python3
"""Campaign 2026-11-pad-transform — Phase 2 sweep CLI (implements PREREG.md exactly).

Families (see PREREG.md — registered 2026-11-14 before any output):
  A_sum    stat S = (C_M + C_N) mod 29, all pairs/offsets, fwd/rev + mirror straddling
  B_weave  difference stat vs alternating-weave pads interleave(C_N,rev), interleave(rev,C_N)
  C_audit  self-matched per-page audit: mirror-family max vs own difference-family p99

Run from repo root:  python3 sweeps/2026-11-pad-transform/run.py [--mask tgt|both]
Outputs: results/sweep_A_sum.csv, sweep_B_weave.csv, audit_C_selfmirror.csv
"""
import argparse, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, ROOT)
import numpy as np
from core import DATA
from core import kernel

TRIVIAL = {"fwd": {0}, "fwdrev": {0}, "revfwd": None, "rev": set()}  # filled per pad len

def page_pads(pages):
    for N, p in pages.items():
        rev = p[::-1]
        yield N, "fwd", p, None
        yield N, "rev", rev, None
        yield N, "fwdrev", np.concatenate([p, rev]), len(p)
        yield N, "revfwd", np.concatenate([rev, p]), len(p)

def _weave(x, y):
    w = np.empty(len(x) + len(y), dtype=np.int8)
    w[0::2], w[1::2] = x, y
    return w

def weave_pads(pages):
    for N, p in pages.items():
        rev = p[::-1]
        yield N, "w1", _weave(p, rev)          # alternate fwd, rev
        yield N, "w2", _weave(rev, p)          # alternate rev, fwd

def trivial_offsets(M, N, orient, nN):
    if M != N: return ()
    return {"fwd": (0,), "fwdrev": (0,), "revfwd": (-nN,), "rev": ()}[orient]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mask", default="tgt", choices=["tgt", "both"])
    ap.add_argument("--floor", type=float, default=40.0)
    a = ap.parse_args()

    pages = kernel.load_pages()
    targets = [n for n in pages if n <= 54]
    pt = {}
    sp = f"{DATA}/solved_plaintexts.json"
    if os.path.exists(sp):
        pt = {k: np.array(v, dtype=np.int8) for k, v in json.load(open(sp)).items()}

    os.makedirs(f"{HERE}/results", exist_ok=True)
    counts = {}

    # ---------- Family A: sum stream ----------
    rows, nwin = [], 0
    for M in targets:
        A = pages[M]
        padstreams = list(page_pads(pages)) + \
                     [(k, o, s if o == "fwd" else s[::-1], None)
                      for k, s in pt.items() for o in ("fwd", "rev")]
        for N, orient, B, straddle in padstreams:
            triv = trivial_offsets(M, N, orient, len(pages.get(N, B))) if orient in TRIVIAL else ()
            for off, nn, chi2, ioc, h in kernel.pair_scan(A, B, mask=a.mask,
                                                          straddle=straddle, stat="sum"):
                nwin += 1
                if off in triv: continue
                if chi2 >= a.floor:
                    top = int(np.argmax(h))
                    rows.append(dict(target=M, pad=N, orient=orient, offset=off, n_valid=nn,
                                     chi2=round(chi2, 2), ioc=round(ioc, 5), top_rune=top,
                                     top_frac=round(float(h[top]) / nn, 4)))
    rows.sort(key=lambda r: -r["chi2"])
    with open(f"{HERE}/results/sweep_A_sum.csv", "w") as f:
        f.write("target,pad,orient,offset,n_valid,chi2,ioc,top_rune,top_frac\n")
        for r in rows:
            f.write(f"{r['target']},{r['pad']},{r['orient']},{r['offset']},{r['n_valid']},"
                    f"{r['chi2']},{r['ioc']},{r['top_rune']},{r['top_frac']}\n")
    counts["A_sum_windows"] = nwin
    print(f"A_sum: {nwin} windows, {len(rows)} rows >= {a.floor}, max={rows[0]['chi2'] if rows else None}")

    # ---------- Family B: alternating-weave pads (difference stat) ----------
    rows, nwin = [], 0
    for M in targets:
        A = pages[M]
        for N, wname, W in weave_pads(pages):
            for off, nn, chi2, ioc, h in kernel.pair_scan(A, W, mask=a.mask):
                nwin += 1
                if chi2 >= a.floor:
                    top = int(np.argmax(h))
                    rows.append(dict(target=M, pad=f"{N}:{wname}", orient="weave", offset=off,
                                     n_valid=nn, chi2=round(chi2, 2), ioc=round(ioc, 5),
                                     top_rune=top, top_frac=round(float(h[top]) / nn, 4)))
    rows.sort(key=lambda r: -r["chi2"])
    with open(f"{HERE}/results/sweep_B_weave.csv", "w") as f:
        f.write("target,pad,orient,offset,n_valid,chi2,ioc,top_rune,top_frac\n")
        for r in rows:
            f.write(f"{r['target']},{r['pad']},{r['orient']},{r['offset']},{r['n_valid']},"
                    f"{r['chi2']},{r['ioc']},{r['top_rune']},{r['top_frac']}\n")
    counts["B_weave_windows"] = nwin
    print(f"B_weave: {nwin} windows, {len(rows)} rows >= {a.floor}, max={rows[0]['chi2'] if rows else None}")

    # ---------- Family C: self-matched per-page mirror audit (all 55 pages) ----------
    out = []
    for M in targets:
        A = pages[M]; rev = A[::-1]
        diff = [c for off, _, c, _, _ in kernel.pair_scan(A, A) if off != 0]  # trivial o=0 excluded
        mir = [c for _, _, c, _, _ in kernel.pair_scan(A, rev)]
        n = len(A)
        for pad, st in ((np.concatenate([A, rev]), n), (np.concatenate([rev, A]), n)):
            mir += [c for _, _, c, _, _ in kernel.pair_scan(A, pad, straddle=st)]
        if not diff or not mir: continue
        p99 = float(np.percentile(diff, 99))
        mm = max(mir)
        out.append(dict(page=M, n_mirror=len(mir), n_diff=len(diff),
                        mirror_max=round(mm, 2), own_diff_p99=round(p99, 2),
                        ratio=round(mm / p99, 3) if p99 > 0 else None,
                        flag_gt_p99=bool(mm > p99), flag_gt_globalnull=bool(mm > 118.8)))
    out.sort(key=lambda r: -r["ratio"])
    with open(f"{HERE}/results/audit_C_selfmirror.csv", "w") as f:
        f.write("page,n_mirror,n_diff,mirror_max,own_diff_p99,ratio,flag_gt_p99,flag_gt_globalnull\n")
        for r in out:
            f.write(f"{r['page']},{r['n_mirror']},{r['n_diff']},{r['mirror_max']},{r['own_diff_p99']},"
                    f"{r['ratio']},{r['flag_gt_p99']},{r['flag_gt_globalnull']}\n")
    nflag = sum(r["flag_gt_p99"] and r["flag_gt_globalnull"] for r in out)
    n99 = sum(r["flag_gt_p99"] for r in out)
    print(f"C_audit: 55 pages, {n99} exceed own-diff p99, {nflag} also exceed global MC max 118.8")
    for r in out[:5]:
        print(f"   page {r['page']:2d}: mirror_max={r['mirror_max']:6.1f} own p99={r['own_diff_p99']:6.1f} "
              f"ratio={r['ratio']}")

    with open(f"{HERE}/results/window_counts.json", "w") as f:
        json.dump(counts, f, indent=1)

if __name__ == "__main__":
    main()
