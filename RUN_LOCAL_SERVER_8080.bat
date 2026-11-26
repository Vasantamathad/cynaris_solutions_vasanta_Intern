@echo off
title TradeSight Local Web Server (Port 8080)
cd /d "c:\CYNARIS PROJECT"
echo ========================================================
echo   Starting TradeSight Web Server on Port 8080...
echo   Dashboard URL: http://localhost:8080
echo ========================================================
start http://localhost:8080
python -m http.server 8080
pause
