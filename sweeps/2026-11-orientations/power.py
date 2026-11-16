#!/usr/bin/env python3
"""Campaign #9 power analysis — 10 plants/family, seed 20261127 (PREREG).

Plant: choose pair, orientation class, op(+order), offset; set the PAD page
so the planted window spells crib English (rune indices of a crib string).
Recovery (PREREG): the planted row is the max over the PLANTED PAIR's whole
scan (all classes/ops/orders/offsets — so a plant surfacing under the wrong
class is a plumbing bug, not a find) AND chi2 >= family null median.

Plants modify the pad-side page in memory only (grids dict copy). O2/T2
plants respect identifiability limits disclosed in REPORT (T2: a and offset
both scanned; O2: plain pair plant)."""
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..")))
import orient as OR                                   # noqa: E402
from core.validate import TRANS                       # noqa: E402

SEED = 20261127
RES = os.path.join(HERE, "results")
L2I = {t: i for i, t in TRANS.items()}   # latin -> rune index (dupes: last)
CRIPLINE = "PIGRIMWITNINTHETUNNEL"        # crib-English letters, 29-alpha only
# (PILGRIM/WITHIN/TUNNEL minus vowels that collide; hits checked via crib list)


def plant_bytes(rng, k):
    """k target residues spelling crib letters (cycled crib line)."""
    return np.array([L2I[CRIPLINE[i % len(CRIPLINE)]] for i in range(k)],
                    np.int8)


def plant_page(grids, page, perm, positions, residues):
    """Set raw cells (perm[j] -> raw index) of `page` to given residues."""
    arr, lens = grids[page]
    arr = arr.copy()
    raw = np.asarray(perm)[np.asarray(positions)]
    arr[raw] = np.asarray(residues, np.int8)
    grids[page] = (arr, lens)


def window_positions(m, n, off):
    """(i, j=i-off) pairs inside both streams."""
    ii = [i for i in range(m) if 0 <= i - off < n]
    return ii, [i - off for i in ii]


def keep_nonzero(A, ii):
    return [i for i in ii if A[i] != 0]          # tgt mask survivors


def plant_scan_pair(g, M, N, classes):
    """Full pair scan (classes x 2 ops x 2 orders x all offsets) -> best row.
    Orders: dMN/dNM and sMN/sNM both scanned (mask correction), flip=True
    means operands swapped, matching iter_fam key semantics."""
    best = (-1.0, None)
    for oM, oN in classes:
        A = OR.read(*g[M], oM)
        B = OR.read(*g[N], oN)
        for op in ("diff", "sum"):
            for flip in (False, True):
                X, Y = (B, A) if flip else (A, B)
                for off, nn, c2, ioc, h in OR.pair_scan(X, Y, mask="tgt",
                                                        stat=op):
                    key = (oM, oN, op, flip, off)
                    if c2 > best[0]:
                        best = (c2, key)
    return best


