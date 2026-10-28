# Anexo 6. Matriz de explicabilidad

Transcripción de la tabla A6.2. La importancia por permutación cuantifica dependencia predictiva; **no** establece causalidad física.

| Característica | Procedimiento | Indicador | Interpretación |
| --- | --- | --- | --- |
| SNR DL actual | Permutación en el conjunto de prueba | Disminución media del F1-macro | Mayor valor: mayor dependencia predictiva |
| Variabilidad de tasa DL | Permutación en el conjunto de prueba | Media y variabilidad entre repeticiones | Dinámica reciente relevante para el diagnóstico |
| RSSI DL y características de MCS/tasa | Permutación en el conjunto de prueba | Importancia global | Dependencia predictiva, no causalidad física |

Resultados cuantitativos en `results/tables/classification_feature_importance.csv`.
