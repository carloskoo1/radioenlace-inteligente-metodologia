# Auditoría adversarial de cierre — Tesis de Ubelser Tamay, versión V27 (18 de noviembre de 2026)

**Estado del documento:** copia pública revisada V27 incorporada a GitHub; nuevo DOI de Zenodo pendiente de ingesta y verificación. No confundir esta revisión con la release preservada `v1.1.1` ni con una aprobación oficial de jurado.

**Archivo revisado:** `TESIS_UBELSER_AUDITORIA_ADVERSARIAL_V27_20261118.docx`  
**SHA-256 del Word revisado:** `38f16f9c036deae734fa1d7991f7ee2ad4e5de087e8463b73bfe78018054d70a`  
**Extensión del Word renderizado:** 109 páginas (número físico del PDF de verificación); **35 tablas y 16 objetos gráficos** en la estructura DOCX, que incluyen figuras y evidencias documentales.  
**Punto de partida:** V26C, con las tres evaluaciones por juicio de expertos, sus observaciones y matriz de subsanación.

## Criterio disciplinar y producto

El aporte tecnológico de pregrado en Ingeniería de Sistemas se presenta como **prototipo de sistema de información inteligente**, de ejecución por lotes y validación retrospectiva. Integra archivos históricos de telemetría, controles de calidad, construcción de datos temporales, diagnóstico de estados operacionales derivados (*proxy*), anomalías, pronóstico y reportes reproducibles. No se declara que el dashboard posterior sea el producto científico original ni se afirma predicción en línea o confirmación de averías físicas reales.

## Trazabilidad obligatoria por objetivo

| Pregunta | Objetivo | Hipótesis | Indicadores efectivamente evaluados | Técnica e instrumento | Resultado e inferencia |
|---|---|---|---|---|---|
| P1. Calidad y comportamiento temporal de la telemetría | OE1. Integrar, depurar y caracterizar la serie | HE1. Calidad y trazabilidad para registros observados | Cobertura, completitud multivariable, duplicados y centinelas | Observación documental estructurada; fichas A2 y A3 | 173 513 registros AP; 118 458 / 180 025 minutos con datos (65,80 %); 117 911 minutos completos entre los observados (99,54 %). Respaldo acotado al período observado |
| P2. Construcción e integración del sistema | OE2. Diseñar, implementar y verificar módulos | HE2. Integración funcional | Pruebas funcionales y salidas por módulo | Ciencia del diseño, evaluación computacional; ficha A4 | Producto ejecutable por lotes y reproducible en entorno Linux auditado; no se probó despliegue predictivo en producción |
| P3. Comparación frente a referentes | OE3. Evaluación diagnóstica y de pronóstico | HE3. Mejoras comparativas | F1-macro, AUC, MAE/RMSE, horizonte, n e IC | Evaluación computacional cronológica; matriz A5 | Clasificación F1-macro 0,5748 frente a 0,5467 de persistencia, pero ventaja no robusta a todos los bloques; mejoras de Ridge en MCS y tasa DL, no uniformes en RSSI. Respaldo parcial |
| P4. Anticipación e interpretabilidad | OE4. Evaluar alerta futura e influencia de variables | HE4. Mayor detección e identificabilidad de predictores | VP/FP/FN/VN, recall, precisión, tasa falsas alertas, importancia por permutación | Análisis temporal; ficha A6 | 723 VP de 1 548 casos proxy no normales futuros; recall 46,71 %, FP 1 742 y tasa de falsas alertas 10,75 %. Respaldo parcial sin bitácora de fallas |

**Hipótesis general:** respaldo parcial; no confundir funcionamiento del artefacto ni mejoras específicas con superioridad integral o eficacia clínica/operacional frente a fallas confirmadas.

## Correcciones sustantivas incorporadas en V27

1. Las preguntas específicas P1–P4 ahora están formuladas explícitamente en la **Introducción**, después de la pregunta general.
2. Los objetivos OE1–OE4 aparecen conectados uno a uno con las preguntas; la **Tabla VIII** dejó de agruparlos en una sola fila y ofrece una fila por objetivo, hipótesis, dimensiones, técnicas e instrumentos.
3. Se aclararon términos y denominaciones metodológicas: observación **documental estructurada**, no una campaña metrológica autónoma; matriz de predictores **temporales**, no causal; ficha A5 como instrumento de evaluación del pronóstico.
4. Tres referencias a Medina Romero et al. que figuraban erróneamente como **[33]** fueron corregidas a **[35]**, conservando [33] para Jacob et al. Se corrigieron asimismo referencias ISO/IEC de la nota del anexo (25012 [18], 25024 [19], 15939 [20]).
5. El resumen y el abstract explicitan metodología, producto, muestra, resultados, limitaciones y **V de Aiken descriptiva = 0,844**.
6. El apartado **4.7, Prueba y contrastación de hipótesis**, contiene una explicación introductoria y una tabla de decisión visible, seguida de HE1–HE4 e hipótesis general. **No se ha desplazado la contrastación a Limitaciones**.
7. Las conclusiones finales quedaron identificadas como **OE1, OE2, OE3 y OE4**, con límites propios; se mantiene un cierre general.
8. Se mantienen las auditorías Linux del 12-11-2026: **purga de 15 casos** y sensibilidad por bloques de bootstrap. Los bloques de 60 representan **60 observaciones elegibles**, no necesariamente 60 minutos reales.
9. Los instrumentos de los anexos A2–A6 conservan la valoración de tres especialistas y la matriz de observaciones. Las fichas firmadas originales no deben alterarse; si se publican sus facsímiles, revisar antes la autorización de difusión pública de las firmas.

