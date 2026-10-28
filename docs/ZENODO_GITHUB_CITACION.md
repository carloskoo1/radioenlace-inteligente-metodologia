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
- **Autores, en orden de citación, con sus identificadores ORCID:**
  1. **Ubelser Tamay** — [0009-0007-2020-2338](https://orcid.org/0009-0007-2020-2338).
  2. **Carlos Jesús Koo Labrín** — [0000-0002-0323-2961](https://orcid.org/0000-0002-0323-2961).
- **Archivo fuente de autoría:** [`CITATION.cff`](../CITATION.cff), con los ORCID y la afiliación de la Universidad Nacional de Cajamarca. La integración de Zenodo admite esta sintaxis sin añadir `.zenodo.json`.
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

## Verificación de los autores antes de publicar

Comprobar que Zenodo importe en este orden a **Ubelser Tamay (ORCID 0009-0007-2020-2338)** y **Carlos Jesús Koo Labrín (ORCID 0000-0002-0323-2961)**. Si no aparecen automáticamente en el depósito, corregir los creadores **antes** de publicar. El DOI **todavía está pendiente** y no se genera por disponer de ORCID.

**Elección de metadatos:** Zenodo admite `CITATION.cff` y `.zenodo.json`, pero en presencia de ambos utiliza solo `.zenodo.json`; por ello, para este repositorio mantenemos un único origen autoritativo de los metadatos de software en `CITATION.cff`. Consulte [la documentación oficial de Zenodo](https://help.zenodo.org/docs/github/describe-software/citation-file/).

## Solución si Zenodo confirma «Repositories synced successfully» pero la lista sigue vacía

En la comprobación del 28 de octubre de 2026, Zenodo mostraba únicamente `carloskoo1/mimo-radio-link-telemetry-analysis` como repositorio habilitado y no listaba `carloskoo1/radioenlace-inteligente-metodologia` en **Repositories**, incluso después de sincronizar. El repositorio de Ubelser **sí existe, es público y la cuenta tiene permisos de administrador**; esto descarta que esté borrado o que sea privado, pero no determina por sí solo la causa de la omisión.

1. **Sin desactivar el repositorio ya archivado**, pulse `Sync now`, espere a que concluya y recargue la página completa. Confirme que ingresó con la cuenta correcta de GitHub.
2. Revise en GitHub [Settings → Applications → Authorized OAuth Apps](https://github.com/settings/applications) la autorización de **Zenodo** y los permisos vigentes. La documentación de GitHub explica cómo revisar aplicaciones autorizadas: https://docs.github.com/en/apps/oauth-apps/using-oauth-apps/reviewing-your-authorized-oauth-apps .
3. Si GitHub ofrece opciones para autorizar o actualizar permisos de Zenodo, revise el alcance y apruebe **solo lo necesario**; una reautorización o revocación no debe hacerse automáticamente porque podría interrumpir el archivo de otros repositorios.
4. Retorne a https://zenodo.org/account/settings/github/ y vuelva a pulsar `Sync now`. Si no aparece, contacte con soporte Zenodo y adjunte el nombre exacto del repositorio y la captura; no invente un DOI.
5. Como alternativa, Zenodo también permite crear **un depósito manual** del paquete científico, con un DOI distinto del que emitiría la integración GitHub. No publique dos depósitos del mismo artefacto sin establecer una política de versiones y relaciones entre identificadores.

**Estado documentado:** sincronización solicitada; repositorio de Ubelser aún no habilitado en Zenodo; DOI pendiente.

