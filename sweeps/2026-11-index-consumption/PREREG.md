# Campaign 2026-11-index-consumption — PREREG

Registered 2026-11-14, **before any campaign output** (this commit contains no
`results/`). Prior campaigns: #1–#5 (see docs/LEDGER.md).

## Why this campaign exists (instrument audit, not lore)

Every statistic campaigns #1–#5 have used is a function of
`(A[i] − k·B[i+o]) mod 29`: the pad is consumed **left-to-right, one rune per
rune, from a fixed start**. That is one point in the space of ways a stream can
be *consumed*. Two things told us the axis is open:

1. **dukotah's own ledger** names it as not covered: Round 22 lane C ran
   decimation at **width 4 only, 4 phases**, adjudicated by an English-only
   panel bar (their standing caveat L7-A says every negative in that repo is
   English-only), and its `not_covered` list reads *"interleave/decimation
   widths ≠ 4"*.
2. **Our own gap**: our stride work (#3 E, #5 K/L) used **phase 0 only**
   (`p[::g]`) and **dropped** elements rather than wrapping. Non-zero phases and
   wrap-around consumption were never swept by either effort.

This is the "aim at the instrument, not the space" move: we are sweeping a
consumption rule our 236M-alignment instrument is structurally blind to, not
another key.

## What is swept

Pad sources: 57 cipher pages (0–54, 56, 57) + 2 solved plaintext streams = 59.
Targets: the 55 unsolved pages (0–54). Statistic: language-agnostic χ² vs
uniform over 29 bins, `min_len = 50`, mask `tgt` primary / `both` sensitivity.
Verdict statistic: **family global max**.

**Family P — drop-decimation, complete phase set.**
`pad = S[b::a]` for width `a ∈ 2..28`, phase `b ∈ 0..a−1`, kept when
`len ≥ 50`; orientations fwd + rev. Widths surviving the length floor are
**{2,3,4,5}** (≥6 length-vacuous: longest page 277 runes). All `a` phases are
swept, so this family is **complete by construction** — it closes our phase-0
gap and dukotah's widths≠4 gap in one stroke. 1,210 pads.

**Family W — cyclic (wrap-around) decimation.**
`pad = [S[(a·j + c) mod L] for j in range(L)]` — a full-length *permutation*
read of the source, not a shortened drop. Step `a ∈ 2..28` with
`gcd(a, L) = 1`; cut `c ∈ C(a) = {(a·⌊i·L/k⌋) mod L : i = 0..k−1}` with
`k = ⌈L/(L − 50 + 1)⌉` cuts; orientations fwd + rev. 4,128 pads.
*(The cut set is spread in the step-a coordinate, not the index coordinate —
see guarantee 1; this was corrected during pre-registration verification,
before any output.)*

## Collapses and coverage guarantees, declared up front

1. **Phases are cuts, and the cut set gives COMPLETE alignment coverage.**
   For `gcd(a,L)=1` the `L` possible starts are cyclic rotations of one
   traversal. A true alignment `(a, v)` (target i pairs with source
   `(a·i + v) mod L`) is tested by cut `c` at offset `o ≡ a⁻¹(c − v) (mod L)`,
   and the cut yields a usable window (≥50 valid positions) iff a
   representative of that class lands in `[50−L, m−50]`. Spreading the cuts as
   `a·⌊i·L/k⌋` makes `a⁻¹·C(a) = {⌊i·L/k⌋}` evenly spaced (gap ⌈L/k⌉), and
   with `k = ⌈L/(L−49)⌉` every residue class is within reach for **every**
   (source length L, step a, alignment v, target length m) in this corpus —
   verified **exhaustively** (59 sources × all coprime steps × all L
   alignments × all 55 targets, actual ᚠ positions, not a bound): **0
   violations**. So family W is complete over its registered step range:
   every cyclic alignment is scanned with ≥50 valid positions.
   *Correction note:* the first draft placed cuts at index-space `⌊i·L/k⌋`;
   the arithmetic shows cuts must be spread in the step-a coordinate
   (index-space cuts cluster in cycle coordinates for some steps — e.g.
   L=277, a=139 puts cuts {0,138} at cycle positions {0,276}, adjacent, so
   long windows were invisible for many alignments). Caught in
   pre-registration verification and fixed **before any output**; pad count
   unchanged (4,128). A doubled-read alternative (2L pad, single cut) was
   tried and rejected: maximal-overlap window semantics break the all-cuts
   equivalence (measured deficits up to 18.5 χ²).
   Residual caveat: each alignment is tested at its **maximal-overlap**
   window (as in #1–#5); a true region shorter than the overlap dilutes.
2. **Step `a` and step `L−a` are reversal-images** (reversing the (a,c)
   traversal yields the (L−a, c″) traversal, c″ = a(L−1)+c), and both fwd and
   rev orientations are scanned. Therefore steps `L−28..L−1` are covered by the
   rev orientation of steps 2..28 — and the induced cut sets {a(L−1)+c} are
   evenly spread in the (L−a)⁻¹ coordinate too, so the completeness check of
   guarantee 1 is run for those steps as well. **Not covered: steps
   29..L−29** (the mid-range).
3. **Target-side permutation collapses to pad-side permutation**: substituting
   `t = a·j + c` turns a permuted-target scan into a scan of the plain target
   against a permuted pad with an additive offset, which the offset scan
   covers. Only the pad side is permuted.
4. **`a = 1` is excluded** — it is the identity pad, i.e. campaign #1's
   running-pad family.
5. **No Caesar-shift dimension.** χ² vs uniform is **invariant under a constant
   shift of the pad** (it rotates the difference histogram; Σc² unchanged).
   Verified numerically (max χ² identical to 4 decimals for s ∈ {0,1,7,14,28}).
   This is what killed the originally-proposed "constant-shift mirror" design as
   a *new* sweep — all 29 shifts are the same test campaign #1 already ran.
6. **Mirror (fwdrev) pads are not swept here**: a cyclic pad is already a
   closed cycle, and its reversal is scanned as the rev orientation.
7. Length floor 50 and the single-2017-root transcription caveat carry over
   from #1–#5; page 55 excluded (missing).

## Decision rule (fixed before running)

- **GO** iff observed family max > **1.1 × family null max** *and* the leader
  survives mask=`both` *and* its decode carries English cribs.
- **Escalation** (as #5): if a family's observed max ≥ its 20-draw null
  **median**, extend that family to **≥200 draws** before any verdict ships.
- Otherwise **NEGATIVE**, reported with coverage × power.

## Null calibration

20 in-page shuffles of the 55 targets (lengths, frequencies and F-density
preserved; pads stay real), **seed 20261120**, shuffle stream shared across
families. Vectorized family max (`scan_max`), with a startup self-check
asserting equality against the `pair_scan` loop path on real streams, **and**
the exhaustive alignment-coverage verification of guarantee 1, both run before
any shuffle. Resumable per-family checkpoints.

## Power probe (planted signal — coverage alone is not enough)

Coverage without power is not citable. We plant **10 synthetic true pads** into
10 distinct targets simultaneously — `A′ = A + pad_window (mod 29)` at a random
(step, cut, orientation, offset) drawn from the family's own geometry — then
run the *unmodified* family scan and record, for each plant, whether the true
window's χ² reaches the family null median (the threshold a real hit would have
to clear). Recovery rate = **power at threshold**. One extra family scan per
family; reported in `results/power.csv` and in the REPORT.

## Cost (measured, not guessed)

`scan_max` throughput measured on this corpus: 0.31 ms per (target, pad) for
P-type pads, 0.57 ms for W-type. Family P: 1,210 pads → ~0.3 min observed,
~7 min null (20 draws). Family W: 4,128 pads → ~2.1 min observed, ~43 min
null. Escalation to 200 draws: ~7 h (W). Both nulls run in parallel; power
probes add one observed-cost pass each. (Supersedes the first-draft estimate
of 1.26 ms/pair — same design, re-measured after the cut-placement fix;
no output existed when either number was written.)

## Deliverables

`run.py`, `calibrate.py`, `results/{obs_maxima,null_P,null_W,leaders_both,
window_counts,power}.csv|json`, `sweep_{P,W}.csv` (repo copies = top 100,000
rows by χ²; full files stream to `work/index-consumption/` with sha256 recorded
in metadata.json and a deterministic regeneration command), `REPORT.md`,
`metadata.json`, LEDGER row #6, README headline.

## Remaining gaps after this campaign (pre-declared)

Mid-range cyclic steps 29..L−29; non-uniform interleavings of two pads;
triple products (k × stride × index-permutation); digit/ornament channels;
page 55; LP1 material (out of scope by design).
