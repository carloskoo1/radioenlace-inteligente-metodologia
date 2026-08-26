from pathlib import Path
import json, math, warnings
import numpy as np
import pandas as pd
import yaml
from sklearn.impute import SimpleImputer
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler, label_binarize
from sklearn.linear_model import Ridge
from sklearn.ensemble import HistGradientBoostingRegressor, HistGradientBoostingClassifier, IsolationForest
from sklearn.metrics import (
    mean_absolute_error, mean_squared_error, f1_score, accuracy_score,
    precision_score, recall_score, confusion_matrix, roc_auc_score,
)

warnings.filterwarnings('ignore')
ROOT=Path(__file__).resolve().parents[2]
RAW=ROOT/'data'/'raw'/'extracted'/'Datos'
OUT=ROOT/'results'/'tables'
OUT.mkdir(exist_ok=True)
CFG=yaml.safe_load((ROOT/'config'/'analysis.yml').read_text(encoding='utf-8'))
SEED=int(CFG['random_seed'])

files=sorted(RAW.glob('epmp_local_*.csv'))
parts=[]
for f in files:
    x=pd.read_csv(f,dtype=str,low_memory=False)
    x['_source_file']=f.name
    parts.append(x)
raw=pd.concat(parts,ignore_index=True)
raw=raw[raw['role'].eq(CFG['source']['role'])].copy()
raw['timestamp']=pd.to_datetime(raw['ts'],errors='coerce',utc=True).dt.tz_convert('America/Lima')
raw=raw.sort_values('timestamp').drop_duplicates('timestamp',keep='last')

num_map={
    'mcs_dl':'mcs_dl','mcs_ul':'mcs_ul','snr_dl':'snr_dl_db','snr_ul':'snr_ul_db',
    'sta_dl_rssi':'rssi_dl_dbm','sta_ul_rssi':'rssi_ul_dbm',
}
for src,dst in num_map.items():
    raw[dst]=pd.to_numeric(raw[src].astype(str).str.strip(),errors='coerce')
raw['rate_dl_mbps']=pd.to_numeric(raw['dl_rate'].astype(str).str.extract(r'([-+]?\d+(?:\.\d+)?)')[0],errors='coerce')

# Treat impossible capture sentinels as missing, without altering the raw files.
raw.loc[raw['snr_dl_db']<=0,'snr_dl_db']=np.nan
raw.loc[raw['snr_ul_db']<=0,'snr_ul_db']=np.nan
raw.loc[raw['rssi_dl_dbm']>=0,'rssi_dl_dbm']=np.nan
raw.loc[raw['rssi_ul_dbm']>=0,'rssi_ul_dbm']=np.nan

cols=['rssi_dl_dbm','rssi_ul_dbm','snr_dl_db','snr_ul_db','mcs_dl','mcs_ul','rate_dl_mbps']
minute=(raw.set_index('timestamp')[cols]
        .resample(CFG['source']['cadence']).median())
minute['observed']=minute[cols].notna().any(axis=1).astype(int)

