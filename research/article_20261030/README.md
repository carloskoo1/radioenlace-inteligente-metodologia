# Reanálisis para artículo de pronóstico de tasa DL

Extensión retrospectiva separada de la tesis cerrada de Ubelser Tamay.
No modifica `src/radioenlace`, el archivo original ni `results/tables`.
La ruta corresponde al radioenlace Cuñacales–San José; el objetivo es el campo
`dl_rate` reportado por el equipo, no throughput TCP ni fallas confirmadas.

## Ejecutar

Entorno utilizado: Linux, Python 3.12.14 y las versiones de `requirements.txt`.
Desde la raíz del repositorio:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
OMP_NUM_THREADS=2 OPENBLAS_NUM_THREADS=2 python research/article_20261030/reanalyse.py
```

Para comprobar invariantes de implementación sin entrenar los modelos:

```bash
python research/article_20261030/reanalyse.py --self-test
```

La ejecución verifica el SHA-256 del ZIP original y genera todo bajo la carpeta
`research/article_20261030/results`. Los archivos voluminosos de predicciones y
serie minutal se regeneran localmente y no se incluyen en esta rama.

## Protocolo

- Solo registros AP. Agregación por mediana en una grilla de calendario de un
  minuto. Los objetivos futuros no se rellenan.
- Arrastre causal de predictores limitado a un minuto. Medias y desviaciones
  de las características usan exclusivamente minutos anteriores al origen.
- Cinco ventanas de entrenamiento creciente; pruebas entre los percentiles
  50–60, 60–70, 70–80, 80–90 y 90–100 de los minutos observados.
- Un origen de entrenamiento se conserva solo si su objetivo futuro es
  anterior al inicio de la prueba. El objetivo de prueba también debe estar
  dentro de la ventana correspondiente.
- Horizonte de 5, 15 y 30 minutos de calendario; comparación pareada en los
  mismos orígenes disponibles. La decisión se toma después de cerrar el bin
  minutal del predictor.
- Modelos con parámetros fijos del trabajo base: Ridge y gradient boosting.
  En esta extensión se desactiva el early stopping interno de boosting y se
  utilizan exactamente 120 iteraciones.
- Modelo aprendido principal sin códigos MCS. Ablaciones con historial de
  tasa solamente y con la codificación numérica antigua de MCS.
- Referentes: persistencia, medias móviles de 5/15/60 minutos, mediana móvil
  de 60 minutos, media y mediana de entrenamiento. Los referentes adicionales
  de 15/60 minutos y constantes se añadieron exploratoriamente después de la
  primera ejecución; se conservan todos sus resultados. No hay preregistro.
- Bootstrap circular pareado por bloques de 60/180/1440 minutos de calendario,
  1000 repeticiones, estratificado por ventana y preservando las ausencias.
  Los intervalos son condicionales al archivo y no están ajustados por
  comparaciones múltiples. No constituyen incertidumbre entre radioenlaces.

## Resultado central

A 15 minutos, sobre 59 035 pronósticos pareados:

| Método | MAE Mbps | RMSE Mbps |
| --- | ---: | ---: |
| Persistencia | 23.054 | 35.234 |
| Media móvil 60 min | 19.006 | 26.943 |
| Mediana móvil 60 min | 18.209 | 28.049 |
| Ridge historial de tasa | 18.875 | 26.470 |
| Ridge tasa y RF sin MCS | 18.920 | 26.484 |
| Gradient boosting sin MCS | 19.276 | 27.240 |

La mejora frente a persistencia no implica superioridad frente a todos los
referentes simples. La mediana tiene menor MAE; Ridge tiene menor RMSE.
Agregar RF no aporta una mejora del MAE agregado frente al historial de tasa
en esta evaluación; no es una prueba formal de equivalencia.

## Trazabilidad y alcance

`boundary_audit.csv` compara Ridge en los cortes originales con y sin purga.
Los candidatos que cruzan la frontera son 5/15/30; el protocolo corregido
retiene cero. El efecto máximo del ajuste sobre MAE es menor de 0.001 Mbps.
`splits.csv` identifica cada intervalo y su población efectiva.
`rolling_metrics.csv` y `pooled_metrics.csv` conservan todos los métodos.
Los dos archivos bootstrap documentan las comparaciones con persistencia y
con referentes más fuertes. `summary.json` identifica entorno y decisiones.

La primera ejecución más su sensibilidad y la segunda ejecución integral
coincidieron para las 33 filas agregadas con tolerancia de 1e-12.
Las pruebas incorporadas verifican purga, causalidad de características,
objetivos ausentes y remuestreo pareado de pronósticos idénticos.

Es un análisis retrospectivo de un solo trayecto ya examinado en la tesis.
No proporciona validación espacial, evaluación prospectiva intocada,
predicción de fallas, throughput de aplicación ni transferencia a AtmosLink
6 GHz. Los vacíos describen adquisición, no disponibilidad del enlace.
Comparte infraestructura y parte del calendario con el manuscrito relacionado
de observabilidad RF/TCP; esa reutilización debe declararse en el artículo.

El código de esta extensión se preparó con asistencia de OpenAI ChatGPT.
Las métricas proceden de ejecutar el archivo de telemetría original.
