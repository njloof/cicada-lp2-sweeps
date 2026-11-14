# Campaign 2026-11-p12-mirror — REPORT

Run 2026-11-14. **Pre-registered before output** (PREREG.md, committed `fea4796`,
earlier than any campaign-#4 computation). Confirmation campaign for campaign
#3's F flag (page 12). Instrument: `core/kernel.py` unchanged; campaign CLIs
committed `6e89deb`/`38103cd`. Seeds 20261116/17/18; corpus hash in metadata.json.

**Standing caveat, registered up front:** #4 sharpens how extreme p12 is under
the null; it cannot undo that the hypothesis was formed on this corpus. All
verdicts below are structural; nothing here is a solve.

## Verdict: DISSOLVED — the campaign #3 flag does not survive the sharp null

| test | statistic | observed | null (1000×, seed 20261116) | p |
|---|---|---|---|---|
| G_null (sharp F) | p12 ratio mirror_max/own-p99 | **2.418** | min 1.74 / med 2.09 / p95 2.59 / **max 3.57** | **0.099** (98/1000) |
| H_shift (prospective) | max \|Δ\|=1 share, max page | 0.2545 (p47; p12 0.2308, 4th) | min 0.228 / med 0.274 / **max 0.385** | 0.877 (p12 pairing 0.999) |
| p12 rev-χ² anatomy | rev-family max | 111.56 | min 53.9 / med 70.3 / p95 89.0 / max 126.7 | **0.003** (single-page calibration) |

Decision rule (registered): CONFIRMED iff G and H both p ≤ 0.01; SUPPORTED iff
one; else dissolved. **DISSOLVED** (G p=0.099 > 0.01; H p=0.877). The #3 20-draw test passed only because 20 draws badly under-resolved the null tail: the 20-draw max was 2.32, the 1000-draw max is 3.57, and ~10% of random 55-page corpora produce a ratio ≥ 2.418. Campaign #3's flag is downgraded to a public note: **page 12's mirror window is extreme for page 12 alone (its own null p=0.003) but roughly the 90th percentile of what a 55-page scan yields by chance — the null must match the scan, and #3's didn't finely enough.**

## The H_shift surprise (reported as found)

Prospective H ranks pages by \|Δ\|=1 **share** at their best rev alignment.
Observed leaders: p47 0.2545 (n=55), p34 0.2456 (n=57), p28 0.240 (n=50),
**p12 0.2308 (n=169)** — fourth place. All leaders but p12 sit at the minimum
window size: share has high variance in small windows, so the max-vs-max null
is dominated by them. In absolute counts p12 carries **39 ±1 hits (chance ≈ 12)**
across 169 positions; the small-window leaders carry 12–14 each. The two
statistics answer different questions — χ² (size-weighted) has crowned p12
three campaigns running; share (size-blind) does not single it out. Both
answers are reported; the registered rule uses the p-values, not the ranking.

## Robustness & descriptives (I, J — registered as context, not gates)

- **I_noise** (uniform 1..28 substitution of non-ᚠ runes; destructive proxy
  for structured glyph error): \|Δ\|=1 fraction median 0.222 / 0.219 / 0.201 at
  f=2/5/10% (obs 0.231; chance 0.069) — even the f=10% 10th-pct (0.172) stays
  2.5× chance. χ² median decays 104.9 / 98.2 / 80.3. The structure degrades
  gracefully; a transcription-artifact origin would need error rates beyond
  the tested range *and* correlated in the mirror direction.
- **J pivot**: pivot rune 88.5/261 sits 5 runes after a line-end `/` (nearest
  marks: `/` at −5, `.` at −7). Weak alignment — not on a boundary.
- **J runs**: ±1 hits are scattered (max run 2 vs null median 1; zero runs ≥3).
  No contiguous exact-shifted block; a soft statistical structure.
- **J controls**: solved plaintexts are **not silent**: ANEND56 ratio 1.49 /
  S 0.174; PARABLE57 ratio 1.69 / S 0.182 (short windows, n≥50). Moderate
  mirror excess exists in known-true LP2 material; extremeness is judged only
  against the page-specific nulls. The instrument detects structure, not
  "ciphertext-ness."

## Ledger entry

> **p12-mirror confirmation (2026-11-14, preregistered).** Sharp 1000-shuffle nulls for campaign #3's page-12 flag plus a prospective corpus-wide shifted-mirror test. G (the #3 F statistic): observed 2.418 vs null med 2.09 / max 3.57 → p=0.099. H (|Δ|=1 share, max-vs-max): p=0.88. p12-only rev-χ²: p=0.003 against its own frequency null. Registered rule → **DISSOLVED**: the #3 flag was a 20-draw resolution artifact. Structure itself is real-but-not-outlier: ±1 mirror excess survives 10% uniform corruption (frac 0.20 vs chance 0.069), is scattered (no runs ≥3), pivots 5 runes off a line break, and solved-plaintext controls fire moderately (PARABLE57 ratio 1.69) — the instrument detects structure, not intent. Covers: sharp calibration of both #3 mirror statistics; NOT covered: page 55, single-root caveat (mitigated by I_noise, not eliminated).**

## Disclosures

1. Selection caveat (registered): p12 was flagged on this corpus before #4
   existed; H is prospective in form but its motivation is the same sighting.
2. H's share statistic is size-blind; per-window counts are reported alongside
   so the reader can weigh the small-window leaders appropriately.
3. I_noise substitutes are uniform over 1..28 (mask geometry preserved); real
   transcription errors are structured — this bounds, not mimics, them.
4. Single-root transcription caveat (data/SOURCES.md) is mitigated by I_noise
   but never eliminated; page 55 remains excluded throughout.
5. H pairing deviation (disclosed): calibrate.py printed the p-value pairing p12's S against the corpus-max null; the registered pairing (corpus max 0.2545, p47) is also computed above (0.877 vs 0.999) — the verdict is identical either way.
6. The p=0.003 anatomy result carries **no** cross-page multiplicity correction; presented only to show the structure is not a frequency artifact. The corpus-level answer is G's p=0.099.
