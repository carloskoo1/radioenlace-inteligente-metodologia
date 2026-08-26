# Datos y trazabilidad

## Fuente principal

`raw/Datos.zip` contiene los 90 archivos diarios originales de telemetría local. Su SHA-256 es:

`786a037e749ce0c5bf7b3d8bd66f419a0a76de809c68857534e03487fc922bfa`

Los archivos originales son inmutables. El script `00_prepare_data.py` verifica el resumen criptográfico antes de extraerlos.

## Selección de la fuente maestra

Se conservaron solamente registros con rol AP. Los agregados de `registros.zip` no se sumaron porque se superponían temporalmente con la fuente local y podían duplicar mediciones. El archivo `salidas.zip` no se publica: contenía productos redundantes, resultados antiguos con partición aleatoria y un archivo de configuración sensible. Solo se conserva el conjunto auxiliar radio–clima previamente depurado.

## Fuente auxiliar

`auxiliary/dataset_final_radio_clima.csv` contiene 3529 observaciones horarias para el análisis exploratorio contemporáneo radio–clima. No se concatenó con la base principal y no se utilizó para afirmar causalidad ni para reemplazar la validación cronológica.

## Privacidad y seguridad

La telemetría incluye una dirección IPv4 privada del equipo. No se publican credenciales, tokens, archivos `.env`, configuraciones de acceso ni direcciones públicas.
