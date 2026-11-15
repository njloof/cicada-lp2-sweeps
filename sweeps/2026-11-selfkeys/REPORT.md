# Campaign #8 report — self-derived value keys (dukotah U3): NEGATIVE, all families

Run 2026-11-15. Pre-registered before output at `3e1cd82` (PREREG.md).
Corpus, statistic, masks, floor as registered; seed 20261124 (null),
20261125 (power).

## Verdict

| family | positions | obs max (argmax) | null med | null max | p | verdict |
|---|---|---|---|---|---|---|
| LS  | 149,976    | 55.26 (p22 ls:i−, o=0)          | 60.00  | 71.55   | 0.81 | **NEGATIVE** |
| VT  | 12,386,792 | 2351.15 (p35 vt:ds, o=0)¹       | 2351.15 | 2351.15 | 1.00 | **NEGATIVE**¹ |
| CF  | 24,773,584 | 76.57 (p30 cf:w3r, o=−62)       | 79.13  | 101.11  | 0.81 | **NEGATIVE** |

³⁷³¹⁰³⁵² positions total (243,900 offset-rows; see disclosure 2).
Every observed max is **below** its null median. GO prongs: (1) fails
everywhere; (3) decode scan of all 60 leaders (top-20 × 3 families),
forward AND reversed, vs the 25-crib house list → **0 hits**. No candidate
survives; prong 4 moot.

¹ **The VT number is an algebraic artifact, not a signal** — see below.

## The vt:ds o=0 degeneracy (pre-output zero_check → mechanism → null confirmation)

The registered pre-output degeneracy check flagged exactly one scheme on
all 55 pages: `vt:ds` with D-zero fraction ≈ 0.31 (baseline 1/29).
Mechanism: v ≡ digitsum(v) (mod 9), and for v ∈ 0..28,
v − digitsum(v) ∈ {0, 9, 18}. So the o=0 difference stream
D = (A − ds(A)) mod 29 is supported on **3 of 29 bins** — any page scores
astronomically (p35: 271 runes → χ² 2351.15) with zero information about
alignment or language.

Confirmation from the null itself: D at o=0 is elementwise, so it is
**invariant under shuffling** — all 20 and then all 200 draws returned
exactly 2351.15 (min = med = max = obs). The derive-from-shuffled null
absorbed the degeneracy exactly as designed; p = 1.0.

The escalation rule fired mechanically (obs ≥ median, by exact tie) and
was honored: VT re-run at 200 draws. It is uninformative for the
artifact, but was run per the registered rule rather than waived.

**Disclosed secondary diagnostic (not a registered test):** VT restricted
to offsets ≥ 1 — obs 81.15 (p30, vt:dsr, o=156) vs 20-draw null
min 74.63 / med 86.04 / max 103.90 → p = 0.81. Negative as well, and the
power diagnostic below shows the restricted family is genuinely sensitive:
10/10 self-consistent plants recovered at planted χ² 203–320, twice the
o≥1 null max. The registered VT verdict therefore rests on a clean
instrument once the artifact is excluded.

## Null — derive-from-shuffled (the methodological core, worked)

Per draw, targets were permuted and **all self-keys re-derived from the
shuffled target** (line sums, value transforms, cumulative pads — the
derivations read the array under test; only line *lengths* are held, as a
transcription property). Seed 20261124, exact sequential
`default_rng(seed)` stream; draws 1–20 are a prefix of the 200-draw VT
stream (verified: identical first-20 maxima). This null reproduces
pushforward structure (the vt:ds artifact above is the extreme case) while
destroying designed positional alignment — the #6 lesson (fixed-pad
shuffle nulls are blind to self-agreement) generalized one level up, and
it paid for itself immediately.

## Power (self-consistent plants, seed 20261125)

| family | criterion | argmax recovery | ≥ null median |
|---|---|---|---|
| LS | planted (ls:i, o=0) is family max | 10/10 | 9/10 |
| VT | registered (family max incl. o=0) | **0/10** | 0/10 |
| VT | disclosed o≥1 criterion | 10/10 | 10/10 (χ² 203–320) |
| CF | planted (cf:pre, o=0) is family max | 10/10 | 9/10 |

