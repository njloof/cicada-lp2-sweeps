# Campaign #9 (design notes — NOT yet preregistered)

_mirror-pair product space × reading-orientation group_ · drafted 2026-11-15,
owner-requested orientation axis. Book page numbers throughout (post-relabel,
`2089fc2`). PREREG.md must be committed before any output (CI gate); this doc
is design only.

## What prior campaigns covered / what is new here

#1–#5, #8 scanned page pairs under id orientation: difference, sum, scaled
(`k·C_N`), stride, index-consumption. **The reading-orientation axis was never
scanned**, and neither was the mirror-pair restriction with orientation.

## Orientation group (owner: "bottom right to top left? reverse line orders?
reverse glyphs within each line?")

Page = line grid. Four read transforms, applied **independently to each page
of a pair** (16 combos, collapses declared in PREREG):

| id | lines | glyphs within line |
|----|-------|--------------------|
| `id` | top→bottom | left→right |
| `rl` | **bottom→top** | left→right |
| `rg` | top→bottom | **right→left** |
| `r180` | **bottom→top** | **right→left** (true bottom-right→top-left corner read) |

Declared-collapse candidates to verify pre-run (χ² is reversal-invariant):
`r180` on BOTH pages of a diff/sum pair permutes the difference sequence →
identical stat to `id`/`id` — if confirmed, 16 combos collapse to 4 per
symmetric op (declare, don't discover). `rl` is NOT a sequence reversal when
line lengths differ — genuinely new. Line-grid structure must be preserved
from the stream (we have it; `data/pages/` keeps lines).

## Pairings

1. **Mirror pairs (owner's first↔last idea):** `(k, 55−k)` over unsolved book
   pages 0–49 + 51–55 → 27 pairs + self-mirrors; both orientations of each
   pair (M,N)/(N,M) for non-commuting ops.
2. **All ordered cross pairs** (55×54) as the completeness arm, id-only, so
   the mirror arm stays a hypothesis, not a fishing license.
3. **Token↔token mirror:** p49 vs p51 base-60 tables (byte streams, 80+72
   tokens; p50's 104 tokens as pad candidate vs both).
4. **Token↔rune:** p50/p49/p51 token bytes vs rune streams (p7 lead from
   earlier notes) — different alphabets; affine bridge `a·T+b mod 29` declared.
5. **Ornament cross-mirrors:** dukotah round-43 leads 6/8 (parked; blocked on
   ornament transcription — likely stays out of #9).

## Ops and instrument

- Ops: `C_M − C_N`, `C_M + C_N`, affine `a·C_M + b·C_N` (a,b ∈ 1..28, declared
  collapses for symmetry), ᚠ-mask both conventions, all offsets both
  directions, n ≥ 50 — same instrument as #1–#8 (χ² language-agnostic).
- **Null: family-specific MC of the max** (target-shuffle), 20 draws +
  escalation rule; orientation choices are part of the scan ⇒ the null must
  take the max over orientations too (else p-values are a multiple-comparison
  lie). Self-pair exclusion per the #6-W lesson.
- Power probes: planted English window per family; report coverage × power.
- Rough size: 2970 pairs × 16 orientations × 2 ops ≈ 95k units × ~200 offsets
  ≈ 2×10⁷ windows before collapse declarations — studio offload via
  `scripts/studio.sh` if needed (bit-identical RNG streams).

## Separate family (unblocked, keep in #9 or split to #10)

Literal **word-sum self-keys (U3)**: word dividers `-` verified present in the
pinned stream (LEDGER footnote #8); line-sum LS was #8; word-sum is the
untested sibling. Derive-from-shuffled null (per #8's method win).

## Explicitly NOT covered (declare in PREREG)

Columnar/transposed reads (grid columns), boustrophedon (tried in dukotah
red_team, English-only), triple products, position-dependent pad derivations,
digit/ornament channels except as tabulated by the red/digit census
(docs/RED_CENSUS.md), LP1-as-target.
