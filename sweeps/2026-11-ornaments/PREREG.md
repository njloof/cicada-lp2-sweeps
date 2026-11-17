# Campaign #13 PREREG — F7: dot-lattices as data (language-agnostic structural tests)

Registered 2026-11-16, BEFORE any campaign output (docs/LEDGER.md rule; CI
gate). Queue slot 5 (docs/MAP.md §G): "F7 ornament bands — language-agnostic
structural test, their listed reopen".

## 0. Object and reopen justification

Object: the **35 red dot-lattice section ornaments** (table `lattices.csv`,
extracted from the gitignored `work/red_census/census.csv`, owner round-1
confirmed size classes 13/10/23, machine-verified cluster counts 2026-11-15).
Each record = (page, band, y0, y1, x0, x1, dots).

Reopen (why this is not already closed): dukotah's ornament work
(round18/L3-ornaments; ELIMINATION-LEDGER A-06/B-12) physically classified
109 bands/39 pages (T=82 mis-grouped text, V=10 vine, W=3 woodcut, D=5
non-runic data) and found no runic message — that is a **physical**
verdict, not a structural-information verdict. R19-FINITE-ORNAMENT-REGISTER
("74 of 74 ornament bands show no language", AUDIT-inhibitors.md:49) is
English-register only; its own `not_covered` concedes English registers are
"underpowered (noisy recovery <0.80) — little information". They explicitly
re-listed a language-agnostic test of (page, position, count) triplets vs
run-structure nulls. That gap is this campaign.

Dup-check (both ledgers, before this campaign):
| candidate | status |
|---|---|
| bands physical classification / runic-content scan | DONE negative (L3, A-06/B-12) |
| bands English register | DONE, self-declared underpowered (R19) |
| lattice sizes/counts | CENSUS only (ours, RED_CENSUS.md; owner-confirmed) |
| lattice page/position/count vs run structure | **OPEN in both ledgers — this campaign** |
| dot-counts as position selectors | OPEN; analogous to our red-digit selection channel (U3: printed 1–5 select lines) |

## 1. Registered families (three verdicts, α = 0.05/3 ≈ 0.0167 each)

Stream = unsolved pages 0–49 + 51–55 (L = 12,956), page_start[p] = cumulative
length. Image anchor of a lattice = page·3600 + y0 (monotone across the book;
image space is page-size-constant, 2400×3600).

**O1 — section-head alignment (exact, no MC).**
22 distinct lattice pages vs 14 pre-declared red-rune head pages
{0,3,6,7,8,15,23,27,33,37,39,40,53,54} (dukotah redrune list, cited not
re-derived). Universe N = 57 pages (0–57 minus 50). Statistic = overlap size;
observed 11. Null = hypergeometric, one-sided (excess co-occurrence).
Caveat disclosed: both lists come from the red-ink census, but lattices
(dot matrices) and heads (red words) are distinct image features; the
co-occurrence was never quantified by anyone. Exact power statement (no
plants needed): report the smallest overlap k with p ≤ α.

**O2 — dot-count vs section length (permutation MC).**
All 35 lattices ordered by image anchor; gap_i = anchor_{i+1} − anchor_i
(34 consecutive gaps; last lattice drops). Statistic = |Spearman ρ| between
dots and gap (ties averaged). Null: permute the dots multiset
{13×31, 10×4, 23×1} across lattices (preserves counts exactly, destroys
pairing), D = 10,000. Two-sided via |ρ|.

**O3 — dot-counts as position selectors (permutation MC).**
For lattices on stream pages only (n = 30; the 5 lattices on solved pages
56–57 have no stream anchor — declared exclusion): selected rune value =
stream[(page_start[page] + dots − 1) mod L]. Statistic = coincidence count
Σ_r C(n_r, 2) (language-agnostic: counts value clustering, no alphabet
assumption). Null: permute the dots multiset {13×27, 10×3} across the 30
positions, D = 10,000. One-sided (excess coincidence).

**O4 — descriptive only, NO verdict, NO α.** y-coordinate histogram and
pairwise differences (line-grid quantization check), x distribution, band-0
lattice count (4), per-page lattice counts, co-occurrence with title bands.

## 2. Power plants (mandatory)

- O1: exact — minimum detectable overlap reported.
- O2: monotone-rearrangement plant (dots ranked against gap ranks; the
  maximum-|ρ| assignment given the fixed multiset). Power = P(plant |ρ| >
  null p95), 20 tie-noise draws.
- O3: **exhaustive ceiling plant** — over all C(30,3) = 4,060 ways to place
  the three 10-dot counts (rest 13), compute the coincidence count; plant =
  argmax. Power = 1 if ceiling > null p95 else **structurally weakly
  powered, declared in advance from the ceiling itself** (the honest
  statement: if even the best permutation of the observed counts cannot beat
  p95, a non-firing obs carries no information).

## 3. Kill gates (before any statistic)

- G1: `lattices.csv` has 35 rows; Counter(dots) = {13: 30, 10: 4, 23: 1};
  matches RED_CENSUS.md classes.
- G2: corpus stream L = 12,956 (core.validate N=Q=29).
- G3: head list has 14 distinct pages, all inside the 57-page universe.

## 4. Seeds / runtime

Seed 20261202; streams `default_rng([seed, crc32(tag)%100000, draw])`, tags
{"O2","O3","plant-O2"}. No escalation needed (D=10,000 is the registered
stage; everything is closed-form or tiny-array). Estimated total runtime
**< 30 s** single-machine (no studio offload).

## 5. Verdict rule

A family fires (FLAG) iff p ≤ 0.0167 **and** the power plant exceeds the
family's null p95 (O1: exact power sentence instead). Otherwise NEGATIVE
with the power sentence. Any FLAG → oracle/crib follow-up registration
before interpretation. Results JSON: `results/f7_results.json`.
