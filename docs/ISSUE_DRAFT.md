# Outreach texts

Issue filed 2026-11-14 → https://github.com/Dukotah/cicada3301/issues/13
Wiki note posted 2026-11-14 → https://uncovering-cicada.fandom.com/wiki/Frequency_Analysis_(Liber_Primus)
(rev 44645, section "Cross-page running-pad hypothesis (2026)" placed above the
page categories; the canonical "Liber Primus Unsolved Pages" page is
sysop-protected, so the note landed on the unprotected Frequency Analysis page).

**Title:** Cross-page running-pad sweeps on LP2: ~74.5M alignments, MC-calibrated,
language-agnostic — 3 clean negatives + 1 public retraction (repo live)

**Body:**

Hi — publishing a standalone results repo that may be useful to ARMADA follow-ups,
particularly because it deliberately avoids the Round 18 failure mode (every
negative adjudicated in English):

**Repo:** https://github.com/njloof/cicada-lp2-sweeps

**Instrument.** Gematria-Primus χ² vs uniform over the 29-symbol alphabet, with a
Monte-Carlo null of the *global max* built by re-running the identical sweep on
in-page-shuffled pages (never Bonferroni — the windows are correlated and
overlapping). No language assumption at the decision level: a hit is a hit in any
plaintext language, and the null is language-free too. Corpus is hash-anchored
(56/56 image SHA-1s, pinned upstream SHAs, CI reproduces all four known decodes
from a fresh clone).

**What was swept** (docs/LEDGER.md has the citable rows; each campaign is
pre-registered before output, CI-gated):

1. **Cross-page difference pads** (C_M − C_N, every ordered page pair, every
   offset, pads forward/reverse/mirror-junction): 3.8M windows — negative.
2. **Pad transforms** (sums — covering subtractive and atbash pads; 2-way weaves;
   per-page audits): 7.5M windows — negative.
3. **Pad algebra** (all 26 multiplicative scalings k·C_N; stride/skip
   consumption C_N[g·t], g∈{2,3} + reversed — the `skip_by_two` analog flagged as
   uncovered in your repo: now closed negative; page-level mirror-outlier audit):
   63.1M windows — negative on the sweep families.
4. **A public self-correction:** campaign 3's registered test flagged page 12
   (mirror-window ratio 2.418 > 20-draw null max 2.32, p≤0.048). Campaign 4 was
   pre-registered solely to break that flag at 1000 draws — and did (p = 0.099;
   1000-draw null max 3.57). The flag is retracted in the ledger, with the
   p12 structure documented as real-but-not-outlier (±1 gematria-adjacency
   excess 23% vs 7% chance, survives 10% uniform corruption; single-page χ²
   p = 0.003 but ~90th percentile corpus-wide).

**Two methodology findings worth stealing regardless of verdict:**
- **Nulls are family-specific.** The sum-statistic null sits ~46 χ² above the
  difference-statistic null; a borrowed threshold crowns four false hits on our
  data. Calibrate per family, per scan.
- **≤20-draw flags are provisional.** 20 draws badly under-resolve max-statistic
  tails. Any flag from a coarse null deserves a dedicated confirmation campaign
  before it circulates as a lead.

**Known limitations, disclosed in-repo:** campaign #1 predates our PREREG rule
(labeled RETROACTIVE); all transcriptions trace to a single 2017 root (rtkd/iddqd
lineage — replication across independent lineages is impossible; we substitute a
noise-robustness study); LP2 page 55 is missing from every lineage and
untranscribable from published images (font interpenetration, 46% held-out
glyph accuracy — documented).

Happy to coordinate on numbering (docs/NUMBERING.md reconciles the LP1/LP2
filename-collision swamp) or on the remaining gaps: non-uniform interleavings,
position-dependent pad derivations (digit/ornament channels), LP1-as-pad.

— njloof

---
# Note → Uncovering Cicada wiki (posted 2026-11-14, rev 44645 on "Frequency Analysis (Liber Primus)")

"Cross-page running-pad hypothesis (2026)" section as posted:

> Systematic elimination sweeps (2026-11, [njloof/cicada-lp2-sweeps](https://github.com/njloof/cicada-lp2-sweeps))
> tested whether unsolved LP2 pages were encrypted using other LP2 pages'
> ciphertext as running pads — differences, sums, weaves, all 26 multiplicative
> scalings, and stride/skip consumption, across every ordered page pair and
> offset (~74.5M alignments). All families are negative against Monte-Carlo
> nulls of the global maximum (language-agnostic 29-symbol χ²). A page-12
> mirror-window flag raised by the third sweep was publicly retracted when a
> pre-registered 1000-shuffle confirmation null put it at p = 0.099; the
> underlying ±1 gematria-adjacency excess (23% vs 7% chance) is documented as
> real-but-not-outlier structure. Campaigns are pre-registered with CI-enforced
> PREREG gates; corpus pipeline reproduces all four known decodes from a clean
> clone. Not a solve; an elimination map with disclosed coverage and gaps.
