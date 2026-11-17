# Campaign #16 report — diamonds vs '.' (PREREG sweeps/2026-11-diamonds/PREREG.md)


G3 corpus L check: load_page sum = 12956 (expect 12,956 if API returns rune lists)

G2 line-count violations (page, baseline, owner): [(49, 4, 13)]

## T1 — ◆4 substitution targets (n=127)

replaced-char census: {'.': 126, 'ᛁ': 1}

rate('.'-replaced) = 0.9921 → **CONFIRMED** (thresholds ≥0.95 / <0.80)

exceptions in t1_exceptions.csv; non-◆ owner edits (quotes/dashes/breaks): 290

## T2 — large-lattice ↔ &/$/§

mark→ornament (◆size, adjacent-ornaments): [((10, '&'), 1), ((10, 'none'), 2), ((13, '$'), 1), ((13, '&'), 21), ((13, '&,&'), 2), ((13, 'none'), 8), ((23, '§'), 1)]

ornament→adjacent-large-◆ (symbol, has_adjacent): [(('$', False), 8), (('$', True), 1), (('&', True), 18), (('§', True), 1)]

## T3 — detector vs owner ◆4 counts: exact match 28/50 pages, Spearman ρ = 0.823 (descriptive)

full table: t3_detector.csv

## T4 — residual '.' (not ◆4): 19 on unsolved pages; line-final 17 (89%); red-adjacent 0 (0%)

◆4-replaced dots: 126; total baseline dots unsolved+56/57 = 145

full table: t4_residual.csv
