# Campaign #7 report — number channels as additive keys (2026-11-number-channels)

**Verdict: NEGATIVE on all four families.** The designed numeric objects of
Liber Primus (line sums, the magic-square trace, the DIVINITY key,
plaintext line sums, digit expansions) and the page-number ramp channel
produce nothing above the family nulls at the additive-key level.
Registered 2026-11-15 (commit `75c166b`, before any output).

## Result table

| family | windows | obs max χ² | null min/med/p95/max (20) | p | verdict |
|---|---|---|---|---|---|
| Vp  | 85,800     | 78.47 | 71.45 / 76.61 / 82.09 / 83.44 | 0.238 | NEGATIVE (escalated) |
| Vs  | 7,450,320  | 84.28 | 79.41 / 90.74 / 98.44 / 105.37 | 0.810 | NEGATIVE |
| R   | 16,459,240 | 74.38 | 68.91 / 77.74 / 88.00 / 103.58 | 0.714 | NEGATIVE |
| D   | 32,835     | 51.26 | 36.00 / 44.74 / 53.41 / 56.02 | 0.191 | NEGATIVE (escalated) |

Observed argmaxes: Vp p15 ← `v:PT56:pcr` (φ-cumulative-reversed page-56
plaintext line sums) at phase 3, n=152; Vs p17 ← `v:WE5:v` at o=−500, n=72;
R p43 ramp 17·i at o=172, n=96; D p37 digit key, o=−414, n=54.
Total **24,028,195** windows (cumulative across campaigns: **353,235,004**).

**Escalation (pre-declared rule):** Vp and D observed maxima exceeded their
20-draw null medians → extended to 200 draws on the same seed stream
(draws 21–200 continue the sequence; first 20 bit-identical). Sharper nulls:
Vp 68.49 / 75.18 / 82.99 / 98.24 → p = 0.224;
D 31.16 / 44.40 / 56.00 / 70.12 → p = 0.179.
Ordinary null-region p-values; verdicts stand as NEGATIVE, no flag.

**GO prong 3 (decode):** all 80 leaders (top-20 × 4 families) decoded
forward AND reversed against 25 cribs → **0 hits**. No candidate survives.

## Instrument finding (pre-output): A WARNING 9/9 prime line sums

During code build — before any campaign output — the long-standing
"757 vs 758" transcription puzzle resolved: the printed A WARNING line sums
are **plaintext-side**, and the scream314 md wrapping reproduces them
exactly. Plaintext line sums (10 md lines):
`[332, 757*, 1009*, 691*, 353*, 769*, 911*, 1051*, 859*, 677*]` —
lines 2–10 are **9/9 prime** (P ≈ 10⁻⁸ by chance). dukotah's claim
confirmed from our corpus independently; line 1 (332) is the title line.
This object (PTAW) is inside the swept key set.

## Power probes (seed 20261123; recovery = planted key wins its page;
"≥ med" also requires χ² ≥ family null median)

| family | argmax recovery | ≥ median | note |
|---|---|---|---|
| Vp | 9/10 | 9/10 | page-wide English plant under a random variant key |
| Vs | 6/10 | 4/10 | window plants n≈50–230; weakest arm — a true Vs hit at n<~90 could hide |
| R  | 10/10 | 8/10 | slope-only criterion (see below) |
| D  | — | — | unprobeable: one usable digit stream on one page (disclosed in PREREG) |

### Identifiability lesson (R family)

For ramp keys `K_i = (c·i + b) mod 29`, **only the slope c is identifiable
from χ²**: b and the window offset each add a constant to the decoded
stream, and χ² against uniform is invariant under constant shifts. All 29
b-values × tied offsets win together at the true c. The first power-probe
run scored 0/10 because it demanded a match on unidentifiable coordinates;
fixed to slope-matching before any verdict was reported (probe criterion
fix, registered statistic untouched). Consequence for reading the sweep:
the R family's 16.5M windows encode ~28 distinct hypotheses × window
geometry — ties are expected and the null (same scan path) accounts for
them correctly. The same shift-invariance is why constant keys (c=0) were
excluded at registration.

## Methodology notes

- Keys: 10 designed sequences × {id, φ, digitsum} × {direct, cumulative} ×
  {sign} × {direction} = 216 deduped variants; page-aligned (Vp) and
  segment-local (Vs) arms; ramps c∈1..28, b∈0..28 (R); printed digits (D).
- χ² is symbol-permutation- and shift-invariant: additive constants and
  alphabet rotations cannot be detected by this statistic and were excluded
  from the key spaces by design (collapse logic as #3/#6).
- Nulls: in-page target shuffle, identical scan path, seed 20261122.
  20-draw nulls computed on studio.local (28 cores, 117 s; ~35× speedup)
  with bit-identical draw contents: all 20 shuffled corpora generated
  sequentially from `default_rng(20261122)` in the exact calibrate.py call
  order, then fanned out (see `run_par.py`); escalation runs local.
- Transcription caveat: line-sum parsing is md-wrapping-dependent; the two
  verified objects (AWARNING 9/9, SOME WISDOM 4/5 + mirror tail) reproduce
  published claims, which bounds the risk for this campaign only.

## Disclosures

1. PT56/PT57/PTWE line-sum sequences are md-wrapping-derived (labelled as
   such in numkeys.py); PTAW/SW5 reproduce published claims and are safe.
2. D family is nearly empty by corpus fact (6 digit glyphs; one page with a
   length-2+ run). Swept and reported for completeness; unprobeable.
3. Vs power is moderate (4/10 at median) — the negative is honest but the
   detection threshold is real: n ≳ 90–100 for reliable detection.
4. The R power-probe criterion was corrected post-registration (before any
   verdict) from exact-triple matching to slope-matching; exact matching
   tested an incoherent hypothesis (b/offset are unidentifiable).
5. Remote compute: nulls ran on the user's Mac Studio via a guarded wrapper
   (`scripts/studio.sh`); code and seed stream vendored and verified
   bit-identical; results cross-checked on return.

## Reproduction

```
python3 sweeps/2026-11-number-channels/run.py                    # ~200 s
python3 sweeps/2026-11-number-channels/run_par.py                # 20 draws, parallel
python3 sweeps/2026-11-number-channels/run_par.py --fams Vp,D --draws 200
python3 sweeps/2026-11-number-channels/power.py --fams Vp,Vs,R --med Vp=75.18,Vs=90.74,R=77.74
```

Full CSVs: `work/number-channels/sweep_<F>.csv` (sha256 in
`results/obs_maxima.csv`); tracked `results/sweep_<F>.csv` = top 100k rows
by χ² (Vp/D ship complete: <8k rows each).

## Ledger entry

> **#7 number-channels (2026-11-number-channels), 2026-11-15 — NEGATIVE.**
> 24.0M windows: designed value-sequence keys (216 variants; LP1 line sums
> incl. newly verified 9/9-prime A WARNING plaintext line sums) page-aligned
> and segment-local, page-number ramps, printed digits. All family maxima
> in null region (p = 0.18–0.81; Vp/D escalated to 200 draws per rule).
> 0/80 leaders decode (both directions, 25 cribs). Power: Vp 9/10,
> Vs 4/10, R 8/10 (slope-only; b/offset unidentifiable from χ²), D
> unprobeable. Cumulative 353.2M windows.
