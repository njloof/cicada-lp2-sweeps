#!/usr/bin/env python3
"""Campaign #7 MC null: per-family null of the global max over in-page-shuffled
targets (identical scan path, house standard). Resumable checkpoints."""
import argparse, json, os, sys, time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
import numkeys as NK  # noqa: E402

RES = os.path.join(HERE, "results")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fams", default="Vp,Vs,R,D")
    ap.add_argument("--draws", type=int, default=20)
    ap.add_argument("--seed", type=int, default=20261122)
    ap.add_argument("--obs", default=None, help="override obs maxima, e.g. Vp=123.4,Vs=...")
    args = ap.parse_args()
    fams = args.fams.split(",")
    os.makedirs(RES, exist_ok=True)
    ckpt_path = os.path.join(RES, f"null_{'_'.join(fams)}_checkpoint.json")
    variants, targets = NK.variants_and_targets()
    arrays0 = {n: np.array(NK.flat(n), dtype=np.int16) for n in targets}
    done, maxima = 0, {f: [] for f in fams}
    if os.path.exists(ckpt_path):
        st = json.load(open(ckpt_path))
        if st.get("seed") == args.seed and st.get("fams") == fams:
            maxima, done = st["maxima"], st["done"]
            print(f"resuming at draw {done}", flush=True)
    rng = np.random.default_rng(args.seed)
    for _ in range(done):  # advance RNG to checkpoint position
        for n in targets:
            rng.permutation(arrays0[n])
    t0 = time.time()
    for d in range(done, args.draws):
        shuf = {n: rng.permutation(arrays0[n]).astype(np.int16) for n in targets}
        best = NK.family_max(fams, variants, targets, shuf)
        for f in fams:
            maxima[f].append(round(best[f][0], 4) if f in best else None)
        json.dump({"seed": args.seed, "fams": fams, "done": d + 1, "maxima": maxima},
                  open(ckpt_path, "w"))
        print(f"draw {d+1}/{args.draws} " +
              " ".join(f"{f}={maxima[f][-1]:.2f}" for f in fams) +
              f"  [{time.time()-t0:.0f}s]", flush=True)
    obs = {}
    if args.obs:
        for part in args.obs.split(","):
            k, v = part.split("=")
            obs[k] = float(v)
    else:
        import csv
        for r in csv.DictReader(open(os.path.join(RES, "obs_maxima.csv"))):
            obs[r["family"]] = float(r["chi2_max"])
    print("\nfamily  n   min     med     p95     max   | obs      p-value  escalate?")
    for f in fams:
        v = sorted(x for x in maxima[f] if x is not None)
        if not v:
            continue
        med = v[len(v) // 2]
        p95 = v[int(0.95 * (len(v) - 1))]
        o = obs.get(f)
        p = None if o is None else (sum(1 for x in v if x >= o) + 1) / (len(v) + 1)
        esc = "YES->200 draws" if o is not None and o >= med else "no"
        print(f"{f:6s} {len(v):3d} {v[0]:7.2f} {med:7.2f} {p95:7.2f} {v[-1]:7.2f} | "
              f"{o if o is not None else float('nan'):7.2f}  "
              f"{p if p is not None else float('nan'):.4f}  {esc}")
    json.dump({"seed": args.seed, "fams": fams, "done": args.draws, "maxima": maxima},
              open(os.path.join(RES, f"null_{'_'.join(fams)}.json"), "w"), indent=2)


if __name__ == "__main__":
    main()
