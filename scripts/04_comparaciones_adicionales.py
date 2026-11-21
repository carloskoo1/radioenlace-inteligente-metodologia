"""Comparaciones complementarias V28 (respuesta a la auditoria adversarial del V27).

Genera, sobre la corrida oficial (HGB determinista, early_stopping=False):
  1. prevalencia de estados por tramo y circularidad de la regla de estados;
  2. comparacion de alertas a tasa de falsas alertas igualada, con IC por bloques;
  3. lineas base adicionales de pronostico (promedios moviles y mediana de entrenamiento).
No modifica ninguna salida de los pasos 00-03. Uso: python scripts/04_comparaciones_adicionales.py
"""
import json
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import yaml
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import Ridge
from sklearn.metrics import roc_auc_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results" / "tables"
CFG = yaml.safe_load((ROOT / "config" / "analysis.yml").read_text(encoding="utf-8"))
SEED = int(CFG["random_seed"])
S = json.loads((OUT / "analysis_summary.json").read_text(encoding="utf-8"))
Q = S["state_thresholds_training_only"]

m = pd.read_csv(OUT / "master_minute.csv.gz")
m["timestamp_local"] = pd.to_datetime(m.timestamp_local, errors="coerce")
m = m.set_index("timestamp_local").sort_index()
cols = ["rssi_dl_dbm", "rssi_ul_dbm", "snr_dl_db", "snr_ul_db", "mcs_dl", "mcs_ul", "rate_dl_mbps"]
pred = m[cols].ffill(limit=1)
f = pd.DataFrame(index=m.index)
for c in cols:
    f[c] = pred[c]
    for lag in [1, 5, 15, 30, 60]:
        f[f"{c}_lag{lag}"] = pred[c].shift(lag)
    for win in [5, 15, 60]:
        f[f"{c}_mean{win}"] = pred[c].shift(1).rolling(win, min_periods=max(3, win // 2)).mean()
        f[f"{c}_std{win}"] = pred[c].shift(1).rolling(win, min_periods=max(3, win // 2)).std()
f["hour_sin"] = np.sin(2 * np.pi * f.index.hour / 24)
f["hour_cos"] = np.cos(2 * np.pi * f.index.hour / 24)
f["dow_sin"] = np.sin(2 * np.pi * f.index.dayofweek / 7)
f["dow_cos"] = np.cos(2 * np.pi * f.index.dayofweek / 7)
fc = list(f.columns)
vt = m.index[m.observed.eq(1)]
cut1 = vt[int(len(vt) * float(CFG["split"]["train"]))]
cut2 = vt[int(len(vt) * (float(CFG["split"]["train"]) + float(CFG["split"]["validation"])))]
st = m.state_proxy

# 1. Prevalencia por tramo y regla de estados
rows = []
masks = {"entrenamiento": m.index < cut1, "validacion": (m.index >= cut1) & (m.index < cut2), "prueba": m.index >= cut2}
for k, mk in masks.items():
    s = st[mk].dropna()
    rows.append(dict(tramo=k, minutos_calendario=int(mk.sum()), minutos_observados=int(m.observed[mk].sum()),
                     cobertura_pct=100 * m.observed[mk].sum() / mk.sum(), con_etiqueta=int(len(s)),
                     normal_pct=100 * (s == "normal").mean(), degradado_pct=100 * (s == "degraded").mean(),
                     critico_pct=100 * (s == "critical").mean()))
prev = pd.DataFrame(rows)
crit = m[st == "critical"]
snr_q01 = Q["snr_dl_db"]["0.01"]
prev["criticos_con_snr_le_p1_pct"] = 100 * float((crit.snr_dl_db <= snr_q01).mean())
prev.to_csv(OUT / "v28_prevalencia_estados_por_tramo.csv", index=False)

# 2. Alertas a FAR igualada (HGB determinista)
ds = f.copy()
ds["target"] = st.shift(-15)
ds = ds[ds.target.notna()]
tr, te = ds.index < cut1, ds.index >= cut2
Xtr, ytr, Xte, yte = ds.loc[tr, fc], ds.loc[tr, "target"], ds.loc[te, fc], ds.loc[te, "target"]
clf = make_pipeline(SimpleImputer(strategy="median"), HistGradientBoostingClassifier(
    max_iter=140, learning_rate=.07, max_leaf_nodes=31, l2_regularization=.2,
    early_stopping=False, random_state=SEED, class_weight="balanced"))
clf.fit(Xtr, ytr)
classes = list(clf.named_steps["histgradientboostingclassifier"].classes_)
proba = clf.predict_proba(Xte)
pred_cls = clf.predict(Xte)
pers = st.reindex(Xte.index).fillna("normal").to_numpy()
act = yte.to_numpy() != "normal"
hg_a, pe_a = pred_cls != "normal", pers != "normal"
pnn = 1 - proba[:, classes.index("normal")]
far_p = (pe_a & ~act).sum() / (~act).sum()
rec_p = (pe_a & act).sum() / act.sum()
far_h = (hg_a & ~act).sum() / (~act).sum()
rec_h = (hg_a & act).sum() / act.sum()
thr = np.quantile(pnn[~act], 1 - far_p)
al = pnn > thr
B = 60
rng = np.random.default_rng(SEED)
n = len(act)
starts = np.arange(n - B + 1)
dr, dfa, dm = [], [], []
for _ in range(1000):
    ss = rng.choice(starts, size=int(np.ceil(n / B)), replace=True)
    idx = np.concatenate([np.arange(s, min(s + B, n)) for s in ss])[:n]
    ai, hi, pi_, mi = act[idx], hg_a[idx], pe_a[idx], al[idx]
    na, pa = max(ai.sum(), 1), max((~ai).sum(), 1)
    dr.append((hi & ai).sum() / na - (pi_ & ai).sum() / na)
    dfa.append((hi & ~ai).sum() / pa - (pi_ & ~ai).sum() / pa)
    dm.append((mi & ai).sum() / na - (pi_ & ai).sum() / na)
lo_r, hi_r = np.quantile(dr, [.025, .975])
lo_f, hi_f = np.quantile(dfa, [.025, .975])
lo_m, hi_m = np.quantile(dm, [.025, .975])
pd.DataFrame([
    dict(comparacion="Persistencia", recall=rec_p, tasa_falsas_alertas=far_p),
    dict(comparacion="HGB (clase predicha)", recall=rec_h, tasa_falsas_alertas=far_h,
         dif_recall_vs_persistencia=rec_h - rec_p, ic_low=lo_r, ic_high=hi_r,
         dif_far_vs_persistencia=far_h - far_p, far_ic_low=lo_f, far_ic_high=hi_f),
    dict(comparacion="HGB (umbral ajustado a la FAR de persistencia)", recall=(al & act).sum() / act.sum(),
         tasa_falsas_alertas=(al & ~act).sum() / (~act).sum(),
         dif_recall_vs_persistencia=(al & act).sum() / act.sum() - rec_p, ic_low=lo_m, ic_high=hi_m),
    dict(comparacion="AUC binario no normal (HGB, score continuo)", recall=roc_auc_score(act, pnn)),
]).to_csv(OUT / "v28_alertas_far_igualada.csv", index=False)

# 3. Lineas base adicionales
res = []
for target in ["rssi_dl_dbm", "mcs_dl", "rate_dl_mbps"]:
    for h in (5, 15, 30):
        d2 = f.copy()
        d2["target"] = m[target].shift(-h)
        d2 = d2[d2.target.notna() & d2[target].notna()]
        t_r, t_e = d2.index < cut1, d2.index >= cut2
        base = {"Persistencia": d2.loc[t_e, target], "Media movil 5 min": d2.loc[t_e, f"{target}_mean5"],
                "Media movil 15 min": d2.loc[t_e, f"{target}_mean15"], "Media movil 60 min": d2.loc[t_e, f"{target}_mean60"],
                "Mediana de entrenamiento": pd.Series(d2.loc[t_r, target].median(), index=d2.index[t_e])}
        rg = make_pipeline(SimpleImputer(strategy="median"), StandardScaler(), Ridge(alpha=1.0)).fit(d2.loc[t_r, fc], d2.loc[t_r, "target"])
        base["Ridge"] = pd.Series(rg.predict(d2.loc[t_e, fc]), index=d2.index[t_e])
        yt = d2.loc[t_e, "target"].to_numpy()
        ok = np.ones(len(yt), bool)
        for v in base.values():
            ok &= np.isfinite(v.to_numpy())
        for k, v in base.items():
            e = yt[ok] - v.to_numpy()[ok]
            res.append(dict(variable=target, horizonte_min=h, modelo=k, n=int(ok.sum()),
                            mae=float(np.mean(np.abs(e))), rmse=float(np.sqrt(np.mean(e ** 2)))))
pd.DataFrame(res).to_csv(OUT / "v28_lineas_base_adicionales.csv", index=False)
print("Comparaciones complementarias V28 generadas en results/tables/v28_*.csv")
