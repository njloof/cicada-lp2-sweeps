# cicada-lp2-sweeps

Cicada 3301 **Liber Primus Part 2** cryptanalysis: pre-registered, MC-calibrated
elimination sweeps with a reproducible corpus pipeline and a public ledger.

**Headline so far:** five campaigns, ~236M swept alignments, four clean
negatives and one self-correction. The cross-page running-pad hypothesis
(an unsolved LP2 page encrypted with another page's ciphertext as a running
pad) is dead across its full known algebra: differences (#1), sums/weaves
(#2), all 26 multiplicative scalings + stride/skip consumption (#3), and the
pairwise product spaces — stride extension/strided mirrors, scaling × stride,
scaling × mirror junction (#5). A page-12 mirror outlier flagged by #3's
registered test was **publicly retracted** when campaign #4's 1000-draw
confirmation null put it at p = 0.099 — the flag was a 20-draw tail-resolution
artifact. See [docs/LEDGER.md](docs/LEDGER.md).

## Why the instrument is trustworthy

- **Language-agnostic statistic** — 29-symbol χ² vs uniform, no English adjudication
  at the decision level (deliberately avoiding the English-only-negative failure
  mode documented in [Dukotah/cicada3301](https://github.com/Dukotah/cicada3301)
  Round 18).
- **MC null of the max** — every verdict is calibrated by re-running the *identical*
  sweep on in-page-shuffled targets, never a Bonferroni band (which is
  anti-conservative for these correlated, overlapping windows). Two hard-earned
  corollaries, both learned on this corpus: nulls are **family-specific**
  (the sum statistic's null sits ~46 χ² above the difference's; a borrowed
  threshold crowns false hits — #5's L observed 112.4 would look "elevated"
  against #3's difference null but sits *below* its own strided-family median
  of 114.2), and **20-draw flags are provisional** — #4 was built solely to
  break #3's page-12 flag at 1000 draws, and succeeded. #5 added a
  pre-declared **escalation rule**: any family whose observed max reaches its
  20-draw null median is extended to ≥200 draws before a verdict ships.
- **CI-enforced trust anchor** — every push reproduces all four known LP1/LP2
  decodes (atbash, Vigenère DIVINITY, φ(prime), transliteration) plus 11 tests,
  and gates that no campaign ships results without a PREREG.md.
- **Hash-anchored corpus** — 56 page images verified against published SHA-1s;
  upstream repos pinned by SHA with content hashes (`fetch_sources.sh`).

## Reproduce

```sh
./fetch_sources.sh                      # 3 pinned community clones + hash checks
python3 -m core.build_corpus            # data/pages/*.txt + manifest (12,956 runes)
python3 -m core.validate                # ALL GATES PASS (trust anchor)
python3 -m pytest -q                    # known decodes + kernel self-tests
python3 -m core.plaintexts              # solved-page pad streams (derived)
python3 sweeps/2026-11-crosspage-pad/run.py --mirror          # the full sweep (~40 s)
python3 sweeps/2026-11-crosspage-pad/calibrate.py --mirror    # MC null (~10 min)
```

## Layout

| path | role |
|---|---|
| `docs/LEDGER.md` | the citable unit — one row per campaign, verdicts + coverage |
| `docs/NUMBERING.md`, `docs/PAGE55.md` | community findings (numbering swamp; the missing page) |
| `core/` | the instrument: corpus, validation, sweep kernel, MC null |
| `sweeps/<date-name>/` | one campaign: `PREREG.md` → `config.yaml` → `results/` → `REPORT.md` + `metadata.json` |
| `data/` | validated corpus + `SOURCES.md` (provenance, diffs, adjudications) |
| `tools/` | documented dead-ends (p55 transcription attempt) |

Campaign rules: PREREG.md before first result (CI-enforced); `metadata.json` pins
corpus hash + core rev + seed; retroactive registrations are allowed only if
clearly labeled. Campaign #1 is labeled RETROACTIVE — it predates the rule.

## Community findings

- LP2 numbering reconciled (LP1 ≠ LP2 filename collisions were corrupting claims).
- LP2 page 55 is missing from every lineage **and** untranscribable from published
  images (font interpenetration diagnosis + 46% held-out accuracy, disclosed).
- PARABLE pos-80 adjudicated ᚣ (Y) over one lineage's ᛖ (E), by plaintext context.
- Doublet count reproduced exactly: 86.

Not affiliated with Cicada 3301. Data derived from public community repos
(Dukotah, iBotPeaches, scream314 — pinned in `fetch_sources.sh`).
