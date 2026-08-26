"""Ejecuta limpieza, estados proxy, diagnóstico, anomalías y pronóstico."""
from pathlib import Path
import runpy

root = Path(__file__).resolve().parents[1]
runpy.run_path(root / "src/radioenlace/pipeline.py", run_name="__main__")
