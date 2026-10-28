# Sistema inteligente para el radioenlace Cuñacales–San José

Repositorio metodológico y reproducible de la investigación sobre diagnóstico y pronóstico operacional mediante analítica de datos temporales.

## Qué reproduce

- depuración e integración de 173 513 registros AP;
- conjunto maestro de 118 458 minutos observados;
- etiquetas operacionales proxy construidas solo con entrenamiento;
- clasificación anticipada a 15 minutos;
- detección de anomalías con Isolation Forest;
- pronóstico de RSSI DL, MCS DL y tasa DL a 5, 15 y 30 minutos;
- comparación con persistencia mediante MAE, RMSE, MAPE y bootstrap por bloques;
- F1-macro, AUC, matriz de confusión, alertas e importancia por permutación;
- tablas y figuras utilizadas en el capítulo de resultados.

## Estructura

```text
config/                 parámetros declarativos del análisis
data/raw/               fuente original inmutable y verificada
data/auxiliary/         conjunto radio–clima complementario
docs/metodologia/       protocolo, capítulo III y diccionario
docs/instrumentos/      fichas metodológicas
src/radioenlace/        implementación del análisis
scripts/                ejecución ordenada y verificación
results/tables/         salidas tabulares y manifiestos
results/figures/        figuras reproducibles
tests/                  comprobaciones automáticas
```

## Reproducción completa

Se recomienda Python 3.12.

```bash
git clone https://github.com/carloskoo1/radioenlace-inteligente-metodologia.git
cd radioenlace-inteligente-metodologia
python -m venv .venv
```

En Linux/macOS:

```bash
source .venv/bin/activate
pip install -r requirements.txt
python scripts/run_all.py
```

En Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python scripts\run_all.py
```

La ejecución finaliza únicamente cuando `verify_outputs.py` confirma los conteos, modelos, horizontes y métricas principales.

Para ejecutar las pruebas automatizadas de desarrollo:

```bash
pip install -r requirements-dev.txt
pytest -q
```

## Decisiones que deben conservarse

1. No mezclar los agregados redundantes con la fuente AP principal.
2. No utilizar división aleatoria ni K-Fold convencional sobre las series temporales.
3. Calcular umbrales y transformaciones únicamente con entrenamiento.
4. No denominar throughput a `rate_dl_mbps`.
5. Presentar los estados como etiquetas proxy hasta disponer de bitácoras de incidencias.
6. Mantener la semilla aleatoria 42 y el bootstrap por bloques de 60 minutos.

## Resultados de referencia

- F1-macro de HistGradientBoosting: aproximadamente 0,575.
- AUC OVR macro: aproximadamente 0,794.
- Anomalías identificadas: 1093 observaciones completas.
- Las mejoras predictivas fueron claras para MCS y tasa DL, pero no uniformes para RSSI.

## Limitaciones

La base no incluye una bitácora completa de fallas o cambios de configuración. Las etiquetas son proxy y las asociaciones radio–clima son contemporáneas, exploratorias y no causales. La tasa DL corresponde al indicador negociado por el radio.

## Seguridad

No incluya `.cdsapirc`, `.env`, claves, tokens, contraseñas, direcciones públicas ni configuraciones de acceso remoto. Revise cada archivo antes de publicarlo.

## Cita y licencia

La información de citación se encuentra en `CITATION.cff`. El código fuente se distribuye bajo licencia MIT. Los datos, documentos, tablas y figuras se publican bajo Creative Commons Atribución 4.0 Internacional (CC BY 4.0). La reutilización debe reconocer la autoría y citar el repositorio y la tesis asociada.

## Material de sustentación y anexos instrumentales (octubre de 2026)

Se incorporaron [materiales de apoyo a la sustentación](docs/sustentacion/README.md), un [visor HTML de resultados publicados](docs/sustentacion/demostracion_resultados_sustentacion.html) y las transcripciones de las fichas de los anexos 2–6 en [docs/instrumentos/](docs/instrumentos/). Estos materiales documentales son posteriores a la versión científica **v1.0.0**, que permanece fija e inalterada. El visor es didáctico y no ejecuta los modelos ni captura telemetría en tiempo real.

## Dashboard ejecutable de demostración

Se añadió [dashboard/app.py](dashboard/app.py) con [instrucciones de instalación](dashboard/README.md). Utiliza Streamlit para explorar salidas reales del pipeline y ejecutar el análisis nuevamente bajo demanda. Esta interfaz es **posterior al estudio**: no estaba desplegada sobre el radioenlace y no debe confundirse con telemetría en tiempo real. Requiere instalar también el archivo dashboard/requirements-dashboard.txt.
