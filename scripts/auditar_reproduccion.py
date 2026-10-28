"""Audita salidas regeneradas comparándolas con la referencia PUBLICADA v1.0.0.

No modifica datos originales ni recalibra modelos para mejorar coincidencia.
La salida se escribe en reproduccion_auditoria.json fuera del directorio results/.
"""
import json
import platform
import sys
from pathlib import Path
import pandas as pd
import sklearn
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"results"/"tables"
TESTS=[
    ("raw_files",90,0,"número de archivos"),
    ("raw_ap_rows",173513,0,"registros AP"),
    ("master_observed_minutes",118458,0,"minutos observados"),
    ("anomaly_flags",1093,0,"anomalías"),
]
checks=[]
s=json.loads((OUT/"analysis_summary.json").read_text(encoding="utf-8"))
for k,expected,tolerance,name in TESTS:
    measured=s.get(k)
    checks.append(dict(name=name,reference=expected,observed=measured,
                       difference=measured-expected,passed=abs(measured-expected)<=tolerance))
d=pd.read_csv(OUT/"classification_metrics.csv")
clf=d.loc[d.model.eq("HistGradientBoosting")].iloc[0]
for k,expected,tol in [
 ("f1_macro",0.5747977997550691,0.001),
 ("auc_ovr_macro",0.7940373885433543,0.001)
]:
    actual=float(clf[k])
    checks.append(dict(name=k,reference=expected,observed=actual,
                       difference=actual-expected,passed=abs(actual-expected)<=tol))
a=pd.read_csv(OUT/"anticipation_metrics.csv")
alert=a.loc[a.model.eq("HistGradientBoosting")].iloc[0]
for k,expected in [("tp",723),("fp",1742),("fn",825),("tn",14464)]:
    actual=int(alert[k])
    checks.append(dict(name="alert_"+k,reference=expected,observed=actual,
                       difference=actual-expected,passed=actual==expected))
f=pd.read_csv(OUT/"forecast_metrics.csv")
for target,h,model,expected in [
 ("mcs_dl",15,"Ridge",0.8694464503168152),
 ("rate_dl_mbps",15,"Ridge",18.984905428168346),
 ("rssi_dl_dbm",15,"Persistencia",0.49878770792218774),
]:
    actual=float(f.loc[f.target.eq(target)&f.horizon_min.eq(h)&
                     f.model.eq(model)&f.split.eq("test"),"mae"].iloc[0])
    checks.append(dict(name="MAE_"+target+"_"+str(h)+"_"+model,reference=expected,
                       observed=actual,difference=actual-expected,passed=abs(actual-expected)<0.0001))
report={
    "reference":"release v1.0.0, commit 8f175ffef568c25cbaee91a1c04da3f2cc38cdb2",
    "environment":{"python":sys.version,"os":platform.platform(),
                   "numpy":np.__version__,"pandas":pd.__version__,
                   "scikit_learn":sklearn.__version__},
    "passed":all(x["passed"] for x in checks),"checks":checks
}
path=ROOT/"reproduccion_auditoria.json"
path.write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding="utf-8")
print(json.dumps(report,indent=2,ensure_ascii=False))
if not report["passed"]:
    raise SystemExit("HAY DIFERENCIAS: revisar métodos y plataforma antes de afirmar reproducción exacta.")
