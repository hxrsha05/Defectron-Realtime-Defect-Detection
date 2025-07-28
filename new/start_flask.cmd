@echo off
cd /d %~dp0
call venv\Scripts\activate.bat
pip install requirements.txt
set FLASK_APP=main.py
flask run
pause
