# Cambios V28 frente a V27

Registro de reemplazos aplicados por `make_v28.py` (el docx no usa control de cambios de Word; este registro es la trazabilidad).

## cifras HGB: corrida determinista V28 (early_stopping=False) (×8)
- V27: 0,575
- V28: 0,566

## cifras HGB: corrida determinista V28 (early_stopping=False) (×8)
- V27: 0,794
- V28: 0,788

## cifras HGB: corrida determinista V28 (early_stopping=False) (×2)
- V27: 0.575
- V28: 0.566

## cifras HGB: corrida determinista V28 (early_stopping=False) (×2)
- V27: 0.794
- V28: 0.788

## cifras HGB: corrida determinista V28 (early_stopping=False) (×2)
- V27: de 0,884 a 0,851
- V28: de 0,884 a 0,874

## cifras HGB: corrida determinista V28 (early_stopping=False) (×3)
- V27: 14 464
- V28: 14 989

## cifras HGB: corrida determinista V28 (early_stopping=False) (×1)
- V27: Se clasificaron correctamente 14 989 estados normales, 511 degradados y 140 críticos.
- V28: Se clasificaron correctamente 14 989 estados normales, 387 degradados y 139 críticos.

## cifras HGB: corrida determinista V28 (early_stopping=False) (×8)
- V27: 46,71 %
- V28: 38,05 %

## cifras HGB: corrida determinista V28 (early_stopping=False) (×1)
- V27: 46.71%
- V28: 38.05%

## cifras HGB: corrida determinista V28 (early_stopping=False) (×6)
- V27: 723 de 1 548
- V28: 589 de 1 548

## cifras HGB: corrida determinista V28 (early_stopping=False) (×1)
- V27: 723 of 1,548
- V28: 589 of 1,548

## cifras HGB: corrida determinista V28 (early_stopping=False) (×4)
- V27: 1 742
- V28: 1 217

## cifras HGB: corrida determinista V28 (early_stopping=False) (×1)
- V27: 1,742
- V28: 1,217

## cifras HGB: corrida determinista V28 (early_stopping=False) (×6)
- V27: 10,75 %
- V28: 7,51 %

## cifras HGB: corrida determinista V28 (early_stopping=False) (×4)
- V27: 29,33 %
- V28: 32,61 %

## A18: referencia cruzada errónea (×1)
- V27: se muestran en la Tabla XI.
- V28: se muestran en la Tabla XIV.

## cifras HGB: corrida determinista V28 (early_stopping=False) (×2)
- V27: celdas 723 / 825 (Anexo 6)
- V28: 589 / 959

## Tabla de pronóstico rssi_dl_dbm h=5: HGB determinista (×1)
- V27: 5 | HGB | 0.380 | 0.661 | 0.502 %
- V28: None | None | 0.362 | 0.659 | 0.479 %

## Tabla de pronóstico rssi_dl_dbm h=15: HGB determinista (×1)
- V27: 15 | HGB | 0.546 | 0.806 | 0.722 %
- V28: None | None | 0.575 | 0.820 | 0.761 %

## Tabla de pronóstico rssi_dl_dbm h=30: HGB determinista (×1)
- V27: 30 | HGB | 0.702 | 0.905 | 0.930 %
- V28: None | None | 0.649 | 0.876 | 0.860 %

## Tabla de pronóstico mcs_dl h=5: HGB determinista (×1)
- V27: 5 | HGB | 0.930 | 4.384 | 0.784 % | 0.482
- V28: None | None | 1.021 | 4.413 | 0.871 % | 0.458

## Tabla de pronóstico mcs_dl h=15: HGB determinista (×1)
- V27: 15 | HGB | 0.913 | 4.383 | 0.768 % | 0.507
- V28: None | None | 1.043 | 4.426 | 0.894 % | 0.471

## Tabla de pronóstico mcs_dl h=30: HGB determinista (×1)
- V27: 30 | HGB | 0.986 | 4.413 | 0.838 % | 0.484
- V28: None | None | 1.009 | 4.426 | 0.860 % | 0.476

