# Campaign #31 PREREG — full-lag key-reuse/structure scan (MAP F24)

Registered 2026-11-19, BEFORE any campaign output (CI gate). Owner green
light 2026-11-19 (verbatim): "Green light."

## 0. Mandate — from the F18(ii) cross-ledger audit

- Wulfic's "periodic keys to period 11,781" sits in the band
  **lags 6479–12915**, scanned by nobody: dukotah Campaign XIV scanned
  book-wide coincidence for lags 1–6478 only (0 peaks >5σ); ours
  excluded periodic L1–40 (IoC/Friedman); dukotah's own correction says
  IoC-invisible periods start at p*≈400.
- Wulfic's "autokey to lag 12,863": at lag w only L−w runes are
  autokey-derived (rest = seed-pad, untestable per #28 L6) — vacuous at
  12,863 — but intermediate large lags (65..~12,800) were never scanned
  by our instrument (#29 capped w at 24/64, disclosed L3).
- Wulfic's restarts claim: REFUTED by measurement (dukotah §6b:
  boundary doublet rate 0.0000 at every boundary class; #18; #30's
  window interior to Q3). Not tested here.

## 1. The reduction (why one statistic covers three families)

Values mod 29; c = ciphertext, p = plaintext, all lags ℓ ∈ [41, 12823]
(n_ℓ = L − ℓ ≥ 132 samples).

- **Periodic key, period ℓ:** c[t+ℓ] − c[t] = p[t+ℓ] − p[t] (key
  cancels). Under H0 flat; under H1 the English pair-difference
  distribution (non-flat; zero-bin excess ≈ IoC 0.066 vs 0.0345).
- **Plaintext-autokey, lag ℓ, sign +1 (keyskip0):** for t ≥ 2ℓ,
  c[t] − c[t−ℓ] = p[t] − p[t−2ℓ] (seed and mid-term cancel). Effective
  samples L − 2ℓ → PT-autokey coverage stops at ℓ ≈ 6400 (disclosed).
- **Ciphertext-autokey, lag ℓ, sign +1:** c[t] − c[t−ℓ] = p[t] EXACTLY
  — the plaintext unigram distribution, blatant if present.

Sign −1 variants are covered by testing the SUM family alongside
(c[t+ℓ] + c[t]): for CT-autokey sign −1, c[t] + c[t−ℓ] = p[t]; for
PT-autokey sign −1, the sum carries the cancellation. Both families
registered: difference D_ℓ and sum S_ℓ for every lag.

## 2. Registered statistic and null

**PRIMARY: T = max over ℓ ∈ [41, 12823] and both families of**
χ²(counts of (c[t+ℓ] ∓ c[t]) mod 29 over 29 bins; expected n_ℓ/29).

- **Null:** value-permutation of the corpus stream (preserves observed
  unigram marginals exactly — conservative given corpus flatness),
  recompute T, D = 2,000 draws, seed 20261231, streams
  default_rng([SEED, crc32(tag)%100000, d]). p = (1 + #{T_perm ≥
  T_obs})/(D+1). Critical value c95 = 95th percentile of T_perm.
- Multiplicity (12,783 lags × 2 families, correlated) is handled by the
  max-statistic null; no other correction.
- Machinery: per-value indicator cross-correlations via FFT
  (C_ab[ℓ] = #{t: s[t+ℓ]=a, s[t]=b}); gate G3 checks FFT counts ==
  brute-force counts on random lags/bins before any output.

## 3. Plants and power curve (F21 — first, before real-data T)

Synthetic streams (Emerson essays values, book-internal file, plants
only, per #29 doctrine), unfiltered (disclosed §6.2):

- periodic: c = p + K, K = random period-ℓ key, ℓ ∈ {41,100,400,1000,
  2000,4000,6400,8000,10000,11781,12400,12823}, signs ±1;
- CT-autokey: c[t] = p[t] ± c[t−ℓ] (c[t<ℓ] = p[t]), same ℓ grid, ±1;
- PT-autokey: c[t] = p[t] ± p[t−ℓ] (c[t<ℓ] = p[t]), ℓ ∈ {41,100,400,
  1000,2000,4000,6400}, ±1.

20 draws/cell. Power(cell) = fraction with T ≥ c95. Power curve reported
over ℓ per family. **Detectability gate:** power ≥ 0.95 for every
periodic and CT-autokey cell with ℓ ≤ 12,400 and every PT-autokey cell
with ℓ ≤ 4000; any cell below bar → that family-band is reported
UNPOWERED and excluded from CLOSED wording.

## 4. Kill gates

- **G1** core.validate full pass (known-solutions regression).
- **G2** stream: L = 12,956; lag-1 zero-difference count = 86 (doublet
  census pin); unigram χ² vs uniform < 100 (flatness sanity).
- **G3** machinery: FFT cross-correlation counts == brute-force counts
  on 200 random (lag, bin) cells, EXACT.

## 5. Verdict rule (registered pre-output, applied verbatim)

- **FLAGGED** — T_obs ≥ c95. Adjudication before any claim: locate
  ℓ* (argmax) and family; decode the implied reading (CT-autokey:
  p̂[t] = c[t] − c[t−ℓ*]; periodic: report per-column structure;
  PT-autokey: report difference reading); crib test on the reading —
  ≥2 distinct letter-space cribs on one page = flag-for-oracle
  (standing bar); else report as structure-without-reading.
- **CLOSED-NOLAGSTRUCTURE** — T_obs < c95 AND every family-band passes
  its detectability gate. Coverage wording must carry the power curve
  and the three conditionals (§6).
- **UNPOWERED-NULL** — otherwise.

## 6. Disclosures (pre-output)

1. **Short-band overlap:** lags 41–6478 were coincidence-scanned
   book-wide by dukotah XIV (0 >5σ). Our scan re-covers them with a
   stronger statistic and our own null; agreement is expected and
   reported as cross-ledger calibration, not new coverage. NEW coverage
   = lags 6479–12823.
2. **Unfiltered plants:** the anti-doublet filter is not applied to
   plants. A filter-modified position (≤86 of them) perturbs the value
   c[t], which touches 2×12,783 of ~1.6e8 lag-difference samples
   (≤0.02%); it cannot manufacture or mask a max-statistic signal at
   ℓ ≥ 41. Deviation from the F21 filter-plant rule, quantitatively
   bounded here.
3. **PT-autokey** reduction needs t ≥ 2ℓ: effective coverage ℓ ≤ 6400
   (power curve decides); sign −1 handled by the sum family only for
   CT-autokey; PT-autokey −1 at lag ℓ leaves a 3-term form
   (p[t]+p[t−2ℓ]−2p[t−ℓ] in the difference) — weaker, plant-cell power
   decides wording.
4. Last ~100 lags (n_ℓ < ~150) are power-faded; curve disclosed.
5. Language-agnostic in form (any plaintext with IoC > 1/29 shows);
   power calibrated on English plants (the registered register,
   disclosed — same caveat as dukotah's L7-A, ours measured).
6. External ledgers Leo-Y-Zhang / TheronEagle / jens-wedin unreachable
   this session (web proxy dead) — F18(ii) debt disclosed, not silently
   closed.

## 7. Machinery

`lag31.py`: numpy FFT indicator cross-correlations; multiprocessing
Pool over null draws and plant cells (local; est < 30 min total —
ETA restated after first timing print). Artifacts:
results/lag31.json (small). Seed 20261231.
