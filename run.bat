@echo off
set PYTHON_SCRIPT="D:\PyQt Projects\Admin Controller\main.py"

echo Running script as Administrator...
powershell -Command "Start-Process cmd -ArgumentList '/c py -3 %PYTHON_SCRIPT%' -Verb RunAs"
