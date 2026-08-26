# Diccionario de datos

| Campo derivado | Tipo | Unidad | Descripción |
|---|---|---|---|
| `timestamp_local` | fecha-hora | America/Lima | Marca temporal consolidada por minuto |
| `rssi_dl_dbm` | numérico | dBm | Potencia recibida en bajada |
| `rssi_ul_dbm` | numérico | dBm | Potencia recibida en subida |
| `snr_dl_db` | numérico | dB | Relación señal a ruido en bajada |
| `snr_ul_db` | numérico | dB | Relación señal a ruido en subida |
| `mcs_dl` | numérico ordinal | código del radio | Nivel MCS de bajada |
| `mcs_ul` | numérico ordinal | código del radio | Nivel MCS de subida |
| `rate_dl_mbps` | numérico | Mbps | Tasa física/negociada DL; no throughput efectivo |
| `observed` | binario | — | Existe al menos un indicador válido en el minuto |
| `state_proxy` | categórico | — | Normal, degradado, crítico o ausente |
| `anomaly_score` | numérico | — | Facilidad relativa de aislamiento |
| `anomaly_flag` | binario | — | Marcación de Isolation Forest |
