#!/usr/bin/env python3
"""Monte-Carlo null machinery shared by campaigns.

Null model: each target page's runes are shuffled IN-PAGE (preserves page length,
symbol frequencies, F density — exactly the structure the real sweep sees). For each
shuffle we run the identical sweep machinery and record the GLOBAL max chi2 over all
windows. The empirical distribution of the max gives the threshold the real search
space actually demands (Bonferroni-on-29-bin-p-values is only a sanity band, and for
correlated overlapping windows it is anti-conservative).
"""
import numpy as np, sys, time
from core import kernel

def null_maxima(pages, targets, pads, n=20, mask="tgt", mirror=False, seed=20261113,
                extra_pads=(), verbose=True):
    """Returns list of global-max chi2, one per shuffle.
    extra_pads: [(name, np.int8 array)] scanned against every target (fwd/rev)."""
    rng = np.random.default_rng(seed)
    maxima = []
    t0 = time.time()
    for it in range(n):
        shuffled = dict(pages)
        for M in targets:                    # shuffle target pages only; pads stay real
            p = pages[M].copy(); rng.shuffle(p); shuffled[M] = p
        _, pairmax = kernel.run_sweep(shuffled, targets, pads, mask=mask,
                                      mirror=mirror, floor=1e18)  # floor: keep no rows
        gmax = max(v[1] for v in pairmax.values())
        for pname, pstream in extra_pads:
            for orient, B in kernel.orientations(pstream):
                for M in targets:
                    for off, nn, chi2, ioc, h in kernel.pair_scan(shuffled[M], B, mask=mask):
                        gmax = max(gmax, chi2)
        maxima.append(gmax)
        if verbose:
            print(f"shuffle {it:2d}: global max chi2 = {gmax:.1f}   ({time.time()-t0:.0f}s)",
                  flush=True)
    return maxima
