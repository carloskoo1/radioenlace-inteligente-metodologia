# Guía para instalar, ejecutar y verificar el dashboard de la tesis de Ubelser Tamay

**Proyecto:** Sistema inteligente para el radioenlace Cuñacales–San José  
**Repositorio público:** https://github.com/carloskoo1/radioenlace-inteligente-metodologia  
**Propósito de esta guía:** permitir que otra persona, en una computadora distinta, pueda descargar el proyecto, abrir el dashboard y realizar pruebas de reproducción científica de manera documentada.  
**Actualización:** 28 de octubre de 2026.

**IMPORTANTE — se ha comprobado una reproducción integral satisfactoria en Linux/Python 3.12.** Consulte la [auditoría independiente verificada](reproducibilidad/AUDITORIA_LINUX_EXITOSA_2026-10-28.md). Los procedimientos Windows de la sección 7 se conservan para auditar diferencias entre plataformas, no como la vía recomendada para reproducir numéricamente el artículo o la tesis.

> **Lea esta diferencia antes de empezar:** (A) *abrir el dashboard* significa ejecutar la interfaz para examinar **resultados históricos ya calculados**; (B) *reproducir el experimento* significa procesar los datos originales y calcular otra vez los resultados. Que A funcione **no demuestra** que B produzca exactamente las cifras publicadas. La auditoría disponible ha encontrado discrepancias de clasificación y alertas.

## 1. ¿Cuál es el producto de la tesis?

El producto científico original es un **sistema computacional modular de análisis de telemetría de un radioenlace real**. Realiza preparación de datos, construcción de características temporales, clasificación de estados operacionales **proxy**, detección de anomalías, pronósticos a 5, 15 y 30 minutos, comparación con modelos de referencia y explicabilidad. Se ejecuta principalmente por lotes mediante scripts Python.

El **dashboard Streamlit** de la carpeta [dashboard/](../dashboard/) es una **extensión creada después** de la implementación científica para explorar los resultados y facilitar su demostración ante otros investigadores y un jurado. **No realiza adquisición de RF en tiempo real, no envía alertas a los equipos, ni sustituye la validación de fallas de campo.**