## Tabla de pronóstico rate_dl_mbps h=5: HGB determinista (×1)
- V27: 5 | HGB | 20.85 | 31.31 | 19.84 %
- V28: None | None | 21.43 | 32.49 | 20.06 %

## Tabla de pronóstico rate_dl_mbps h=15: HGB determinista (×1)
- V27: 15 | HGB | 22.00 | 33.34 | 20.44 %
- V28: None | None | 21.88 | 33.15 | 20.34 %

## Tabla de pronóstico rate_dl_mbps h=30: HGB determinista (×1)
- V27: 30 | HGB | 21.76 | 32.66 | 20.29 %
- V28: None | None | 21.86 | 32.87 | 20.23 %

## Tabla XIV: HGB determinista (×1)
- V27: HGB | 17 754 | 0.851 | 0.566 | 0.869 | 0.638 | 0.571 | 0.788
- V28: HGB | 17 754 | 0.874 | 0.566 | 0.880 | 0.614 | 0.546 | 0.788

## Tabla XIX: HGB determinista (×1)
- V27: HistGradientBoosting | 589 | 1742 | 959 | 14464 | 0.293 | 0.467 | 10.75 %
- V28: HistGradientBoosting | 589 | 1217 | 959 | 14989 | 0.326 | 0.380 | 7.51 %

## Tabla XX fila 1: importancia por permutación determinista (×1)
- V27: SNR DL actual | 0.1782 | 0.0008
- V28: SNR DL actual | 0.1718 | 0.0015

## Tabla XX fila 2: importancia por permutación determinista (×1)
- V27: Desv. tasa DL (60 min) | 0.0169 | 0.0002
- V28: Media MCS UL (60 min) | 0.0103 | 0.0059

## Tabla XX fila 3: importancia por permutación determinista (×1)
- V27: RSSI DL actual | 0.0131 | 0.0006
- V28: Desv. tasa DL (60 min) | 0.0095 | 0.0035

## Tabla XX fila 4: importancia por permutación determinista (×1)
- V27: Media MCS UL (60 min) | 0.0081 | 0.0025
- V28: RSSI DL actual | 0.0087 | 0.0019

## Tabla XX fila 5: importancia por permutación determinista (×1)
- V27: Tasa DL rezago 5 min | 0.0054 | 0.0025
- V28: Tasa DL rezago 5 min | 0.0066 | 0.0011

## Tabla XX fila 6: importancia por permutación determinista (×1)
- V27: Media RSSI DL (15 min) | 0.0038 | 0.0009
- V28: Media SNR UL (60 min) | 0.0050 | 0.0028

## Tabla XX fila 7: importancia por permutación determinista (×1)
- V27: Desv. MCS DL (5 min) | 0.0033 | 0.0018
- V28: Tasa DL rezago 15 min | 0.0047 | 0.0024

## Tabla XX fila 8: importancia por permutación determinista (×1)
- V27: Desv. RSSI DL (60 min) | 0.0032 | 0.0050
- V28: Tasa DL actual | 0.0044 | 0.0012

## Tabla XX fila 9: importancia por permutación determinista (×1)
- V27: Desv. RSSI UL (60 min) | 0.0031 | 0.0019
- V28: Desv. MCS DL (15 min) | 0.0040 | 0.0014

## Tabla XX fila 10: importancia por permutación determinista (×1)
- V27: Desv. MCS DL (15 min) | 0.0027 | 0.0011
- V28: Media RSSI UL (60 min) | 0.0040 | 0.0052

## A4/A13: importancia por permutación recalculada (×1)
- V27: con una importancia media de 0,1782. En un segundo nivel aparecieron la variabilidad de la tasa DL durante 60 minutos, RSSI DL actual, la media de MCS UL durante 60 minutos y el rezago de cinco minutos de la tasa DL.
- V28: con una importancia media de 0,1718. En un segundo nivel aparecieron la media de MCS UL durante 60 minutos, la variabilidad de la tasa DL durante 60 minutos, RSSI DL actual y el rezago de cinco minutos de la tasa DL.

