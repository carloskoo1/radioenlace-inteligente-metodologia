# Auditoría independiente en Linux — reproducción satisfactoria (28-10-2026)

**Resultado:** el pipeline científico completó todas las etapas y el verificador original pasó en GitHub Actions con Ubuntu y Python 3.12. Se reprodujeron las cifras centrales de clasificación y alertas archivadas en la referencia de la tesis. No se afirma equivalencia byte a byte de todos los archivos binarios.

## Evidencia independiente

- [Ejecución pública GitHub Actions](https://github.com/carloskoo1/radioenlace-inteligente-metodologia/actions/runs/40744307330) — identificador 40744307330; conclusión success.
- Código exacto de la ejecución: commit **528b8a9fac79ac2846ef5f2f62802a3ec1b50c06**, rama candidata de reproducibilidad.
- Referencia histórica: release **v1.0.0**, commit **8f175ffef568c25cbaee91a1c04da3f2cc38cdb2**.
- Diferencia de ejecución respecto al código histórico: la importancia por permutación usa **un solo trabajador** en lugar de todos los procesos disponibles. No se cambiaron los datos, reglas de estados, semilla, entrenamiento del clasificador ni algoritmos de pronóstico.
- Entorno: Ubuntu de GitHub Actions, Python **3.12**, dependencias declaradas.
- Etapas completadas: verificación de SHA-256, preparación de 90 archivos, núcleo de diagnóstico y pronóstico, análisis extendido, bootstrap, figuras y verificador final.

## Métricas reproducidas

| Indicador | Referencia v1.0.0 | Reejecución Linux |
|---|---:|---:|
| Archivos diarios | 90 | 90 |
| Registros AP | 173 513 | 173 513 |
| Minutos observados | 118 458 | 118 458 |
| Anomalías | 1 093 | 1 093 |
| F1-macro HGB a 15 min | 0,5747978 | 0,5747978 |
| AUC multiclase HGB | 0,7940374 | 0,7940374 |
| Alertas verdaderas positivas | 723 | 723 |
| Alertas falsas positivas | 1 742 | 1 742 |
| MAE Ridge MCS DL a 15 min | 0,86944645 | 0,86944645 |
| MAE Ridge tasa DL a 15 min | 18,98490543 | 18,98490543 |

El registro público finaliza con: **«Verificación superada: conteos, modelos, horizontes y métricas principales coherentes.»** y **«Flujo reproducido correctamente.»** Los logs y tablas se conservaron como artefacto de la acción con retención temporal.

## Por qué difiere Windows

En Windows/Python 3.12 y 3.13, usando los datos originales y las bibliotecas declaradas, se repitieron los conteos, estados, umbrales y resultados de Ridge y persistencia; pero algunos valores de HistGradientBoosting difirieron: F1-macro **0,5787394**, AUC **0,7967051**, alertas **644** verdaderas positivas y **1 327** falsas positivas. Limitar hilos no restableció la referencia en Windows.

La evidencia indica **dependencia de plataforma de algunos resultados numéricos**. Todavía no se ha identificado el mecanismo exacto de esa diferencia (bibliotecas nativas, cálculo de punto flotante u otro factor). No debe declararse que Windows reproduce exactamente las cifras Linux ni imputar incorrectamente el problema a una manipulación de datos. Véase [auditoría Windows](AUDITORIA_WINDOWS_PY313_2026-10-28.md).

## Instrucciones reproducibles en Linux

Use **Ubuntu y Python 3.12**. En Windows, se puede utilizar Linux mediante WSL2 o una máquina virtual. Ejecute:

~~~bash
git clone https://github.com/carloskoo1/radioenlace-inteligente-metodologia.git
cd radioenlace-inteligente-metodologia
git checkout 528b8a9fac79ac2846ef5f2f62802a3ec1b50c06
python3.12 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python scripts/run_all.py
~~~

Se utiliza el commit exacto probado en la acción pública, y se debe comprobar el SHA-256 del archivo original de telemetría indicado en [data/README.md](../../data/README.md).

Existe también una [acción manual del release científico](../../.github/workflows/reproduccion_cientifica.yml); no debe confundirse con la corrida independiente exacta aquí documentada, que utilizó el commit candidato indicado.

El Dockerfile experimental de la rama candidata **no tiene todavía una ejecución de contenedor comprobada**, por lo que no se declara como alternativa ya validada.

## Alcance de la solución

**Quedó demostrada la reproducción integral del proceso y de las métricas principales en el entorno Linux indicado.** No está demostrada la equivalencia exacta en todos los sistemas operativos o de todos los archivos binarios.

Para la defensa se recomienda mostrar la acción Linux exitosa y explicar la limitación computacional documentada en Windows. Esta evidencia no exige sustituir las cifras científicas originales de la tesis, ahora reproducidas en Linux.
