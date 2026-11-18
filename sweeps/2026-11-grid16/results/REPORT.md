# Campaign #22 report — p15 grid as 16 stream pointers

G1 N=12956; G2 sites=86; G3 grid=16 recorded

S1 0-based: k=0/16 p=1.0000 | 1-based: k=0/16 p=1.0000 | expected 0.106; P(>=1)=0.101 P(>=2)=0.0050

S2 aligned-window crib hits: obs=0/16 windows; null P(>=0)=1 by construction, MC skipped

Holm: S1-0b adj_p=1.0000, S1-1b adj_p=1.0000, S2 adj_p=1.0000

VERDICT: GRID-NULL-WEAKLY-POWERED — all observed zeros; S1 near-blind (exp 0.106); S2 blind unless global alignment holds; pointer reading SUSPENDED, not retired; option (b) ink-sweep remains

S3 (report-only) 0-based window decodes:
  3258: AEEOESWUEORFCEC
  3222: URBTHOEPAEIAINEA
  3152: MPUEAPCEABAEXBA
  3038: MYEOPFOEAGHTOX
  3278: MPAEWEAYMTJTHR
  3299: BUXJUEFREAOEUI
  3298: LBUXJUEFREAOEU
  2838: ICWIAEAAENTHIIACS
  3288: THRTGBRXEWDLB
  3294: XEWDLBUXJUEF
  3296: WDLBUXJUEFREA
  2472: BNJEASSCWJIANGU
  4516: IACACAWNIAAHDB
  1206: PBTAEGDXAEOURW
  708: GTHMWYTHIATHOERFEO
  1820: ONSUNGXNEAWNGD

DISCLOSURES: (1) FIRST COMPLETED RUN INVALID (not retained): MC early-break capped beats at 101/20000 when obs=0, yielding p=0.0050 and a spurious GRID-SELECTS; true P(null>=0)=1. Fixed before this run. (2) grid seen pre-registration (owner S12 answer); pointer-semantics channel choice post-hoc to containment. (3) row-2 doublet contribution fixed at 0 by #20 glance. (4) S2 conditional on global keystream alignment (zero power under other alignments). (5) S3 shifted repeats at 3288-3299 are window overlap, not signal.
