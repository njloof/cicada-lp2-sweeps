# Pre-registration — Campaign #9: reading orientations × mirror pairs (2026-11-orientations)

Registered 2026-11-16. This file is committed before any campaign output
exists (CI gate). Space drafted from docs/CAMPAIGN9_MIRROR_DESIGN.md at the
owner's instruction ("make sure we consider mirror pairs including reversing
the direction of one or both pages"); owner scope GO recorded before the
sweep runs.

## Hypothesis

An LP2 designed object lives in a **page pair read under reading
orientations** — one or both pages read bottom-to-top, right-to-left, or
corner-to-corner (bottom-right→top-left) — that the id-orientation scans
of #1–#8 cannot see. Pair restriction tested: **mirror pairs (k, 55−k)**
(owner's first↔last idea). Book page numbers throughout (post-relabel
`2089fc2`).

## Orientation group and DECLARED collapses (the space, tightened before running)

Page = line grid from the pinned stream (`data/pages/`, lines preserved).
Four read transforms: `id`, `rl` (reverse line order), `rg` (reverse glyphs
within each line), `r180` = rl∘rg (true bottom-right→top-left corner read;
as a flat sequence, r180 = full reversal R). Applied independently to both
pages of a pair: 16 combos.

χ² of a window is invariant under reversing the window's symbol sequence,
and diff/sum commute with reversal: R(A) − R(B) = R(A − B) at the mirrored
offset (same for +). Therefore **(o_M, o_N) ≡ (r180∘o_M, r180∘o_N)** —
composing BOTH orientations with r180 reverses the result sequence and
changes no statistic at any offset (offsets are scanned exhaustively).
Pairing the 16 combos:

    (id,id)≡(r180,r180)   (id,rl)≡(r180,rg)   (id,rg)≡(r180,rl)   (id,r180)≡(r180,id)
    (rl,id)≡(rg,r180)     (rl,rl)≡(rg,rg)     (rl,rg)≡(rg,rl)     (rl,r180)≡(rg,id)

**16 → 8 orientation classes** (canonical reps: (id,id), (id,rl), (id,rg),
(id,r180), (rl,id), (rl,rl), (rl,rg), (rg,id)).
`rl` is NOT a flat reversal when line lengths differ — genuinely new; `rg`
likewise. For **diff** both operand orders are kept (D and −D have different
χ²). For **sum** the naive commutative collapse (o_M,o_N) ≡ (o_N,o_M) is
**invalid under the house tgt mask**: the mask drops target-side F positions,
so swapping operands changes the masked set. (Registered correction: the
first draft of this PREREG claimed the collapse; the registration-time pilot
on real pages falsified it — maxima differ at 23/24 real-pair checks. Sum is
therefore scanned in BOTH operand orders everywhere.)
Registration-time verification: all identities checked on synthetic
unequal-length line grids (seed 1) through the exact window/χ² semantics —
all hold; two implementation traps found doing it (rl must slice lines with
the ORIGINAL length list then reverse the list; the offset range is
[MINL−m, n−MINL], a transposed range silently breaks the identity). The
synthetic check ran UNMASKED, which is why it passed the sum-commute claim
the real-pilot then killed — lesson: pilot against the actual masked
instrument, not a toy.
**Pre-output verification (mandatory, output-blocking):** on a 3-pair pilot
of the REAL corpus, confirm each declared identity's family max matches to
the last bit; any mismatch means the space is re-declared before the sweep
counts.

## Families

1. **O1 — mirror × orientation (the hypothesis arm).** 55 unsolved pages
   {0–49, 51–55}; mirror pairing (k, 55−k) → 28 nominal pairs, minus
   (5, 50) since p50 is runeless → **27 pairs**, no self-mirror (55 odd,
   27.5 not a page). Per pair: 8 orientation classes × {diff (M,N), diff
   (N,M), sum (M,N), sum (N,M)} = 32 directed scans (sum both orders per
   the mask correction above). Instrument unchanged: core.kernel
   pair_scan semantics, MIN_LEN 50, record floor 40, tgt mask primary /
   both for confirmation, all offsets both directions.
2. **O2 — all ordered pairs, id-only (CONTROL arm).** 55×54 ordered diff +
   55×54 ordered sum = the #1/#2 space re-run as a positive control (sum
   ordered per the mask correction — a superset of #2's coverage): it must
   REACH their maxima (same corpus modulo relabel labels). If it doesn't,
   the harness changed and O1 results are void. Declared: O2 is calibration,
   not a second fishing license; its flags are reported but carry no
   new-hypothesis claim.
