# Campaign #27 — REPORT: key-consumption discriminator scan

Run 2026-11-19. PREREG committed before output (c0ec6ca) + dated SD-correction
addendum (see Disclosures). Owner-approved escalation of #26-A1 (SEPARATES).
Seed 20261227. Runtime ~3 s local (not days; studio rule untouched).

## Verdict (verbatim): **UNINFORMATIVE**

Rule: NO-EXCESS requires both variants p ≥ 0.025 **and** power bar 19/20;
"NO-EXCESS with failed power bar: UNINFORMATIVE." Both p's clear the flag,
but detection on redraw plants came back 6/20 (V1) and 9/20 (V2).

## Results (corrected statistic, seeds unchanged)

| variant | Z | p (normal) | p (bootstrap 10k) | α̂ ± sd |
|---|---|---|---|---|
| V1 solved-LP English | +0.24 | 0.405 | 0.397 | +0.006 ± 0.024 |
| V2 quadgram | +1.46 | 0.072 | 0.075 | +0.034 ± 0.023 |

Normal and bootstrap p now agree (they disagree by construction with the
pre-addendum SD — see Disclosures). Descriptive: V2's α̂ = +0.034 ± 0.023 sits
at the redraw prediction (α ≈ 0.036 hidden rejects ≈ 463 at 1/28 reject rate;
reviewer's ≈ 374 by 0.19-leak arithmetic) but is only 1.5σ from zero — with
detection power this low, that alignment is noise-compatible and is NOT
promoted.

## Why the power bar failed — the real finding

The emitted-level redraw signal is a ~3% mixture of the English
letter-difference distribution into an otherwise EXACT uniform (mod 29)
difference stream. But English difference distributions mod 29 are themselves
nearly uniform: Σ(π_E−u)²/u ≈ 0.15 (V2), smaller for solved-LP English (V1).
Single-stream signal-to-noise is therefore Z ≈ α·sqrt(N·χ²_π) ≈ 0.036·
sqrt(12,869·0.15) ≈ 1.5 — far below the 1.96 flag, matching the measured
9/20. #26 A1's two-sample separation (p = 1.5e-18) compared 2,000 streams per
idiom: it detected a consistent MEAN-SHIFT of the dc statistic across
replicates. Theoretical identifiability (distributions differ) ≠ practical
decidability from ONE 12,956-rune stream. No emitted-level statistic of this
family can settle key consumption on this corpus; a sharper discriminator
would need structure below the emitted level (e.g., key-hypothesis-conditioned
decodes — the prefilter-power story), or more data.

## Consequences

- Decoder class: the key-consumption question stays OPEN; skip-tolerant
  remains the conservative default for power claims. The deferred
  #23/#24A/#25D MAP annotations (planned under MEMO-EQUIV/NO-EXCESS) are
  still NOT applied — UNINFORMATIVE is not "skip confirmed".
- The #26 power-first design rule pays for itself on its first reuse: the
  registered bar blocked both failure modes (false NO-EXCESS → skip, and
  any temptation to read V2's α̂ as signal).

## Disclosures (dated)

1. **Registered SD formula was wrong (addendum, pre-verdict):** PREREG's
   sd = sqrt(N·Σu·w²) omitted the multinomial covariance; correct
   Var(T) = N·Σw²/u (28× larger variance). The registered bootstrap
   (exact-null calibration) exposed it on the first run (Z_normal 40.9 vs
   p_boot 0.075); the registered α̂ SE already used the correct variance —
   the file was internally inconsistent. Corrected, re-run with unchanged
   seeds; first-run bootstrap p's are bit-reproducible and stand.
2. The first (pre-correction) run printed "REDRAW-EXCESS" under the inflated
   Z — that line is VOID: no verdict may issue when the analytic null and the
   registered exact-null calibration disagree; the corrected run governs.
   (Recorded here, not deleted.)
3. Power bar evaluated only under the corrected statistic (the first run's
   17/20, 17/20 were computed under the inflated Z and are likewise void).

## Reproduction

    python3 -m core.validate
    python3 sweeps/2026-11-discriminator/scan.py
    # artifact: results/discriminator.json
