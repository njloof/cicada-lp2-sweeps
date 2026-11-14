#!/usr/bin/env python3
"""Write data/solved_plaintexts.json — LP2 solved pages as rune-index plaintext streams
(used as extra pad candidates: the pad = P_N variant of the hypothesis).

AN END  (56): phi(prime) shift-down decode with null-F search (validate machinery).
PARABLE (57): direct transliteration => plaintext == ciphertext indices.
Run: python3 -m core.plaintexts   (from repo root)
"""
import json, os, numpy as np
from core import ROOT
import core.validate as V

def an_end_plain():
    ct = V.flat(56)
    res = V.brute_interrupters(ct, V.phi_prime_stream(len(ct)),
                               ["DEEPWEB", "PILGRIM", "HASHESTO"])
    assert res and res[1] == 3, f"AN END decode failed: {res}"
    # recover indices by re-decoding with the winning convention/null-set:
    # brute_interrupters returns text only, so redo the winning assignment explicitly
    from itertools import product
    fpos = [t for t, c in enumerate(ct) if c == 0]
    stream = V.phi_prime_stream(len(ct))
    conv_fn = {"skip": V.decode_skipnull, "hold": V.decode_holdnull}[res[2]]
    import itertools
    for r in range(len(fpos) + 1):
        for combo in itertools.combinations(fpos, r):
            cs = set(combo)
            idx = conv_fn(ct, stream, [t in cs for t in range(len(ct))])
            if V.translit(idx) == res[0]:
                return idx
    raise AssertionError("could not reproduce winning decode indices")

def parable_plain():
    return V.flat(57)

def main():
    out = {"ANEND56": an_end_plain(), "PARABLE57": parable_plain()}
    for k, v in out.items():
        assert all(0 <= i < 29 for i in v) and len(v) > 50
    json.dump(out, open(f"{ROOT}/data/solved_plaintexts.json", "w"))
    print("wrote data/solved_plaintexts.json:",
          {k: len(v) for k, v in out.items()})

if __name__ == "__main__":
    main()
