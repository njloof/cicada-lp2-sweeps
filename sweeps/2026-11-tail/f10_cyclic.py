#!/usr/bin/env python3
"""Campaign #24 Lane B — F10 mid-range cyclic steps (PREREG
sweeps/2026-11-tail/PREREG.md, committed 1a48cec BEFORE output).

W harness (#6) extended to steps a coprime in 29..L-29 (the
mid-range #6 left open). Self-pair pads EXCLUDED (#6 AMENDMENT
inherited). Statistic: chi2 vs uniform, 29 bins, of (A - pad) mod 29.
Null: target-shuffle MC, 20 draws, seed 20261225; shuffle stream
pre-drawn single-process (bit-identical), scans parallelized (fork).
Gate B-G1: exhaustive cut-coverage for mid-range steps, k-boost rule
(k0..16 per source, disclosed). GO iff obs > 1.1 x null-max AND the
top cell survives mask=both above the same bar AND >=2 English cribs
(#6 rule). Budget-chunked + checkpointed (10-min foreground cap);
fully resumable.

Run (studio):  python3 sweeps/2026-11-tail/f10_cyclic.py --budget 480
"""
import argparse
import heapq
import json
import math
import multiprocessing as mp
import os
import random
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, ROOT)
import numpy as np                      # noqa: E402
from core import DATA, kernel           # noqa: E402
import core.validate as V               # noqa: E402
from core.cribs import REPR as CRIBS    # noqa: E402

WORK = os.path.join(ROOT, "work", "tail_f10")
OUT = os.path.join(HERE, "results")
Q = 29
SEED = 20261225
NDRAW = 20
TRACK_TOP = 1000                       # rows persisted per target
VAL = [g[1] for g in V.GEMATRIA]
MERGE = str.maketrans("KVZQ", "CUSS")
G = {}


def load_sources():
    # p50 is the runeless hole: dropped defensively (a stale pre-hole
    # lp2_50.txt lingers on the studio mirror — rsync does not delete)
    pages = {n: a for n, a in kernel.load_pages().items() if n != 50}
    # 55 unsolved pages (p55 unsolved — #6's n<=54 predates the p55
    # census; G1 asserts N=12,956 here)
    targets = [n for n in pages if n <= 55]
    pt = {}
    sp = f"{DATA}/solved_plaintexts.json"
    if os.path.exists(sp):
        # keys are names ("ANEND56", "PARABLE57") — kept as str source keys
        pt = {k: np.array(v, dtype=np.int8)
              for k, v in json.load(open(sp)).items()}
    return pages, targets, {**pages, **pt}


def usable_offsets(A, L):
    m = len(A)
    pre = np.concatenate([[0], np.cumsum(A != 0)])
    return np.array([o for o in range(50 - L, m - 49)
                     if pre[min(m, o + L)] - pre[max(0, o)] >= 50])