La versión científica de referencia se conserva en la etiqueta [v1.0.0](https://github.com/carloskoo1/radioenlace-inteligente-metodologia/releases/tag/v1.0.0). Para utilizar el dashboard se descarga la rama **main**, donde fue añadido después de esa versión.

## 2. Requisitos en otra computadora

En Windows 10/11:

1. Conexión a Internet para descargar el repositorio y las librerías durante la primera instalación.
2. **Python 3.12** (recomendado): https://www.python.org/downloads/ . Si el instalador ofrece **Add Python to PATH**, actívelo.
3. **Git para Windows:** https://git-scm.com/downloads/win .
4. PowerShell o Terminal de Windows y un navegador como Firefox, Chrome o Edge.
5. Espacio libre suficiente para el proyecto, su entorno virtual y las dependencias. La descarga de bibliotecas científicas puede ser considerable.

**Compruebe las instalaciones** abriendo PowerShell y ejecutando:

~~~powershell
py -3.12 --version
git --version
~~~

Deberían mostrarse Python 3.12.x y una versión de Git. Si uno de los comandos no existe, complete su instalación antes de continuar.

## 3. Instalación en Windows, paso a paso

### Paso 3.1 — Descargar una copia limpia

En PowerShell:

~~~powershell
cd $HOME
git clone https://github.com/carloskoo1/radioenlace-inteligente-metodologia.git
cd radioenlace-inteligente-metodologia
~~~

Esto crea una carpeta del proyecto en su perfil de usuario. No copie únicamente la dirección `localhost` que se usa en otra computadora: **localhost es siempre la computadora donde está abierto el navegador**.

Si ya existe esa carpeta, no ejecute `git clone` encima de ella. Utilice otro nombre de destino para una copia nueva:

~~~powershell
cd $HOME
git clone https://github.com/carloskoo1/radioenlace-inteligente-metodologia.git radioenlace-inteligente-dashboard-nuevo
cd radioenlace-inteligente-dashboard-nuevo
~~~

### Paso 3.2 — Método más sencillo: iniciador incluido

Dentro de la carpeta del repositorio, ejecute:

~~~powershell
.\dashboard\iniciar_windows.bat
~~~

Este archivo crea un entorno virtual (si no existe), instala las dependencias del análisis y de Streamlit, y arranca el dashboard. **Mantenga abierta esa ventana**; al cerrarla se detendrá el servidor.

> El iniciador actual revisa e instala dependencias cada vez que se usa; no requiere repetir la instalación manual, pero puede necesitar conexión a Internet. Para un inicio más directo después de haber instalado todo, use el procedimiento del paso 3.3.

### Paso 3.3 — Método manual para mayor control (alternativa al paso 3.2)

Ejecute estos comandos en la carpeta del repositorio:

~~~powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pip install -r dashboard\requirements-dashboard.txt
.\.venv\Scripts\python.exe -m streamlit run dashboard\app.py
~~~

**No hace falta activar el entorno** mediante `Activate.ps1`; aquí se invoca directamente el Python de `.venv`, evitando bloqueos de la política de ejecución de PowerShell.

Cuando Streamlit muestre la dirección local, abra en el navegador:

**http://localhost:8501**

El dashboard contiene ocho pestañas: **Producto**, **Calidad de datos**, **Diagnóstico**, **Pronóstico**, **Alertas**, **Anomalías**, **Explicabilidad** y **Reproducibilidad**.

### Paso 3.4 — Cómo volverlo a iniciar posteriormente

Si ya está instalado, no necesita volver a crear el entorno:

~~~powershell
cd "$HOME\radioenlace-inteligente-metodologia"
.\.venv\Scripts\python.exe -m streamlit run dashboard\app.py
~~~

Si utilizó el nombre alternativo `radioenlace-inteligente-dashboard-nuevo`, reemplace la ruta correspondiente. Deje abierta la ventana de PowerShell mientras use la aplicación. Para detenerla, presione **Ctrl+C** en esa misma ventana.

## 4. Comprobar que está funcionando de verdad

**Verificación visual:** deberían aparecer las ocho pestañas y datos del radioenlace, por ejemplo los conteos de registros en *Producto* y las comparaciones de resultados en *Diagnóstico* y *Pronóstico*.

**Verificación HTTP:** en una segunda ventana de PowerShell (sin cerrar la primera):

~~~powershell
(Invoke-WebRequest -Uri "http://127.0.0.1:8501/_stcore/health" -UseBasicParsing).StatusCode
~~~

Una respuesta **200** indica que el servidor web responde. Puede comprobarse además que la página carga y que no hay errores de ejecución; **200 por sí solo no valida resultados científicos**.

**Lo que se verificó previamente:** en la computadora de trabajo *Research*, el servidor respondió HTTP 200, la aplicación mostró ocho secciones y una prueba de ejecución de la interfaz no reportó excepciones. Esto **no equivale a haber comprobado todas las configuraciones de Windows ni todas las computadoras externas**.

## 5. Problemas frecuentes y sus soluciones

| Síntoma | Causa probable | Qué hacer |
|---|---|---|
| Firefox muestra «No se puede conectar» a `localhost:8501` | Streamlit no está ejecutándose en esa computadora | Vuelva a abrir PowerShell, entre a la carpeta correcta e inicie `python -m streamlit run` como se indica en 3.4. No cierre la ventana. |
| `No module named streamlit` | Se usó otro Python o no se instalaron dependencias | Use `.\.venv\Scripts\python.exe -m pip install -r dashboard\requirements-dashboard.txt` y arranque con ese mismo ejecutable. |
| `dashboard/app.py` no existe | Copia local desactualizada o carpeta incorrecta | Descargue la rama `main` en una carpeta nueva y compruebe que exista `dashboard\app.py`. |
| `py -3.12` no se reconoce | Python 3.12 o su lanzador no está instalado | Instale Python 3.12 y abra una ventana nueva de PowerShell. |
| `git` no se reconoce | Git no está instalado o no está en PATH | Instale Git para Windows y abra otra terminal. |
| El puerto 8501 está ocupado | Otra aplicación está utilizando el puerto | Use `.\.venv\Scripts\python.exe -m streamlit run dashboard\app.py --server.port 8502` y abra `http://localhost:8502`. |
| Error durante `pip install` | Conexión, proxy, permisos o incompatibilidad | Revise el mensaje completo; utilice Python 3.12, el entorno virtual y conexión estable. No ignore un error de instalación. |
| Se abre el dashboard pero faltan algunas visualizaciones | Ciertas salidas detalladas aún no se generaron en esa copia | El dashboard muestra las tablas publicadas; algunas gráficas individuales requieren ejecutar el análisis. **Ejecutarlo puede sobrescribir las tablas locales y revelar las discrepancias documentadas**: hágalo en una copia para auditoría. |

**Seguridad:** no es necesario abrir puertos del router ni desactivar el firewall para usarlo localmente. No exponga esta aplicación a Internet sin revisar sus controles; la función de reejecución del pipeline debe reservarse a entornos confiables.

## 6. ¿Se puede instalar en Linux o macOS?

Sí, siempre que se disponga de Git y un Python compatible (se recomienda 3.12). En una terminal:

~~~bash
git clone https://github.com/carloskoo1/radioenlace-inteligente-metodologia.git
cd radioenlace-inteligente-metodologia
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m pip install -r dashboard/requirements-dashboard.txt
.venv/bin/python -m streamlit run dashboard/app.py
~~~

Abra la URL local que muestre Streamlit. También está disponible `bash dashboard/iniciar_linux_mac.sh` como iniciador. El funcionamiento en Linux/macOS dependerá de la plataforma y las dependencias; una instalación exitosa no debe confundirse con reproducción científica comprobada.

## 7. Reproducir científicamente los resultados (procedimiento separado)

**No ejecute la reproducción en el directorio que usa para exhibir resultados publicados**, porque el análisis vuelve a generar tablas y figuras. Cree una segunda copia para fines de auditoría.

### 7.1 — Copia científica fija v1.0.0

En otra ventana de PowerShell:

~~~powershell
cd $HOME
git clone --branch v1.0.0 --depth 1 https://github.com/carloskoo1/radioenlace-inteligente-metodologia.git ubelser-auditoria-v1
cd ubelser-auditoria-v1
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
~~~

La etiqueta fija permite identificar el código publicado que se intenta reproducir, independientemente de nuevas incorporaciones en la rama `main`.

### 7.2 — Verificar la integridad del archivo de datos

Desde la carpeta `ubelser-auditoria-v1`:

~~~powershell
(Get-FileHash -Algorithm SHA256 "data\raw\Datos.zip").Hash
~~~

El valor esperado es:

~~~text
786A037E749CE0C5BF7B3D8BD66F419A0A76DE809C68857534E03487FC922BFA
~~~

Si no coincide, **detenga la auditoría** y compruebe la descarga: no modifique los datos originales para forzar una coincidencia.

### 7.3 — Recalcular el análisis

~~~powershell
.\.venv\Scripts\python.exe scripts\run_all.py *> reproduccion_ejecucion.log
$LASTEXITCODE
~~~

El comando puede consumir tiempo y recursos de cómputo. El archivo `reproduccion_ejecucion.log` conserva la salida del proceso. **No borre el registro si hay errores**. El valor `0` indica que el programa terminó satisfactoriamente según sus propias comprobaciones; valores diferentes indican que hay que inspeccionar el log.

**Advertencia respaldada por auditorías anteriores:** la reejecución de la versión científica en Windows produjo el mismo número de registros originales, minutos observados y anomalías, y coincidencia de varios pronósticos; sin embargo, **no reprodujo exactamente F1-macro, AUC ni los conteos de alertas**. Por ello, es posible que `run_all.py` termine con error al llegar a `verify_outputs.py`. No oculte ni fuerce el resultado modificando tolerancias.

### 7.4 — Registrar el entorno técnico

Conserve, junto al log:

~~~powershell
.\.venv\Scripts\python.exe --version
.\.venv\Scripts\python.exe -m pip freeze > dependencias_ejecucion.txt
git rev-parse HEAD
~~~

El registro de versión de Python, bibliotecas, sistema operativo, commit, integridad de datos, ejecución y diferencias encontradas permite que otros investigadores auditen el trabajo.

Para ver un análisis **ya realizado** de la discrepancia, consulte [Auditoría de Windows y Python 3.12/3.13](reproducibilidad/AUDITORIA_WINDOWS_PY313_2026-10-28.md).

### 7.5 — Cómo interpretar el resultado sin tergiversarlo

| Control | Hallazgo documentado hasta el 28-10-2026 |
|---|---|
| Archivos de origen | 90 archivos; integridad SHA-256 verificada |
| Registros AP | 173 513; coincidencia |
| Minutos observados | 118 458; coincidencia |
| Anomalías | 1 093; coincidencia |
| Pronósticos de referencia seleccionados | Coincidencia en determinados MAE |
| F1-macro de clasificación | 0,5747978 publicado frente a 0,5787394 recalculado; **no coincide** |
| AUC multiclase | 0,7940374 publicado frente a 0,7967051 recalculado; **no coincide** |
| Verdaderos positivos de alertas | 723 publicados frente a 644 recalculados; **no coincide** |
| Falsos positivos de alertas | 1 742 publicados frente a 1 327 recalculados; **no coincide** |

**La reproducibilidad numérica integral fue comprobada en el entorno Linux/Python 3.12 indicado en la auditoría independiente. La equivalencia numérica en Windows nativo no está demostrada.** La causa de las discrepancias del clasificador sigue bajo investigación. No atribuirla automáticamente a Python, a los hilos del procesador o al sistema operativo sin evidencia.

El repositorio principal contiene además [scripts/auditar_reproduccion.py](../scripts/auditar_reproduccion.py) (agregado después de `v1.0.0`) para comparar resultados recalculados con la referencia publicada. No se encuentra dentro de la etiqueta científica antigua. Si se utiliza, debe ejecutarse en una copia de auditoría que incluya ese script y conservar explícitamente qué versión de código y datos se evaluó.

## 8. Buenas prácticas y límites para reutilizar esta investigación

- La evaluación se hizo con telemetría del radioenlace **Cuñacales–San José**. No representa automáticamente todos los radioenlaces.
- Los estados «normal», «degradado» y «crítico» proceden de **reglas proxy**; no están confirmados mediante una bitácora completa de fallas reales.
- `rate_dl_mbps` es la **tasa negociada que reporta el equipo**, no throughput efectivo de usuario.
- Los resultados de las asociaciones radio–clima son exploratorios y no prueban causalidad.
- Mantenga separaciones cronológicas y transformaciones entrenadas exclusivamente con datos anteriores a la prueba.
- No publique direcciones externas, contraseñas ni archivos de configuración sensibles que pudieran aparecer en sus copias locales.
- Cite el proyecto según [CITATION.cff](../CITATION.cff) y las licencias publicadas.

## 9. Estructura útil del repositorio

| Ruta | Qué encontrará |
|---|---|
| [`dashboard/app.py`](../dashboard/app.py) | Interfaz interactiva Streamlit |
| [`dashboard/iniciar_windows.bat`](../dashboard/iniciar_windows.bat) | Iniciador Windows |
| [`scripts/run_all.py`](../scripts/run_all.py) | Secuencia de reproducción |
| [`scripts/verify_outputs.py`](../scripts/verify_outputs.py) | Verificador básico del flujo |
| [`src/radioenlace/`](../src/radioenlace/) | Implementación computacional |
| [`config/analysis.yml`](../config/analysis.yml) | Parámetros del experimento |
| [`data/raw/Datos.zip`](../data/raw/Datos.zip) | Archivo de datos originales |
| [`results/tables/`](../results/tables/) | Tablas de resultados publicadas |
| [`results/figures/`](../results/figures/) | Figuras publicadas |
| [`docs/instrumentos/`](instrumentos/) | Fichas de registro y evaluación |
| [`docs/reproducibilidad/`](reproducibilidad/) | Auditorías y criterios de comparación |

---

**Si usted es un investigador externo:** primero complete las secciones **2 a 4** para comprobar que el dashboard puede instalarse y abrirse. Después, si desea comprobar el artículo o la tesis científicamente, realice por separado la sección **7** y documente tanto las coincidencias como las discrepancias. Conservar hallazgos discordantes es parte de la transparencia científica.
