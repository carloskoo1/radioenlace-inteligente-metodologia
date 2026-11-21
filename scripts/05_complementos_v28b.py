"""Complementos V28 para los hallazgos A9, A10, A13, A21, A23 y A24 de la auditoria.

Analisis ADITIVOS: leen results/tables (regenerado por run_all.py) y escriben
solo archivos results/tables/v28b_*. No modifican modelos ni cifras principales.
Ejecutar despues de scripts/run_all.py.
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd
import yaml
from scipy.stats import spearmanr
from sklearn.ensemble import HistGradientBoostingClassifier, HistGradientBoostingRegressor, IsolationForest
from sklearn.impute import SimpleImputer
from sklearn.inspection import permutation_importance
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results" / "tables"
CFG = yaml.safe_load((ROOT / "config" / "analysis.yml").read_text(encoding="utf-8"))
SEED = int(CFG["random_seed"])
H = int(CFG["classification"]["horizon_minutes"])
COLS = ["rssi_dl_dbm", "rssi_ul_dbm", "snr_dl_db", "snr_ul_db", "mcs_dl", "mcs_ul", "rate_dl_mbps"]

m = pd.read_csv(OUT / "master_minute.csv.gz")
m["timestamp_local"] = pd.to_datetime(m["timestamp_local"], utc=True)
m = m.set_index("timestamp_local").sort_index()
assert m.index.is_unique and m.index.is_monotonic_increasing

pred = m[COLS].ffill(limit=int(CFG["quality"]["predictor_forward_fill_limit_minutes"]))
f = pd.DataFrame(index=m.index)
for c in COLS:
    f[c] = pred[c]
    for lag in [1, 5, 15, 30, 60]:
        f[f"{c}_lag{lag}"] = pred[c].shift(lag)
    for win in [5, 15, 60]:
        f[f"{c}_mean{win}"] = pred[c].shift(1).rolling(win, min_periods=max(3, win // 2)).mean()
        f[f"{c}_std{win}"] = pred[c].shift(1).rolling(win, min_periods=max(3, win // 2)).std()
loc = m.index.tz_convert("America/Lima")
f["hour_sin"] = np.sin(2 * np.pi * loc.hour / 24)
f["hour_cos"] = np.cos(2 * np.pi * loc.hour / 24)
f["dow_sin"] = np.sin(2 * np.pi * loc.dayofweek / 7)
f["dow_cos"] = np.cos(2 * np.pi * loc.dayofweek / 7)
FC = list(f.columns)

valid = m.index[m["observed"].eq(1)]
cut1 = valid[int(len(valid) * float(CFG["split"]["train"]))]
cut2 = valid[int(len(valid) * (float(CFG["split"]["train"]) + float(CFG["split"]["validation"])))]
states = m["state_proxy"]


def clf(seed=SEED):
    return make_pipeline(
        SimpleImputer(strategy="median"),
        HistGradientBoostingClassifier(max_iter=140, learning_rate=.07, max_leaf_nodes=31,
                                       l2_regularization=.2, early_stopping=False,
                                       random_state=seed, class_weight="balanced"))


def alert_stats(y, p):
    a = np.asarray(y) != "normal"
    q = np.asarray(p) != "normal"
    tp = int((a & q).sum()); fp = int((~a & q).sum()); fn = int((a & ~q).sum()); tn = int((~a & ~q).sum())
    return {"tp": tp, "fp": fp, "fn": fn, "tn": tn,
            "recall": tp / (tp + fn) if tp + fn else None,
            "false_alert_rate": fp / (fp + tn) if fp + tn else None}


ds = f.copy()
ds["target"] = states.shift(-H)
ds = ds[ds["target"].notna()]
tr = ds.index < cut1
va = (ds.index >= cut1) & (ds.index < cut2)
te = ds.index >= cut2
Xtr, ytr = ds.loc[tr, FC], ds.loc[tr, "target"]
Xva, yva = ds.loc[va, FC], ds.loc[va, "target"]
Xte, yte = ds.loc[te, FC], ds.loc[te, "target"]

model = clf()
model.fit(Xtr, ytr)
p0 = model.predict(Xte)
ref = pd.read_csv(OUT / "classification_metrics.csv")
ref_f1 = float(ref.loc[ref["model"] == "HistGradientBoosting", "f1_macro"].iloc[0])
f1_now = float(f1_score(yte, p0, average="macro"))
assert abs(f1_now - ref_f1) < 1e-6, (f1_now, ref_f1)

result = {"f1_macro_reconstruido": f1_now, "f1_macro_referencia": ref_f1}

# ---- A9 / A24: determinismo (la semilla ya no cambia el clasificador ni el regresor)
seed_rows = []
for s in [0, 1, 7, 123]:
    mm = clf(s)
    mm.fit(Xtr, ytr)
    seed_rows.append({"semilla": s, "predicciones_distintas_vs_base": int((mm.predict(Xte) != p0).sum())})
result["determinismo_clasificador_por_semilla"] = seed_rows

z = f.copy()
z["target"] = m["mcs_dl"].shift(-5)
z = z[z["target"].notna() & z["mcs_dl"].notna()]
ztr = z.index < cut1
zte = z.index >= cut2
reg = make_pipeline(SimpleImputer(strategy="median"), HistGradientBoostingRegressor(
    max_iter=120, learning_rate=.07, max_leaf_nodes=31, l2_regularization=.2,
    early_stopping=False, random_state=SEED))
reg.fit(z.loc[ztr, FC], z.loc[ztr, "target"])
newp = reg.predict(z.loc[zte, FC])
st = pd.read_csv(OUT / "forecast_test_predictions.csv")
st = st[(st["target"] == "mcs_dl") & (st["horizon_min"] == 5) & (st["model"] == "HistGradientBoosting")]
assert len(st) == len(newp), (len(st), len(newp))
result["determinismo_regresor_mcs_h5_max_abs_dif"] = float(np.max(np.abs(st["predicted"].to_numpy() - newp)))
result["determinismo_regresor_mcs_h5_mae"] = float(np.mean(np.abs(st["actual"].to_numpy() - newp)))

# ---- A10: etiquetas futuras que cruzan fronteras, por horizonte
rows = []
for h in [5, 15, 30]:
    y = states.shift(-h)
    idx = m.index[y.notna()]
    tcross = int(((idx[idx < cut1] + pd.Timedelta(minutes=h)) >= cut1).sum())
    vcross = int(((idx[(idx >= cut1) & (idx < cut2)] + pd.Timedelta(minutes=h)) >= cut2).sum())
    rows.append({"horizonte_min": h, "entrenamiento_cruza_a_validacion": tcross,
                 "validacion_cruza_a_prueba": vcross})
bd = pd.DataFrame(rows)
bd.to_csv(OUT / "v28b_frontera_por_horizonte.csv", index=False)
assert int(bd.loc[bd.horizonte_min == 15, "entrenamiento_cruza_a_validacion"].iloc[0]) == 15

# ---- A13: metricas de validacion y estabilidad de la importancia por permutacion
pv = model.predict(Xva)
pro_v = model.predict_proba(Xva)
cl = model.named_steps["histgradientboostingclassifier"].classes_
per_v = states.reindex(Xva.index).fillna("normal").to_numpy()
per_t = states.reindex(Xte.index).fillna("normal").to_numpy()
val_rows = []
for name, y, p, pro in [("HGB validacion", yva, pv, pro_v), ("Persistencia validacion", yva, per_v, None),
                        ("HGB prueba", yte, p0, model.predict_proba(Xte)), ("Persistencia prueba", yte, per_t, None)]:
    r = {"modelo": name, "n": int(len(y)), "accuracy": float(accuracy_score(y, p)),
         "f1_macro": float(f1_score(y, p, average="macro"))}
    r["auc_ovr_macro"] = float(roc_auc_score(y, pro, labels=cl, multi_class="ovr", average="macro")) if pro is not None else None
    r.update(alert_stats(y, p))
    val_rows.append(r)
pd.DataFrame(val_rows).to_csv(OUT / "v28b_validacion_clasificacion.csv", index=False)

sel = np.linspace(0, len(Xte) - 1, min(3000, len(Xte)), dtype=int)
pi3 = permutation_importance(model, Xte.iloc[sel], yte.iloc[sel], scoring="f1_macro", n_repeats=3,
                             random_state=SEED, n_jobs=-1)
pi30 = permutation_importance(model, Xte.iloc[sel], yte.iloc[sel], scoring="f1_macro", n_repeats=30,
                              random_state=SEED + 1, n_jobs=-1)
imp = pd.DataFrame({"feature": FC, "media_3rep": pi3.importances_mean, "sd_3rep": pi3.importances_std,
                    "media_30rep": pi30.importances_mean, "sd_30rep": pi30.importances_std})
imp["rango_3rep"] = imp["media_3rep"].rank(ascending=False).astype(int)
imp["rango_30rep"] = imp["media_30rep"].rank(ascending=False).astype(int)
imp = imp.sort_values("media_30rep", ascending=False)
imp.to_csv(OUT / "v28b_importancia_estabilidad.csv", index=False)
top3 = set(imp.sort_values("rango_3rep").head(10)["feature"])
top30 = set(imp.head(10)["feature"])
result["importancia"] = {
    "spearman_rangos_3_vs_30": float(spearmanr(imp["media_3rep"], imp["media_30rep"])[0]),
    "solape_top10": len(top3 & top30),
    "top5_30rep": list(imp.head(5)["feature"]),
    "top5_3rep": list(imp.sort_values("rango_3rep").head(5)["feature"]),
}

# ---- A21: Isolation Forest, tasa de anomalias por tramo
anom = m[COLS].dropna()
iso = make_pipeline(StandardScaler(), IsolationForest(
    n_estimators=int(CFG["anomaly_detection"]["estimators"]),
    contamination=float(CFG["anomaly_detection"]["contamination"]), random_state=SEED, n_jobs=-1))
iso.fit(anom.loc[anom.index < cut1])
flag = iso.predict(anom) == -1
seg = np.where(anom.index < cut1, "entrenamiento", np.where(anom.index < cut2, "validacion", "prueba"))
an = pd.DataFrame({"tramo": seg, "flag": flag}).groupby("tramo").agg(minutos=("flag", "size"), anomalias=("flag", "sum"))
an["tasa_pct"] = 100 * an["anomalias"] / an["minutos"]
an.reset_index().to_csv(OUT / "v28b_anomalias_por_tramo.csv", index=False)

# ---- A23: persistencia con huecos rellenados con 'normal' frente a excluirlos
ok = states.reindex(Xte.index).notna().to_numpy()
rows = []
for etiqueta, mask in [("Con huecos como normal (pipeline)", np.ones(len(Xte), bool)), ("Sin huecos (excluidos)", ok)]:
    for nombre, p in [("Persistencia", per_t), ("HistGradientBoosting", p0)]:
        r = {"escenario": etiqueta, "modelo": nombre, "n": int(mask.sum()),
             "f1_macro": float(f1_score(np.asarray(yte)[mask], np.asarray(p)[mask], average="macro"))}
        r.update(alert_stats(np.asarray(yte)[mask], np.asarray(p)[mask]))
        rows.append(r)
pd.DataFrame(rows).to_csv(OUT / "v28b_persistencia_sin_huecos.csv", index=False)
result["prueba_minutos_sin_estado_actual"] = int((~ok).sum())

(OUT / "v28b_resumen.json").write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
print(json.dumps(result, indent=2, ensure_ascii=False))
for nombre in ["v28b_frontera_por_horizonte", "v28b_validacion_clasificacion", "v28b_anomalias_por_tramo", "v28b_persistencia_sin_huecos"]:
    print("\n" + nombre + "\n" + pd.read_csv(OUT / f"{nombre}.csv").to_string(index=False))
print("\nIMPORTANCIA (top 10, 30 rep)\n", imp.head(10).to_string(index=False))
