@echo off
title Build Support Tools

echo Limpando build antigo...
rmdir /s /q build
rmdir /s /q dist

echo.
echo Gerando executavel Support Tools...
pyinstaller --onefile --noconsole --icon=icons\icon.ico main.py

echo.
echo Renomeando executavel...
rename "dist\main.exe" "Support_Tools.exe"

echo.
echo Build finalizada com sucesso!
echo O executavel esta em: dist\Support_Tools.exe

explorer dist
pause
