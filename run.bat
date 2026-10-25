@echo off
cd /d "%~dp0"
echo Installing dependencies if needed...
python -m pip install -r requirements.txt
cd src
echo Starting Weather Dashboard...
python main.py
pause
