# Mi_primer_repositorio

## Senderos de Luz (versión web)

`index.html` contiene un juego narrativo inspirado en la Biblia pensado para niños, adultos y ancianos. Permite:

- Elegir el nombre, grupo de edad y modo de acompañamiento (cuento, estrategia o reflexión).
- Recorrer caminos temáticos con preguntas interactivas y Puertas de Sabiduría.
- Ganar gemas, virtudes y recuerdos, así como registrar testimonios personales.
- Activar misiones comunitarias para compartir lo aprendido con otras personas.

### Cómo jugar
1. Abre una terminal y entra en la carpeta del repositorio:
   ```bash
   cd /home/andrea/Mi_primer_repositorio
   ```
2. Inicia un servidor sencillo para abrir el juego en tu navegador (opcional pero recomendado):
   ```bash
   python3 -m http.server 8000
   ```
3. Abre tu navegador y visita `http://localhost:8000/index.html`.  
   Si prefieres no usar servidor, también puedes abrir `index.html` directamente haciendo doble clic desde tu explorador de archivos.

### Cómo guardar los cambios en GitHub
1. Revisa qué archivos cambiaste:
   ```bash
   git status
   ```
2. Añade los archivos nuevos o modificados al historial:
   ```bash
   git add index.html README.md senderos_de_luz.py
   ```
   > Ajusta la lista si solo quieres subir algunos archivos.
3. Crea un mensaje de confirmación (commit) describiendo el cambio:
   ```bash
   git commit -m "Agregar versión web de Senderos de Luz"
   ```
4. Sube tus cambios a GitHub:
   ```bash
   git push
   ```
5. Ve a tu repositorio en la web de GitHub para confirmar que los archivos están allí.

Si es la primera vez que conectas este repositorio con GitHub, asegúrate de haber configurado el control remoto con:
```bash
git remote add origin https://github.com/tu-usuario/Mi_primer_repositorio.git
```
y luego ejecuta `git push -u origin main` (reemplaza `main` por el nombre de tu rama si es distinto).
