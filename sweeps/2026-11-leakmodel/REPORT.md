# Campaign #26 — REPORT: leak-model changepoint fit + key-consumption identifiability

Run 2026-11-18/19. PREREG committed before any output (b45ad51), with two
dated pre-/mid-registration addenda (G4 restatement a06a8be; power clause
plant-relative 5ee80d3 — see Disclosures). Seed 20261226. Lane A2 ran on
studio.local (28 cores) per owner steer; Lane A1 is minutes-local.

## Verdicts (verbatim against the registered rules)

- **Lane A1 — SEPARATES.** The flat-key idiom-equivalence claim is FALSE for
  the plaintext-redraw-with-key-held idiom: `dc_chi2` separates it from
  key-skip at min-p = 1.5e-18 (Bonferroni ×8). Registered SEPARATES branch:
  the separating statistic is reported here; **discriminator design and any
  corpus scan go to owner BEFORE execution** (not run).
- **Lane A2 — NULL-RETIRE** (stopping rule: "P1 ∧ P2 ∧ P3 ∧ CV-sign does NOT
  hold ⇒ verdict NULL-RETIRE"). All four clauses fail. **Qualified UNINFORMATIVE
  by the registered power rule**: plant detection 0/10 positions (bar ≥ 8/10) —
  "verdict NULL is UNINFORMATIVE (lane stays open as underpowered, disclosed) —
  never 'no changepoints'." The registered statistic cannot certify a
  half-rate 1,649-rune window; T7 remains a recorded anomaly (gap-ac1,
  campaign #10), neither certified nor refuted as a mechanism.
- Per the stopping rule, **Track C (seed spaces) proceeds to launch** — owner
  parked it "for when it completes"; it has completed.

## Lane A1 — key-consumption identifiability (local, N=2,000/idiom, L=12,956)

Flat uniform i.i.d. mod-29 keystream, English-quadgram plaintext, anti-doublet
reject filter; idioms: key-skip (advance key, hold plaintext) vs plaintext
redraw (advance plaintext, HOLD key). Battery: dc_chi2, sym_ac1, block_chi2,
bigram_chi2; KS + t per statistic, registered rule = min p, Bonferroni 8.

| statistic | KS p | t p |
|---|---|---|
| dc_chi2 | 0.024 | **1.5e-18** |
| sym_ac1 | 0.64 | 0.12 |
| block_chi2 | 0.79 | 0.60 |
| bigram_chi2 | 0.68 | 0.026 |

Mechanism (why the memo was wrong): the uniform key washes redraw out at
single-position marginals, but NOT across rejects inside one emission — the
held key meets successive English letters, so post-reject emission
differences follow the *plaintext* difference distribution (non-uniform),
while key-skip yields uniform key differences. Scope split: independent
UNIFORM replacement ≡ key-skip at emitted level (the original memo claim
survives for that rule); plaintext-redraw is separable key-free.

Cross-check against the reviewer's F2 fingerprint: observed corpus dc is flat
(χ² 41.4/27 df, p = 0.038); with ≈374 hidden rejects, redraw predicts an
inflation ≈10× the observed excess — the corpus leans key-skip, weakly. NOT
scanned with a purpose-built discriminator (owner-gated per PREREG).

Artifact: `results/a1_equiv.json`.

## Lane A2 — changepoint model comparison (studio; gates G1–G4 all PASS first)

Leak sequence: 12,955 pairs, 86 events, rate 0.00664. Exact DP, min span 50,
BIC params 1+2k (registered conservative form).

Observed k-profile (ΔBIC = BIC(M0) − BIC(Mk); penalty side-by-side per PREREG —
locations at k·lnN [registered, shown] vs 2k·lnN [heavier]):

| k | fitted bounds (coords) | ΔBIC (k·lnN) | ΔBIC (2k·lnN) | 2ΔLL |
|---|---|---|---|---|
| 1 | [4580] | −14.1 | −23.6 | 4.8 |
| 2 | **[5771, 5837]** | **−24.7** | −43.6 | 13.2 |
| 3 | [4580, 8935, 9596] | −38.7 | −67.1 | 18.1 |
| 4 | [2741, 4389, 8935, 9596] | −50.2 | −88.1 | 25.5 |

Registered clauses:

- **P1 FAIL**: ΔBIC₂ = −24.7 ≤ 10 (M2 *worse* than flat under the registered
  penalty; the k=2 optimum is a 66-rune burst at [5771, 5837] with rate
  0.0606, not a void).
- **P2 FAIL**: 10,000-draw M0 parametric bootstrap, p(ΔBIC₂ ≥ obs) = **0.576**
  (null max 0.757).
- **P3 FAIL**: k=2 bounds miss both T7 windows. (Null location clause
  p = 0.0004 — 3/10,000 draws hit the fixed T7 windows with a low middle —
  so the clause is rare under M0, but the observed M2 fit does not hit it.)
- **CV-sign FAIL**: 10-fold page-block predictive LL M2 = −536.1 < M0 = −518.3
  (M2 worse out-of-sample; same sign as ΔBIC, but the registered sign is
  improvement).

**Power (the load-bearing disclosure): 0/10 positions pass 8/20 draws**
(plants at 300…9900, half-rate 1,649-rune windows, expected ~5.5 events
removed). Structural: paying the (1+2k)·lnN = 37.9-nat penalty at k=2 needs
2ΔLL > 38; a half-rate void supplies ~13. The k=4 fit shows exactly this
failure mode — it places changepoints at **2741 and 4389** (within ±1 of the
T7 edges) with middle rate 0.00121 vs outers 0.0066/0.0097, yet ΔBIC₄ = −50.2.
The T7 pattern is VISIBLE and UNCERTIFIABLE by this statistic. Hence
UNINFORMATIVE, per the registered power rule.

Descriptive (no p-values, per PREREG): 2-state leak HMM by EM collapses to one
state (p_lo ≈ p_hi ≈ 0.00664, π_hi ≈ 0; BIC 1081.3 > M0 1043.5 — no hidden
state structure at 86 events).

Reopening the mechanism lane would need a statistic without location search —
e.g., a fixed-window (T7-edges-named-in-advance) rate-ratio test with
matched-window null, which is dukotah-I2 territory; that is a NEW registered
campaign, not this one.

Artifact: `results/a2_fit.json` (obs, null, cv, hmm, power, VERDICT).

## Disclosures (dated, not silent)

1. **A1 first-run aggregation bug (2026-11-19, before REPORT):** code
   aggregated `max(min(p_ks,p_t))` (best-behaved statistic) while PREREG L47
   registers MIN p; first run therefore printed MEMO-EQUIV with dc_chi2 at
   1.5e-18 in plain sight. Fixed (e53f9a4); re-run bit-identical statistics
   (seeds pinned); only the aggregation changed. Verdict above is the
   registered-rule verdict.
2. **Power clause restated plant-relative (addendum 5ee80d3):** registered
   "detection = P1∧P3" at random positions with P3's FIXED void windows is
   internally inconsistent (identically zero off-void). Restated plant-relative
   before any power output (the lane had crashed, producing none). PRIMARY
   prediction, null, CV, stopping rule untouched.
3. **Four studio launch failures before first A2 output** — missing
   manifest.json/krisyotam_runes.txt in SYNC_PATHS, image-provenance gate on a
   host without the 211 MB images (CICADA_SKIP_IMAGE_GATE added; full suite
   always passes locally pre-sync), and spawn-multiprocessing globals
   (worker initializer added). Gates re-ran and passed each time; no
   statistic was touched pre-gate on any attempt.
4. Bootstrap checkpoint (10,000 draws) survived the power crash; resume is
   bit-identical (house per-draw seeding); checkpoints gitignored per policy.

## What this campaign does NOT claim

No mechanism retired for T7 (power failed — UNINFORMATIVE, not absence).
No corpus discriminator scan (owner-gated). No upstream claims. No re-touch
of the grid lane. #23/#24A/#25D MAP power annotations (planned under
MEMO-EQUIV) are NOT applied — SEPARATES means the decoder-class question is
live and goes to owner.

## Reproduction

    python3 -m core.validate                       # gates (local, full)
    python3 sweeps/2026-11-leakmodel/fit.py a1     # ~3 min local
    scripts/studio.sh sync && \
      scripts/studio.sh run sweeps/2026-11-leakmodel/fit.py a2   # ~25 min studio
