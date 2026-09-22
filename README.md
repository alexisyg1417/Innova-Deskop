# INNOVA Desktop

Aplicación de escritorio de demostración para la administración inmobiliaria de INNOVA.

## Funciones
- Panel con indicadores del inventario.
- Consulta, búsqueda y filtrado de propiedades.
- Registro de nuevas propiedades.
- Cambio de estado: disponible, en proceso o vendida.
- Agenda de citas con clientes.
- Confirmación, seguimiento y cancelación de citas.
- Persistencia local con SQLite.

## Ejecutar en Windows
1. Instala Python 3 desde python.org si aún no lo tienes.
2. Abre esta carpeta y ejecuta `run.bat`.
3. También puedes ejecutar `python app.py` desde PowerShell.

No requiere paquetes externos: usa Tkinter y SQLite incluidos con la instalación estándar de Python en Windows.

## Empaquetar como .exe (opcional)
En Windows:

```powershell
pip install pyinstaller
pyinstaller --onefile --windowed --name "INNOVA Desktop" app.py
```

El ejecutable aparecerá en la carpeta `dist`.
