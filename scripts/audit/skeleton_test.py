#!/usr/bin/env python3
"""Campaign #21 — separator-skeleton qualification (PREREG
sweeps/2026-11-skeleton, committed 2f8c015 BEFORE output).

V1: p56 dash <-> canonical word-boundary alignment via verified regions
(difflib, merged alphabet), analytic hypergeometric.
V2: merged-alphabet quadgram+crib scorer blind holdout on p56/p57 vs
1,000 letter-shuffles (seed 20261221).
V3: report-only per-unit skeleton panel.

Usage: python3 -I scripts/audit/skeleton_test.py   (runtime: seconds)
"""
import difflib
import itertools
import math
import os
import random
import re
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
sys.path.insert(0, ROOT)
import core.validate as V  # noqa: E402
from core.cribs import REPR as CRIBS  # noqa: E402

OUT = os.path.join(ROOT, "sweeps", "2026-11-skeleton", "results")
MD = os.path.join(ROOT, "docs", "ORACLE_PAGES.md")
KDIR = os.path.join(ROOT, "sources", "dukotah", "liber-primus", "data")
MERGE = str.maketrans("KVZQ", "CUSS")
SEED = 20261221
BOOK = list(range(50)) + list(range(51, 58))


def blocks_of_md():
    txt = open(MD).read()
    out = {}
    for m in re.finditer(r"## p(\d+).*?\*\*Ciphertext\*\*[^\n]*\n+"
                         r"```[a-zA-Z]*\n(.*?)```", txt, re.S):
        out[int(m.group(1))] = m.group(2)
    return out


def rune_seg(line):
    m = re.match(r"\s*\d+\s+(.*)", line)
    if not m:
        return None
    s = re.split(r"\s{2,}=\s", m.group(1))[0].strip()
    return s


WORDS = {w.strip().lower() for w in
         open("/usr/share/dict/words") } if os.path.exists(
    "/usr/share/dict/words") else frozenset()


def _join_run(lines):
    """Rejoin a run of body lines of the signed file. The file wraps
    MID-WORD without hyphens (TH|ERE, HA|SHES, PILGR|IM) but also wraps
    at word boundaries (the|divinity). Deterministic rule: merge the
    wrap iff the merged fragment is an English word OR either fragment
    alone is not an English word (/usr/share/dict/words); else space."""
    out = lines[0]
    for nxt in lines[1:]:
        a = re.sub(r"[^A-Za-z]", "", out.split()[-1]).lower()
        b = re.sub(r"[^A-Za-z]", "", nxt.split()[0]).lower()
        if (a + b) in WORDS or a not in WORDS or b not in WORDS:
            out += nxt
        else:
            out += " " + nxt
    return out


def _runs(seg):
    """Body lines -> runs of visually-contiguous lines (hex hash lines
    and blanks are run separators and are dropped)."""
    runs, cur = [], []
    for l in seg.splitlines():
        t = l.strip()
        if not t or re.fullmatch(r"[0-9a-f]+", t):
            if cur:
                runs.append(_join_run(cur))
                cur = []
            continue
        cur.append(t)
    if cur:
        runs.append(_join_run(cur))
    return runs


def canon_words():
    """(words56, words57) from the PGP-signed file. First line of the
    p56 section is a heading ('AN END') -> word boundary; hash lines
    excluded; wraps repaired by _join_run."""
    raw = open(os.path.join(KDIR, "keys", "solved_plaintext.txt")).read()
    # anchor at the LAST "AN END" before the p56 koan body (earlier hits
    # are the LP1 WELCOME text "…FIND AN END TO ALL STRUGGLE…")
    i = raw.rfind("AN END", 0, raw.find("WITHIN THE DEEP WEB"))
    seg = raw[i:raw.find(" Parable", i)]
    lines = seg.splitlines()
    head = lines[0].strip()
    w56 = (head + " " + " ".join(_runs("\n".join(lines[1:])))).split()
    j = raw.find("Parable", i)
    seg = raw[j:raw.find("emerge.", j) + len("emerge.")]
    seg = " ".join(_runs(seg)).replace("Parable :", "PARABLE .") \
                             .replace(":", " . ")
    w57 = seg.split()
    return w56, w57


def build_canon(words):
    """letters (merged), word-start set, sentence-end letter-set."""
    letters, starts, sends = [], set(), set()
    for w in words:
        if w in (".", ","):
            if letters:
                sends.add(len(letters) - 1)
            continue
        trail = w.rstrip().endswith((".", ","))
        w = re.sub(r"[^A-Za-z]", "", w)
        if not w:
            continue
        starts.add(len(letters))
        letters.extend(list(w.upper().translate(MERGE)))
        if trail:
            sends.add(len(letters) - 1)
    return "".join(letters), starts, sends


