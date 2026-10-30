"""Retrospective article extension. Does not overwrite thesis artifacts.

Run with Python 3.12 and repository requirements. Origins are CLOSED minute
bins. No future target is filled; current predictors may be carried 1 minute.
"""
from pathlib import Path
import argparse, hashlib, importlib.metadata, json, platform, sys, zipfile
import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge
from sklearn.ensemble import HistGradientBoostingRegressor
from threadpoolctl import threadpool_limits

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
OUT=HERE/'results'
SEED=42
EXPECTED='786a037e749ce0c5bf7b3d8bd66f419a0a76de809c68857534e03487fc922bfa'
TARGET='rate_dl_mbps'
COLS=['rssi_dl_dbm','rssi_ul_dbm','snr_dl_db','snr_ul_db','mcs_dl','mcs_ul',TARGET]

def load_minutes():
    archive=ROOT/'data/raw/Datos.zip'
    assert hashlib.sha256(archive.read_bytes()).hexdigest()==EXPECTED
    parts=[]
    with zipfile.ZipFile(archive) as z:
        names=sorted(n for n in z.namelist() if n.endswith('.csv'))
        for name in names:
            with z.open(name) as f:
                x=pd.read_csv(f,dtype=str,low_memory=False)
            x=x.loc[x.role.eq('AP')].copy()
            x['_file']=name
            parts.append(x)
    raw=pd.concat(parts,ignore_index=True)
    raw['timestamp']=pd.to_datetime(raw.ts,errors='coerce',utc=True).dt.tz_convert('America/Lima')
    raw=raw.sort_values('timestamp').drop_duplicates('timestamp',keep='last')
    for a,b in {'sta_dl_rssi':'rssi_dl_dbm','sta_ul_rssi':'rssi_ul_dbm','snr_dl':'snr_dl_db','snr_ul':'snr_ul_db','mcs_dl':'mcs_dl','mcs_ul':'mcs_ul'}.items():
        raw[b]=pd.to_numeric(raw[a].str.strip(),errors='coerce')
    raw[TARGET]=pd.to_numeric(raw.dl_rate.str.extract(r'([-+]?\d+(?:\.\d+)?)')[0],errors='coerce')
    for c in ['rssi_dl_dbm','rssi_ul_dbm']:raw.loc[raw[c]>=0,c]=np.nan
    for c in ['snr_dl_db','snr_ul_db']:raw.loc[raw[c]<=0,c]=np.nan
    minute=raw.set_index('timestamp')[COLS].resample('1min').median()
    info={'raw_files':len(names),'raw_ap_rows':len(raw),'minutes':len(minute),
          'observed_minutes':int(minute.notna().any(axis=1).sum()),
          'target_observed':int(minute[TARGET].notna().sum()),
          'start':str(minute.index.min()),'end':str(minute.index.max()),
          'mcs_dl_raw_unique':sorted(raw.mcs_dl.dropna().unique().tolist()),
          'mcs_dl_minute_noninteger':int(((minute.mcs_dl.dropna()%1)!=0).sum()),
          'dl_rate_raw_examples':raw.dl_rate.drop_duplicates().head(10).tolist()}
    return minute,info

