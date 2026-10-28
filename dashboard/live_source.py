"""Fuente de telemetría actual, exclusivamente de lectura.

Lee únicamente la base local de AtmosLink cuando el administrador la configura.
No establece conexiones con radios, no modifica SQLite y no ejecuta modelos.
"""
from contextlib import closing
from datetime import datetime, timezone
from pathlib import Path
import sqlite3


def _parse_time(value):
    if not value:
        return None
    try:
        dt = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
        return dt if dt.tzinfo else None
    except (TypeError, ValueError):
        return None


def read_recent_ap(db_path, limit=180, stale_after_seconds=300):
    """Devuelve registros AP de lectura sola, estado y antigüedad de la fuente.

    Nunca mezcla AP con SM ni publica direcciones IP/identificadores.
    Un fallo de lectura es reportado y no se disfraza como ausencia de fallas.
    """
    if not db_path:
        return {"status": "unconfigured", "message": "Defina UBELSER_LIVE_DB_PATH.", "rows": []}
    path = Path(db_path).expanduser()
    if not path.is_file():
        return {"status": "missing", "message": "La ruta configurada no corresponde a una base SQLite local disponible.", "rows": []}
    try:
        uri = path.resolve().as_uri() + "?mode=ro"
        with closing(sqlite3.connect(uri, uri=True, timeout=2)) as conn:
            conn.execute("PRAGMA query_only=ON")
            conn.row_factory = sqlite3.Row
            rows = [dict(r) for r in conn.execute(
                """SELECT timestamp_local, sta_dl_rssi AS rssi_dl_dbm,
                          snr_dl AS snr_dl_db, mcs_dl, dl_rate AS rate_dl_mbps
                   FROM radio_link_local
                   WHERE radio_role = 'AP' AND (error IS NULL OR error = '')
                   ORDER BY id DESC LIMIT ?""",
                (min(max(int(limit), 1), 720),),
            ).fetchall()]
            try:
                config = conn.execute(
                    """SELECT timestamp_local, frequency_band, channel_bandwidth_mhz
                       FROM radio_link_config_telemetry ORDER BY id DESC LIMIT 1"""
                ).fetchone()
                config = dict(config) if config else None
            except sqlite3.DatabaseError:
                config = None
    except (sqlite3.Error, OSError, ValueError) as exc:
        return {"status": "error", "message": f"No se pudo leer SQLite: {type(exc).__name__}", "rows": []}

    rows.reverse()
    if not rows:
        return {"status": "empty", "message": "La fuente aún no contiene registros AP elegibles.", "rows": [], "config": config}

    last = _parse_time(rows[-1].get("timestamp_local"))
    age = (datetime.now(timezone.utc) - last.astimezone(timezone.utc)).total_seconds() if last else None
    status = "fresh" if age is not None and -120 <= age <= stale_after_seconds else "stale"
    return {"status": status, "message": "Lectura satisfactoria" if status == "fresh" else "Los últimos datos están desactualizados o tienen hora no verificable.",
            "rows": rows, "config": config, "last_timestamp": str(rows[-1].get("timestamp_local")), "age_seconds": age}