VAL = [g[1] for g in V.GEMATRIA]  # positional romanization per rune index


def dash_positions(block, nulls=()):
    """boundaries in LETTER space (decode strings are romanized, and
    digraphs like TH/NG/EO are 1 rune = 2 letters): last letter index
    before each '-' (and each ◆N/§ mark). Null-F runes advance the rune
    counter but not the letter counter (skip convention)."""
    dashes, marks, r, L = [], [], 0, 0
    for raw in block.splitlines():
        s = rune_seg(raw)
        if s is None or s in ("&", "$", "§") or \
                not any(0x16A0 <= ord(c) <= 0x16FF for c in s):
            continue
        s = re.sub(r"[A-Za-z]+", "", s.replace("*", ""))
        i = 0
        while i < len(s):
            ch = s[i]
            if 0x16A0 <= ord(ch) <= 0x16FF:
                if r not in nulls:
                    L += len(VAL[V.R2I[ch]])
                r += 1
                i += 1
            elif ch == "-":
                dashes.append(L - 1)
                i += 1
            elif ch == "◆":
                m = re.match(r"◆(\d+)", s[i:])
                marks.append((m.group(1), L - 1))
                i += len(m.group(0))
            elif ch == "§":
                marks.append(("23", L - 1))
                i += 1
            else:
                i += 1
    return dashes, marks, L


def verified(d, c, minlen=4):
    sm = difflib.SequenceMatcher(None, d, c, autojunk=False)
    return [(a, b, s) for a, b, s in sm.get_matching_blocks()
            if s >= minlen]


def hyper_p(k, B, G, n):
    """P(X >= k), X ~ hypergeometric(G, B, n) — upper tail."""
    if n > G or B > G:
        return 1.0
    num = sum(math.comb(B, i) * math.comb(G - B, n - i)
              for i in range(max(k, n - (G - B)), min(n, B) + 1))
    return num / math.comb(G, n)


