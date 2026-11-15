"""Shared construction for campaign #8 (self-derived value keys).
PREREG: PREREG.md — registered 2026-11-15 before any output.
All keys are derived from the target page's OWN rune values; the null
therefore re-derives them from shuffled targets (derive-from-shuffled)."""
import os, sys

import numpy as np

_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
sys.path.insert(0, _ROOT)
from core.validate import flat, GEMATRIA, N as Q  # noqa: E402
from core.kernel import pair_scan  # noqa: E402

PRIME = np.array([p for _r, _t, p in GEMATRIA], dtype=np.int64)
TARGETS = list(range(55))
PAGES = os.path.join(_ROOT, "data", "pages")


def phi(n):
    if n <= 1:
        return n
    r, d, nn = n, 2, n
    while d * d <= nn:
        if nn % d == 0:
            while nn % d == 0:
                nn //= d
            r -= r // d
        d += 1
    if nn > 1:
        r -= r // nn
    return r


def digitsum(v):
    return sum(int(c) for c in str(abs(v)))


PHI_MAP = np.array([phi(v) % Q for v in range(Q)], dtype=np.int16)
DS_MAP = np.array([digitsum(v) % Q for v in range(Q)], dtype=np.int16)


def page_lines(n):
    """Line-structured page from the pinned corpus (line structure is part
    of the transcription; the single-root caveat in docs/TRANSCRIPTION_AUDIT
    applies)."""
    p = os.path.join(PAGES, f"lp2_{n:02d}.txt")
    return [[int(x) for x in ln.split()] for ln in open(p) if ln.strip()]


def line_lengths(n):
    """Corpus line lengths for page n — the segmentation the LS family uses.
    Lengths (not values) come from disk: values must come from the array
    under test so the derive-from-shuffled null re-derives keys from the
    shuffled target rather than from the unshuffled corpus."""
    return [len(l) for l in page_lines(n)]


def chi2_of(vals):
    nn = len(vals)
    if nn < 50:
        return -1.0
    h = np.bincount(vals, minlength=Q).astype(np.float64)
    return (Q / nn) * float((h * h).sum()) - nn


# ---------- LS: line-sum segment self-keys ----------

def ls_keys(n, A):
    """[(tag, K piecewise-constant key)] — 12 variants minus constants.
    Line SUMS come from A (the array under test); line LENGTHS from the
    corpus. This is what makes the derive-from-shuffled null meaningful:
    shuffle A and the segment values change with it, while the segmentation
    (a transcription property) is held fixed."""
    A = np.asarray(A)
    lens = line_lengths(n)
    assert sum(lens) == len(A), f"wrapping integrity p{n}"
    edges = np.cumsum([0] + lens)
    sums = [int(PRIME[A[edges[i]:edges[i + 1]]].sum()) for i in range(len(lens))]
    out = []
    for tname, T in (("i", lambda s: s), ("p", phi), ("d", digitsum)):
        for cum in (False, True):
            for sign in (1, -1):
                vals = [T(s) % Q for s in sums]
                if cum:
                    run, acc = [], 0
                    for v in vals:
                        acc = (acc + v) % Q
                        run.append(acc)
                    vals = run
                if sign < 0:
                    vals = [(-v) % Q for v in vals]
                if len(set(vals)) < 2:
                    continue  # constant key: chi2-invariant, excluded
                K = np.repeat(np.array(vals, dtype=np.int16), lens)
                out.append((f"ls:{tname}{'c' if cum else ''}{'-' if sign < 0 else ''}", K))
    return out


# ---------- VT / CF: self-derived pads ----------

def vt_pads(A):
    pads = [("vt:phi", PHI_MAP[A]), ("vt:ds", DS_MAP[A])]
    return [(t + ("r" if rev else ""), (p[::-1] if rev else p))
            for t, p in pads for rev in (False, True)]


def _slide(A, w):
    c = np.concatenate([[0], np.cumsum(A.astype(np.int64))])
    i = np.arange(len(A))
    lo = np.maximum(0, i - w)
    return ((c[i] - c[lo]) % Q).astype(np.int16)


def cf_pads(A):
    pre = np.empty(len(A), dtype=np.int16)
    pre[0] = 0
    pre[1:] = np.cumsum(A.astype(np.int64)[:-1]) % Q
    pads = [("cf:pre", pre)] + [(f"cf:w{w}", _slide(A, w)) for w in (2, 3, 5)]
    return [(t + ("r" if rev else ""), (p[::-1] if rev else p))
            for t, p in pads for rev in (False, True)]


def pad_by_tag(tag, n, A):
    """Recover a pad by tag (for mask=both recompute and power checks)."""
    if tag.startswith("ls:"):
        for t, K in ls_keys(n, A):
            if t == tag:
                return K
        return None
    for t, p in vt_pads(A) + cf_pads(A):
        if t == tag:
            return p
    return None


def iter_rows(fams, targets, arrays=None):
    """Yield (fam, target, tag, offset, n_valid, chi2) rows; count windows
    via the caller (each yielded row is one window's positions)."""
    for n in targets:
        A = np.asarray(arrays[n] if arrays is not None else flat(n), dtype=np.int16)
        if "LS" in fams:
            for tag, K in ls_keys(n, A):
                keep = A != 0
                c2 = chi2_of((A[keep] - K[keep]) % Q)
                if c2 >= 0:
                    yield ("LS", n, tag, 0, int(keep.sum()), c2)
        if "VT" in fams:
            for tag, pad in vt_pads(A):
                for off, nn, c2, _ioc, _h in pair_scan(A, pad, mask="tgt", min_len=50):
                    yield ("VT", n, tag, off, nn, c2)
        if "CF" in fams:
            for tag, pad in cf_pads(A):
                for off, nn, c2, _ioc, _h in pair_scan(A, pad, mask="tgt", min_len=50):
                    yield ("CF", n, tag, off, nn, c2)


def window_counts(fams, targets, arrays=None):
    """Count valid positions (windows) per family without scanning stats."""
    tot = {f: 0 for f in fams}
    for n in targets:
        A = np.asarray(arrays[n] if arrays is not None else flat(n), dtype=np.int16)
        m = len(A)
        nz = int((A != 0).sum())
        if "LS" in fams:
            tot["LS"] += nz * len(ls_keys(n, A))
        if "VT" in fams:
            tot["VT"] += 4 * nz * m  # 4 pads x full overlap grid (mask=tgt)
        if "CF" in fams:
            tot["CF"] += 8 * nz * m
    return tot


def family_max(fams, targets, arrays):
    best = {}
    for fam, n, tag, off, nn, c2 in iter_rows(fams, targets, arrays):
        if fam not in best or c2 > best[fam][0]:
            best[fam] = (c2, n, tag, off, nn)
    return best


def zero_check(targets):
    """Pre-output degeneracy check: per-scheme D-zero fraction at maximal
    overlap vs the no-structure baseline. Returns flagged rows."""
    flags = []
    for n in targets:
        A = np.array(flat(n), dtype=np.int16)
        for fam, pairs in (("LS", ls_keys(n, A)), ("VT", vt_pads(A)), ("CF", cf_pads(A))):
            for tag, K in pairs:
                keep = A != 0
                if fam != "LS":
                    keep = np.ones(len(A), dtype=bool)  # o=0 full overlap
                    keep &= (A != 0)
                D = (A - K) % Q
                zf = float((D[keep] == 0).mean())
                if zf > 0.15:
                    flags.append((fam, n, tag, round(zf, 3)))
    return flags
