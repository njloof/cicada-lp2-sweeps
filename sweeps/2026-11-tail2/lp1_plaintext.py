#!/usr/bin/env python3
"""Campaign #25 Lane E — LP1 pages under the corrected premise
(plaintext confirmation; PREREG sweeps/2026-11-tail2/PREREG.md committed
86f6755 BEFORE output; tested-family correction appended at
implementation, pre-output).

Tested statistic: Caesar + atbash-Caesar (a in {1,28}, s in 0..28) x
fwd/rev, merged quadgram log-prob per letter, best per page; full affine
observed and REPORTED (not tested). Null: rune-shuffle surrogates,
S=1,000/draw, D=200, seed 20261228, per-replicate substreams, family-
matched; Holm across 9 pages. A surviving page = LP1-PAGE-PLAINTEXT flag
for the owner (new ground truth, never auto-certified).

Run (studio):  python3 sweeps/2026-11-tail2/lp1_plaintext.py
"""
import argparse
import json
import multiprocessing as mp
import os
import random
import re
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, ROOT)
import numpy as np                      # noqa: E402
import core.validate as V               # noqa: E402
from core.cribs import REPR as CRIBS    # noqa: E402

OUT = os.path.join(HERE, "results")
WORK = os.path.join(ROOT, "work", "tail2_e")
MERGE = str.maketrans("KVZQ", "CUSS")
R2I = {g[0]: i for i, g in enumerate(V.GEMATRIA)}
VAL = [g[1] for g in V.GEMATRIA]
SEED = 20261228
S_SHUF, D = 1000, 200
# log10 quadgram prob per window; calibrated from controls (smoke):
# true PTs ~ -4.3..-4.6, ciphertext/shuffles ~ -6.3..-7.7 -> bar midpoint
ENGLISH_BAR = -5.2
Q = 29
# dense quadgram table over 26 letters
QG = os.path.join(ROOT, "sources", "dukotah", "liber-primus", "data",
                  "english_quadgrams.txt")
_tab = np.full(26 ** 4, -3.0, dtype=np.float32)   # floor ~ log10(0.01/N)
_tot = 0
for _ln in open(QG):
    _w, _c = _ln.split()
    if re.fullmatch(r"[A-Z]{4}", _w):
        _k = 0
        for _ch in _w:
            _k = _k * 26 + (ord(_ch) - 65)
        _tab[_k] = float(_c)
        _tot += int(_c)
_tab = np.log10(np.maximum(_tab, 0.01)) - np.log10(_tot)
_tab[~np.isfinite(_tab)] = np.log10(0.01 / _tot)

VAL1 = np.array([ord(g[0]) for g in [v for v in VAL]], dtype=np.uint8)
VAL2 = np.array([(ord(v[1]) if len(v) > 1 else 0) for v in VAL],
                dtype=np.uint8)
MERGE26 = np.arange(26, dtype=np.uint8)
for _a, _b in (("K", "C"), ("V", "U"), ("Z", "S"), ("Q", "S")):
    MERGE26[ord(_a) - 65] = ord(_b) - 65


def decode_scores(X):
    """X: (m, n) rune indices -> merged quadgram log-prob per letter
    (m,) — fully vectorized incl. digraph expansion + merge fold."""
    m, n = X.shape
    l1 = VAL1[X]                                   # (m, n)
    l2 = VAL2[X]
    ex = l2 > 0                                    # digraph second letter
    # NB: affine shifts do NOT preserve the digraph-index set -> the
    # letter count varies per row; pad to Tmax and mask.
    Ts = n + ex.sum(axis=1)                        # (m,)
    Tmax = int(Ts.max())
    p1 = np.arange(n)[None, :] + np.cumsum(ex, axis=1) - ex
    arr = np.full((m, Tmax), 65, dtype=np.uint8)   # pad 'A' (masked out)
    off = (np.arange(m) * Tmax)[:, None]
    arr.reshape(-1)[(off + p1).reshape(-1)] = l1.reshape(-1)
    sel = (off + p1 + 1)[ex]
    arr.reshape(-1)[sel] = l2[ex]
    a = MERGE26[arr.astype(np.int16) - 65]
    k = (((a[:, 0:Tmax - 3].astype(np.int64) * 26 + a[:, 1:Tmax - 2]) * 26
          + a[:, 2:Tmax - 1]) * 26 + a[:, 3:Tmax])
    ok = (np.arange(Tmax - 3)[None, :] < (Ts - 3)[:, None])
    vals = _tab[k]
    vals[~ok] = 0.0
    return vals.sum(axis=1) / (Ts - 3)


