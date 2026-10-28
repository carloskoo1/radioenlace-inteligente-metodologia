# Material para la sustentación — Ubelser Tamay

**Instalación en otra computadora y replicación por terceros:** [guía detallada de instalación, ejecución y reproducibilidad](../GUIA_INSTALACION_DASHBOARD_Y_REPRODUCIBILIDAD.md). Incluye comprobaciones, incidencias frecuentes y las discrepancias documentadas de la auditoría independiente.

Este directorio acompaña el producto científico y tecnológico publicado en este repositorio. **No modifica los experimentos ni los resultados de la versión fija [v1.0.0](https://github.com/carloskoo1/radioenlace-inteligente-metodologia/releases/tag/v1.0.0).**

## ¿Qué producto presenta la tesis?

Un sistema computacional modular, reproducible y ejecutado por lotes que transforma telemetría del radioenlace Cuñacales–San José en información para diagnóstico, detección de anomalías, pronóstico multihorizonte y explicabilidad.

- **Producto tecnológico ejecutable:** `src/radioenlace/` y `scripts/run_all.py`.
- **Producto científico:** datos originales, parámetros y protocolo, tablas, gráficos, comparaciones de modelos y controles de verificación.
- **Demostración didáctica:** [demostracion_resultados_sustentacion.html](demostracion_resultados_sustentacion.html), un visor de resultados existentes para facilitar la exposición. **No es un sistema de monitoreo en vivo ni ejecuta predicciones nuevas.**

## Instrumentos técnicos de la tesis

Se han incorporado transcripciones en Markdown de las tablas de los anexos 2–6 para permitir su consulta y revisión independiente:

- [`ANEXO_2_FICHA_TELEMETRIA.md`](../instrumentos/ANEXO_2_FICHA_TELEMETRIA.md)
- [`ANEXO_3_CONTROL_CALIDAD.md`](../instrumentos/ANEXO_3_CONTROL_CALIDAD.md)
- [`ANEXO_4_VERIFICACION_FUNCIONAL.md`](../instrumentos/ANEXO_4_VERIFICACION_FUNCIONAL.md)
- [`ANEXO_5_MATRIZ_EVALUACION.md`](../instrumentos/ANEXO_5_MATRIZ_EVALUACION.md)
- [`ANEXO_6_CONDICIONES_ALERTAS.md`](../instrumentos/ANEXO_6_CONDICIONES_ALERTAS.md)
- [`ANEXO_6_MATRIZ_EXPLICABILIDAD.md`](../instrumentos/ANEXO_6_MATRIZ_EXPLICABILIDAD.md)

Los instrumentos son fichas y matrices técnicas, no escalas psicométricas; la validez se vincula a la correspondencia entre variables, dimensiones, indicadores, campos y evidencias; la consistencia se verifica mediante reglas uniformes y la confiabilidad tecnológica se apoya en datos originales conservados, ejecución determinista y verificaciones funcionales. No corresponde atribuirles alfa de Cronbach.

## Cómo reproducir los análisis

```bash
pip install -r requirements.txt
python scripts/run_all.py
```

La presencia de código y verificadores no sustituye una **ejecución independiente, desde cero, en un entorno limpio**. Las etiquetas operacionales son **proxy**, no incidentes corroborados mediante bitácoras de campo.

## Estado documental

Se han incorporado al repositorio archivos binarios de referencia en [docs/material_original/](../material_original/): `Tesis_Ubelser_Tamay_FUENTE_2026-10-28.docx` y `Presentacion_Ubelser_BASE_2026-10-28.pptx`. **Estos son material fuente/base**, no equivalen necesariamente a la última tesis compaginada o a la última presentación revisada. La tesis fuente contiene contenido provisional y no se identifica como tesis aprobada.

La extensión visual [dashboard/](../../dashboard/) incluye un software Streamlit ejecutable para navegar resultados históricos; fue añadida con posterioridad a la investigación sellada.

**Auditoría independiente:** [Windows Python 3.12/3.13](../reproducibilidad/AUDITORIA_WINDOWS_PY313_2026-10-28.md). Los conteos de datos, anomalías y ciertos pronósticos coinciden, pero la clasificación y las alertas difieren de la versión científica. No afirmar reproducibilidad numérica integral antes de resolver el hallazgo.
