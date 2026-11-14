#!/usr/bin/env python3
"""Build the validated LP2 corpus from community sources (Phase 0).

Sources (fetched 2026-11-13, see data/SOURCES.md):
  - Dukotah/cicada3301  data/krisyotam_runes.txt  (canonical rune stream, % page breaks, / line breaks)
  - Dukotah/cicada3301  dataset/liber_primus.json  (published image hashes, gematria, solved refs)
  - iBotPeaches/cicada_3301  liber_primus/*.jpg    (published page images, unified numbering = onion7 + 17)
  - iBotPeaches/cicada_3301  liber_primus/markdown/74.md (PARABLE, independent transcription)
  - scream314/cicada3301  liber_primus.md           (solved-page ciphertexts + plaintexts)

Numbering (reconciled — see SOURCES.md):
  LP2 page N = onion7 file N.jpg = ibotpeaches file (N+17).jpg.
  LP2 0-54   = krisyotam stream segments 0-54   (12,956 runes, unsolved)
  LP2 55     = MISSING from every community transcription (image exists: 72.jpg)
  LP2 56     = AN END   (krisyotam segment 55; SOLVED, phi(prime) keystream)
  LP2 57     = PARABLE  (krisyotam segment 56; SOLVED, direct transliteration)

Output: data/pages/lp2_NN.txt  (rune indices, space-separated, one transcription line per line)
        data/manifest.json     (per-page metadata + hashes)
Run: python3 -m core.build_corpus   (from repo root, after ./fetch_sources.sh)
"""
import json, hashlib, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))          # core/
ROOT = os.path.dirname(HERE)
SRC  = os.path.join(ROOT, "sources")
OUT  = os.path.join(ROOT, "data")

KRIS   = f"{SRC}/dukotah/liber-primus/data/krisyotam_runes.txt"
DATSET = f"{SRC}/dukotah/liber-primus/dataset/liber_primus.json"
IBOT   = f"{SRC}/ibotpeaches/liber_primus"
SCREAM = f"{SRC}/scream314/liber_primus.md"

RUNE_CHARS = set("ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛄᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛟᛞᚪᚫᚣᛡᛠ")
GEMATRIA_RUNES = "ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛄᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛟᛞᚪᚫᚣᛡᛠ"  # index order, verified below

def sha1(b): return hashlib.sha1(b).hexdigest()

def main():
    ds = json.load(open(DATSET))
    # verify gematria order matches our table
    assert [e["rune"] for e in ds["gematria"]] == list(GEMATRIA_RUNES), "gematria order mismatch"
    rune_to_idx = {r: i for i, r in enumerate(GEMATRIA_RUNES)}

    # --- canonical stream: krisyotam, % page breaks, / line breaks ---
    raw = open(KRIS, encoding="utf-8").read()
    segs = [s for s in raw.split("%") if any(c in RUNE_CHARS for c in s)]
    assert len(segs) == 57, f"expected 57 segments, got {len(segs)}"

    # cross-check against dataset JSON (flattened) — must be rune-identical
    dsr = {p["page"]: p["runes"] for p in ds["pages"]}
    for i, seg in enumerate(segs):
        flat = "".join(c for c in seg if c in RUNE_CHARS)
        assert flat == dsr[i], f"segment {i} != dataset entry {i}"

    # cross-check PARABLE against ibotpeaches independent copy (adjudicated: duk/ibot agree vs scream314)
    ib = open(f"{IBOT}/markdown/74.md", encoding="utf-8").read()
    ib_parable = "".join(c for c in ib.split("```")[1].split("####")[0] if c in RUNE_CHARS)
    seg_parable = "".join(c for c in segs[56] if c in RUNE_CHARS)
    assert ib_parable == seg_parable, "PARABLE disagrees with ibotpeaches copy"

    os.makedirs(f"{OUT}/pages", exist_ok=True)
    manifest = {}
    for i, seg in enumerate(segs):
        # map stream segment -> LP2 page: 0-54 identity; 55->56 (AN END), 56->57 (PARABLE)
        lp2 = i if i <= 54 else i + 1
        lines = []
        for ln in seg.split("/"):
            idxs = [rune_to_idx[c] for c in ln if c in RUNE_CHARS]
            if idxs: lines.append(idxs)
        flat = [i for ln in lines for i in ln]
        name = f"lp2_{lp2:02d}.txt"
        with open(f"{OUT}/pages/{name}", "w") as f:
            f.write("\n".join(" ".join(map(str, ln)) for ln in lines) + "\n")
        status = "unsolved" if lp2 <= 54 else "solved"
        # published image hash by TRUE lp2 number: dataset entry N carries image N.jpg's
        # published hash (entry labels are correct for images; only the runes pairing was off)
        manifest[lp2] = {
            "file": f"pages/{name}",
            "onion7": f"{lp2}.jpg",
            "ibotpeaches": f"{lp2+17}.jpg",
            "n_runes": len(flat),
            "n_lines": len(lines),
            "n_f": flat.count(0),
            "status": status,
            "runes_sha1": sha1("".join(map(str, flat)).encode()),
            "published_image_sha1": ds["pages"][lp2]["image"].get("published_sha1") if lp2 <= 56 else None,
        }
    manifest[55] = {  # the hole
        "file": None, "onion7": "55.jpg", "ibotpeaches": "72.jpg",
        "n_runes": None, "n_lines": 4, "n_f": None,
        "status": "unsolved_UNTRANSCRIBED",
        "note": "Image exists and is ~70 runes, but this page is absent from krisyotam, "
                "scream314 and relikd lineages (all jump 54->56). Excluded from sweep.",
        "published_image_sha1": ds["pages"][55]["image"].get("published_sha1"),
    }
    total = sum(m["n_runes"] for k, m in manifest.items() if k <= 54 and m["n_runes"])
    manifest["_corpus"] = {
        "unsolved_total_runes_0_54": total,
        "gematria": [{"index": i, "rune": r, "prime": e["prime"]}
                     for i, (r, e) in enumerate(zip(GEMATRIA_RUNES, ds["gematria"]))],
        "interrupter": "ᚠ",
    }
    with open(f"{OUT}/manifest.json", "w") as f:
        json.dump(manifest, f, indent=1)
    print(f"corpus written: {total} runes across pages 0-54; "
          f"AN END={manifest[56]['n_runes']} PARABLE={manifest[57]['n_runes']}; page 55 missing")

if __name__ == "__main__":
    main()
