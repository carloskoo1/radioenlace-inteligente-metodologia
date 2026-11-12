# Auditoría final de Ubelser: separación temporal y robustez estadística (12-11-2026)

**Versión científica auditada:** `v1.0.0` (código y datos de referencia preservados).  
**Entorno:** GitHub Actions, Ubuntu, Python 3.12, versiones de dependencias del repositorio.  
**Propósito:** probar dos observaciones abiertas en la revisión V21 de la tesis, sin modificar el release científico ni presentar una nueva campaña.

## Evidencia ejecutada (dos flujos)

1. [Auditoría de sensibilidad con bloque en minutos reales y bloques de observaciones](https://github.com/carloskoo1/radioenlace-inteligente-metodologia/actions/runs/43303423639), **finalizada satisfactoriamente**. Contiene los logs y el artefacto ZIP de resultados.
2. [Auditoría adicional con purga y bloques de 30, 60 y 120 observaciones](https://github.com/carloskoo1/radioenlace-inteligente-metodologia/actions/runs/43304829640), **finalizada satisfactoriamente**, con código auditable en [scripts/auditoria_final_purga_y_bloques.py](../../scripts/auditoria_final_purga_y_bloques.py).

La primera auditoría reentrenó el clasificador HistGradientBoosting, reconstruyó los resultados de referencia sin diferencia numérica de F1-macro y auditó el efecto de eliminar etiquetas futuras que cruzaban la frontera entrenamiento–validación. La segunda corroboró el conteo de purga y sometió el mismo contraste a otros tamaños de bloque.

## Resultado 1. Purga temporal

| Indicador | Original | Entrenamiento purgado |
|---|---:|---:|
| Registros utilizados para entrenar clasificación | 82 373 | 82 358 |
| Observaciones de prueba | 17 754 | 17 754 |
| F1-macro | 0,5747978 | 0,5773422 |
| AUC multiclase | 0,7940374 | 0,8008972 |
| Alertas verdaderas positivas (TP) | 723 | 754 |
| Falsas alertas (FP) | 1 742 | 1 686 |

**Se retiraron 15 casos del entrenamiento** cuyo objetivo a 15 minutos correspondía al tramo cronológico siguiente. La purga cambió 959 predicciones del modelo. La evidencia no equivale a 959 averías reales: las clases son etiquetas *proxy*. El conjunto de prueba es el mismo; no es un nuevo conjunto de validación independiente.

La segunda auditoría también cuantificó observaciones atravesando los límites para pronósticos de 5, 15 y 30 minutos: 5, 15 y 30 por frontera, respectivamente. No se identificó un límite interior adicional dentro del segmento final de prueba.

## Resultado 2. Sensibilidad de la diferencia F1-macro

Ganancia de F1-macro del clasificador original sobre persistencia: **0,0281276**.

| Bloques | IC 95 % de la diferencia, clasificador original | ¿Incluye cero? |
|---|---|---|
| 15 observaciones | [0,00863; 0,04608] | No |
| 60 observaciones | [-0,01767; 0,04386] | Sí |
| 180 observaciones | [-0,03109; 0,04381] | Sí |
| 60 minutos de calendario | [-0,01933; 0,04618] | Sí |

Primera auditoría: 500 réplicas por condición. En la segunda auditoría, bloques de 30 observaciones produjeron un IC positivo, pero los de **60 y 120 observaciones** también incluyeron cero, tanto en el clasificador original como en el purgado. La conclusión robusta es que **no se demuestra superioridad general concluyente del clasificador** frente a persistencia para todos los supuestos de dependencia temporal evaluados.

Los tamaños de bloque del código publicado representan cantidades de observaciones filtradas, **no automáticamente minutos transcurridos**. En la segunda auditoría hubo 104 saltos temporales mayores a un minuto dentro de la secuencia de prueba y un salto máximo de 107 minutos.

## Resultado 3. Pronóstico Ridge

En el subconjunto pareado de **17 632 observaciones elegibles** del análisis de sensibilidad a 15 minutos, Ridge mantuvo una reducción media del MAE de aproximadamente **0,4033 unidades de código MCS** frente a persistencia, con intervalos positivos bajo bloques de 15, 60, 180 observaciones y 60 minutos reales. La segunda auditoría también obtuvo intervalos positivos para MAE de MCS y tasa DL en los horizontes de 5, 15 y 30 minutos bajo bloques de 30, 60 y 120 observaciones. En RSSI DL no hubo superioridad consistente de Ridge en MAE.

**No sustituir** con estas cifras las tablas publicadas de pronóstico: los subconjuntos y criterios de emparejamiento de las pruebas de sensibilidad pueden diferir de los usados en todos los reportes principales.

## Dictamen académico y alcance

La purga temporal y la sensibilidad del bootstrap **ya fueron ejecutadas**, no están pendientes. Ambas pruebas apoyan el cierre del riesgo específico de frontera temporal y delimitan la incertidumbre estadística sin cambiar la conclusión general de la tesis: **respaldo parcial**.

Persisten límites legítimos: un solo radioenlace, ausencia de una bitácora exhaustiva de incidentes físicos, estados *proxy*, diferencia entre tasa negociada y throughput, ausencia de calibración metrológica independiente y diferencias numéricas de HistGradientBoosting en Windows. La reproducción verificada corresponde al entorno Linux indicado. No declarar validez externa, causalidad o superioridad universal.

**Documento académico actualizado:** V22 de la tesis, con Anexo 8 y dictamen de tres perspectivas (telecomunicaciones, metodología y estadística). Este documento de GitHub expone evidencia pública de los experimentos; no sustituye el texto formal ni una aprobación del jurado.

