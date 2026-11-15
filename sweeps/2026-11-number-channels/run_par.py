#!/usr/bin/env python3
"""Parallel MC null for campaign #7 (runs on studio.local; identical
semantics to calibrate.py). Draw contents are bit-identical to the
registered single-stream design: all 20 shuffled corpora are generated
sequentially from default_rng(seed) in the exact call order calibrate.py
uses (per draw, one rng.permutation per target, ascending target order);
only the heavy family_max scans are then fanned out to worker processes.
Writes the same checkpoint/final JSON shapes as calibrate.py."""
import csv, json, multiprocessing as mp, os, sys, time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
import numkeys as NK  # noqa: E402

RES = os.path.join(HERE, "results")
import argparse
_ap = argparse.ArgumentParser()
_ap.add_argument("--fams", default="Vp,Vs,R,D")
_ap.add_argument("--draws", type=int, default=20)
_ap.add_argument("--seed", type=int, default=20261122)
_args = _ap.parse_args()
FAMS = _args.fams.split(",")
SEED = _args.seed
DRAWS = _args.draws

_VARIANTS = None
_ARRAYS0 = None


def _init():
    global _VARIANTS, _ARRAYS0
    _VARIANTS, tg = NK.variants_and_targets()
    _ARRAYS0 = {n: np.array(NK.flat(n), dtype=np.int16) for n in tg}


def _one_draw(shuf):
    return NK.family_max(FAMS, _VARIANTS, sorted(shuf.keys()), shuf)


def main():
    t0 = time.time()
    variants, targets = NK.variants_and_targets()
    arrays0 = {n: np.array(NK.flat(n), dtype=np.int16) for n in targets}
    rng = np.random.default_rng(SEED)
    draws = []
    for _ in range(DRAWS):  # exact calibrate.py RNG call order
        draws.append({n: rng.permutation(arrays0[n]).astype(np.int16) for n in targets})
    print(f"shuffled corpora generated in {time.time()-t0:.1f}s", flush=True)
    with mp.Pool(min(DRAWS, mp.cpu_count()), initializer=_init) as pool:
        results = pool.map(_one_draw, draws)
    maxima = {f: [round(r[f][0], 4) if f in r else None for r in results] for f in FAMS}
    os.makedirs(RES, exist_ok=True)
    json.dump({"seed": SEED, "fams": FAMS, "done": DRAWS, "maxima": maxima},
              open(os.path.join(RES, f"null_{'_'.join(FAMS)}_checkpoint.json"), "w"))
    json.dump({"seed": SEED, "fams": FAMS, "done": DRAWS, "maxima": maxima},
              open(os.path.join(RES, f"null_{'_'.join(FAMS)}.json"), "w"), indent=2)
    obs = {r["family"]: float(r["chi2_max"])
           for r in csv.DictReader(open(os.path.join(RES, "obs_maxima.csv")))}
    print("\nfamily  n   min     med     p95     max   | obs      p-value  escalate?")
    for f in FAMS:
        v = sorted(x for x in maxima[f] if x is not None)
        med, p95 = v[len(v) // 2], v[int(0.95 * (len(v) - 1))]
        o = obs.get(f)
        p = (sum(1 for x in v if x >= o) + 1) / (len(v) + 1)
        esc = "YES->200 draws" if o >= med else "no"
        print(f"{f:6s} {len(v):3d} {v[0]:7.2f} {med:7.2f} {p95:7.2f} {v[-1]:7.2f} | "
              f"{o:7.2f}  {p:.4f}  {esc}")
    print(f"\ntotal {time.time()-t0:.0f}s on {mp.cpu_count()} cores", flush=True)


if __name__ == "__main__":
    _init()
    main()
