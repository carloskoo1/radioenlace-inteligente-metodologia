"""Cheap deterministic extension of the completed run; no model is refitted.

The additional simple baselines are explicitly exploratory sensitivity.
The main reanalyse.py now includes them in one complete reproducible run.
"""
import json
import numpy as np
import pandas as pd
from reanalyse import OUT,TARGET,bootstrap_calendar,train_mask,score

master=pd.read_csv(OUT/'minute_master.csv.gz')
master['timestamp']=pd.to_datetime(master.timestamp,utc=True).dt.tz_convert('America/Lima')
minute=master.set_index('timestamp')
pred=pd.read_csv(OUT/'predictions.csv.gz')
pred['timestamp']=pd.to_datetime(pred.timestamp,utc=True).dt.tz_convert('America/Lima')
new_names=['TrailingMean15','TrailingMean60','TrailingMedian60','TrainingMean','TrainingMedian']
pred=pred[~pred.model.isin(new_names)].copy()
splits=pd.read_csv(OUT/'splits.csv')
p=minute[TARGET].ffill(limit=1)
values={'TrailingMean15':p.rolling(15,min_periods=1).mean(),
        'TrailingMean60':p.rolling(60,min_periods=1).mean(),
        'TrailingMedian60':p.rolling(60,min_periods=1).median()}
parts=[pred]
for (fold,h),g in pred[pred.model.eq('Persistence')].groupby(['fold','horizon_min']):
    start=pd.Timestamp(splits.loc[(splits.fold==fold)&(splits.horizon_min==h),'test_start'].iloc[0])
    yy=minute[TARGET].shift(-int(h))
    tr=yy.notna() & p.notna() & train_mask(minute.index,start,int(h))
    for name in new_names:
        a=g.copy();a['model']=name
        if name=='TrainingMean':a['predicted']=float(yy[tr].mean())
        elif name=='TrainingMedian':a['predicted']=float(yy[tr].median())
        else:a['predicted']=values[name].reindex(g.timestamp).to_numpy()
        parts.append(a)
pred=pd.concat(parts,ignore_index=True)
assert pred.predicted.notna().all()
pred.to_csv(OUT/'predictions.csv.gz',index=False,compression='gzip')
rolling=[];pooled=[]
for (f,h,m),g in pred.groupby(['fold','horizon_min','model']):rolling.append(dict(fold=f,horizon_min=h,model=m,**score(g.actual,g.predicted)))
for (h,m),g in pred.groupby(['horizon_min','model']):pooled.append(dict(horizon_min=h,model=m,**score(g.actual,g.predicted)))
pd.DataFrame(rolling).to_csv(OUT/'rolling_metrics.csv',index=False)
po=pd.DataFrame(pooled)
po['mae_reduction_pct']=po.apply(lambda r:100*(1-r.mae/float(po.loc[(po.horizon_min==r.horizon_min)&po.model.eq('Persistence'),'mae'].iloc[0])),axis=1)
po.to_csv(OUT/'pooled_metrics.csv',index=False)
print(po.to_string(index=False),flush=True)
bootstrap_calendar(pred).to_csv(OUT/'bootstrap_calendar.csv',index=False)
pd.concat([bootstrap_calendar(pred,reference=ref,comparators=['Ridge_RF_noMCS','Ridge_Rate_only','HGB_RF_noMCS']) for ref in ['TrailingMean60','TrailingMedian60']],ignore_index=True).to_csv(OUT/'bootstrap_stronger_baselines.csv',index=False)
info=json.loads((OUT/'summary.json').read_text());info['additional_baselines']='Means 15/60, median 60, and training constants added as exploratory sensitivity after the first execution; all results retained.'
(OUT/'summary.json').write_text(json.dumps(info,indent=2))
print('BASELINE SENSITIVITY COMPLETE',flush=True)
