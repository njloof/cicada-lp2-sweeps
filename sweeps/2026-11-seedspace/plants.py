#!/usr/bin/env python3
"""Campaign #28 power plants (PREREG: registered FIRST output after commit).

Synthetic only — no corpus touched. Per lane, 20 plants:
  w* uniform in [0,2^32); P = #26-A1 quadgram sampler stream (bit-identical
  loader/sampler); S* = keyskip1 reject-loop encode of P under K(w*) with a
  random sign and (B/C) reduction; plant score = engine primary statistic of
  (w*, sign, red) against S*. House seeding default_rng([20261228, crc32
  ("plant")%100000, d]).

    python3 plants.py            # writes results/plants.json
"""
import json, os, subprocess, sys, zlib
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "sources/dukotah/liber-primus/analysis/round19/G3"))
sys.path.insert(0, os.path.join(ROOT, "sources/dukotah/liber-primus/analysis/round28/L4"))
from core import validate as V                                   # noqa: E402
import gen_py27, gen28                                           # noqa: E402

ENG = os.path.join(HERE, "seedspace_engine")
QUAD = os.path.join(ROOT, "sources/dukotah/liber-primus/data/english_quadgrams.txt")
SEED = 20261228
L = 120
NPLANT = 20

def rng_for(tag, d): return np.random.default_rng([SEED, zlib.crc32(tag.encode()) % 100000, d])

def load_quad(path):   # bit-identical to #26-A1 / #27
    ctx = {}
    for ln in open(path, encoding="utf-8"):
        q, c = ln.split()
        ctx.setdefault(q[:3], [[], []])
        ctx[q[:3]][0].append(q[3]); ctx[q[:3]][1].append(int(c))
    out = {}
    for k, (chs, ws) in ctx.items():
        cw = np.cumsum(ws); out[k] = (chs, cw / cw[-1])
    return out

def sampler(Q, rng, n):   # bit-identical to #26-A1
    AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    st = "THE"; out = []
    for _ in range(n):
        e = Q.get(st)
        ch = AZ[rng.integers(26)] if e is None else e[0][int(np.searchsorted(e[1], rng.random()))]
        out.append(V.LATIN2IDX[ch]); st = st[1:] + ch
    return out

def keystream(lane, w, red):
    if lane == "A":
        r = gen_py27.py27_seed(int(w))
        return gen_py27.ks_random29(r, 400)
    mode = "mt" if lane == "B" else "php"
    return gen28.php_stream(int(w), mode, red, 400)

def encode_keyskip1(P, K, sign, L):
    """keyskip1: on reject (c == prev) the KEY advances, plaintext held."""
    out, prev, pi, ki = [], -1, 0, 0
    while len(out) < L:
        p, k = P[pi], K[ki]
        c = (p + sign * k) % 29
        while c == prev:
            ki += 1
            c = (p + sign * K[ki]) % 29
        out.append(c); prev = c; pi += 1; ki += 1
    return bytes(out)

def main():
    Q = load_quad(QUAD)
    res = {"seed": SEED, "plants": {}}
    for lane in "ABC":
        rows = []
        for d in range(NPLANT):
            rng = rng_for("plant", d)
            w = int(rng.integers(2**32))
            sign = 1 if rng.random() < 0.5 else -1
            red = "none" if lane == "A" else ("scale" if d % 2 == 0 else "mod")
            P = sampler(Q, rng_for("plantP" + lane, d), 400)
            K = keystream(lane, w, "none" if lane == "A" else red)
            S = encode_keyskip1(P, K, sign, L)
            pf = os.path.join(HERE, "results", f"plant_{lane}_{d}.bin")
            os.makedirs(os.path.dirname(pf), exist_ok=True)
            open(pf, "wb").write(S)
            sc = subprocess.run([ENG, "--score", lane, str(w), str(sign), red, QUAD, pf],
                                capture_output=True, text=True)
            rows.append({"d": d, "seed": w, "sign": sign, "red": red,
                         "score": float(sc.stdout.strip())})
            print(f"plant {lane}/{d}: seed={w} sign={sign:+d} red={red} score={rows[-1]['score']:.2f}")
        res["plants"][lane] = rows
    os.makedirs(os.path.join(HERE, "results"), exist_ok=True)
    json.dump(res, open(os.path.join(HERE, "results", "plants.json"), "w"), indent=1)
    for lane in "ABC":
        ss = [r["score"] for r in res["plants"][lane]]
        print(f"lane {lane}: min={min(ss):.2f} median={float(np.median(ss)):.2f} max={max(ss):.2f}")

if __name__ == "__main__":
    main()
