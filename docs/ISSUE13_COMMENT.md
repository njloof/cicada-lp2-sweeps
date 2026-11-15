<!-- POSTED 2026-11-15T04:28:19Z as
https://github.com/Dukotah/cicada3301/issues/13#issuecomment-6889165135 (author njloof).
Body below is the exact posted text. -->

Update from the issue author — this thread described our first sweep; five more campaigns have since landed in [njloof/cicada-lp2-sweeps](https://github.com/njloof/cicada-lp2-sweeps) (public ledger: `docs/LEDGER.md`). Headline, one week of wall-clock:

**The cross-page running-pad hypothesis is dead across its full known algebra.** ~329M swept alignments, six preregistered campaigns, every verdict calibrated against a per-family Monte-Carlo null of the global max (in-page-shuffled targets — never a Bonferroni band), language-agnostic χ² at the decision level (per the English-only-negative failure mode documented in your Round 18):

| # | space swept | windows | verdict |
|---|---|---|---|
| 1 | differences, fwd/rev/mirror pads | 3,798,361 | negative |
| 2 | sums + interleaved weaves | 7,522,132 | negative |
| 3 | all 26 scalings, strides, mirror-outlier audit | 63,149,262 | negative + one flag |
| 4 | 1000-draw confirmation of that flag | — | **flag retracted** (p = 0.099; 20-draw tail artifact) |
| 5 | pairwise products: stride×mirror, k×stride, k×mirror | 161,505,246 | negative |
| 6 | index consumption: all-phase drop-decimation, cyclic wrap reads (provably complete alignment coverage) | 93,231,808 | negative |

Two things in there we think are worth more to the community than the negatives themselves:

1. **A trap we demonstrated live:** campaign #5's observed 112.4 looks "elevated" against campaign #3's difference-statistic null — but its own strided-family null median is 114.2. Cross-campaign threshold borrowing crowns false hits on this corpus; every family needs its own max-null. Related: our biggest-ever flag (195.2, campaign #6) dissolved under anatomy — all 16 extreme rows were **self-pair** permutation scans, where gcd(a±1, L) fixed points of the permutation manufacture ᚠ pile-ups arithmetically, and target-shuffle nulls are structurally blind to that channel. If you're scanning permutation-style self-pads anywhere, check the gcd before believing the χ².
2. **Power probes**, so a negative can say what it can see: planting English-strength plaintext (IoC ≈ 0.066) behind a true pad recovers 7/10 in the cyclic family at the null-median threshold, and the planted window becomes the family global max. These sweeps would have found a real pad of that shape.

What would actually reopen this: page 55 (missing from every lineage), LP1 material (out of scope by design), digit/ornament-derived keystreams (position-dependent pad derivation — the last named gap), and the plaintext-side question the palindrome clues actually point to (reading-order/procedural structure, not cross-page pad geometry — #6 makes that distinction close to definitive).

All of it reproduces from a hash-anchored corpus (`metadata.json` pins corpus sha256 + seed + git rev; CI re-runs the four known decodes on every push). Happy to cross-link anything useful here — and thanks for the Round 18/22 writeups, which shaped the instrument design directly.
