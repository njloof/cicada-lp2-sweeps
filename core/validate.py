#!/usr/bin/env python3
"""Phase 0 validation gates — the sweep runs only if every gate passes.

Page labels are BOOK pages (relabeled 2026-11-15; Dukotah/cicada3301#14):
book p50 exists but has zero runes (token table), so it carries no page file;
the unsolved rune corpus is book 0-49 + 51-55.

Gates:
  1. Corpus integrity: pages parse, no stray chars, image provenance re-verified
     (sha1 of ibotpeaches image == published hash) for book 0-56 incl. p50.
  2. Total unsolved rune count (book 0-49 + 51-55) == 12,956 (dukotah figure).
  3. Duplicate trap: no page is a prefix/substring of another (the page_27/page_44
     phantom-key-reuse trap that burned the community).
  4. Doublet count across the unsolved corpus ~= 86 (anti-doublet leak check).
     This is the corpus's HEADLINE feature, not a footnote: 86 observed vs
     ~445 expected under flat unigrams (deficit ~17 sigma; suppression ~0.81,
     leak ~0.19). Solved pages sit at 1-2.4% doublets, unsolved at 0.66% —
     the filter is the defining machine artifact of the unsolved bulk.
  5. Known-solutions regression suite (the rig must reproduce every solved text;
     extended 2026-11-18 after the external review — see docs/LEDGER.md
     Corrections; this gate must pass BEFORE any campaign launch):
       every solved section is first content-pinned (SCREAM_PINS: rune count +
       sha256[:16]) — solved status is welded to the rune string, not the page
       number, because scream314 folds 11/12 into the 10 block and 15 into 14.
       A WARNING (LP1)  atbash                       -> BELIEVE/FROM THIS/TRUE
       SOME WISDOM(LP1) identity (standard futhark)  -> PRIMES/TOTIENT/ENCRYPTED
       A KOAN     (LP1) atbash+shift+3               -> COAN/MASTER/STUDENT
       WELCOME-CONT LP1 03+04 as ONE stream: Vigenere DIVINITY, 11 wiki
                      F-skips (no key consumption), continuous key across the
                      page break (04 starts at phase 387 mod 8 = 3)
                      -> WELCOME/PILGRIM/JOURNEY + INTELLIGENCE/COMMAND
       INSTRUCTN  (LP1) atbash+shift+3               -> UNREASONABLE/EACH DAY
       10/13/16   (LP1) identity                     -> koan text (see gates)
       CIRCUMF. (LP1)   Vigenere FIRFUMFERENFE       -> LESSON/MASTER/EXPLAINED/STUDENT
       AN END   (LP2 56) phi(prime) shift-down       -> DEEPWEB/PILGRIM/HASHESTO
       PARABLE  (LP2 57) direct transliteration      -> DIUINITY/EMERGE
     F-interrupter pages: only ciphertext-F positions are ambiguous (non-F cannot
     be null), so we brute-force the 2^(#F) null/non-null assignments and require
     the expected words in the best candidate.
     LP1 pages 03/14 were listed as open leads until 2026-11-18; both solved in
     the 2014 public wave (wiki "CICADA 3301 2014 PUZZLE FACTS PART 4", 12 Jan
     2014; scream314 lineage) — the regression-suite failure mode the review
     flagged is exactly this: a decode in this file not connected to the
     open-lead list.
  6. p15 decimal grid closed form: the 16 recorded cells equal
     {|3301 - prime(F+1)| : F distinct Fibonacci 0..987}; Fibonacci order is a
     square spiral from the red 3299 = 3301 - prime(1). Grid containment and
     pointer readings are RETRACTED (values cluster in 2838-3299 by
     construction; see LEDGER Corrections C2).
Run: python3 validate.py
"""
import json, os, re, sys, hashlib, itertools

HERE = os.path.dirname(os.path.abspath(__file__))          # core/
ROOT = os.path.dirname(HERE)                                 # repo root
DATA = os.path.join(ROOT, "data")
SRC  = os.path.join(ROOT, "sources")

GEMATRIA = [("ᚠ","F",2),("ᚢ","U",3),("ᚦ","TH",5),("ᚩ","O",7),("ᚱ","R",11),("ᚳ","C",13),
            ("ᚷ","G",17),("ᚹ","W",19),("ᚻ","H",23),("ᚾ","N",29),("ᛁ","I",31),("ᛄ","J",37),
            ("ᛇ","EO",41),("ᛈ","P",43),("ᛉ","X",47),("ᛋ","S",53),("ᛏ","T",59),("ᛒ","B",61),
            ("ᛖ","E",67),("ᛗ","M",71),("ᛚ","L",73),("ᛝ","NG",79),("ᛟ","OE",83),("ᛞ","D",89),
            ("ᚪ","A",97),("ᚫ","AE",101),("ᚣ","Y",103),("ᛡ","IA",107),("ᛠ","EA",109)]
