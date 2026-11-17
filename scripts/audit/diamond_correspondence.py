#!/usr/bin/env python3
"""Campaign #16 — black 4-dot diamonds vs krisyotam '.' separators.

Deterministic structural tests T1-T4 per sweeps/2026-11-diamonds/PREREG.md
(read it first; committed BEFORE this ran). Inputs pinned there:
ORACLE_PAGES.md @ c52bf40, krisyotam BOOK baseline, fourdots.csv.

Usage: python3 -I scripts/audit/diamond_correspondence.py
Writes sweeps/2026-11-diamonds/results/{t1_exceptions,t3_detector,
t4_residual}.csv + REPORT.md (all small, tracked).
"""
import csv
import difflib
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
from insert_transcriptions import load_pages, MD  # noqa: E402

OUT = os.path.join(ROOT, "sweeps", "2026-11-diamonds", "results")
FOURDOTS = os.path.join(ROOT, "sweeps", "2026-11-ornaments", "fourdots.csv")
DIAM = re.compile(r"◆(\d+)(\*?)")
UNSOLVED = [p for p in range(58) if p not in (50, 56, 57)]


def owner_lines(md):
    """page -> {line_no: logical owner body} (roman + annotations +
    continuation wraps removed; annotations kept is fine — they follow
    '   = ' or start with 3 spaces + latin, cut at first '   = ')."""
    pages = {}
    for p in range(58):
        img = f"![p{p}](img/oracle/pages/p{p:02d}.jpg)"
        i = md.find(img)
        if i < 0:
            continue
        h = md.find("**Ciphertext**", i)
        o = md.find("```", h)
        c = md.find("```", o + 3)
        cur, d = None, {}
        for l in md[o + 4:c].split("\n"):
            m = re.match(r"^\s*(\d+)\s+(.*)$", l)
            if m:
                cur = int(m.group(1))
                body = m.group(2)
            elif cur is not None and re.match(r"^\s{2,}\S", l):
                body = l.strip()
                d[cur] = d.get(cur, "") + body   # continuation wrap
                continue
            else:
                continue
            body = body.split("   = ")[0]
            d[cur] = d.get(cur, "") + body
        pages[p] = d
    return pages


