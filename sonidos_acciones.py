import os

import pygame


# Nombres de los recursos de audio por acción; una cadena vacía deja esa acción sin sonido.
SONIDO_PASOS_CAMINAR = "pasos_caminar.wav"
SONIDO_PASOS_CORRER = "pasos_correr.wav"
SONIDO_SALTO = "salto.wav"
SONIDO_ATERRIZAJE = "aterrizaje.wav"
SONIDO_RODAR = ""
SONIDO_ATAQUE_ESPADA = "ataque_espada.wav"
SONIDO_ATAQUE_EMBESTIDA = "ataque_embestida.wav"
SONIDO_ATAQUE_AEREO = ""
SONIDO_ATAQUE_GIRO = ""
SONIDO_GOLPE_ENEMIGO = "golpe_enemigo.wav"
SONIDO_DERROTA_ENEMIGO = "derrota_enemigo.wav"
SONIDO_DANO_JUGADOR = "golpe_PERSONAJE- copia.wav"
SONIDO_DERROTA_JUGADOR = "derrota_jugador.wav"
SONIDO_PERDER_PARTIDA = ""
SONIDO_VICTORIA = "victoria.wav"
SONIDO_CURACION_POCION = "curacion_pocion.wav"
SONIDO_ABRIR_COFRE = "abrir_cofre.wav"
SONIDO_RECOGER_POCION = "recoger_pocion.wav"
SONIDO_ACTIVAR_BERSERKER = "activar_berserker.wav"
SONIDO_ATAQUE_ENEMIGO_CUERPO = "ataque_enemigo_cuerpo.wav"
SONIDO_ATAQUE_ENEMIGO_DISTANCIA = "ataque_enemigo_distancia.wav"
SONIDO_ATAQUE_JEFE = "ataque_jefe.wav"
SONIDO_INICIO_OLEADA = "inicio_oleada.wav"
SONIDO_COMPLETAR_OLEADA = ""

# Relaciona claves lógicas usadas por el juego con los nombres de archivo configurables.
ARCHIVOS_SONIDO = {
    "pasos_caminar": SONIDO_PASOS_CAMINAR,
    "pasos_correr": SONIDO_PASOS_CORRER,
    "salto": SONIDO_SALTO,
    "aterrizaje": SONIDO_ATERRIZAJE,
    "rodar": SONIDO_RODAR,
    "ataque_espada": SONIDO_ATAQUE_ESPADA,
    "ataque_embestida": SONIDO_ATAQUE_EMBESTIDA,
    "ataque_aereo": SONIDO_ATAQUE_AEREO,
    "ataque_giro": SONIDO_ATAQUE_GIRO,
    "golpe_enemigo": SONIDO_GOLPE_ENEMIGO,
    "derrota_enemigo": SONIDO_DERROTA_ENEMIGO,
    "dano_jugador": SONIDO_DANO_JUGADOR,
    "derrota_jugador": SONIDO_DERROTA_JUGADOR,
    "perder_partida": SONIDO_PERDER_PARTIDA,
    "victoria": SONIDO_VICTORIA,
    "curacion_pocion": SONIDO_CURACION_POCION,
    "abrir_cofre": SONIDO_ABRIR_COFRE,
    "recoger_pocion": SONIDO_RECOGER_POCION,
    "activar_berserker": SONIDO_ACTIVAR_BERSERKER,
    "ataque_enemigo_cuerpo": SONIDO_ATAQUE_ENEMIGO_CUERPO,
    "ataque_enemigo_distancia": SONIDO_ATAQUE_ENEMIGO_DISTANCIA,
    "ataque_jefe": SONIDO_ATAQUE_JEFE,
    "inicio_oleada": SONIDO_INICIO_OLEADA,
    "completar_oleada": SONIDO_COMPLETAR_OLEADA,
}


