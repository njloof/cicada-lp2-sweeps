# Campaign #12 / F18 — PREREG2: PB1 statistic amended BEFORE ANY OUTPUT

_Dated 2026-11-16. PREREG.md (d478ca9) stands as written and is marked
SUPERSEDED-BEFORE-RUN below — **zero output was produced under v1**; the
defect is a two-line proof, not a result._

## Why v1 cannot be run

v1 statistic: per-PAGE-marginal χ² of D_s,p[i] = B[(v[i]+s) mod 256] mod 29.
The key is value-INDEPENDENT (B fixed), so the page's decode histogram is

    H[x] = Σ_r c_p[r] · 1[B[(r+s) mod 256] mod 29 = x],   c_p = value counts

— a function of the value COUNTS only. The registered null (permute page
values) preserves c_p exactly ⇒ null ≡ observed for every draw; the MC
p-value is degenerate (≡1). The page-marginal register is structurally
blind to SELECTION ORDER, which is the entire content of a page→blob scan.
(This is the mirror image of campaign #11's lesson: there value-DEPENDENT
keys washed the marginal; here value-independent keys make it invariant.)

## PB1′ — the amended registered family (everything else inherited from v1)

- D_s,p as in v1; offsets after G2 (all 228 qualify: image ≥ 14).
- **Statistic**: sliding windows W = 60, stride 30 (full windows only,
  n = 60); per-window 29-cell χ² = (29/60)Σh² − 60; family MAX over
  (page, s, window) ≈ 55×228×7 ≈ 88k windows. The window histogram
  depends on ORDER, so the null below is non-degenerate.
- **Null**: derive-from-shuffled, unchanged in spirit — each draw permutes
  each page's values (preserves c_p and every marginal EXACTLY; destroys
  order), recomputes the full grid, takes the max. Seed 20261201, stream
  and escalation (20→200 on obs ≥ median) as v1.
- **Plants**: as v1 (random (p,s*), 35-rune window, crib from the offset's
  image alphabet, self-check decode==crib) — now scored against the
  windowed statistic; power = fraction > null p95. A 35-rune plant sits
  inside a 60-rune window (dilution ×1.7, not ×7) — the window register is
  exactly the instrument lesson registered after #11.
- **Verdict / crib gate / FLAGGED-FOR-ORACLE / mandatory power sentence**:
  as v1 (p ≤ 0.05 on the single family).
- **Cost**: per draw ≈ one einsum (window-count matrices × 228 stacked
  29×29 selection matrices) — estimate <60 s for the full pipeline at
  launch; measured value reported.

## Disclosure line for the REPORT

"PB1 ran with a registered pre-output amendment (PREREG2): the v1
page-marginal statistic + derive-from-shuffled null was provably
degenerate (order-invariant statistic); no v1 output exists. Amended
statistic = windowed χ² (W60/stride30), same null, same seed, same plant
class."
