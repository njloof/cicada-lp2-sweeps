# Pending instrument audit: rune→index transcription fidelity

**Status: harness live (2026-11-15) — `scripts/audit/make_checklist.py`;
machine triage pass 1 done (structural only, work/audit/SUMMARY.md,
30/55 row-count agreement, 25 pages ranked for the human visual pass);
visual pass not yet run, not yet a campaign.** Raised when asked whether the
visual-rune → ciphertext transcriptions our analyses run on need verification.
Short answer: yes — it is the last unquantified systematic risk to all six
campaign negatives.

## What is already verified

- **Image layer:** all 56 published LP2 page images re-hashed against published
  SHA-1s (Phase 0; CI re-checks). The bytes we anchor to are the real pages.
- **Solved chains:** CI reproduces all four known decodes (atbash, Vigenère
  DIVINITY, φ(prime), transliteration), which validates the transcription of
  the *solved* material (LP1 pages, LP2 56/57) at the functional level.
- **One adjudicated error found and fixed:** PARABLE pos-80 ᛖ→ᚣ (data/SOURCES.md).

## What is NOT verified

- **The 55 unsolved pages (0–54) rest on a single 2017 root.** dukotah's
  `analysis/transcription/TRANSCRIPTION-VERDICT.md` establishes that *every*
  machine-readable LP2 transcription (krisyotam, relikd, wiki, cadrypt,
  scream314 — and therefore our `data/pages/`, which is the krisyotam stream)
  descends from one 2017 transcription (rtkd/iddqd). **Cross-lineage diffs buy
  nothing** — they agree because they are copies. The only independent check is
  visual re-verification against the published images.
- The error rate on unsolved pages has never been estimated. Known residue:
  scream314's "dump 23–26" section (1,021 runes) absent from the stream
  (unresolved; stream wins by image-hash anchoring).

## Why it matters for the ledger

Every negative is conditioned on transcription fidelity. One wrong rune at
position *x* corrupts every swept window covering *x*, biasing χ² **down** —
errors can only hide a true hit, not manufacture one (the #6 195.2 flag was
arithmetic, not transcription). Since our true-hit detection threshold sits
near the null max (power probe: planted windows recover at χ² ≈ 121–141 vs
null median ≈ 102–107), a handful of errors in the right place is exactly the
budget that could bury a real pad. The negatives are honest *conditional*
statements; the audit measures the condition.

## Planned checks (campaign #7-candidate: instrument audit, not a sweep)

1. **Confusion-pair visual census.** Re-read pages by hand/OCR against the
   published images, prioritized by historic leader load (49, 7, 12, 4, 6, 10,
   32, 35, 45 — pages that carried maxima or flags). Deliverable: per-page
   disagreement count, per-rune-pair confusion table (expect ᚦ/ᛈ, ᚫ/ᚪ, ᛖ/ᚣ-class
   pairs), and an estimated per-rune error rate ε.
2. **Sensitivity rescan.** Inject confusion-pair errors at rate ε into shuffled
   corpora and re-run one family's null + observed max; report how far the
   family max moves per error. Deliverable: a robustness margin — "a true pad
   of strength X survives up to ~k errors per page."
3. **Resolve the scream314 dump 23–26 discrepancy** while the images are open.

Cost: item 1 is human-hours, not machine-time; item 2 ≈ one 50-min family run
per ε level; item 3 is bounded. Run before any future campaign whose decision
threshold sits within ~10 χ² of the null max.
