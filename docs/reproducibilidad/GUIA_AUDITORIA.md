# Auditoría independiente de reproducibilidad

Se diferencia **repetición del flujo** (ejecutar los scripts) de **reproducción de los resultados publicados** (comparar las métricas con la referencia). La segunda requiere controles explícitos, no solamente disponibilidad del código.

Pasos recomendados, preferentemente en una máquina distinta de la utilizada originalmente:

1. Descargar la etiqueta pública inmutable v1.0.0 y verificar el commit 8f175ffef568c25cbaee91a1c04da3f2cc38cdb2.
2. Crear un entorno limpio y anotar sistema operativo, Python, NumPy, pandas y scikit-learn.
3. Instalar requirements.txt, ejecutar scripts/run_all.py y conservar íntegramente su salida.
4. Si el flujo finaliza, comparar resultados recalculados con la publicación; no reemplazar automáticamente tablas cuando existan discrepancias.
5. Utilizar el script adicional scripts/auditar_reproduccion.py (disponible en la rama main) para registrar diferencias en reproduccion_auditoria.json.

**Límites:** la semilla aleatoria fijada no garantiza bit a bit idénticos entre sistemas operativos, bibliotecas numéricas, arquitecturas de CPU o distintos números de hilos. Las diferencias requieren evaluación y documentación; no deben ocultarse. Una clasificación distinta puede alterar las alertas y las conclusiones interpretativas.

**Datos:** la fuente original se controla mediante SHA-256; las etiquetas son proxy; la tasa DL no equivale a throughput TCP; la comparación por bloques evita ignorar la dependencia temporal.

**Estado:** disponer del repositorio y un script de comprobación no certifica de antemano la reproducción independiente. Solo debe afirmarse una vez comparadas las salidas de una ejecución completa en un entorno limpio.
