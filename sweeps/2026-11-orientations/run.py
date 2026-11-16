#!/usr/bin/env python3
"""Campaign #9 runner — orientations x mirror pairs. PREREG.md committed
ab28743 before any output (CI gate).

Phases:
  --pilot        OUTPUT-BLOCKING collapse-identity check on 3 real mirror
                 pairs (all 16 combos -> 8 classes, exact histogram
                 identity expected); nonzero exit = space re-declared first
  --phase obs    observed sweep, families O1/O2/T1/T2; full CSVs stream to
                 work/orientations/ (sha256), top-100k heap per house policy;
                 leaders get mask=both recompute
  --phase null   family-specific target-shuffle MC of the max INCLUDING
                 orientation+pairing (seed 20261126, 20 draws, checkpointed)

Run from repo root:
  python3 sweeps/2026-11-orientations/run.py --pilot
  python3 sweeps/2026-11-orientations/run.py --phase obs
  python3 sweeps/2026-11-orientations/run.py --phase null [--draws 20]
"""
import argparse, hashlib, heapq, json, os, sys, time, zlib

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import orient as OR  # noqa: E402
from core.kernel import pair_scan  # noqa: E402

WORK = os.path.join(OR.ROOT, "work", "orientations")
RES = os.path.join(HERE, "results")
HDR = "family,key,offset,n_valid,chi2"
PILOT_PAIRS = [(0, 55), (6, 49), (23, 32)]
SEED_NULL = 20261126


class Sink:
    def __init__(self, fam, floor):
        os.makedirs(WORK, exist_ok=True)
        self.path = os.path.join(WORK, f"sweep_{fam}.csv")
        self.f = open(self.path, "w")
        self.f.write(HDR + "\n")
        self.fam = fam
        self.sha = hashlib.sha256((HDR + "\n").encode())
        self.heap, self.floor, self.rows, self.windows, self.positions = \
            [], floor, 0, 0, 0
        self.max = (-1.0, None)

    def add(self, key, off, nn, c2):
        self.windows += 1
        self.positions += nn
        if c2 > self.max[0]:
            self.max = (c2, (key, off, nn))
        if c2 < self.floor:
            return
        self.rows += 1
        s = f"{self.fam},{key},{off},{nn},{c2:.4f}\n"
        self.f.write(s)
        self.sha.update(s.encode())
        item = (c2, key, off, nn)
        if len(self.heap) < 100_000:
            heapq.heappush(self.heap, item)
        elif item > self.heap[0]:
            heapq.heapreplace(self.heap, item)

    def close(self):
        self.f.close()
        return self.sha.hexdigest()


