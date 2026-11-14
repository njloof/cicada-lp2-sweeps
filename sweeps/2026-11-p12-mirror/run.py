#!/usr/bin/env python3
"""Campaign 2026-11-p12-mirror — Phase 4 confirmation CLI (implements PREREG.md).

Observed side + descriptives; the 1000-shuffle nulls live in calibrate.py.
  obs_G_ratios.csv   campaign #3 F statistic per page (ratio = mirror_max/own-diff p99)
  obs_H_shift.csv    S = max over rev alignments of (h[1]+h[28])/n per page
  I_noise.csv        survival curve: chi2max / |d|=1 fraction vs corruption f
  J_pivot.txt        raw-transcription context at the anti-diagonal pivot
  J_runs.csv         run-length profile of the |d|=1 indicator vs its null
  J_controls.csv     G/H statistics on solved plaintexts (instrument control)

Run from repo root:  python3 sweeps/2026-11-p12-mirror/run.py
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, ROOT)
import numpy as np
from core import DATA, kernel
from core.validate import R2I

P12_OFF, P12_N = -83, 261          # campaign #3 flagged window (rev alignment)
Q = 29

def page_ratio_stats(A):
    """Exact campaign #2/#3 F quantities: (mirror_max, own_diff_p99)."""
    rev = A[::-1]; n = len(A)
    diff = [c for off, _, c, _, _ in kernel.pair_scan(A, A) if off != 0]
    mir = [c for _, _, c, _, _ in kernel.pair_scan(A, rev)]
    for pad in (np.concatenate([A, rev]), np.concatenate([rev, A])):
        mir += [c for _, _, c, _, _ in kernel.pair_scan(A, pad, straddle=n)]
    if not diff or not mir: return None
    return max(mir), float(np.percentile(diff, 99))

def shift_stat(A):
    """H statistic: max over rev alignments of |d|=1 share. -> (S, off, n)."""
    best = (-1.0, None, None)
    for off, nn, c, ioc, h in kernel.pair_scan(A, A[::-1]):
        s = (int(h[1]) + int(h[28])) / nn
        if s > best[0]: best = (s, int(off), int(nn))
    return best

def p12_window(A, off=P12_OFF):
    """Position list + delta stream of the flagged window (tgt mask, original coords).
    Alignment is against the REVERSED page: pad slot j=i-off holds A[n-1-j]."""
    n = len(A)
    idxs = [i for i in range(n) if A[i] != 0 and 0 <= i - off < n]   # pad slot j = i - off
    d = np.array([(int(A[i]) - int(A[n - 1 - (i - off)])) % Q for i in idxs])
    return np.array(idxs), d

