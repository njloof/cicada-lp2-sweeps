# Campaign #17 report — language triage


G1 separators EXACT (2,729 '-', 173 '.'); unsolved words n=3322; G2 reference n=45 solved-page English words; G3 PASS

## S1 word-length histogram bins 1/2/3/4-6/7+

unsolved: ['9.8%', '18.7%', '23.8%', '34.7%', '13.1%']  mean 3.90

English ref : ['2.2%', '17.8%', '24.4%', '42.2%', '13.3%']

## S2 short words: unsolved f1=9.8% f2<=2=28.4% | English ref f1=2.2% f2<=2=20.0%

## S3 apostrophe class (owner-marked): {'initial': 0, 'medial': 6, 'final': 0} — medial/final >0 refutes Latin (Latin has no apostrophes)

## S4 permutation chi-square: obs=3.36 p=0.5062 (D=20000, seed 20261205) → **CONSISTENT-English** (low-power disclosed: reference n=45)