N = 29
R2I = {r: i for i, (r, _, _) in enumerate(GEMATRIA)}
TRANS = {i: t for i, (_, t, _) in enumerate(GEMATRIA)}
# structural markers: - word, / line, % page, . title, & section, $ page-end, § EOF
# digits = printed number channel on some pages (not runes; excluded from index stream)
ALLOWED = set(R2I) | set(" \n\t/-·.%⁘⁚⁖⁜&$§0123456789")

def translit(idxs): return "".join(TRANS[i] for i in idxs)

LATIN2IDX = {}
for i, (r, t, _) in enumerate(GEMATRIA):
    if len(t) == 1: LATIN2IDX[t] = i
for a, b in (("V", "U"), ("K", "C"), ("Q", "C"), ("Z", "S")):
    LATIN2IDX[a] = LATIN2IDX[b]  # rune alphabet collapses these

def load_page(n):
    p = f"{DATA}/pages/lp2_{n:02d}.txt"
    return [[int(x) for x in ln.split()] for ln in open(p) if ln.strip()]

def flat(n): return [i for ln in load_page(n) for i in ln]

def is_prime(n):
    if n < 2: return False
    for d in range(2, int(n**0.5) + 1):
        if n % d == 0: return False
    return True

def phi_prime_stream(length):
    out, p = [], 2
    while len(out) < length:
        out.append((p - 1) % N)
        p += 1
        while not is_prime(p): p += 1
    return out

def keyword_stream(key, length):
    k = [LATIN2IDX[c] for c in key]
    return [k[t % len(k)] for t in range(length)]

SCREAM = f"{SRC}/scream314/liber_primus.md"

# Content pins: (n_runes, sha256-hex[:16] of the concatenated index string) for
# every solved LP1 rune section. Pages are pinned BY CONTENT, not by number:
# scream314 folds the 11/12 text into the 10.jpg block and the 15 text into
# 14.jpg, and the 2014 wiki numbers the Welcome pages as "page 4 and 5" —
# per-JPEG triage mis-files pages, so a solved status must be welded to the
# exact rune string. Verified 2026-11-18 (rig + external review round 2).
SCREAM_PINS = {
    "Runes - 01.jpg": (184, "e4999b527224a631"),
    "03.jpg":         (394, "fe093a0ccac7eb59"),
    "04.jpg":         (121, "5ad8e046ce854f2f"),
    "05.jpg":         (157, "3090d71764e5eb53"),
    "06.jpg":         (742, "a8d7c9315a38b95d"),
    "09.jpg":         (38,  "8691617cc1d8ac94"),
    "10.jpg":         (629, "9021da2d7d507f9c"),   # block carries 11/12 text too
    "13.jpg":         (125, "07c1525452f7e568"),
    "14.jpg":         (319, "7860ffacbbd44124"),   # block ends with the 15.jpg text
    "16.jpg":         (89,  "ab2523cd4d8ce007"),
}

def scream_runes(label, sc=None):
    """Runes of a scream314 section = the indented block after the 'Runes:'
    marker. NOT the whole section: 03/04 carry the note 'Every clear text F is
    an ᚠ (F)', whose stray rune used to LEAD the extraction by one — that
    phantom is why the old WELCOME gate reported '1 null-F' (external review
    reply §6 flagged the count; fixed 2026-11-18). Sections without the marker
    (only 01) fall back to the pre-'---' extraction, content-pinned below.
    Indented prose (the garbled 'translate to' blocks) is excluded."""
    if sc is None:
        sc = open(SCREAM, encoding="utf-8").read()
    sec = [s for s in re.split(r"^## ", sc, flags=re.M) if s.startswith(label)][0]
    lines = sec.split("\n")
    marks = [j for j, l in enumerate(lines) if l.strip() == "Runes:"]
    if not marks:                                    # legacy fallback (01)
        return [R2I[c] for c in sec.split("---")[0] if c in R2I]
    out = []
    for l in lines[marks[0] + 1:]:
        if not l.startswith("    "):
            if l.strip():
                break
            continue
        cs = [c for c in l if c in R2I]
        if not cs and l.strip():
            break                                    # indented prose block
        out += [R2I[c] for c in cs]
    return out

