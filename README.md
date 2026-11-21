# Sistema inteligente para el radioenlace Cuñacales–San José

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23748244.svg)](https://doi.org/10.5281/zenodo.23748244)

**Versión GitHub más reciente: v1.2.0 (18-11-2026), con tesis V27 revisada.** [Abrir el release](https://github.com/carloskoo1/radioenlace-inteligente-metodologia/releases/tag/v1.2.0). **El DOI de Zenodo mostrado en la insignia corresponde exclusivamente a v1.1.1**, depósito histórico del 28-10-2026, no a v1.2.0. [Consultar el depósito histórico](https://zenodo.org/records/23748244). La asignación de DOI nuevo para v1.2.0 sigue pendiente de confirmación.

**Tesis académica revisada más reciente (V27):** [descargar Word público V27](docs/tesis/TESIS_UBELSER_V27_PUBLICA_OPTIMIZADA_20261118.docx). Incluye la auditoría adversarial de trazabilidad entre preguntas, objetivos, variables, instrumentos, resultados, contrastación y conclusiones. La [versión editorial histórica del 28-10-2026](docs/entrega_final/TESIS_UBELSER_TAMAY_FINAL_IEEE_2026-10-28.docx) se conserva para trazabilidad, pero no debe confundirse con V27.

Repositorio metodológico y reproducible de la investigación sobre diagnóstico y pronóstico operacional mediante analítica de datos temporales.

**¿Quiere ejecutar el producto en otra computadora?** Consulte la [guía completa de instalación del dashboard y reproducción científica](docs/GUIA_INSTALACION_DASHBOARD_Y_REPRODUCIBILIDAD.md), con instrucciones para Windows, Linux/macOS, soluciones a errores y auditoría independiente de los resultados.

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

- F1-macro de HistGradientBoosting: aproximadamente 0,566 (V28, sin parada temprana; la V27 informaba 0,575 con parada temprana automática).
- AUC OVR macro: aproximadamente 0,788 (V27: 0,794).
- Anomalías identificadas: 1093 observaciones completas.
- Las mejoras predictivas fueron claras para MCS y tasa DL, pero no uniformes para RSSI.

## Limitaciones

La base no incluye una bitácora completa de fallas o cambios de configuración. Las etiquetas son proxy y las asociaciones radio–clima son contemporáneas, exploratorias y no causales. La tasa DL corresponde al indicador negociado por el radio.

## Seguridad

No incluya `.cdsapirc`, `.env`, claves, tokens, contraseñas, direcciones públicas ni configuraciones de acceso remoto. Revise cada archivo antes de publicarlo.

## Cita y licencia

La información de citación se encuentra en [`CITATION.cff`](CITATION.cff). **DOI de la versión v1.1.1:** [10.5281/zenodo.23748244](https://doi.org/10.5281/zenodo.23748244). **DOI general del software:** [10.5281/zenodo.23748243](https://doi.org/10.5281/zenodo.23748243). El código fuente se distribuye bajo licencia MIT. Los datos, documentos, tablas y figuras se publican bajo Creative Commons Atribución 4.0 Internacional (CC BY 4.0). La reutilización debe reconocer la autoría y citar el repositorio y la tesis asociada.

## Material de sustentación y anexos instrumentales (octubre de 2026)

Se incorporaron [materiales de apoyo a la sustentación](docs/sustentacion/README.md), un [visor HTML de resultados publicados](docs/sustentacion/demostracion_resultados_sustentacion.html) y las transcripciones de las fichas de los anexos 2–6 en [docs/instrumentos/](docs/instrumentos/). Estos materiales documentales son posteriores a la versión científica **v1.0.0**, que permanece fija e inalterada. El visor es didáctico y no ejecuta los modelos ni captura telemetría en tiempo real.

## Dashboard ejecutable de demostración

Se añadió [dashboard/app.py](dashboard/app.py) con [instrucciones de instalación](dashboard/README.md), incluida una **novena pestaña de telemetría actual** (solo lectura; requiere fuente local autorizada). Utiliza Streamlit para explorar salidas reales del pipeline y ejecutar el análisis nuevamente bajo demanda. Esta interfaz es **posterior al estudio**: no estaba desplegada sobre el radioenlace y no debe confundirse con telemetría en tiempo real. Requiere instalar también el archivo dashboard/requirements-dashboard.txt.

### Producto, auditoría y archivos de trabajo

- [Definición del producto tecnológico y su relación con cada objetivo](docs/PRODUCTO_TECNOLOGICO.md).
- [Auditoría independiente realizada en Windows y sus discrepancias documentadas](docs/reproducibilidad/AUDITORIA_WINDOWS_PY313_2026-10-28.md).
- [Guía para auditar reproducciones](docs/reproducibilidad/GUIA_AUDITORIA.md).
- [Acción manual de reproducción en Linux y Python 3.12](.github/workflows/reproduccion_cientifica.yml), que permite generar un nuevo registro verificable sin modificar el release científico.
- [Copias de Word y PowerPoint disponibles como documentos de origen](docs/material_original/); **no son las revisiones finales de sustentación**.

**Actualización de reproducibilidad (28-10-2026):** una [ejecución independiente en Linux/Python 3.12](docs/reproducibilidad/AUDITORIA_LINUX_EXITOSA_2026-10-28.md) completó el flujo completo y reprodujo las cifras originales de F1-macro, AUC y alertas. La ejecución nativa en Windows continúa mostrando diferencias de HistGradientBoosting; por ello, **Linux/Python 3.12 es el entorno verificado**. Se conserva [la auditoría de Windows](docs/reproducibilidad/AUDITORIA_WINDOWS_PY313_2026-10-28.md) para trazabilidad.


## Cierre documental y preservación Zenodo

- [**Tesis final de Ubelser con formato IEEE (Word, 28-10-2026)**](docs/entrega_final/TESIS_UBELSER_TAMAY_FINAL_IEEE_2026-10-28.docx), con dedicatoria a sus padres y agradecimiento al Dr. Carlos Jesús Koo Labrín. La [copia de cierre documental anterior](docs/material_original/TESIS_UBELSER_TAMAY_CIERRE_DOCUMENTAL_2026-10-28.docx) se conserva para trazabilidad.
- [**Dictamen técnico-académico de cierre (Word)**](docs/material_original/DICTAMEN_TECNICO_ACADEMICO_UBELSER_2026-10-28.docx) y [versión consultable en Markdown](docs/DICTAMEN_CIERRE_CIENTIFICO_UBELSER_2026-10-28.md): favorable al cierre científico con controles editoriales finales.
- [**Depósito, DOI y citación verificados en Zenodo**](docs/ZENODO_GITHUB_CITACION.md): registro público de v1.1.1, ambos ORCID comprobados, integridad del ZIP y procedimiento para futuras versiones. **DOI: [10.5281/zenodo.23748244](https://doi.org/10.5281/zenodo.23748244)**.

La presentación que figura en `docs/material_original/` se identifica expresamente como **BASE**, no como la última presentación de defensa. El release científico `v1.0.0` no se modifica.


### Auditoría adversarial final — noviembre de 2026

Las dos pruebas computacionales pendientes de la tesis (purga de etiquetas que cruzan fronteras temporales y sensibilidad del bootstrap a la definición y longitud de los bloques) **se ejecutaron satisfactoriamente** el 12 de noviembre de 2026. Se conservaron el código y los datos científicos `v1.0.0` sin alteraciones. [Consultar resultados, límites inferenciales y enlaces a las dos ejecuciones reproducibles](docs/reproducibilidad/AUDITORIA_FINAL_PURGA_BLOQUES_2026-11-12.md). El F1-macro del clasificador no acredita superioridad robusta bajo todos los bloques evaluados; la hipótesis general mantiene respaldo parcial.


### Revisión académica V27 — 18 de noviembre de 2026

La auditoría adversarial de la **tesis V26C → V27** documentó la alineación explícita entre preguntas P1–P4, objetivos OE1–OE4, hipótesis HE1–HE4, operacionalización, técnicas, instrumentos, resultados y conclusiones; corrigió la numeración de tres citas de Medina Romero ([35]), amplió la matriz de consistencia, reescribió Resumen/Abstract y verificó la sección **4.7 de contrastación**. Las métricas históricas no se alteraron.

- [**Informe científico y matriz de trazabilidad V27**](docs/tesis/AUDITORIA_ADVERSARIAL_V27_2026-11-18.md).
- **Tesis V27 ya publicada en GitHub:** [copia pública optimizada](docs/tesis/TESIS_UBELSER_V27_PUBLICA_OPTIMIZADA_20261118.docx), sin imágenes de firmas, SHA-256 `04c1f4b4b220e5653dc363fdea5014783c6d74ddc06fa6b39b96fe94053fa959`. El ejemplar íntegro con firmas se conserva en el expediente reservado; su SHA-256 es `38f16f9c036deae734fa1d7991f7ee2ad4e5de087e8463b73bfe78018054d70a`.
- **Zenodo `v1.1.1`**: DOI histórico [10.5281/zenodo.23748244](https://doi.org/10.5281/zenodo.23748244), **sin cambios**. Se emitirá un DOI de una nueva versión únicamente después de subir y verificar la nueva tesis.

La V27 conserva las valoraciones auténticas de los tres especialistas, con observaciones. La publicación de facsímiles con firmas requiere autorización de divulgación apropiada o una copia pública que las oculte.


### Estado de preservación v1.2.0 (18-11-2026)

- **Release GitHub confirmada:** [v1.2.0 — Tesis V27 revisada](https://github.com/carloskoo1/radioenlace-inteligente-metodologia/releases/tag/v1.2.0), con archivo público [Word V27](https://github.com/carloskoo1/radioenlace-inteligente-metodologia/blob/v1.2.0/docs/tesis/TESIS_UBELSER_V27_PUBLICA_OPTIMIZADA_20261118.docx).
- **Verificación automática:** [GitHub Actions 44455235286](https://github.com/carloskoo1/radioenlace-inteligente-metodologia/actions/runs/44455235286) — archivo íntegro y `CITATION.cff` válidos; release creada correctamente.
- **Zenodo:** el sondeo automatizado no encontró un DOI nuevo para `v1.2.0` durante la ejecución. **No atribuir el DOI de `v1.1.1` a esta versión.** Verificar en [Zenodo → GitHub](https://zenodo.org/account/settings/github/) el estado de ingesta, errores y DOI antes de citar `v1.2.0` como depositada.
