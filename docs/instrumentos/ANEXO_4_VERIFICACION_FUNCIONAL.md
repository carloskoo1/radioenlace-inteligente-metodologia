# Anexo 4. Ficha de verificación funcional del sistema

La tabla A4.1 documenta el criterio funcional para cada módulo. La verificación funcional no equivale a validación de fallas reales.

| Módulo | Entrada | Proceso verificado | Salida esperada | Criterio de cumplimiento |
| --- | --- | --- | --- | --- |
| Preparación | Archivos de telemetría | Integración, depuración y malla temporal | Conjunto maestro y reporte de calidad | Salida generada y trazable |
| Clasificación | Características temporales | Entrenamiento y predicción a 15 min | Estados, probabilidades y métricas | Resultados reproducibles en prueba |
| Anomalías | Filas multivariables completas | Ajuste de Isolation Forest | Puntuación y marca de anomalía | Modelo ajustado solo con entrenamiento |
| Pronóstico | Rezagos y ventanas | Persistencia, Ridge y HGB | Predicciones a 5, 15 y 30 min | Mismos periodos para todos los modelos |
| Evaluación | Predicciones y valores observados | Métricas y bootstrap por bloques | MAE, RMSE, MAPE, F1 e intervalos | 1 000 réplicas y bloques de 60 min |
| Explicabilidad | Clasificador y prueba | Importancia por permutación | Jerarquía de características | Disminución del F1-macro registrada |

Referencia de la ejecución: `scripts/run_all.py`, `scripts/verify_outputs.py`, `src/radioenlace/`.
