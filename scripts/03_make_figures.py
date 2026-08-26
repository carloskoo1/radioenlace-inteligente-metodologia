"""Regenera las figuras publicables a partir de las tablas de resultados."""
from pathlib import Path
import os
import runpy

root = Path(__file__).resolve().parents[1]
os.environ.setdefault("MPLCONFIGDIR", str(root / ".mplconfig"))
runpy.run_path(root / "src/radioenlace/figures.py", run_name="__main__")
