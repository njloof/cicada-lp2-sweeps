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

## Findings — visual pass, tail pages (2026-11-15)

**p49 RESOLVED — no missing runes.** Image (66.jpg) = 3 rune lines + a 10×8
Latin token table + tree ornaments + red dot-matrix. The FFT "13 visible
rows" counted the token rows. Stream seg 49 (62 runes, 3 lines) matches.
The owner's I/l ambiguities were in the TOKEN font (sans-serif 1/l, 0/O),
not the rune lines.

**Token tables = a payload, already characterized by dukotah.** pp49–51
carry base-60 two-char tokens (byte = d0·60+d1; lowercase-f value 41 never
occurs — the F-skip fingerprint). 80+104+72 = 256 tokens = a 2048-bit
high-entropy pad; not a prime, not a polyalphabetic key over any runic
page, not text (Campaign VII); hash-structure and keystream-correlation
leads null (Campaign IX). **6 of 256 bytes are contested between the three
witnesses (relikd / scream314-tokens / scream314-decimals) — indices 25,
175, 182, 199, 215, 237 — and dukotah says the master images are needed to
adjudicate: exactly the sans-serif 1/l/0/O class the owner is seeing.**
A visual pass over those 6 cells closes an open dukotah item.

**TAIL SEGMENTATION DEFECT (first systematic stream issue found).**
Image p50 = pure 13×8 token table, ZERO runes — yet stream seg 50 holds 89
runes/3 lines. Image p51 = 9×8 table + 4 rune lines. Seg 50's first line
(ᛗᚢ-ᚪᛈᛡ-…) does not match p51's first rune line (ᛈᛈᛋ-ᚠᛉᛏ-…) in shape or
word grouping. Image p55 (72.jpg) = 4 rune lines + red dot-matrix + a GRAY
BINARY-TREE DIAGRAM + cicada plate; seg 54 = 4 lines/74 runes (line counts
agree, groupings unverified). Hypothesis: the stream skips the runeless
book p50, shifting segs 50–54 by +1 — but the seg-50/p51 line mismatch
means it is shift-with-corruption, not a clean shift. Consequences if
confirmed: campaign page labels ≥50 are off by one (content statistics
unaffected — arrays were scanned correctly, only named wrong); "page 55
not covered" is false (it is our "54"); the stream's tail dividers are
unreliable. **Decider: transcribe p51's 4 rune lines (crops ready at
work/audit/p51_runes/rune_0..3.png) and pair against segs 50/51.**

**Ornaments = pre-declared untested channel (ours: not-covered list;
dukotah round43 lead 8: "p32/p55 tree anomalies cross-mirror diff (low
prior)", lead 6: "dot constellations census" — both never run).** The
most data-like ornament features: dot clusters beside each tree (filled vs
hollow counts differ left/right and across pages), red dot-matrices
(p49, p55 — color is in NO transcription), and the p55 gray branching
diagram. Trees plausibly frame the payload pages thematically; the dot
clusters are the better stego candidate.