def decode_skipnull(ct, stream, null_mask):
    """P[t] = (C[t] - K[t']) where K advances only on non-null positions;
    null positions (ciphertext F declared null) emit nothing."""
    out, ki = [], 0
    for t, c in enumerate(ct):
        if null_mask[t]: continue
        out.append((c - stream[ki]) % N); ki += 1
    return out

def decode_holdnull(ct, stream, null_mask):
    """Variant: null F passes through as plaintext F, key does NOT advance."""
    out, ki = [], 0
    for t, c in enumerate(ct):
        if null_mask[t]: out.append(0)
        else: out.append((c - stream[ki]) % N); ki += 1
    return out

def brute_interrupters(ct, stream, expect, max_f=20, rmax=None):
    """Try all null/non-null assignments over ciphertext-F positions (both null
    conventions); return best (text, words_found, convention, n_nulls).
    Early-exit: first decode only the head (enough to contain the first crib) and
    only continue full decode when the head crib matches."""
    fpos = [t for t, c in enumerate(ct) if c == 0]
    if len(fpos) > max_f: return None
    crib0 = expect[0]
    head = min(len(ct), 60 + max_f)  # crib0 may sit ~20 chars in; keep generous
    best = None
    for r in range((rmax or len(fpos)) + 1):
        for combo in itertools.combinations(fpos, r):
            cs = set(combo)
            for conv, fn in (("skip", decode_skipnull), ("hold", decode_holdnull)):
                part = fn(ct[:head], stream, [t in cs for t in range(head)])
                if crib0 not in translit(part): continue
                txt = translit(fn(ct, stream, [t in cs for t in range(len(ct))]))
                found = sum(w in txt for w in expect)
                if best is None or found > best[1]:
                    best = (txt, found, conv, r)
                if found == len(expect): return best
    return best or ("", 0, "-", -1)

