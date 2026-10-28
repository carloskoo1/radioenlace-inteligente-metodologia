# Auditoría independiente — Windows, Python 3.13 (28-10-2026)

> **Actualización 28-10-2026:** el análisis completo **sí se reprodujo en Ubuntu/Python 3.12** mediante una [auditoría independiente de GitHub Actions](AUDITORIA_LINUX_EXITOSA_2026-10-28.md), con F1-macro 0,574798, AUC 0,794037, 723 alertas correctas y 1 742 falsas alertas. Las diferencias descritas abajo quedan delimitadas a las ejecuciones Windows probadas. El mecanismo técnico exacto de la variación entre plataformas aún no está identificado; no se debe afirmar que los datos científicos originales son irreproducibles.

## Procedimiento

Se clonó una copia limpia de la etiqueta científica **v1.0.0**, commit `8f175ffef568c25cbaee91a1c04da3f2cc38cdb2`, en un directorio aislado. Se instaló `requirements.txt` con Python 3.13 y se ejecutó `python scripts/run_all.py` sin modificar los archivos fuente. La verificación SHA-256 de `Datos.zip` fue satisfactoria y se procesaron los 90 archivos originales.

El flujo completó preparación, modelado central, bootstrap, explicabilidad y generación de figuras. **La ejecución terminó con código 1 al fallar el verificador final `scripts/verify_outputs.py`**, debido a una diferencia en F1-macro.

## Comparación numérica

| Indicador | Referencia v1.0.0 | Reejecución Python 3.13 Windows | Coincidencia |
|---|---:|---:|---|
| Archivos originales | 90 | 90 | Sí |
| Registros AP | 173 513 | 173 513 | Sí |
| Minutos observados | 118 458 | 118 458 | Sí |
| Observaciones anómalas | 1 093 | 1 093 | Sí |
| F1-macro HGB | 0,5747978 | 0,5787394 | No |
| AUC multiclase HGB | 0,7940374 | 0,7967051 | No |
| Alertas verdaderas positivas | 723 | 644 | No |
| Alertas falsas positivas | 1 742 | 1 327 | No |
| Alertas falsas negativas | 825 | 904 | No |
| Alertas verdaderas negativas | 14 464 | 14 879 | No |
| MAE Ridge MCS DL 15 min | 0,86944645 | 0,86944645 | Sí |
| MAE Ridge tasa DL 15 min | 18,98490543 | 18,98490543 | Sí |
| MAE persistencia RSSI DL 15 min | 0,49878771 | 0,49878771 | Sí |

Los resultados indicados como coincidentes superaron los controles de la auditoría. Las cifras de clasificación y anticipación **no se consideran reproducidas exactamente** con este entorno. Las desviaciones no deben eliminarse ajustando la tolerancia sin justificación científica.

## Interpretación provisional

La integridad de datos y determinados resultados de pronóstico sí se reproducen, pero el clasificador y las alertas difieren. **No se ha determinado todavía la causa.** Puede estar relacionada con diferencias de plataforma, condiciones de ejecución, ordenamiento, paralelismo o sensibilidad del modelo. Esto es una hipótesis de investigación metodológica, no un hecho demostrado.

Esta auditoría **no invalida automáticamente** todos los resultados de la tesis, pero impide afirmar en su estado actual que toda la ejecución presenta equivalencia numérica entre entornos.

## Acciones para cerrar la observación

1. Repetir el núcleo en Python 3.12, que es la versión recomendada en el README científico.
2. Comparar huellas de la matriz de características, particiones temporales, cuantiles y etiquetas antes de entrenar.
3. Comprobar la sensibilidad a hilos/número de trabajadores y la determinación de HistGradientBoosting.
4. Documentar el criterio aceptable de equivalencia: conteos, pronósticos, clasificación y alertas por separado, sin ocultar resultados discordantes.
5. Conservar la referencia v1.0.0 inmutable; cualquier corrección metodológica posterior debe publicarse con nueva versión, números y trazabilidad.

*Este documento se refiere exclusivamente a la auditoría ejecutada sobre Windows/Python 3.13, no equivale a un resultado de Linux ni del entorno Python 3.12.*

## Segunda comprobación — Python 3.12 en Windows

Se preparó otro entorno virtual limpio con **Python 3.12** y las mismas versiones declaradas en `requirements.txt`. Se clonó otra copia limpia de la etiqueta `v1.0.0`, se verificó nuevamente el SHA-256 del archivo fuente y se ejecutaron las etapas `00_prepare_data.py` y `01_run_core.py` (núcleo científico).

El núcleo terminó con **código 0**, pero volvió a obtener: F1-macro HGB **0,578739**, AUC **0,796705**, **644** verdaderos positivos de alerta y **1 327** falsos positivos. Estos resultados coincidieron con los obtenidos en Windows/Python 3.13 y no con los valores publicados v1.0.0. **El cambio de Python 3.13 a 3.12 no eliminó la diferencia.** No se ejecutó el análisis extendido completo en este segundo entorno durante esta comprobación; por ello, no corresponde afirmar una segunda reproducción integral.

La causa permanece sin determinar. No debe atribuirse automáticamente a la versión de Python. Se recomienda inspeccionar determinismo de HistGradientBoosting, paralelismo, datos intermedios y procedencia exacta de las tablas selladas, antes de generar una versión corregida.

## Tercera comprobación — Python 3.12 y un hilo de cálculo

Se volvió a ejecutar `01_run_core.py` con Python 3.12 y las variables de entorno `OMP_NUM_THREADS=1`, `OPENBLAS_NUM_THREADS=1` y `MKL_NUM_THREADS=1`. Terminó con código 0 y **repitió exactamente las cifras del segundo ensayo**: F1-macro HGB 0,578739, AUC 0,796705, 644 verdaderos positivos y 1 327 falsos positivos. Limitar el número de hilos mediante estas variables **tampoco restauró las cifras publicadas** en Windows. No se ha contrastado aún contra una ejecución limpia Linux del mismo release.
