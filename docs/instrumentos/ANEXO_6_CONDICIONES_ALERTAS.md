# Anexo 6. Ficha de condiciones futuras y alertas

Tabla A6.1 de la tesis. La condición futura no normal corresponde a una etiqueta operacional **proxy**, no a una falla de campo confirmada.

| Campo | Definición operacional | Unidad | Resultado de referencia |
| --- | --- | --- | --- |
| Horizonte | Separación entre la alerta y la condición evaluada | min | 15 |
| Condición futura no normal | Estado degradado o crítico en t + 15 | Binaria | 1 548 casos en prueba |
| Condiciones anticipadas | Verdaderos positivos | Casos | 589 |
| Recall de alerta | VP / (VP + FN) | % | 38,05 % |
| Precisión de alerta | VP / (VP + FP) | % | 32,61 % |
| Tasa de falsas alertas | FP / (FP + VN) | % | 7,51 % |
| Condiciones no detectadas | Falsos negativos | Casos | 959 |

Véase `results/tables/anticipation_metrics.csv` para la comparación con persistencia.
