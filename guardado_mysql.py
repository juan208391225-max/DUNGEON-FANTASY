import json
import os


# Error de configuración explícito para que la interfaz distinga fallos de conexión
# de los casos en los que faltan datos de acceso o la dependencia MySQL.
class ConfiguracionMySQLError(RuntimeError):
    pass


class MySQLSaveSlots:
    # Abstrae la conexión y las operaciones de consulta/guardado de las ranuras.
    def __init__(self, configuracion=None, connector=None):
        self.configuracion = configuracion or {
            "host": os.getenv("PRISION_DB_HOST", ""),
            "port": os.getenv("PRISION_DB_PORT", "3306"),
            "user": os.getenv("PRISION_DB_USER", ""),
            "password": os.getenv("PRISION_DB_PASSWORD", ""),
            "database": os.getenv("PRISION_DB_NAME", ""),
            "player_id": os.getenv("PRISION_PLAYER_ID", "jugador_local"),
        }
        self.connector = connector

    # Valida ajustes y crea la conexión usando la dependencia inyectada o el conector real.
    def _connect(self):
        requeridos = ("host", "user", "password", "database")
        faltantes = [clave for clave in requeridos if not self.configuracion.get(clave)]
        if faltantes:
            raise ConfiguracionMySQLError(
                "Configura las variables PRISION_DB_HOST, PRISION_DB_USER, "
                "PRISION_DB_PASSWORD y PRISION_DB_NAME."
            )
        connector = self.connector
        if connector is None:
            try:
                import mysql.connector
            except ImportError as error:
                raise ConfiguracionMySQLError(
                    "Falta mysql-connector-python. Instala las dependencias de requirements-mysql.txt."
                ) from error
            connector = mysql.connector
        return connector.connect(
            host=self.configuracion["host"],
            port=int(self.configuracion["port"]),
            user=self.configuracion["user"],
            password=self.configuracion["password"],
            database=self.configuracion["database"],
            connection_timeout=5,
        )

    # Devuelve las ranuras del jugador, decodificando su carga JSON cuando sea necesario.
    def listar(self):
        conexion = self._connect()
        cursor = None
        try:
            cursor = conexion.cursor()
            cursor.execute(
                "SELECT slot_number, payload, updated_at "
                "FROM save_slots WHERE player_id = %s ORDER BY slot_number",
                (self.configuracion["player_id"],),
            )
            return [
                {
                    "slot": fila[0],
                    "payload": json.loads(fila[1]) if isinstance(fila[1], str) else fila[1],
                    "updated_at": str(fila[2]),
                }
                for fila in cursor.fetchall()
            ]
        finally:
            if cursor is not None:
                cursor.close()
            conexion.close()

    # Inserta o reemplaza el progreso de una ranura permitida y confirma la transacción.
    def guardar(self, ranura, progreso):
        if ranura not in (1, 2, 3):
            raise ValueError("La ranura debe ser 1, 2 o 3.")
        conexion = self._connect()
        cursor = None
        try:
            cursor = conexion.cursor()
            cursor.execute(
                "INSERT INTO save_slots (player_id, slot_number, payload) "
                "VALUES (%s, %s, %s) "
                "ON DUPLICATE KEY UPDATE payload = VALUES(payload), "
                "updated_at = CURRENT_TIMESTAMP",
                (
                    self.configuracion["player_id"],
                    ranura,
                    json.dumps(progreso, ensure_ascii=False),
                ),
            )
            conexion.commit()
        finally:
            if cursor is not None:
                cursor.close()
            conexion.close()