def main():
    pages = kernel.load_pages()
    targets = [n for n in pages if n <= 54]
    os.makedirs(f"{HERE}/results", exist_ok=True)
    A12 = pages[12]

    # ---- observed G and H tables ----
    g_rows = []
    for M in targets:
        st = page_ratio_stats(pages[M])
        if st: g_rows.append(dict(page=M, mirror_max=round(st[0], 2), p99=round(st[1], 2),
                                  ratio=round(st[0] / st[1], 3)))
    g_rows.sort(key=lambda r: -r["ratio"])
    with open(f"{HERE}/results/obs_G_ratios.csv", "w") as f:
        f.write("page,mirror_max,p99,ratio\n")
        for r in g_rows: f.write(f"{r['page']},{r['mirror_max']},{r['p99']},{r['ratio']}\n")
    print("obs G top5:", [(r["page"], r["ratio"]) for r in g_rows[:5]], flush=True)

    h_rows = []
    for M in targets:
        s, off, nn = shift_stat(pages[M])
        h_rows.append(dict(page=M, S=round(s, 4), off=off, n=nn))
    h_rows.sort(key=lambda r: -r["S"])
    with open(f"{HERE}/results/obs_H_shift.csv", "w") as f:
        f.write("page,S,off,n\n")
        for r in h_rows: f.write(f"{r['page']},{r['S']},{r['off']},{r['n']}\n")
    print("obs H top5:", [(r["page"], r["S"]) for r in h_rows[:5]], flush=True)

    # ---- I_noise: survival curve (seed 20261117) ----
    rng = np.random.default_rng(20261117)
    idxs, d0 = p12_window(A12)
    obs_frac = float(np.mean((d0 == 1) | (d0 == 28)))
    obs_chi2 = max(c for _, _, c, _, _ in kernel.pair_scan(A12, A12[::-1]))
    nonf = np.nonzero(A12 != 0)[0]
    with open(f"{HERE}/results/I_noise.csv", "w") as f:
        f.write("f,reps,chi2_med,chi2_p10,frac_med,frac_p10,frac_ge_obs\n")
        for fr in (0.02, 0.05, 0.10):
            k = int(round(fr * len(nonf)))
            chis, fracs = [], []
            for _ in range(200):
                An = A12.copy()
                pos = rng.choice(nonf, size=k, replace=False)
                An[pos] = rng.integers(1, Q, size=k)
                chis.append(max(c for _, _, c, _, _ in kernel.pair_scan(An, An[::-1])))
                _, dn = p12_window(An)                       # geometry follows mask; disclose
                fracs.append(float(np.mean((dn == 1) | (dn == 28))))
            chis, fracs = np.array(chis), np.array(fracs)
            f.write(f"{fr},200,{np.median(chis):.1f},{np.percentile(chis,10):.1f},"
                    f"{np.median(fracs):.4f},{np.percentile(fracs,10):.4f},"
                    f"{float(np.mean(fracs >= obs_frac)):.3f}\n")
            print(f"I f={fr}: chi2 med {np.median(chis):.1f} (obs {obs_chi2:.1f}), "
                  f"frac med {np.median(fracs):.3f} (obs {obs_frac:.3f})", flush=True)

    # ---- J(a): pivot mapping into raw transcription ----
    raw = open(f"{DATA}/pages/lp2_12.txt").read()
    rune_pos = [k for k, ch in enumerate(raw) if ch in R2I]
    pivot = 177 / 2                                        # i + j' = 177 -> pivot 88.5
    lo, hi = int(np.floor(pivot)), int(np.ceil(pivot))
    k_lo, k_hi = rune_pos[lo], rune_pos[hi]
    ctx = raw[max(0, k_lo - 25):k_hi + 25].replace("\n", "\\n")
    with open(f"{HERE}/results/J_pivot.txt", "w") as f:
        f.write(f"anti-diagonal const 177 -> pivot rune {pivot} of {len(rune_pos)}\n"
                f"raw offsets: rune#{lo}@{k_lo}, rune#{hi}@{k_hi}\ncontext: ...{ctx}...\n")
    print(open(f"{HERE}/results/J_pivot.txt").read().strip())

    # ---- J(b): |d|=1 run structure vs null (seed 20261118) ----
    b = ((d0 == 1) | (d0 == 28)).astype(np.int8)
    def runs(x):
        e = np.diff(np.concatenate([[0], x.astype(int), [0]]))
        starts, ends = np.flatnonzero(e == 1), np.flatnonzero(e == -1)  # alternate by construction
        if len(starts) == 0: return 0, 0
        L = ends - starts
        return int(L.max()), int((L >= 3).sum())
    obs_maxrun, obs_r3 = runs(b)
    rng2 = np.random.default_rng(20261118)
    nmax, nr3 = [], []
    for _ in range(2000):
        p = A12.copy(); rng2.shuffle(p)
        _, dd = p12_window(p)
        bb = ((dd == 1) | (dd == 28)).astype(np.int8)
        m, r3 = runs(bb); nmax.append(m); nr3.append(r3)
    nmax, nr3 = np.array(nmax), np.array(nr3)
    with open(f"{HERE}/results/J_runs.csv", "w") as f:
        f.write("stat,observed,null_median,null_p95,null_max,p_exceed\n")
        f.write(f"max_run,{obs_maxrun},{np.median(nmax)},{np.percentile(nmax,95)},"
                f"{nmax.max()},{(1+(nmax>=obs_maxrun).sum())/2001:.4f}\n")
        f.write(f"runs_ge3,{obs_r3},{np.median(nr3)},{np.percentile(nr3,95)},"
                f"{nr3.max()},{(1+(nr3>=obs_r3).sum())/2001:.4f}\n")
    print(f"J runs: max_run obs={obs_maxrun} (null med {np.median(nmax)}), "
          f"runs>=3 obs={obs_r3} (null med {np.median(nr3)})", flush=True)

    # ---- J(c): solved-plaintext controls ----
    pt = {k: np.array(v, dtype=np.int8) for k, v in json.load(open(f"{DATA}/solved_plaintexts.json")).items()}
    with open(f"{HERE}/results/J_controls.csv", "w") as f:
        f.write("name,len,ratio,S,rev_chi2max\n")
        for name, P in pt.items():
            st = page_ratio_stats(P)
            s, off, nn = shift_stat(P)
            rc = max(c for _, _, c, _, _ in kernel.pair_scan(P, P[::-1]))
            f.write(f"{name},{len(P)},{st[0]/st[1]:.3f},{s:.4f},{rc:.1f}\n")
            print(f"control {name}: ratio={st[0]/st[1]:.3f} S={s:.4f} revmax={rc:.1f}")

if __name__ == "__main__":
    main()