def do_plant(fam, rng, grids, null_med):
    """One plant; returns dict(ok, chi2, detail)."""
    if fam in ("O1", "O2"):
        pairs = (OR.MIRROR_PAIRS if fam == "O1"
                 else [(m, n) for m in OR.UNSOLVED[:12]
                       for n in OR.UNSOLVED[13:25] if m != n])
        M, N = pairs[rng.integers(len(pairs))]
        oM, oN = OR.CLASSES[rng.integers(len(OR.CLASSES))] \
            if fam == "O1" else ("id", "id")
        op = ("diff", "sum")[rng.integers(2)]
        rng.integers(2)   # keep stream layout stable (flip is not a thing:
        # a physical plant lights BOTH rows - (flip=False,+off) with D=res
        # and (flip=True,-off) with D=-res; -res is a bin permutation of res
        # -> identical chi2; only the tgt-mask side differs slightly)
        A = OR.read(*grids[M], oM)
        B_len = len(grids[N][0])
        m = len(A)
        off = int(rng.integers(-(B_len - 60), m - 60))
        ii, jj = window_positions(m, B_len, off)
        ii = keep_nonzero(A, ii)
        jj = [i - off for i in ii]
        k = len(ii)
        if k < 60:
            return {"ok": None, "why": "window<60"}
        res = plant_bytes(rng, k)
        # pad values so that (A - P) or (A + P) = res at the window
        padres = ((A[ii] - res) % 29) if op == "diff" else ((res - A[ii]) % 29)
        g = {p: (a.copy(), l) for p, (a, l) in grids.items()}
        perm = OR.perm_of(grids[N][1], oN if fam == "O1" else "id")
        plant_page(g, N, perm, jj, padres)
        classes = OR.CLASSES if fam == "O1" else [("id", "id")]
        c2, key = plant_scan_pair(g, M, N, classes)
        # physical plant = BOTH mirror rows: (False,+off) and (True,-off)
        same = key[:3] == (oM, oN, op) and \
            ((key[3], key[4]) == (False, off) or
             (key[3], key[4]) == (True, -off))
        ok = same and c2 >= null_med
        return {"ok": bool(ok), "chi2": round(float(c2), 2),
                "planted": (oM, oN, op, off), "found": key,
                "n": k, "ge_med": bool(c2 >= null_med)}
    if fam in ("T1", "T2"):
        tab = OR.token_tab("canon")
        var = "canon"
        S = OR.tok_streams(tab)
        if fam == "T1":
            oM, oN = OR.CLASSES[rng.integers(len(OR.CLASSES))]
            op = ("diff", "sum")[rng.integers(2)]
            A = S["p49"][oM]
            off = int(rng.integers(-(len(S["p51"]["id"]) - 60),
                                   len(A) - 60))
            ii, jj = window_positions(len(A), len(S["p51"]["id"]), off)
            ii = [i for i in ii if A[i] != 0]
            jj = [i - off for i in ii]
            k = len(ii)
            if k < 60:
                return {"ok": None, "why": "window<60"}
            res = plant_bytes(rng, k)
            padres = ((A[ii] - res) % 29) if op == "diff" \
                else ((res - A[ii]) % 29)
            # token = 1 byte, 8 per row: oriented stream index jj -> raw
            perm = OR.perm_of([8] * 9, oN)      # p51: 9 rows x 8
            raws = np.asarray(perm)[np.asarray(jj)]
            tab2 = tab.copy()
            tab2[184 + raws] = padres.astype(np.uint8)
            S2 = OR.tok_streams(tab2)
            best = (-1.0, None)
            for cM, cN in OR.CLASSES:
                for o2 in ("diff", "sum"):
                    for X, Y, flip in ((S2["p49"][cM], S2["p51"][cN], False),
                                       (S2["p51"][cN], S2["p49"][cM], True)):
                        for off2, nn, c2, ioc, h in OR.pair_scan(
                                X, Y, mask="tgt", stat=o2):
                            if c2 > best[0]:
                                best = (c2, (cM, cN, o2, flip, off2))
            ok = (best[1][:3] == (oM, oN, op) and
                  ((best[1][3], best[1][4]) == (False, off) or
                   (best[1][3], best[1][4]) == (True, -off)) and
                  best[0] >= null_med)
            return {"ok": bool(ok), "chi2": round(float(best[0]), 2),
                    "planted": (oM, oN, op, off), "found": best[1],
                    "n": k, "ge_med": bool(best[0] >= null_med)}
        # T2: pick a, plant table residue so a*T hits the crib at page M
        a = int(rng.integers(2, 29))
        M = OR.UNSOLVED[rng.integers(len(OR.UNSOLVED))]
        A = grids[M][0]
        T = ("p49", "p50", "p51")[rng.integers(3)]
        base_len = {"p49": 80, "p50": 104, "p51": 72}[T]     # tokens = bytes
        off = int(rng.integers(-(base_len - 60), len(A) - 60))
        ii, jj = window_positions(len(A), base_len, off)
        ii = [i for i in ii if A[i] != 0]
        jj = [i - off for i in ii]
        k = len(ii)
        if k < 60:
            return {"ok": None, "why": "window<60"}
        res = plant_bytes(rng, k)
        inv = pow(a, 27, 29)
        # want D = A - pad = res at the window => pad = A - res => T = (A-res)/a
        tres = (((A[np.asarray(ii)] - res) % 29) * inv % 29).astype(np.uint8)
        tab2 = tab.copy()
        sl = {"p49": 0, "p50": 80, "p51": 184}[T]
        # T2 is id-orientation only: stream index = raw byte offset directly
        tab2[sl + np.asarray(jj)] = tres
        base = OR.tok_streams(tab2)[T]["id"].astype(np.int32) % 29
        pad = ((a * base) % 29).astype(np.int8)
        best = (-1.0, None)
        for a2 in range(2, 29):
            p2 = ((a2 * base) % 29).astype(np.int8)
            for off2, nn, c2, ioc, h in OR.pair_scan(A, p2, mask="tgt",
                                                     stat="diff"):
                if c2 > best[0]:
                    best = (c2, (a2, off2))
        ok = best[1] == (a, off) and best[0] >= null_med
        return {"ok": bool(ok), "chi2": round(float(best[0]), 2),
                "planted": (a, off), "found": best[1], "n": k,
                "ge_med": best[0] >= null_med}


def main():
    grids = OR.load_grids()
    try:
        med = json.load(open(f"{RES}/null_summary.json"))["nulls"]
    except FileNotFoundError:
        sys.exit("null_summary.json missing - run --phase null first")
    rng = np.random.default_rng(SEED)
    out = {}
    for fam in OR.FAMS:
        rows, tries = [], 0
        while len(rows) < 10 and tries < 60:
            tries += 1
            r = do_plant(fam, rng, grids, med[fam]["median"])
            if r.get("ok") is None:
                continue
            rows.append(r)
        okc = sum(1 for r in rows if r["ok"])
        out[fam] = {"plants": len(rows), "recovered": okc,
                    "null_med": med[fam]["median"], "detail": rows}
        print(f"{fam}: {okc}/{len(rows)} recovered (median "
              f"{med[fam]['median']})", flush=True)
    with open(f"{RES}/power.json", "w") as f:
        json.dump({"seed": SEED, "crib_line": CRIPLINE, "power": out},
                  f, indent=2, default=str)


if __name__ == "__main__":
    main()
