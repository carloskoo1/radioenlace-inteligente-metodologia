"""Dashboard para resultados reales del pipeline de tesis, sin adquisición RF en vivo."""
from pathlib import Path
import json
import hashlib
import subprocess
import sys
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results" / "tables"
ZIP = ROOT / "data" / "raw" / "Datos.zip"
SHA = "786a037e749ce0c5bf7b3d8bd66f419a0a76de809c68857534e03487fc922bfa"
st.set_page_config(page_title="Sistema inteligente Cuñacales–San José", page_icon="📡", layout="wide")
st.title("📡 Sistema inteligente: radioenlace Cuñacales–San José")
st.caption("Ubelser Tamay · Universidad Nacional de Cajamarca · Investigación con datos de campo")
st.info("Este dashboard es una extensión posterior del sistema científico. Explora resultados "
        "del pipeline histórico; no hay telemetría en vivo ni alarmas autónomas. "
        "Los estados operacionales son etiquetas proxy, no fallas de campo confirmadas.")

@st.cache_data
def csv(name, **kw):
    return pd.read_csv(OUT / name, **kw)

@st.cache_data
def summary():
    return json.loads((OUT / "analysis_summary.json").read_text(encoding="utf-8"))

def exists(name):
    return (OUT / name).exists()

def downloadable(df, name, key):
    st.download_button("Descargar CSV", data=df.to_csv(index=False),
                       file_name=name, mime="text/csv", key=key)

tabs=st.tabs(["Producto","Calidad de datos","Diagnóstico","Pronóstico",
              "Alertas","Anomalías","Explicabilidad","Reproducibilidad"])
with tabs[0]:
    st.subheader("¿Qué producto construyó la tesis?")
    st.markdown("El producto original es un **sistema computacional modular por lotes**: "
                "prepara telemetría de un radioenlace real, diagnostica estados, "
                "detecta anomalías, pronostica RSSI/MCS/tasa DL y explica resultados. "
                "La interfaz visual se desarrolló después, como extensión de demostración.")
    st.code("TELEMETRÍA → DEPURACIÓN → CARACTERÍSTICAS TEMPORALES → MODELOS → RESULTADOS")
    st.markdown("[Versión científica fija 1.0.0](https://github.com/carloskoo1/radioenlace-inteligente-metodologia/releases/tag/v1.0.0)")
    if exists("analysis_summary.json"):
        x=summary()
        a,b,c=st.columns(3)
        a.metric("Archivos originales", x["raw_files"])
        b.metric("Registros AP", f'{x["raw_ap_rows"]:,}')
        c.metric("Minutos observados", f'{x["master_observed_minutes"]:,}')
with tabs[1]:
    st.subheader("OE1 · Calidad de telemetría y comportamiento temporal")
    if exists("analysis_summary.json"):
        x=summary()
        a,b=st.columns(2)
        a.metric("Cobertura temporal", f'{100*x["master_observed_minutes"]/x["master_minutes_total"]:.2f}%')
        b.metric("Completitud entre minutos observados", f'{100*x["anomaly_complete_rows"]/x["master_observed_minutes"]:.2f}%')
        st.caption("Los dos porcentajes tienen denominadores distintos. "
                   "Se conservaron los intervalos sin adquisición.")
    if exists("daily_summary.csv"):
        d=csv("daily_summary.csv")
        d["date"]=pd.to_datetime(d["date"])
        st.line_chart(d.set_index("date")[["records"]],y_label="Minutos observados por día")
        downloadable(d,"calidad_diaria.csv","dl_cal")
    if exists("master_minute.csv.gz"):
        d=csv("master_minute.csv.gz")
        metric=st.selectbox("Métrica del radio", ["rssi_dl_dbm","snr_dl_db","mcs_dl","rate_dl_mbps"])
        d["timestamp_local"]=pd.to_datetime(d["timestamp_local"], errors="coerce")
        st.line_chart(d.set_index("timestamp_local")[[metric]].resample("D").median())
with tabs[2]:
    st.subheader("OE3 · Comparación del diagnóstico")
    if exists("classification_metrics.csv"):
        d=csv("classification_metrics.csv")
        st.dataframe(d,hide_index=True,use_container_width=True)
        st.caption("F1-macro pondera por igual las tres clases; AUC representa discriminación y no porcentaje de aciertos.")
        if exists("classification_bootstrap_comparison.csv"):
            q=csv("classification_bootstrap_comparison.csv").iloc[0]
            st.warning(f'Mejora de F1-macro: {q.difference_hgb_minus_persistence:.3f}; '
                       f'intervalo 95% [{q.ci_low:.3f}, {q.ci_high:.3f}]. '
                       'Incluye cero: la mejora no fue concluyente.')
        if exists("classification_confusion.csv"):
            st.dataframe(csv("classification_confusion.csv",index_col=0),use_container_width=True)
        downloadable(d,"diagnostico.csv","dl_clas")
