# LP2 page 55 — the missing page

> **SUPERSEDED 2026-11-15.** There was never a missing page. "Page 55" was
> the tail +1 shift: the runes-only extraction dropped the root's
> empty-of-runes p50 slot, so stream segs 50–56 are book pages 51–57.
> This page (72.jpg) = **book p55 = stream seg 54**, fully transcribed
> (4 lines, 76 runes, line signature [24,22,22,8] matches the image), and
> owner-adjacent p51 pairing closed 92/92. Proof:
> [STREAM_TAIL_EVIDENCE.md](STREAM_TAIL_EVIDENCE.md) · posted as
> [Dukotah/cicada3301#14](https://github.com/Dukotah/cicada3301/issues/14).
> Corpus relabeled to book numbers 2026-11-15. Text below retained as the
> historical record.

**Status (historical): untranscribed in every community lineage; untranscribable from published
images with current methods.** Excluded from all sweeps in this repo (coverage is
therefore 55/56 unsolved pages).

## The gap

- The page **image exists**: onion7 `55.jpg` = ibotpeaches `72.jpg`,
  sha1 `4f3d2d52…` (published hash verified against the ibotpeaches bytes).
  4 rune lines ≈ 70–95 runes + cicada artwork.
- Every machine-readable transcription **skips from page 54 to page 56**:
  krisyotam stream (57 `%`-segments = 0–54 + AN END + PARABLE), relikd/LiberPrayground,
  scream314. Confirmed independently by dukotah (`relikd_fp`: relikd has the p55
  *image* but no runes).

## The failed transcription attempt (2026-11-13, tools/p55_transcribe.py)

Approach: build glyph templates from the 55 *verified* pages (image bytes + known
rune labels from the stream), cross-validate, then classify page 55.

- 1,149 glyphs reconciled from 12,956 (9% of lines segment cleanly at all).
- Held-out glyph accuracy on verified pages: **46%** — hopeless.
- Diagnosis (from the page-0 line-0 band): the decorative LP font **interpenetrates** —
  X-shaped runes physically touch their neighbours, so every connected component is
  band-height, and word separators are dot-matrix ornaments. Component segmentation
  is structurally impossible, not merely hard.

This independently corroborates dukotah's dedicated glyph-reader failure on the same
page (alignment 0.145, "far into the garbage band"). Any future attempt needs a
different instrument entirely (e.g., stroke-model fitting or hand transcription by a
runologist with the high-res scan).

## Consequence for the ledger

Every negative in this repo covers LP2 0–54. If a pad or keystream relationship
involves page 55 specifically, these sweeps cannot see it.
