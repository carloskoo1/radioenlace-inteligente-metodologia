from pathlib import Path
import pandas as pd, numpy as np, matplotlib.pyplot as plt, seaborn as sns

ROOT=Path(__file__).resolve().parents[2]; R=ROOT/'results'/'tables'; O=ROOT/'results'/'figures'; O.mkdir(parents=True,exist_ok=True)
sns.set_theme(style='whitegrid',font_scale=.95); colors={'blue':'#1F4E79','orange':'#ED7D31','green':'#70AD47','red':'#C00000','gray':'#7F8C8D'}

daily=pd.read_csv(R/'daily_summary.csv'); daily['date']=pd.to_datetime(daily.date)

fig,ax=plt.subplots(figsize=(10,4.5)); ax.bar(daily.date,daily.records,color=colors['blue'],width=.9); ax.axhline(1440,color=colors['orange'],ls='--',lw=1.5,label='Máximo teórico diario (1 440 min)'); ax.set(ylabel='Minutos con observación',xlabel='Fecha'); ax.legend(frameon=False,loc='lower right'); fig.tight_layout(); fig.savefig(O/'figura_4_1_disponibilidad.png',dpi=240,bbox_inches='tight'); plt.close(fig)

fig,axs=plt.subplots(4,1,figsize=(10,9),sharex=True)
series=[('rssi_dl_mean','RSSI DL medio (dBm)',colors['blue']),('snr_dl_mean','SNR DL medio (dB)',colors['orange']),('mcs_dl_median','MCS DL mediano',colors['green']),('rate_dl_mean','Tasa DL media (Mbps)',colors['red'])]
for ax,(c,l,co) in zip(axs,series): ax.plot(daily.date,daily[c],color=co,lw=1.2); ax.set_ylabel(l); ax.grid(alpha=.3)
axs[-1].set_xlabel('Fecha'); fig.tight_layout(); fig.savefig(O/'figura_4_2_telemetria_diaria.png',dpi=240,bbox_inches='tight'); plt.close(fig)

summary=__import__('json').loads((R/'analysis_summary.json').read_text()); sc=summary['state_counts']; labels=['Normal','Degradado','Crítico']; vals=[sc['normal'],sc['degraded'],sc['critical']]
fig,ax=plt.subplots(figsize=(7.2,4.6)); bars=ax.bar(labels,vals,color=[colors['green'],colors['orange'],colors['red']]); ax.set_ylabel('Minutos clasificados'); ax.bar_label(bars,labels=[f'{v:,}\n({100*v/sum(vals):.1f} %)' for v in vals],padding=3); ax.set_ylim(0,max(vals)*1.18); fig.tight_layout(); fig.savefig(O/'figura_4_3_estados.png',dpi=240,bbox_inches='tight'); plt.close(fig)

cm=pd.read_csv(R/'classification_confusion.csv',index_col=0); cm.index=['Normal','Degradado','Crítico']; cm.columns=['Normal','Degradado','Crítico']
fig,ax=plt.subplots(figsize=(6.3,5)); sns.heatmap(cm,annot=True,fmt=',d',cmap='Blues',cbar=False,ax=ax); ax.set(xlabel='Estado pronosticado',ylabel='Estado observado'); fig.tight_layout(); fig.savefig(O/'figura_4_4_confusion.png',dpi=240,bbox_inches='tight'); plt.close(fig)

boot=pd.read_csv(R/'forecast_bootstrap_comparison.csv'); targets=[('rssi_dl_dbm','RSSI'),('mcs_dl','MCS'),('rate_dl_mbps','Tasa DL')]
fig,axs=plt.subplots(1,3,figsize=(11,4.2),sharey=False)
for ax,(t,title) in zip(axs,targets):
 g=boot[boot.target.eq(t)]; x=np.arange(3); w=.34
 for j,(model,co) in enumerate([('Ridge',colors['blue']),('HistGradientBoosting',colors['orange'])]):
  q=g[g.model.eq(model)].sort_values('horizon_min'); ax.bar(x+(j-.5)*w,q.rmse_reduction_pct,width=w,label=model,color=co)
 ax.axhline(0,color='black',lw=.8); ax.set_xticks(x,['5','15','30']); ax.set_title(title); ax.set_xlabel('Horizonte (min)'); ax.set_ylabel('Reducción del RMSE (%)')
axs[0].legend(frameon=False,fontsize=8); fig.tight_layout(); fig.savefig(O/'figura_4_5_reduccion_rmse.png',dpi=240,bbox_inches='tight'); plt.close(fig)

al=pd.read_csv(R/'anticipation_metrics.csv'); metrics=['precision','recall','false_alert_rate']; labs=['Precisión','Recall','Tasa de falsas alertas']; x=np.arange(3); w=.34
fig,ax=plt.subplots(figsize=(7.6,4.8))
for j,(model,co) in enumerate([('Persistencia',colors['gray']),('HistGradientBoosting',colors['blue'])]):
 q=al[al.model.eq(model)].iloc[0]; ax.bar(x+(j-.5)*w,[q[m]*100 for m in metrics],width=w,label=model,color=co)
ax.set_xticks(x,labs); ax.set_ylabel('Porcentaje (%)'); ax.legend(frameon=False); fig.tight_layout(); fig.savefig(O/'figura_4_6_alertas.png',dpi=240,bbox_inches='tight'); plt.close(fig)

a=pd.read_csv(R/'top_anomalies.csv'); a=a[a.anomaly_flag.eq(1)].copy(); a['timestamp']=pd.to_datetime(a.timestamp); a=a.sort_values('timestamp')
fig,ax=plt.subplots(figsize=(10,4.7)); ax.scatter(a.timestamp,a.rate_dl_mbps,c=a.anomaly_score,cmap='Reds',s=22,alpha=.75); ax.set(xlabel='Fecha',ylabel='Tasa DL en anomalías (Mbps)'); cb=fig.colorbar(ax.collections[0],ax=ax); cb.set_label('Puntuación de anomalía'); fig.tight_layout(); fig.savefig(O/'figura_4_7_anomalias.png',dpi=240,bbox_inches='tight'); plt.close(fig)

imp=pd.read_csv(R/'classification_feature_importance.csv').head(12).sort_values('importance_mean')
fig,ax=plt.subplots(figsize=(8.2,5.5)); ax.barh(imp.feature,imp.importance_mean,xerr=imp.importance_std,color=colors['blue'],alpha=.9); ax.set_xlabel('Disminución media del F1-macro por permutación'); fig.tight_layout(); fig.savefig(O/'figura_4_8_importancia.png',dpi=240,bbox_inches='tight'); plt.close(fig)

c=pd.read_csv(R/'radio_climate_spearman.csv').set_index('meteorological_variable'); c.index=['Temperatura','Punto de rocío','Precipitación','Presión','Viento']; c.columns=['RSSI DL','SNR DL']
fig,ax=plt.subplots(figsize=(6.5,4.7)); sns.heatmap(c,annot=True,fmt='.2f',cmap='RdBu_r',center=0,vmin=-.5,vmax=.5,ax=ax); ax.set(xlabel='Indicador radioeléctrico',ylabel='Variable meteorológica'); fig.tight_layout(); fig.savefig(O/'figura_4_9_correlacion_clima.png',dpi=240,bbox_inches='tight'); plt.close(fig)
print('\n'.join(str(p) for p in sorted(O.glob('*.png'))))
