"""Consulta de telemetría RF en respaldos ZIP ya descargados, sin extracción ni escrituras.

La fuente es el CSV integrado de 6 GHz. Los datos observados proceden del respaldo
y NO constituyen telemetría RF en vivo ni validación de los modelos de Ubelser.
"""
from collections import deque
from datetime import datetime, timezone
from pathlib import Path
from zipfile import ZipFile, BadZipFile
import csv
import io
import re


BACKUP_CSV = "scientific_campaign_6g_integrated.csv"
BACKUP_NAME_RE = re.compile(r"^backup_CU01_\d{8}_\d{6}\.zip$", re.I)


def _date(value):
    try:
        v = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
        return v if v.tzinfo else None
    except (TypeError, ValueError):
        return None


def default_backup_directory():
    """Solo detección local; no consulta red ni Controlador."""
    candidate = Path("G:/Mi unidad/AtmosLink_Backups_UNC/CU01/field")
    return candidate if candidate.is_dir() else None


def read_recent_backup(directory, limit=180):
    """Lee últimos registros válidos sin extraer bases ni modificar respaldos."""
    if not directory:
        return {"status": "unconfigured", "message": "Directorio de respaldos no configurado.", "rows": []}
    folder = Path(directory).expanduser()
    if not folder.is_dir():
        return {"status": "missing", "message": "No existe el directorio de respaldos indicado.", "rows": []}
    archives = sorted((f for f in folder.glob("backup_CU01_*.zip")
                       if BACKUP_NAME_RE.match(f.name)), key=lambda f: f.name, reverse=True)
    if not archives:
        return {"status": "empty", "message": "No se encontraron respaldos CU01.", "rows": []}
    limit = max(1, min(int(limit), 720))
    last_error = None
    # Si se está copiando un ZIP nuevo, ignorarlo y recurrir a una copia anterior.
    for archive in archives[:4]:
        try:
            if archive.stat().st_size < 1024:
                continue
            with ZipFile(archive) as z:
                if BACKUP_CSV not in z.namelist():
                    last_error = "Respaldo sin CSV científico de RF integrado."
                    continue
                info = z.getinfo(BACKUP_CSV)
                if info.file_size > 700_000_000:
                    last_error = "CSV sobrepasa el límite de lectura segura."
                    continue
                buff = deque(maxlen=limit)
                with z.open(info) as stream:
                    reader = csv.DictReader(io.TextIOWrapper(
                        stream, encoding="utf-8-sig", errors="replace", newline=""))
                    required = {"rf_timestamp_local", "frequency_band", "dl_rssi_dbm",
                                "dl_snr_db", "dl_mcs", "reported_dl_link_rate_mbps"}
                    if not required.issubset(set(reader.fieldnames or [])):
                        last_error = "Columnas RF requeridas ausentes."
                        continue
                    count = 0
                    for rec in reader:
                        count += 1
                        if count > 300_000:
                            raise ValueError("Límite de filas para lectura del respaldo excedido.")
                        if rec.get("field_analysis_valid") != "1":
                            continue
                        stamp = _date(rec.get("rf_timestamp_local"))
                        if not stamp:
                            continue
                        if rec.get("frequency_band") != "6_GHZ":
                            continue
                        if rec.get("collection_status") and "OPERATIONAL" not in rec["collection_status"]:
                            continue
                        buff.append({
                            "timestamp_local": rec.get("rf_timestamp_local"),
                            "rssi_dl_dbm": rec.get("dl_rssi_dbm"),
                            "snr_dl_db": rec.get("dl_snr_db"),
                            "mcs_dl": rec.get("dl_mcs"),
                            "rate_dl_mbps": rec.get("reported_dl_link_rate_mbps"),
                        })
                records = sorted(buff, key=lambda r: r["timestamp_local"])
                if not records:
                    last_error = "El respaldo no contiene observaciones RF 6 GHz válidas."
                    continue
                last = _date(records[-1]["timestamp_local"])
                age = (datetime.now(timezone.utc) - last.astimezone(timezone.utc)).total_seconds()
                return {
                    "status": "backup", "message": "Respaldo histórico reciente (no en vivo)",
                    "rows": records, "last_timestamp": records[-1]["timestamp_local"],
                    "age_seconds": age, "source": "backup",
                    "backup_name": archive.name,
                    "backup_timestamp": datetime.fromtimestamp(
                        archive.stat().st_mtime, timezone.utc).astimezone().isoformat(),
                    "config": {"frequency_band": "6_GHZ", "channel_bandwidth_mhz": None},
                }
        except (BadZipFile, OSError, ValueError, EOFError, csv.Error, UnicodeError) as exc:
            last_error = type(exc).__name__
    return {"status": "error", "message": last_error or "No hay respaldos legibles.",
            "rows": []}
