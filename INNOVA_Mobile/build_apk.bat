@echo off
where flutter >nul 2>nul
if errorlevel 1 (
  echo Flutter no fue encontrado. Instala Flutter y agregalo al PATH.
  pause
  exit /b 1
)
if not exist android (
  echo Ejecuta setup_and_run.bat primero para generar el proyecto Android.
  pause
  exit /b 1
)
flutter pub get
flutter build apk --release
if errorlevel 1 (
  echo Ocurrio un error al generar el APK.
) else (
  echo APK generado en build\app\outputs\flutter-apk\app-release.apk
)
pause
