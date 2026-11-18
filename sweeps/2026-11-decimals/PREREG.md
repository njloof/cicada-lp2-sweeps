# Campaign #20 PREREG — p15 decimal grid as selector (MAP slot 9)

Registered 2026-11-17, BEFORE confirmatory output (CI gate). Owner
approved ordering (decimals before 6c crib design). Objects: p15's 4×4
printed digit grid, rows 3278 / 3299(red; dukotah R18-H9 measured
lighter ink tone min-grey 47-51 vs 0.0 elsewhere — the SAME channel our
owner transcribed by eye as red `*`) / 3298 / 2838. 3299 = prime
immediately preceding 3301 (dukotah note, verified here). Axis
AXIS-ALIGNED (#19). Context findings from the DESIGN PASS (disclosed
post-hoc origin; confirmatory value = reading space enumerated before
any registered test ran, but B1-B3 were observed during design):
all four rows lie inside the T7 void [2740,4389] AND inside the pre-axis
span [1874,3602]; digit sums = {20,21,22,23} distinct consecutive;
3298 = 2×1649 where #10 QUOTED the void as 1,649 (exact span 1,650 —
caveat disclosed, numeric flag gets no p).

## 1. Battery (Holm across B1-B5, alpha 0.05)

- **B1 void containment (post-hoc origin):** all four decimal values
  inside void [2740,4389]. Null: 4 uniform draws without replacement
  from 12,956. p = C(1650,4)/C(12956,4) analytic.
- **B2 pre-axis span containment (post-hoc origin):** all four inside
  [1874,3602]. Same null, K=1729.
- **B3 digit-sum consecutiveness (post-hoc origin):** sums of the four
  rows are distinct with range exactly 3. Null: 4 random 4-digit rows
  (lead digit 1-9, rest 0-9), MC D=200,000, seed 20261220.
- **B4 doublet hits at 0-based positions (a priori):** count of
  {3278,3299,3298,2838} that are doublet sites. Null hypergeometric
  (86 sites). Observed 0 -> NO p-value by design (one-sided test aims
  at excess; 0 hits = null result, power disclosed: P(>=1)=0.026).
- **B5 doublet hits at 1-based positions (a priori):** same, shifted.

Descriptive (no p): transliterations at R1 0-based (UOEWT), R2 1-based
(OWGEA), R3 Q3a-local (ACUO), R4 digit-sums-as-p15-positions (IUIU);
3299 prime + ink/red double-mark; 3298 = 2×1649 (1649-vs-1650 caveat).

## 2. Gates

G1 N=12,956; G2 grid rows == owner/krisyotam record (3278/3299*/3298/
2838, 3299 marked); G3 void span = 1,650 (sites 2740/3140/3852/4389).

## 3. Verdict rule (pre-output)

- DECIMALS-STRUCTURED: any of B1-B3 survives Holm -> decimals carry
  structural signal; FLAG FOR CONFIRMATION (independent prediction
  required before adoption; post-hoc origin disclosed).
- DECIMALS-NULL: none survives -> decimal-as-position family retired
  in-CD (consistent with #15 retiring digits 1-5), power disclosed.
- B4/B5 can only contribute nulls (observed 0 hits).

## 4. Runtime

MC 200k + analytic: < 30 s local. No studio.
