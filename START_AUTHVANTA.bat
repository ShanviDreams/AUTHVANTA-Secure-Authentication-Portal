@echo off
cd /d "%~dp0"
start "AUTHVANTA Server" cmd /k "cd /d "%~dp0" && venv\Scripts\python.exe run.py"
timeout /t 3 /nobreak >nul
start "CodeArena Demo" cmd /k "cd /d "%~dp0" && venv\Scripts\python.exe codearena\app.py"
timeout /t 3 /nobreak >nul
start "" http://127.0.0.1:5001
