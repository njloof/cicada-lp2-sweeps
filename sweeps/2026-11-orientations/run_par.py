#!/usr/bin/env python3
"""Parallel MC null (house pattern from #7 run_par.py) — BIT-IDENTICAL to
run.py --phase null: each draw's rng is reconstructed in the worker as
default_rng([seed, crc32(fam), d]) and scan_null_draw makes the same rng
calls in the same order as the serial path, so results are independent of
worker scheduling and reproducible from the pinned seed alone.

  python3 sweeps/2026-11-orientations/run_par.py [--fams O1,O2,T1,T2]
          [--draws 20] [--seed 20261126]
Writes the same null_checkpoint.json / null_summary.json shapes as run.py.
"""
import argparse, json, os, sys, time, zlib
import multiprocessing as mp

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..")))
import orient as OR                                    # noqa: E402

RES = os.path.join(HERE, "results")
_G = None


def _init():
    global _G
    _G = OR.load_grids()


def _one(job):
    fam, seed, d = job
    rng = np.random.default_rng([seed, zlib.crc32(fam.encode()) % 100000, d])
    return fam, d, OR.scan_null_draw(fam, _G, rng)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fams", default="O1,O2,T1,T2")
    ap.add_argument("--draws", type=int, default=20)
    ap.add_argument("--seed", type=int, default=20261126)
    a = ap.parse_args()
    fams, seed, draws = a.fams.split(","), a.seed, a.draws
    os.makedirs(RES, exist_ok=True)
    ck_path = f"{RES}/null_checkpoint.json"
    done = json.load(open(ck_path)) if os.path.exists(ck_path) else {}
    jobs = []
    for fam in fams:
        vals = done.setdefault(fam, [])
        for d in range(len(vals), draws):
            jobs.append((fam, seed, d))
    print(f"{len(jobs)} draws to run on {mp.cpu_count()} cores", flush=True)
    t0 = time.time()
    got = {fam: {} for fam in fams}          # fam -> {draw idx: value}
    base = {fam: len(done[fam]) for fam in fams}
    with mp.Pool(min(max(len(jobs), 1), mp.cpu_count()), initializer=_init) as p:
        for fam, d, v in p.imap_unordered(_one, jobs):
            got[fam][d] = v
            # flush only the contiguous prefix so the checkpoint stays in
            # DRAW ORDER (the serial path resumes at index len(vals))
            n = base[fam]
            while n in got[fam]:
                done[fam].append(got[fam].pop(n))
                n += 1
            json.dump(done, open(ck_path, "w"))
            print(f"{fam} d{d}: {v:.2f} [{time.time()-t0:.0f}s]", flush=True)
    json.dump(done, open(ck_path, "w"))
    out = {}
    for fam, vals in done.items():
        v = np.array(vals)
        out[fam] = {"draws": len(v), "min": round(float(v.min()), 3),
                    "median": round(float(np.median(v)), 3),
                    "p95": round(float(np.percentile(v, 95)), 3),
                    "max": round(float(v.max()), 3)}
    json.dump({"seed": seed, "nulls": out}, open(f"{RES}/null_summary.json", "w"),
              indent=2)
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
