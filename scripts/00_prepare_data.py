"""Verifica y extrae el archivo original sin modificarlo."""
from hashlib import sha256
from pathlib import Path
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / "data/raw/Datos.zip"
DEST = ROOT / "data/raw/extracted"
EXPECTED = "786a037e749ce0c5bf7b3d8bd66f419a0a76de809c68857534e03487fc922bfa"

digest = sha256(ARCHIVE.read_bytes()).hexdigest()
if digest != EXPECTED:
    raise SystemExit(f"SHA-256 inesperado para {ARCHIVE.name}: {digest}")

DEST.mkdir(parents=True, exist_ok=True)
with ZipFile(ARCHIVE) as zf:
    for member in zf.infolist():
        target = (DEST / member.filename).resolve()
        if DEST.resolve() not in target.parents and target != DEST.resolve():
            raise SystemExit(f"Ruta insegura dentro del ZIP: {member.filename}")
    zf.extractall(DEST)

files = sorted((DEST / "Datos").glob("epmp_local_*.csv"))
if len(files) != 90:
    raise SystemExit(f"Se esperaban 90 archivos diarios y se encontraron {len(files)}")
print(f"Datos preparados: {len(files)} archivos; SHA-256 verificado.")
