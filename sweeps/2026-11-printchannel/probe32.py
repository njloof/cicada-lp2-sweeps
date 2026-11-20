#!/usr/bin/env python3
"""#32 preflight: studio venv imaging stack + disk + provenance file present."""
import os, shutil, sys
for mod in ("numpy", "PIL", "scipy"):
    try:
        m = __import__(mod)
        print(mod, getattr(m, "__version__", "?"))
    except ImportError:
        print(mod, "MISSING")
print("cwd:", os.getcwd())
print("provenance:", os.path.exists("sources/dukotah/liber-primus/analysis/stego/provenance.json"))
hdu, _, _ = shutil.disk_usage(".")
print(f"free: {hdu/1e9:.1f} GB")
