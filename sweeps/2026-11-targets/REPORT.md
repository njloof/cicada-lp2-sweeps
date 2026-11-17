# Campaign #14 report — F13: token table as TARGET

Run 2026-11-16. Queue slot 6. Registration: `PREREG.md` (`31c38c3`),
committed before any output. Verdict: **R1 NEGATIVE (powered), R2 NEGATIVE
(powered)** — the p50/canon token table resists every consumption direction
now measured by both ledgers.

| family | hypothesis | obs | null (D=20) | p | plants |
|---|---|---|---|---|---|
| R1 T2-re-power (pad→page, affine a∈2..28, W=240, canon-only) | table pads a page under affine scaling | 74.89 (p25,a15,o55) | med 78.40, p95 92.62, max 94.23 | **0.905** | **20/20** |
| R2 blob-as-target (B − a·v, n=256, a∈1..28, o∈0..255) | a page's runes unlock structure IN the table | 76.82 (p25,a2,o55) | med 80.33, p95 87.29, max 88.15 | **0.810** | **20/20** |

α = 0.025/family; seed 20261203; escalation not fired (both obs BELOW the
null median); runtime 921 s vs ≤25 min estimate — held.

## Why these are believed

The T2 W-lesson (campaign #10) was that its NEGATIVE was structurally
unreachable: plants of ≤72 tokens could never beat a 1.9M-window family
median. This campaign fixed exactly that: **long windows (W=240) and a
shrunk family (canon-only)** for R1, and a fixed n=256 target-space
statistic for R2. Both power plants — English-strength cribs of full
window/blob length — beat their family p95 **20/20**. The instruments can
see; they saw nothing. Both obs sit BELOW the null median (the same
"real data decodes flatter than permutations of itself" anti-signal as
PB1, campaign #12) — recorded, nothing built on it.

Anecdote kept honest: both argmaxes land on page 25 at offset o=55. Below
median in both families = noise; noted only because it is the kind of
coincidence that gets over-read later.

## Disclosures

- **Smoke run**: pre-launch pipeline check at `--stage 1` (verdict
  meaningless, D=1), output to gitignored `work/scratch/`, not used for
  any number here; obs values bit-identical to the stage-20 run
  (determinism check).
- **Bug fixed pre-launch**: window cumsum off-by-one (IndexError, first
  launch died at gate-pass; no statistic produced under the buggy code).
- Plant cribs use English letter frequencies over runes representable by
  single-letter TRANS; K,Q,V,Z unrepresented (~1% mass renormalized).
- R1 dropped the e0/superseded table variants (witness-discounted, as
  registered); sign folded into a for R2 (as registered, Beaufort covered).

## E-enumerations

- E1 argmax tables: in `results/f13_results.json` (R2 carries top-5).
- No crib stage (nothing fired; none required).

## What this closes

Token-table consumption, complete direction map across both ledgers:
blob→page additive/Beaufort/atbash (theirs), blob→page affine (ours T2,
now re-powered R1), page→blob selection (ours PB1), **blob-as-target
(R2, this campaign)** — all negative; R1/R2 with measured power. The
remaining open questions about the table are not sweep-shaped: its glyph
values (oracle S1–S3; owner round-#3 answered S1 "unclear") and p50's
104-token stream as its own object (needs a census, not a scan).

## Files / regeneration

```
python3 f13.py            # ~15 min local; stage-20, auto-escalate
```

## Not covered (as registered)

PB1-affine selection a≠1 (inherits instrument lesson #2 blindness —
registering a knowingly-blind negative declined); p50 104-token stream as
separate target; mod 28; transpositions; non-English plants; multi-page
key chaining.
