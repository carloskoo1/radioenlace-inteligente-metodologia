"""Ejecuta bootstrap por bloques, explicabilidad y análisis radio–clima."""
from pathlib import Path
import runpy

root = Path(__file__).resolve().parents[1]
runpy.run_path(root / "src/radioenlace/extended.py", run_name="__main__")
