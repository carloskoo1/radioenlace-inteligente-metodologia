# Anexo 2. Ficha digital de registro de telemetría

Instrumento técnico de elaboración propia para documentar los registros y sus reglas de verificación. Transcripción de la tabla A2.1 de la tesis de Ubelser Tamay (versión de revisión, octubre de 2026).

| Campo | Unidad o formato | Descripción | Regla de verificación |
| --- | --- | --- | --- |
| Fecha y hora | AAAA-MM-DD HH:MM:SS; America/Lima | Instante de generación de la lectura | Marca temporal interpretable y ordenable |
| Rol | AP/estación | Función del equipo que generó el registro | Conservar únicamente el rol AP para el análisis principal |
| RSSI DL/UL | dBm | Potencia recibida en bajada y subida | Valores ≥ 0 dBm se tratan como ausentes |
| SNR DL/UL | dB | Relación señal-ruido en bajada y subida | Valores ≤ 0 dB se tratan como ausentes |
| MCS DL/UL | Nivel reportado | Esquema de modulación y codificación | Conversión numérica y conservación del código original |
| Tasa DL | Mbps | Tasa física o negociada reportada por el radio | Extracción numérica; no se interpreta como throughput efectivo |
| Archivo de origen | Texto | Fuente diaria de la observación | Trazabilidad con el archivo original |

Los registros fuente originales están en `data/raw/Datos.zip`. El script `scripts/00_prepare_data.py` comprueba su SHA-256 antes de extraerlos.
