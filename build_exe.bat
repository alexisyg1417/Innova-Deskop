@echo off
cd /d "%~dp0"
echo Instalando/actualizando PyInstaller...
python -m pip install --upgrade pyinstaller
if errorlevel 1 goto :error

echo.
echo Generando INNOVA Desktop.exe...
python -m PyInstaller --noconfirm --clean --onefile --windowed --name "INNOVA Desktop" app.py
if errorlevel 1 goto :error

echo.
echo Listo. El ejecutable esta en: dist\INNOVA Desktop.exe
pause
exit /b 0

:error
echo.
echo Ocurrio un error durante la compilacion.
pause
exit /b 1
