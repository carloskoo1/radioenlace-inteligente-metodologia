@echo off
setlocal
cd /d "%~dp0.."
if not exist .venv\Scripts\python.exe (
  py -3.12 -m venv .venv
  if errorlevel 1 python -m venv .venv
)
.venv\Scripts\python.exe -m pip install -r requirements.txt
if errorlevel 1 goto :error
.venv\Scripts\python.exe -m pip install -r dashboard\requirements-dashboard.txt
if errorlevel 1 goto :error
echo Iniciando dashboard local... No es una aplicacion de telemetria en vivo.
.venv\Scripts\python.exe -m streamlit run dashboard\app.py
exit /b %errorlevel%
:error
echo Error de instalacion. Revise Python, la conexion y el archivo requirements.txt.
pause
exit /b 1