## Fuentes y métodos utilizados

- **Sistemas de Información y ciencia del diseño:** Hevner et al. [16]; Peffers et al. [17].
- **Calidad de datos y medición:** ISO/IEC 25012 [18]; ISO/IEC 25024 [19]; ISO/IEC/IEEE 15939 [20].
- **Diagnóstico y desequilibrio de clases:** Fawcett [21]; Saito y Rehmsmeier [22].
- **Anomalías y modelos:** Chandola et al. [23]; Liu et al. [24]; Hyndman y Athanasopoulos [25]; Hoerl y Kennard [26]; Friedman [27].
- **Metodología de investigación y técnicas:** Hernández-Sampieri y Mendoza [30]; Kitchenham et al. [32]; Jacob et al. [33]; Medina Romero et al. [35].
- **Replicabilidad e incertidumbre temporal:** TriScale [34]; Künsch [38].
- **Auditorías reproducibles:** [purga temporal y sensibilidad por bloques](../reproducibilidad/AUDITORIA_FINAL_PURGA_BLOQUES_2026-11-12.md).

Los números entre corchetes son las referencias IEEE del propio Word; no son nuevas referencias bibliográficas inventadas.

## Juicio de expertos

**Aidé Yanet Huamán Rivera**, **Jaime Ayay Valdez** y **Víctor Sánchez Cáceres** revisaron el contenido de cinco instrumentos (A2–A6), con puntuaciones de 3 y 4 en claridad, pertinencia, coherencia y suficiencia. El resultado descriptivo global es **V de Aiken = 0,844**; la suficiencia presenta **V = 0,667**. Los expertos emitieron observaciones subsanables, no certificaciones de calibración metrológica ni de exactitud operativa de modelos. La versión enviada por correo a los tres fue **V25**; los originales recibidos deben conservarse sin reescribir sus leyendas o firmas.

## Paquete público preparado (no depositado todavía)

Se preparó un ejemplar de publicación de **103 páginas**, con resultados, tablas, datos bibliográficos y valoraciones de expertos, **sin las seis imágenes de formularios firmados**; los originales íntegros permanecen en el expediente privado.

- Nombre: `TESIS_UBELSER_V27_COPIA_PUBLICA_SIN_FIRMAS_20261118.docx`.
- SHA-256: `d466d42d1ce4e14bdeb059d8db9925fd5c2e8622a095b8b2a64d06b7bad04733`.
- Ruta prevista en GitHub: `docs/tesis/TESIS_UBELSER_V27_COPIA_PUBLICA_SIN_FIRMAS_20261118.docx`.

**Archivo público verificado en GitHub:** [descargar V27 optimizada](TESIS_UBELSER_V27_PUBLICA_OPTIMIZADA_20261118.docx) — 1 206 277 bytes; SHA-256 `04c1f4b4b220e5653dc363fdea5014783c6d74ddc06fa6b39b96fe94053fa959`. La copia pública tiene 103 páginas; contiene las tablas y resultados sin imágenes de firmas. La copia completa, con las fichas firmadas, se conserva en Google Drive bajo acceso de propietario y no se destina a publicación abierta.

## Alcance archivístico y preservación

El DOI **[10.5281/zenodo.23748244](https://doi.org/10.5281/zenodo.23748244)** identifica la release archivada `v1.1.1` de octubre de 2026. **No identifica la V27 de noviembre de 2026**.

Para archivar V27 de forma honesta se debe primero colocar el Word realmente revisado y un ejemplar público sin datos sensibles en el repositorio, comprobar su SHA-256 y **solo entonces** emitir una nueva release, revisar la ingesta por Zenodo y registrar el nuevo DOI de versión. No modificar los objetos ya archivados ni afirmar que una nueva versión fue preservada hasta verificarlo.

**Dictamen:** favorable en coherencia científica para pregrado con límites explicitados; el cierre administrativo y la aprobación de tesis corresponden a la UNC.