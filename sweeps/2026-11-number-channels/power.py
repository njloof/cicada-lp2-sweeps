#!/usr/bin/env python3
"""Campaign #7 power probe (registered in PREREG): plant English-strength
plaintext behind one key of each family at a random phase; report recovery at
the family null median. D family is unprobeable (single length>=2 digit
stream, page 37 only) — disclosed in REPORT."""
import argparse, csv, os, sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
import numkeys as NK  # noqa: E402
from core.validate import (flat, translit, brute_interrupters, keyword_stream,
                           phi_prime_stream, LATIN2IDX, N as Q)  # noqa: E402

RES = os.path.join(HERE, "results")


def epool():
    sc = __import__("re").split  # noqa: F841  (keep import surface minimal)
    from core.validate import R2I
    import re
    md = open(os.path.join(HERE, "..", "..", "sources", "scream314", "liber_primus.md"),
              encoding="utf-8").read()
    def sr(label):
        sec = [s for s in re.split(r"^## ", md, flags=re.M) if s.startswith(label)][0]
        return [R2I[c] for c in sec.split("---")[0] if c in R2I]
    texts = []
    texts.append(brute_interrupters(flat(56), phi_prime_stream(len(flat(56))),
                                    ["DEEPWEB", "PILGRIM", "HASHESTO"])[0])
    texts.append(translit(flat(57)))
    texts.append(translit([(Q - 1 - c) % Q for c in sr("Runes - 01.jpg")]))
    we = sr("03.jpg")
    texts.append(brute_interrupters(we, keyword_stream("DIVINITY", len(we)),
                                    ["WELCOME", "PILGRIM", "JOURNEY"])[0])
    idx = []
    for t in texts:
        idx += [LATIN2IDX[c] for c in t if c in LATIN2IDX and LATIN2IDX[c] != 0]
    return np.array(idx, dtype=np.int16)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fams", default="Vp,Vs,R")
    ap.add_argument("--plants", type=int, default=10)
    ap.add_argument("--seed", type=int, default=20261123)
    ap.add_argument("--med", default="", help="family=median,...")
    args = ap.parse_args()
    fams = [f for f in args.fams.split(",") if f != "D"]
    med = dict()
    for part in filter(None, args.med.split(",")):
        k, v = part.split("=")
        med[k] = float(v)
    variants, targets = NK.variants_and_targets()
    arrays0 = {n: np.array(flat(n), dtype=np.int16) for n in targets}
    E = epool()
    rng = np.random.default_rng(args.seed)
    rows = []
    for fam in fams:
        planted_rows = []
        for p in range(args.plants):
            arrs = {n: arrays0[n].copy() for n in targets}
            n = int(rng.choice(targets))
            m = len(arrs[n])
            st = int(rng.integers(0, max(1, m - 60)))
            wlen = m - st
            if wlen < 50:
                continue
            e = np.tile(E, 2 + wlen // len(E))
            e = e[int(rng.integers(0, len(E))):][:wlen]
            if fam == "Vp":
                kid, key = variants[int(rng.integers(len(variants)))]
                ka = np.array(key, dtype=np.int16)
                o = int(rng.integers(len(ka)))
                K = ka[(np.arange(m) - o) % len(ka)]
                arrs[n] = ((e + K) % Q).astype(np.int16)
                plant = (n, kid, o)
                c2p, _ = NK.chi2_page(arrs[n], K)
            elif fam == "Vs":
                kid, key = variants[int(rng.integers(len(variants)))]
                pad = NK.tiled(key, m)
                o = st
                arrs[n][st:m] = ((e + pad[0:wlen]) % Q).astype(np.int16)
                plant = (n, kid, o)
                A = arrs[n]
                vals = (A[st:m] - pad[0:wlen]) % Q
                vals = vals[A[st:m] != 0]
                h = np.bincount(vals, minlength=Q).astype(np.float64)
                c2p = (Q / len(vals)) * float((h * h).sum()) - len(vals)
            else:  # R
                c, b = int(rng.integers(1, Q)), int(rng.integers(0, Q))
                pad = NK.ramp_pad(c, b, m)
                o = st
                arrs[n][st:m] = ((e + pad[0:wlen]) % Q).astype(np.int16)
                plant = (n, f"r{c}.{b}", o)
                A = arrs[n]
                vals = (A[st:m] - pad[0:wlen]) % Q
                vals = vals[A[st:m] != 0]
                h = np.bincount(vals, minlength=Q).astype(np.float64)
                c2p = (Q / len(vals)) * float((h * h).sum()) - len(vals)
            best = NK.family_max([fam], variants, targets, arrs)[fam]
            hit = (best[1], best[2], best[3]) == plant
            planted_rows.append((p, n, plant[1], plant[2], round(c2p, 2),
                                 round(best[0], 2), best[1], best[2], best[3], hit))
        rec = sum(1 for r in planted_rows if r[-1])
        at = (sum(1 for r in planted_rows if r[-1] and r[4] >= med.get(fam, -1))
              if fam in med else None)
        os.makedirs(RES, exist_ok=True)
        with open(os.path.join(RES, f"power_{fam}.csv"), "w") as f:
            f.write("plant,target,key,offset,planted_chi2,family_max,max_target,max_key,max_offset,argmax_hit\n")
            for r in planted_rows:
                f.write(",".join(str(x) for x in r) + "\n")
        msg = f"{fam}: argmax recovery {rec}/{len(planted_rows)}"
        if at is not None:
            msg += f"; recovered AND >= null median: {at}/{len(planted_rows)}"
        print(msg, flush=True)
        rows.append((fam, rec, len(planted_rows)))


if __name__ == "__main__":
    main()
