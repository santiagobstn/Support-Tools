@echo off
title Build - Support Tools
color 0A

echo ===========================================
echo        BUILD DO SUPPORT TOOLS
echo ===========================================
echo.

REM Navega para a pasta do script
cd /d "%~dp0"

REM Limpa pastas antigas
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist __pycache__ rmdir /s /q __pycache__

echo Limpando builds antigos... OK
echo.

REM Gera o executável
echo Gerando executável...
pyinstaller ^
 --onefile ^
 --noconsole ^
 --clean ^
 --icon=icons\icon.ico ^
 --name "Support_Tools" ^
 main.py

echo.
echo ===========================================
echo       BUILD FINALIZADA COM SUCESSO
echo ===========================================
echo Executável gerado em: dist\Support_Tools.exe
echo.

REM Abre a pasta dist no Explorer
explorer dist

pause
