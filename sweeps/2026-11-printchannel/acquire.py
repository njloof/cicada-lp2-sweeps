#!/usr/bin/env python3
"""#32 acquire: onion JPEGs from Internet Archive + G0 sha1 vs dukotah provenance.
Run on studio: scripts/studio.sh run sweeps/2026-11-printchannel/acquire.py
Images land in work/images/ (gitignored, never pulled)."""
import hashlib, json, os, sys, time, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
BASE = "https://archive.org/download/ky2khlqdf7qdznac.onion"
OUT = os.path.join(ROOT, "work", "images")

def sha1(p):
    h = hashlib.sha1()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

def main():
    os.makedirs(OUT, exist_ok=True)
    prov = json.load(open(os.path.join(
        ROOT, "sources/dukotah/liber-primus/analysis/stego/provenance.json")))
    want = {r["page"]: r["sha1"] for r in prov["rows"]}
    print(f"provenance rows: {len(want)} (pages {min(want)}..{max(want)})")
    t0 = time.time(); receipt = {}; fails = []
    for page in sorted(want):
        dst = os.path.join(OUT, f"{page}.jpg")
        if not (os.path.exists(dst) and os.path.getsize(dst) > 10000):
            for attempt in range(4):
                try:
                    urllib.request.urlretrieve(f"{BASE}/{page}.jpg", dst + ".part")
                    os.replace(dst + ".part", dst)
                    break
                except Exception as e:
                    if attempt == 3:
                        raise
                    print(f"p{page} retry {attempt}: {e}"); time.sleep(3 * (attempt + 1))
        got = sha1(dst)
        ok = got == want[page]
        receipt[page] = {"sha1": got, "ok": ok}
        if not ok: fails.append(page)
        if page % 10 == 0:
            print(f"p{page} ok={ok} ({time.time()-t0:.0f}s)")
    json.dump(receipt, open(os.path.join(HERE, "results", "acquire_receipt.json"), "w"), indent=1)
    print(f"G0: {len(want)-len(fails)}/{len(want)} sha1 EXACT; fails={fails} "
          f"({time.time()-t0:.0f}s)")
    sys.exit(0 if not fails else 1)

if __name__ == "__main__":
    os.makedirs(os.path.join(HERE, "results"), exist_ok=True)
    main()
