"""Auditoría no destructiva de cortes y sensibilidad inferencial para la tesis Ubelser.

Ejecutar después de scripts/run_all.py, en Linux/Python 3.12.
Los resultados se escriben EXCLUSIVAMENTE en audit/sensibilidad_20261112.
No modifica el release v1.0.0 ni las tablas de referencia.
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd
import yaml
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import Ridge
from sklearn.metrics import f1_score, mean_absolute_error, roc_auc_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "audit" / "sensibilidad_20261112"
OUT.mkdir(parents=True, exist_ok=True)
CFG = yaml.safe_load((ROOT / "config" / "analysis.yml").read_text(encoding="utf-8"))
SEED = int(CFG["random_seed"])
B = 500  # Sensibilidad exploratoria: 500 remuestreos por escenario.
H = 15
LAGS = [1, 5, 15, 30, 60]
WINS = [5, 15, 60]
COLS = ["rssi_dl_dbm", "rssi_ul_dbm", "snr_dl_db", "snr_ul_db", "mcs_dl",
        "mcs_ul", "rate_dl_mbps"]

m = pd.read_csv(ROOT / "results" / "tables" / "master_minute.csv.gz")
m["timestamp_local"] = pd.to_datetime(m["timestamp_local"], utc=True)
m = m.set_index("timestamp_local").sort_index()
assert m.index.is_unique, "El índice temporal debe ser único."
assert m.index.is_monotonic_increasing
pred = m[COLS].ffill(limit=1)
f = pd.DataFrame(index=m.index)
for col in COLS:
    f[col] = pred[col]
    for lag in LAGS:
        f[f"{col}_lag{lag}"] = pred[col].shift(lag)
    for win in WINS:
        f[f"{col}_mean{win}"] = pred[col].shift(1).rolling(
            win, min_periods=max(3, win // 2)).mean()
        f[f"{col}_std{win}"] = pred[col].shift(1).rolling(
            win, min_periods=max(3, win // 2)).std()
local_idx = m.index.tz_convert("America/Lima")
f["hour_sin"] = np.sin(2 * np.pi * local_idx.hour / 24)
f["hour_cos"] = np.cos(2 * np.pi * local_idx.hour / 24)
f["dow_sin"] = np.sin(2 * np.pi * local_idx.dayofweek / 7)
f["dow_cos"] = np.cos(2 * np.pi * local_idx.dayofweek / 7)
feature_cols = list(f.columns)

valid = m.index[m["observed"].eq(1)]
cut1 = valid[int(len(valid) * float(CFG["split"]["train"]))]
cut2 = valid[int(len(valid) * (float(CFG["split"]["train"])
                              + float(CFG["split"]["validation"])))]
date_pad = pd.Timedelta(minutes=H)
states = m["state_proxy"]

def clf_model():
    return make_pipeline(
        SimpleImputer(strategy="median"),
        HistGradientBoostingClassifier(
            max_iter=140, learning_rate=.07, max_leaf_nodes=31,
            l2_regularization=.2, random_state=SEED, class_weight="balanced"))

def cls_metrics(y_true, y_hat, proba, classes):
    actual = np.asarray(y_true)
    predicted = np.asarray(y_hat)
    aa = actual != "normal"
    pp = predicted != "normal"
    tp = int(np.count_nonzero(aa & pp))
    fp = int(np.count_nonzero(~aa & pp))
    fn = int(np.count_nonzero(aa & ~pp))
    tn = int(np.count_nonzero(~aa & ~pp))
    return {
        "n_test": int(len(actual)), "f1_macro": float(f1_score(actual, predicted, average="macro")),
        "auc_ovr_macro": float(roc_auc_score(actual, proba, labels=classes, multi_class="ovr", average="macro")),
        "tp": tp, "fp": fp, "fn": fn, "tn": tn,
        "alert_precision": float(tp / (tp + fp)) if tp + fp else None,
        "alert_recall": float(tp / (tp + fn)) if tp + fn else None,
    }

y = states.shift(-H)
ds = f.copy()
ds["target"] = y
ds = ds[ds["target"].notna()]
Xte = ds.loc[ds.index >= cut2, feature_cols]
yte = ds.loc[ds.index >= cut2, "target"]
tr_base = ds.index < cut1
tr_purged = tr_base & ((ds.index + date_pad) < cut1)
Xtr = ds.loc[tr_base, feature_cols]
ytr = ds.loc[tr_base, "target"]
Xtr_purged = ds.loc[tr_purged, feature_cols]
ytr_purged = ds.loc[tr_purged, "target"]

cl0, cl1 = clf_model(), clf_model()
cl0.fit(Xtr, ytr)
cl1.fit(Xtr_purged, ytr_purged)
p0, p1 = cl0.predict(Xte), cl1.predict(Xte)
pro0, pro1 = cl0.predict_proba(Xte), cl1.predict_proba(Xte)
cls0 = cl0.named_steps["histgradientboostingclassifier"].classes_
cls1 = cl1.named_steps["histgradientboostingclassifier"].classes_
persist = states.reindex(Xte.index).fillna("normal").to_numpy()
d0, d1 = cls_metrics(yte, p0, pro0, cls0), cls_metrics(yte, p1, pro1, cls1)
d1["n_train_original"] = len(Xtr)
d1["n_train_purged"] = len(Xtr_purged)
d1["removed_cross_boundary_train"] = len(Xtr) - len(Xtr_purged)
d1["n_predictions_changed"] = int((p0 != p1).sum())
assert len(Xte) == 17754, f"Prueba no comparable: {len(Xte)} casos."

def bootstrap_indices(n, block, rng, times=None):
    inds = []
    if times is None:
        starts = max(1, n - block + 1)
        while sum(len(z) for z in inds) < n:
            s = int(rng.integers(0, starts))
            inds.append(np.arange(s, min(s + block, n), dtype=np.int32))
    else:
        # Bloque de reloj real: últimos <=60 minutos desde el inicio elegido.
        while sum(len(z) for z in inds) < n:
            s = int(rng.integers(0, n))
            e = int(np.searchsorted(times, times[s] + 60, side="left"))
            inds.append(np.arange(s, max(s + 1, e), dtype=np.int32))
    return np.concatenate(inds)[:n]

def sensitivity_cls(actual, pred_class, pred_persistence, times):
    data = []
    n = len(actual)
    for kind, block in [("observaciones", 15), ("observaciones", 60),
                        ("observaciones", 180), ("minutos_reales", 60)]:
        rng = np.random.default_rng(SEED + 10 * block + (1 if kind == "minutos_reales" else 0))
        res = []
        for _ in range(B):
            idx = bootstrap_indices(n, block, rng, times=times if kind == "minutos_reales" else None)
            res.append(f1_score(actual[idx], pred_class[idx], average="macro")
                       - f1_score(actual[idx], pred_persistence[idx], average="macro"))
        lo, hi = np.quantile(res, [.025, .975])
        data.append({"metric": "delta_f1_hgb_minus_persistencia", "scenario": kind,
                     "block": block, "n_boot": B, "estimate": float(f1_score(actual, pred_class, average="macro")
                                      - f1_score(actual, pred_persistence, average="macro")),
                     "ci_low": float(lo), "ci_high": float(hi), "ci_excludes_zero": bool(lo > 0 or hi < 0)})
    return data

def sensitivity_forecast(actual, ridge, persistence, times, label):
    data = []
    aa = np.asarray(actual, dtype=float)
    rr = np.asarray(ridge, dtype=float)
    pp = np.asarray(persistence, dtype=float)
    n = len(aa)
    gain = np.abs(aa - pp) - np.abs(aa - rr)
    for kind, block in [("observaciones", 15), ("observaciones", 60),
                        ("observaciones", 180), ("minutos_reales", 60)]:
        rng = np.random.default_rng(SEED + 1000 + 10 * block + (1 if kind == "minutos_reales" else 0))
        res = []
        for _ in range(B):
            idx = bootstrap_indices(n, block, rng, times=times if kind == "minutos_reales" else None)
            res.append(float(gain[idx].mean()))
        lo, hi = np.quantile(res, [.025, .975])
        data.append({"metric": label, "scenario": kind, "block": block,
                     "n_boot": B, "estimate": float(gain.mean()),
                     "ci_low": float(lo), "ci_high": float(hi), "ci_excludes_zero": bool(lo > 0 or hi < 0)})
    return data

# Los tiempos son minutos UTC reales para evitar la ambigüedad del DST.
times_cls = np.asarray(Xte.index.asi8 // 60_000_000_000, dtype=np.int64)
boot_cls = sensitivity_cls(yte.to_numpy(), p0, persist, times_cls)
boot_cls_purge = sensitivity_cls(yte.to_numpy(), p1, persist, times_cls)

forecast_results = []
forecast_boot = []
cut_diagnostics = []
for target in ["rssi_dl_dbm", "mcs_dl", "rate_dl_mbps"]:
    h = 15
    z = f.copy()
    z["target"] = m[target].shift(-h)
    z = z[z["target"].notna() & m[target].notna()]
    train = z.index < cut1
    validmask = (z.index >= cut1) & (z.index < cut2)
    train_purged = train & ((z.index + pd.Timedelta(minutes=h)) < cut1)
    val_purged = validmask & ((z.index + pd.Timedelta(minutes=h)) < cut2)
    test = z.index >= cut2
    cut_diagnostics.append({
        "target": target, "horizon_minutes": h,
        "removed_train": int(train.sum() - train_purged.sum()),
        "removed_validation": int(validmask.sum() - val_purged.sum()),
        "n_test": int(test.sum()),
    })
    baseline = make_pipeline(SimpleImputer(strategy="median"), StandardScaler(), Ridge(alpha=1.0))
    purged = make_pipeline(SimpleImputer(strategy="median"), StandardScaler(), Ridge(alpha=1.0))
    baseline.fit(z.loc[train, feature_cols], z.loc[train, "target"])
    purged.fit(z.loc[train_purged, feature_cols], z.loc[train_purged, "target"])
    yt = z.loc[test, "target"].to_numpy(dtype=float)
    pb = z.loc[test, target].to_numpy(dtype=float)
    pr0 = baseline.predict(z.loc[test, feature_cols])
    pr1 = purged.predict(z.loc[test, feature_cols])
    forecast_results.append({
        "target": target, "n_test": int(len(yt)),
        "mae_persistencia": float(mean_absolute_error(yt, pb)),
        "mae_ridge_original": float(mean_absolute_error(yt, pr0)),
        "mae_ridge_purgado": float(mean_absolute_error(yt, pr1)),
        "delta_mae_purgado_menos_original": float(mean_absolute_error(yt, pr1) - mean_absolute_error(yt, pr0)),
    })
    if target == "mcs_dl":
        minutes = np.asarray(z.loc[test].index.asi8 // 60_000_000_000, dtype=np.int64)
        forecast_boot += sensitivity_forecast(yt, pr0, pb, minutes, "ganancia_mae_ridge_mcs15")
        forecast_boot += sensitivity_forecast(yt, pr1, pb, minutes, "ganancia_mae_ridge_purgado_mcs15")

reference = pd.read_csv(ROOT / "results" / "tables" / "classification_metrics.csv")
ref = reference[reference["model"] == "HistGradientBoosting"].iloc[0]
comparison = {"f1_reference": float(ref.f1_macro), "f1_rebuilt": float(d0["f1_macro"]),
              "f1_abs_delta": abs(float(ref.f1_macro) - float(d0["f1_macro"]))}
results = {
    "method": "Sensibilidad retrospectiva, no estimacion prospectiva ni nuevo test independiente",
    "environment": "Ubuntu GitHub Actions / Python 3.12",
    "cut_train": str(cut1), "cut_validation": str(cut2),
    "classification_original": d0, "classification_purged": d1,
    "reference_check": comparison, "forecast": forecast_results,
    "boundary_counts": cut_diagnostics,
    "bootstrap_classification_original": boot_cls,
    "bootstrap_classification_purged": boot_cls_purge,
    "bootstrap_mcs15": forecast_boot,
    "limitations": [
        "El test cronologico se reutiliza para analisis de sensibilidad; no es segunda cohorte.",
        "La purga evita etiquetas futuras que cruzan entrenamiento/validacion, no altera las caracteristicas ni el etiquetado proxy.",
        "Los bloques de observaciones no son bloques de tiempo real.",
        "Los intervalos de bootstrap son exploratorios y dependen de la hipotesis de dependencia temporal.",
        "La variabilidad entre plataformas de HistGradientBoosting persiste como limitacion."],
}
(OUT / "resultados.json").write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
pd.DataFrame(boot_cls + boot_cls_purge + forecast_boot).to_csv(OUT / "sensibilidad_bootstrap.csv", index=False)
pd.DataFrame(forecast_results).to_csv(OUT / "sensibilidad_ridge.csv", index=False)
print("AUDITORIA_SENSIBILIDAD_BEGIN")
print(json.dumps(results, indent=2, ensure_ascii=False))
print("AUDITORIA_SENSIBILIDAD_END")