def main():
    os.makedirs(OUT, exist_ok=True)
    rep, fails = [], []
    blocks = blocks_of_md()
    assert sorted(blocks) == list(range(58))

    # ---------------- G1 ----------------
    stream = []
    for n in list(range(50)) + [51, 52, 53, 54, 55]:
        stream.extend(V.flat(n))
    N = len(stream)
    assert N == 12956, f"G1 FAIL N={N}"
    tc = Counter()
    for p in BOOK:
        for raw in blocks[p].splitlines():
            s = rune_seg(raw)
            if s is None or s in ("&", "$", "§") or \
                    not any(0x16A0 <= ord(c) <= 0x16FF for c in s):
                continue
            s = re.sub(r"⟦['\"]⟧(?=\s*[A-Za-z])", "", s)
            s = re.sub(r"⟦(['\"])⟧", r"\1", s)
            s = re.sub(r"[A-Za-z]+", "", s)
            s = s.replace("◆3", "◆4")  # stipulation applied in census
            for d, k in Counter(re.findall(r"◆(\d+)", s)).items():
                tc[f"◆{d}"] += k
            tc['"'] += s.count('"')
            tc["'"] += s.count("'")
            tc["dot"] += s.count(".") + s.count("◆4")
    g1 = (tc["◆4"] == 129 and tc["◆13"] == 32 and tc["◆10"] == 3 and
          tc["◆23"] == 1 and tc['"'] == 14 and tc["'"] == 3 and
          tc["dot"] == 148)
    assert g1, f"G1 census FAIL {dict(tc)}"
    rep.append(f"G1 PASS: N={N}; census {dict((k, v) for k, v in tc.items())}")

    # ---------------- G3 decode + null set ----------------
    ct56 = V.flat(56)
    res = V.brute_interrupters(ct56, V.phi_prime_stream(len(ct56)),
                              ["DEEPWEB", "PILGRIM", "HASHESTO"])
    assert res and res[1] == 3 and res[2] == "skip", f"G3 FAIL {res}"
    D56 = res[0]
    fpos = [t for t, c in enumerate(ct56) if c == 0]
    nulls = None
    for r in range(len(fpos) + 1):
        for combo in itertools.combinations(fpos, r):
            cs = set(combo)
            idx = V.decode_skipnull(ct56, V.phi_prime_stream(len(ct56)),
                                    [t in cs for t in range(len(ct56))])
            if V.translit(idx) == D56:
                nulls = combo
                break
        if nulls is not None:
            break
    assert nulls is not None, "G3 null-set FAIL"
    rep.append(f"G3 PASS: decode len {len(D56)}, null-F at CT {nulls}")

    w56, w57 = canon_words()
    C56, S56, E56 = build_canon(w56)
    C57, S57, E57 = build_canon(w57)
    D57 = V.translit(V.flat(57)).upper().translate(MERGE)
    rep.append(f"canonical: p56 {len(C56)} letters/{len(w56)} words "
               f"(stream {len(D56)}); p57 {len(C57)} letters/{len(w57)} "
               f"words (stream {len(D57)})")

    # ---------------- G2: p57 reproduction ----------------
    dsh57, mks57, _ = dash_positions(blocks[57])
    vb57 = verified(D57, C57)

    def align(b, vb, C, starts):
        for a, c0, s in vb:
            if a <= b < a + s - 1:
                cc = c0 + (b - a)
                return (cc + 1) in starts or C[cc] in ".,"
        return None  # outside verified regions

    al57 = [align(b, vb57, C57, S57) for b in dsh57]
    inside57 = [x for x in al57 if x is not None]
    g2d = all(inside57) and len(inside57) >= 12
    m57 = 0
    for ch, b in mks57:
        for a, c0, s in vb57:
            if a <= b < a + s:
                cc = c0 + (b - a)
                if ch == "4" and cc in E57:
                    m57 += 1
                if ch == "23" and cc == len(C57) - 1:
                    m57 += 1
    g2 = g2d and m57 == 3  # 2 sentence ◆4 + 1 book-end ◆23
    rep.append(f"G2 p57: dashes {sum(inside57)}/{len(inside57)} aligned "
               f"(of {len(dsh57)}; {len(dsh57)-len(inside57)} outside "
               f"verified); marks {m57}/3 -> {'PASS' if g2 else 'FAIL'}")
    assert g2, "G2 FAIL"

    # ---------------- V1: p56 dashes ----------------
    dsh56, mks56, n56 = dash_positions(blocks[56], nulls=set(nulls))
    # CT dash idx -> decode boundary: dash_positions already counted
    # non-nulls, so b is decode-side already.
    vb56 = verified(D56, C56)
    al56 = [align(b, vb56, C56, S56) for b in dsh56]
    excl = [b for b, x in zip(dsh56, al56) if x is None]
    inside = [b for b, x in zip(dsh56, al56) if x is not None]
    k = sum(1 for x in inside if x)
    n = len(inside)
    gaps = []
    for a, c0, s in vb56:
        gaps.extend(range(a, a + s - 1))
    G = len(set(gaps))
    B = sum(1 for b in sorted(set(gaps)) if align(b, vb56, C56, S56))
    p_v1 = hyper_p(k, B, G, n)
    # relikd cross-check
    rk = open(os.path.join(KDIR, "sources", "relikd_p56_an_end.txt")).read()
    rk = "".join(l for l in rk.splitlines()
                 if not re.fullmatch(r"[0-9a-f⁘\s]*", l.strip() or "x"))
    rpos, rr, rL = [], 0, 0
    for ch in rk:
        if 0x16A0 <= ord(ch) <= 0x16FF:
            if rr not in nulls:
                rL += len(VAL[V.R2I[ch]])
            rr += 1
        elif ch == "•":
            rpos.append(rL - 1)
    disagree = sorted(set(dsh56) ^ set(rpos))
    rep.append(f"V1: dashes n={n} aligned k={k}; verified gaps G={G}, "
               f"slots B={B}; excluded (unverified region) {excl}; "
               f"block-vs-relikd disagreements {disagree}; "
               f"hypergeometric p = {p_v1:.3e}")

    # ---------------- V2: scorer holdout ----------------
    qg = {}
    tot = 0
    for line in open(os.path.join(KDIR, "english_quadgrams.txt")):
        w, c = line.split()
        qg[w] = int(c)
        tot += int(c)
    floor = math.log10(0.01 / tot)

    def qscore(t):
        t = re.sub(r"[^A-Z]", "", t.translate(MERGE))
        s = 0.0
        for i in range(len(t) - 3):
            s += math.log10(qg.get(t[i:i + 4], 0) / tot) if t[i:i + 4] in qg \
                else floor
        return s / max(1, len(t) - 3)

    def cscore(t):
        t = t.translate(MERGE)
        return sum(1 for c in CRIBS if c in t) / max(1, len(t)) * 100

    rng = random.Random(SEED)
    v2 = []
    for nm, C in (("p56", C56), ("p57", C57)):
        base = qscore(C) + 0.5 * cscore(C)
        beats = 0
        ls = list(C)
        for _ in range(1000):
            rng.shuffle(ls)
            sc = qscore("".join(ls)) + 0.5 * cscore("".join(ls))
            if sc >= base:
                beats += 1
        v2.append((nm, base, beats))
        rep.append(f"V2 {nm}: true score {base:.3f}, beaten by {beats}/1000 "
                   f"shuffles")
    g_v2 = all(b == 0 for _, _, b in v2)

    # ---------------- V3: report-only panel ----------------
    UNITS = [("Q1", [0, 1, 2]), ("Q2", [3, 4, 5, 6, 7]),
             ("Q3a", list(range(8, 15))), ("Q3ax", [15]),
             ("Q3b", list(range(16, 23))), ("Q4", [23, 24, 25, 26]),
             ("Q5", list(range(27, 33))), ("Q6", list(range(33, 40))),
             ("Q7a", list(range(40, 50))), ("Q7b", list(range(50, 54))),
             ("Q7c", [54, 55])]
    panel = []
    for uid, pg in UNITS:
        wl, sl = [], []
        for p in pg:
            for raw in blocks[p].splitlines():
                s = rune_seg(raw)
                if s is None or s in ("&", "$", "§") or \
                        not any(0x16A0 <= ord(c) <= 0x16FF for c in s):
                    continue
                s = re.sub(r"⟦['\"]⟧(?=\s*[A-Za-z])", "", s)
                s = re.sub(r"⟦(['\"])⟧", r"\1", s)
                s = re.sub(r"[A-Za-z0-9]+", "", s).replace("*", "")
                s = s.replace("◆3", "◆4").replace("◆4", ".").replace(
                    "◆13", "¶").replace("◆10", ".").replace("◆23", "§")
                s = s.replace("/", "").strip()
                for wd in s.split("-"):
                    for w in re.split(r"[.'¶§\"]+'?", wd):
                        if w:
                            wl.append(len(w))
                for sent in re.split(r"\.+", s):
                    ws = [w for wd in sent.split("-")
                          for w in re.split(r"[¶§\"']+", wd) if w]
                    if ws:
                        sl.append(len(ws))
        panel.append(f"  {uid}: words {len(wl)}, mean len "
                     f"{sum(wl)/len(wl):.2f}; sentences {len(sl)}, mean "
                     f"{sum(sl)/max(1,len(sl)):.1f} words")
    rep.append("V3 (report-only):\n" + "\n".join(panel))

    # ---------------- verdict ----------------
    if p_v1 < 0.05 and g_v2:
        verdict = ("SKELETON-QUALIFIED — separator skeleton adopted as crib "
                   "constraint set (word lengths, sentence breaks, quotes, "
                   "merged alphabet)")
    elif p_v1 >= 0.2:
        verdict = ("SKELETON-PAGE-DEPENDENT — channel real on p57 only; "
                   "p56 skeleton noise-grade; constraints NOT adopted; "
                   "feeds oracle round")
    else:
        verdict = ("INCONCLUSIVE — no adoption, no rejection; #22 "
                   "candidate")
    if not g_v2:
        verdict = "SCORER-FAIL (V2) — " + verdict
    rep.append(f"VERDICT: {verdict}")
    rep.append(
        "DISCLOSURES: (1) design-pass peek (PREREG). (2) FIRST COMPLETED "
        "RUN WAS INVALID (pre-fix, not retained as output): canonical "
        "anchor matched 'FIND AN END' in the WELCOME text (4,727-letter "
        "blob), hyper_p summed the LOWER tail (p=1.0), and the relikd "
        "cross-check truncated at the hash marker; all three fixed before "
        "this run. (3) PREREG arithmetic note 'canonical 91 > stream 85' "
        "was a rune-vs-letter error: 85 runes -> 91 letters via TH/NG/EO "
        "digraphs; lengths match exactly. (4) signed-file mid-word wraps "
        "repaired by the dictionary rule in _join_run "
        "(/usr/share/dict/words) — post-registration instrument detail. "
        "(5) mid-tail unverified region: excluded dashes listed above. "
        "(6) shuffles = weak null; V3 descriptive only.")
    with open(f"{OUT}/REPORT.md", "w") as f:
        f.write("# Campaign #21 report — separator-skeleton "
                "qualification\n\n" + "\n\n".join(rep) + "\n")
    print("\n".join(rep))


if __name__ == "__main__":
    main()