## A4: circularidad etiqueta-predictor declarada (×1)
- V27: respecto de un único valor instantáneo.
- V28: respecto de un único valor instantáneo. Esta lectura debe matizarse: la regla que construye las etiquetas proxy declara crítico todo minuto con SNR DL igual o inferior a su percentil 1 de entrenamiento, y el 84,6 % de los minutos críticos cumple esa condición. Por ello, parte de la importancia del SNR DL refleja la construcción de la etiqueta y no solo una relación independiente con el desempeño del enlace. Además, la importancia se estimó con tres permutaciones sobre 3 000 casos, de modo que el orden de las características de segundo nivel es poco estable (desviaciones comparables a las media

## A2: comparación de alertas a tasa de falsas alertas igualada (×1)
- V27: no un sistema de alerta de fallas de campo validado.
- V28: no un sistema de alerta de fallas de campo validado. Con la configuración determinista, el aumento de recall (2,58 puntos porcentuales; IC del 95 % por bloques de −1,68 a 6,98 puntos) no fue concluyente. Cuando el umbral del modelo se ajustó a la tasa de falsas alertas de persistencia (6,10 %), el recall fue igual al de persistencia (35,47 %). La diferencia observada corresponde, por tanto, a un cambio del punto de operación y no a una mayor capacidad de discriminación demostrada (Tabla A8.5).

## HGB determinista: MCS DL (×1)
- V27: HistGradientBoosting también redujo los errores, aunque quedó ligeramente por debajo de Ridge.
- V28: HistGradientBoosting también redujo el MAE (entre 18,5 % y 22,1 % frente a persistencia), pero con una ganancia claramente menor que la de Ridge.

## A6: líneas base adicionales (×1)
- V27: aunque su mejora de MAE a 15 minutos no fue concluyente al 95 %.
- V28: aunque su mejora de MAE no fue concluyente al 95 % en ninguno de los tres horizontes. Al incorporar promedios móviles como referencias adicionales (Tabla A8.6), un promedio de 15 o de 60 minutos igualó o superó a Ridge en el MAE de la tasa DL en los tres horizontes; la ventaja de Ridge sobre persistencia en esta variable corresponde, en buena parte, a la suavización temporal. En MCS DL, Ridge conservó una ventaja de 16,6 % sobre el mejor promedio móvil a 15 minutos.

## A6: alcance de la afirmación sobre Ridge (×1)
- V27: En términos operacionales, Ridge fue el modelo más consistente para anticipar cambios en MCS y tasa DL,
- V28: En términos operacionales, entre los tres modelos evaluados Ridge fue el más consistente para anticipar cambios en MCS y tasa DL (frente a promedios móviles solo mantuvo su ventaja en MCS; Tabla A8.6),

## A2: discusión de alertas (×1)
- V27: Para el horizonte de 15 minutos, el sistema anticipó 589 de 1 548 condiciones futuras no normales, equivalentes al 38,05 %, y superó en 174 detecciones al refer...
- V28: Para el horizonte de 15 minutos, el sistema anticipó 589 de 1 548 condiciones futuras no normales, equivalentes al 38,05 %, frente a 549 (35,47 %) de persistencia. La diferencia de 40 detecciones no fue concluyente al 95 % y se acompañó de una mayor tasa de falsas alertas (7,51 % frente a 6,10 %). Por tanto, el resultado no autoriza a presentar la salida como una alarma autónoma ni como una mejora comprobada frente a persistencia; corresponde interpretarla como apoyo preventivo sujeto a calibración, validación prospectiva con incidencias reales y confirmación técnica.

## A2/A4: respuesta a P4 (×1)
- V27: Resultado y respuesta. A 15 minutos, el sistema anticipó 589 de 1 548 condiciones futuras no normales, con un recall de 38,05 %, frente a 35,47 % para persisten...
- V28: Resultado y respuesta. A 15 minutos, el sistema anticipó 589 de 1 548 condiciones futuras no normales, con un recall de 38,05 %, frente a 35,47 % para persistencia; la diferencia (2,58 puntos porcentuales) no fue concluyente al 95 % y la tasa de falsas alertas fue 7,51 % frente a 6,10 %. A igual tasa de falsas alertas no hubo ganancia de recall. La importancia por permutación identificó al SNR DL como indicador principal, seguido por la media de MCS UL (60 min), la variabilidad de la tasa DL (60 min) y el RSSI DL; el peso del SNR DL está condicionado por la regla que define el estado crítico.

## A2: discusión de anticipación (×1)
- V27: A un horizonte de 15 minutos, el modelo identificó 589 de 1 548 condiciones futuras no normales, equivalente a un recall de 38,05 %, frente al 35,47 % de persis...
- V28: A un horizonte de 15 minutos, el modelo identificó 589 de 1 548 condiciones futuras no normales (recall de 38,05 %), frente a 35,47 % de persistencia. La diferencia de 2,58 puntos porcentuales no fue concluyente y desapareció al igualar la tasa de falsas alertas; por ello no se demostró que las características temporales permitan reconocer una proporción adicional de degradaciones. En términos operacionales, el resultado no acredita un margen adicional para iniciar una revisión remota respecto de persistencia: solo muestra que el modelo desplaza el punto de operación hacia mayor sensibilidad c

## A2/A4: conclusión OE4 (×1)
- V27: Conclusión OE4 (P4/HE4). El sistema identificó retrospectivamente 589 de 1 548 condiciones futuras no normales a 15 minutos, con recall de 38,05 %, frente a 35,...
- V28: Conclusión OE4 (P4/HE4). El sistema identificó retrospectivamente 589 de 1 548 condiciones futuras no normales a 15 minutos, con recall de 38,05 %, frente a 35,47 % para persistencia; la diferencia no fue concluyente al 95 % y se anuló al igualar la tasa de falsas alertas. La contrapartida fue una tasa de falsas alertas de 7,51 % y una precisión de 32,61 %. El análisis de importancia por permutación señaló SNR DL, media de MCS UL, variabilidad de la tasa DL y RSSI DL como características influyentes. Como los estados fueron etiquetas proxy, la regla del estado crítico utiliza el propio SNR DL 

## A6: conclusión OE3 matizada (×1)
- V27: Para RSSI DL, persistencia mantuvo el menor MAE, mientras que los modelos aprendidos redujeron el RMSE.
- V28: Para RSSI DL, persistencia mantuvo el menor MAE, mientras que los modelos aprendidos redujeron el RMSE. Frente a promedios móviles, la ventaja de Ridge se mantuvo en MCS DL pero no en la tasa DL (Tabla A8.6).

## A2: costo de la sensibilidad (×1)
- V27: La mayor sensibilidad tuvo un costo: la tasa de falsas alertas aumentó de 6,10 % a 7,51 % y la precisión disminuyó de 35,72 % a 32,61 %. En otras palabras, el s...
- V28: La mayor sensibilidad tuvo un costo: la tasa de falsas alertas aumentó de 6,10 % a 7,51 % y la precisión disminuyó de 35,72 % a 32,61 %. En otras palabras, el sistema anticipó 40 detecciones adicionales, pero generó 229 falsas alertas adicionales; además, la ganancia de recall no fue concluyente al 95 % ni se mantuvo a igual tasa de falsas alertas. La utilidad práctica dependerá, por tanto, del costo relativo de omitir una degradación frente al costo de revisar una alerta que no se confirma.

## A2/A5: decisión de HE4 con criterio explícito (×1)
- V27: La HE4 sostuvo que el sistema anticiparía una proporción mayor de condiciones futuras no normales que persistencia a un horizonte de 15 minutos e identificaría ...
- V28: La HE4 sostuvo que el sistema anticiparía una proporción mayor de condiciones futuras no normales que persistencia a un horizonte de 15 minutos e identificaría los indicadores más influyentes. A 15 minutos, el recall aumentó 2,58 puntos porcentuales y la tasa de falsas alertas 1,41 puntos; el intervalo del 95 % de la diferencia de recall incluyó cero (−1,68 a 6,98 puntos) y, a la misma tasa de falsas alertas que persistencia, el recall fue igual (35,47 %). La explicabilidad identificó SNR DL, media de MCS UL, variabilidad de la tasa DL y RSSI DL entre los factores principales, con la salvedad 

## A2: Tabla XXI, fila HE4 (×1)
- V27: HE4 | 723/1 548 condiciones proxy no normales anticipadas (recall 38,05 %); más falsas alertas; SNR DL fue predictor influyente. | Respaldo parcial; sin fallas reales verificadas
- V28: None | 589/1 548 condiciones proxy no normales anticipadas (recall 38,05 % frente a 35,47 %; IC del 95 % de la diferencia incluye cero; sin ganancia a igual tasa de falsas alertas); SNR DL fue predictor influyente, condicionado por la regla de etiquetado. | Respaldo parcial (solo explicabilidad); anticipación no respaldada; sin fallas reales verificadas

## A2: hipótesis general (×1)
- V27: y mayor sensibilidad de alertas proxy; sin embargo,
- V28: y una sensibilidad de alertas proxy numéricamente mayor, pero no concluyente; sin embargo,

## A5: remisión a criterios y cifras vigentes (×1)
- V27: Las métricas proceden del conjunto de prueba cronológicamente posterior al entrenamiento;
- V28: Los criterios de decisión se enuncian en el Capítulo I; las cifras de HistGradientBoosting proceden de la corrida determinista de la V28 (parada temprana desactivada). Las métricas proceden del conjunto de prueba cronológicamente posterior al entrenamiento;

## A5: hipótesis y criterios en Cap. I (×6)
- V27: (no existía enunciado formal)
- V28: Hipótesis y criterios de decisión. Las hipótesis se enuncian / Hipótesis general (HG). El sistema inteligente basado en ana / HE1. Tras integrar, sincronizar y depurar la telemetría, los / HE2. En la ejecución integral, cada módulo recibe sus entrad / HE3. El sistema supera a persistencia en F1-macro con interv / HE4. A 15 minutos el recall de alertas supera al de persiste

## A3: causa y corrección de la no reproducibilidad (×1)
- V27: Las diferencias halladas en Windows para algunas métricas de HistGradientBoosting impiden declarar equivalencia numérica multiplataforma.
- V28: Las diferencias halladas entre plataformas en HistGradientBoosting pudieron deberse a la parada temprana automática de la librería (early_stopping='auto'), que reserva una submuestra aleatoria de validación; esa causa no se demostró. Lo comprobado es que, con esa configuración, el recall de alertas varió entre 38,6 % y 43,2 % según la semilla. En la V28 la parada temprana se desactivó (early_stopping=False) y todas las cifras de HistGradientBoosting se regeneraron con esa configuración. La equivalencia numérica del modelo corregido entre plataformas no ha sido verificada.

## A3: configuración declarada (×1)
- V27: (sin mención)
- V28: early_stopping=False

## A3: configuración declarada (×1)
- V27: (sin mención)
- V28: early_stopping=False

## A15: cita con página sobre fuente incorrecta (a confirmar contra [35]) (×1)
- V27: análisis documental sistemático de los archivos digitales [33, p. 30].
- V28: análisis documental sistemático de los archivos digitales [35].

## A16: ERA5-Land corresponde a [40] (×1)
- V27: Copernicus Climate Data Store [38].
- V28: Copernicus Climate Data Store [40].

## A17: Aiken pasa a la lista de referencias (×2)
- V27: L. R. Aiken, “Three Coefficients for Analyzing the Reliability and Validity of Ratings”, Educational and Psychological Measurement, vol. 45, no. 1, pp. 131–142, 1985, doi: 10.1177/0013164485451012
- V28: [41]

## A17: nueva referencia [41] (×1)
- V27: (ausente en la lista)
- V28: [41] L. R. Aiken, “Three Coefficients for Analyzing the Reliability and Validity of Ratings”, Educational and Psychological Measurement, vol. 45, no. 1, pp. 131–142, 1985, doi: 10.1177/0013164485451012

## resumen/abstract: cifras V28 (×1)
- V27: El clasificador obtuvo F1-macro de 0,566 y AUC de 0,788; su ventaja global sobre persistencia no fue robusta frente a todas las longitudes de bloque de bootstrap.
- V28: El clasificador, entrenado sin parada temprana para obtener resultados deterministas, obtuvo F1-macro de 0,566 y AUC de 0,788; su ventaja sobre persistencia (0,547) no fue concluyente al 95 %.

## resumen/abstract: cifras V28 (×1)
- V27: (recall de 38,05 %), con 1 217 falsas alertas.
- V28: (recall de 38,05 % frente a 35,47 % de persistencia), con 1 217 falsas alertas; la diferencia de recall no fue concluyente y desapareció al igualar la tasa de falsas alertas.

## resumen/abstract: cifras V28 (×1)
- V27: mientras que la comparación de RSSI mostró resultados mixtos.
- V28: mientras que la comparación de RSSI mostró resultados mixtos; frente a promedios móviles, la ventaja de Ridge se mantuvo en MCS pero no en tasa DL.

## resumen/abstract: cifras V28 (×1)
- V27: El aporte es un software informacional reproducible en el entorno Linux verificado;
- V28: El aporte es un software informacional cuyas cifras se regeneraron de forma determinista en la reejecución V28 (la equivalencia multiplataforma no fue verificada);

## resumen/abstract: cifras V28 (×1)
- V27: Classification achieved a macro-F1 of 0.566 and multiclass AUC of 0.788; its overall gain over persistence was not robust across all tested block-bootstrap lengths.
- V28: Classification, trained without early stopping to obtain deterministic results, achieved a macro-F1 of 0.566 and multiclass AUC of 0.788; its gain over persistence (0.547) was not conclusive at 95%.

## resumen/abstract: cifras V28 (×1)
- V27: (38.05% recall), with 1,217 false alerts.
- V28: (38.05% recall versus 35.47% for persistence), with 1,217 false alerts; the recall difference was not conclusive and disappeared at an equal false-alert rate.

## resumen/abstract: cifras V28 (×1)
- V27: whereas RSSI results were mixed.
- V28: whereas RSSI results were mixed; against moving-average baselines, Ridge's advantage held for MCS but not for downlink rate.

## resumen/abstract: cifras V28 (×1)
- V27: in a verified Linux environment;
- V28: with deterministic figures in the V28 rerun (cross-platform equivalence not verified);

## Tabla A8.1: se conservan las cifras históricas de la V27 (×1)
- V27: Entrenamiento (casos) | 82 373 | 82 358
- V28: Entrenamiento (casos) | 82 373 | 82 358

## Tabla A8.1: se conservan las cifras históricas de la V27 (×1)
- V27: Evaluación de prueba (casos) | 17 754 | 17 754
- V28: Evaluación de prueba (casos) | 17 754 | 17 754

## Tabla A8.1: se conservan las cifras históricas de la V27 (×1)
- V27: F1-macro | 0,5748 | 0,5773
- V28: F1-macro | 0,5748 | 0,5773

## Tabla A8.1: se conservan las cifras históricas de la V27 (×1)
- V27: AUC multiclase | 0,7880 | 0,8009
- V28: AUC multiclase | 0,7940 | 0,8009

## Tabla A8.1: se conservan las cifras históricas de la V27 (×1)
- V27: Alertas verdaderas positivas | 589 | 754
- V28: Alertas verdaderas positivas | 723 | 754

## Tabla A8.1: se conservan las cifras históricas de la V27 (×1)
- V27: Falsas alertas | 1 217 | 1 686
- V28: Falsas alertas | 1 742 | 1 686

## figuras 5-8 regeneradas (×4)
- V27: figura_4_4, 4_7, 4_5 y 4_8 de la V27
- V28: figuras regeneradas con la corrida V28


## Correccion posterior a la revalidacion (19-nov-2026)
- 4.3.2: diferencia de F1-macro frente a persistencia 0,028 -> 0,019 e IC 95 % [-0,017; 0,046] -> [-0,023; 0,045], segun results/tables/classification_bootstrap_comparison.csv. Hallazgo del experto V. Sanchez; era un residuo de V27 que el barrido anterior no detecto. Las tablas del Anexo A8.1 (V27) se conservan como historicas.
