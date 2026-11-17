# Campaign #18 report — segmentation tests

G1 stream 12956 EXACT; G2 partition EXACT; G3 void reproduced EXACTLY (86 doublets; span sites [2740, 3140, 3852, 4389], gaps [400, 712, 537], sum 1649; flanking sites 2580/4580; mean internal gap 550 vs corpus mean 151)

S1 void [2740,4389] (1650 runes) contained in ['P4']; nearest group edge distance 866; P(random 1650-window in one group) = 0.2684

S2 per-group doublets (obs/exp/z): [('P1', 4, 25.8, -4.37), ('P2', 5, 17.3, -3.01), ('P3', 1, 24.0, -4.78), ('P4', 20, 133.6, -10.0), ('P5', 8, 19.3, -2.63), ('P6', 15, 59.1, -5.84), ('P7', 12, 58.7, -6.2), ('P8', 16, 84.3, -7.57), ('P9', 5, 31.9, -4.85)]; 9/9 groups deficient, sign-test p = 0.0020

S3 dots per group {'P1': 9, 'P2': 7, 'P3': 11, 'P4': 49, 'P5': 5, 'P6': 26, 'P7': 22, 'P8': 35, 'P9': 9}; chi2 = 2.97, permutation p = 0.9364 (D=20000, seed 20261218)

S4 words n=3322; chi2 across 9 groups = 23.76, permutation p = 0.8544

Holm S2: raw p=0.0020 adj=0.0078 -> SUPPORTS

Holm S1: raw p=0.2684 adj=0.8053 -> NEUTRAL

Holm S4: raw p=0.8544 adj=1.0000 -> NEUTRAL

Holm S3: raw p=0.9364 adj=0.9364 -> NEUTRAL

VERDICT: 1 SUPPORTS, 0 REFUTES -> NO-GROUPS-EVIDENCE (segmentation stays a presentation frame; pipeline NOT restructured)

DISCLOSURES: (1) S2 WEAK DISCRIMINATION — a single stream with a global anti-repeat filter also predicts per-group deficits; the 9/9 result is consistent-with, not evidence-for, separate streams (per-group rates do vary, 0.52%-1.48%, unregistered follow-up). (2) VOID CONVENTION — #10 quoted '2739-4388'; exact sites are 2740/3140/3852/4389 (their span minus one) and the span is doublet-SPARSE (mean gap 550 vs 151), not literally zero; G3 reproduces sites+gaps EXACTLY. (3) S4 RERUN — first run had a comprehension-variable leak (tot computed for one group only); fixed pre-report, seed unchanged, verdict identical. (4) S3/S4 homogeneity is NOT a refutation (shared register possible) per PREREG §3.
