#!/usr/bin/env python3
"""Campaign #8 MC null — DERIVE-FROM-SHUFFLED (registered design): per draw,
targets are permuted and ALL self-key derivations are recomputed on the
shuffled targets (iter_rows derives pads from the arrays it receives, so
passing shuffled arrays IS the null). Draw contents bit-identical to the
sequential default_rng(seed) stream; only scans fan out (studio.local via
scripts/studio.sh, or local). Same file shapes as calibrate-style runs."""
import argparse, csv, json, multiprocessing as mp, os, sys, time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import selfkeys as SK  # noqa: E402

RES = os.path.join(HERE, "results")
_ap = argparse.ArgumentParser()
_ap.add_argument("--fams", default="LS,VT,CF")
_ap.add_argument("--draws", type=int, default=20)
_ap.add_argument("--seed", type=int, default=20261124)
_args = _ap.parse_args()
FAMS = _args.fams.split(",")
SEED = _args.seed
DRAWS = _args.draws

_ARRAYS0 = None


def _init():
    global _ARRAYS0
    _ARRAYS0 = {n: np.array(SK.flat(n), dtype=np.int16) for n in SK.TARGETS}


def _one_draw(shuf):
    return SK.family_max(FAMS, SK.TARGETS, shuf)


def main():
    t0 = time.time()
    arrays0 = {n: np.array(SK.flat(n), dtype=np.int16) for n in SK.TARGETS}
    rng = np.random.default_rng(SEED)
    draws = []
    for _ in range(DRAWS):  # exact sequential RNG stream (per draw, ascending targets)
        draws.append({n: rng.permutation(arrays0[n]).astype(np.int16) for n in SK.TARGETS})
    print(f"shuffled corpora generated in {time.time()-t0:.1f}s", flush=True)
    with mp.Pool(min(DRAWS, mp.cpu_count()), initializer=_init) as pool:
        results = pool.map(_one_draw, draws)
    maxima = {f: [round(r[f][0], 4) if f in r else None for r in results] for f in FAMS}
    os.makedirs(RES, exist_ok=True)
    tag = "_".join(FAMS)
    json.dump({"seed": SEED, "fams": FAMS, "done": DRAWS, "maxima": maxima},
              open(os.path.join(RES, f"null_{tag}_checkpoint.json"), "w"))
    json.dump({"seed": SEED, "fams": FAMS, "done": DRAWS, "maxima": maxima},
              open(os.path.join(RES, f"null_{tag}.json"), "w"), indent=2)
    obs = {r["family"]: float(r["chi2_max"])
           for r in csv.DictReader(open(os.path.join(RES, "obs_maxima.csv")))}
    print("\nfamily  n   min     med     p95     max   | obs      p-value  escalate?")
    for f in FAMS:
        v = sorted(x for x in maxima[f] if x is not None)
        med, p95 = v[len(v) // 2], v[int(0.95 * (len(v) - 1))]
        o = obs.get(f)
        p = (sum(1 for x in v if x >= o) + 1) / (len(v) + 1)
        esc = "YES->200 draws" if o is not None and o >= med else "no"
        print(f"{f:6s} {len(v):3d} {v[0]:7.2f} {med:7.2f} {p95:7.2f} {v[-1]:7.2f} | "
              f"{o if o is not None else float('nan'):7.2f}  {p:.4f}  {esc}")
    print(f"\ntotal {time.time()-t0:.0f}s on {mp.cpu_count()} cores", flush=True)


if __name__ == "__main__":
    _init()
    main()
