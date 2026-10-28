# Integración GitHub–Zenodo y DOI del software científico

**Repositorio:** [carloskoo1/radioenlace-inteligente-metodologia](https://github.com/carloskoo1/radioenlace-inteligente-metodologia)  
**Estado al 28/10/2026:** tesis de cierre y dictamen publicados en GitHub; **DOI de Zenodo aún no emitido**. No sustituya este texto por un DOI de otro proyecto.

## Enlace para activar la preservación

Abra su sesión de Zenodo en Research:

**[Configurar GitHub en Zenodo](https://zenodo.org/account/settings/github/)**.

Se verificó que la cuenta Zenodo ya estaba vinculada a GitHub, pero solo mostraba otro repositorio habilitado. Para este proyecto:

1. En Zenodo, abra **Perfil → GitHub**.
2. Pulse **Sync now** para refrescar el listado.
3. Localice **carloskoo1/radioenlace-inteligente-metodologia** y active su interruptor.
4. Si el repositorio no aparece, abra los permisos de la aplicación Zenodo en GitHub, autorice **únicamente ese repositorio** y regrese a **Sync now**. No necesita conceder acceso general a otros repositorios.
5. **Después** de activar el repositorio, publique una **nueva release** de GitHub con un número de versión nuevo (no reetiquete ni altere el release científico `v1.0.0`).
6. Espere a que Zenodo archive la release, registre el DOI y genere su ficha. Copie el DOI exacto desde Zenodo a este documento y al README del repositorio.

**No cree una release nueva antes de conectar el repositorio** si espera que sea archivada automáticamente: Zenodo no realiza siempre una ingesta retroactiva de releases anteriores. La integración está documentada por [Zenodo](https://help.zenodo.org/docs/github/enable-repository/).

## Metadatos sugeridos para el archivo de software

- **Tipo:** Software.
- **Título:** Metodología reproducible para el diagnóstico y pronóstico del radioenlace Cuñacales–San José.
- **Autores:** Ubelser Tamay; Carlos Jesús Koo Labrín (según `CITATION.cff`).
- **Afiliación:** Universidad Nacional de Cajamarca, Perú.
- **Descripción:** Código, protocolos, datos, resultados y documentos complementarios para análisis temporal de telemetría RF de un radioenlace rural altoandino, con clasificación de estados operacionales proxy, detección de anomalías, pronóstico a 5, 15 y 30 minutos y evaluación temporal reproducida en Ubuntu/Python 3.12 sobre un commit controlado.
- **Palabras clave:** rural wireless link; telemetry; machine learning; temporal validation; reproducibility; Andes; Peru.
- **Licencia:** MIT para el código; CC BY 4.0 para datos y documentos, según los ficheros de licencia. Si el depósito incluye ambos tipos, revisar sus condiciones por archivo.
- **Relación:** enlace a GitHub y a la tesis de Ubelser, identificada como versión documental de cierre pendiente de aprobación académica.

## Precauciones antes de asignar DOI

El release histórico `v1.0.0` permanece inmutable. La ejecución independiente que reprodujo los resultados principales en Linux utilizó un **commit candidato** con una diferencia de ejecución documentada en la etapa de explicabilidad, no debe describirse como un clon byte a byte de `v1.0.0`.

La tesis completa no debe denominarse «aprobada», «sustentada» o «publicación institucional» mientras no exista conformidad de la UNC. El dashboard posterior de AtmosLink no demuestra inferencia de fallas en tiempo real.

**Enlace persistente DOI:** pendiente de confirmación por Zenodo.  
**Ficha Zenodo:** pendiente de publicación y verificación.

Cuando se obtenga el DOI, actualizar este archivo y la sección de citación del README sin inventar metadatos.
