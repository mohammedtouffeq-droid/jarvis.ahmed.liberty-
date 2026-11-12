@echo off
title J.A.R.V.I.S. Liberty // Boss Ahmed
color 0b
cd /d "%~dp0"
echo ⚡ Initializing J.A.R.V.I.S. Tactical Aerospace Engine...
start "" "http://localhost:7777"
python server.py
pause
