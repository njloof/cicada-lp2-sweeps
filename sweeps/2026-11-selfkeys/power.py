#!/usr/bin/env python3
"""Campaign #8 power probe — SELF-CONSISTENT plants (PREREG): naive planting
is impossible for self-keys because the scan derives the key from the
OBSERVED page; plants must solve A2 = E + key(A2).
  VT: sequential solve over [st, m) at offset o = st (fwd pads; o=0 implicit
      per-position — skipped, disclosed)
  CF: sequential solve over the whole page, hit at (cf:pre, o=0)
  LS: per-line 29-way fixed-point search, T=id (tag ls:i); lines with no
      fixed point stay unplanted and coverage is reported
Recovery = planted (tag, offset) is family max on the planted page AND
chi2 >= family null median."""
import argparse, os, re, sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import selfkeys as SK  # noqa: E402
from core.kernel import Q  # noqa: E402
from core.validate import (flat, translit, brute_interrupters, keyword_stream,
                           LATIN2IDX)  # noqa: E402

RES = os.path.join(HERE, "results")


def epool():
    from core.validate import R2I, phi_prime_stream
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
    ap.add_argument("--fams", default="LS,VT,CF")
    ap.add_argument("--plants", type=int, default=10)
    ap.add_argument("--seed", type=int, default=20261125)
    ap.add_argument("--med", default="")
    args = ap.parse_args()
    fams = args.fams.split(",")
    med = {}
    for part in filter(None, args.med.split(",")):
        k, v = part.split("=")
        med[k] = float(v)
    E = epool()
    rng = np.random.default_rng(args.seed)
    arrays0 = {n: np.array(flat(n), dtype=np.int16) for n in SK.TARGETS}
    os.makedirs(RES, exist_ok=True)
    for fam in fams:
        planted_rows = []
        for p in range(args.plants):
            n = int(rng.choice(SK.TARGETS))
            m = len(arrays0[n])
            A2 = arrays0[n].copy()
            if fam == "LS":
                lens = SK.line_lengths(n)
                edges = np.cumsum([0] + lens)
                e = np.tile(E, 2 + m // len(E))
                e = e[int(rng.integers(0, len(E))):][:m]
                planted_lines = 0
                for s, L in enumerate(lens):
                    kfix = None
                    for k in range(Q):  # 29-way fixed-point search (T=id)
                        cand = (e[edges[s]:edges[s + 1]] + k) % Q
                        if int(SK.PRIME[cand].sum()) % Q == k:
                            kfix = k
                            break
                    if kfix is not None:
                        A2[edges[s]:edges[s + 1]] = (e[edges[s]:edges[s + 1]] + kfix) % Q
                        planted_lines += 1
                plant = ("ls:i", 0)
                cov = planted_lines / len(lens)
            elif fam == "VT":
                f_map, f_tag = (SK.PHI_MAP, "vt:phi") if rng.integers(2) else (SK.DS_MAP, "vt:ds")
                o = int(rng.integers(1, 21))
                st = o  # window start == offset: maximal window == planted region
                wlen = m - st
                if wlen < 50:
                    continue
                e = np.tile(E, 2 + wlen // len(E))
                e = e[int(rng.integers(0, len(E))):][:wlen]
                for i in range(st, m):  # sequential self-consistent solve
                    A2[i] = (e[i - st] + f_map[A2[i - o]]) % Q
                plant = (f_tag, o)
                cov = 1.0
            else:  # CF
                wlen = m
                e = np.tile(E, 2 + wlen // len(E))
                e = e[int(rng.integers(0, len(E))):][:wlen]
                run = 0
                for i in range(m):  # A2[i] = E[i] + strict-past cumulative of A2
                    A2[i] = (e[i] + run) % Q
                    run = (run + int(A2[i])) % Q
                plant = ("cf:pre", 0)
                cov = 1.0
            arrs = {n: A2}
            best = SK.family_max([fam], [n], arrs)[fam]
            hit = (best[2], best[3]) == plant
            planted_rows.append((p, n, plant[0], plant[1], round(cov, 2),
                                 round(best[0], 2), best[2], best[3], hit))
        rec = sum(1 for r in planted_rows if r[-1])
        at = (sum(1 for r in planted_rows if r[-1] and r[5] >= med.get(fam, -1))
              if fam in med else None)
        with open(os.path.join(RES, f"power_{fam}.csv"), "w") as f:
            f.write("plant,target,tag,offset,coverage,fam_chi2,argmax_tag,argmax_off,hit\n")
            for r in planted_rows:
                f.write(",".join(str(x) for x in r) + "\n")
        msg = f"{fam}: argmax recovery {rec}/{len(planted_rows)}"
        if at is not None:
            msg += f"; recovered AND >= null median: {at}/{len(planted_rows)}"
        print(msg, flush=True)


if __name__ == "__main__":
    main()
