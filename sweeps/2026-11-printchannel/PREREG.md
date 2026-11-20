# Campaign #32 PREREG — print channels wave 1: glyph metrics + value-dependence (MAP F25)

Registered 2026-11-19, BEFORE any campaign output (CI gate). Owner lane
pick 2026-11-19 (verbatim): "Let's continue down the live lanes, F19
Track B is as good as any."

## 0. Mandate and dup position

External review Track B (~25% weight): machine-measured print channels.
dukotah R44 covered stego/geometry/chroma/font-variants/bar-units 8–19;
their own wording leaves **sub-2-pixel placement and kerning NOT
excluded**. P3-punct-channels (their round 44) is punctuation/quotes —
disjoint. Our niche: language-agnostic association tests between what
was WRITTEN (rune values) and how it was PLACED (print geometry).

Wave 1 (this campaign): metrics table + two registered tests.
Wave 2 (deferred, needs wave-1 asset): line-break residual model.

## 1. Objects and inputs

- **Images:** onion-original pages 0–55 from Internet Archive item
  `ky2khlqdf7qdznac.onion` (`<n>.jpg`, ~33 MB). **Gate G0: sha1 must
  match dukotah `analysis/stego/provenance.json` for every page they
  verified (56 rows); byte-exactness is the precondition for any
  sub-pixel claim.** Stored in `work/` on studio (never git).
- **Transcription:** krisyotam canon with line structure
  (`data/pages/lp2_*.txt`), 13,136 runes incl. solved p50; unsolved
  corpus 12,956 as usual.
- **Component extraction:** grayscale, Otsu binarization (fixed
  threshold registered after inspecting page-0 histogram — PRE-OUTPUT
  calibration only, no test touched), `scipy.ndimage.label`, components
  grouped into transcription lines by y-band matching page line
  structure; per-line alignment: component count == line rune count ⇒
  clean; else split-by-vertical-projection once, else line EXCLUDED
  (coverage disclosed). **Gate G1 (fidelity): ≥95% of the 12,956
  unsolved runes aligned; per-page coverage table persisted.**
- **Metrics per aligned rune** (registered set, 8): sub-pixel centroid
  fractional parts (fx, fy), centroid (cx, cy), bbox width/height, ink
  area, ink density (area/bbox), kerning gap to previous rune in line.
  Within-line z-scores used in tests (kills page/line position
  confounds).

## 2. Registered tests (both language-agnostic)

- **T1 value↔metric association.** For each metric m: eta-squared of
  within-line z(m) grouped by rune value (29 groups), summed over lines.
  T1 = max over the 8 metrics. **Null: permute rune-value labels within
  each line** (D = 2,000; preserves ALL spatial structure — component
  order, spacing, geometry — and destroys only value↔geometry coupling;
  this is the exact null for "does the print encode the value").
  p = add-one on the max-statistic.
- **T2 sub-pixel placement uniformity.** Rayleigh R of frac(cx) over
  all aligned unsolved runes (mod-1 fractional part; circular). Null:
  analytic uniform (large-n Rayleigh p) + MC cross-check (D=20,000).
  R reported with the p.

Multiplicity: T1's null covers its metric family; T2 is one test.
Bonferroni ×2 across {T1, T2} for the FLAG threshold.

## 3. Plants (power curve FIRST)

Inject into the REAL table (spatial structure untouched): value→metric
mappings on the metric with the strongest registered role:
(i) z(m) += eps·(value−14)/14, eps grid {0.02, 0.05, 0.10, 0.20};
(ii) frac(cx) = (value/29 + jitter·U) mod 1, jitter grid {0.1, 0.3, 1.0}
(T2 class). 20 draws/cell. Power at the registered alpha. Detectability
gate: power ≥ 0.95 at eps = 0.10 (T1) and jitter ≤ 0.3 (T2), else the
respective test is UNPOWERED and its negative is not informative.

## 4. Gates

- **G0** image sha1 == dukotah provenance, every verified page, EXACT.
- **G1** alignment fidelity ≥95% unsolved runes; coverage table saved.
- **G2** machinery: on 3 random lines, brute-force centroid/area by
  pixel loop == pipeline output (tol 1e-6); line y-band grouping
  reproduces the transcription's per-page line rune counts.
- **G3** core.validate PASS (corpus cleared).

## 5. Verdict rule (registered, applied verbatim)

- **FLAGGED** — min(p_T1, p_T2) ≤ 0.025 (Bonferroni ×2). Print channel
  finding = flag-for-oracle (human adjudication required before any
  claim; a machine-measured geometry association is not "a reading").
- **CLOSED-PRINTNULL** — otherwise AND both detectability gates pass.
  Wording carries: closed for VALUE-DEPENDENT geometry at plant-
  calibrated strength; value-INDEPENDENT channels (global drift,
  justification rhythm, T7-like process artifacts) are NOT addressed by
  these tests and remain open by disclosure.
- **UNPOWERED-NULL** — otherwise.

## 6. Disclosures (pre-output)

1. JPEG is lossy: sub-pixel claims carry JPEG-compression noise; the
   null (permutation within line) is computed on the SAME pixels, so
   test validity is unaffected — but a FLAGGED would need PNG-source
   confirmation before interpretation.
2. Hand-written runes: component↔rune alignment errors are the main
   instrument risk; G1 coverage + excluded-line list disclosed; T1's
   within-line z-scoring means a mis-split line dilutes, not fakes,
   signal (permutation null keeps the same alignment).
3. Red marks/ornaments excluded from rune components (luminance
   channel + line-band gating); they are wave-2/oracle objects.
4. Compute on studio per owner rule (ETA > 2 min): download+verify,
   extraction, nulls; table pulled back small (top-K + sha256 + regen
   command in results/, full table in work/ per repo hygiene).
5. p50/p56/p57 images downloaded for provenance completeness; tests run
   on unsolved pages only.

## 7. Machinery

`acquire.py` (download + sha1 receipt), `table32.py` (extract → table +
G1/G2), `tests32.py` (plants → nulls → T_obs → verdict). All under
studio via scripts/studio.sh. Seed 20261232.
