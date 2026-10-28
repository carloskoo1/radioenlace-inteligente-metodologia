# Dashboard ejecutable del radioenlace Cuñacales–San José

**Extensión de interfaz creada para demostrar el producto científico**, posterior a la versión sellada v1.0.0. Explora datos y salidas calculadas, permite filtrar predicciones históricas y puede ejecutar nuevamente el pipeline original.

No captura RF en tiempo real, no envía alarmas a la red y no realiza inferencia interactiva sobre equipos operativos. Los estados son **etiquetas proxy**, no incidencias confirmadas.

**Para investigadores que quieran instalarlo en otra computadora:** [Guía completa paso a paso (Windows, Linux/macOS, verificación HTTP, solución de fallos y auditoría de reproducibilidad)](../docs/GUIA_INSTALACION_DASHBOARD_Y_REPRODUCIBILIDAD.md). El dashboard puede abrirse con las tablas publicadas sin necesidad de recalcular los modelos; una reproducción científica completa se ejecuta por separado.

## Ejecución local

Se recomienda Python 3.12, usando un entorno virtual:

    git clone https://github.com/carloskoo1/radioenlace-inteligente-metodologia.git
    cd radioenlace-inteligente-metodologia
    python -m venv .venv
    # Active .venv según su sistema operativo
    pip install -r requirements.txt
    pip install -r dashboard/requirements-dashboard.txt
    python scripts/run_all.py
    streamlit run dashboard/app.py