3. **T1 — token↔token mirror.** p49 (80 tokens) and p51 (72) base-60
   tables as byte streams (canonical bytes — at the split cell idx 246 the
   shipped `canon_256.bin` reads **0xc6** (3I), matching our pixel
   adjudication and the owner read; the CAMPAIGN-VII doc hex and
   `canon_256_superseded.bin` carry the old 0xe0 (3i, root+relikd), and
   re-running canonicalize.py on the pinned witness lineage also yields
   0xe0 — dukotah doc/bin drift, disclosed. BOTH variants scanned
   (`canon` = shipped bin, `e0` = dissenting-witness reading), flagged in
   CSV, no cherry-pick), mod 29 into the 29-bin space; p50's 104 tokens as
   pad candidate against both; diff both orders + sum; orientation classes
   on the token grids (8 rows/cols structure: rl = row order, rg = within
   row). MIN_LEN 50 bytes.
4. **T2 — token→rune affine bridge.** T1 bytes as pads for every unsolved
   rune page: D = A − (a·(T mod 29) + b) mod 29; b is constant → excluded
   by shift-invariance (declared); a ∈ 2..28 (a=1 = direct bridge; a=0
   constant → excluded). All offsets; id orientation only (pads are flat
   byte streams; token-grid orientations live in T1).

Windows ≈ 0.36M (O1: 27 pairs × 32 directed scans × ~420 offsets) +
~2.5M (O2) + <0.1M (T1/T2) ≈ **3M windows** — exact counts reported.
(The design doc's 2×10⁷ estimate predated the collapse declarations and
the mirror restriction.)

## Null (family-specific MC of the max — orientations INCLUDED in the max)

Target-shuffle per family, 20 draws, seed **20261126**, resumable
checkpoint, house pattern: per draw every unsolved page is permuted
independently (rune marginal preserved), the FULL family scan reruns —
all pairs, all 8 orientation classes, both ops — and the family max is
collected. The max is taken **including orientation and pairing choices**:
orientation is part of the hypothesis space, so per-class p-values would
be a multiple-comparison lie (the #3→#4 lesson, and the #5 family-null
rule). O2's null is its own (different pair set). Self-pair exclusion is
automatic (no pair has M=N); the #6-W fixed-point channel cannot arise
(distinct pages, no cyclic index consumption).

Escalation rule (unchanged): family obs ≥ its 20-draw null median →
≥ 200 draws on the same seed stream before verdict.

## GO prongs (all required)

1. obs > 1.1 × family null max (20 draws);
2. mask=both survives with n ≥ 50;
3. decode of the winning window (fwd AND reversed) yields English/cribs
   (25-crib house list);
4. (bonus, not required) the same orientation+pair scheme hits a second
   pair.

## Power

Per family: 10 plants, seed **20261127**. Plant = choose a pair, an
orientation class, an offset; set the pad so the planted window decodes to
crib English; recovery requires the planted row to be the FAMILY max on
the planted pair AND χ² ≥ family null median. Report coverage × power per
family; unprobeable reported as such. O2 plants verify the control arm's
sensitivity; O1 plants additionally verify orientation plumbing (a plant
in class (rg, id) that only surfaces under (id, id) is a bug, not a find).

## Degeneracy pre-checks (pre-output)

- Collapse identities verified (above) — output-blocking.
- p50 exclusion asserted; stream line lengths per page sum to page totals
  (validate.py already gates this).
- Per-class D-zero-fraction vs 1/29 + mask baseline; any class > 0.15 must
  be mechanistically explained before the sweep counts (#6 scar tissue).

## Cost (estimate at registration; measured figure goes in REPORT)

Scan ~2.5M windows: pair_scan is vectorized per offset — local < 2 min
(#8 measured 2 s for 37M positions of its shape; O2 dominates here).
20-draw null ≈ 48M windows: local if < 10 min, else scripts/studio.sh
(28 cores, bit-identical RNG streams). Escalation 200 draws ≈ 10× null.

## Not covered (disclosed)

Columnar/transposed reads (grid columns — orientation is line/glyph
reversal only); boustrophedon (tried in dukotah red_team, English-only
instrument); triple products; position-dependent pad derivations;
interleavings; **literal word-sum U3 — deferred to #10** pending the
transcription audit's divider-fidelity pass (only p51 dividers are
independently verified so far; #8 amendment); red-digit/red-matrix
selection channels (census is descriptive; become hypothesis space only
if the owner's double-check confirms the reads — future campaign);
ornaments; mid-range cyclic steps (#6); LP1-as-target; p50 as TARGET
(runeless — it appears only as pad source in T1).
