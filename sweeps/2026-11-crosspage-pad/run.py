#!/usr/bin/env python3
"""Campaign 2026-11-crosspage-pad — Phase 1/1b sweep CLI (see PREREG.md, config.yaml).

Run from repo root:  python3 sweeps/2026-11-crosspage-pad/run.py [--mirror] [--mask tgt|both]
Outputs results/sweep_phase1*.csv in this campaign dir.
"""
import argparse, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, ROOT)
import numpy as np
from core import DATA
from core import kernel

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mirror", action="store_true", help="include palindrome mirror pads")
    ap.add_argument("--mask", default="tgt", choices=["tgt", "both"])
    ap.add_argument("--floor", type=float, default=40.0)
    ap.add_argument("--out", default=f"{HERE}/results/sweep_phase1.csv")
    a = ap.parse_args()

    pages = kernel.load_pages()
    targets = [n for n in pages if n <= 54]                 # unsolved only
    pads = list(pages)                                      # 0-54 + AN END + PARABLE ciphertext
    extra = []
    sp = f"{DATA}/solved_plaintexts.json"
    if os.path.exists(sp):
        for k, v in json.load(open(sp)).items():
            extra.append((k, np.array(v, dtype=np.int8)))
    else:
        print("note: no data/solved_plaintexts.json — skipping plaintext pads "
              "(run: python3 -m core.plaintexts)", file=sys.stderr)

    rows, pairmax = kernel.run_sweep(pages, targets, pads, mask=a.mask,
                                     mirror=a.mirror, floor=a.floor)
    # solved-page plaintext pads (fwd/rev), scanned against every unsolved target
    for pname, pstream in extra:
        for orient, B in kernel.orientations(pstream):
            for M in targets:
                for off, nn, chi2, ioc, h in kernel.pair_scan(pages[M], B, mask=a.mask):
                    if chi2 >= a.floor:
                        top = int(np.argmax(h))
                        rows.append(dict(target=M, pad=pname, orient=orient, offset=off,
                                         n_valid=nn, chi2=round(chi2, 2), ioc=round(ioc, 5),
                                         top_rune=top, top_frac=round(float(h[top]) / nn, 4)))
    os.makedirs(os.path.dirname(a.out), exist_ok=True)
    rows.sort(key=lambda r: -r["chi2"])
    with open(a.out, "w") as f:
        f.write("target,pad,orient,offset,n_valid,chi2,ioc,top_rune,top_frac\n")
        for r in rows:
            f.write(f"{r['target']},{r['pad']},{r['orient']},{r['offset']},{r['n_valid']},"
                    f"{r['chi2']},{r['ioc']},{r['top_rune']},{r['top_frac']}\n")
    print(f"wrote {a.out}: {len(rows)} rows")

if __name__ == "__main__":
    main()