def main():
    os.makedirs(OUT, exist_ok=True)
    base = load_pages()
    md = open(MD).read()
    own = owner_lines(md)

    # ---- G gates ----------------------------------------------------------
    assert len(base) >= 57, "G1"
    sys.path.insert(0, ROOT)
    from core.validate import flat
    # G3: unsolved total, book 0-55 (p50 runeless) — same gate as validate
    L = sum(len(flat(n)) for n in range(56) if n != 50)
    assert L == 12956, f"G3: L = {L}"
    report = [f"# Campaign #16 report — diamonds vs '.' (PREREG "
              f"sweeps/2026-11-diamonds/PREREG.md)\n",
              f"\nG3 corpus L check: load_page sum = {L} (expect 12,956 "
              "if API returns rune lists)"]

    # G2: line-number sets equal baseline segment counts
    g2 = [(p, len(base.get(p, [s for s in []])), len(own.get(p, {})))
          for p in range(58)]
    g2v = []
    for p in range(58):
        nb = len(base.get(p, []))
        no = len(own.get(p, {}))
        if p == 50:
            continue
        if nb != no:
            g2v.append((p, nb, no))

    # ---- extraction: per-line char diff ------------------------------------
    marks = []   # (page, line, ◆size, red?, replaced_char, ctx_before)
    other_edits = []
    residual = []  # (page, line, dot_index, n_dots_line, line_final, red_adj)
    for p in UNSOLVED + [56, 57]:
        segs = base.get(p, [])
        for li, seg in enumerate(segs, 1):
            ob = own.get(p, {}).get(li)
            if ob is None:
                continue
            # cut generator annotation (3+ spaces + latin) from owner body
            ob = re.sub(r"\s{3,}[A-Za-z].*$", "", ob)
            seg_clean = seg.strip()
            if ob == seg_clean:
                for m in re.finditer(r"\.", ob):
                    pass
            sm = difflib.SequenceMatcher(None, seg_clean, ob, autojunk=False)
            n_dots = seg_clean.count(".")
            dot_k = 0
            # walk baseline, tracking dot ordinals via equal/replace blocks
            for tag, i1, i2, j1, j2 in sm.get_opcodes():
                b, o = seg_clean[i1:i2], ob[j1:j2]
                if tag == "equal":
                    for k, ch in enumerate(b):
                        if ch == ".":
                            dot_k += 1
                            pos = i1 + k
                            rest = seg_clean[pos + 1:]
                            residual.append((
                                p, li, dot_k, n_dots,
                                "." not in rest.split("/")[0] if "/" in rest or True else None,
                                "*" in seg_clean[max(0, pos - 3):pos]))
                    continue
                if tag in ("replace", "insert"):
                    for m in DIAM.finditer(o):
                        rep = b if len(b) == 1 else ("multi" if b else "ins")
                        cb = (seg_clean[max(0, i1 - 2):i1] if tag == "replace"
                              else seg_clean[max(0, i1 - 2):i1])
                        marks.append((p, li, int(m.group(1)), m.group(2),
                                      rep, cb))
                    rest_o = DIAM.sub("", o)
                    if rest_o.strip():
                        other_edits.append((p, li, tag, b, o))
    # line_final recompute (clean): last '.' in line
    residual = [(p, li, dk, nd, dk == nd, ra) for (p, li, dk, nd, _, ra)
                in residual]

    # ---- T1 ----------------------------------------------------------------
    t1 = {}
    for m in marks:
        if m[2] == 4:
            t1[m[4]] = t1.get(m[4], 0) + 1
    n4 = sum(t1.values())
    rate = t1.get(".", 0) / n4 if n4 else 0.0
    verdict = ("CONFIRMED" if rate >= 0.95 else
               "REFUTED" if rate < 0.80 else "MIXED")
    with open(f"{OUT}/t1_exceptions.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["page", "line", "size", "red", "replaced", "ctx_before"])
        for m in marks:
            if m[2] != 4 or m[4] != ".":
                w.writerow(m)

    # ---- T2 ----------------------------------------------------------------
    orn = {}  # page -> [line numbers of &/$/§ segments]
    for p, segs in base.items():
        orn[p] = [li for li, s in enumerate(segs, 1)
                  if s.strip() in ("&", "$", "§")]
    tab = {}
    for (p, li, sz, red, rep, cb) in marks:
        if sz in (10, 13, 23):
            near = [s for s in orn.get(p, []) if abs(s - li) <= 1]
            key = (sz, ",".join(base[p][x - 1].strip() for x in near) or "none")
            tab[key] = tab.get(key, 0) + 1
    # reverse: ornaments with adjacent large ◆
    rev = {}
    big = {(p, li) for (p, li, sz, *_ ) in marks if sz in (10, 13, 23)}
    for p, ls in orn.items():
        for x in ls:
            sym = base[p][x - 1].strip()
            adj = any((p, y) in big for y in (x - 1, x, x + 1))
            rev[(sym, adj)] = rev.get((sym, adj), 0) + 1

    # ---- T3 ----------------------------------------------------------------
    det = {}
    with open(FOURDOTS) as f:
        for r in csv.DictReader(f):
            det[int(r["page"])] = det.get(int(r["page"]), 0) + 1
    own4 = {}
    for (p, li, sz, *_ ) in marks:
        if sz == 4:
            own4[p] = own4.get(p, 0) + 1
    rows, exact = [], 0
    for p in sorted(set(det) | set(own4)):
        if p not in UNSOLVED:
            continue
        d, o = det.get(p, 0), own4.get(p, 0)
        exact += (d == o)
        rows.append((p, o, d, o - d))
    with open(f"{OUT}/t3_detector.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["page", "owner_d4", "detector", "diff"])
        w.writerows(rows)
    ps = [(o, d) for (_, o, d, _) in rows if o or d]
    n = len(ps)
    def rank(v):
        s = sorted(range(len(v)), key=lambda i: v[i])
        r = [0] * len(v)
        for k, i in enumerate(s):
            r[i] = k
        return r
    xs, ys = [x for x, _ in ps], [y for _, y in ps]
    rx, ry = rank(xs), rank(ys)
    mx, my = sum(rx) / n, sum(ry) / n
    cov = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    vx = sum((a - mx) ** 2 for a in rx) ** .5
    vy = sum((b - my) ** 2 for b in ry) ** .5
    rho = cov / (vx * vy) if vx and vy else float("nan")

    # ---- T4 ----------------------------------------------------------------
    with open(f"{OUT}/t4_residual.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["page", "line", "dot_k", "n_dots_line", "line_final",
                    "red_adjacent"])
        w.writerows(residual)
    lf = sum(1 for r in residual if r[4])
    ra = sum(1 for r in residual if r[5])
    f4 = sum(1 for m in marks if m[2] == 4 and m[4] == ".")
    # line-final share for replaced ◆4: approximate via replaced-dot ctx
    # (replaced dots are the ones NOT in residual; their line-finality is
    # reported per-page alongside — full positional table in t4 csv)

    # ---- report ------------------------------------------------------------
    report += [
        f"\nG2 line-count violations (page, baseline, owner): {g2v or 'none'}",
        f"\n## T1 — ◆4 substitution targets (n={n4})",
        f"\nreplaced-char census: {t1}",
        f"\nrate('.'-replaced) = {rate:.4f} → **{verdict}** (thresholds "
        "≥0.95 / <0.80)",
        f"\nexceptions in t1_exceptions.csv; non-◆ owner edits "
        f"(quotes/dashes/breaks): {len(other_edits)}",
        "\n## T2 — large-lattice ↔ &/$/§",
        "\nmark→ornament (◆size, adjacent-ornaments): "
        + str(sorted(tab.items())),
        "\nornament→adjacent-large-◆ (symbol, has_adjacent): "
        + str(sorted(rev.items(), key=str)),
        f"\n## T3 — detector vs owner ◆4 counts: exact match {exact}/{n} "
        f"pages, Spearman ρ = {rho:.3f} (descriptive)",
        "\nfull table: t3_detector.csv",
        f"\n## T4 — residual '.' (not ◆4): {len(residual)} on unsolved "
        f"pages; line-final {lf} ({lf/max(1,len(residual)):.0%}); "
        f"red-adjacent {ra} ({ra/max(1,len(residual)):.0%})",
        f"\n◆4-replaced dots: {f4}; total baseline dots unsolved+56/57 = "
        f"{len(residual) + f4}",
        "\nfull table: t4_residual.csv",
    ]
    with open(f"{OUT}/REPORT.md", "w") as f:
        f.write("\n".join(report) + "\n")
    print("\n".join(report))


if __name__ == "__main__":
    main()