VT's registered 0/10 is the artifact dominating the family max on every
planted page — the plant is present and strong (o≥1 diagnostic), it just
cannot out-shout a 3-bin pushforward. Reported, not fudged: the
registered criterion stands in this table; the diagnostic is labeled.

## Disclosures

1. **CSV column bug, fixed pre-report.** The streamed sweep CSVs were
   written without the family column declared in the header (rows shifted
   one column left). Observed maxima, leaders, and nulls were computed
   in-memory and are unaffected; the sweep was re-run after the fix
   (identical maxima; new CSV sha256s in `results/obs_maxima.csv`). The
   shipped CSVs are the post-fix files.
2. **Window semantics.** PREREG's ~36M was a positions estimate; measured
   positions = 37,310,352 (LS 149,976 + VT 12,386,792 + CF 24,773,584).
   The sweep CSVs hold one row per (page, pad, offset) window — 243,900
   rows ≥ floor. Both counts are reported; `window_counts.json` holds
   positions.
3. **Cost amendment (labeled, house rules).** PREREG's cost section said
   "< 2 min local"; measured: observed sweep **2 s**, 20-draw null
   **11 s**, 200-draw VT null **34 s** (8 cores). The estimate had priced
   a per-position loop; `pair_scan` is vectorized per offset. Studio
   offload was prepared but unnecessary at this scale — the wrapper
   stands for future campaigns.
4. **VT escalation was mechanical** (exact tie at the degenerate value);
   run anyway per rule. No LS/CF escalation (obs below medians).
5. **LS is coarse by construction**: 12 hypotheses per page, page-level
   χ², 660 rows. Its negative is a clean but narrow statement about the
   md-line segmentation of the transcription (single-root caveat applies;
   the transcription audit is the dependency for anything finer).
6. Full CSVs ship **complete** in `results/` (837 B / 187 KB / 291 KB —
   below the top-K truncation threshold; no split needed).
7. **Post-report self-correction (2026-11-15, during the transcription
   audit):** the "word boundaries unobservable" premise (PREREG hypothesis
   + not-covered) is wrong at the stream level — the pinned krisyotam
   source encodes word dividers `-` and sentence dots `.` alongside the
   line marks `/`; our corpus tokenization drops them. The registered
   LS test is untouched (lines were a legitimate registered choice —
   divider *fidelity* is unverified single-root data), but the literal
   word-sum U3 is unblocked for a future campaign once the visual pass
   checks the dividers. Labeled amendment in PREREG.md; ledger footnote.

## Regeneration

```
python3 sweeps/2026-11-selfkeys/run.py                    # observed, ~2 s
python3 sweeps/2026-11-selfkeys/run_par.py                # 20-draw null, ~11 s
python3 sweeps/2026-11-selfkeys/run_par.py --fams VT --draws 200   # escalation
python3 sweeps/2026-11-selfkeys/power.py --med LS=60.0,VT=2351.15,CF=79.13
```

## Ledger entry

| 8 | 2026-11-15 | self-derived value keys (U3 made precise): line-sum segment keys (LS, the LP1 line-sum design's LP2 analog), value-transform self-lags φ/digitsum (VT), strict-past cumulative feedback (CF) | 37,310,352 positions (243,900 rows) — preregistered before run (`3e1cd82`) | 20× derive-from-shuffled MC, seed 20261124 (keys re-derived per draw); VT escalated 200× per rule | **NEGATIVE all families** (p = 0.81, 1.00, 0.81; obs below medians; 0/60 leaders decode fwd+rev vs 25 cribs) | VT max = proven vt:ds o=0 pushforward artifact (D ∈ {0,9,18}, shuffle-invariant, 200/200 draws identical); o≥1 diagnostic negative & powered (10/10). Power LS 10/10, CF 10/10. NOT covered: word-boundary schemes (unobservable), doublets/ornaments (post-audit), f=id self-lags & primer autokey (=#1), cross-page self-keys, page 55, LP1-as-target | [report](../sweeps/2026-11-selfkeys/REPORT.md) |