def kboost_map(pages, targets, sources):
    """B-G1: minimal k in {k0..16} with COMPLETE mid-range alignment
    coverage per source (guarantee-1 machinery; rev pads of step a
    induce cuts {a(L-1)+c} for step L-a, also mid-range)."""
    kmap = {}
    for N, S in sources.items():
        L = len(S)
        k0 = math.ceil(L / (L - 49))
        if L <= 58:                      # no mid-range steps exist
            kmap[N] = k0
            continue
        ok = False
        for k in range(k0, 17):
            bad = 0
            for M in targets:
                us = usable_offsets(pages[M], L)
                if len(us) == 0:
                    raise SystemExit(f"B-G1: no usable offsets {N}->{M}")
                for a in range(29, L - 28):
                    if math.gcd(a, L) != 1:
                        continue
                    cuts = [(a * ((i * L) // k)) % L for i in range(k)]
                    for ap, cs in ((a, cuts),
                                   (L - a, [(a * (L - 1) + c) % L
                                            for c in cuts])):
                        if not (29 <= ap <= L - 29):
                            continue
                        cov = np.zeros(L, bool)
                        for c in cs:
                            cov[(c - ap * us) % L] = True
                        bad += int((~cov).sum())
            if bad == 0:
                kmap[N] = k
                ok = True
                break
        if not ok:
            raise SystemExit(f"B-G1 FAIL: source {N} L={L} no k<=16")
        if kmap[N] != k0:
            print(f"  k-boost: source {N} L={L} k {k0}->{kmap[N]}",
                  flush=True)
    return kmap


def build_pad(S, a, i, k, rev):
    L = len(S)
    c = (a * ((i * L) // k)) % L
    pad = S[(a * np.arange(L) + c) % L]
    return pad[::-1] if rev else pad


def all_pads(sources, kmap):
    """(N, name, pad) list; name = c{a}.{i}[r]."""
    out = []
    for N, S in sources.items():
        L = len(S)
        k = kmap[N]
        for a in range(29, L - 28):
            if math.gcd(a, L) != 1:
                continue
            for i in range(k):
                out.append((N, f"c{a}.{i}", build_pad(S, a, i, k, False)))
                out.append((N, f"c{a}.{i}r", build_pad(S, a, i, k, True)))
    return out


def scan_max(A, B, mask="tgt", min_len=kernel.MIN_LEN):
    m, n = len(A), len(B)
    if mask == "both":
        Valid = (A[:, None] != 0) & (B[None, :] != 0)
    else:
        Valid = np.repeat((A != 0)[:, None], n, axis=1)
    ii, jj = np.nonzero(Valid)
    d = (ii - jj) + (n - 1)
    vals = (A[ii].astype(np.int32) - B[jj].astype(np.int32)) % Q
    H = np.bincount(d * Q + vals,
                    minlength=(m + n - 1) * Q).reshape(m + n - 1, Q)
    cnt = H.sum(1)
    ok = cnt >= min_len
    if not ok.any():
        return -1.0
    with np.errstate(divide="ignore", invalid="ignore"):
        chi2 = (Q / cnt) * (H * H).sum(1) - cnt
    return float(chi2[ok].max())


def selfcheck():
    M = G["targets"][0]
    A = G["pages"][M]
    done = 0
    for N, w, W in G["pads"]:
        if N == M:
            continue
        loop = max(c for _, _, c, _, _ in kernel.pair_scan(A, W))
        assert abs(loop - scan_max(A, W)) < 1e-6, (N, w)
        done += 1
        if done >= 5:
            return


def obs_target(M):
    A = G["pages"][M]
    heap, mx, nwin, seq = [], -1.0, 0, 0
    for N, w, W in G["pads"]:
        if N == M:
            continue
        for off, nn, chi2, ioc, h in kernel.pair_scan(A, W):
            nwin += 1
            if chi2 > mx:
                mx = chi2
            seq += 1
            # (chi2, seq, row): seq tiebreaks so mixed int/str source
            # keys are never tuple-compared
            item = (round(chi2, 2), seq, (M, N, w, off, nn))
            if len(heap) < TRACK_TOP:
                heapq.heappush(heap, item)
            elif item > heap[0]:
                heapq.heapreplace(heap, item)
    return M, mx, nwin, heap


def null_task(dM):
    d, M = dM
    A = G["pages"][M][G["shuffles"][d][M]]
    mx = -1.0
    for N, w, W in G["pads"]:
        if N == M:
            continue
        v = scan_max(A, W)
        if v > mx:
            mx = v
    return d, mx


def main():
    try:
        mp.set_start_method("fork")
    except RuntimeError:
        pass
    global NDRAW
    ap = argparse.ArgumentParser()
    ap.add_argument("--budget", type=int, default=480)
    ap.add_argument("--ndraw", type=int, default=20,
                    help="null draws; PREREG escalation rule -> 200")
    a = ap.parse_args()
    NDRAW = a.ndraw
    t0 = time.time()
    os.makedirs(WORK, exist_ok=True)
    os.makedirs(OUT, exist_ok=True)
    pages, targets, sources = load_sources()
    assert sum(len(pages[n]) for n in targets) == 12956, "G1 FAIL"

    KF = f"{WORK}/kmap.json"
    if os.path.exists(KF):
        # JSON stringifies int keys; restore numeric page keys, keep names
        kmap = {(int(k) if k.isdigit() else k): v
                for k, v in json.load(open(KF)).items()}
    else:
        kmap = kboost_map(pages, targets, sources)
        json.dump(kmap, open(KF, "w"))
    pads = all_pads(sources, kmap)
    G.update(pages=pages, targets=targets, sources=sources, kmap=kmap,
             pads=pads)
    selfcheck()
    boosts = {N: k for N, k in kmap.items()
              if k != math.ceil(len(sources[N]) / (len(sources[N]) - 49))
              and len(sources[N]) > 58}
    print(f"pads={len(pads)} kboosts={boosts}", flush=True)

    # ---- observed scan (parallel over targets, resumable) ----
    DONEF, ROWSF = f"{WORK}/obs_done.json", f"{WORK}/obs_rows.jsonl"
    done = json.load(open(DONEF)) if os.path.exists(DONEF) else []
    todo = [M for M in targets if M not in done]
    if todo:
        with mp.Pool() as pool:
            for M, mx, nwin, heap in pool.imap_unordered(obs_target, todo):
                with open(ROWSF, "a") as f:
                    for c2, _, row in sorted(heap, key=lambda r: -r[0]):
                        f.write(json.dumps([c2] + list(row)) + "\n")
                done.append(M)
                json.dump(done, open(DONEF, "w"))
                print(f"  obs target {M}: max {mx:.1f} win {nwin} "
                      f"({time.time()-t0:.0f}s)", flush=True)
                if time.time() - t0 > a.budget:
                    pool.terminate()
                    print(f"PARTIAL (observed {len(done)}/55) — rerun",
                          flush=True)
                    return

    # ---- null: shuffle stream pre-drawn once (bit-identical) ----
    SF = f"{WORK}/shuffles.json"

    def draw_stream():
        # one sequential stream, d-major M-minor (bit-identical reruns)
        rng = random.Random(SEED)
        sh = {}
        for d in range(NDRAW):
            sh[str(d)] = {}
            for M in targets:
                ix = list(range(len(pages[M])))
                rng.shuffle(ix)
                sh[str(d)][str(M)] = ix
        return sh

    shf = json.load(open(SF)) if os.path.exists(SF) else None
    if shf is not None and (len(shf) != NDRAW or any(
            len(v) != len(targets) for v in shf.values())):
        print("shuffles.json malformed (first-run comprehension bug) — "
              "redrawn from seed", flush=True)
        shf = None
    if shf is None:
        shf = draw_stream()
        json.dump(shf, open(SF, "w"))
    G["shuffles"] = {int(d): {int(M): np.array(v)
                              for M, v in dd.items()}
                     for d, dd in shf.items()}
    NULLF = f"{WORK}/null_maxes.txt"
    nulls = ([int(x) for x in open(NULLF).read().split()]
             if os.path.exists(NULLF) else [])
    with mp.Pool() as pool:
        for d in range(len(nulls), NDRAW):
            res = pool.map(null_task, [(d, M) for M in targets])
            gm = max(mx for _, mx in res)
            nulls.append(int(round(gm * 100)))
            with open(NULLF, "a") as f:
                f.write(f"{int(round(gm*100))}\n")
            print(f"  null draw {d+1}/{NDRAW}: max {gm:.1f} "
                  f"({time.time()-t0:.0f}s)", flush=True)
            if time.time() - t0 > a.budget:
                pool.terminate()
                print(f"PARTIAL (null {len(nulls)}/{NDRAW}) — rerun",
                      flush=True)
                return

    # ---- verdict ----
    rows = [json.loads(l) for l in open(ROWSF)]
    rows.sort(key=lambda r: -r[0])
    obs, M, N, w, off, nn = rows[0]
    assert M in targets and N in sources, f"bad top row {rows[0]}"
    nulls_f = [x / 100 for x in nulls]
    nmax = max(nulls_f)
    beats = sum(1 for x in nulls_f if x >= obs)
    p = (1 + beats) / (len(nulls_f) + 1)
    # prong 2: top cell re-windowed under mask=both
    A = pages[M]
    S = sources[N]
    k = kmap[N]
    a_, i_ = w[1:].split(".")
    a = int(a_)
    rev = i_.endswith("r")
    i = int(i_[:-1] if rev else i_)
    pad = build_pad(S, a, i, k, rev)
    m, n = len(A), len(pad)
    ii = np.arange(max(0, off), min(m, off + n))
    keep = (A[ii] != 0) & (pad[ii - off] != 0)
    nnb = int(keep.sum())
    if nnb >= kernel.MIN_LEN:
        vals = (A[ii][keep].astype(int) - pad[ii - off][keep].astype(int)) % Q
        h = np.bincount(vals, minlength=Q)
        both = (Q / nnb) * float((h * h).sum()) - nnb
    else:
        both = -1.0
    # prong 3: cribs in the top decode (mask=tgt window)
    D = (A[ii].astype(int) - pad[ii - off].astype(int)) % Q
    txt = "".join(VAL[x] for x in D.tolist()).upper().translate(MERGE)
    cribs = [c for c in CRIBS if c in txt]
    go = obs > 1.1 * nmax and both > 1.1 * nmax and len(cribs) >= 2
    med = sorted(nulls_f)[len(nulls_f) // 2]
    rep = [
        f"pads={len(pads)} (k-boosts {boosts}); top row {rows[0]}",
        f"obs max {obs:.1f}; null ({NDRAW} draws, seed {SEED}): min "
        f"{min(nulls_f):.1f} med {med:.1f} max {nmax:.1f}; p={p:.4f}",
        f"prong1 obs>1.1*nullmax({1.1*nmax:.1f}): {obs > 1.1*nmax}; "
        f"prong2 mask=both {both:.1f} (n={nnb}): {both > 1.1*nmax}; "
        f"prong3 cribs {cribs[:6]}: {len(cribs) >= 2}",
        f"decode: {txt[:80]}",
        "VERDICT: " + ("GO -> FLAG FOR OWNER (never auto-certified)"
                       if go else
                       "NEGATIVE — mid-range cyclic steps 29..L-29 closed "
                       "(self-pairs excluded, #6 amendment inherited)"),
        f"escalation (#6 rule): obs >= null median? {obs >= med} "
        f"(True & not GO -> extend to >=200 draws before verdict)",
        "DISCLOSURES: (1) self-pair pads excluded (#6 AMENDMENT). (2) "
        "persisted rows = top-1000 per target, not the full ~611M-window "
        "family (repo size policy). (3) shuffle stream pre-drawn "
        "single-process: bit-identical under parallel scan. (4) kmap in "
        f"work/tail_f10/kmap.json. (5) runtime {time.time()-t0:.0f}s "
        "across chunks."]
    with open(f"{OUT}/LANE_B_REPORT.md", "w") as f:
        f.write("# Campaign #24 Lane B (F10 mid-range cyclic) report\n\n"
                + "\n\n".join(rep) + "\n")
    print("\n".join(rep))


if __name__ == "__main__":
    main()
