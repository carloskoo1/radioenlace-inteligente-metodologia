# Ficha de control de calidad de datos

| Control | Criterio | Evidencia generada |
|---|---|---|
| Integridad de fuente | SHA-256 coincide con el manifiesto | Salida de `00_prepare_data.py` |
| Rol | Solo registros AP | `analysis_summary.json` |
| Temporalidad | Fecha válida, orden cronológico y zona America/Lima | Base maestra |
| Unicidad | Una observación por minuto después de consolidar | Base maestra |
| Validez RSSI | RSSI < 0 dBm | Valores no válidos convertidos en ausentes |
| Validez SNR | SNR > 0 dB | Valores no válidos convertidos en ausentes |
| Ausencias | Vacíos largos no interpolados | Columna `observed` |
| Fuga temporal | Umbrales, imputación y entrenamiento sin usar prueba | Código y protocolo |
