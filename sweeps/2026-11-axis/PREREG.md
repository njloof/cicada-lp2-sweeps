# Campaign #19 PREREG — p15 axis reading: void-centering test + v2 re-power (MAP 6d/queue slot 8)

Registered 2026-11-17, BEFORE any campaign output (CI gate). Owner
approval 2026-11-17 (verbatim): "I'm open to proceeding with the p15
axis reading and see where it takes us -- that, and pick up the queue at
#19." Context: campaign #18 tested the 10-group v1 segmentation
(NO-GROUPS-EVIDENCE, 0 REFUTES, LEDGER 18); owner round-7/8 notes +
terminator map produced v2 (7 groups + nestings, SEGMENTS.md, 4d44c21);
doublet-sensitive rerun (83a1b0d) found the T7 void roughly CENTERED on
the p15 decimals/infinity axis (post-hoc lead; this campaign makes it
the confirmatory test).

## 0. Objects

- Stream = pp00–55 book order, p50 skipped, 12,956 runes (0-based
  positions, #18 convention).
- **Axis junction** J = midpoint between last rune of p15 line 0 and
  first rune below p15's `&`/`$` lines (the & sits after L0, 9 runes;
  J computed from data, gate G4 pins it).
- **Void** (campaign #10, replicated #18): doublet-SPARSE span, internal
  doublet sites 2740/3140/3852/4389; gaps 400/712/537; largest gap 712
  between sites 3140 and 3852.
- Doublets: adjacent equal runes, 86 corpus-wide.

## 1. Registered statistics

**V1 — largest-gap center vs axis (PRIMARY).** Statistic: d1 =
|midpoint of the largest inter-doublet gap − J|. Observed gap = 712
(sites 3140–3852). Null: permute the 86 doublet sites uniformly over
positions 1..12955 WITHOUT replacement (D = 20,000, seed 20261219),
recompute largest-gap midpoint and d1. p = (count d1_perm <= d1_obs +
1)/(D+1). DIRECTIONAL: small p = void structure centered on the axis
consistent with the owner's reading; large p = centering was luck.

**V1b — fixed-span center vs axis (secondary, analytic).** Statistic:
d2 = |midpoint of #10's span [2740, 4389] − J|. Null: uniform placement
of a 1,650-rune span over the stream; p = P(|center − J| <= d2_obs)
analytic (edge-corrected).

Multiplicity: Holm over {V1, V1b}, alpha = 0.05.

**V4 — v2-unit homogeneity (report-only, non-falsifying).** Sentence-dot
density and word-length chi-square across the 11 v2 units (Q1, Q2, Q3a,
Q3ax, Q3b, Q4, Q5, Q6, Q7a, Q7b, Q7c) vs permutation nulls as #18 S3/S4
(D = 20,000, same seed). Homogeneity expected from the exploratory run;
this re-powers #18's S3/S4 on the v2 partition. No verdict weight.

Descriptive (no p-values): axis-excluded segment lengths (1729/1744 raw,
1720/1734 doublet-collapsed); doublet mirror 0/10 (from 83a1b0d,
confirmed by construction).

## 2. Kill gates

- G1 stream L = 12,956 EXACT; v2 partition + subsections reproduce the
  SEGMENTS.md table exactly.
- G2 terminator map EXACT: page-end &/$ pages = {2,7,14,22,26,32,39,49,
  53,55,56,57}; p15 &/$ mid-page; 86 doublets; void sites/gaps as #18 G3.
- G3 decoration-boundary agreement: all 7 v2 right edges (2,7,22,26,32,
  39,55) are page-end terminators (7/7). DISCLOSED: not independent
  evidence — krisyotam '&' lines and owner decoration notes record the
  same ornament channel; G3 tests transcription fidelity, not a new
  discovery.
- G4 junction J computed from data must equal 3611.5 +- 0.5 (p15 L0 = 9
  runes, p15 starts at 3603).

## 3. Verdict rule (registered pre-output)

- AXIS-ALIGNED: min(Holm-adjusted p over {V1, V1b}) < 0.05 -> void
  centering stands as a structural fact; axis becomes a tracked feature
  (no pipeline re-keying: #18 still governs group independence).
- NO-AXIS-EVIDENCE: otherwise -> axis stays a presentation frame only.
- V4 never changes the verdict (non-falsifying, per #18 S3/S4 rule).

## 4. Disclosures (pre-output)

- The void was localized in #10 BEFORE the axis existed; the axis is new
  (owner r8), so V1/V1b test a new prediction against old data.
- The exploratory per-unit panel (IoC/z/wlen/dots, 4d44c21) preceded
  registration; it is descriptive context, not confirmatory output.
- Largest-gap and fixed-span statistics are correlated (same 4 sites);
  Holm is conservative for 2 near-duplicate tests.

## 5. Runtime

20k permutations x 2 tests on 13k items: < 60 s local. No studio.
