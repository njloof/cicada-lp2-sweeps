#!/usr/bin/env python3
"""GO prong 3: decode every leader window (fwd AND reversed) vs the versioned
crib list (core/cribs.py). Writes results/leaders_decode.csv. House pattern
from #7/#8 (which reported 0/80, 0/60 hits)."""
import csv
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..")))
import orient as OR                      # noqa: E402
from core.cribs import crib_hits, decode_window, REPR   # noqa: E402
from run import resolve                  # noqa: E402

RES = os.path.join(HERE, "results")


def main():
    grids = OR.load_grids()
    rows = list(csv.DictReader(open(f"{RES}/leaders_both.csv")))
    out, hits_total = [], 0
    for r in rows:
        fam, key, off = r["family"], r["key"], int(r["offset"])
        A, B, op = resolve(fam, key, grids)
        if A is None:
            print("UNRESOLVED", fam, key)
            sys.exit(1)
        fwd, rev = decode_window(A, B, op, off, mask="tgt")
        hf, hr = crib_hits(fwd), crib_hits(rev)
        hits_total += len(hf) + len(hr)
        out.append((fam, key, off, len(fwd), ";".join(hf), ";".join(hr),
                    fwd[:60], rev[:60]))
    with open(f"{RES}/leaders_decode.csv", "w") as f:
        f.write("family,key,offset,len,hits_fwd,hits_rev,fwd_head,rev_head\n")
        for t in out:
            f.write(",".join(str(x) for x in t) + "\n")
    print(f"{len(rows)} leaders x fwd+rev vs {len(REPR)} representable "
          f"cribs: {hits_total} hits")
    for t in out:
        if t[4] or t[5]:
            print("  HIT", t[:6])


if __name__ == "__main__":
    main()
