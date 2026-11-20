# Campaign #32 — ORACLE ADJUDICATION ASK (verdict PARTIAL-COVERAGE-FLAGGED)

Owner request 2026-11-20: "present the adjudication needed from me
clearly." Everything below is full-page (owner policy 2026-11-17, never
crops); figures regenerate with `mk_adj_fig32.py`.

## 1. The situation in four lines

1. The two registered print-channel tests both came back **significant**
   → verdict rule fired `FLAGGED` verbatim, and FLAGGED = flag-for-oracle.
2. Post-hoc diagnostics (disclosed; verdict unchanged) say the flags are
   almost certainly **typography, not encoding**: the value picks the
   glyph, and each glyph has a fixed print signature.
3. Placement itself shows **no** value-dependence (kerning gap CV 0.57 —
   essentially free).
4. Your call is what the flag *means*, not whether the arithmetic ran
   (gates: G0 56/56 byte-exact, G2 deviation 0 at 1e-6, G3 PASS,
   coverage 74.41% with every excluded line itemized on full pages).

## 2. The flags

| test | observed | null | p | plant gate |
|---|---|---|---|---|
| T1 eta²(area \| value), within-line z | **0.8455** | median 0.0041, c95 0.0053 | 5.0e-4 (floor 1/2001) | PASS (power 1.0 @ eps 0.10) |
| T2 Rayleigh frac(cx), n=9,640 | **R = 0.0478** | uniform | 2.7e-10 | **FAIL** (power 0.05 @ jitter 0.3) |

## 3. Why "typography, not encoding" is the leading reading

- **figs/area_by_value.png** — ink area is determined by value to a few
  percent (the 16–84 bands are JPEG-noise wide). Of course it is: value
  = glyph identity, and every printed glyph has its own ink amount.
  eta² = 0.85 is exactly this triviality. Within-line w and h have CV
  **0.0000** per value — the print is metrically fixed per glyph.
- **figs/frac_cx.png** — the sub-pixel x-centroid is near-deterministic
  **per value** (circular resultant 0.8–0.9 for most values): each
  glyph sits in an (integer-ish) typeset cell with a fixed centroid
  offset. The global Rayleigh is the mixture of 29 fixed per-value
  directions — a shape fingerprint, not a placement code.
- The registered null (permute values within line) cannot remove
  value→glyph→size: it permutes values ACROSS different glyphs, so the
  observed statistic is made of structure the null destroys wholesale.
  That is a design flaw in the wave-1 metric set, disclosed in REPORT §5.
- T2's plant gate already told us the same story from the power side:
  with near-uniform value frequencies the registered plant class has
  ~zero resultant at any jitter — T2 was never powered against its own
  alternative, so its p-value must not be read as "powered and
  significant".

## 4. What the flags are NOT

- Not a kerning/spacing channel: gap CV 0.57, no registered signal
  once size-morphometrics are set aside.
- Not an alignment artifact of the pipeline: G2 verified metrics at
  1e-6; count gates pin every line to the transcription.
- Not (yet) evidence against Track B's hypothesis: the correct test
  (below) has not been run.

## 5. Coverage honesty (what 74.41% excludes, on the pages)

- **figs/p0_coverage.jpg** — l0 header is RED-ink print (excluded by
  the registered red-ink rule — policy cost, not data loss); every
  other line aligned 19–24/24.
- **figs/p15_coverage.jpg** — worst page (28%): red header + red/black
  mixed line + the decimal grid + ornaments contaminate the count gate;
  excluded-line labels are region-approximate (the row is unknown by
  construction). Red/mixed/faded/off-by-one taxonomy in REPORT §8.

## 6. The decision (pick one, or direct otherwise)

- **(A) ARTIFACT — close wave 1 as no-channel.** Verdict text becomes
  "flag adjudicated as glyph-morphology main effect"; morphology
  metrics (area/w/h/density) retired for value-association use; the
  table ships to wave 2 (line-break residuals) unchanged.
- **(B) REAL — treat as a genuine print-channel lead.** Then the
  registered §6.1 condition binds first: PNG-source re-acquisition and
  re-run before ANY interpretation, plus alignment improvement toward
  the 95% bar. We assess this path as unlikely to survive re-run, but
  it is your adjudication, not our prediction.
- **(C) WAVE-1b (recommended).** New PREREG, ~1 hour of compute, table
  reused: residualize every metric by value (subtract per-value
  within-line mean), then test whether a rune's RESIDUAL placement
  depends on context (neighbour values, line position) under a
  within-line, within-value permutation null. That is the test that
  actually asks "does the print encode the value beyond glyph
  identity" — and its plants can be calibrated against the confound
  instead of drowning in it.
- **Independent of A/B/C — relay?** The Track B reviewers asked for
  print channels. The methodologically interesting package (byte-exact
  instrument + null placement result + morphology-confound lesson +
  wave-1b design) is ready as response text whenever you approve;
  relay remains owner-gated and nothing has been sent.

## 7. Receipts

REPORT.md (verdict + gates + disclosures + addendum) ·
results/tests32.json · results/coverage32.json · figs/*.
Full table: studio `work/table32.jsonl`, sha256
`ff11c6c99d52b77037201d2fa5f396c4f65ce0cb5dddf63b303919284424b7c1`;
regeneration: `scripts/studio.sh run
sweeps/2026-11-printchannel/table32.py && scripts/studio.sh run
sweeps/2026-11-printchannel/tests32.py` (seed 20261232).