# Causal short-gap fill (one minute only) for predictors; targets remain observed.
pred=minute[cols].ffill(limit=int(CFG['quality']['predictor_forward_fill_limit_minutes']))
features=pd.DataFrame(index=minute.index)
for c in cols:
    features[c]=pred[c]
    for lag in [1,5,15,30,60]:
        features[f'{c}_lag{lag}']=pred[c].shift(lag)
    for win in [5,15,60]:
        features[f'{c}_mean{win}']=pred[c].shift(1).rolling(win,min_periods=max(3,win//2)).mean()
        features[f'{c}_std{win}']=pred[c].shift(1).rolling(win,min_periods=max(3,win//2)).std()
features['hour_sin']=np.sin(2*np.pi*features.index.hour/24)
features['hour_cos']=np.cos(2*np.pi*features.index.hour/24)
features['dow_sin']=np.sin(2*np.pi*features.index.dayofweek/7)
features['dow_cos']=np.cos(2*np.pi*features.index.dayofweek/7)

valid_times=minute.index[minute['observed'].eq(1)]
cut1=valid_times[int(len(valid_times)*float(CFG['split']['train']))]
cut2=valid_times[int(len(valid_times)*(float(CFG['split']['train'])+float(CFG['split']['validation'])))]

def period_mask(idx,part):
    if part=='train': return idx<cut1
    if part=='validation': return (idx>=cut1)&(idx<cut2)
    return idx>=cut2

def metrics_reg(y,p,target):
    ok=np.isfinite(y)&np.isfinite(p)
    y=np.asarray(y)[ok]; p=np.asarray(p)[ok]
    res={'n':int(len(y)),'mae':float(mean_absolute_error(y,p)),
         'rmse':float(mean_squared_error(y,p)**0.5)}
    nz=np.abs(y)>1e-12
    res['mape_pct']=float(np.mean(np.abs((y[nz]-p[nz])/y[nz]))*100) if nz.any() else None
    if target=='mcs_dl': res['rounded_accuracy']=float(np.mean(np.rint(p)==np.rint(y)))
    return res

targets=list(CFG['forecast']['targets'])
horizons=list(CFG['forecast']['horizons_minutes'])
forecast_rows=[]
predictions=[]
feature_cols=list(features.columns)
for target in targets:
  for h in horizons:
    y=minute[target].shift(-h)
    ds=features.copy()
    ds['target']=y
    # Require target and current value; imputation handles noncritical predictor gaps.
    ds=ds[ds['target'].notna() & ds[target].notna()]
    tr=ds.index<cut1; va=(ds.index>=cut1)&(ds.index<cut2); te=ds.index>=cut2
    Xtr=ds.loc[tr,feature_cols]; ytr=ds.loc[tr,'target']
    Xva=ds.loc[va,feature_cols]; yva=ds.loc[va,'target']
    Xte=ds.loc[te,feature_cols]; yte=ds.loc[te,'target']
    models={
      'Persistencia':None,
      'Ridge':make_pipeline(SimpleImputer(strategy='median'),StandardScaler(),Ridge(alpha=1.0)),
      'HistGradientBoosting':make_pipeline(SimpleImputer(strategy='median'),HistGradientBoostingRegressor(max_iter=120,learning_rate=.07,max_leaf_nodes=31,l2_regularization=.2,random_state=SEED)),
    }
    for name,model in models.items():
        if model is None:
            pva=ds.loc[va,target].to_numpy(); pte=ds.loc[te,target].to_numpy()
        else:
            model.fit(Xtr,ytr)
            pva=model.predict(Xva); pte=model.predict(Xte)
        mv=metrics_reg(yva,pva,target); mt=metrics_reg(yte,pte,target)
        forecast_rows.append({'target':target,'horizon_min':h,'model':name,'split':'validation',**mv})
        forecast_rows.append({'target':target,'horizon_min':h,'model':name,'split':'test',**mt})
        if name in ('Persistencia','Ridge','HistGradientBoosting'):
            tmp=pd.DataFrame({'timestamp':Xte.index,'target':target,'horizon_min':h,'model':name,'actual':yte.to_numpy(),'predicted':pte})
            predictions.append(tmp)

forecast=pd.DataFrame(forecast_rows)
forecast.to_csv(OUT/'forecast_metrics.csv',index=False)
pd.concat(predictions,ignore_index=True).to_csv(OUT/'forecast_test_predictions.csv',index=False)

# Operational states from training-only robust quantiles. These are provisional proxy labels.
base=minute[['rssi_dl_dbm','snr_dl_db','mcs_dl','rate_dl_mbps']]
train_base=base.loc[base.index<cut1]
q={c:{str(p):float(train_base[c].quantile(p)) for p in [.01,.05,.10,.25]} for c in train_base.columns}

def state_from(df):
    low05=pd.DataFrame({c:df[c]<=q[c]['0.05'] for c in df.columns})
    low10=pd.DataFrame({c:df[c]<=q[c]['0.1'] for c in df.columns})
    critical=(low05.sum(axis=1)>=2) | (df['rate_dl_mbps']<=q['rate_dl_mbps']['0.01']) | (df['snr_dl_db']<=q['snr_dl_db']['0.01'])
    degraded=(low10.sum(axis=1)>=1)
    s=pd.Series('normal',index=df.index,dtype='object')
    s[degraded]='degraded'; s[critical]='critical'
    s[df.notna().sum(axis=1)<3]=np.nan
    return s

states=state_from(base)
minute['state_proxy']=states
state_counts=states.value_counts(dropna=False).to_dict()

# Predict state 15 minutes ahead using only current/past telemetry.
h=int(CFG['classification']['horizon_minutes'])
future_state=states.shift(-h)
ds=features.copy(); ds['target']=future_state
ds=ds[ds['target'].notna()]
tr=ds.index<cut1; te=ds.index>=cut2
Xtr=ds.loc[tr,feature_cols]; ytr=ds.loc[tr,'target']
Xte=ds.loc[te,feature_cols]; yte=ds.loc[te,'target']
clf=make_pipeline(SimpleImputer(strategy='median'),HistGradientBoostingClassifier(max_iter=140,learning_rate=.07,max_leaf_nodes=31,l2_regularization=.2,random_state=SEED,class_weight='balanced'))
clf.fit(Xtr,ytr)
pred_cls=clf.predict(Xte)
proba=clf.predict_proba(Xte); classes=clf.named_steps['histgradientboostingclassifier'].classes_
persist=states.reindex(Xte.index).fillna('normal').to_numpy()

def cls_metrics(name,p,proba_arr=None):
    res={'model':name,'horizon_min':h,'n':len(yte),'accuracy':accuracy_score(yte,p),
         'f1_macro':f1_score(yte,p,average='macro'),'f1_weighted':f1_score(yte,p,average='weighted'),
         'precision_macro':precision_score(yte,p,average='macro',zero_division=0),
         'recall_macro':recall_score(yte,p,average='macro',zero_division=0)}
    if proba_arr is not None:
        try: res['auc_ovr_macro']=roc_auc_score(yte,proba_arr,labels=classes,multi_class='ovr',average='macro')
        except Exception: res['auc_ovr_macro']=None
    return res
class_metrics=pd.DataFrame([cls_metrics('Persistencia',persist),cls_metrics('HistGradientBoosting',pred_cls,proba)])
class_metrics.to_csv(OUT/'classification_metrics.csv',index=False)
cm=pd.DataFrame(confusion_matrix(yte,pred_cls,labels=['normal','degraded','critical']),index=['actual_normal','actual_degraded','actual_critical'],columns=['pred_normal','pred_degraded','pred_critical'])
cm.to_csv(OUT/'classification_confusion.csv')

# Alert metrics: nonnormal event 15 minutes ahead.
actual_alert=(yte.to_numpy()!='normal'); predicted_alert=(pred_cls!='normal'); persist_alert=(persist!='normal')
alert_rows=[]
for name,p in [('Persistencia',persist_alert),('HistGradientBoosting',predicted_alert)]:
    tp=int((p&actual_alert).sum()); fp=int((p&~actual_alert).sum()); fn=int((~p&actual_alert).sum()); tn=int((~p&~actual_alert).sum())
    alert_rows.append({'model':name,'horizon_min':15,'tp':tp,'fp':fp,'fn':fn,'tn':tn,
                       'precision':tp/(tp+fp) if tp+fp else None,'recall':tp/(tp+fn) if tp+fn else None,
                       'false_alert_rate':fp/(fp+tn) if fp+tn else None})
pd.DataFrame(alert_rows).to_csv(OUT/'anticipation_metrics.csv',index=False)

# Isolation Forest on contemporaneous complete telemetry, fitted only on training.
anom_cols=['rssi_dl_dbm','rssi_ul_dbm','snr_dl_db','snr_ul_db','mcs_dl','mcs_ul','rate_dl_mbps']
anom=minute[anom_cols].dropna()
atr=anom.index<cut1
iso=make_pipeline(StandardScaler(),IsolationForest(n_estimators=int(CFG['anomaly_detection']['estimators']),contamination=float(CFG['anomaly_detection']['contamination']),random_state=SEED,n_jobs=-1))
iso.fit(anom.loc[atr])
score=-iso.decision_function(anom)
flag=(iso.predict(anom)==-1)
anomaly_df=anom.copy(); anomaly_df['anomaly_score']=score; anomaly_df['anomaly_flag']=flag.astype(int); anomaly_df['state_proxy']=states.reindex(anom.index)
anomaly_df.sort_values('anomaly_score',ascending=False).head(1000).reset_index().to_csv(OUT/'top_anomalies.csv',index=False)

# Daily summary and processed master.
master_out=minute.reset_index().rename(columns={'timestamp':'timestamp_local'})
master_out.to_csv(OUT/'master_minute.csv.gz',index=False,compression='gzip')
daily=master_out.assign(date=lambda z:z['timestamp_local'].dt.date).groupby('date').agg(
    records=('observed','sum'),rssi_dl_mean=('rssi_dl_dbm','mean'),rssi_dl_min=('rssi_dl_dbm','min'),
    snr_dl_mean=('snr_dl_db','mean'),snr_dl_min=('snr_dl_db','min'),mcs_dl_median=('mcs_dl','median'),
    rate_dl_mean=('rate_dl_mbps','mean'),rate_dl_min=('rate_dl_mbps','min'),
    normal=('state_proxy',lambda s:(s=='normal').sum()),degraded=('state_proxy',lambda s:(s=='degraded').sum()),critical=('state_proxy',lambda s:(s=='critical').sum())
).reset_index()
daily.to_csv(OUT/'daily_summary.csv',index=False)

summary={
 'raw_files':len(files),'raw_ap_rows':int(len(raw)),'master_minutes_total':int(len(minute)),
 'master_observed_minutes':int(minute['observed'].sum()),'period_start':str(minute.index.min()),'period_end':str(minute.index.max()),
 'train_end':str(cut1),'validation_end':str(cut2),'state_thresholds_training_only':q,'state_counts':{str(k):int(v) for k,v in state_counts.items()},
 'anomaly_complete_rows':int(len(anom)),'anomaly_flags':int(flag.sum()),
 'limitations':['Operational states are proxy labels derived from training quantiles, not field-validated ground truth.',
                'rate_dl_mbps is negotiated/data rate from dl_rate, not confirmed application throughput.',
                'Scenario/configuration and incident logs were not supplied.']
}
(OUT/'analysis_summary.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False),encoding='utf-8')
print(json.dumps(summary,indent=2,ensure_ascii=False))
print('\nFORECAST TEST\n',forecast[forecast.split.eq('test')].to_string(index=False))
print('\nCLASSIFICATION\n',class_metrics.to_string(index=False))
print('\nALERTS\n',pd.DataFrame(alert_rows).to_string(index=False))
