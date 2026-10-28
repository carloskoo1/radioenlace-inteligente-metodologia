# Depósito verificado en Zenodo y citación del software

**Estado al 28 de octubre de 2026: publicado y verificado.** El repositorio de Ubelser está habilitado en la integración GitHub–Zenodo. La versión **v1.1.1** cuenta con un registro público y un DOI propio.

| Referencia | Enlace |
|---|---|
| DOI de la versión preservada v1.1.1 | [10.5281/zenodo.23748244](https://doi.org/10.5281/zenodo.23748244) |
| Ficha pública en Zenodo | [Registro 23748244](https://zenodo.org/records/23748244) |
| DOI que agrupa las versiones del software | [10.5281/zenodo.23748243](https://doi.org/10.5281/zenodo.23748243) |
| Release de GitHub archivada | [v1.1.1](https://github.com/carloskoo1/radioenlace-inteligente-metodologia/releases/tag/v1.1.1) |
| Código exacto preservado | [9cf41e078af00915807e3e3d26d27569922a4004](https://github.com/carloskoo1/radioenlace-inteligente-metodologia/tree/9cf41e078af00915807e3e3d26d27569922a4004) |
| Validación y publicación automatizadas | [GitHub Actions: ejecución 40779132008](https://github.com/carloskoo1/radioenlace-inteligente-metodologia/actions/runs/40779132008) |

Para citar o repetir una versión concreta, utilice el **DOI de versión 10.5281/zenodo.23748244**. El DOI general agrupa las versiones y puede resolver a una versión posterior.

## Autoría comprobada en el registro público

Los metadatos públicos de Zenodo contienen, en este orden:

| Autor | ORCID | Afiliación |
|---|---|---|
| Ubelser Tamay | [0009-0007-2020-2338](https://orcid.org/0009-0007-2020-2338) | Universidad Nacional de Cajamarca |
| Carlos Jesús Koo Labrín | [0000-0002-0323-2961](https://orcid.org/0000-0002-0323-2961) | Universidad Nacional de Cajamarca |

El depósito está clasificado como **Software**, tiene acceso abierto y fecha de publicación **2026-10-28**.

## Contenido preservado

El ZIP de Zenodo conserva el estado de la release v1.1.1, incluidos el código, los datos publicados, los resultados, el dashboard, las guías, los instrumentos y los documentos complementarios.

Entre los documentos archivados se verificaron:

- [Tesis de cierre documental en Word](material_original/TESIS_UBELSER_TAMAY_CIERRE_DOCUMENTAL_2026-10-28.docx).
- [Dictamen técnico-académico en Word](material_original/DICTAMEN_TECNICO_ACADEMICO_UBELSER_2026-10-28.docx).
- Metadatos de autoría y citación de `CITATION.cff` correspondientes a la release.

La presentación incluida en el paquete se identifica como **BASE**. No debe confundirse con la presentación posterior de 59 diapositivas.

La tesis se conserva como **versión de cierre documental pendiente de aprobación académica**. El DOI identifica y preserva el paquete de software y sus documentos; no constituye una aprobación del jurado ni un depósito institucional de grado de la UNC.

## Verificación del archivo depositado

Se consultó la [API pública del registro](https://zenodo.org/api/records/23748244), se descargó su ZIP y se comprobaron los siguientes datos:

| Comprobación | Resultado |
|---|---|
| Versión declarada | v1.1.1 |
| Tamaño del ZIP | 7 742 535 bytes |
| Entradas del ZIP, incluidos directorios | 102 |
| MD5 publicado por Zenodo y recalculado | `257e496d42b2c7280797f1dec9270a55` |
| SHA-256 recalculado del ZIP | `aa9904f1c936e636417f78a60e426c94c40b98a8de574b5d05a0b2ae17467af4` |
| Tesis, dictamen y CITATION.cff del ZIP | Coinciden exactamente con sus blobs de GitHub en la versión preservada |
| Dashboard y ejecutor científico | Se comprobó la presencia de `dashboard/app.py` y `scripts/run_all.py` |
| Autores y ORCID | Ambos identificadores coinciden con los declarados |
| Referencia histórica v1.0.0 | Conserva el commit `8f175ffef568c25cbaee91a1c04da3f2cc38cdb2` |

El DOI se añadió a la documentación y a `CITATION.cff` de la rama principal después de su emisión. La release archivada conserva su instantánea original.

## Cita sugerida

Tamay, U., & Koo Labrín, C. J. (2026). *Metodología reproducible para el diagnóstico y pronóstico del radioenlace Cuñacales–San José* (v1.1.1) [Software]. Zenodo. https://doi.org/10.5281/zenodo.23748244

## Licencias y alcance científico

El código se distribuye bajo **MIT**, según [LICENSE-CODE](../LICENSE-CODE). Los datos, documentos, tablas y figuras se distribuyen bajo **CC BY 4.0**, según [LICENSE-DATA-DOCS](../LICENSE-DATA-DOCS). El campo de licencia de Zenodo corresponde al software; la descripción del depósito identifica expresamente la licencia de los datos y documentos.

La [auditoría independiente en Linux](reproducibilidad/AUDITORIA_LINUX_EXITOSA_2026-10-28.md) identifica el commit científico efectivamente ejecutado, sus métricas y sus límites. La preservación de v1.1.1 no sustituye esa evidencia por una afirmación de equivalencia en todos los sistemas operativos.

El dashboard es una extensión posterior al estudio. La telemetría reciente obtenida de respaldos se muestra de forma descriptiva y no acredita predicción validada en tiempo real.

## Publicar futuras versiones

1. Mantenga habilitado el repositorio en [Zenodo → GitHub](https://zenodo.org/account/settings/github/).
2. Prepare los cambios y actualice versión, fecha, autores y descripción en `CITATION.cff`.
3. Conserve un único identificador SPDX del código en el campo `license`; describa las licencias de datos y documentos en sus archivos y en el resumen.
4. Valide los metadatos y publique una release nueva con etiqueta propia, sin mover etiquetas anteriores.
5. Verifique en Zenodo el estado publicado, la versión, ambos ORCID y los archivos.
6. Incorpore el DOI de esa versión al README y a la citación. Evite crear depósitos manuales duplicados del mismo paquete.

El [flujo de publicación](../.github/workflows/publicar_zenodo.yml) contiene la versión que publica. Antes de usarlo para una versión posterior, actualice su etiqueta y sus notas. El flujo conserva las releases existentes.

## Incidencia de importación resuelta

El primer intento, **v1.1.0**, fue rechazado con `Citation metadata load failed`. El archivo pasaba la validación estándar CFF, pero contenía una lista en `license`, incompatible con el importador de Zenodo. Esta limitación está [documentada en el repositorio oficial de Zenodo](https://github.com/zenodo/zenodo/issues/2515).

La versión **v1.1.1** utiliza un valor escalar `license: MIT` y explica por separado el alcance de CC BY 4.0. Zenodo la archivó correctamente. La release v1.1.0 se conserva como trazabilidad del intento fallido; el depósito público verificado corresponde a v1.1.1.

Referencias oficiales: [habilitar un repositorio](https://help.zenodo.org/docs/github/enable-repository/), [metadatos CITATION.cff](https://help.zenodo.org/docs/github/describe-software/citation-file/) y [errores de importación](https://support.zenodo.org/help/en-gb/24-github-integration/204-why-does-my-github-release-fail-with-an-error).
