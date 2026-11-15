# Pre-registration — Campaign #8: self-derived value keys (2026-11-selfkeys)

Registered 2026-11-15. This file is committed before any campaign output
exists (CI gate). Scope approved by the project owner same day.

## Hypothesis

An unsolved LP2 page's additive key is derived from **the page's own rune
values** (dukotah U3, "word-sum self-keys", made precise). Word boundaries
are unobservable on unsolved pages, so **lines are the only available
segmentation** and "word-sum" is operationalized as "line-sum" — disclosed
up front. The design precedent is verified, not speculative: LP1's printed
numbers are plaintext/ciphertext **line sums** (AWARNING 9/9 prime
plaintext line sums, verified in #7 pre-output; SOME WISDOM 4/5 + mirror
tail).

## Statistic (unchanged house instrument)

χ² vs uniform over 29 bins on the difference stream D = (A − K) mod 29,
window semantics and masks as in core.kernel.pair_scan: MIN_LEN = 50,
record floor 40, tgt mask primary, both mask for confirmation. χ² is
invariant under constant shifts and symbol permutations; constant keys are
excluded (they cannot move χ²).

## Families

Let A be the target page (m runes), primes p(r) from GEMATRIA, page lines
from the scream314 md wrapping (transcription caveat: md line structure is
a transcription guess; bounded by the fact that the verified LP1 objects
reproduce through the same wrapping).

1. **LS — line-sum segment self-keys.** Per line s: v_s = T(S_s) mod 29,
   S_s = Σ p(r) over line s; K = piecewise-constant v_s over line s;
   D = (A − K) mod 29, whole page (no offsets: the key IS page-aligned).
   T ∈ {id, φ, digitsum} × {direct, cumulative across lines} × {sign ±}
   = 12 variants. Variants with < 2 distinct values (constant →
   shift-invariant) are excluded at construction. This is the direct LP2
   analog of the verified LP1 design: if A = E + lineSum(A), the decode
   falls out.
2. **VT — value-transform self-lag.** pad = f(A) elementwise,
   f ∈ {φ(v) mod 29, digitsum(v)}; D[i] = A[i] − pad[i − o] for all
   offsets o (pair_scan), pad forward and reversed. f = id is EXCLUDED as
   already covered: raw self-lag differences are exactly #1's self-pairs
   (#1's max, the p≈0.10 self-mirror, was this channel).
3. **CF — cumulative-feedback self-keys.** Strict-past pads:
   K[i] = Σ_{j<i} A[j] mod 29 (prefix) and sliding windows w ∈ {2,3,5}:
   K[i] = Σ_{j=i−w}^{i−1} A[j] mod 29; all offsets, fwd+rev. Classic
   ciphertext-autokey with primer p is a lag difference → covered by #1;
   only value-space cumulative variants are new here.

Windows ≈ 36M (VT ~12M, CF ~24M, LS ~0.15M) — exact counts reported.

## Null (the methodological core)

**Derive-from-shuffled.** Per draw, per target: Aπ = rng.permutation(A);
ALL self-key derivations are recomputed on Aπ (LS line sums from the
shuffled page's lines; VT pad = f(Aπ); CF pad = cumulative(Aπ)); the
identical scan runs; family maxima collected. Seed 20261124, 20 draws,
resumable checkpoint.

Why not the #6-pattern target-shuffle-with-fixed-pad null: when the pad
is derived from the target, shuffling the target against a FIXED pad
destroys exactly the self-agreement the family tests — the #6 blindness
generalized one level up. Derive-from-shuffled preserves value marginals,
pushforward distributions (e.g. VT o=0: D = A − f(A) has a non-uniform
pushforward under uniform A — the null reproduces it exactly), and LS
piecewise-constant structure + fixed-point algebra, while destroying
designed positional alignment. Under the alternative (English D), the
shuffled derivation does not produce English D — the null is not
signal-inflated.

Escalation rule (unchanged): any family with obs ≥ its 20-draw null
median → extend to ≥ 200 draws on the same seed stream before verdict.

## GO prongs (all required)

1. obs > 1.1 × family null max (20 draws);
2. mask=both survives with n ≥ 50;
3. decode (fwd AND reversed) yields English/cribs — 25-crib list, house
   standard;
4. (bonus, not required) cross-page consistency: same scheme hitting
   multiple pages.

## Degeneracy pre-checks (pre-output, from the #6 scar tissue)

- No permutation self-pairs exist in these families (no fixed-point ᚠ
  channel by construction); startup check verifies per-scheme D-zero
  fraction on the real corpus against the no-structure baseline (~1/29 +
  mask effects): any scheme > 0.15 zero-fraction must be mechanistically
  explained before the sweep counts.
- LS: exclude constant keys; verify per-page line lengths sum to m
  (wrapping integrity).
- VT/CF o=0 rows retained (no triviality: f ≠ id; CF strict past) but
  flagged in the CSV for audit.

## Power (self-consistent plants — naive planting is impossible here)

A plant must satisfy the self-consistency the family tests: A2 = E + key(A2).
- VT: sequential solve A2[i] = E[i−st] + f(A2[i−o]) over window [st, m),
  o ≥ 1 (o=0 plant is per-position implicit; skipped, disclosed).
- CF: sequential solve A2[i] = E + K2[i] with K2 the strict-past
  cumulative of A2 itself (hit lands at o=0 by construction).
- LS: per-line 29-way fixed-point search for T(sum(E_s) + |s|·k) ≡ k;
  lines with no fixed point are skipped and reported. Plant uses T=id.
Recovery = planted row is family max on the planted page AND χ² ≥ family
null median. Seed 20261125, 10 plants/family. Any family unprobeable is
reported as such, not fudged.

## Cost

Observed sweep < 2 min local; nulls via scripts/studio.sh on 28 cores
(minutes); escalation 200 draws < 10 min. All cheap by construction —
self-keys are one pad per page per scheme, not 216-variant grids.

> **Amendment (post-run, labeled per house rules, 2026-11-15):** measured
> on 8-core laptop: observed sweep 2 s; 20-draw null 11 s; 200-draw VT
> escalation 34 s. The <2 min estimate priced a per-position loop;
> pair_scan is vectorized per offset, so the null needed no studio
> offload. Registered statistic, null design, and decision rule unchanged.

## Not covered (disclosed)

Word-boundary schemes (unobservable segmentation); doublet/ornament
channels (transcription-adjacent — after the audit); f=id self-lags and
primer-autokey (covered by #1); cross-page self-keys (page N's sums as
keys for page M — that is #1's space with transformed pads; only f ∈
{φ, digitsum} of ANOTHER page would be new and is deferred, low prior);
page 55; LP1-as-target.
