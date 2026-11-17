# Campaign #18 PREREG — decoration-based segmentation of LP2 (MAP 6d)

Registered 2026-11-17, BEFORE any campaign output (CI gate). Owner
hypothesis (2026-11-17, verbatim intent): page decorations "mostly denote
areas that are all part of the same passage: either they decorate a series
of pages in a row, or they begin and end a series of pages, or both;
occasionally a single symbol ... our ciphertext can be divided, not into
pages, but into groups based on the decorations as delimiting symbols."
Owner count question answered machine-side; owner CORRECTION accepted
(p0 shares the fence+∞ family with p1/p2 → merged). Prior support
(docs/PRIORS.md): LP1 was keyed per page-SECTION (transliteration →
Atbash → Vigenère-DIUINITY → shift-3 → totient); symmetry is documented
house style (LP1 180° palindromes; owner's p7↔p23 flipped-5-dot bracket);
jbo-tools independently sections pp23–26 as a "mayfly" ornament group.

## 0. Objects

**Segmentation (owner decoration classes; data-encoded in the script):**

| id | pages | delimiting evidence |
|----|-------|---------------------|
| P1 | pp00–02 | fence + ∞ top/bottom family (owner p0 correction) |
| P2 | pp03–04 | undecorated gap |
| P3 | pp05–07 | symmetric spiral-scrolls ×3 |
| P4 | pp08–23 | interior of p7↔p23 flipped-5-dot bracket |
| P5 | pp24–25 | mirrored cicadas ×2 (jbo "mayfly" group agrees) |
| P6 | pp26–32 | gap |
| P7 | pp33–39 | pixel-identical black stamp ×7 (machine-verified) |
| P8 | pp40–48 | p40↔p48 margin-asymmetry bracket |
| P9 | pp49–55 | gap; contains the whole base-60 token stream |
| P10 | pp56–57 | solved closing pages (EXCLUDED from stream stats) |

Stream = pp00–49, 51–55 in book order, 12,956 runes (p50 runeless).
Group stream ranges: P1 0–728 · P2 729–1206 · P3 1207–1873 ·
P4 1874–5718 · P5 5719–6261 · P6 6262–7959 · P7 7960–9639 ·
P8 9640–12047 · P9 12048–12955.

## 1. Registered statistics (exploratory panel; multiplicity DISCLOSED)

**S1 — T7 void containment/alignment.** Campaign #10 localized the
doublet-slip void to stream pos 2739–4388 (1,649 runes, zero doublets).
If groups are real independent streams, the void should be a property of
one stream: statistic = the void is contained within a single group (and
distance of void edges to group edges). Null: uniform placement of a
1,649-rune window over 12,956 positions (analytic). p = P(random window
contained in one group). DIRECTIONAL: containment is CONSISTENT-with-
groups; edge-alignment would be stronger. No claim if p ≥ 0.05.

**S2 — per-group doublet deficit decomposition.** The corpus anomaly is
0.66% vs 3.45% expected (~86/12,956). Per group: observed doublets,
expected (adjacent-pair independence, group-local rune frequencies),
z-score. If the deficit is a property of independent per-group streams,
it should appear in most groups (sign test, analytic binomial null,
n = 9 groups). If it is a pooled artifact (e.g. a cross-page boundary
effect), expect it to concentrate at page joins.

**S3 — sentence-dot (krisyotam `.`/◆) density homogeneity.** `.` =
sentence separator. Per-group '.' per 100 runes; χ² vs uniform-in-stream
null (permutation of '.' labels over stream positions, D = 20,000, seed
20261218). Independent passages plausibly differ in sentence density;
one continuous text should not.

**S4 — word-length profile differentiation.** Per-group word-length
histogram (bins 1/2/3/4–6/7+, #17 convention, krisyotam separators);
χ² across groups vs permutation null (labels permuted, D = 20,000, same
seed). Groups differing ⇒ consistent with separate plaintexts; identical
⇒ consistent with one text OR identical registers (not decisive).

## 2. Kill gates

G1 stream L = 12,956 EXACT (core.validate flat, p50 absent, pp56–57
excluded). G2 segmentation partitions pp00–55 EXACTLY once (9 groups,
owner-corrected). G3 void position reproduces #10: zero-doublet span
2739–4388 recomputed from the corpus must match (doublet list = adjacent
equal runes; span contains zero, flanks contain ≥1).

## 3. Verdict rule (registered pre-output)

Structural campaign (precedent #13 O4): NO single decisive verdict.
Report = panel of four p-values, Holm-corrected, each labeled
SUPPORTS/NEUTRAL/REFUTES for "groups are independent streams." A
SEGMENTATION-CONSISTENT reading requires ≥2 SUPPORTS with 0 REFUTES.
Any REFUTES (esp. S2 page-join concentration, or S1 non-containment with
p < 0.05 against) → groups stay a reading frame for presentation but do
NOT restructure the analysis pipeline (per-group frequency analysis,
per-group cribs stay unadopted).

## 4. Runtime

Deterministic + two 20k permutation nulls on ≤13k items: **< 60 s**,
local. No studio.

## 5. Not covered (declared)

Whether groups have distinct KEYS (crib design is 6c, downstream); the
identity of single-symbol decorations (owner round #6 S9/S10 live);
krisyotam separator fidelity at page joins (caveat inherited from #17);
P10 solved pages (different construction, excluded).
