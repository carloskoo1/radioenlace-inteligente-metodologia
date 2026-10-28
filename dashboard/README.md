# Dashboard ejecutable del radioenlace Cuñacales–San José

**Extensión de interfaz creada para demostrar el producto científico**, posterior a la versión sellada v1.0.0. Explora datos y salidas calculadas, permite filtrar predicciones históricas y puede ejecutar nuevamente el pipeline original.

No captura RF en tiempo real, no envía alarmas a la red y no realiza inferencia interactiva sobre equipos operativos. Los estados son **etiquetas proxy**, no incidencias confirmadas.

## Ejecución local

Se recomienda Python 3.12, usando un entorno virtual:

    git clone https://github.com/carloskoo1/radioenlace-inteligente-metodologia.git
    cd radioenlace-inteligente-metodologia
    python -m venv .venv
    # Active .venv según su sistema operativo
    pip install -r requirements.txt
    pip install -r dashboard/requirements-dashboard.txt
    python scripts/run_all.py
    streamlit run dashboard/app.py

Abra en un navegador la dirección local indicada por Streamlit (usualmente http://localhost:8501).

## Navegación

- Producto: cadena funcional e indicadores generales.
- Calidad de datos: distingue cobertura temporal de completitud.
- Diagnóstico: matriz de confusión, F1 y AUC, intervalos de confianza.
- Pronóstico: compara persistencia, Ridge y HGB por objetivo y horizonte; si el pipeline ha corrido, muestra mediciones y predicciones individuales.
- Alertas: sensibilidad y falsas alarmas.
- Anomalías y explicabilidad: ordenamiento de casos e importancia por permutación.
- Reproducibilidad: integridad SHA-256 de datos y ejecución nuevamente del flujo.

## Origen y límites

El análisis original y sus resultados están documentados en la [versión científica v1.0.0](https://github.com/carloskoo1/radioenlace-inteligente-metodologia/releases/tag/v1.0.0). La interfaz se añadió en main como herramienta adicional. Las métricas no son garantía de generalización a nuevos radioenlaces ni evidencia de fallas reales verificadas.

Para defensa, distinga entre: (1) producto computacional evaluado en la tesis; (2) dashboard añadido posteriormente; (3) validación de desempeño fuera de muestra; y (4) reproducción independiente desde los archivos originales.
