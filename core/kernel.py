#!/usr/bin/env python3
"""Cross-page pad sweep kernel — the instrument every campaign shares.

Model:  C_M[t] = (P_M[t] + C_N[t - o]) mod 29   =>   D = (C_M - C_N) at true offset = P_M
Search: ordered pairs (M target, N pad), all offsets, pad orientations.

Orientations:
  fwd      pad = C_N                 (diagonal family  i - j = o)
  rev      pad = reverse(C_N)        (anti-diagonal     i + j = const)
  fwdrev   pad = C_N + rev(C_N)      (mirror set — junction-straddling windows only)
  revfwd   pad = rev(C_N) + C_N      (mirror set)
  (Target-reversed scanning is a no-op: chi2 is order-invariant and the pairing
   family is identical to pad-reversed, up to offset relabeling.)

Masking:
  primary ("tgt")  drop target-side F positions only — alignment-safe (null-F in the
                   target shifts pad alignment for everything downstream; dropping all
                   target Fs is correct whether each F was null or not) and keeps the
                   ~6.6% pad-F positions, which are unambiguously valid D = C_M = P_M.
  handoff ("both") drop positions where either stream has F (conservative superset).

chi2 = (29/n) * sum(c^2) - n   vs uniform over 29 bins;  ioc = sum(c(c-1))/(n(n-1)).

Trivial-window exclusions (self-pairs): the pad window equal to the target itself
gives all-zero D (chi2 = 29*n - n); mirror pads contain the plain pad as a
sub-window, so the identity reappears at other offsets — all excluded.
"""
import numpy as np, os, sys, time
from core import DATA, Q

MIN_LEN = 50

def load_pages():
    pages = {}
    for n in range(58):
        p = f"{DATA}/pages/lp2_{n:02d}.txt"
        if os.path.exists(p):
            pages[n] = np.array([int(x) for ln in open(p) for x in ln.split()], dtype=np.int8)
    return pages

def pair_scan(A, B, mask="tgt", min_len=MIN_LEN, straddle=None):
    """All-offset scan of target A (len m) vs pad B (len n).
    Yields (offset, n_valid, chi2, ioc, hist) for every window with >= min_len valid positions.
    Vectorized: full m x n difference matrix; offset = i - j diagonal.
    straddle: if given, keep only windows whose pad span [jmin, jmax] crosses the
    junction index (used for mirror pads so windows lying wholly in one half — which
    duplicate the plain fwd/rev scans — are not counted twice)."""
    m, n = len(A), len(B)
    Af, Bf = A.astype(np.int16), B.astype(np.int16)
    Diff = (Af[:, None] - Bf[None, :]) % Q                      # m x n
    if mask == "both":
        Valid = (A[:, None] != 0) & (Bf[None, :] != 0)
    else:  # "tgt"
        Valid = np.repeat((A != 0)[:, None], n, axis=1)
    ii, jj = np.nonzero(Valid)
    d = ii - jj                                                  # offset index in [-(n-1), m-1]
    vals = Diff[ii, jj]
    off = d + (n - 1)                                            # shift to >= 0
    n_off = m + n - 1
    # histogram per (offset, symbol) in one bincount
    H = np.bincount(off * Q + vals, minlength=n_off * Q).reshape(n_off, Q)
    cnt = H.sum(1)
    good = cnt >= min_len
    if straddle is not None:
        jmin = -(np.arange(n_off) - (n - 1))                     # pad index at i=0, per offset
        jmax = jmin + m - 1
        good &= (jmin < straddle) & (jmax >= straddle)           # window must cross the junction
    for oi in np.nonzero(good)[0]:
        h = H[oi]; nn = cnt[oi]
        chi2 = (Q / nn) * float((h * h).sum()) - nn
        ioc = float((h * (h - 1)).sum()) / (nn * (nn - 1))
        yield int(oi - (n - 1)), int(nn), chi2, ioc, h

def orientations(page, want_mirror=False):
    rev = page[::-1]
    yield "fwd", page
    yield "rev", rev
    if want_mirror:
        yield "fwdrev", np.concatenate([page, rev])
        yield "revfwd", np.concatenate([rev, page])

def run_sweep(pages, targets, pads, mask="tgt", mirror=False, floor=40.0):
    """Returns (rows, per_pair_max). rows = dicts for windows with chi2 >= floor."""
    rows, pairmax = [], {}
    t0 = time.time()
    for M in targets:
        A = pages[M]
        for N in pads:
            # trivial self-pair identities: mirror pads contain the plain pad as a
            # sub-window, so C_N - C_N reappears at other offsets (all-zero D)
            trivial = {}
            if M == N:
                nN = len(pages[N])
                trivial = {"fwd": {0}, "fwdrev": {0}, "revfwd": {-nN}, "rev": set()}
            for orient, B in orientations(pages[N], mirror):
                straddle = len(pages[N]) if orient in ("fwdrev", "revfwd") else None
                best = None
                for off, nn, chi2, ioc, h in pair_scan(A, B, mask=mask, straddle=straddle):
                    if M == N and off in trivial.get(orient, ()):
                        continue   # trivial identity: pad window == target itself
                    key = (M, N, orient)
                    if best is None or chi2 > best[1]: best = (off, chi2, nn, ioc)
                    if chi2 >= floor:
                        top = int(np.argmax(h))
                        rows.append(dict(target=M, pad=N, orient=orient, offset=off,
                                         n_valid=nn, chi2=round(chi2, 2), ioc=round(ioc, 5),
                                         top_rune=top, top_frac=round(float(h[top]) / nn, 4)))
                if best: pairmax[(M, N, orient)] = best
    print(f"sweep: {len(pairmax)} pair-orientations in {time.time()-t0:.1f}s, "
          f"{len(rows)} rows >= {floor}", file=sys.stderr)
    return rows, pairmax
