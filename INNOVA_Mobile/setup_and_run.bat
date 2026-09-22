@echo off
where flutter >nul 2>nul
if errorlevel 1 (
  echo Flutter no fue encontrado. Instala Flutter y agregalo al PATH.
  echo Guia: https://docs.flutter.dev/get-started/install/windows/mobile
  pause
  exit /b 1
)

if not exist android (
  echo Generando archivos de plataforma Android...
  copy /Y lib\main.dart main_backup.dart >nul
  copy /Y pubspec.yaml pubspec_backup.yaml >nul
  flutter create . --platforms=android
  copy /Y main_backup.dart lib\main.dart >nul
  copy /Y pubspec_backup.yaml pubspec.yaml >nul
  del main_backup.dart
  del pubspec_backup.yaml
)

flutter pub get
flutter run
pause
