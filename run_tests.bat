@echo off
REM One command setup + run (Windows).
REM   run_tests.bat              run everyone's tests
REM   run_tests.bat jasmine      run only tests\jasmine
cd /d "%~dp0"

if not exist ".venv" (
  echo Creating .venv ...
  python -m venv .venv
)
call .venv\Scripts\activate.bat
pip install -q -r requirements.txt

set TARGET=tests
if not "%~1"=="" if exist "tests\%~1" set TARGET=tests\%~1

pytest %TARGET% --html=report.html --self-contained-html
echo.
echo Screenshots: screenshots\    HTML report: report.html
