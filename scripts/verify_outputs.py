"""Comprueba invariantes principales de la corrida reproducida."""
import json
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results/tables"
s = json.loads((OUT / "analysis_summary.json").read_text(encoding="utf-8"))
assert s["raw_files"] == 90
assert s["raw_ap_rows"] == 173_513
assert s["master_observed_minutes"] == 118_458
assert s["anomaly_flags"] == 1_093

c = pd.read_csv(OUT / "classification_metrics.csv")
hgb = c.loc[c.model.eq("HistGradientBoosting")].iloc[0]
assert abs(hgb.f1_macro - 0.575) < 0.002
assert abs(hgb.auc_ovr_macro - 0.794) < 0.002

a = pd.read_csv(OUT / "anticipation_metrics.csv")
assert set(a.model) == {"Persistencia", "HistGradientBoosting"}
f = pd.read_csv(OUT / "forecast_metrics.csv")
assert set(f.horizon_min) == {5, 15, 30}
assert set(f.target) == {"rssi_dl_dbm", "mcs_dl", "rate_dl_mbps"}
print("Verificación superada: conteos, modelos, horizontes y métricas principales coherentes.")
