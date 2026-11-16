#!/usr/bin/env python3
"""Build the validated LP2 corpus from community sources (Phase 0).

Sources (fetched 2026-11-13, see data/SOURCES.md):
  - Dukotah/cicada3301  data/krisyotam_runes.txt  (canonical rune stream, % page breaks, / line breaks)
  - Dukotah/cicada3301  dataset/liber_primus.json  (published image hashes, gematria, solved refs)
  - iBotPeaches/cicada_3301  liber_primus/*.jpg    (published page images, unified numbering = onion7 + 17)
  - iBotPeaches/cicada_3301  liber_primus/markdown/74.md (PARABLE, independent transcription)
  - scream314/cicada3301  liber_primus.md           (solved-page ciphertexts + plaintexts)

Numbering (reconciled — see SOURCES.md; TAIL RELABELED 2026-11-15,
upstream Dukotah/cicada3301#14 — see docs/STREAM_TAIL_EVIDENCE.md):
  LP2 book page N = onion7 file N.jpg = ibotpeaches file (N+17).jpg.
  Stream segment -> book page: 0-49 identity; 50-54 -> 51-55 (the tail +1
  shift: the runes-only extraction dropped the root's empty-of-runes p50
  slot and renumbered the tail); 55 -> 56 (AN END), 56 -> 57 (PARABLE).
  Book p50 has NO segment — zero runes; it is the 13x8 base-60 token table
  (67.jpg), part of the pp49-51 pad candidate.
  Unsolved rune corpus: book 0-49 + 51-55 = 12,956 runes, 55 pages.

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
        # map stream segment -> BOOK page (relabeled 2026-11-15): identity to 49,
        # then +1 throughout: segs 50-54 -> 51-55 (tail shift), 55->56, 56->57.
        lp2 = i if i <= 49 else i + 1
        lines = []
        for ln in seg.split("/"):
            idxs = [rune_to_idx[c] for c in ln if c in RUNE_CHARS]
            if idxs: lines.append(idxs)
        flat = [i for ln in lines for i in ln]
        name = f"lp2_{lp2:02d}.txt"
        with open(f"{OUT}/pages/{name}", "w") as f:
            f.write("\n".join(" ".join(map(str, ln)) for ln in lines) + "\n")
        status = "unsolved" if i <= 54 else "solved"
        # published image hash by TRUE book number: dataset entry N carries image
        # N.jpg's published hash (entry labels were always correct for images;
        # pre-relabel, only the runes pairing was off). Now content matches label.
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
    manifest[50] = {  # the real hole: a book page with zero runes
        "file": None, "onion7": "50.jpg", "ibotpeaches": "67.jpg",
        "n_runes": 0, "n_lines": 0, "n_f": None,
        "status": "no_runes_token_page",
        "note": "Book p50 = 13x8 base-60 token table (with pp49/51 the 256-token "
                "2048-bit pad candidate), zero runes. The rtkd root has a slot for "
                "it; the runes-only extraction into krisyotam dropped the empty "
                "slot, causing the tail +1 shift (Dukotah/cicada3301#14). "
                "Excluded from rune sweeps; token payload under visual audit.",
        "published_image_sha1": ds["pages"][50]["image"].get("published_sha1"),
    }
    total = sum(m["n_runes"] for k, m in manifest.items() if k <= 55 and m["n_runes"])
    manifest["_corpus"] = {
        "unsolved_total_runes": total,  # book pages 0-49 + 51-55
        "relabel_2026_11_15": "stream segs 50-54 relabeled to book pages 51-55 "
                              "(tail +1 shift proven in docs/STREAM_TAIL_EVIDENCE.md, "
                              "posted as Dukotah/cicada3301#14); old labels lp2_50..54 "
                              "= book lp2_51..55; pre-relabel result CSVs need -0/+1 "
                              "on ids 50-54 when citing book pages",
        "gematria": [{"index": i, "rune": r, "prime": e["prime"]}
                     for i, (r, e) in enumerate(zip(GEMATRIA_RUNES, ds["gematria"]))],
        "interrupter": "ᚠ",
    }
    with open(f"{OUT}/manifest.json", "w") as f:
        json.dump(manifest, f, indent=1)
    print(f"corpus written: {total} runes across book pages 0-49 + 51-55; "
          f"AN END={manifest[56]['n_runes']} PARABLE={manifest[57]['n_runes']}; "
          f"p50 = runeless token page")

if __name__ == "__main__":
    main()