with tabs[3]:
    st.subheader("OE3 · Pronóstico de indicadores de radioenlace")
    if exists("forecast_metrics.csv"):
        d=csv("forecast_metrics.csv")
        d=d.loc[d.split.eq("test")]
        col1,col2=st.columns(2)
        metric=col1.selectbox("Variable", sorted(d.target.unique()))
        horizon=col2.selectbox("Horizonte", sorted(d.horizon_min.unique()),
                               format_func=lambda v:f"{v} minutos")
        v=d.loc[d.target.eq(metric)&d.horizon_min.eq(horizon)].copy()
        st.bar_chart(v.set_index("model")[["mae"]], y_label="MAE: error promedio (menor es mejor)")
        st.dataframe(v[["model","n","mae","rmse","mape_pct"]],hide_index=True,use_container_width=True)
        st.caption("Persistencia = utilizar el último valor. RMSE penaliza errores grandes. "
                   "La tasa DL es la negociada por el radio; NO throughput de aplicación.")
        if exists("forecast_test_predictions.csv"):
            p=csv("forecast_test_predictions.csv")
            p=p.loc[p.target.eq(metric)&p.horizon_min.eq(horizon)].copy()
            p["timestamp"]=pd.to_datetime(p["timestamp"],errors="coerce")
            days=sorted(p.timestamp.dt.date.dropna().unique())
            if len(days)>0:
                day=st.selectbox("Día para visualizar medición versus predicción",days)
                z=p.loc[p.timestamp.dt.date.eq(day)]
                pred=z.pivot_table(index="timestamp",columns="model",values="predicted")
                obs=z.drop_duplicates("timestamp").set_index("timestamp")[["actual"]]
                st.line_chart(obs.join(pred))
        downloadable(v,"metricas_pronostico.csv","dl_for")
    else:
        st.warning("Ejecute el pipeline para generar métricas.")
with tabs[4]:
    st.subheader("OE4 · Alertas anticipadas a 15 minutos")
    if exists("anticipation_metrics.csv"):
        a=csv("anticipation_metrics.csv")
        st.dataframe(a,hide_index=True,use_container_width=True)
        st.bar_chart(a.set_index("model")[["recall","false_alert_rate"]])
        row_hgb=a.loc[a.model.eq("HistGradientBoosting")].iloc[0]
        row_ref=a.loc[a.model.eq("Persistencia")].iloc[0]
        total=int(row_hgb.tp+row_hgb.fn)
        st.markdown(f"**{int(row_hgb.tp):,} de {total:,}** condiciones futuras proxy "
                    f"anticipadas frente a **{int(row_ref.tp):,}** con persistencia. "
                    f"Falsas alertas: **{100*row_hgb.false_alert_rate:.2f}%** frente a "
                    f"**{100*row_ref.false_alert_rate:.2f}%**.")
        st.warning("Las alertas son una ayuda preventiva. No demuestran detección de fallas verificadas.")
        downloadable(a,"alertas.csv","dl_al")
with tabs[5]:
    st.subheader("Identificación de anomalías")
    if exists("top_anomalies.csv"):
        d=csv("top_anomalies.csv")
        st.metric("Anomalías reportadas en toda la serie", f'{summary()["anomaly_flags"]:,}' if exists("analysis_summary.json") else "No disponible")
        st.caption("Esta tabla contiene las 1 000 observaciones con puntuación más alta. "
                   "Anomalía estadística no significa automáticamente falla real.")
        st.dataframe(d.head(200),hide_index=True,use_container_width=True)
        downloadable(d,"anomalias.csv","dl_an")
with tabs[6]:
    st.subheader("OE4 · Explicabilidad")
    if exists("classification_feature_importance.csv"):
        d=csv("classification_feature_importance.csv")
        st.bar_chart(d.nlargest(12,"importance_mean").set_index("feature")[["importance_mean"]],horizontal=True)
        st.dataframe(d.head(20),hide_index=True,use_container_width=True)
        st.caption("Importancia por permutación: menor F1 al alterar un indicador. "
                   "Es dependencia predictiva, no causalidad física.")
        downloadable(d,"importancia.csv","dl_imp")
with tabs[7]:
    st.subheader("Reproducción completa")
    st.markdown("Código científico: versión fija 1.0.0. Semilla 42, "
                "separación temporal 70/15/15 y bootstrap de 1 000 réplicas "
                "por bloques de 60 minutos.")
    if ZIP.exists():
        with st.spinner("Comprobando integridad de datos originales"):
            checksum=hashlib.sha256(ZIP.read_bytes()).hexdigest()
        if checksum==SHA: st.success("Integridad SHA-256 verificada.")
        else: st.error("El SHA-256 NO coincide con la fuente publicada.")
    st.code("pip install -r requirements.txt\n"
            "pip install -r dashboard/requirements-dashboard.txt\n"
            "python scripts/run_all.py\n"
            "streamlit run dashboard/app.py",language="bash")
    if st.button("Volver a ejecutar análisis original (puede tomar tiempo)",type="primary"):
        with st.status("Procesando fuente original, modelos y verificaciones",expanded=True) as status:
            try:
                r=subprocess.run([sys.executable,str(ROOT/"scripts"/"run_all.py")],
                                 cwd=ROOT,capture_output=True,text=True,timeout=3600)
                st.code((r.stdout+"\n"+r.stderr)[-14000:],language="text")
                if r.returncode==0:
                    st.cache_data.clear()
                    status.update(label="Flujo ejecutado y comprobado",state="complete")
                else: status.update(label="Error: revisar registro",state="error")
            except subprocess.TimeoutExpired:
                status.update(label="Tiempo máximo superado; revisar entorno",state="error")
    if st.button("Comparar resultados recalculados con la versión publicada"):
        audit=ROOT/"scripts"/"auditar_reproduccion.py"
        if audit.exists() and exists("analysis_summary.json"):
            result=subprocess.run([sys.executable,str(audit)],cwd=ROOT,
                                  capture_output=True,text=True)
            st.code((result.stdout+"\n"+result.stderr)[-12000:],language="json")
            if result.returncode:
                st.error("Existen diferencias con la versión científica publicada. Documentarlas antes de afirmar reproducibilidad exacta.")
            else:
                st.success("Las métricas principales auditadas coinciden con la referencia.")
        else:
            st.warning("Faltan resultados o el script de auditoría.")

    st.caption("La reproducción independiente exige guardar log de ejecución, "
               "versiones del entorno y comparaciones con tablas publicadas.")
st.divider()
st.caption("Extensión de sustentación del sistema científico; no telemetría ni pronósticos en vivo.")
