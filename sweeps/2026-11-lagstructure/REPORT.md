# Campaign #31 REPORT — full-lag key-reuse/structure scan: CLOSED-NOLAGSTRUCTURE

Registered before output: PREREG `17185d8` (no statistic at registration).
Owner green light 2026-11-19. Local run 256 s (12 workers), seed 20261231.
Registered rule applied verbatim.

## What was swept

T = max over lags ℓ ∈ [41, 12823] × {difference, sum} of χ²-vs-uniform
(29 bins) of (c[t+ℓ] ∓ c[t]) mod 29 — one statistic simultaneously
covering, by registered algebraic reduction:

- **periodic keys** of every period 41…12823 (key cancels at ℓ = P),
- **plaintext-autokey** every lag 41…6400+ (diff at ℓ = p[t]−p[t−2ℓ]),
- **ciphertext-autokey** every lag 41…12823 (diff at ℓ = p[t] exactly).

New coverage over both prior ledgers: **lags 6479–12823** (dukotah XIV
stopped at 6478; ours previously L1–40 + #29 lag caps 24/64). This is
where Wulfic's unverified "periodic to 11,781" claim sits.

## Result

| quantity | value |
|---|---|
| T_obs | **67.8** at ℓ*=11248 (sum family) |
| permutation null (D=2,000) | median 69.0, max 93.0, c95 = 76.6 |
| p | **0.618** — T_obs is *below the null median* |
| weak cells | none (all detectability gates pass) |

**VERDICT: CLOSED-NOLAGSTRUCTURE.** No key-reuse or lagged-plaintext
structure at any lag from 41 to 12,823, under either sign convention,
with full power. The corpus is *less* lag-structured than random
permutations of itself — the only structure the difference families
know about is the adjacency (lag-1) doublet hole, outside the band.

## Power curve (fraction ≥ c95, 20 draws/cell)

- periodic: 1.00 at every grid lag 41…12400; 0.15 at 12823 (n=132,
  predicted fade, outside the registered detectability band ≤12400).
- CT-autokey: **1.00 at every grid lag 41…12823** (plaintext-unigram
  signature is blatant).
- PT-autokey: 1.00 at 41…6400 (both signs).

## Cross-ledger adjudication (F18(ii))

- **Wulfic "periodic to 11,781":** tested directly by our instrument at
  that lag (power 1.00) — **absent**. Claim neither copied nor needed:
  the band is now closed in two independent ledgers (dukotah ≤6478,
  ours 41–12823 with a stronger statistic).
- **Wulfic "autokey to 12,863":** vacuous as stated (seed-pad
  remainder), and every non-vacuous large-lag autokey variant is now
  closed by this scan (CT: full band; PT: to 6400, power-faded beyond).
- **Wulfic "restarts per section/line/page":** refuted by measurement
  (dukotah §6b boundary doublets 0.0000; #18; #30 interior window) —
  not re-tested here.
- **Residual F18(ii) debt:** Leo-Y-Zhang / TheronEagle / jens-wedin
  ledgers unreachable this session (web proxy dead) — disclosed, open.

## Validation & disclosed defects (all pre-output, gates-first)

- G1 core.validate PASS; G2 census (86 doublets, unigram χ² 26.4);
  G3 FFT-vs-brute 200/200 exact.
- **Gate-caught defects (disclosed, #26 style):** first two runs died
  IN G3 before any output — (1) `rfft` taken at signal length while
  `irfft` requested NFFT (zero-pad in frequency ≠ time); (2) exact
  float==int comparison in the gate. No statistic was computed under
  either defect; fix commits precede the run that produced results.

## Limitations (PREREG §6 + report)

Unfiltered plants (perturbation ≤0.02% of samples, bounded); PT-autokey
sign −1 3-term form weaker (plant cell still 1.00); last ~100 lags
power-faded for the periodic family only; English-register power
calibration (measured, unlike dukotah's L7-A caveat); short band
41–6478 re-covers dukotah XIV — agreement (both null) is cross-ledger
calibration.

## Reproduction

    python3 -m core.validate
    python3 sweeps/2026-11-lagstructure/lag31.py        # ~4 min, 12 workers

Tracked: results/lag31.json (small). Seed 20261231.
