#!/usr/bin/env python3
"""Campaign #28 verdict: merge worker states, compute null_max, apply the
registered gate and verdict rules (PREREG f1ab025 + addendum), adjudicate
top candidates with the house crib list.

    python3 verdict.py                 # merge + verdict (no adjudication)
    python3 verdict.py --adjudicate N  # also full-decode top N per lane, crib hits
"""
import json, os, subprocess, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, ROOT)
from core.cribs import CRIBS, crib_hits                                  # noqa: E402

ENG = os.path.join(HERE, "seedspace_engine")
QUAD = os.path.join(ROOT, "sources/dukotah/liber-primus/data/english_quadgrams.txt")
RES = os.path.join(HERE, "results")
SPACE = 2**32
NWORK_DEFAULT = 28
MARGIN = 2.0
REDNAME = {0: "scale", 1: "mod"}

def merge_lane(lane, nwork):
    hist = np.zeros(1400, dtype=np.uint64)
    cands = []
    done = 0
    for i in range(nwork):
        p = os.path.join(RES, f"w_{lane}_{i}", f"state_{lane}.txt")
        if not os.path.exists(p):
            continue
        sec, cur = 0, None
        with open(p) as f:
            for line in f:
                if line.startswith("CURSOR "):
                    cur = int(line.split()[1]); continue
                if line.startswith("HIST"): sec = 1; continue
                if line.startswith("TOP"): sec = 2; continue
                if sec == 1:
                    b, n = line.split(); hist[int(b)] += int(n)
                elif sec == 2:
                    s, sd, sg, rd = line.split()
                    cands.append((float(s), int(sd), int(sg), int(rd)))
        if cur is not None:
            lo, hi = i * (SPACE // nwork), ((i + 1) * (SPACE // nwork) if i < nwork - 1 else SPACE)
            if cur >= hi: done += hi - lo
    cands.sort(reverse=True)
    return hist, cands, done

def main():
    nwork = int(os.environ.get("NWORK", NWORK_DEFAULT))
    plants = json.load(open(os.path.join(RES, "plants.json")))["plants"]
    out = {"margin_gate": MARGIN, "lanes": {}}
    any_flag = False
    for lane in "ABC":
        hist, cands, done = merge_lane(lane, nwork)
        ps = [r["score"] for r in plants[lane]]
        pmin = min(ps)
        null_max = cands[0][0] if cands else None
        B = pmin - MARGIN
        flagged = [c for c in cands if c[0] >= B]
        frac = done / SPACE
        gate = (null_max is not None) and (pmin - null_max >= MARGIN) and (
            sum(1 for s in ps if s >= null_max + MARGIN) == len(ps))
        if flagged: verdict = "FLAGGED"
        elif frac < 1.0: verdict = f"IN PROGRESS ({frac*100:.1f}% swept)"
        elif gate: verdict = "CLOSED-NO-KEY"
        else: verdict = "UNPOWERED-NULL"
        any_flag |= verdict == "FLAGGED"
        out["lanes"][lane] = {
            "swept_frac": frac, "null_max": null_max,
            "null_max_seed": cands[0][1] if cands else None,
            "plant_min": pmin, "plant_scores": ps, "flag_bar_B": B,
            "gate_margin_pass": gate, "n_flagged": len(flagged),
            "VERDICT": verdict,
            "top10": [{"score": s, "seed": sd, "sign": sg, "red": rd}
                      for s, sd, sg, rd in cands[:10]],
        }
        print(f"lane {lane}: swept {frac*100:.2f}% null_max={null_max} "
              f"plant_min={pmin:.2f} B={B:.2f} gate={'PASS' if gate else 'FAIL'} "
              f"-> {verdict}")
        np.savetxt(os.path.join(RES, f"hist_{lane}.txt"),
                   np.c_[np.arange(1400) * 0.5 - 500.0, hist], fmt="%.1f\t%d")
        with open(os.path.join(RES, f"top_{lane}.tsv"), "w") as f:
            for s, sd, sg, rd in cands[:1024]:
                f.write(f"{s:.4f}\t{sd}\t{sg}\t{rd}\n")

    if "--adjudicate" in sys.argv:
        N = int(sys.argv[sys.argv.index("--adjudicate") + 1])
        for lane in "ABC":
            adj = []
            for row in out["lanes"][lane]["top10"][:N]:
                red = "none" if lane == "A" else REDNAME[row["red"]]
                r = subprocess.run([ENG, "--decode", lane, str(row["seed"]),
                                    str(row["sign"]), red, QUAD,
                                    os.path.join(HERE, "corpus.bin")],
                                   capture_output=True, text=True)
                txt = r.stdout.strip()
                hits = crib_hits(txt)
                adj.append({**row, "red": red, "cribs": hits,
                            "head": txt[:120]})
                print(f"  {lane} seed={row['seed']} score={row['score']:.2f} "
                      f"cribs={hits} head={txt[:60]}")
            out["lanes"][lane]["adjudicated"] = adj

    out["CAMPAIGN_VERDICT"] = ("FLAGGED (see lanes)" if any_flag else
                               "all lanes CLOSED-NO-KEY" if all(
                                   v["VERDICT"] == "CLOSED-NO-KEY"
                                   for v in out["lanes"].values()) else
                               "see per-lane verdicts")
    json.dump(out, open(os.path.join(RES, "verdict.json"), "w"), indent=1)
    print("CAMPAIGN:", out["CAMPAIGN_VERDICT"])

if __name__ == "__main__":
    main()
