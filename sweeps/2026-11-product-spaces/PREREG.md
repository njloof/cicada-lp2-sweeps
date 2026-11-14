# PREREG — 2026-11-product-spaces (Phase 5 / campaign #5)

**Status: REGISTERED BEFORE OUTPUT.** Written 2026-11-14; no campaign #5
computation has been run. Amendments only before the first result-producing run,
appended with timestamp + disclosure.

## Motivation

Campaigns #1–#3 swept the pad families pairwise-independently; the #3 ledger row
names what stayed open: the **scaling × stride product space**, the
**scaling × mirror-junction** product space (mirror orderings excluded from D by
that campaign's scope), and **stride extension** beyond g∈{2,3}. Campaign #4
closed the p12 flag question. This campaign closes the pairwise product spaces
so the elimination map has no product-space holes at the pairwise level.
Position-dependent pad derivations (digit/ornament channels) need an instrument
redesign and are **not** in scope here (campaign #6 candidate).

## Collapses declared up front (free coverage, not swept twice)

- `k ∈ {0,1,28}` and sign symmetry `k ↔ 29−k`: exactly campaign #3's collapses.
- **Straddle-only mirrors.** Mirror pads contain the plain pad as a sub-window;
  the junction-straddle filter (campaign #1's convention: window pad-span
  crosses the junction index `s = len(C_N)`, equivalently `-s < off ≤ m−1−s`)
  removes windows already swept by #1 (k=1) and by family L/D (k>1). No
  double-counting across families.
- **Trivial self-pair mirror identities** excluded as in #1: `fwdrev` off 0 and
  `revfwd` off −len(C_N) for M=N (pad window == target, all-zero D).
  Strided pads (g ≥ 2) can never equal the target — no trivial windows exist
  in K/L, so no exclusion there.
- **Mask k-invariance**: `k·0 = 0` — pad-side ᚠ geometry is k-invariant
  (campaign #3 observation, reused for the mult_scan helper).
- **Null-distribution note (declared, not used as a shortcut)**: under the
  shuffled-target null, `(A − k·B) mod 29` is i.i.d. uniform for every k, so the
  *marginal* per-window null is k-free; only the max-statistic multiplicity
  changes. The nulls below are still computed honestly over the full k-space.

## Families swept

**K — stride extension + strided mirrors (new geometry).**
(a) `pad[t] = C_N[g·t]`, `pad[t] = C_N[n−1−g·t]`, **g ∈ {4..8}** (extension of
#3's E beyond g=3). Pre-declared vacuity disclosure: with the longest page 261
runes, `261//6 = 43 < 50 = MIN_LEN`, so g ∈ {6,7,8} contribute **zero** pads;
effective stride coverage after this campaign is g ∈ {2..5}, and the ledger must
say so.
(b) **Strided mirror pads**: `q = C_N[::g]`, pads `[q, rev(q)]` and `[rev(q), q]`,
g ∈ {2..5}, straddle-only (junction = len(q)); both strided streams
(`C_N[::g]` and `C_N[n−1−g·t]`-derived) get both orderings. Difference
statistic, all targets, min_len 50, mask tgt primary / both sensitivity.

**L — scaling × stride (product of #3's D and E).**
`D = (C_M − k·W) mod 29`, k ∈ {2..27}, W ∈ strided pads
`C_N[::g]`, `C_N[n−1−g·t]` for g ∈ {2..5} (all survive-or-drop by length).
Solved-plaintext pads contribute **no** strided pads ≥ 50 (lengths 84/95 →
42/47 after g=2) — disclosed, they participate only via M.

**M — scaling × mirror junction (the product #3's D excluded).**
`D = (C_M − k·B) mod 29`, k ∈ {2..27}, B ∈ plain mirror pads
`[C_N, rev(C_N)]`, `[rev(C_N), C_N]` for all 57 ciphertext pads **plus** the
2 solved plaintexts mirrored; straddle-only; trivial self-pair offsets excluded.

Targets: 55 unsolved pages (≤54). Statistic, floor (40), and min_len (50) as
campaigns #1–#3. `core/kernel.py` **unchanged**; `mult_scan` is a campaign-local
copy of #3's helper; straddle filtering is the post-hoc offset test above.

## Instrument & calibration

Per-family MC null of the **global max**: 20 in-page shuffles (all 55 targets
shuffled, lengths/frequencies/F-density preserved; pads stay real), seed
**20261119**, shared shuffle stream across families, resumable RNG checkpoints
(#4's pattern). One process per family may run in parallel; the stream is
seed-identical either way.

**Escalation rule (new, pre-declared — the #4 lesson made explicit):** if a
family's observed max ≥ its 20-draw null **median**, that family's null is
extended to ≥200 draws before any verdict is written. A near-null observed value
at 20 draws is provisional by house rule; far-below observed values need no
extension (negative is decided with the null band disclosed).

## Decision rule (fixed now)

GO on K, L, or M iff observed max χ² > 1.1 × that family's MC null max **and**
the window survives mask=both **and** decodes with English cribs. Otherwise
NEGATIVE for that family. No structural prong this campaign.

## Cost & runtime disclosure (pre-declared)

Observed: K minutes; L ≈ 15–25 min (~1.2×10¹¹ pair-ops); M ≈ 25–40 min.
Nulls (20 draws): K < 1 h; L ≈ 6 h; M ≈ 9–13 h — resumable, run in background
chunks, one process per family. Wall-clock is disclosed up front so chunking is
never post-hoc.

## Deliverables & repo policy

results/ CSVs (floor 40, χ²-sorted, **top 100k rows tracked**; full CSVs to
`work/` with sha256 + deterministic regeneration command disclosed in the
REPORT — repo size policy). `obs_maxima.csv` (family, windows, observed max —
calibrate.py reads it, no hardcoded drift), `null_K.csv` / `null_L.csv` /
`null_M.csv`, `window_counts.json`, `metadata.json` (corpus manifest sha256,
core rev, seed, exact counts), REPORT.md + ledger row with
coverage/not-covered.

## Remaining gaps after this campaign (pre-declared)

Position-dependent pad derivations (digit/ornament channels — needs min_len
redesign + own null; campaign #6 candidate); non-uniform interleavings beyond
constant stride; **triple** products (k × stride × mirror; only pairwise
products close here); effective stride coverage ends at g=5 (length-bound,
disclosed); page 55; pads derived from LP1 pages (out of scope by design).
