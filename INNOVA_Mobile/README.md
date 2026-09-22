# INNOVA Mobile

Prototipo de aplicación móvil inmobiliaria desarrollado con **Flutter y Dart** para el Subproducto No. 4.

## Funciones incluidas
- Inicio con propiedades destacadas.
- Catálogo con búsqueda y filtros de Venta/Renta.
- Vista de detalle de propiedad.
- Favoritos durante la sesión.
- Agenda de visitas.
- Acción para acceder al perfil del vendedor.
- Navegación inferior adaptada a teléfono.

## Ejecutar en Windows
1. Instala **Flutter** y **Android Studio**.
2. Configura un emulador Android o conecta un teléfono con depuración USB.
3. Abre esta carpeta.
4. Ejecuta `setup_and_run.bat`.

El archivo genera automáticamente las carpetas de plataforma Android si todavía no existen y después ejecuta `flutter run`.

## Generar APK
Después de haber ejecutado la aplicación al menos una vez, usa:

`build_apk.bat`

El APK se genera normalmente en:

`build\app\outputs\flutter-apk\app-release.apk`

## Comandos manuales

```bash
flutter create . --platforms=android
flutter pub get
flutter run
flutter build apk --release
```

## Repositorio sugerido
https://github.com/alexisyg1417/Innova-Mobile