def family_X(ct, a_list):
    """(a,s) x fwd/rev decode index matrix."""
    rows = []
    for c in (ct, ct[::-1]):
        for a in a_list:
            for s in range(Q):
                rows.append((a * c + s) % Q)
    return np.array(rows, dtype=np.int64)


PAGES = {}
G = {}


def null_draw(d):
    rng = random.Random(f"{SEED}:{d}")
    dm = {}
    for k, ct in PAGES.items():
        n = len(ct)
        gm = -9.9
        for _ in range(S_SHUF):
            perm = list(range(n))
            rng.shuffle(perm)
            gm = max(gm, float(decode_scores(
                family_X(ct[perm], G["TESTED_A"])).max()))
        dm[k] = round(gm, 5)
    return d, dm


def lp1_pages():
    txt = open(os.path.join(ROOT, "sources", "scream314",
                            "liber_primus.md")).read()
    lp1 = txt[txt.index("# LP1"):txt.index("# LP2")]
    pages, cur = {}, None
    for line in lp1.splitlines():
        m = re.match(r"## (.+)", line)
        if m:
            cur = m.group(1)
            pages[cur] = []
        elif cur is not None:
            pages[cur].extend(c for c in line
                              if 0x16A0 <= ord(c) <= 0x16FF)
    return {k: [R2I[c] for c in v if c in R2I]
            for k, v in pages.items() if len(v) >= 60}


def merged_txt(Xrow):
    return "".join(VAL[x] for x in Xrow.tolist()).upper().translate(MERGE)


