from pathlib import Path
import numpy as np, pandas as pd
import yaml
from sklearn.impute import SimpleImputer
from sklearn.pipeline import make_pipeline
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.inspection import permutation_importance
from sklearn.metrics import f1_score

ROOT=Path(__file__).resolve().parents[2]; OUT=ROOT/'results'/'tables'
CFG=yaml.safe_load((ROOT/'config'/'analysis.yml').read_text(encoding='utf-8'))
SEED=int(CFG['random_seed']); N_BOOT=int(CFG['bootstrap']['resamples']); BLOCK=int(CFG['bootstrap']['moving_block_minutes'])
rng=np.random.default_rng(SEED)

# Paired moving-block bootstrap for forecast MAE and RMSE differences.
p=pd.read_csv(OUT/'forecast_test_predictions.csv')
rows=[]
for (target,h),g in p.groupby(['target','horizon_min']):
    z=g.pivot_table(index='timestamp',columns='model',values=['actual','predicted'],aggfunc='first')
    actual=z[('actual','Persistencia')].to_numpy()
    base=z[('predicted','Persistencia')].to_numpy()
    n=len(actual); block=BLOCK; starts=np.arange(max(1,n-block+1))
    for model in ['Ridge','HistGradientBoosting']:
        pred=z[('predicted',model)].to_numpy()
        ok=np.isfinite(actual)&np.isfinite(base)&np.isfinite(pred)
        y,b,m=actual[ok],base[ok],pred[ok]; n=len(y); starts=np.arange(max(1,n-block+1))
        mae_gain=np.mean(np.abs(y-b))-np.mean(np.abs(y-m))
        rmse_gain=np.sqrt(np.mean((y-b)**2))-np.sqrt(np.mean((y-m)**2))
        bm=[]; br=[]
        for _ in range(N_BOOT):
            ss=rng.choice(starts,size=int(np.ceil(n/block)),replace=True)
            idx=np.concatenate([np.arange(s,min(s+block,n)) for s in ss])[:n]
            bm.append(np.mean(np.abs(y[idx]-b[idx]))-np.mean(np.abs(y[idx]-m[idx])))
            br.append(np.sqrt(np.mean((y[idx]-b[idx])**2))-np.sqrt(np.mean((y[idx]-m[idx])**2)))
        lo,hi=np.quantile(bm,[.025,.975]); rlo,rhi=np.quantile(br,[.025,.975])
        rows.append({'target':target,'horizon_min':h,'model':model,'n':n,
          'mae_reduction_abs':mae_gain,'mae_reduction_pct':100*mae_gain/np.mean(np.abs(y-b)),
          'mae_gain_ci_low':lo,'mae_gain_ci_high':hi,'mae_supported_95':bool(lo>0),
          'rmse_reduction_abs':rmse_gain,'rmse_reduction_pct':100*rmse_gain/np.sqrt(np.mean((y-b)**2)),
          'rmse_gain_ci_low':rlo,'rmse_gain_ci_high':rhi,'rmse_supported_95':bool(rlo>0)})
pd.DataFrame(rows).to_csv(OUT/'forecast_bootstrap_comparison.csv',index=False)

