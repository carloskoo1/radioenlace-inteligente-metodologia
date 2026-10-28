# Anexo 5. Matriz de evaluación diagnóstica y predictiva

Tabla A5.1 de la tesis. Las métricas se calculan sobre observaciones cronológicamente posteriores al entrenamiento.

| Tarea | Modelo o referente | Indicadores | Comparación | Criterio de interpretación |
| --- | --- | --- | --- | --- |
| Clasificación a 15 min | Persistencia y HGB | F1-macro, precisión macro, recall macro, exactitud y AUC | Diferencia pareada de F1-macro | Mejora concluyente si el IC 95 % favorable no incluye cero |
| Pronóstico RSSI DL | Persistencia, Ridge y HGB | MAE, RMSE y MAPE | Ganancia frente a persistencia | Menor error; IC 95 % mediante bootstrap por bloques |
| Pronóstico MCS DL | Persistencia, Ridge y HGB | MAE, RMSE, MAPE y exactitud redondeada | Ganancia frente a persistencia | Menor error y estabilidad entre horizontes |
| Pronóstico tasa DL | Persistencia, Ridge y HGB | MAE, RMSE y MAPE | Ganancia frente a persistencia | Menor error; valores en Mbps y porcentaje |

**Lectura para jurados:** MAE es el error absoluto promedio; cuanto menor, mejor. RMSE penaliza más los errores grandes. Un intervalo de confianza que incluye cero no sostiene una mejora concluyente bajo el procedimiento aplicado.