def main():
    try:
        mp.set_start_method("fork")
    except RuntimeError:
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--budget", type=int, default=480)
    a = ap.parse_args()
    t0 = time.time()
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(WORK, exist_ok=True)
    rep = []
    pages = lp1_pages()
    assert len(pages) == 9, f"target count {len(pages)}"
    rep.append(f"Targets (9 LP1 pages >=60 runes, scream314 lineage): "
               + ", ".join(f"{k[:12]}:{len(v)}" for k, v in pages.items()))

    # controls: TRUE plaintexts (solved_plaintexts — p56 flat is CT!)
    sp = json.load(open(f"{V.DATA}/solved_plaintexts.json"))
    ctrl = []
    for name in ("ANEND56", "PARABLE57"):
        pt = np.array(sp[name], dtype=np.int64)
        sc = decode_scores(family_X(pt, [1]))[0]   # identity
        ctrl.append(f"  control {name} PT identity: {sc:.3f}")
    ctrl.append(f"  control p56-CT identity (must be LOW): "
                f"{decode_scores(family_X(np.array(V.flat(56), dtype=np.int64), [1]))[0]:.3f}")
    rep.append("Controls (English bar %.1f, calibrated from PT controls):"
               "\n%s" % (ENGLISH_BAR, "\n".join(ctrl)))
    TESTED_A = [1, 28]
    # plant: true PT under Caesar s=13, run THROUGH the tested family
    # (registered power probe; scoring the shifted text at identity is
    # meaningless — quadgrams match English orthography, corrected
    # post-output, PREREG correction 2)
    pt56 = np.array(sp["ANEND56"], dtype=np.int64)
    pX = family_X((pt56 + 13) % Q, TESTED_A)
    psc = decode_scores(pX)
    pbi = int(np.argmax(psc))
    pn = len(TESTED_A) * Q * 2
    pcell = (TESTED_A[(pbi // Q) % 2], pbi % Q,
             "fwd" if pbi < pn // 2 else "rev")
    rep.append(f"Plant ANEND56-PT Caesar s=13 through family: "
               f"{psc.max():.3f} at a={pcell[0]} s={pcell[1]} {pcell[2]} "
               f"({'PASS' if psc.max() >= ENGLISH_BAR else 'FAIL'}"
               f"{', cell recovered' if pcell == (1, 16, 'fwd') else ''})")
    AFFINE_A = list(range(1, Q))
    obs = {}
    for k, ct in pages.items():
        ct = np.array(ct, dtype=np.int64)
        st = decode_scores(family_X(ct, TESTED_A))
        sa = decode_scores(family_X(ct, AFFINE_A))
        bi = int(np.argmax(st))
        ba = int(np.argmax(sa))
        nrow = len(TESTED_A) * Q * 2
        obs[k] = dict(tested=float(st.max()),
                      tested_a=TESTED_A[(bi // Q) % 2],
                      tested_s=bi % Q,
                      tested_dir=("fwd" if bi < nrow // 2 else "rev"),
                      affine=float(sa.max()),
                      affine_a=AFFINE_A[(ba // Q) % 28],
                      affine_s=ba % Q,
                      ident=float(decode_scores(family_X(ct, [1]))[0]),
                      txt=merged_txt(family_X(ct, TESTED_A)[bi]))
        rep.append(f"  {k[:14]}: tested best {obs[k]['tested']:.3f} "
                   f"(a={obs[k]['tested_a']} s={obs[k]['tested_s']} "
                   f"{obs[k]['tested_dir']}), full-affine "
                   f"{obs[k]['affine']:.3f}, identity {obs[k]['ident']:.3f}")

    # null: per replicate, per page, S shuffles, family-matched max
    # (parallel over draws; per-draw substreams keep the stream
    # bit-identical under any chunking)
    NULLF = os.path.join(WORK, "null_maxes.json")
    nulls = json.load(open(NULLF)) if os.path.exists(NULLF) else {}
    PAGES.clear()
    PAGES.update({k: np.array(v, dtype=np.int64) for k, v in pages.items()})
    G["TESTED_A"] = TESTED_A
    todo = [d for d in range(D) if str(d) not in nulls]
    if todo:
        with mp.Pool() as pool:
            for d, dm in pool.imap_unordered(null_draw, todo):
                nulls[str(d)] = dm
                json.dump(nulls, open(NULLF, "w"))
                if (len(nulls)) % 20 == 0:
                    print(f"  null {len(nulls)}/{D} "
                          f"({time.time()-t0:.0f}s)", flush=True)
                if time.time() - t0 > a.budget:
                    pool.terminate()
                    print(f"PARTIAL (null {len(nulls)}/{D}) — rerun",
                          flush=True)
                    return

    # per-page p + Holm
    raw_p = {}
    for k in pages:
        o = obs[k]["tested"]
        beats = sum(1 for dm in nulls.values() if dm[k] >= o)
        raw_p[k] = (1 + beats) / (D + 1)
    order = sorted(raw_p, key=lambda k: raw_p[k])
    holm = {}
    run = 0.0
    for i, k in enumerate(order):
        # Holm adjusted p = max_{j<=i} (m-j+1)*p_j, capped at 1
        # (running MAX; the first implementation used min — corrected,
        # PREREG correction 2; rejection set unchanged)
        run = max(run, (len(order) - i) * raw_p[k])
        holm[k] = min(1.0, run)
    rep.append("Per-page p (obs vs family-matched shuffle null, D=200) / "
               "Holm / null-max margin (p=0.0050 is the floor 1/201, "
               "0/200 beats; margin shown per #24 p-floor lesson):")
    for k in order:
        nmax = max(dm[k] for dm in nulls.values())
        rep.append(f"  {k[:14]}: obs {obs[k]['tested']:.3f} "
                   f"p={raw_p[k]:.4f} holm={holm[k]:.4f} "
                   f"nullmax {nmax:.3f} "
                   f"{'ENGLISH-LEVEL' if obs[k]['tested'] >= ENGLISH_BAR and holm[k] < 0.05 else ''}")
    rep.append("Best tested-family decodes (first 160 letters, merged):")
    for k in order:
        rep.append(f"  {k[:14]} [{obs[k]['tested_a']}|{obs[k]['tested_s']}|"
                   f"{obs[k]['tested_dir']}]: {obs[k]['txt'][:160]}")
    sig = [k for k in order if holm[k] < 0.05
           and obs[k]["tested"] >= ENGLISH_BAR]
    verdict = ("LP1-PAGE-PLAINTEXT — FLAG FOR OWNER: " + ", ".join(sig)
               + " score English-level under a Caesar/atbash layer "
               "(new ground truth in the scream314 lineage; never "
               "auto-certified)" if sig else
               "LP1-SIMPLE-NULL — identity/Caesar/atbash/reverse retired "
               "for the 9 LP1 rune pages (scream314 lineage); phi-prime "
               "already retired by #24 Lane C; premise 'largely readable "
               "English' NOT mechanically confirmed for these pages")
    rep.append(f"VERDICT: {verdict}")
    rep.append("DISCLOSURES: (1) tested family = a in {1,28} x s x "
               "fwd/rev (corrected pre-output from full affine, priced "
               "null cost); full affine reported untested. (2) rune-"
               "shuffle null preserves rune multiset; digraph letter "
               "adjacency is broken by the shuffle (conservative). "
               "(3) scream314 lineage only (9.2% agreement with dukotah "
               "stream). (4) quadgram floor log10(0.01/N). "
               f"(5) runtime {time.time()-t0:.0f} s.")
    with open(f"{OUT}/LANE_E_REPORT.md", "w") as f:
        f.write("# Campaign #25 Lane E (LP1 plaintext confirmation) report\n\n"
                + "\n\n".join(rep) + "\n")
    print("\n".join(rep))


if __name__ == "__main__":
    main()
