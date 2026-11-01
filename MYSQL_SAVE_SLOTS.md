# Ranuras de guardado MySQL

El juego incluye tres ranuras por jugador. Desde **Ajustes > Partidas guardadas**:

- En el menu principal, **Cargar** inicia la partida guardada.
- Con el juego pausado, **Guardar** sobrescribe la ranura elegida.
- Se conservan las zonas completadas, la vida, las pociones, los cofres abiertos y los niveles de mejoras.

## Preparar MySQL

1. Instala el conector en el entorno del juego:

   ```powershell
   .\.venv\Scripts\python.exe -m pip install -r .\requirements-mysql.txt
   ```

2. Crea/selecciona la base de datos y ejecuta el contenido de `mysql_schema.sql`.
3. Configura estas variables de entorno antes de ejecutar el juego:

   - `PRISION_DB_HOST`
   - `PRISION_DB_PORT` (opcional; por defecto `3306`)
   - `PRISION_DB_USER`
   - `PRISION_DB_PASSWORD`
   - `PRISION_DB_NAME`
   - `PRISION_PLAYER_ID` (opcional; por defecto `jugador_local`)

Si MySQL no esta configurado o no se puede conectar, la pantalla de ranuras muestra el error y no finge que el guardado tuvo exito. El juego puede seguir iniciando una partida nueva sin MySQL.

La conexion directa desde el juego es apropiada solo para desarrollo local. No incluyas credenciales de MySQL en una version distribuida del juego: para publicarlo, la base debe estar detras de un servidor/API autenticado.