# Rebuild causal feature matrix and classifier for permutation-based explainability.
m=pd.read_csv(OUT/'master_minute.csv.gz')
m['timestamp_local']=pd.to_datetime(m.timestamp_local,errors='coerce')
m=m.set_index('timestamp_local').sort_index()
cols=['rssi_dl_dbm','rssi_ul_dbm','snr_dl_db','snr_ul_db','mcs_dl','mcs_ul','rate_dl_mbps']
pred=m[cols].ffill(limit=1); f=pd.DataFrame(index=m.index)
for c in cols:
    f[c]=pred[c]
    for lag in [1,5,15,30,60]: f[f'{c}_lag{lag}']=pred[c].shift(lag)
    for win in [5,15,60]:
        f[f'{c}_mean{win}']=pred[c].shift(1).rolling(win,min_periods=max(3,win//2)).mean()
        f[f'{c}_std{win}']=pred[c].shift(1).rolling(win,min_periods=max(3,win//2)).std()
f['hour_sin']=np.sin(2*np.pi*f.index.hour/24); f['hour_cos']=np.cos(2*np.pi*f.index.hour/24)
f['dow_sin']=np.sin(2*np.pi*f.index.dayofweek/7); f['dow_cos']=np.cos(2*np.pi*f.index.dayofweek/7)
feature_cols=list(f.columns)
valid_times=m.index[m.observed.eq(1)]; cut1=valid_times[int(len(valid_times)*float(CFG['split']['train']))]; cut2=valid_times[int(len(valid_times)*(float(CFG['split']['train'])+float(CFG['split']['validation'])))]
y=m.state_proxy.shift(-15); ds=f.copy(); ds['target']=y; ds=ds[ds.target.notna()]
tr=ds.index<cut1; te=ds.index>=cut2
Xtr=ds.loc[tr,feature_cols]; ytr=ds.loc[tr,'target']; Xte=ds.loc[te,feature_cols]; yte=ds.loc[te,'target']
clf=make_pipeline(SimpleImputer(strategy='median'),HistGradientBoostingClassifier(max_iter=140,learning_rate=.07,max_leaf_nodes=31,l2_regularization=.2,random_state=SEED,class_weight='balanced'))
clf.fit(Xtr,ytr); pred_hgb=clf.predict(Xte); pred_per=m.state_proxy.reindex(Xte.index).fillna('normal').to_numpy()

# Moving-block bootstrap difference in macro F1.
n=len(yte); block=BLOCK; starts=np.arange(n-block+1); diffs=[]
yt=yte.to_numpy()
for _ in range(N_BOOT):
    ss=rng.choice(starts,size=int(np.ceil(n/block)),replace=True)
    idx=np.concatenate([np.arange(s,min(s+block,n)) for s in ss])[:n]
    diffs.append(f1_score(yt[idx],pred_hgb[idx],average='macro')-f1_score(yt[idx],pred_per[idx],average='macro'))
lo,hi=np.quantile(diffs,[.025,.975])
pd.DataFrame([{'metric':'f1_macro','horizon_min':15,'difference_hgb_minus_persistence':f1_score(yt,pred_hgb,average='macro')-f1_score(yt,pred_per,average='macro'),'ci_low':lo,'ci_high':hi,'supported_95':bool(lo>0)}]).to_csv(OUT/'classification_bootstrap_comparison.csv',index=False)

# Permutation importance on a time-spread subset, using macro F1.
sel=np.linspace(0,len(Xte)-1,min(3000,len(Xte)),dtype=int)
pi=permutation_importance(clf,Xte.iloc[sel],yte.iloc[sel],scoring='f1_macro',n_repeats=3,random_state=SEED,n_jobs=1)
imp=pd.DataFrame({'feature':feature_cols,'importance_mean':pi.importances_mean,'importance_std':pi.importances_std}).sort_values('importance_mean',ascending=False)
imp.to_csv(OUT/'classification_feature_importance.csv',index=False)

# Anomaly distribution.
a=pd.read_csv(OUT/'top_anomalies.csv'); a=a[a.anomaly_flag.eq(1)].copy(); a['timestamp']=pd.to_datetime(a.timestamp,errors='coerce')
state=a.state_proxy.fillna('sin_estado').value_counts().rename_axis('state').reset_index(name='count'); state['pct']=100*state['count']/state['count'].sum(); state.to_csv(OUT/'anomaly_by_state.csv',index=False)

# Supplemental radio-climate Spearman correlations (contemporaneous, not causal).
c=pd.read_csv(ROOT/'data/auxiliary/dataset_final_radio_clima.csv')
rf=['dl_rssi','dl_snr']; met=['temp_c','dewpoint_c','precip_mm','press_hpa','wind_ms']
cr=c[rf+met].corr(method='spearman').loc[met,rf].reset_index().rename(columns={'index':'meteorological_variable'})
cr.to_csv(OUT/'radio_climate_spearman.csv',index=False)
print(pd.DataFrame(rows).to_string(index=False))
print('\nCLASS BOOT\n',pd.read_csv(OUT/'classification_bootstrap_comparison.csv').to_string(index=False))
print('\nTOP FEATURES\n',imp.head(15).to_string(index=False))
print('\nCLIMATE\n',cr.to_string(index=False))
