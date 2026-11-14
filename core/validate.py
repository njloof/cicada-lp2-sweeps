#!/usr/bin/env python3
"""Phase 0 validation gates — the sweep runs only if every gate passes.

Gates:
  1. Corpus integrity: pages parse, no stray chars, image provenance re-verified
     (sha1 of ibotpeaches image == published hash) for LP2 0-56.
  2. Total unsolved rune count (LP2 0-54) == 12,956 (dukotah ledger figure).
  3. Duplicate trap: no page is a prefix/substring of another (the page_27/page_44
     phantom-key-reuse trap that burned the community).
  4. Doublet count across LP2 0-54 ~= 86 (order-of-magnitude anti-doublet leak).
  5. Smoke decodes (the rig must reproduce known text):
       A WARNING (LP1)  atbash                       -> BELIEVE/FROM THIS/TRUE
       WELCOME  (LP1)   Vigenere DIVINITY, subtract  -> WELCOME/PILGRIM/JOURNEY
       AN END   (LP2 56) phi(prime) shift-down       -> DEEPWEB/PILGRIM/HASHESTO
       PARABLE  (LP2 57) direct transliteration      -> DIUINITY/EMERGE
     F-interrupter pages: only ciphertext-F positions are ambiguous (non-F cannot
     be null), so we brute-force the 2^(#F) null/non-null assignments and require
     the expected words in the best candidate.
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
        if m["file"] is None: continue
        lines = load_page(n)
        allidx = [i for ln in lines for i in ln]
        assert all(0 <= i < N for i in allidx), f"page {n} bad index"
        assert len(allidx) == m["n_runes"], f"page {n} count drift"
        if m.get("published_image_sha1"):
            img = f"{SRC}/ibotpeaches/liber_primus/{n+17:02d}.jpg"
            got = hashlib.sha1(open(img, "rb").read()).hexdigest()
            ok = got == m["published_image_sha1"]
            print(f"{'PASS' if ok else 'FAIL'}  image provenance lp2_{n:02d} <- {os.path.basename(img)}")
            if not ok: fails.append(f"image {n}")
    # stray-character audit of the raw canonical stream
    raw = open(f"{SRC}/dukotah/liber-primus/data/krisyotam_runes.txt", encoding="utf-8").read()
    stray = set(raw) - ALLOWED
    print(f"{'PASS' if not stray else 'FAIL'}  stream charset (stray: {stray or 'none'})")
    if stray: fails.append("charset")

    # ---- Gate 2: total ----
    total = sum(man[str(n)]["n_runes"] or 0 for n in range(55))
    ok = total == 12956
    print(f"{'PASS' if ok else 'FAIL'}  unsolved total (LP2 0-54) = {total} (expect 12,956)")
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
              for p in map(flat, [n for n in streams if n <= 54]))
    ok = 60 <= dbl <= 120
    print(f"{'PASS' if ok else 'FAIL'}  doublets = {dbl} (expect ~86, accept 60-120)")
    if not ok: fails.append("doublets")

    # ---- Gate 5: smoke decodes ----
    # LP1 pages come from the scream314 transcription (independent of krisyotam stream)
    sc = open(f"{SRC}/scream314/liber_primus.md", encoding="utf-8").read()
    def scream_runes(label):
        sec = [s for s in re.split(r"^## ", sc, flags=re.M) if s.startswith(label)][0]
        return [R2I[c] for c in sec.split("---")[0] if c in R2I]

    # A WARNING: atbash, no interrupters
    aw = scream_runes("Runes - 01.jpg")
    txt = translit([(N - 1 - c) % N for c in aw])
    exp = ["BELIEUE", "FROMTHIS", "TRUE"]  # BELIEVE: V->U in runes
    ok = all(w in txt for w in exp)
    print(f"{'PASS' if ok else 'FAIL'}  A WARNING atbash: {txt[:58]}...")
    if not ok: fails.append("AWARNING")

    # WELCOME: Vigenere DIVINITY subtract, with interrupter search
    we = scream_runes("03.jpg")
    res = brute_interrupters(we, keyword_stream("DIVINITY", len(we)),
                             ["WELCOME", "PILGRIM", "JOURNEY"])
    ok = res and res[1] == 3
    print(f"{'PASS' if ok else 'FAIL'}  WELCOME vigenere DIVINITY ({res[2]}, {res[3]} null-F): "
          f"{res[0][:58]}...")
    if not ok: fails.append("WELCOME")

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

    print()
    if fails:
        print("GATES FAILED:", fails); sys.exit(1)
    print("ALL GATES PASS — corpus is cleared for the sweep.")

if __name__ == "__main__":
    main()
