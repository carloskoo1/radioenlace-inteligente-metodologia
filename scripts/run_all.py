"""Ejecuta el flujo completo en el orden metodológico declarado."""
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
steps = ["00_prepare_data.py", "01_run_core.py", "02_run_extended.py", "03_make_figures.py", "verify_outputs.py"]
for step in steps:
    print(f"\n=== {step} ===", flush=True)
    subprocess.run([sys.executable, str(ROOT / "scripts" / step)], cwd=ROOT, check=True)
print("\nFlujo reproducido correctamente.")
