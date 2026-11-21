"""Auditoría de sensibilidad independiente de la tesis de Ubelser.

Solo lee salidas regeneradas de una copia limpia de v1.0.0. No modifica la
versión científica, los modelos publicados, ni los resultados de referencia.
Salida: JSON + CSV y resumen de consola para revisión académica.
"""
from pathlib import Path
import json
import os
import numpy as np
import pandas as pd
import yaml
from sklearn.impute import SimpleImputer
from sklearn.pipeline import make_pipeline
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import f1_score, confusion_matrix

ROOT=Path(os.environ.get("UBELSER_AUDIT_ROOT", ".")).resolve()
OUT=ROOT/"results"/"tables"
AUD=Path(os.environ.get("UBELSER_AUDIT_OUT", "audit_sensitivity")).resolve()
AUD.mkdir(parents=True, exist_ok=True)
CFG=yaml.safe_load((ROOT/"config"/"analysis.yml").read_text(encoding="utf-8"))
SEED=int(CFG["random_seed"])
BLOCKS=[30, 60, 120]
REPS=500
rng=np.random.default_rng(SEED)

m=pd.read_csv(OUT/"master_minute.csv.gz",parse_dates=["timestamp_local"]).set_index("timestamp_local").sort_index()
cols=["rssi_dl_dbm","rssi_ul_dbm","snr_dl_db","snr_ul_db","mcs_dl","mcs_ul","rate_dl_mbps"]
pred=m[cols].ffill(limit=1)
features=pd.DataFrame(index=m.index)
for c in cols:
    features[c]=pred[c]
    for lag in [1,5,15,30,60]: features[f"{c}_lag{lag}"]=pred[c].shift(lag)
    for win in [5,15,60]:
        features[f"{c}_mean{win}"]=pred[c].shift(1).rolling(win,min_periods=max(3,win//2)).mean()
        features[f"{c}_std{win}"]=pred[c].shift(1).rolling(win,min_periods=max(3,win//2)).std()
features["hour_sin"]=np.sin(2*np.pi*features.index.hour/24)
features["hour_cos"]=np.cos(2*np.pi*features.index.hour/24)
features["dow_sin"]=np.sin(2*np.pi*features.index.dayofweek/7)
features["dow_cos"]=np.cos(2*np.pi*features.index.dayofweek/7)
eligible=m.index[m.observed.eq(1)]
cut1=eligible[int(len(eligible)*float(CFG["split"]["train"]))]
cut2=eligible[int(len(eligible)*(float(CFG["split"]["train"])+float(CFG["split"]["validation"])))]
h=int(CFG["classification"]["horizon_minutes"])
st=m["state_proxy"]
ds=features.copy()
ds["target"]=st.shift(-h)
ds=ds[ds.target.notna()]
train=ds.index<cut1
test=ds.index>=cut2
# Original labels at t+h are accessible only if that future timestamp belongs to
# the same split; otherwise the original training/validation protocol leaks across.
def cross_count(horizon):
    counts={}
    for label,lower,upper in [("train",None,cut1),("validation",cut1,cut2),("test",cut2,None)]:
        y=m["rssi_dl_dbm"].shift(-horizon)
        origin=m.index[y.notna()]
        if lower is not None: origin=origin[origin>=lower]
        if upper is not None: origin=origin[origin<upper]
        if upper is None:
            counts[label]=0
        else:
            counts[label]=int(((origin+pd.Timedelta(minutes=horizon))>=upper).sum())
    return counts

train_cross=((ds.index[train]+pd.Timedelta(minutes=h))>=cut1)
test_cross=False # final test is after validation; no future split inside study.
xtrain=ds.loc[train,features.columns]
ytrain=ds.loc[train,"target"]
xtest=ds.loc[test,features.columns]
ytest=ds.loc[test,"target"]
def fit(x,y):
    estimator=make_pipeline(SimpleImputer(strategy="median"),HistGradientBoostingClassifier(
        max_iter=140, learning_rate=.07,max_leaf_nodes=31,l2_regularization=.2,
        early_stopping=False,random_state=SEED,class_weight="balanced"))
    estimator.fit(x,y)
    return estimator
original=fit(xtrain,ytrain)
purged=fit(xtrain.loc[~train_cross],ytrain.loc[~train_cross])
yp=ytest.to_numpy()
b=st.reindex(xtest.index).fillna("normal").to_numpy()
po=original.predict(xtest);pp=purged.predict(xtest)
def cls_result(name,p):
    positives=(yp!="normal"); predicted=(p!="normal")
    tp=int(np.sum(positives&predicted)); fp=int(np.sum(~positives&predicted))
    fn=int(np.sum(positives&~predicted)); tn=int(np.sum(~positives&~predicted))
    return dict(model=name,n=int(len(yp)),f1_macro=float(f1_score(yp,p,average="macro")),
                tp=tp,fp=fp,fn=fn,tn=tn,
                recall=float(tp/(tp+fn)),false_alert_rate=float(fp/(fp+tn)))
metrics=[cls_result("Persistencia",b),cls_result("HGB_original",po),cls_result("HGB_purga_frontera",pp)]
def samples(n,block,rng):
    starts=rng.integers(0,max(1,n-block+1),size=int(np.ceil(n/block)))
    return np.concatenate([np.arange(s,min(s+block,n)) for s in starts])[:n]
sensitivity=[]
for block in BLOCKS:
    rr=np.random.default_rng(SEED+block)
    for model,p in [("HGB_original",po),("HGB_purga_frontera",pp)]:
        gains=[]
        for _ in range(REPS):
            idx=samples(len(yp),block,rr)
            gains.append(f1_score(yp[idx],p[idx],average="macro")
                         -f1_score(yp[idx],b[idx],average="macro"))
        lo,hi=np.quantile(gains,[.025,.975])
        sensitivity.append(dict(task="F1_macro",horizon=15,model=model,block_observations=block,
            ci_low=float(lo),ci_high=float(hi),supported_95=bool(lo>0),replications=REPS))
# Comparison of MAE Ridge vs persistence at 5/15/30 for each variable
f=pd.read_csv(OUT/"forecast_test_predictions.csv")
for (target,hor),g in f.groupby(["target","horizon_min"]):
    pivot=g.pivot_table(index="timestamp",columns="model",values=["actual","predicted"],aggfunc="first")
    if not all(("predicted",name) in pivot.columns for name in ("Persistencia","Ridge")):continue
    y=pivot[("actual","Persistencia")].to_numpy()
    base=pivot[("predicted","Persistencia")].to_numpy()
    model=pivot[("predicted","Ridge")].to_numpy()
    ok=np.isfinite(y)&np.isfinite(base)&np.isfinite(model)
    y=y[ok];base=base[ok];model=model[ok]
    for block in BLOCKS:
        rr=np.random.default_rng(SEED+block+int(hor)+len(target))
        gains=[]
        for _ in range(REPS):
            idx=samples(len(y),block,rr)
            gains.append(float(np.mean(np.abs(y[idx]-base[idx]))
                               -np.mean(np.abs(y[idx]-model[idx]))))
        lo,hi=np.quantile(gains,[.025,.975])
        sensitivity.append(dict(task="MAE",target=target,horizon=int(hor),model="Ridge",
            block_observations=block,ci_low=float(lo),ci_high=float(hi),
            supported_95=bool(lo>0),replications=REPS))
# Observations are not equivalent to elapsed minutes in a series with gaps.
actual_gaps=(xtest.index.to_series().diff().dt.total_seconds().dropna()/60)
report={
 "commit_scientific":"v1.0.0","date_range":[str(m.index.min()),str(m.index.max())],
 "cut_train_validation":str(cut1),"cut_validation_test":str(cut2),
 "classification_horizon_minutes":h,
 "eligible_train_before_purge":int(train.sum()),
 "eligible_train_removed_by_purge":int(train_cross.sum()),
 "eligible_train_after_purge":int((~train_cross).sum()),
 "cross_boundary_counts_by_horizon":{str(k):cross_count(k) for k in [5,15,30]},
 "test_elapsed_gap_over_1min":int((actual_gaps>1).sum()),
 "test_elapsed_gap_max_minutes":float(actual_gaps.max()),
 "classification_metrics":metrics,
 "sensitivity_ci":sensitivity,
 "bootstrap_blocks_are_observation_counts":True,
 "note":"Sensibilidad de remuestreo sobre la misma secuencia de test. No es validacion de campo."
}
(AUD/"auditoria_sensibilidad.json").write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding="utf-8")
pd.DataFrame(metrics).to_csv(AUD/"metricas_clasificacion_purgadas.csv",index=False)
pd.DataFrame(sensitivity).to_csv(AUD/"sensibilidad_bloques.csv",index=False)
print("AUDITORIA_FINAL",json.dumps({k:v for k,v in report.items() if k!="sensitivity_ci"},ensure_ascii=False,indent=2))
print("SENSIBILIDAD\n",pd.DataFrame(sensitivity).to_string(index=False))
