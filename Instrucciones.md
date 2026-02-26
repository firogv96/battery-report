# Monitor de Salud de Batería (Windows)

¡Hola! He creado la aplicación basada en Python con una interfaz gráfica moderna, simple y agradable (usando la librería `customtkinter`) que cumple con todo lo solicitado.

## Funcionalidades

- **Salud de la Batería**: Calculada dividiendo la capacidad de carga máxima actual entre la capacidad de diseño original. Se muestra un porcentaje y una barra de progreso que cambia de color según el nivel de salud (verde, naranja o rojo).
- **Ciclos de Carga**: Lee directamente la cantidad de veces que la batería ha completado un ciclo de carga.
- **Reducción de Capacidad**: Muestra cuántos `mWh` (milivatios-hora) se han perdido en comparación a cuando la batería era nueva.
- **Botón de Información**: Un modal rápido que te muestra información sobre la versión actual (v1.1.0) y la información de contacto del desarrollador Firo.

## ¿Cómo funciona?

Internamente, la aplicación utiliza el comando nativo de Windows:
`powercfg /batteryreport /xml`
Esto genera un archivo temporal del cual extraemos los valores exactos registrados por el sistema operativo, garantizando máxima precisión.

## Archivos Generados

1. **`app.py`**: El código fuente en Python de la aplicación.
2. **`dist/Salud de Batería Windows v1.2.0.exe`**: El archivo **Ejecutable (.exe)**. Tiene el ícono de batería incorporado. Puedes usar este archivo sin necesidad de instalar Python; simplemente haz doble clic sobre él y funcionará de manera independiente.
3. **`battery_report.xml`**: Archivo temporal creado por la aplicación para leer la información. (Puedes ignorarlo o borrarlo).

## ¿Cómo probarla?

Dirígete a la carpeta `dist/` en tu proyecto (`d:\Mis cosas\Utilidad Battery Report\win-battery-report\dist\`) y ejecuta el archivo **`Salud de Batería Windows v1.2.0.exe`**.

Si deseas modificar el código fuente `app.py`, puedes volver a generar el ejecutable abriendo la terminal en la raíz y ejecutando:
`pyinstaller --noconfirm --windowed --onefile --icon="D:\Mis cosas\Utilidad Battery Report\battery.ico" --name="Salud de Batería Windows v1.2.0" app.py`

¡Espero que sea exactamente lo que buscas!