def main():
    fails = []
    man = json.load(open(f"{DATA}/manifest.json"))

    # ---- Gate 1: integrity + image provenance ----
    for n in range(58):
        m = man[str(n)]
        # image provenance is checked even for the runeless p50 (file is None):
        # the image is the evidence that page exists and is what we say it is
        if m.get("published_image_sha1"):
            img = f"{SRC}/ibotpeaches/liber_primus/{n+17:02d}.jpg"
            got = hashlib.sha1(open(img, "rb").read()).hexdigest()
            ok = got == m["published_image_sha1"]
            print(f"{'PASS' if ok else 'FAIL'}  image provenance lp2_{n:02d} <- {os.path.basename(img)}")
            if not ok: fails.append(f"image {n}")
        if m["file"] is None: continue
        lines = load_page(n)
        allidx = [i for ln in lines for i in ln]
        assert all(0 <= i < N for i in allidx), f"page {n} bad index"
        assert len(allidx) == m["n_runes"], f"page {n} count drift"
    # stray-character audit of the raw canonical stream
    raw = open(f"{SRC}/dukotah/liber-primus/data/krisyotam_runes.txt", encoding="utf-8").read()
    stray = set(raw) - ALLOWED
    print(f"{'PASS' if not stray else 'FAIL'}  stream charset (stray: {stray or 'none'})")
    if stray: fails.append("charset")

    # ---- Gate 2: total ----
    total = sum(man[str(n)]["n_runes"] or 0 for n in range(56))  # book 0-55 (p50: 0)
    ok = total == 12956
    print(f"{'PASS' if ok else 'FAIL'}  unsolved total (book 0-49 + 51-55) = {total} (expect 12,956)")
    if not ok: fails.append("total")

    # ---- Gate 3: duplicate / prefix trap ----
    dup = []
    streams = {n: "".join(map(str, flat(n))) for n in range(58) if man[str(n)]["file"]}
    for a in streams:
        for b in streams:
            if a != b and streams[b].startswith(streams[a]):
                dup.append((a, b))
    ok = not dup
    print(f"{'PASS' if ok else 'FAIL'}  no page is a prefix of another {dup or ''}")
    if dup: fails.append("prefix")
    # substring check on rune-index strings (len>=50 to skip trivial short matches)
    sub = [(a, b) for a in streams for b in streams
           if a != b and len(streams[a]) >= 50 and streams[a] in streams[b]]
    print(f"{'PASS' if not sub else 'FAIL'}  no page is a substring of another {sub or ''}")
    if sub: fails.append("substring")

    # ---- Gate 4: doublet count (adjacent identical RUNE INDICES, within pages) ----
    dbl = sum(sum(1 for x, y in zip(p, p[1:]) if x == y)
              for p in map(flat, [n for n in streams if n <= 55]))  # unsolved book pages
    ok = 60 <= dbl <= 120
    print(f"{'PASS' if ok else 'FAIL'}  doublets = {dbl} (expect ~86, accept 60-120)")
    if not ok: fails.append("doublets")

    # ---- Gate 5: known-solutions regression suite ----
    # LP1 pages come from the scream314 transcription (independent of krisyotam stream)
    sc = open(SCREAM, encoding="utf-8").read()

    # 5a: content pins — every solved section must be byte-identical to the
    # rune string the decodes were verified against (numbering is not trusted)
    for label, (npin, hpin) in SCREAM_PINS.items():
        ct = scream_runes(label, sc)
        got = hashlib.sha256("".join(map(str, ct)).encode()).hexdigest()[:16]
        ok = (len(ct), got) == (npin, hpin)
        print(f"{'PASS' if ok else 'FAIL'}  pin {label}: {len(ct)} runes {got} (want {npin} {hpin})")
        if not ok: fails.append(f"pin {label}")

    # A WARNING: atbash, no interrupters
    aw = scream_runes("Runes - 01.jpg", sc)
    txt = translit([(N - 1 - c) % N for c in aw])
    exp = ["BELIEUE", "FROMTHIS", "TRUE"]  # BELIEVE: V->U in runes
    ok = all(w in txt for w in exp)
    print(f"{'PASS' if ok else 'FAIL'}  A WARNING atbash: {txt[:58]}...")
    if not ok: fails.append("AWARNING")

    # WELCOME + WELCOME CONTINUED (scream314 03+04; the 2014 wiki numbers these
    # "page 4 and 5"): ONE continuous DIVINITY stream across the page break.
    # The wiki lists 11 F-interrupters over the 515-rune join (7 in 03, 4 in 04
    # at in-page 27/49/71/120); interrupters do NOT consume key, so 04 starts
    # at phase (394-7) mod 8 = 3 — decoding 04 with a page-restarted key fails,
    # which is exactly what this gate pins (key continuity). Deterministic
    # exact-skip decode, no search: the old presence-based search early-exited
    # on cribs that all sit before the first interrupter and reported a
    # meaningless null count ("1 null-F" was a phantom note-rune, then "0").
    # Recipe: external review round 2, 2026-11-18.
    we, fo = scream_runes("03.jpg", sc), scream_runes("04.jpg", sc)
    both = we + fo
    SKIPS = [48, 74, 84, 132, 159, 160, 250, 421, 443, 465, 514]
    pt = decode_skipnull(both, keyword_stream("DIVINITY", len(both)),
                         [t in set(SKIPS) for t in range(len(both))])
    txt = translit(pt)
    ok = (len(both) == 515 and all(both[t] == 0 for t in SKIPS) and len(pt) == 504
          and all(w in txt for w in ("WELCOME", "PILGRIM", "JOURNEY",
                                     "BENGUNTOYOURSEL", "INTELLIGENCEISHOLY",
                                     "COMMANDYOUROWNSEL")))
    print(f"{'PASS' if ok else 'FAIL'}  WELCOME-CONTINUED 03+04 vigenere DIVINITY, "
          f"11 wiki skips, continuous key: {txt[:58]}...")
    if not ok: fails.append("WELCOME0304")

    # AN END: phi(prime) shift-down, from our corpus
    ae = flat(56)
    res = brute_interrupters(ae, phi_prime_stream(len(ae)),
                             ["DEEPWEB", "PILGRIM", "HASHESTO"])
    ok = res and res[1] == 3
    print(f"{'PASS' if ok else 'FAIL'}  AN END phi(prime) ({res[2]}, {res[3]} null-F): "
          f"{res[0][:58]}...")
    if not ok: fails.append("ANEND")

    # PARABLE: direct transliteration
    txt = translit(flat(57))
    ok = "DIUINITY" in txt and "EMERGE" in txt
    print(f"{'PASS' if ok else 'FAIL'}  PARABLE translit: {txt[:58]}...")
    if not ok: fails.append("PARABLE")

    # SOME WISDOM: identity under standard futhark (dukotah method "shift+0")
    txt = translit(scream_runes("05.jpg", sc))
    ok = all(w in txt for w in ("THEPRIMESARESACRED", "TOTIENT", "ENCRYPTED"))
    print(f"{'PASS' if ok else 'FAIL'}  SOME WISDOM identity: {txt[:58]}...")
    if not ok: fails.append("WISDOM")

    # A KOAN (master/student): atbash + shift+3 (dukotah method string; plain
    # mod-29 atbash alone yields garbage — the +3 is real)
    txt = translit([(N - 1 - c + 3) % N for c in scream_runes("06.jpg", sc)])
    ok = all(w in txt for w in ("ACOAN", "MASTER", "STUDENT"))
    print(f"{'PASS' if ok else 'FAIL'}  A KOAN atbash+3: {txt[:58]}...")
    if not ok: fails.append("KOAN06")

    # CIRCUMFERENCE KOAN: Vigenere FIRFUMFERENFE, interrupter search
    # (public since the 2014 wave; listed as an open lead until 2026-11-18 —
    # never again)
    ci = scream_runes("14.jpg", sc)
    res = brute_interrupters(ci, keyword_stream("FIRFUMFERENFE", len(ci)),
                             ["LESSON", "MASTER", "EXPLAINED", "STUDENT"])
    ok = res and res[1] == 4
    print(f"{'PASS' if ok else 'FAIL'}  CIRCUMFERENCE vigenere FIRFUMFERENFE "
          f"({res[2]}, {res[3]} null-F): {res[0][:58]}...")
    if not ok: fails.append("CIRCUMF")

    # AN INSTRUCTION (09): atbash+shift+3, same transform as 06
    txt = translit([(N - 1 - c + 3) % N for c in scream_runes("09.jpg", sc)])
    ok = all(w in txt for w in ("INSTRUCTIAND", "UNREASONABLE", "EACHDAY"))
    print(f"{'PASS' if ok else 'FAIL'}  INSTRUCTION atbash+3: {txt[:58]}...")
    if not ok: fails.append("INSTR09")

    # 10/13/16: identity (plain transliteration). The 10.jpg block carries the
    # 11/12 continuation and 14.jpg carries 15 — pins above weld the folds.
    for label, cribs in (("10.jpg", ("THELOSSOFDIUINITY", "CIRCUMFERENCE", "BEHAUIARSWHICH")),
                         ("13.jpg", ("SOMEWISDOM", "GREATWEALTH", "BEPREPARED")),
                         ("16.jpg", ("WESTIAN", "DISCOUERTRUTH", "FOLLOWYOURTRUT"))):
        txt = translit(scream_runes(label, sc))
        ok = all(w in txt for w in cribs)
        print(f"{'PASS' if ok else 'FAIL'}  {label} identity: {txt[:58]}...")
        if not ok: fails.append(f"IDENT{label}")

    # ---- Gate 6: p15 decimal grid closed form (external review 2026-11-18) ----
    # Recorded owner pass, 3 witnesses (docs/RED_CENSUS.md, docs/ORACLE_QUEUE.md):
    # 4x4 layout, 3299 red at row 2 col 2. Values = |3301 - prime(F+1)| over
    # distinct Fibonacci F; Fibonacci order = square spiral from the red cell
    # ((1,1)->(1,2)->(2,2)->(2,1)->(2,0)->(1,0)->(0,0)->...->(3,0)).
    # dukotah round44 reported 14/16 (signed difference); |.| gives 16/16:
    # 1206 = prime(611)-3301, 4516 = prime(988)-3301. Containment/pointer
    # readings RETRACTED — the 11 small-F cells land in 2838..3299 by
    # construction, so void-window containment was a construction artifact.
    GRID = [3258, 3222, 3152, 3038, 3278, 3299, 3298, 2838,
            3288, 3294, 3296, 2472, 4516, 1206, 708, 1820]
    FIBS = [0, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987]
    def nth_prime(k):
        n, c = 1, 0
        while c < k:
            n += 1
            if is_prime(n): c += 1
        return n
    formula = sorted(abs(3301 - nth_prime(f + 1)) for f in FIBS)
    ok = formula == sorted(GRID) and 3301 - nth_prime(1) == 3299
    print(f"{'PASS' if ok else 'FAIL'}  p15 grid = |3301-prime(Fib+1)| 16/16, origin 3299")
    if not ok: fails.append("grid16")

    print()
    if fails:
        print("GATES FAILED:", fails); sys.exit(1)
    print("ALL GATES PASS — corpus is cleared for the sweep.")

if __name__ == "__main__":
    main()
