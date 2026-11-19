# Campaign #27 PREREG — key-consumption discriminator scan (owner-approved 2026-11-19)

Registered and committed BEFORE any corpus statistic is touched. Escalation
branch of campaign #26 (PREREG §A1: "Verdict SEPARATES … follow-up
discriminator design goes to owner BEFORE any scan"). Owner approval of the
scan received 2026-11-19 ("Welcome to run A1 discriminator scan"); design is
that scan. Seed 20261227. Runtime: seconds-local (not days; owner's
studio rule untouched).

## Hypotheses (emitted-level, flat-key idealization — disclosed)

- **H_skip** (null): anti-doublet rejects consume key (dukotah key-skip) or
  replace uniformly ⇒ every adjacent pair is i.i.d. uniform over the 28
  non-predecessor values ⇒ the consecutive-difference distribution is EXACTLY
  uniform on 1..28 (any plaintext, any flat key).
- **H_redraw** (alt): rejects resample PLAINTEXT with the key HELD ⇒ the
  post-reject difference equals a plaintext letter-difference (the held key
  cancels) ⇒ ~α ≈ 374/12,869 ≈ 2.9% of pair-differences follow the English
  difference distribution π_E, the rest uniform. (Reviewer round-3 arithmetic:
  hidden rejections ≈ N·qs/(1−qs) ≈ 374.)

#26 A1 established separability (p = 1.5e-18 in simulation, omnibus dc_chi2);
this scan is the corpus test.

## Statistic (pre-specified, one-sided, directional — NOT an omnibus re-run)

Observed: d_t = (s[t] − s[t−1]) mod 29 over the 12,955 adjacent pairs of the
pinned unsolved stream, EXCLUDING the 86 zeros (observed doublets, leak);
N ≈ 12,869 nonzero diffs, counts n_d, d = 1..28.

Direction w = π_E − u (u = uniform on 1..28). Score statistic

    T = Σ_d (n_d − N·u_d) · w_d / u_d ,      Z = T / sqrt(N · Σ_d u_d w_d²)

p = one-sided normal upper tail (exact multinomial null; 10,000 multinomial
bootstrap draws as a consistency check, reported descriptively). Mixture
weight α̂ reported by 1-D projection (descriptive).

**Two pre-specified π_E variants, Bonferroni 2 (flag if p < 0.025):**
- **V1 (primary): solved-LP English.** Rune-index difference distribution of
  the solved LP1 plaintext streams (the ten gated sections, decoded with
  THEIR OWN verified methods, hold convention — interrupter F's kept as
  letters, per LEDGER C7); within-page consecutive diffs only, zeros excluded.
  This is in-domain English (the koan register of the corpus itself).
- **V2: quadgram sampler.** Difference distribution of the #26 A1
  English-quadgram sampler stream (seed-pinned, bit-identical to A1's
  sampler), zeros excluded.

Prediction: H_redraw ⇒ Z large positive in BOTH variants (correlated tests;
Bonferroni is conservative by construction). H_skip ⇒ Z ~ N(0,1).

## Gates (before any corpus statistic)

- G1 `python3 -m core.validate` full local pass (mandatory suite).
- G2 corpus pins: L = 12,956; doublets = 86; nonzero diffs = 12,869.
- G3 π_E sanity: V1 stream length = 2,798 runes total across the ten sections
  (fixed-parser count); V2 sampler reproduces A1's first stream's first 50
  indices (seed-pinned check).

## Power (registered FIRST per the #26 lesson — detectability is a gate)

20 plant streams per variant: #26 A1 redraw-idiom emissions (L = 12,956,
house seeding), score under the SAME statistic. Detection = p < 0.025.
Bar: ≥ 19/20 per variant, else verdict NO-EXCESS is UNINFORMATIVE (never
"skip confirmed"). Expected: very high — A1's omnibus separated at 1.5e-18
and this test uses the known direction.

## Verdicts (verbatim)

- **REDRAW-EXCESS** (any variant p < 0.025): plaintext-redraw-with-held-key
  supported for the corpus filter; decoder class = redraw-tolerant; report to
  owner before any MAP/LEDGER promotion of downstream power claims.
- **NO-EXCESS** (both p ≥ 0.025) AND power bar met: corpus consistent with
  key-skip / uniform replacement at emitted level; skip-tolerant decoder
  class adopted; #23/#24A/#25D power claims get their deferred MAP
  annotations (skip-tolerant columns).
- **NO-EXCESS with failed power bar**: UNINFORMATIVE.

## Disclosed limitations

1. Flat-key idealization: a STRUCTURED keystream can also bend the difference
   histogram; NO-EXCESS does not prove key-skip, and REDRAW-EXCESS would need
   a structured-key null re-check before promotion (registered as a
   mandatory follow-up, not a caveat).
2. π_E proxies LP2's unknown plaintext with solved-LP English / quadgram
   English; misspecification dilutes but does not bias the null (null is
   exact regardless of π_E).
3. The 86 leaked doublets are excluded as zeros; their idiom is out of scope.
4. One corpus, one scan; no variants beyond the two registered π_E; no
   windowed/subset rescans without new registration.

## Execution

    python3 -m core.validate
    python3 sweeps/2026-11-discriminator/scan.py        # seconds, local
    # artifacts: results/discriminator.json, REPORT.md

## Addendum (2026-11-19, after first scan run, before verdict): registered SD formula corrected

The registered sd = sqrt(N·Σ u·w²) is WRONG: it omits the multinomial
covariance. Correct: Var(T) = N·Σ w²/u (the covariance term collapses since
Σw = 0) — the registered sd was 28× too small. The bootstrap (registered as
the exact-null calibration) exposed it immediately (Z_normal=40.9 vs
p_boot=0.075 on V2), and the registered α̂ standard error already used the
correct variance — the file was internally inconsistent. First run therefore
produced no verdict beyond the bootstrap; corrected run governs, seeds
unchanged. Hypotheses, direction, variants, flag level, power bar, and
verdict wording are UNCHANGED; the bootstrap p's from the first run are
bit-reproducible and stand as computed.
