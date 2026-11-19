# Campaign #26 PREREG — Track A: leak-model changepoint fit + key-consumption identifiability (registered 2026-11-19, BEFORE any campaign output)

Owner steer 2026-11-18: Track A leads; run on studio; Track C parked until this
reports. External review round-2 hand-off adopted (docs/MAP.md F17 Track A):
leak idioms A–O enumerated, survivors D-with-drift / J-scattered / M / N / O;
closed-form leak rate; changepoint-BIC + HMM fit plan; stopping rule.
This campaign turns the corpus headline (86 doublets vs ~445 expected, ~17σ)
into a mechanism test, with the T7 void as the registered prediction.

## Premise facts (read-only, verified before registration, no decode output)

- Corpus: book 0–49 + 51–55 = 12,956 runes (validate gate 2); 12,955 adjacent
  pairs; 86 observed doublets (gate 4). Leak sequence L_t = 1[C_t = C_{t−1}],
  t = 1..12,955; 86 ones; emission rate 86/12,955 = 0.664%.
- Redraw-idiom closed form (reviewer round 2): emission rate = q(1−s)/(1−qs)
  with q = 1/29 ⇒ implied single-redraw acceptance s = 0.813.
- T7 localization (campaign #10, LEDGER C1 wording): void-boundary doublet
  sites at 2740 and 4389, internal sites 3140, 3852; the anomaly is three
  consecutive large gaps 400/712/537 vs corpus-typical ~150 — a LOW-LEAK
  segment, not a doublet-free void. Interior (2741–4388): 2 events in 1,648
  runes (0.12%) vs 84 in 11,307 outside (0.74%).
- Solved pages do NOT carry the filter (p56 2.38%, p57 1.06% doublets,
  small-n caveat): the filter is an artifact of the unsolved bulk only.
- dukotah R34 I2 (CONFIRMED): key skips are invisible in emitted ciphertext
  (with-skip prefilter power 0.62–0.66, not 0.998).
- SEGMENTS v2 (Q1–Q7) is NOT owner-signed-off ⇒ section-boundary model is
  tertiary/descriptive only.
- Page boundaries: 54 internal boundaries at known cumulative offsets.

## Lane A1 — key-consumption IDENTIFIABILITY memo (simulation proof; minutes, local)

Question on the table (MAP headline): does the filter consume key on a
rejected doublet (dukotah "key-skip") or resample plaintext with key held
(Wulfic "independent replacement")? Decides the decoder class for every
sweep — IF decidable.

- Claim to test by simulation: under a FLAT (uniform i.i.d. mod-29) keystream,
  the two idioms generate emitted streams that are distributionally identical
  for every emitted-level statistic. Both emit "uniform over the 28
  non-predecessor values, independently at each position": key-skip leaves the
  key i.i.d. uniform at whatever positions it lands on; redraw conditions the
  plaintext but the uniform key washes it out.
- Design: English-like plaintext (quadgram sampler, dukotah english_quadgrams)
  + flat key, both idioms, N = 2,000 matched-seed stream pairs, length
  12,956. Battery (two-sample KS/chi2 per pair-set, pooled): doublet-gap
  distribution, ΔC distribution, gap ac1, block dispersion, run-length stats.
  Report min p with Bonferroni over the battery.
- Verdict MEMO-EQUIV (expected): key consumption NOT identifiable from the
  unsolved corpus; DECISION (this is the "decision first" item): all future
  power claims adopt the SKIP-TOLERANT decoder class (I2 with-skip column
  0.62–0.66); #23/#24A/#25D power statements get MAP annotations — no re-runs.
- Verdict SEPARATES (unexpected): report which statistic; follow-up
  discriminator design goes to owner BEFORE any scan (conditional escalation,
  not pre-registered here).
- Disclosed limitation: with a STRUCTURED key the idioms differ in key↔
  position alignment, but alignment is only testable given a key hypothesis —
  that is the prefilter-power story, not an emitted-level test.

## Lane A2 — PRIMARY: changepoint model comparison on the leak sequence (studio)

- Data: L_t binary sequence, 12,955 positions, 86 events (gates below).
- Models: M0 = Bernoulli(p). M_k = piecewise-constant Bernoulli, k = 1..4
  changepoints, EXACT DP segmentation (optimal, no greedy), minimum segment
  length 50 runes (disclosed; void is 1,649 ⇒ unaffected).
- Placement classes: PRIMARY free (any position); SECONDARY page boundaries
  only (54); tertiary Q-section boundaries (descriptive; v2 unsigned).
- Selection: BIC, params = 1 + 2k (k locations + k+1 rates); report the
  k·ln(n) vs 2k·ln(n) penalty conventions side by side, verdict uses the
  conservative 1+2k form.
- REGISTERED PRIMARY STATISTIC: ΔBIC₂ = BIC(M0) − BIC(M2, free), plus the two
  changepoint locations ĉ1, ĉ2 of the M2-free fit.
- REGISTERED PREDICTION (T7-as-changepoint), all three clauses required:
  (P1) ΔBIC₂ > 10;
  (P2) calibrated p(ΔBIC₂ ≥ obs) < 0.05 under the M0 parametric bootstrap;
  (P3) LOCATION: ĉ1 ∈ 2740 ± 150 and ĉ2 ∈ 4389 ± 150, middle segment rate
  below both outer segments (±150 = corpus-typical inter-event spacing;
  changepoints are only identifiable to that resolution).
- Null calibration (load-bearing — BIC asymptotics are invalid under
  changepoint search): parametric bootstrap M0, p = 86/12,955, D = 10,000
  replicates of length 12,955, refit M2-free per replicate; null distributions
  of ΔBIC₂ and of the location clause. The prediction names FIXED positions,
  so the null location clause uses the SAME fixed windows {2740±150,
  4389±150} on every replicate (not each replicate's own best pair).
  p = (1 + #{null ≥ obs})/(D+1), per clause.
- Holdout (reviewer requirement): 10-fold PAGE-BLOCK CV predictive log-loss,
  M0 vs M2-free; CV improvement must have the same sign as ΔBIC₂ or the
  verdict is downgraded to WEAK regardless of BIC.
- Registered tests = P1, P2, P3 + CV sign ⇒ 4 items, Holm within the lane.
  Everything else (k-profile, page-boundary class best, per-segment implied
  s_i via closed form, 2-state leak HMM EM fit vs M2) is DESCRIPTIVE, reported
  without p-values. The reviewer's "HMM pinned at 1/29" refers to keystream
  emission; our leak-HMM fits rates (s_lo, s_hi, transition) by EM — BIC vs M2
  reported descriptively only (86 events is thin for 4 params; disclosed).
- Power (plant-based, not assumed): plant = constant-rate segment with
  half-rate leak (expected ~6 events in 1,649) at 10 random positions × 20
  draws under M0-with-plant; detection = P1∧P3. Pass bar: ≥ 8/10 positions.
  If power fails, verdict NULL is UNINFORMATIVE (lane stays open as
  underpowered, disclosed) — never "no changepoints".
- Stopping rule (pre-committed, reviewer F9 rule): if P1 ∧ P2 ∧ P3 ∧ CV-sign
  does NOT hold ⇒ verdict NULL-RETIRE: the changepoint/leak-mechanism lane is
  RETIRED for this corpus, T7 remains a recorded anomaly (gap-ac1 statistic
  only, no mechanism lane), and Track C proceeds to launch. If all hold ⇒
  QUALIFIES: session-boundary becomes the leading mechanism; per-segment
  rates + drift models go to a NEW registered campaign (not this one).
- Seeds/streams: numpy Random(f"20261226:{d}") substreams, D = 1..10,000,
  resumable bit-identical checkpoints (gitignored per policy 48bacae).
- Runtime estimate (studio 28c): DP fit ~ms; bootstrap 10,000 × M2-free DP
  (12,955 × 2 segments DP ≈ 0.1 s) ≈ 20 min single-core, parallelized ~1–2
  min wall; CV minutes. Total < 30 min studio.

## Gates (all before any statistic is touched)

- G1 validate.py ALL gates pass (known-solutions suite mandatory pre-launch).
- G2 doublet count == 86; site tuple bit-identical to campaign #10's list
  (sweeps/2026-11-t7-replication/).
- G3 page lengths sum to 12,956; 54 page-boundary offsets reproduce the
  #10-cited void edges (2740/4389 are inter-site, not page edges — assert
  both readings separately).
- G4 DP recovers planted changepoints exactly on 5 synthetic sequences
  (k = 1..4, known rates) — the fitter is tested before the corpus is.

## Execution (studio per owner steer — nothing days-long on this host)

scripts/studio.sh sync && scripts/studio.sh run
sweeps/2026-11-leakmodel/fit.py all ; scripts/studio.sh pull … (Lane A1
simulation runs locally: minutes). REPORT.md carries verdicts, calibrated
p's, k-profile figure, and the retired-or-qualified outcome verbatim against
the stopping rule.

## Addendum (2026-11-19, pre-output — no real-data statistic touched yet): G4 restated

As written ("DP recovers planted changepoints exactly"), G4 fails by
construction, not by fitter bug: on random Bernoulli sequences the MLE
changepoint has inherent location jitter of tens of runes (observed ±15–45 at
rates 0.05/0.005) — "exact" is not a meaningful demand for the estimator.
G4 is restated as the two claims that ARE meaningful, and stronger than the
original in the part that matters:
- **G4a (optimizer exactness):** DP == exhaustive brute force (all cut
  combinations) on 3 small sequences (N=200, k=1..3, random rates) — the DP
  is exactly optimal, no heuristic.
- **G4b (recovery within registered resolution):** on the 4 synthetic
  sequences (N=20,000, k=1..4, rates 0.05/0.005), every fitted changepoint
  within ±150 of planted — the same resolution the registered location clause
  P3 uses. Exact-match is reported descriptively.

Everything else (P1–P3, null calibration, CV, power, stopping rule) unchanged.

## What this campaign does NOT do

No crib/English scoring anywhere (language-free lane). No re-registration of
the grid lane (LEDGER C6). No upstream claims without owner approval. A
FLAG-level outcome still never auto-certifies a mechanism — QUALIFIES means
"model comparison favors sessions", the strongest word statistics allow here.

## Addendum (2026-11-19, after observed fit + null, before any power output): power clause restated plant-relative

The power paragraph registers "detection = P1∧P3" at 10 RANDOM plant
positions, but P3 as defined names the FIXED void windows {2740±150,
4389±150}. Read literally, detection is identically zero for every plant off
the void and the 8/10 bar cannot pass — the paragraph is internally
inconsistent. Restated (the only coherent reading, clause structure
unchanged): for a plant window starting at w, the location clause uses
w±150 and (w+1649)±150, middle rate below both outers. The PRIMARY T7
prediction (P1–P3 with fixed windows), the null calibration, the CV and the
stopping rule are UNCHANGED; the observed fit and the 10,000-draw null were
computed before this addendum and are untouched by it. The power lane
produced NO output before the fix (it crashed: the same fixed-window clause
plus a slice-arithmetic bug at plants below the void).