class AudioAcciones:
    # Carga efectos, administra sus canales y controla reproducción, bucles y pausas.
    def __init__(self, carpeta, archivos=None):
        self.carpeta = carpeta
        self.archivos = dict(ARCHIVOS_SONIDO if archivos is None else archivos)
        self.sonidos = {}
        self.canales = {}
        self.canales_pausados = set()
        self.errores = {}

    # Reinicia el estado y carga únicamente los recursos configurados, registrando errores.
    def cargar(self):
        self.sonidos.clear()
        self.canales.clear()
        self.canales_pausados.clear()
        self.errores.clear()
        configurados = {nombre: archivo for nombre, archivo in self.archivos.items() if archivo}
        if not configurados:
            return
        if not pygame.mixer.get_init():
            self.errores["audio"] = "El mezclador de audio de Pygame no esta disponible."
            print("Aviso de audio: " + self.errores["audio"])
            return
        for nombre, archivo in configurados.items():
            ruta = archivo if os.path.isabs(archivo) else os.path.join(self.carpeta, archivo)
            try:
                if not os.path.isfile(ruta):
                    raise FileNotFoundError(f"No existe el archivo: {ruta}")
                self.sonidos[nombre] = pygame.mixer.Sound(ruta)
            except (FileNotFoundError, pygame.error) as error:
                self.errores[nombre] = str(error)
                print(f"Aviso de audio ({nombre}): {error}")

    # Reproduce un efecto único; puede bloquearse por otros sonidos o reemplazar sonidos activos.
    def reproducir(
        self, nombre, volumen=1.0, bloquear_si_activo=(), reemplazar=(), loops=0
    ):
        sonido = self.sonidos.get(nombre)
        if sonido is None or not pygame.mixer.get_init():
            return False
        if any(
            self.sonidos.get(nombre_bloqueo)
            and self.sonidos[nombre_bloqueo].get_num_channels() > 0
            for nombre_bloqueo in bloquear_si_activo
        ):
            return False
        for nombre_anterior in reemplazar:
            self.detener(nombre_anterior)
        sonido.set_volume(max(0.0, min(1.0, float(volumen))))
        canal = sonido.play(loops=loops)
        if canal is not None:
            self.canales[nombre] = canal
            self.canales_pausados.discard(nombre)
        return True

    # Mantiene una reproducción en bucle sin crear canales duplicados para el mismo efecto.
    def reproducir_bucle(self, nombre, volumen=1.0, reemplazar=()):
        sonido = self.sonidos.get(nombre)
        if sonido is None or not pygame.mixer.get_init():
            return False
        canal = self.canales.get(nombre)
        if (
            canal is not None
            and canal.get_sound() is sonido
            and canal.get_busy()
        ):
            sonido.set_volume(max(0.0, min(1.0, float(volumen))))
            return True
        return self.reproducir(
            nombre, volumen, reemplazar=reemplazar, loops=-1
        )

    # Detiene y olvida los canales asociados a los sonidos indicados.
    def detener(self, *nombres):
        for nombre in nombres:
            canal = self.canales.pop(nombre, None)
            self.canales_pausados.discard(nombre)
            sonido = self.sonidos.get(nombre)
            if sonido is None:
                continue
            if canal is not None and canal.get_sound() is sonido:
                canal.stop()
            else:
                sonido.stop()

    # Pausa solo canales activos que todavía corresponden al efecto solicitado.
    def pausar(self, *nombres):
        for nombre in nombres:
            canal = self.canales.get(nombre)
            if (
                canal is not None
                and canal.get_sound() is self.sonidos.get(nombre)
                and canal.get_busy()
                and nombre not in self.canales_pausados
            ):
                canal.pause()
                self.canales_pausados.add(nombre)

    # Reanuda los canales pausados y limpia su marca de pausa.
    def reanudar(self, *nombres):
        for nombre in nombres:
            canal = self.canales.get(nombre)
            if canal is None or nombre not in self.canales_pausados:
                continue
            if canal.get_sound() is self.sonidos.get(nombre):
                canal.unpause()
            self.canales_pausados.discard(nombre)