def pilot(grids):
    """All 16 orientation combos on 3 real pairs: verify the declared
    identity (oM,oN) == (r180 oM, r180 oN) EXACTLY (histograms are
    reversal-identical -> bit-identical chi2). Output-blocking."""
    bad = []
    for M, N in PILOT_PAIRS:
        for oM, oN, cM, cN in OR.PAIRING:
            if (cM, cN) < (oM, oN):
                continue      # check each collapse pair once
            for op in ("diff", "sum"):
                A1 = OR.read(*grids[M], oM); B1 = OR.read(*grids[N], oN)
                A2 = OR.read(*grids[M], cM); B2 = OR.read(*grids[N], cN)
                m1 = OR.scan_max(A1, B1, op)
                m2 = OR.scan_max(A2, B2, op)
                if abs(m1[0] - m2[0]) > 1e-9:
                    bad.append((M, N, oM, oN, cM, cN, op, m1, m2))
        # NB: sum-commutativity is NOT checked - falsified at registration:
        # the tgt mask is target-side, so operand order changes the masked
        # set. Sum is therefore scanned in BOTH orders (PREREG correction).
    n_checks = len(PILOT_PAIRS) * (len(OR.PAIRING) // 2 * 2)
    if bad:
        print(f"PILOT FAIL ({len(bad)} mismatches of ~{n_checks}):")
        for b in bad[:10]:
            print("  ", b)
        sys.exit(1)
    print(f"pilot PASS: collapse identities exact on {len(PILOT_PAIRS)} real "
          f"pairs (16 combos -> 8 classes). Space cleared.")


def zero_check(grids):
    """PREREG degeneracy pre-check: D-zero fraction at offset 0 per
    orientation class over mirror pairs (baseline ~1/29 + mask effects)."""
    flags = []
    for oM, oN in OR.CLASSES:
        fr = []
        for M, N in OR.MIRROR_PAIRS:
            A = OR.read(*grids[M], oM); B = OR.read(*grids[N], oN)
            k = min(len(A), len(B))
            keep = A[:k] != 0
            d = (A[:k] - B[:k])[keep] % 29
            fr.append(float((d == 0).mean()))
        mx = max(fr)
        if mx > 0.15:
            flags.append({"class": f"{oM}.{oN}", "max_zero_frac": round(mx, 4)})
    return flags


def phase_obs(grids, floor):
    os.makedirs(RES, exist_ok=True)
    flags = zero_check(grids)
    with open(f"{RES}/zero_check.json", "w") as f:
        json.dump(flags, f, indent=2)
    print(f"zero_check: {len(flags)} flagged (>0.15)", flags, flush=True)
    summary, leaders = [], []
    t0 = time.time()
    for fam in OR.FAMS:
        s = Sink(fam, floor)
        for key, off, nn, c2 in OR.scan_rows(fam, grids):
            s.add(key, off, nn, c2)
        sha = s.close()
        summary.append((fam, s.windows, s.positions, s.rows, s.max, sha))
        print(f"{fam}: windows={s.windows:,} positions={s.positions:,} "
              f"rows>={floor:g}: {s.rows:,} max={s.max[0]:.2f} "
              f"argmax={s.max[1]} sha={sha[:12]} [{time.time()-t0:.0f}s]",
              flush=True)
        for c2, key, off, nn in sorted(s.heap, reverse=True)[:20]:
            leaders.append((fam, key, off, c2, nn))
    with open(f"{RES}/obs_maxima.csv", "w") as f:
        f.write("family,windows,positions,rows_ge_floor,chi2_max,key,offset,"
                "n_valid,full_csv_sha256\n")
        for fam, w, pos, r, (c2, am), sha in summary:
            key, off, nn = am
            f.write(f"{fam},{w},{pos},{r},{c2:.4f},{key},{off},{nn},{sha}\n")
    # leaders: mask=both recompute (house confirmation prong)
    with open(f"{RES}/leaders_both.csv", "w") as f:
        f.write("family,key,offset,chi2_tgt,n_tgt,chi2_both,n_both\n")
        for fam, key, off, c2, nn in leaders:
            cb, nb = recompute_both(fam, key, off, grids)
            f.write(f"{fam},{key},{off},{c2:.4f},{nn},{cb:.4f},{nb}\n")
    with open(f"{RES}/window_counts.json", "w") as f:
        json.dump({fam: {"windows": w, "positions": pos, "rows_ge_floor": r}
                   for fam, w, pos, r, _, _ in summary}, f, indent=2)
    print(f"total {sum(x[1] for x in summary):,} windows / "
          f"{sum(x[2] for x in summary):,} positions in "
          f"{time.time()-t0:.0f}s", flush=True)


def recompute_both(fam, key, off, grids):
    """mask=both chi2 at the recorded offset (confirmation prong)."""
    A, B, op = resolve(fam, key, grids)
    if A is None:
        return -1.0, 0
    for o, nn, c2, ioc, h in pair_scan(A, B, mask="both", stat=op):
        if o == off:
            return c2, nn
    return -1.0, 0


def resolve(fam, key, grids):
    """Recover (A, B, op) for a recorded key by PARSING the key (iterating
    the family would re-run thousands of scans per leader)."""
    if fam == "O1":
        pair, o, op = key.split("|")
        M, N = map(int, pair.split("-"))
        oM, oN = o.split(".")
        A, B = OR.read(*grids[M], oM), OR.read(*grids[N], oN)
        if op in ("dNM", "sNM"):
            A, B = B, A
        return A, B, ("diff" if op[0] == "d" else "sum")
    if fam == "O2":
        pair, op = key.split("|")
        M, N = map(int, pair.split(">"))
        return grids[M][0], grids[N][0], ("diff" if op == "d" else "sum")
    if fam == "T1":
        var, rest = key.split(":", 1)
        pair, o, op = rest.split("|")
        oM, oN = o.split(".")
        S = OR.tok_streams(OR.token_tab(var))
        if pair == "49-51":
            A, B = S["p49"][oM], S["p51"][oN]
            if op in ("dMN", "sMN"):
                pass
            elif op in ("dNM", "sNM"):
                A, B = B, A
            else:
                return None, None, None
            return A, B, ("diff" if op[0] == "d" else "sum")
        T = pair.split("-")[0]                       # "p49-p50" / "p51-p50"
        return S[T][oM], S["p50"][oN], op
    if fam == "T2":
        var, rest = key.split(":", 1)
        T, astr, M = rest.split("|")
        a, M = int(astr[1:]), int(M)
        base = OR.tok_streams(OR.token_tab(var))[T]["id"]   # T already "p49" etc.
        pad = ((a * base.astype(np.int32)) % OR.Q).astype(np.int8)
        return grids[M][0], pad, "diff"
    return None, None, None


def phase_null(grids, draws, seed, only=None):
    os.makedirs(RES, exist_ok=True)
    ck_path = f"{RES}/null_checkpoint.json"
    done = {}
    if os.path.exists(ck_path):
        done = json.load(open(ck_path))
    t0 = time.time()
    for fam in (only or OR.FAMS):
        vals = done.setdefault(fam, [])
        # per-family independent stream: seed + family offset, draw index.
        # crc32, NOT hash(): str hash is salted per process (PYTHONHASHSEED)
        # and silently broke reproducibility in the first 20-draw run
        # (disclosed in REPORT; that checkpoint was discarded).
        fam_off = zlib.crc32(fam.encode()) % 100000
        while len(vals) < draws:
            d = len(vals)
            rng = np.random.default_rng([seed, fam_off, d])
            vals.append(OR.scan_null_draw(fam, grids, rng))
            json.dump(done, open(ck_path, "w"))
            print(f"{fam} draw {d+1}/{draws}: {vals[-1]:.2f} "
                  f"[{time.time()-t0:.0f}s]", flush=True)
    out = {}
    for fam, vals in done.items():
        v = np.array(vals)
        out[fam] = {"draws": len(v), "min": round(float(v.min()), 3),
                    "median": round(float(np.median(v)), 3),
                    "p95": round(float(np.percentile(v, 95)), 3),
                    "max": round(float(v.max()), 3)}
    with open(f"{RES}/null_summary.json", "w") as f:
        json.dump({"seed": seed, "nulls": out}, f, indent=2)
    print(json.dumps(out, indent=2))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pilot", action="store_true")
    ap.add_argument("--phase", choices=["obs", "null"], default=None)
    ap.add_argument("--floor", type=float, default=40.0)
    ap.add_argument("--draws", type=int, default=20)
    ap.add_argument("--only", default=None,
                    help="comma list of families (escalation runs)")
    ap.add_argument("--seed", type=int, default=SEED_NULL)
    args = ap.parse_args()
    grids = OR.load_grids()
    print(f"grids: {len(grids)} pages; unsolved {len(OR.UNSOLVED)}; "
          f"mirror pairs {len(OR.MIRROR_PAIRS)}", flush=True)
    if args.pilot:
        pilot(grids)
    if args.phase == "obs":
        pilot(grids)          # output-blocking, every obs run
        phase_obs(grids, args.floor)
    elif args.phase == "null":
        phase_null(grids, args.draws, args.seed,
                   args.only.split(",") if args.only else None)


if __name__ == "__main__":
    main()
