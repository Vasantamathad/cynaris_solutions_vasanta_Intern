@echo off
title Deploy to Vercel - TradeSight Export Analytics
cd /d "c:\CYNARIS PROJECT"
echo ========================================================
echo   Deploying TradeSight Project to Vercel...
echo ========================================================
echo.
echo If prompted, log in with GitHub in the browser window.
echo.
npx vercel --prod
pause
