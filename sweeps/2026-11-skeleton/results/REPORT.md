# Campaign #21 report — separator-skeleton qualification

G1 PASS: N=12956; census {'◆13': 32, '"': 14, "'": 3, 'dot': 148, '◆4': 129, '◆10': 3, '◆23': 1}

G3 PASS: decode len 91, null-F at CT (47,)

canonical: p56 91 letters/25 words (stream 91); p57 101 letters/21 words (stream 100)

G2 p57: dashes 16/16 aligned (of 16; 0 outside verified); marks 3/3 -> PASS

V1: dashes n=15 aligned k=15; verified gaps G=78, slots B=19; excluded (unverified region) [51, 56, 57, 60, 93, 97]; block-vs-relikd disagreements [23]; hypergeometric p = 8.874e-13

V2 p56: true score -0.615, beaten by 0/1000 shuffles

V2 p57: true score 0.677, beaten by 0/1000 shuffles

V3 (report-only):
  Q1: words 174, mean len 4.24; sentences 33, mean 5.3 words
  Q2: words 280, mean len 4.15; sentences 56, mean 5.0 words
  Q3a: words 413, mean len 4.25; sentences 80, mean 5.2 words
  Q3ax: words 41, mean len 3.95; sentences 8, mean 5.1 words
  Q3b: words 441, mean len 3.99; sentences 79, mean 5.6 words
  Q4: words 253, mean len 4.07; sentences 47, mean 5.4 words
  Q5: words 353, mean len 4.11; sentences 69, mean 5.1 words
  Q6: words 428, mean len 3.97; sentences 81, mean 5.3 words
  Q7a: words 614, mean len 4.08; sentences 117, mean 5.2 words
  Q7b: words 136, mean len 3.96; sentences 26, mean 5.2 words
  Q7c: words 76, mean len 4.08; sentences 15, mean 5.1 words

VERDICT: SKELETON-QUALIFIED — separator skeleton adopted as crib constraint set (word lengths, sentence breaks, quotes, merged alphabet)

DISCLOSURES: (1) design-pass peek (PREREG). (2) FIRST COMPLETED RUN WAS INVALID (pre-fix, not retained as output): canonical anchor matched 'FIND AN END' in the WELCOME text (4,727-letter blob), hyper_p summed the LOWER tail (p=1.0), and the relikd cross-check truncated at the hash marker; all three fixed before this run. (3) PREREG arithmetic note 'canonical 91 > stream 85' was a rune-vs-letter error: 85 runes -> 91 letters via TH/NG/EO digraphs; lengths match exactly. (4) signed-file mid-word wraps repaired by the dictionary rule in _join_run (/usr/share/dict/words) — post-registration instrument detail. (5) mid-tail unverified region: excluded dashes listed above. (6) shuffles = weak null; V3 descriptive only.