Abra en un navegador la dirección local indicada por Streamlit (usualmente http://localhost:8501).

## Navegación

- Producto: cadena funcional e indicadores generales.
- Calidad de datos: distingue cobertura temporal de completitud.
- Diagnóstico: matriz de confusión, F1 y AUC, intervalos de confianza.
- Pronóstico: compara persistencia, Ridge y HGB por objetivo y horizonte; si el pipeline ha corrido, muestra mediciones y predicciones individuales.
- Alertas: sensibilidad y falsas alarmas.
- Anomalías y explicabilidad: ordenamiento de casos e importancia por permutación.
- Reproducibilidad: integridad SHA-256 de datos y ejecución nuevamente del flujo.

## Origen y límites

La [auditoría independiente en Linux/Python 3.12](../docs/reproducibilidad/AUDITORIA_LINUX_EXITOSA_2026-10-28.md) ha reproducido las métricas principales, mientras que Windows nativo arroja algunas diferencias de HGB. Para reproducir exactamente los resultados científicos recomendamos Linux, no Windows nativo.

El análisis original y sus resultados están documentados en la [versión científica v1.0.0](https://github.com/carloskoo1/radioenlace-inteligente-metodologia/releases/tag/v1.0.0). La interfaz se añadió en main como herramienta adicional. Las métricas no son garantía de generalización a nuevos radioenlaces ni evidencia de fallas reales verificadas.

Para defensa, distinga entre: (1) producto computacional evaluado en la tesis; (2) dashboard añadido posteriormente; (3) validación de desempeño fuera de muestra; y (4) reproducción independiente desde los archivos originales.


## Telemetría actual (extensión de solo lectura, octubre de 2026)

La aplicación incorpora una **novena pestaña: «Telemetría actual»**, distinta de los resultados históricos de la tesis. La fuente original ePMP de la tesis no debe confundirse con la adquisición actual de AtmosLink, cuya configuración registra operación en **6 GHz**.

El adaptador [live_source.py](live_source.py) consulta de manera limitada una base SQLite local que contiene la tabla `radio_link_local` (solo registros AP). No inicia consultas a radios, no escribe en SQLite y no interfiere con el proceso de captura. Muestra RSSI DL, SNR DL, MCS DL, tasa DL negociada y hasta 180 registros; refresca la visualización cada 30 segundos y marca como **desactualizada** cualquier fuente cuya última medición supere cinco minutos de antigüedad.

**Para habilitarlo en un equipo Linux donde exista una copia local autorizada de la base:**

~~~bash
export UBELSER_LIVE_DB_PATH="/ruta/local/autorizada/weather_local.db"
.venv/bin/python -m streamlit run dashboard/app.py --server.address 127.0.0.1
~~~

En la instalación observada del Controlador, la base se encuentra en `/home/carlos/Proyectos/EstacionMeteorologica/SQLite/CU01/weather_local.db`; esa ruta **solo existe en ese equipo o donde se monte autorizadamente**, no en el PC Research por el hecho de tener conexión a Internet. Para consultar desde otra computadora, será necesario un mecanismo **privado de transporte autorizado** (por ejemplo, exportación saneada y sincronización segura o túnel SSH), sin exponer SQLite ni la interfaz a Internet.

El dashboard de **Research** mantiene operativas las vistas históricas aunque no tenga acceso a esa fuente. La nueva pestaña mostrará «fuente no configurada» hasta que se establezca el origen autorizado.

**Importante:** las lecturas actuales son reales, pero la extensión todavía **no implementa inferencia predictiva en vivo**. No se deben aplicar sin validación los modelos históricos a una configuración de radio que difiere del conjunto de entrenamiento. Antes de activar predicción real, verificar hardware, banda/frecuencia, unidades, distribución de señales, esquemas MCS, calidad de adquisición y deriva temporal. Las etiquetas del estudio fueron *proxy* y no incidentes confirmados.

Pruebas del adaptador: `python -m unittest discover -s tests -p test_live_source.py -v`. Esas pruebas emplean una base SQLite **sintética y temporal**, nunca la base de producción.


## Alternativa recomendada: datos reales desde los respaldos que ya llegan a Research

**Comprobado el 28 de octubre de 2026.** Research tiene acceso a los respaldos de CU01 a través de Google Drive para escritorio. En esa instalación se detectó la carpeta:

```text
G:/Mi unidad/AtmosLink_Backups_UNC/CU01/field/
```

El ZIP `backup_CU01_20261028_061956.zip` contiene `scientific_campaign_6g_integrated.csv` con **16 028 registros** de telemetría 6 GHz hasta las **05:56:51, hora de Perú**. En esa misma fecha había varios ZIP, aproximadamente cada seis horas. La disponibilidad de nuevos respaldos depende de la sincronización externa; el dashboard no los crea.

La pestaña **Telemetría actual** detecta automáticamente esa ruta en Research y lee los **últimos 180 registros válidos** directamente del CSV comprimido. No necesita extraer la base `weather_local.db` (~1,77 GB en el respaldo revisado), ni modificar los ZIP, ni conectarse a Controlador. El gráfico muestra RSSI, SNR, MCS y tasa DL **negociada**. Se comprueba la marca temporal de la última lectura y el nombre del respaldo.

**Importante:** refrescar la página cada cinco minutos **no produce datos nuevos**. Solo detecta ZIP más recientes. Las cifras pueden tener horas de antigüedad y siempre se presentan como **telemetría real de un respaldo, no en tiempo real**.

Si los ZIP están en otra ubicación en Windows, configure la ruta antes de iniciar:

```powershell
$env:UBELSER_BACKUP_DIR = "D:\\Respaldos\\CU01"
.\\.venv\\Scripts\\python.exe -m streamlit run dashboard\\app.py
```

En Linux/macOS: `export UBELSER_BACKUP_DIR="/ruta/autorizada/a/field"`.

La conexión opcional `UBELSER_LIVE_DB_PATH` conserva prioridad cuando se configura explícitamente; en ese caso se consulta una **copia SQLite local autorizada** en modo solo lectura. Sin dicha variable, se usa la fuente de respaldos. No exponga la base ni dispositivos por Internet.

El proceso de respaldo AtmosLink no se modifica. **No se entrenan modelos ni se generan predicciones en vivo con los nuevos datos**, que corresponden a un escenario de radio 6 GHz diferente del conjunto histórico evaluado en la tesis.

Pruebas: `python -m unittest discover -s tests -p test_backup_source.py -v`.
