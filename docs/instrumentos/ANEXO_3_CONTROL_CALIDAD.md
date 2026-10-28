# Anexo 3. Ficha de control de calidad de datos

Matriz aplicada en la tesis (tabla A3.1). Los resultados se basan en la fuente AP y la malla de un minuto.

| Criterio | Indicador | Resultado | Evidencia o regla aplicada |
| --- | --- | --- | --- |
| Trazabilidad | Archivos diarios revisados | 90 | Conservación de las fuentes originales |
| Unicidad | Duplicados temporales eliminados | 10 | Se conservó la última observación del mismo instante |
| Cobertura | Minutos observados / malla total | 118 458 / 180 025 = 65,80 % | Las brechas extensas se conservaron como ausencias |
| Completitud | Filas multivariables completas / minutos observados | 117 911 / 118 458 = 99,54 % | Evaluación sobre los minutos con alguna observación |
| Validez | Lecturas centinela tratadas | 776 | RSSI ≥ 0 dBm y SNR ≤ 0 dB se reemplazaron por ausentes |
| Consistencia temporal | Zona horaria y orden | Conforme | America/Lima; orden cronológico ascendente |
| Imputación causal | Arrastre máximo | 1 minuto | Solo para predictores; los objetivos futuros no se interpolaron |

**Aclaración metodológica:** cobertura temporal (65,80 %) y completitud entre minutos observados (99,54 %) tienen denominadores distintos. La última no implica adquisición continua.
