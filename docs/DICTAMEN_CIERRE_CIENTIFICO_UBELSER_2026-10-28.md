# Dictamen técnico-académico de cierre científico — Tesis de José Ubelser Tamay

**Fecha:** 28 de octubre de 2026.  
**Institución:** Universidad Nacional de Cajamarca (UNC).  
**Naturaleza:** informe de apoyo a la evaluación metodológica, **no** acta oficial de un jurado.

## Objeto

Evaluar si corresponde cerrar la investigación aplicada sobre un sistema inteligente de diagnóstico y pronóstico de telemetría del radioenlace rural Cuñacales–San José, sin incorporar mediciones o modelos de otra campaña.

## Evidencia revisada

- Tesis de trabajo, con cuatro objetivos específicos y respuestas por objetivo en el capítulo IV; apartados 4.6 (preguntas) y 4.7 (hipótesis); conclusiones organizadas por resultados.
- Fuente original: 90 archivos, 173 513 registros AP, 118 458 minutos observados; documentación de integridad, depuración y partición temporal cronológica.
- Producto científico: scripts, configuración, experimentos, tablas y figuras. El dashboard Streamlit se agregó como **extensión posterior**.
- Auditoría pública Linux (Ubuntu y Python 3.12) sobre el **commit candidato 528b8a9fac79ac2846ef5f2f62802a3ec1b50c06**, no exactamente el commit original `v1.0.0` sin ajustes: [ejecución de GitHub Actions](https://github.com/carloskoo1/radioenlace-inteligente-metodologia/actions/runs/40744307330).
- Auditorías de Windows/Python 3.12 y 3.13: valores diferentes del clasificador HistGradientBoosting y de alertas; limitación de equivalencia numérica entre plataformas no resuelta.

## Valoración técnica

| Criterio | Dictamen |
|---|---|
| Pertinencia y aplicación | Problema real de telemetría y desempeño operacional del enlace rural, **suficiente**. |
| Correspondencia de objetivos y resultados | Resultados explícitos por objetivo y respuestas a las preguntas, **suficiente**. |
| Producto tecnológico | Pipeline funcional y documentado; dashboard posterior, **verificable**. |
| Calidad y trazabilidad | Controles y registros publicados, con brechas temporales documentadas; **suficiente con limitaciones**. |
| Hipótesis general | **Respaldo parcial**, en coherencia con el desempeño desigual de los modelos y su incertidumbre. |
| Reproducción | Métricas principales reproducidas bajo Linux en commit candidato controlado; **no equivalencia universal ni byte a byte**. |
| Validez externa | Caso único, etiquetas de estado proxy; **no extrapolar sin validación**. |
| Cierre editorial | Corregidos agradecimiento y dedicatoria; **requiere comprobación final de paginación, citas, índices y formato UNC**. |

## Interpretación

Una investigación no exige que cada algoritmo supere a todas las referencias en todos los indicadores. Exige demostrar **qué se desarrolló**, **cómo se evaluó**, **qué resultados produjo** y **qué límites tiene su interpretación**. Aquí, Ridge mejora algunos pronósticos de MCS y tasa reportada por el equipo; persistencia obtiene mejor MAE para determinados pronósticos RSSI; y la mejora en F1-macro de la clasificación no resulta concluyente al 95 %. La detección anticipada incrementa también falsas alarmas.

Las etiquetas «normal», «degradado» y «crítico» son **proxy**, no fallas de campo confirmadas. La tasa DL reportada por el equipo **no equivale** a throughput TCP. El nuevo dashboard con respaldos de AtmosLink 6 GHz no constituye inferencia prospectiva validada en esta tesis.

## Dictamen

**FAVORABLE PARA EL CIERRE CIENTÍFICO Y LA PREPARACIÓN DE LA SUSTENTACIÓN, CON VERIFICACIONES EDITORIALES FINALES.**

No recomiendo ampliar la toma de datos ni cambiar hipótesis para forzar una confirmación total. Las verificaciones documentales previas al depósito universitario deben incluir paginación, índices y títulos, leyendas, citas IEEE, bibliografía, anexos y que Resumen/Abstract inicien en páginas independientes según el formato vigente. La autorización de entrega y defensa compete a la UNC y su jurado.

## Artefactos de consulta

- [Tesis actualizada — Word](material_original/TESIS_UBELSER_TAMAY_CIERRE_DOCUMENTAL_2026-10-28.docx), con dedicatoria a los padres y agradecimiento al Dr. Carlos Jesús Koo Labrín.
- [Código y resultados científicos v1.0.0](https://github.com/carloskoo1/radioenlace-inteligente-metodologia/releases/tag/v1.0.0).
- [Auditoría Linux](reproducibilidad/AUDITORIA_LINUX_EXITOSA_2026-10-28.md).
- [Guía independiente de instalación y reproducción](GUIA_INSTALACION_DASHBOARD_Y_REPRODUCIBILIDAD.md).

**Advertencia de versión:** el archivo Word actualizado es la **versión de cierre documental para revisión final**; no se presenta como tesis aprobada oficialmente. El PowerPoint publicado en `docs/material_original/` es una presentación **base**, no el archivo más reciente compartido en la conversación.
