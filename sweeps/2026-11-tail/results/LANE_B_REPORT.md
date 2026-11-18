# Campaign #24 Lane B (F10 mid-range cyclic) report

pads=25400 (k-boosts {}); top row [130.96, 32, 10, 'c112.0r', 70, 50]

obs max 131.0; null (200 draws, seed 20261225): min 101.6 med 111.9 max 136.1; p=0.0149

prong1 obs>1.1*nullmax(149.7): False; prong2 mask=both -1.0 (n=49): False; prong3 cribs []: False

decode: FFNIXUNGNGEOFPFTHUAEFJEOTHMFFFNFOEOEAFFFFUNGTHJIOEIFJOLESBLFPXTH

VERDICT: NEGATIVE — mid-range cyclic steps 29..L-29 closed (self-pairs excluded, #6 amendment inherited)

escalation (#6 rule): obs >= null median? True -> ESCALATION EXECUTED: null
extended 20 -> 200 draws (same seed, sequential stream, first 20 bit-identical
to banked values); extended null max 136.1 EXCEEDS obs 131.0 (3/200 draws
beat obs, p=0.0149) — the 20-draw "beats all" was the p-floor artifact
(1/21 = 0.0476 minimum). Verdict NEGATIVE stands on all three GO prongs.

DISCLOSURES: (1) self-pair pads excluded (#6 AMENDMENT). (2) persisted rows = top-1000 per target, not the full ~611M-window family (repo size policy). (3) shuffle stream pre-drawn single-process: bit-identical under parallel scan. (4) kmap in work/tail_f10/kmap.json. (5) runtime 291s across chunks.