def make_features(minute,columns):
    p=minute[columns].ffill(limit=1)
    x=pd.DataFrame(index=minute.index)
    for c in columns:
        x[c]=p[c]
        for lag in [1,5,15,30,60]:x[f'{c}_lag{lag}']=p[c].shift(lag)
        for w in [5,15,60]:
            v=p[c].shift(1).rolling(w,min_periods=max(3,w//2))
            x[f'{c}_mean{w}']=v.mean();x[f'{c}_std{w}']=v.std()
    x['hour_sin']=np.sin(2*np.pi*x.index.hour/24)
    x['hour_cos']=np.cos(2*np.pi*x.index.hour/24)
    x['dow_sin']=np.sin(2*np.pi*x.index.dayofweek/7)
    x['dow_cos']=np.cos(2*np.pi*x.index.dayofweek/7)
    return x

def train_mask(index,cut,h,purge=True):
    return (index+pd.Timedelta(minutes=h)<cut) if purge else index<cut

def score(y,p):
    e=np.asarray(y)-np.asarray(p)
    return {'n':len(e),'mae':float(np.abs(e).mean()),'rmse':float(np.sqrt(np.square(e).mean()))}

def new_model(name):
    if name=='Ridge':return make_pipeline(SimpleImputer(strategy='median'),StandardScaler(),Ridge(alpha=1.0))
    return make_pipeline(SimpleImputer(strategy='median'),HistGradientBoostingRegressor(max_iter=120,learning_rate=.07,max_leaf_nodes=31,l2_regularization=.2,random_state=SEED,early_stopping=False))

def bootstrap_calendar(predictions,resamples=1000,reference='Persistence',comparators=None):
    """Paired, stratified by fold; circular CALENDAR blocks retain missing minutes.

    Each fold resamples its original calendar duration. All models use the
    same eligible origins. Percentile intervals are conditional, unadjusted
    for multiple models/horizons, and do not represent spatial uncertainty.
    """
    out=[]
    for h,hdf in predictions.groupby('horizon_min'):
        models=sorted(set(hdf.model)-{reference}) if comparators is None else comparators
        piv=hdf.pivot(index=['fold','timestamp'],columns='model',values='predicted')
        actual=hdf.drop_duplicates(['fold','timestamp']).set_index(['fold','timestamp']).actual
        for length in [60,180,1440]:
            # Stable seed independent of Python's hash randomization.
            rng=np.random.default_rng(SEED+int(h)*10000+length)
            sums={m:np.zeros((resamples,5)) for m in models}
            for fold,fp in piv.groupby(level=0):
                fp=fp.droplevel(0); yy=actual.xs(fold,level=0).reindex(fp.index)
                idx=pd.date_range(fp.index.min(),fp.index.max(),freq='1min')
                n=len(idx);L=min(length,n)
                blocks=int(np.ceil(n/L)); starts=rng.integers(0,n,size=(resamples,blocks))
                # Trim the last drawn block to exactly the original duration.
                widths=np.full(blocks,L);widths[-1]=n-L*(blocks-1)
                b=np.abs(yy-fp[reference]).reindex(idx).to_numpy()
                for model in models:
                    mm=np.abs(yy-fp[model]).reindex(idx).to_numpy()
                    a=np.column_stack([np.nan_to_num(b),np.nan_to_num(mm),np.nan_to_num(b*b),np.nan_to_num(mm*mm),np.isfinite(b).astype(float)])
                    ext=np.concatenate([a,a[:L]],axis=0)
                    cs=np.vstack([np.zeros((1,5)),np.cumsum(ext,axis=0)])
                    stats=(cs[starts+widths[None,:]]-cs[starts]).sum(axis=1)
                    sums[model]+=stats
            for model,st in sums.items():
                d_mae=(st[:,0]-st[:,1])/st[:,4]
                d_rmse=np.sqrt(st[:,2]/st[:,4])-np.sqrt(st[:,3]/st[:,4])
                for metric,d in [('mae',d_mae),('rmse',d_rmse)]:
                    out.append({'horizon_min':int(h),'reference':reference,'model':model,'block_minutes':length,'metric':metric,
                                'improvement_ci_low':float(np.quantile(d,.025)),
                                'improvement_ci_high':float(np.quantile(d,.975)),
                                'resamples':resamples})
    return pd.DataFrame(out)

def self_test():
    ix=pd.date_range('2026-01-01',periods=100,freq='1min',tz='UTC');cut=ix[70]
    for h in [5,15,30]:
        mask=train_mask(ix,cut,h)
        assert ((ix[mask]+pd.Timedelta(minutes=h))<cut).all()
        assert mask.sum()==70-h
    frame=pd.DataFrame({c:np.arange(100,dtype=float) for c in COLS},index=ix)
    a=make_features(frame,COLS); changed=frame.copy();changed.loc[ix[51]:,:]=99999
    b=make_features(changed,COLS)
    pd.testing.assert_frame_equal(a.loc[:ix[50]],b.loc[:ix[50]])
    missing=frame.copy();missing.loc[ix[72],TARGET]=np.nan
    assert pd.isna(missing[TARGET].shift(-5).loc[ix[67]])
    # Calendar blocks with identical forecasts must have zero paired difference.
    rows=[]
    for t in ix[::3]:
        for m in ['Persistence','Ridge_RF_noMCS']:
            rows.append(dict(fold=1,timestamp=t,horizon_min=5,model=m,actual=3.,predicted=2.))
    z=bootstrap_calendar(pd.DataFrame(rows),20)
    assert (z.improvement_ci_low==0).all() and (z.improvement_ci_high==0).all()
    print('PASS: purge, causal features, unfilled future, paired calendar bootstrap',flush=True)

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    self_test()
    minute,info=load_minutes();print(json.dumps(info,indent=2),flush=True)
    assert info['raw_ap_rows']==173513 and info['observed_minutes']==118458
    observed=minute.index[minute.notna().any(axis=1)]
    sets={
      'RF_noMCS':[c for c in COLS if not c.startswith('mcs')],
      'RF_withMCS':COLS,
      'Rate_only':[TARGET],
    }
    features={k:make_features(minute,v) for k,v in sets.items()}
    metrics=[];predictions=[];splits=[];audit=[]
    cut1=observed[int(len(observed)*.7)];cut2=observed[int(len(observed)*.85)]
    for h in [5,15,30]:
        y=minute[TARGET].shift(-h)
        eligible=y.notna() & minute[TARGET].ffill(limit=1).notna()
        for mode,purge in [('original_unpurged',False),('corrected_purged',True)]:
            tr=eligible & train_mask(minute.index,cut1,h,purge)
            te=eligible & (minute.index>=cut2)
            model=new_model('Ridge');model.fit(features['RF_withMCS'].loc[tr],y[tr])
            pp=model.predict(features['RF_withMCS'].loc[te])
            audit.append({'mode':mode,'horizon_min':h,'train_n':int(tr.sum()),'candidate_boundary_crossing_rows':int((eligible & (minute.index<cut1) & (minute.index+pd.Timedelta(minutes=h)>=cut1)).sum()),'retained_boundary_crossing_rows':int((tr & (minute.index+pd.Timedelta(minutes=h)>=cut1)).sum()),**score(y[te],pp)})
    for fold,frac in enumerate([.5,.6,.7,.8,.9],1):
        start=observed[int(len(observed)*frac)]
        stop=observed[int(len(observed)*(frac+.1))] if frac<.9 else minute.index.max()+pd.Timedelta(minutes=1)
        for h in [5,15,30]:
            y=minute[TARGET].shift(-h)
            eligible=y.notna() & minute[TARGET].ffill(limit=1).notna()
            tr=eligible & train_mask(minute.index,start,h)
            te=eligible & (minute.index>=start) & (minute.index+pd.Timedelta(minutes=h)<stop)
            assert (minute.index[tr].max()+pd.Timedelta(minutes=h))<start
            assert (minute.index[te].max()+pd.Timedelta(minutes=h))<stop
            splits.append({'fold':fold,'horizon_min':h,'train_n':int(tr.sum()),'test_n':int(te.sum()),'train_origin_end':str(minute.index[tr].max()),'train_label_end':str(minute.index[tr].max()+pd.Timedelta(minutes=h)),'test_start':str(start),'test_end_exclusive':str(stop),'test_origin_start':str(minute.index[te].min()),'test_origin_end':str(minute.index[te].max()),'test_target_missing_rows':int(((minute.index>=start)&(minute.index<stop)&y.isna()).sum())})
            # Primary comparisons and prespecified feature ablations.
            configurations=[('Persistence',None,None),('TrailingMean5',None,None),
              ('TrailingMean15',None,None),('TrailingMean60',None,None),
              ('TrailingMedian60',None,None),('TrainingMean',None,None),('TrainingMedian',None,None),
              ('Ridge_RF_noMCS','Ridge','RF_noMCS'),('HGB_RF_noMCS','HGB','RF_noMCS'),
              ('Ridge_RF_withMCS','Ridge','RF_withMCS'),('Ridge_Rate_only','Ridge','Rate_only')]
            for name,kind,feature_set in configurations:
                if name=='Persistence':p=minute[TARGET].ffill(limit=1)[te].to_numpy()
                elif name.startswith('TrailingMean'):
                    w=int(name.replace('TrailingMean',''));p=minute[TARGET].ffill(limit=1).rolling(w,min_periods=1).mean()[te].to_numpy()
                elif name=='TrailingMedian60':p=minute[TARGET].ffill(limit=1).rolling(60,min_periods=1).median()[te].to_numpy()
                elif name=='TrainingMean':p=np.full(te.sum(),y[tr].mean())
                elif name=='TrainingMedian':p=np.full(te.sum(),y[tr].median())
                else:
                    x=features[feature_set];model=new_model(kind);model.fit(x.loc[tr],y[tr]);p=model.predict(x.loc[te])
                metrics.append({'fold':fold,'horizon_min':h,'model':name,**score(y[te],p)})
                predictions.append(pd.DataFrame({'fold':fold,'timestamp':minute.index[te],'horizon_min':h,'model':name,'actual':y[te].to_numpy(),'predicted':p}))
            print(f'Completed fold {fold}, horizon {h}, train={tr.sum()}, test={te.sum()}',flush=True)
            pd.DataFrame(metrics).to_csv(OUT/'rolling_metrics.csv',index=False)
    pr=pd.concat(predictions,ignore_index=True)
    prediction_temp=OUT/'predictions.tmp.gz'
    pr.to_csv(prediction_temp,index=False,compression='gzip')
    prediction_temp.replace(OUT/'predictions.csv.gz')
    pd.DataFrame(splits).to_csv(OUT/'splits.csv',index=False)
    pd.DataFrame(audit).to_csv(OUT/'boundary_audit.csv',index=False)
    pooled=[]
    for (h,m),g in pr.groupby(['horizon_min','model']):pooled.append({'horizon_min':h,'model':m,**score(g.actual,g.predicted)})
    po=pd.DataFrame(pooled)
    po['mae_reduction_pct']=po.apply(lambda r:100*(1-r.mae/float(po.loc[(po.horizon_min==r.horizon_min)&po.model.eq('Persistence'),'mae'].iloc[0])),axis=1)
    po.to_csv(OUT/'pooled_metrics.csv',index=False)
    print(po.to_string(index=False),flush=True)
    ci=bootstrap_calendar(pr)
    ci.to_csv(OUT/'bootstrap_calendar.csv',index=False)
    sensitivity=pd.concat([bootstrap_calendar(pr,reference=ref,comparators=['Ridge_RF_noMCS','Ridge_Rate_only','HGB_RF_noMCS']) for ref in ['TrailingMean60','TrailingMedian60']],ignore_index=True)
    sensitivity.to_csv(OUT/'bootstrap_stronger_baselines.csv',index=False)
    master_temp=OUT/'minute_master.tmp.gz'
    minute.reset_index().to_csv(master_temp,index=False,compression='gzip')
    master_temp.replace(OUT/'minute_master.csv.gz')
    info.update({'seed':SEED,'platform':platform.platform(),'python':sys.version,
       'packages':{p:importlib.metadata.version(p) for p in ['numpy','pandas','scikit-learn','scipy','threadpoolctl']},
       'raw_sha256':EXPECTED,'features':{k:len(x.columns) for k,x in features.items()},
       'primary_model':'Ridge_RF_noMCS','primary_metric':'MAE','primary_horizon_minutes':15,
       'selection':'Fixed thesis hyperparameters; no tuning or test-based selection in this extension.',
       'hgb_early_stopping':False,
       'additional_baselines':'Means 15/60, median 60, and training constants added as exploratory sensitivity after the first execution; all results retained.',
       'scope':'Retrospective robustness on previously analysed link; no independent external validation.'})
    (OUT/'summary.json').write_text(json.dumps(info,indent=2))
    print('ALL COMPLETE',flush=True)

if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--self-test',action='store_true');args=a.parse_args()
    with threadpool_limits(limits=2):
        if args.self_test:self_test()
        else:main()
