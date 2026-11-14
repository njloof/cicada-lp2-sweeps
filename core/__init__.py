"""Core instrument: gematria tables, corpus, validation, sweep kernel, MC null.

Paths are resolved relative to the repo root so every module works both as
`python3 -m core.<name>` and when imported from campaign scripts.
"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
SRC  = os.path.join(ROOT, "sources")
Q    = 29
