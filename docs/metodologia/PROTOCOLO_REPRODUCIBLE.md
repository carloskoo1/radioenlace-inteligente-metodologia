# Protocolo metodológico reproducible

## 1. Diseño y unidad de análisis

La investigación fue cuantitativa, aplicada, de nivel predictivo, diseño no experimental longitudinal y método hipotético-deductivo apoyado en ciencia del diseño. La unidad de análisis fue el registro de telemetría del radioenlace Cuñacales–San José asociado con fecha, hora y rol del equipo.

La población accesible estuvo constituida por 173 513 registros AP recuperados entre el 26 de enero y el 31 de mayo de 2026. La muestra analítica se obtuvo mediante utilización censal y filtros técnicos de elegibilidad: 118 458 minutos presentaron al menos una observación válida.

## 2. Preparación

1. Leer los 90 archivos diarios sin modificar sus bytes.
2. Conservar únicamente `role == AP`.
3. Interpretar `ts` como fecha con zona horaria y convertirla a `America/Lima`.
4. Ordenar y eliminar marcas temporales duplicadas, conservando la última observación.
5. Convertir RSSI, SNR, MCS y tasa DL a valores numéricos.
6. Tratar RSSI >= 0 dBm y SNR <= 0 dB como centinelas inválidos.
7. Consolidar por minuto mediante la mediana.
8. Conservar los vacíos largos; aplicar arrastre causal de un minuto únicamente a predictores.

La tasa DL es la tasa física o negociada reportada por el radio, no throughput efectivo de usuario.

## 3. Separación cronológica

Los minutos observados se ordenaron y dividieron 70 % para entrenamiento, 15 % para validación y 15 % para prueba. Los cortes obtenidos fueron 6 de mayo de 2026 a las 03:01 y 18 de mayo de 2026 a las 12:42, hora de Lima. Ningún registro posterior fue utilizado para construir características, umbrales o imputaciones de un periodo anterior.

## 4. Características

Para cada indicador se utilizaron el valor actual; retardos de 1, 5, 15, 30 y 60 minutos; medias y desviaciones móviles de 5, 15 y 60 minutos; y codificación cíclica de hora y día de la semana. Las ventanas móviles se desplazaron un periodo antes de calcularse para evitar fuga futura.

## 5. Estados proxy

Los umbrales se calcularon solo con entrenamiento. Un minuto fue crítico cuando al menos dos indicadores fueron menores o iguales al percentil 5, o cuando la tasa DL o el SNR DL fueron menores o iguales al percentil 1. Fue degradado cuando al menos un indicador fue menor o igual al percentil 10 sin cumplir la condición crítica. El resto fue normal. Se exigieron al menos tres indicadores disponibles.

Estas etiquetas son referencias operacionales derivadas y no sustituyen una bitácora de fallas validada en campo.

## 6. Modelos y evaluación

- Pronóstico de RSSI DL, MCS DL y tasa DL a 5, 15 y 30 minutos: persistencia, Ridge e HistGradientBoosting.
- Diagnóstico anticipado a 15 minutos: persistencia e HistGradientBoostingClassifier.
- Anomalías: Isolation Forest entrenado únicamente con el tramo de entrenamiento y contaminación de 1 %.
- Pronóstico: MAE, RMSE y MAPE; exactitud redondeada adicional para MCS.
- Clasificación: exactitud, precisión, recall, F1-macro, F1 ponderado y AUC OVR macro.
- Anticipación: precisión, recall y tasa de falsas alertas.
- Inferencia comparativa: bootstrap pareado por bloques móviles de 60 minutos, 1000 remuestreos e IC 95 %.
- Explicabilidad: importancia por permutación sobre una muestra temporalmente distribuida del conjunto de prueba.

## 7. Alcance de las conclusiones

Los resultados permiten evaluar desempeño fuera de muestra respecto de referentes reproducibles. No permiten afirmar causalidad física, throughput efectivo ni validación clínica/operacional de las etiquetas. HE1 y HE2 se respaldaron preliminarmente; HE3 y HE4 se respaldaron parcialmente porque las mejoras no fueron uniformes.
