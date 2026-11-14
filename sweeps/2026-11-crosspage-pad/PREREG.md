# PREREG — 2026-11-crosspage-pad

> **STATUS: RETROACTIVE.** This pre-registration was written on 2026-11-14, *after*
> the sweep it describes was run and reported. It documents what was actually
> pre-committed to nothing; it is disclosed here rather than hidden, per the repo
> rule that the gate enforces existence and the report enforces honesty. Campaigns
> after this one register before their first output.

## Hypothesis

Some unsolved LP2 pages were enciphered with **another LP2 page's ciphertext as a
running pad**: `C_M[t] = (P_M[t] + C_N[t−o]) mod 29`. At the true (M, N, o),
`D = (C_M − C_N) mod 29 = P_M`, whose 29-symbol histogram is non-uniform
(language-agnostic — no English adjudication at the statistic level); wrong
alignments are uniform.

Motivation: dukotah `ruled_out` "page-on-page key reuse" covered only the
shared-keystream variant (c1−c2 = p1−p2, English-minus-English IoC) at offset 0
(ARMADA FOLLOWUP-TESTS #4); their FINAL-VERDICT #4 recommended the full-offset
sweep and it had never been run.

## Search space (as run)

- Targets: LP2 0–54 (55 unsolved pages, 12,956 runes). Page 55 untranscribable (all lineages).
- Pads: 57 ciphertext streams (0–54, 56 AN END, 57 PARABLE) + 2 solved plaintexts.
- Orientations: fwd, rev (complete: target-reversal is a χ² no-op); mirror set
  N‖rev(N), rev(N)‖N counted only in junction-straddling windows.
- Offsets: all with n_valid ≥ 50 after ᚠ-masking (primary: target-side F only,
  alignment-safe; sensitivity: both-side per handoff).
- Total: 3,798,361 windows.

## Instrument and calibration

χ² vs uniform over 29 bins + IoC per window. Null: 20 in-page rune shuffles of
every target (preserving lengths, symbol frequencies, F density), identical sweep
machinery, global max per shuffle. Seed 20261113. Bonferroni sanity band χ²≈92.2
(known anti-conservative for correlated windows; MC is the decision instrument).

## Decision rule (as applied)

GO iff observed max χ² > 1.1 × MC null max **and** the top hit survives mask=both
**and** the window decodes with English cribs (readability check).

## Result

NEGATIVE. Observed max 111.6 (self-mirror, p≈0.10 vs null max 118.8); best
cross-page 86.4 < null median 99.0; decode garbage. Details: REPORT.md.
