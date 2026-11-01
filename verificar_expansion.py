import os
import math
import runpy
import sys
import tempfile
import unittest
import json
from unittest.mock import patch

# Ejecuta las pruebas de integración con controladores de audio/vídeo simulados
# para que la suite no requiera abrir una ventana ni conectarse a MySQL.
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import pygame


# Importa el módulo del juego interceptando el cierre y el evento de salida de Pygame.
def cargar_juego_sin_ventana():
    obtener_eventos = pygame.event.get
    cerrar_pygame = pygame.quit
    salir = sys.exit
    pygame.event.get = lambda: [pygame.event.Event(pygame.QUIT)]
    pygame.quit = lambda: None
    sys.exit = lambda codigo=0: None
    try:
        return runpy.run_path(os.path.join(os.path.dirname(__file__), "PRISION FANTASY.py"))
    finally:
        pygame.event.get = obtener_eventos
        pygame.quit = cerrar_pygame
        sys.exit = salir


# El espacio de nombres del juego se reutiliza en las pruebas de sus funciones y clases.
JUEGO = cargar_juego_sin_ventana()


class FakeMySQLCursor:
    # Cursor falso que registra consultas y entrega una fila de ejemplo sin base real.
    def __init__(self):
        self.query = None
        self.params = None
        self.closed = False

    def execute(self, query, params=None):
        self.query = query
        self.params = params

    def fetchall(self):
        return [(1, '{"version": 1}', "fecha")]

    def close(self):
        self.closed = True


class FakeMySQLConnection:
    # Conexión falsa que permite verificar liberación de recursos y confirmaciones.
    def __init__(self):
        self.cursor_instancia = FakeMySQLCursor()
        self.committed = False
        self.closed = False

    def cursor(self):
        return self.cursor_instancia

    def commit(self):
        self.committed = True

    def close(self):
        self.closed = True


class FakeMySQLConnector:
    # Sustituto compatible con mysql.connector.connect para capturar parámetros.
    def __init__(self):
        self.conexion = FakeMySQLConnection()
        self.argumentos = None

    def connect(self, **kwargs):
        self.argumentos = kwargs
        return self.conexion


class VerificacionesExpansion(unittest.TestCase):
    # Pruebas de audio, interfaz, guardado, oleadas, mapa, enemigos, jefes y mejoras.
    def test_configuracion_contiene_24_sonidos_de_accion_editables(self):
        from sonidos_acciones import ARCHIVOS_SONIDO

        estado = JUEGO["reproducir_sonido"].__globals__
        self.assertEqual(len(ARCHIVOS_SONIDO), 24)
        self.assertTrue(all(nombre for nombre in ARCHIVOS_SONIDO))
        esperados = {
            "pasos_caminar": "pasos_caminar.wav",
            "pasos_correr": "pasos_correr.wav",
            "salto": "salto.wav",
            "aterrizaje": "aterrizaje.wav",
            "ataque_espada": "ataque_espada.wav",
            "ataque_embestida": "ataque_embestida.wav",
            "golpe_enemigo": "golpe_enemigo.wav",
            "derrota_enemigo": "derrota_enemigo.wav",
            "dano_jugador": "golpe_PERSONAJE- copia.wav",
            "derrota_jugador": "derrota_jugador.wav",
            "victoria": "victoria.wav",
            "curacion_pocion": "curacion_pocion.wav",
            "abrir_cofre": "abrir_cofre.wav",
            "recoger_pocion": "recoger_pocion.wav",
            "activar_berserker": "activar_berserker.wav",
            "ataque_enemigo_cuerpo": "ataque_enemigo_cuerpo.wav",
            "ataque_enemigo_distancia": "ataque_enemigo_distancia.wav",
            "ataque_jefe": "ataque_jefe.wav",
            "inicio_oleada": "inicio_oleada.wav",
        }
        for nombre, archivo in esperados.items():
            self.assertEqual(ARCHIVOS_SONIDO[nombre], archivo)
            self.assertTrue(os.path.isfile(os.path.join(
                os.path.dirname(__file__), "sonidos", archivo
            )))
        self.assertTrue(all(
            archivo == "" for nombre, archivo in ARCHIVOS_SONIDO.items()
            if nombre not in esperados
        ))
        self.assertEqual(set(estado["audio_acciones"].archivos), set(ARCHIVOS_SONIDO))

    def test_audio_acciones_carga_instancias_separadas_y_aplica_volumen(self):
        from sonidos_acciones import AudioAcciones

        class SonidoPrueba:
            def __init__(self):
                self.volumen = None
                self.reproducciones = 0
                self.canales_activos = 0

            def set_volume(self, volumen):
                self.volumen = volumen

            def play(self, loops=0):
                self.reproducciones += 1
                self.canales_activos += 1

            def get_num_channels(self):
                return self.canales_activos

            def get_busy(self):
                return self.canales_activos > 0

            def pause(self):
                self.pausado = True

            def unpause(self):
                self.pausado = False

        with tempfile.TemporaryDirectory() as carpeta:
            for archivo in ("ataque.wav", "rodar.wav"):
                with open(os.path.join(carpeta, archivo), "wb") as sonido_vacio:
                    sonido_vacio.write(b"test")
            creados = []

            def crear_sonido(ruta):
                sonido = SonidoPrueba()
                creados.append((ruta, sonido))
                return sonido

            audio = AudioAcciones(carpeta, {"ataque": "ataque.wav", "rodar": "rodar.wav"})
            with patch("sonidos_acciones.pygame.mixer.get_init", return_value=True), \
                    patch("sonidos_acciones.pygame.mixer.Sound", side_effect=crear_sonido):
                audio.cargar()
                self.assertTrue(audio.reproducir("ataque", 0.35))
                self.assertTrue(audio.reproducir("rodar", 0.8))

            self.assertEqual(len(creados), 2)
            self.assertIsNot(creados[0][1], creados[1][1])
            self.assertEqual(creados[0][1].volumen, 0.35)
            self.assertEqual(creados[1][1].volumen, 0.8)
            self.assertEqual(creados[0][1].reproducciones, 1)
            self.assertEqual(creados[1][1].reproducciones, 1)

    def test_pasos_en_bucle_se_mantienen_se_detienen_y_no_se_superponen(self):
        from sonidos_acciones import AudioAcciones

        class CanalPrueba:
            def __init__(self, sonido, loops):
                self.sonido = sonido
                self.loops = loops
                self.ocupado = True

            def get_sound(self):
                return self.sonido

            def get_busy(self):
                return self.ocupado

            def stop(self):
                self.ocupado = False

        class SonidoPrueba:
            def __init__(self):
                self.reproducciones = 0
                self.canal = None

            def set_volume(self, volumen):
                self.volumen = volumen

            def play(self, loops=0):
                self.reproducciones += 1
                self.canal = CanalPrueba(self, loops)
                return self.canal

            def stop(self):
                if self.canal is not None:
                    if hasattr(self, "canal"):
                        self.canal.stop()

        with tempfile.TemporaryDirectory() as carpeta:
            for archivo in ("caminar", "correr"):
                with open(os.path.join(carpeta, archivo), "wb") as sonido_vacio:
                    sonido_vacio.write(b"test")
            sonidos = {}

            def crear_sonido(ruta):
                sonido = SonidoPrueba()
                sonidos[os.path.basename(ruta)] = sonido
                return sonido

            audio = AudioAcciones(
                carpeta, {"pasos_caminar": "caminar", "pasos_correr": "correr"}
            )
            with patch("sonidos_acciones.pygame.mixer.get_init", return_value=True), \
                    patch("sonidos_acciones.pygame.mixer.Sound", side_effect=crear_sonido):
                audio.cargar()
                self.assertTrue(audio.reproducir_bucle("pasos_caminar", 0.5))
                canal_caminar = sonidos["caminar"].canal
                self.assertEqual(canal_caminar.loops, -1)
                self.assertTrue(audio.reproducir_bucle("pasos_caminar", 0.6))
                self.assertEqual(sonidos["caminar"].reproducciones, 1)
                self.assertTrue(audio.reproducir_bucle(
                    "pasos_correr", 0.8, reemplazar=("pasos_caminar",)
                ))
                self.assertFalse(canal_caminar.ocupado)
                canal_correr = sonidos["correr"].canal
                self.assertEqual(canal_correr.loops, -1)
                audio.detener("pasos_caminar", "pasos_correr")
                self.assertFalse(canal_correr.ocupado)

    def test_ataque_nuevo_interrumpe_el_sonido_anterior(self):
        from sonidos_acciones import AudioAcciones

        class CanalPrueba:
            def __init__(self, sonido):
                self.sonido = sonido
                self.ocupado = True

            def get_sound(self):
                return self.sonido

            def get_busy(self):
                return self.ocupado

            def stop(self):
                self.ocupado = False

        class SonidoPrueba:
            def set_volume(self, volumen):
                pass

            def play(self, loops=0):
                self.canal = CanalPrueba(self)
                return self.canal

            def stop(self):
                if hasattr(self, "canal"):
                    self.canal.stop()

        audio = AudioAcciones(".", {
            "ataque_espada": "espada.wav",
            "ataque_embestida": "embestida.wav",
        })
        audio.sonidos = {
            nombre: SonidoPrueba() for nombre in audio.archivos
        }
        with patch("sonidos_acciones.pygame.mixer.get_init", return_value=True):
            self.assertTrue(audio.reproducir("ataque_espada"))
            canal_anterior = audio.canales["ataque_espada"]
            self.assertTrue(audio.reproducir(
                "ataque_embestida", reemplazar=("ataque_espada", "ataque_embestida")
            ))
        self.assertFalse(canal_anterior.ocupado)
        self.assertTrue(audio.canales["ataque_embestida"].ocupado)

    def test_jugador_inicia_y_detiene_pasos_segun_su_movimiento(self):
        estado = JUEGO["reproducir_sonido"].__globals__
        audio_original = estado["audio_acciones"]
        posicion_original = estado["pos_raton_mundo"]

        class AudioPrueba:
            def __init__(self):
                self.bucles = []
                self.detenciones = []

            def reproducir_bucle(self, nombre, volumen, reemplazar=()):
                self.bucles.append((nombre, volumen, reemplazar))
                return True

            def detener(self, *nombres):
                self.detenciones.append(nombres)

        class Teclas(dict):
            def __getitem__(self, tecla):
                return self.get(tecla, False)

        audio = AudioPrueba()
        jugador = JUEGO["Partida"]().jugador
        estado["audio_acciones"] = audio
        estado["pos_raton_mundo"] = lambda: pygame.Vector2(jugador.rect.center)
        try:
            with patch("pygame.mouse.get_pressed", return_value=(False, False, False)):
                jugador.actualizar(Teclas({pygame.K_d: True}), 0.01)
                self.assertEqual(audio.bucles[-1][0], "pasos_caminar")
                jugador.actualizar(
                    Teclas({pygame.K_d: True, pygame.K_LSHIFT: True}), 0.01
                )
                self.assertEqual(audio.bucles[-1][0], "pasos_correr")
                self.assertEqual(audio.bucles[-1][2], ("pasos_caminar",))
                jugador.actualizar(Teclas(), 0.01)
                self.assertEqual(audio.detenciones[-1], ("pasos_caminar", "pasos_correr"))
        finally:
            estado["audio_acciones"] = audio_original
            estado["pos_raton_mundo"] = posicion_original

    def test_acciones_del_jugador_y_cofre_disparan_sus_sonidos(self):
        estado = JUEGO["reproducir_sonido"].__globals__
        reproducir_original = estado["reproducir_sonido"]
        llamados = []

        def registrar_sonido(nombre, **opciones):
            llamados.append(nombre)

        try:
            estado["reproducir_sonido"] = registrar_sonido
            jugador = JUEGO["Partida"]().jugador
            jugador.empezar("atacar")
            jugador.vida = 50
            jugador.recibir_dano(5)
            jugador.morir()

            partida = JUEGO["Partida"]()
            cofre = estado["mapa"].cofres[0]
            partida.jugador.rect.center = cofre.rect.center
            self.assertTrue(partida.abrir_cofre())
            partida._recoger_pociones()
            self.assertIn("ataque_espada", llamados)
            self.assertIn("dano_jugador", llamados)
            self.assertIn("derrota_jugador", llamados)
            self.assertIn("abrir_cofre", llamados)
            self.assertIn("recoger_pocion", llamados)
        finally:
            estado["reproducir_sonido"] = reproducir_original

    def test_botones_de_ajustes_tienen_espacio_y_no_se_superponen(self):
        estado = JUEGO["show_ajustes"].__globals__
        botones = (
            estado["boton_canciones"],
            estado["ranuras_boton"],
            estado["zona_boton"]("volver", 790),
        )
        for indice, boton in enumerate(botones):
            for otro in botones[indice + 1:]:
                self.assertFalse(
                    boton.colliderect(otro),
                    f"Botones superpuestos: {boton} y {otro}",
                )

    def test_hud_separa_puntuacion_vida_oleada_y_pociones(self):
        estado = JUEGO["Partida"].__init__.__globals__
        fuente = estado["fuente_peq"]
        ancho_puntos = fuente.size("PUNTOS: 999999")[0]
        alto = fuente.render("texto de prueba", True, (255, 255, 255)).get_height()
        puntos = pygame.Rect(20, 12, ancho_puntos, alto)
        record = pygame.Rect(20, 40, fuente.size("BEST SCORE: 999999")[0], alto)
        barra_vida = pygame.Rect(20, 78, 320, 26)
        texto_vida = pygame.Rect(368, 78, fuente.size("VIDA 100/100")[0], alto)
        oleada = pygame.Rect(20, 108, fuente.size("OLEADA 99/99 - zona final")[0], alto)
        estado_oleada = pygame.Rect(20, 136, fuente.size("Enemigos restantes: 99")[0], alto)
        pocion = pygame.Rect(20, 184, 64, 64)
        berserker = pygame.Rect(20, 254, fuente.size("BERSERKER ACTIVO 99.9s")[0], alto)

        self.assertFalse(puntos.colliderect(record))
        self.assertFalse(record.colliderect(barra_vida))
        self.assertFalse(barra_vida.colliderect(texto_vida))
        self.assertFalse(texto_vida.colliderect(oleada))
        self.assertFalse(oleada.colliderect(estado_oleada))
        self.assertFalse(estado_oleada.colliderect(pocion))
        self.assertFalse(pocion.colliderect(berserker))

    def test_pantallas_de_musica_y_controles_reservan_espacio_para_volver(self):
        estado = JUEGO["show_musica"].__globals__
        filas = [fila for _, fila in estado["filas_visibles"]()]
        if filas:
            self.assertFalse(filas[-1].colliderect(estado["boton_anterior"]))
            self.assertFalse(filas[-1].colliderect(estado["boton_siguiente"]))

        fuente = estado["fuente_peq"]
        pista = fuente.render("(rueda del raton para ver mas)", True, (200, 200, 200))
        rect_pista = pista.get_rect(center=(estado["width"] // 2, 745))
        self.assertFalse(rect_pista.colliderect(estado["boton_volver_musica"]))

        controles = JUEGO["show_controles"].__globals__
        ultimo_y = 185 + (len(controles["LISTA_CONTROLES"]) - 1) * 40
        ultimo_control = pygame.Rect(0, ultimo_y - fuente.get_height() // 2,
                                     estado["width"], fuente.get_height())
        self.assertFalse(ultimo_control.colliderect(controles["boton_volver_controles"]))

    def test_textos_largos_de_canciones_y_guardados_se_ajustan_al_ancho_disponible(self):
        estado = JUEGO["show_musica"].__globals__
        ajustar = estado["renderizar_texto_ajustado"]
        fuente = estado["fuente_peq"]
        for ancho in (120, 360, 594, 790):
            texto = ajustar("Nombre de archivo muy largo " * 12, fuente, (255, 255, 255), ancho)
            self.assertLessEqual(texto.get_width(), ancho)

    def test_descripciones_de_mejoras_no_exceden_el_ancho_de_sus_tarjetas(self):
        partida = JUEGO["Partida"]()
        estado = JUEGO["Partida"].__init__.__globals__
        fuente = estado["fuente_peq"]
        for poder, _, _ in estado["BONIFICACIONES"]:
            nivel = partida.jugador.bonificaciones[poder]
            lineas = {
                "viento": (f"Cada {max(1, 4 - nivel - 1)} golpe(s) conectados",
                           "lanza un tajo de largo alcance."),
                "dano": ("+15% de dano por nivel", "mejora todos los ataques."),
                "berserker": (f"Pulsa V: {5 + 2 * (nivel + 1)}s de poder",
                              "mas dano y velocidad,", "menos dano recibido."),
            }[poder]
            self.assertLessEqual(
                max(fuente.size(linea)[0] for linea in lineas),
                partida.tarjetas_bonificacion[0].width - 20,
                f"Texto de {poder} sobresale de la tarjeta.",
            )

    def test_fondo_mp4_se_carga_y_se_dibuja_debajo_de_los_botones(self):
        estado = JUEGO["show_menu"].__globals__
        video = estado["video_fondo"]
        self.assertTrue(os.path.isfile(os.path.join(os.path.dirname(__file__), "fondo.mp4")))
        self.assertIsNotNone(video)
        self.assertEqual(video.superficie.get_size(), (JUEGO["width"], JUEGO["height"]))

        dibujar_video = video.dibujar
        llamadas = []
        try:
            def registrar_y_dibujar(superficie):
                llamadas.append(True)
                dibujar_video(superficie)

            video.dibujar = registrar_y_dibujar
            botones_antes = [(op["texto"], op["rect"].copy()) for op in estado["opciones"]]
            estado["show_menu"]()
            botones_despues = [(op["texto"], op["rect"].copy()) for op in estado["opciones"]]
            self.assertEqual(llamadas, [True])
            self.assertEqual(botones_despues, botones_antes)
        finally:
            video.dibujar = dibujar_video

    def test_f4_activa_y_desactiva_el_hud_sin_anunciarse_en_controles(self):
        estado = JUEGO["manejar_eventos"].__globals__
        estado_anterior = {
            clave: estado[clave]
            for clave in ("JUGAR", "PAUSA", "CARGANDO", "MOSTRAR_HUD")
        }
        obtener_eventos = pygame.event.get
        try:
            estado.update(JUGAR=True, PAUSA=False, CARGANDO=False, MOSTRAR_HUD=True)
            pygame.event.get = lambda: [
                pygame.event.Event(pygame.KEYDOWN, key=pygame.K_F4)
            ]
            JUEGO["manejar_eventos"]()
            self.assertFalse(estado["MOSTRAR_HUD"])

            JUEGO["manejar_eventos"]()
            self.assertTrue(estado["MOSTRAR_HUD"])
            self.assertFalse(any("F4" in control for control, _ in JUEGO["LISTA_CONTROLES"]))
        finally:
            pygame.event.get = obtener_eventos
            estado.update(estado_anterior)

    def test_h_oculta_y_muestra_solo_los_controles_inferiores(self):
        estado = JUEGO["manejar_eventos"].__globals__
        estado_anterior = {
            clave: estado[clave]
            for clave in ("JUGAR", "PAUSA", "CARGANDO", "MOSTRAR_HUD", "MOSTRAR_CONTROLES")
        }
        obtener_eventos = pygame.event.get
        try:
            estado.update(
                JUGAR=True,
                PAUSA=False,
                CARGANDO=False,
                MOSTRAR_HUD=True,
                MOSTRAR_CONTROLES=True,
            )
            pygame.event.get = lambda: [
                pygame.event.Event(pygame.KEYDOWN, key=pygame.K_h)
            ]
            JUEGO["manejar_eventos"]()
            self.assertFalse(estado["MOSTRAR_CONTROLES"])
            self.assertTrue(estado["MOSTRAR_HUD"])

            JUEGO["manejar_eventos"]()
            self.assertTrue(estado["MOSTRAR_CONTROLES"])
            self.assertTrue(estado["MOSTRAR_HUD"])
        finally:
            pygame.event.get = obtener_eventos
            estado.update(estado_anterior)

    def test_hud_oculto_no_dibuja_textos_ni_indicadores(self):
        estado = JUEGO["partida"].dibujar.__globals__
        partida = JUEGO["Partida"]()
        nombres = (
            "texto_borde",
            "dibujar_barra_vida",
            "dibujar_mira",
        )
        originales = {nombre: estado[nombre] for nombre in nombres}
        original_numeros = estado["numeros_dano"].dibujar
        original_hud = partida.oleadas.dibujar_hud
        original_flecha = partida.oleadas.dibujar_flecha
        hud_anterior = estado["MOSTRAR_HUD"]

        def fallo_si_se_dibuja(*args, **kwargs):
            self.fail("Se dibujó texto o indicador mientras el HUD estaba oculto")

        try:
            estado["MOSTRAR_HUD"] = False
            for nombre in nombres:
                estado[nombre] = fallo_si_se_dibuja
            estado["numeros_dano"].dibujar = fallo_si_se_dibuja
            partida.oleadas.dibujar_hud = fallo_si_se_dibuja
            partida.oleadas.dibujar_flecha = fallo_si_se_dibuja
            partida.dibujar(pygame.Surface((JUEGO["width"], JUEGO["height"])), False)
        finally:
            estado.update(originales)
            estado["numeros_dano"].dibujar = original_numeros
            partida.oleadas.dibujar_hud = original_hud
            partida.oleadas.dibujar_flecha = original_flecha
            estado["MOSTRAR_HUD"] = hud_anterior

    def test_guardado_restaurable_conserva_zonas_mejoras_y_pociones(self):
        estado = JUEGO["capturar_progreso_guardado"].__globals__
        partida = JUEGO["Partida"]()
        partida.oleadas.zonas[0]["estado"] = "completada"
        partida.oleadas.zonas[1]["estado"] = "completada"
        partida.jugador.vida = 73
        partida.jugador.rect.center = (2875, 1940)
        partida.jugador.pos.update(partida.jugador.rect.center)
        partida.jugador.pociones = 2
        partida.jugador.bonificaciones.update(viento=1, dano=2, berserker=3)
        partida.puntuacion = 420
        partida.bestscore = 950
        estado["mapa"].cofres[0].abierto = True
        progreso = JUEGO["capturar_progreso_guardado"](partida)
        self.assertEqual(progreso["zonas_completadas"], 2)
        self.assertEqual(progreso["posicion"], [2875, 1940])
        self.assertEqual(progreso["cofres_abiertos"], [0])

        nueva_partida = JUEGO["Partida"]()
        JUEGO["aplicar_progreso_guardado"](nueva_partida, progreso)
        self.assertEqual(
            sum(zona["estado"] == "completada" for zona in nueva_partida.oleadas.zonas),
            2,
        )
        self.assertEqual(nueva_partida.jugador.rect.center, (2875, 1940))
        self.assertEqual(tuple(nueva_partida.jugador.pos), (2875, 1940))
        self.assertEqual(nueva_partida.jugador.vida, 73)
        self.assertEqual(nueva_partida.jugador.pociones, 2)
        self.assertEqual(nueva_partida.jugador.bonificaciones["berserker"], 3)
        self.assertEqual(nueva_partida.puntuacion, 420)
        self.assertEqual(nueva_partida.bestscore, 950)
        self.assertEqual(nueva_partida.oleadas.puntuacion, 420)
        self.assertIn((17, 8), estado["mapa"].puertas_abiertas)
        self.assertTrue(estado["mapa"].cofres[0].abierto)

    def test_guardado_anterior_sin_posicion_y_posicion_invalida(self):
        partida = JUEGO["Partida"]()
        progreso = JUEGO["capturar_progreso_guardado"](partida)
        progreso.pop("posicion")
        JUEGO["validar_progreso_guardado"](progreso)

        progreso["posicion"] = [JUEGO["MUNDO_ANCHO"], 100]
        with self.assertRaisesRegex(ValueError, "posicion invalida"):
            JUEGO["validar_progreso_guardado"](progreso)

    def test_puntuacion_de_enemigo_disminuye_con_tiempo_y_no_se_duplica(self):
        partida = JUEGO["Partida"]()
        oleadas = partida.oleadas
        zona = oleadas.zonas[0]
        zona.update(
            estado="activa", generados=zona["total"], matados=0,
            tiempo_oleada=150.0,
        )
        partida.jugador.rect.center = zona["rect"].center
        enemigo = JUEGO["Enemigo"](*partida.jugador.rect.center, tipo="goblin")
        enemigo.de_oleada = True
        enemigo.vida = 0
        enemigo.t_muerte = 0.0
        partida.enemigos.agregar(enemigo)

        oleadas.actualizar(0, partida.jugador, partida.enemigos)
        self.assertEqual(enemigo.puntos_base, 100)
        self.assertEqual(oleadas.puntuacion, 65)
        self.assertEqual(zona["puntos_ganados"], 65)
        oleadas.actualizar(0, partida.jugador, partida.enemigos)
        self.assertEqual(oleadas.puntuacion, 65)

        zona.update(estado="activa", tiempo_oleada=300.0)
        enemigo_lento = JUEGO["Enemigo"](*partida.jugador.rect.center, tipo="goblin")
        enemigo_lento.de_oleada = True
        enemigo_lento.vida = 0
        enemigo_lento.t_muerte = 0.0
        partida.enemigos.agregar(enemigo_lento)
        oleadas.actualizar(0, partida.jugador, partida.enemigos)
        self.assertEqual(oleadas.puntuacion, 95)
        self.assertEqual(zona["puntos_ganados"], 95)

    def test_reloj_de_puntuacion_sigue_bajando_fuera_de_zona_abierta(self):
        partida = JUEGO["Partida"]()
        zona = partida.oleadas.zonas[0]
        zona.update(estado="activa", cerrada=False, tiempo_oleada=12.0)
        partida.jugador.rect.center = (0, 0)

        partida.oleadas.actualizar(2.5, partida.jugador, partida.enemigos)

        self.assertEqual(zona["tiempo_oleada"], 14.5)

    def test_mysql_save_slots_usa_parametros_y_guarda_payload_json(self):
        from guardado_mysql import MySQLSaveSlots

        conector = FakeMySQLConnector()
        almacen = MySQLSaveSlots(
            {
                "host": "localhost",
                "port": 3306,
                "user": "test",
                "password": "test",
                "database": "test",
                "player_id": "jugador_pruebas",
            },
            connector=conector,
        )
        progreso = {"version": 1, "zonas_completadas": 2}
        almacen.guardar(2, progreso)
        consulta = conector.conexion.cursor_instancia
        self.assertIn("VALUES (%s, %s, %s)", consulta.query)
        self.assertEqual(consulta.params[:2], ("jugador_pruebas", 2))
        self.assertEqual(json.loads(consulta.params[2]), progreso)
        self.assertTrue(conector.conexion.committed)
        self.assertTrue(conector.conexion.closed)

        registros = almacen.listar()
        self.assertEqual(registros[0]["slot"], 1)
        self.assertEqual(registros[0]["payload"], {"version": 1})

    def test_mysql_save_slots_informa_configuracion_incompleta(self):
        from guardado_mysql import ConfiguracionMySQLError, MySQLSaveSlots

        almacen = MySQLSaveSlots(
            {
                "host": "",
                "port": "3306",
                "user": "",
                "password": "",
                "database": "",
                "player_id": "jugador_pruebas",
            }
        )
        with self.assertRaisesRegex(ConfiguracionMySQLError, "PRISION_DB_HOST"):
            almacen.listar()

    def test_pantalla_de_ranuras_muestra_errores_de_conexion(self):
        estado = JUEGO["refrescar_ranuras"].__globals__
        almacen_original = estado["almacen_guardados"]
        try:
            class AlmacenInaccesible:
                def listar(self):
                    raise OSError("servidor sin conexion")

            estado["almacen_guardados"] = AlmacenInaccesible()
            JUEGO["refrescar_ranuras"]()
            self.assertIn("servidor sin conexion", estado["estado_ranuras"])
            JUEGO["show_ranuras"]()
        finally:
            estado["almacen_guardados"] = almacen_original

    def test_ajustes_abre_ranuras_y_carga_la_partida_seleccionada(self):
        estado = JUEGO["manejar_eventos"].__globals__
        claves = (
            "JUGAR", "PAUSA", "AJUSTES", "RANURAS", "MUSICA", "CARGANDO",
            "tiempo_carga_restante", "progreso_carga_pendiente", "ranuras_guardadas",
            "almacen_guardados", "estado_ranuras", "ranura_activa",
        )
        anterior = {clave: estado[clave] for clave in claves}
        obtener_eventos = pygame.event.get
        progreso = {
            "version": 1,
            "zonas_completadas": 2,
            "vida": 80,
            "pociones": 1,
            "mejoras": {"viento": 1, "dano": 0, "berserker": 0},
        }

        class AlmacenPruebas:
            def listar(self):
                return [{"slot": 1, "payload": progreso, "updated_at": "fecha"}]

        def evento_en(rect):
            ancho, alto = estado["ventana"].get_size()
            x, y = rect.center
            pos = (round(x * ancho / estado["width"]), round(y * alto / estado["height"]))
            return pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=pos)

        try:
            estado.update(
                JUGAR=False,
                PAUSA=False,
                AJUSTES=True,
                RANURAS=False,
                MUSICA=False,
                CARGANDO=False,
                almacen_guardados=AlmacenPruebas(),
                ranuras_guardadas={},
                progreso_carga_pendiente=None,
            )
            pygame.event.get = lambda: [evento_en(estado["ranuras_boton"])]
            JUEGO["manejar_eventos"]()
            self.assertTrue(estado["RANURAS"])
            self.assertIn(1, estado["ranuras_guardadas"])

            pygame.event.get = lambda: [evento_en(estado["ranuras_cargar"][1])]
            JUEGO["manejar_eventos"]()
            self.assertTrue(estado["CARGANDO"])
            self.assertFalse(estado["RANURAS"])
            self.assertEqual(estado["progreso_carga_pendiente"], progreso)
        finally:
            pygame.event.get = obtener_eventos
            estado.update(anterior)

    def test_final_de_partida_permite_abrir_ranuras_y_guardar_progreso(self):
        estado = JUEGO["manejar_eventos"].__globals__
        claves = (
            "JUGAR", "PAUSA", "AJUSTES", "RANURAS", "MUSICA", "CARGANDO",
            "partida", "ranuras_guardadas", "almacen_guardados", "estado_ranuras",
        )
        anterior = {clave: estado[clave] for clave in claves}
        obtener_eventos = pygame.event.get
        progreso_guardado = []

        class AlmacenPruebas:
            def listar(self):
                return []

            def guardar(self, ranura, progreso):
                progreso_guardado.append((ranura, progreso))

        def evento_en(rect):
            ancho, alto = estado["ventana"].get_size()
            x, y = rect.center
            pos = (round(x * ancho / estado["width"]), round(y * alto / estado["height"]))
            return pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=pos)

        try:
            partida = JUEGO["Partida"]()
            for zona in partida.oleadas.zonas:
                zona["estado"] = "completada"
            partida.jugador.vida = 64
            partida.jugador.pociones = 2
            partida.jugador.bonificaciones.update(viento=2, dano=1)
            self.assertTrue(partida.terminada)

            estado.update(
                JUGAR=True,
                PAUSA=False,
                AJUSTES=False,
                RANURAS=False,
                MUSICA=False,
                CARGANDO=False,
                partida=partida,
                ranuras_guardadas={},
                almacen_guardados=AlmacenPruebas(),
            )
            pygame.event.get = lambda: [evento_en(estado["boton_ranuras_final"])]
            JUEGO["manejar_eventos"]()
            self.assertTrue(estado["RANURAS"])

            pygame.event.get = lambda: [evento_en(estado["ranuras_guardar"][2])]
            JUEGO["manejar_eventos"]()
            self.assertEqual(len(progreso_guardado), 1)
            ranura, progreso = progreso_guardado[0]
            self.assertEqual(ranura, 2)
            self.assertEqual(progreso["zonas_completadas"], len(JUEGO["ZONAS"]))
            self.assertEqual(progreso["vida"], 64)
            self.assertEqual(progreso["pociones"], 2)
            self.assertEqual(progreso["mejoras"]["viento"], 2)
        finally:
            pygame.event.get = obtener_eventos
            estado.update(anterior)

    def test_partida_completada_pausada_conserva_las_opciones_de_pausa(self):
        estado = JUEGO["manejar_eventos"].__globals__
        claves = (
            "JUGAR", "PAUSA", "AJUSTES", "RANURAS", "MUSICA", "CARGANDO",
            "CONTROLES", "partida",
        )
        anterior = {clave: estado[clave] for clave in claves}
        obtener_eventos = pygame.event.get

        def evento_en(rect):
            ancho, alto = estado["ventana"].get_size()
            x, y = rect.center
            pos = (round(x * ancho / estado["width"]), round(y * alto / estado["height"]))
            return pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=pos)

        try:
            partida = JUEGO["Partida"]()
            for zona in partida.oleadas.zonas:
                zona["estado"] = "completada"
            estado.update(
                JUGAR=True,
                PAUSA=True,
                AJUSTES=False,
                RANURAS=False,
                MUSICA=False,
                CARGANDO=False,
                CONTROLES=False,
                partida=partida,
            )
            reanudar = next(op["rect"] for op in estado["opciones_pausa"] if op["modo"] == "reanudar")
            pygame.event.get = lambda: [evento_en(reanudar)]
            JUEGO["manejar_eventos"]()
            self.assertFalse(estado["PAUSA"])
        finally:
            pygame.event.get = obtener_eventos
            estado.update(anterior)

    def test_pantalla_de_carga_al_iniciar_partida(self):
        estado = JUEGO["iniciar_carga"].__globals__
        estado_anterior = {
            clave: estado[clave]
            for clave in ("JUGAR", "CARGANDO", "PAUSA", "tiempo_carga_restante", "partida", "siguiente")
        }
        try:
            partida_anterior = estado["partida"]
            llamadas_siguiente = []
            estado["siguiente"] = lambda: llamadas_siguiente.append(True)
            JUEGO["iniciar_carga"]()
            self.assertTrue(estado["JUGAR"])
            self.assertTrue(estado["CARGANDO"])
            self.assertEqual(estado["tiempo_carga_restante"], estado["TIEMPO_CARGA"])

            JUEGO["show_carga"](0.6)
            self.assertTrue(estado["CARGANDO"])
            self.assertFalse(llamadas_siguiente)
            self.assertAlmostEqual(
                estado["tiempo_carga_restante"],
                estado["TIEMPO_CARGA"] - 0.6,
            )

            JUEGO["show_carga"](estado["TIEMPO_CARGA"])
            self.assertFalse(estado["CARGANDO"])
            self.assertIsNot(estado["partida"], partida_anterior)
            self.assertEqual(llamadas_siguiente, [True])
        finally:
            estado.update(estado_anterior)

    def test_contador_de_pociones_muestra_icono_y_cantidad_sin_etiqueta(self):
        partida = JUEGO["Partida"]()
        estado = partida.dibujar.__globals__
        cargar_imagen_original = estado["cargar_imagen_pocion"]
        texto_borde_original = estado["texto_borde"]
        tamanos_icono = []
        textos = []
        try:
            def cargar_icono(tamano):
                tamanos_icono.append(tuple(tamano))
                return pygame.Surface(tamano, pygame.SRCALPHA)

            def registrar_texto(superficie, texto, *args, **kwargs):
                textos.append(str(texto))

            estado["cargar_imagen_pocion"] = cargar_icono
            estado["texto_borde"] = registrar_texto
            partida.jugador.pociones = 3
            partida.dibujar(pygame.Surface((JUEGO["width"], JUEGO["height"])), False)
            self.assertEqual(tamanos_icono, [(64, 64)])
            self.assertIn("3", textos)
            self.assertNotIn("Pociones: 3", textos)
        finally:
            estado["cargar_imagen_pocion"] = cargar_imagen_original
            estado["texto_borde"] = texto_borde_original

    def test_clic_derecho_y_tecla_r_activan_rodar_y_e_mantiene_giro(self):
        jugador = JUEGO["Partida"]().jugador
        teclas = {
            pygame.K_SPACE: False,
            pygame.K_r: False,
            pygame.K_e: False,
            pygame.K_q: False,
            pygame.K_v: False,
        }

        nuevas = jugador.pulsaciones(teclas, (False, False, True))
        self.assertTrue(nuevas["rodar"])
        self.assertFalse(nuevas["giro"])

        jugador.prev = {}
        teclas[pygame.K_r] = True
        nuevas = jugador.pulsaciones(teclas, (False, False, False))
        self.assertTrue(nuevas["rodar"])

        jugador.prev = {}
        teclas[pygame.K_r] = False
        teclas[pygame.K_e] = True
        nuevas = jugador.pulsaciones(teclas, (False, False, False))
        self.assertFalse(nuevas["rodar"])
        self.assertTrue(nuevas["giro"])

    def test_mapa_rectangular_y_zonas_conectadas(self):
        mapa = JUEGO["mapa"]
        filas = JUEGO["MAPA"]
        zonas = JUEGO["partida"].oleadas.zonas
        puertas_configuradas = {
            puerta
            for grupo in JUEGO["PUERTAS_POR_OLEADA"].values()
            for puerta in grupo
        }
        self.assertEqual((len(filas[0]), len(filas)), (80, 48))
        self.assertEqual({len(fila) for fila in filas}, {80})
        self.assertEqual(set(mapa.suelo_puerta), puertas_configuradas)
        self.assertEqual([z["nombre"] for z in zonas],
                         ["Bosque Susurrante", "Ruinas del Templo", "Pantano Venenoso", "Prision",
                          "Arena del Carcelero", "Aldea Abandonada", "Selva Antigua",
                          "Desfiladero de la Mina", "Cumbre del Dragon"])
        for zona in zonas:
            self.assertTrue(zona["puntos"], zona["nombre"])
            self.assertTrue(mapa.camino(mapa.inicio, zona["destino"]), zona["nombre"])
        self.assertEqual(
            [zona["total"] for zona in zonas[:-1]],
            [zona["enemigos_derrotar"] for zona in JUEGO["ZONAS"][:-1]],
        )
        self.assertTrue(all(z["total"] > 0 for z in zonas[:-1]))
        self.assertEqual(zonas[0]["max_vivos"], 3)
        self.assertEqual(zonas[0]["intervalo"], 1.0)
        self.assertEqual(zonas[0]["tipos_enemigos"], ("goblin", "mago"))
        self.assertEqual(zonas[1]["tipos_enemigos"], ("goblin", "mago"))
        self.assertEqual(zonas[2]["tipos_enemigos"], ("bruja", "trol"))
        self.assertEqual(zonas[3]["tipos_enemigos"], ("bruja", "trol"))
        self.assertEqual(zonas[4]["tipo_jefe"], "orco")
        self.assertEqual(set(zonas[4]["tipos_apoyo"]), {"lich", "espectro"})
        for zona in zonas[5:8]:
            self.assertEqual(set(zona["tipos_enemigos"]), {"lich", "espectro"})
        for sprite in ("goblin", "goblin_mago", "bruja", "trol", "lich", "espectro"):
            self.assertTrue(os.path.isfile(JUEGO["ruta_sprite_enemigo"](sprite)), sprite)
        self.assertTrue(all(not zona["cerrada"] for zona in zonas))
        self.assertGreater(sum(fila.count("m") + fila.count("b") for fila in filas), 20)
        self.assertEqual(sum(zona["jefe"] for zona in zonas), 2)
        self.assertTrue(zonas[4]["jefe"])
        self.assertEqual(zonas[4]["sprite_jefe"], "orco_jefe_de_guerra")
        self.assertEqual(zonas[4]["tipo_jefe"], "orco")
        self.assertEqual(zonas[4]["total"], 1)
        self.assertTrue(zonas[-1]["jefe"])
        self.assertEqual(zonas[-1]["total"], 1)
        self.assertEqual(zonas[-1]["sprite_jefe"], "dragon")
        self.assertTrue(os.path.isfile(JUEGO["ruta_sprite_enemigo"]("dragon")))
        self.assertTrue(os.path.isfile(JUEGO["ruta_sprite_enemigo"]("orco_jefe_de_guerra")))
        self.assertEqual(
            JUEGO["JEFE_ALTURA_SPRITE"],
            JUEGO["TAM_TILE"] * 2.5,
        )

    def test_avanzar_oleada_abre_sus_puertas_y_reiniciar_las_cierra(self):
        partida = JUEGO["Partida"]()
        mapa = JUEGO["mapa"]
        puertas_oleada = JUEGO["PUERTAS_POR_OLEADA"][1]
        puerta = (17, 8)
        puerta_siguiente_oleada = JUEGO["PUERTAS_POR_OLEADA"][2][0]
        celdas_puertas = [
            pygame.Rect(x * JUEGO["TAM_TILE"] + 50, y * JUEGO["TAM_TILE"] + 50, 20, 20)
            for x, y in puertas_oleada
        ]
        celda_puerta = celdas_puertas[1]
        celda_puerta_siguiente_oleada = pygame.Rect(
            puerta_siguiente_oleada[0] * JUEGO["TAM_TILE"] + 50,
            puerta_siguiente_oleada[1] * JUEGO["TAM_TILE"] + 50,
            20,
            20,
        )
        self.assertTrue(all(mapa.choca(celda) for celda in celdas_puertas))
        self.assertTrue(mapa.choca(celda_puerta_siguiente_oleada))

        zona = partida.oleadas.zonas[0]
        zona.update(estado="activa", generados=zona["total"], matados=zona["total"] - 1)
        partida.jugador.rect.center = zona["rect"].center
        enemigo = JUEGO["Enemigo"](*partida.jugador.rect.center)
        enemigo.de_oleada = True
        enemigo.vida = 0
        partida.enemigos.agregar(enemigo)
        partida.oleadas.actualizar(0, partida.jugador, partida.enemigos)
        self.assertEqual(zona["estado"], "completada")
        self.assertTrue(set(puertas_oleada).issubset(mapa.puertas_abiertas))
        self.assertTrue(all(not mapa.choca(celda) for celda in celdas_puertas))
        self.assertNotIn(puerta_siguiente_oleada, mapa.puertas_abiertas)
        self.assertTrue(mapa.choca(celda_puerta_siguiente_oleada))

        zona_siguiente = partida.oleadas.zonas[1]
        zona_siguiente.update(
            estado="activa",
            generados=zona_siguiente["total"],
            matados=zona_siguiente["total"] - 1,
        )
        partida.jugador.rect.center = zona_siguiente["rect"].center
        enemigo = JUEGO["Enemigo"](*partida.jugador.rect.center)
        enemigo.de_oleada = True
        enemigo.vida = 0
        partida.enemigos.agregar(enemigo)
        partida.oleadas.actualizar(0, partida.jugador, partida.enemigos)
        self.assertEqual(zona_siguiente["estado"], "completada")
        self.assertIn(puerta_siguiente_oleada, mapa.puertas_abiertas)
        self.assertFalse(mapa.choca(celda_puerta_siguiente_oleada))

        JUEGO["Partida"]()
        self.assertTrue(set(puertas_oleada).isdisjoint(mapa.puertas_abiertas))
        self.assertTrue(all(mapa.choca(celda) for celda in celdas_puertas))
        self.assertNotIn(puerta_siguiente_oleada, mapa.puertas_abiertas)
        self.assertTrue(mapa.choca(celda_puerta_siguiente_oleada))

    def test_puertas_y_rejas_de_prision_se_abren_con_su_oleada(self):
        partida = JUEGO["Partida"]()
        mapa = JUEGO["mapa"]
        grupos_prision = {
            oleada: JUEGO["PUERTAS_POR_OLEADA"][oleada]
            for oleada in (3, 4)
        }

        def celda_puerta(posicion):
            x, y = posicion
            return pygame.Rect(
                x * JUEGO["TAM_TILE"] + 50,
                y * JUEGO["TAM_TILE"] + 50,
                20,
                20,
            )

        def completar_oleada(numero):
            zona = partida.oleadas.zonas[numero - 1]
            zona.update(
                estado="activa",
                generados=zona["total"],
                matados=zona["total"] - 1,
            )
            partida.jugador.rect.center = zona["rect"].center
            enemigo = JUEGO["Enemigo"](*partida.jugador.rect.center)
            enemigo.de_oleada = True
            enemigo.vida = 0
            partida.enemigos.agregar(enemigo)
            partida.oleadas.actualizar(0, partida.jugador, partida.enemigos)
            self.assertEqual(zona["estado"], "completada")

        rejas_prision = grupos_prision[3][1:]
        puertas_salida_prision = grupos_prision[4]
        posiciones_a_verificar = rejas_prision + puertas_salida_prision
        self.assertTrue(
            all(mapa.choca(celda_puerta(p)) for p in posiciones_a_verificar)
        )

        completar_oleada(1)
        completar_oleada(2)
        self.assertTrue(
            all(mapa.choca(celda_puerta(p)) for p in posiciones_a_verificar)
        )

        completar_oleada(3)
        self.assertTrue(set(grupos_prision[3]).issubset(mapa.puertas_abiertas))
        self.assertTrue(
            all(not mapa.choca(celda_puerta(p)) for p in grupos_prision[3])
        )
        self.assertTrue(
            all(mapa.choca(celda_puerta(p)) for p in puertas_salida_prision)
        )

        zona_prision = partida.oleadas.zonas[3]
        partida.jugador.rect.center = zona_prision["rect"].center
        partida.oleadas.actualizar(0, partida.jugador, partida.enemigos)
        self.assertEqual(zona_prision["estado"], "preparando")
        self.assertEqual(mapa.reja_temporal, (24, 19, 4))
        centro_reja = pygame.Rect(
            26 * JUEGO["TAM_TILE"] + 50,
            19 * JUEGO["TAM_TILE"] + 50,
            20,
            20,
        )
        self.assertTrue(mapa.choca(centro_reja))

        zona_prision.update(
            estado="activa",
            generados=zona_prision["total"],
            matados=zona_prision["total"] - 1,
        )
        enemigo = JUEGO["Enemigo"](*partida.jugador.rect.center)
        enemigo.de_oleada = True
        enemigo.vida = 0
        partida.enemigos.agregar(enemigo)
        partida.oleadas.actualizar(0, partida.jugador, partida.enemigos)
        self.assertEqual(zona_prision["estado"], "completada")
        self.assertIsNone(mapa.reja_temporal)
        self.assertFalse(mapa.choca(centro_reja))

        self.assertTrue(set(puertas_salida_prision).issubset(mapa.puertas_abiertas))
        self.assertTrue(
            all(not mapa.choca(celda_puerta(p)) for p in puertas_salida_prision)
        )

    def test_cofres_solo_abren_fuera_de_combate_y_dan_pocion_de_30(self):
        partida = JUEGO["Partida"]()
        mapa = JUEGO["mapa"]
        cofre = mapa.cofres[0]
        self.assertTrue(os.path.isfile(os.path.join(os.path.dirname(__file__), "mapa", "cofre_abierto.png")))
        self.assertEqual(cofre.imagen_abierta.get_size(), cofre.frames[0].get_size())
        partida.jugador.rect.center = cofre.rect.center
        self.assertIs(partida.cofre_cercano(), cofre)
        self.assertTrue(partida.puede_abrir_cofre())

        enemigo = JUEGO["Enemigo"](cofre.rect.centerx + 200, cofre.rect.centery)
        partida.enemigos.agregar(enemigo)
        self.assertFalse(partida.puede_abrir_cofre())
        self.assertFalse(partida.abrir_cofre())
        self.assertFalse(cofre.abierto)
        partida.enemigos.lista.clear()

        self.assertTrue(partida.puede_abrir_cofre())
        self.assertTrue(partida.abrir_cofre())
        self.assertTrue(cofre.abierto)
        self.assertIsNot(cofre.imagen_abierta, cofre.frames[0])
        self.assertEqual(len(partida.pociones_mundo), 1)
        self.assertEqual(
            JUEGO["cargar_imagen_pocion"]((18 * JUEGO["ESCALA_TILES"],) * 2).get_size(),
            (18 * JUEGO["ESCALA_TILES"],) * 2,
        )
        self.assertTrue(os.path.isfile(os.path.join(os.path.dirname(__file__), "pociones", "pocion_roja.png")))
        partida.dibujar(pygame.Surface((JUEGO["width"], JUEGO["height"])), False)
        self.assertFalse(partida.abrir_cofre())

        partida._recoger_pociones()
        self.assertEqual(partida.jugador.pociones, 1)
        self.assertFalse(partida.pociones_mundo)
        partida.jugador.vida = 60
        partida.jugador.decidir_accion(
            {"saltar": False, "rodar": False, "giro": False, "beber": True, "berserker": False},
            False,
            False,
            False,
            pygame.Vector2(),
            1,
            False,
        )
        self.assertEqual(partida.jugador.accion, "beber")
        self.assertEqual(partida.jugador.vida, 90)
        self.assertEqual(partida.jugador.pociones, 0)
        self.assertFalse(partida.jugador.beber_pocion())

    def test_arquetipos_de_enemigo_comparten_clase_y_definen_combate(self):
        arquetipos = JUEGO["ARQUETIPOS_ENEMIGO"]
        self.assertEqual(set(arquetipos), {"goblin", "mago", "bruja", "trol", "lich", "espectro"})
        self.assertEqual(arquetipos["goblin"]["ataque"], "cuerpo_a_cuerpo")
        self.assertEqual(arquetipos["mago"]["sprite"], "goblin_mago")
        self.assertEqual(arquetipos["mago"]["ataque"], "distancia")
        self.assertEqual(arquetipos["bruja"]["sprite"], "bruja")
        self.assertEqual(arquetipos["bruja"]["ataque"], "distancia")
        self.assertEqual(arquetipos["trol"]["ataque"], "cuerpo_a_cuerpo")
        self.assertEqual(arquetipos["lich"]["ataque"], "distancia")
        self.assertEqual(arquetipos["espectro"]["ataque"], "cuerpo_a_cuerpo")
        self.assertGreater(arquetipos["trol"]["escala"], arquetipos["goblin"]["escala"])
        self.assertGreater(arquetipos["lich"]["escala"], arquetipos["mago"]["escala"])
        self.assertGreater(arquetipos["espectro"]["escala"], arquetipos["trol"]["escala"])
        for tipo, perfil in arquetipos.items():
            enemigo = JUEGO["Enemigo"](1000, 1000, tipo=tipo)
            self.assertEqual(enemigo.vida, perfil["vida"])
            self.assertEqual(enemigo.dano, perfil["dano"])
            self.assertEqual(enemigo.tipo_ataque, perfil["ataque"])
            self.assertEqual(
                enemigo.imagenes[("normal", 1)].get_height(),
                round(JUEGO["cargar_sprite_enemigo"](perfil["sprite"]).get_height() * enemigo.escala),
            )

    def test_enemigo_a_distancia_lanza_proyectil_configurable(self):
        partida = JUEGO["Partida"]()
        enemigo = JUEGO["Enemigo"](1000, 1000, agresivo=True, tipo="mago")
        ataque = {
            "fase": "preparar", "t": 0.4, "golpeo": False,
            "tipo": "distancia", "direccion": pygame.Vector2(1, 0),
            "origen": tuple(enemigo.rect.center), "lado": 1,
        }
        proyectiles = []
        enemigo.ataque = ataque
        enemigo._atacar(0.01, partida.jugador, proyectiles)
        enemigo._atacar(0.2, partida.jugador, proyectiles)
        self.assertEqual(len(proyectiles), 1)
        self.assertEqual(proyectiles[0].dano, JUEGO["ARQUETIPOS_ENEMIGO"]["mago"]["dano"])
        self.assertFalse(proyectiles[0].eliminado)

    def test_proyectil_del_lich_es_azul_y_mas_grande(self):
        arquetipos = JUEGO["ARQUETIPOS_ENEMIGO"]
        mago = JUEGO["Enemigo"](1000, 1000, tipo="mago")
        bruja = JUEGO["Enemigo"](1000, 1000, tipo="bruja")
        lich = JUEGO["Enemigo"](1000, 1000, tipo="lich")
        ataque = {
            "origen": (100, 50),
            "direccion": pygame.Vector2(1, 0),
        }
        proyectil_mago = JUEGO["EnemigoProyectil"](mago, ataque)
        proyectil_bruja = JUEGO["EnemigoProyectil"](bruja, ataque)
        proyectil_lich = JUEGO["EnemigoProyectil"](lich, ataque)
        self.assertGreater(proyectil_lich.rect.width, proyectil_mago.rect.width)
        self.assertGreater(proyectil_lich.rect.height, proyectil_mago.rect.height)
        self.assertEqual(proyectil_lich.color, (40, 115, 255))
        self.assertEqual(proyectil_lich.color_brillo, (135, 220, 255))
        self.assertEqual(proyectil_mago.imagen.get_size(), (84, 80))
        self.assertEqual(proyectil_bruja.imagen.get_size(), (94, 90))
        self.assertEqual(proyectil_lich.imagen.get_size(), (110, 106))
        self.assertEqual(arquetipos["mago"]["proyectil_sprite"], "proyectil_mago.png")
        self.assertEqual(arquetipos["bruja"]["proyectil_sprite"], "proyectil_mago.png")
        self.assertEqual(arquetipos["lich"]["proyectil_sprite"], "proyectil_lich.png")
        self.assertEqual(proyectil_lich.imagen.get_at((0, 0)).a, 0)
        for proyectil, asset in (
            (proyectil_mago, "proyectil_mago.png"),
            (proyectil_bruja, "proyectil_mago.png"),
            (proyectil_lich, "proyectil_lich.png"),
        ):
            self.assertEqual(
                pygame.image.tobytes(proyectil.imagen, "RGBA"),
                pygame.image.tobytes(
                    JUEGO["cargar_imagen_proyectil"](asset, proyectil.imagen.get_size()),
                    "RGBA",
                ),
            )
        superficie = pygame.Surface((200, 100))
        proyectil_lich.dibujar(superficie)
        centro_renderizado = superficie.get_at(proyectil_lich.rect.center)
        self.assertGreater(centro_renderizado.b, centro_renderizado.r)
        self.assertGreater(centro_renderizado.g, centro_renderizado.r)

    def test_jefe_orco_lluvia_espadas_apoyos_y_dragon_final(self):
        self.assertEqual(JUEGO["JEFE_ORCO_INTERVALO_ATAQUE"], 3.0)
        partida = JUEGO["Partida"]()
        zona = partida.oleadas.zonas[4]
        partida.jugador.rect.center = zona["rect"].center
        partida.oleadas._generar(zona, partida.jugador, partida.enemigos)
        jefe = partida.enemigos.lista[0]
        self.assertTrue(jefe.es_jefe)
        self.assertEqual(jefe.tipo_jefe, "orco")
        self.assertEqual(jefe.nombre_jefe, "JEFE ORCO")
        imagen_rey = JUEGO["cargar_sprite_enemigo"]("orco_jefe_de_guerra")
        escala_rey = JUEGO["TAM_TILE"] * 1.55 / imagen_rey.get_height()
        self.assertEqual(
            jefe.imagen_jefe.get_size(),
            (round(imagen_rey.get_width() * escala_rey), round(imagen_rey.get_height() * escala_rey)),
        )
        self.assertEqual(
            jefe.vida_max, 280 * JUEGO["JEFE_ORCO_MULTIPLICADOR_VIDA"]
        )
        self.assertLess(jefe.imagen_jefe.get_height(), JUEGO["JEFE_ALTURA_SPRITE"])
        self.assertEqual(set(jefe.imagenes_lluvia), {"hacha", "espada"})
        self.assertEqual(jefe.imagenes_lluvia["hacha"].get_size(), (80, 80))
        self.assertGreater(jefe.imagenes_lluvia["espada"].get_width(), 80)
        self.assertEqual(
            [jefe._arma_lluvia(i) for i in range(6)],
            ["hacha", "espada", "hacha", "espada", "hacha", "espada"],
        )
        self.assertEqual(zona["generados"], 1)
        jefe.rect.center = (partida.jugador.rect.centerx + 3000, partida.jugador.rect.centery + 700)
        jefe.pos.update(jefe.rect.midbottom)
        jefe.t_cd = 0
        jefe.t_aparicion = 0
        partida.enemigos.actualizar(0.01, partida.jugador)
        self.assertEqual(jefe.ataque_jefe["fase"], "aviso")
        self.assertEqual(jefe.ataque_jefe["tipo"], "lluvia_espadas")
        self.assertEqual(jefe.ataque_jefe["advertencia"], 1.5)
        self.assertEqual(jefe.ataque_jefe["objetivo"], partida.jugador.rect.center)
        self.assertEqual(
            jefe._zona_lluvia_espadas(jefe.ataque_jefe).center,
            partida.jugador.rect.center,
        )
        self.assertEqual(jefe.t_cd, JUEGO["JEFE_ORCO_INTERVALO_ATAQUE"])
        apoyos = [e for e in partida.enemigos if getattr(e, "invocado_por_jefe", False)]
        self.assertEqual(len(apoyos), 3)
        self.assertTrue(all(not e.de_oleada for e in apoyos))
        self.assertEqual(zona["generados"], 1)
        self.assertEqual(zona["matados"], 0)
        jefe.ataque_jefe = None
        jefe.t_cd = 2.0
        posicion_jefe = jefe.rect.center
        jefe.actualizar(0.5, partida.jugador, [partida.jugador])
        self.assertEqual(jefe.rect.center, posicion_jefe)
        self.assertIsNone(jefe.ataque_jefe)
        self.assertEqual(jefe.t_cd, 1.5)

        class JugadorObjetivo:
            muerto = False

            def __init__(self, rect):
                self.rect = rect
                self.danos = []

            def cuerpo(self):
                return self.rect

            def recibir_dano(self, cantidad, origen):
                self.danos.append(cantidad)

        jefe.rect.center = (900, 700)
        jefe.pos.update(jefe.rect.midbottom)
        jefe.ataque_jefe = {
            "tipo": "lluvia_espadas", "fase": "activo", "t": 0.1,
            "objetivo": (900, 700), "lado": 1, "orientacion": "horizontal",
        }
        zona_ataque = jefe._zona_lluvia_espadas(jefe.ataque_jefe)
        jugador_hitbox_separada = JugadorObjetivo(
            pygame.Rect(zona_ataque.centerx, zona_ataque.bottom + 50, 20, 10)
        )
        jugador_hitbox_separada.cuerpo = lambda: pygame.Rect(
            zona_ataque.centerx - 10, zona_ataque.centery - 30, 20, 60
        )
        self.assertTrue(zona_ataque.colliderect(jugador_hitbox_separada.cuerpo()))
        self.assertFalse(zona_ataque.colliderect(jugador_hitbox_separada.rect))
        self.assertFalse(jefe._impacto(jugador_hitbox_separada))
        self.assertEqual(jugador_hitbox_separada.danos, [])
        jugador_hitbox_separada.rect.center = zona_ataque.center
        self.assertTrue(jefe._impacto(jugador_hitbox_separada))
        self.assertEqual(jugador_hitbox_separada.danos, [jefe.dano + 10])

        for orientacion in ("horizontal", "vertical"):
            jefe.ataque_jefe = {
                "tipo": "lluvia_espadas", "fase": "aviso", "t": 0.1,
                "objetivo": (900, 700), "lado": 1, "orientacion": orientacion,
            }
            zona_ataque = jefe._zona_lluvia_espadas(jefe.ataque_jefe)
            if orientacion == "horizontal":
                self.assertGreater(zona_ataque.width, zona_ataque.height)
            else:
                self.assertGreater(zona_ataque.height, zona_ataque.width)
            superficie = pygame.Surface((1600, 1400))
            jefe.dibujar(superficie)
            self.assertEqual(
                superficie.get_at((zona_ataque.left + 2, zona_ataque.centery))[:3],
                (255, 205, 75),
            )

            objetivo = JugadorObjetivo(pygame.Rect(0, 0, 40, 40))
            objetivo.rect.center = zona_ataque.center
            jefe.ataque_jefe["fase"] = "activo"
            jefe._impacto(objetivo)
            self.assertEqual(objetivo.danos, [jefe.dano + 10])

        jefe._iniciar_ataque("lluvia_espadas", (900, 700))
        self.assertEqual(len(jefe.apoyos_pendientes), 0)
        partida.enemigos.actualizar(0, partida.jugador)
        apoyos = [e for e in partida.enemigos if getattr(e, "invocado_por_jefe", False)]
        self.assertEqual(len(apoyos), 3)
        self.assertEqual(zona["generados"], 1)
        zona["estado"] = "activa"
        jefe.vida = 0
        for previa in partida.oleadas.zonas[:4]:
            previa["estado"] = "completada"
        partida.jugador.rect.center = zona["rect"].center
        partida.enemigos.proyectiles.append(object())
        partida.oleadas.actualizar(0, partida.jugador, partida.enemigos)
        self.assertEqual(zona["estado"], "completada")
        self.assertEqual(zona["matados"], 1)
        self.assertEqual(partida.enemigos.lista, [jefe])
        self.assertFalse(any(e in partida.enemigos.lista for e in apoyos))
        self.assertFalse(partida.enemigos.proyectiles)

        final = partida.oleadas.zonas[-1]
        partida.oleadas._generar(final, partida.jugador, partida.enemigos)
        dragon = partida.enemigos.lista[-1]
        self.assertEqual(dragon.tipo_jefe, "dragon")
        self.assertEqual(dragon.nombre_jefe, "EL CARCELERO")
        self.assertEqual(
            dragon.vida_max, 210 * JUEGO["JEFE_DRAGON_MULTIPLICADOR_VIDA"]
        )

    def test_jefe_orco_reproduce_sonido_al_activarse_el_area_roja(self):
        partida = JUEGO["Partida"]()
        jefe = JUEGO["Jefe"](1400, 1300, tipo="orco")
        jefe.t_aparicion = 0
        sonidos = []
        estado = JUEGO["reproducir_sonido"].__globals__
        with patch.dict(
            estado,
            {"reproducir_sonido": lambda nombre, **kwargs: sonidos.append(nombre)},
        ):
            jefe._iniciar_ataque("lluvia_espadas", partida.jugador.rect.center)
            self.assertEqual(sonidos, [])
            jefe.actualizar(1.49, partida.jugador, [])
            self.assertEqual(jefe.ataque_jefe["fase"], "aviso")
            self.assertEqual(sonidos, [])
            jefe.actualizar(0.02, partida.jugador, [])
            self.assertEqual(jefe.ataque_jefe["fase"], "activo")
            self.assertEqual(sonidos, ["ataque_jefe"])

    def test_lluvia_del_orco_dibuja_armas_cayendo_con_la_camara_en_cuenta(self):
        jefe = JUEGO["Jefe"](1500, 1300, tipo="orco")
        jefe.ataque_jefe = {
            "tipo": "lluvia_espadas", "fase": "activo", "t": 0.165,
            "objetivo": (900, 700), "lado": 1, "orientacion": "vertical",
        }
        color_arma = (255, 0, 255, 255)
        jefe.imagenes_lluvia = {}
        for nombre in ("hacha", "espada"):
            imagen = pygame.Surface((80, 80), pygame.SRCALPHA)
            imagen.fill(color_arma)
            jefe.imagenes_lluvia[nombre] = imagen
        superficie = pygame.Surface((900, 1000), pygame.SRCALPHA)
        camara = (100, 50)

        jefe.dibujar(superficie, camara)

        x_mundo = 740 + round(320 * (0.5 / 13))
        y_objetivo = 180 + round(1040 * 0.25)
        y_mundo = 50 + (y_objetivo - 50) * 0.25
        posicion_arma = (round(x_mundo - camara[0]), round(y_mundo - camara[1]))
        self.assertEqual(superficie.get_at(posicion_arma), color_arma)

    def test_dragon_reserva_aliento_para_corta_distancia_y_acorta_ataques(self):
        partida = JUEGO["Partida"]()
        zona = partida.oleadas.zonas[-1]
        partida.jugador.rect.center = zona["rect"].center
        partida.oleadas._generar(zona, partida.jugador, partida.enemigos)
        dragon = partida.enemigos.lista[-1]
        dragon.t_aparicion = 0
        dragon.t_cd = 0

        partida.jugador.rect.center = (dragon.rect.centerx + 1200, dragon.rect.centery)
        dragon.actualizar(0.01, partida.jugador, [partida.jugador])
        self.assertEqual(dragon.ataque_jefe["tipo"], "meteoro")
        self.assertEqual(dragon.ataque_jefe["advertencia"], 0.8)

        dragon.ataque_jefe = None
        dragon.t_cd = 0
        partida.jugador.rect.center = (dragon.rect.centerx + 400, dragon.rect.centery)
        dragon.actualizar(0.01, partida.jugador, [partida.jugador])
        self.assertEqual(dragon.ataque_jefe["tipo"], "aliento")

        dragon.ataque_jefe = {"fase": "recuperacion", "tipo": "meteoro", "t": 0.7}
        dragon.t_cd = 0
        dragon.actualizar(0.01, partida.jugador, [partida.jugador])
        self.assertEqual(dragon.ataque_jefe, None)
        self.assertEqual(dragon.t_cd, JUEGO["JEFE_DRAGON_INTERVALO_ATAQUE"])

    def test_salir_de_una_zona_abierta_no_cancela_la_oleada(self):
        partida = JUEGO["Partida"]()
        oleadas = partida.oleadas
        zona = oleadas.zonas[0]
        zona.update(estado="activa", generados=2, matados=1, t_spawn=0.4)
        partida.jugador.rect.center = (17 * JUEGO["TAM_TILE"], 8 * JUEGO["TAM_TILE"])

        self.assertFalse(oleadas.bloquea(partida.jugador.rect))
        oleadas.actualizar(0.2, partida.jugador, partida.enemigos)
        self.assertEqual(zona["estado"], "activa")
        self.assertEqual((zona["generados"], zona["matados"]), (2, 1))
        self.assertAlmostEqual(zona["t_spawn"], 0.4)

    def test_configuracion_de_zona_selecciona_sprite_disponible(self):
        partida = JUEGO["Partida"]()
        zona = partida.oleadas.zonas[0]
        partida.jugador.rect.center = zona["rect"].center
        partida.oleadas._generar(zona, partida.jugador, partida.enemigos)
        enemigo = partida.enemigos.lista[0]
        self.assertIn(enemigo.tipo, ("goblin", "mago"))
        self.assertEqual(zona["generados"], 1)

    def test_cada_oleada_ofrece_una_mejora_y_respeta_el_nivel_maximo(self):
        partida = JUEGO["Partida"]()
        teclas = pygame.key.get_pressed()
        for indice, zona in enumerate(partida.oleadas.zonas):
            zona["estado"] = "completada"
            partida.actualizar(0, teclas)
            self.assertEqual(partida.retraso_bonificacion, JUEGO["RETARDO_ELECCION_BONIFICACION"])
            self.assertFalse(partida.bonificacion_pendiente)
            self.assertFalse(partida.terminada)
            self.assertFalse(partida.elegir_bonificacion(0))
            partida.actualizar(0.5, teclas)
            self.assertFalse(partida.bonificacion_pendiente)
            partida.actualizar(0.5, teclas)
            self.assertTrue(partida.bonificacion_pendiente)
            poder = indice % 3
            self.assertTrue(partida.elegir_bonificacion(poder))
            nivel_esperado = (indice // 3) + 1
            self.assertEqual(partida.jugador.bonificaciones[JUEGO["BONIFICACIONES"][poder][0]], nivel_esperado)
        self.assertTrue(partida.terminada)
        partida.bonificacion_pendiente = True
        self.assertFalse(partida.elegir_bonificacion(1))
        self.assertTrue(partida.bonificacion_pendiente)
        partida.dibujar(pygame.Surface((JUEGO["width"], JUEGO["height"])), False)

    def test_tajo_de_viento_usa_hitbox_del_primer_ataque(self):
        jugador = JUEGO["partida"].jugador
        objetivo = (jugador.rect.centerx + 1000, jugador.rect.centery - 20 * JUEGO["escala_jugador"])
        tajo = JUEGO["TajoViento"](jugador, objetivo)
        ancho, alto = JUEGO["HITBOX_ATAQUES"]["atacar"]
        self.assertEqual(tajo.rect.size, (ancho * JUEGO["escala_jugador"], alto * JUEGO["escala_jugador"]))
        self.assertEqual(
            tajo.rect.centery,
            jugador.rect.centery - 20 * JUEGO["escala_jugador"],
        )
        tajo.dibujar(pygame.Surface((JUEGO["width"], JUEGO["height"])))

    def test_tajo_de_viento_apunta_en_diagonal_al_objetivo(self):
        jugador = JUEGO["partida"].jugador
        jugador.rect.center = (15 * JUEGO["TAM_TILE"], 8 * JUEGO["TAM_TILE"])
        origen = pygame.Vector2(
            jugador.rect.centerx,
            jugador.rect.centery - 20 * JUEGO["escala_jugador"],
        )
        objetivo = origen + pygame.Vector2(500, 500)
        tajo = JUEGO["TajoViento"](jugador, objetivo)
        self.assertAlmostEqual(tajo.direccion.x, 2 ** -0.5)
        self.assertAlmostEqual(tajo.direccion.y, 2 ** -0.5)
        posicion_inicial = tajo.pos.copy()
        tajo.actualizar(0.1, [])
        self.assertAlmostEqual(tajo.pos.x - posicion_inicial.x, tajo.pos.y - posicion_inicial.y)

    def test_tajo_de_viento_atraviesa_objetos_solidos_del_mapa(self):
        jugador = JUEGO["partida"].jugador
        jugador.rect.center = (15 * JUEGO["TAM_TILE"], 8 * JUEGO["TAM_TILE"])
        tajo = JUEGO["TajoViento"](
            jugador,
            (jugador.rect.centerx + 1000, jugador.rect.centery - 20 * JUEGO["escala_jugador"]),
        )
        mapa = JUEGO["mapa"]
        tile = next(
            (columna, fila)
            for fila, celdas in enumerate(mapa.terreno_solido)
            for columna, solido in enumerate(celdas)
            if solido and 2 <= columna < mapa.cols - 2 and 2 <= fila < mapa.filas - 2
        )
        tajo.pos.update(
            (tile[0] + 0.5) * JUEGO["TAM_TILE"],
            (tile[1] + 0.5) * JUEGO["TAM_TILE"],
        )
        tajo._actualizar_rect()
        self.assertTrue(mapa.choca(tajo.rect))
        tajo.actualizar(0.01, [])
        self.assertFalse(tajo.eliminado)

    def test_viento_se_activa_sin_acertar_y_atraviesa_varios_enemigos(self):
        class Objetivo:
            def __init__(self, x, y):
                self.rect = pygame.Rect(0, 0, 20, 20)
                self.rect.center = (x, y)
                self.vida = 100

            def vivo(self):
                return self.vida > 0

            def cuerpo(self):
                return self.rect

            def recibir_dano(self, cantidad, origen):
                self.vida = max(0, self.vida - cantidad)
                return True

        jugador = JUEGO["partida"].jugador
        jugador.bonificaciones["viento"] = 1
        jugador.ataques_lanzados = 0
        jugador.tajo_viento_pendiente = False
        jugador.rect.center = (15 * JUEGO["TAM_TILE"], 8 * JUEGO["TAM_TILE"])
        jugador.mirando = 1
        for _ in range(3):
            jugador.empezar("atacar")
        self.assertTrue(jugador.tajo_viento_pendiente)

        objetivo = (jugador.rect.centerx + 1000, jugador.rect.centery - 20 * JUEGO["escala_jugador"])
        tajo = JUEGO["TajoViento"](jugador, objetivo)
        jugador.tajo_viento_pendiente = False
        primero = Objetivo(tajo.rect.centerx + 100, tajo.rect.centery)
        segundo = Objetivo(tajo.rect.centerx + 270, tajo.rect.centery)
        for _ in range(4):
            tajo.actualizar(0.1, [primero, segundo])
        self.assertLess(primero.vida, 100)
        self.assertLess(segundo.vida, 100)
        self.assertFalse(tajo.eliminado)

    def test_viento_y_berserker_mejoran_el_combate(self):
        jugador = JUEGO["partida"].jugador
        jugador.bonificaciones = {"viento": 1, "dano": 2, "berserker": 2}
        secuencia = []
        for _ in range(3):
            jugador.empezar("atacar")
            secuencia.append(jugador.tajo_viento_pendiente)
            jugador.tajo_viento_pendiente = False
        self.assertEqual(secuencia, [False, False, True])
        dano_base = jugador.multiplicador_dano
        self.assertAlmostEqual(dano_base, 1.3)
        self.assertTrue(jugador.activar_berserker())
        self.assertAlmostEqual(jugador.multiplicador_dano, 1.82)
        self.assertAlmostEqual(jugador.multiplicador_velocidad, 1.24)
        vida = jugador.vida
        jugador.recibir_dano(25)
        self.assertEqual(vida - jugador.vida, 19)
        self.assertFalse(jugador.activar_berserker())

    def test_berserker_dibuja_aura_solo_mientras_esta_activo(self):
        jugador = JUEGO["partida"].jugador
        tiempo_anterior = jugador.berserker_tiempo
        self.addCleanup(setattr, jugador, "berserker_tiempo", tiempo_anterior)
        jugador.rect.center = (250, 180)
        jugador.z = 0
        jugador.invulnerable = 0
        fondo = (20, 25, 30)
        sin_aura = pygame.Surface((500, 360))
        sin_aura.fill(fondo)
        jugador.berserker_tiempo = 0
        jugador.dibujar(sin_aura)

        con_aura = pygame.Surface((500, 360))
        con_aura.fill(fondo)
        jugador.berserker_tiempo = 1
        jugador.dibujar(con_aura)

        imagen_rect = jugador.imagen.get_rect(
            midbottom=(jugador.rect.centerx, jugador.rect.bottom - jugador.z)
        )
        punto_aura = (imagen_rect.left - 2, imagen_rect.centery)
        self.assertEqual(sin_aura.get_at(punto_aura)[:3], fondo)
        color_aura = con_aura.get_at(punto_aura)
        self.assertNotEqual(color_aura[:3], fondo)
        self.assertGreater(color_aura.r, color_aura.g)

    def test_ataques_del_dragon_causan_dano_en_sus_areas(self):
        class Objetivo:
            def __init__(self):
                self.rect = pygame.Rect(0, 0, 40, 40)
                self.danos = []

            def cuerpo(self):
                return self.rect

            def recibir_dano(self, cantidad, origen):
                self.danos.append(cantidad)

        jefe = JUEGO["Jefe"](1000, 1000, tipo="dragon")
        jefe.t_aparicion = 0
        jefe.mirando = 1
        for tipo in ("meteoro", "aliento", "cuerpo_a_cuerpo"):
            objetivo = Objetivo()
            if tipo == "meteoro":
                objetivo.rect.center = (1050, 1000)
                marca = tuple(objetivo.rect.center)
            elif tipo == "aliento":
                origen = jefe._origen_aliento(0)
                objetivo.rect.center = (round(origen.x + 280), round(origen.y))
                marca = tuple(objetivo.rect.center)
            else:
                objetivo.rect.center = jefe._zona_cuerpo_a_cuerpo(lado=1).center
                marca = tuple(objetivo.rect.center)
            jefe._iniciar_ataque(tipo, marca)
            if tipo == "aliento":
                jefe.ataque_jefe["angulo"] = 0
            jefe.ataque_jefe["fase"] = "activo"
            jefe._impacto(objetivo)
            self.assertEqual(len(objetivo.danos), 1, tipo)
            if tipo == "meteoro":
                self.assertEqual(jefe.radio_golpe, 150)
                self.assertEqual(jefe.imagen_meteoro.get_size(), (180, 172))
                superficie = pygame.Surface((1200, 1200))
                jefe.dibujar(superficie)
                meteor_y = int(marca[1] - 320)
                self.assertNotEqual(superficie.get_at((marca[0], meteor_y))[:3], (0, 0, 0))

    def test_aliento_del_dragon_sigue_al_jugador_y_gira_su_hitbox(self):
        partida = JUEGO["Partida"]()
        dragon = JUEGO["Jefe"](1000, 1000, tipo="dragon")
        dragon.t_aparicion = 0
        jugador = partida.jugador
        dragon._iniciar_ataque("aliento", (dragon.rect.centerx + 350, dragon.rect.centery))
        dragon.ataque_jefe["fase"] = "activo"
        dragon.ataque_jefe["t"] = 0.1

        origen = dragon._origen_aliento(0)
        punto_derecha = (round(origen.x + 300), round(origen.y))
        jugador.rect.center = (dragon.rect.centerx, dragon.rect.centery + 380)
        dragon.actualizar(0.1, jugador, [jugador])

        self.assertAlmostEqual(dragon.ataque_jefe["angulo"], math.pi / 2, delta=0.15)
        self.assertTrue(dragon.ataque_jefe["golpeo"])
        self.assertLess(jugador.vida, jugador.vida_max)
        centro_fuego = dragon._origen_aliento(dragon.ataque_jefe["angulo"])
        punto_abajo = pygame.Rect(round(centro_fuego.x - 15), round(centro_fuego.y + 280), 30, 30)
        self.assertTrue(dragon._aliento_colisiona(punto_abajo, dragon.ataque_jefe["angulo"]))
        self.assertFalse(dragon._aliento_colisiona(pygame.Rect(punto_derecha, (30, 30)), dragon.ataque_jefe["angulo"]))

        dragon.mirando = 1
        sprite_horizontal = dragon.imagenes_jefe[dragon.mirando]
        dragon.angulo_mirada = math.pi / 2
        self.assertIs(dragon.imagenes_jefe[dragon.mirando], sprite_horizontal)

    def test_jefe_es_unico_esquivable_y_cierra_la_campana(self):
        partida = JUEGO["Partida"]()
        oleadas = partida.oleadas
        zona = oleadas.zonas[-1]
        for previa in oleadas.zonas[:-1]:
            previa["estado"] = "completada"
        zona["estado"] = "activa"
        partida.jugador.rect.center = zona["rect"].center

        oleadas._generar(zona, partida.jugador, partida.enemigos)
        jefes = [e for e in partida.enemigos if getattr(e, "es_jefe", False)]
        self.assertEqual(len(jefes), 1)
        self.assertEqual((zona["generados"], zona["total"]), (1, 1))

        jefe = jefes[0]
        self.assertEqual(jefe.tipo, "dragon")
        self.assertLessEqual(jefe.imagen_jefe.get_height(), JUEGO["TAM_TILE"] * 2.5)
        self.assertLess(jefe.imagen_jefe.get_width(), JUEGO["TAM_TILE"] * 3)
        jefe.t_aparicion = 0
        jugador = partida.jugador
        jefe.t_cd = 10
        jugador.rect.centerx = jefe.rect.centerx - 400
        jefe.actualizar(0.01, jugador, partida.enemigos.lista)
        self.assertEqual(jefe.mirando, -1)
        sprite_izquierda = jefe.imagenes_jefe[-1]
        jugador.rect.centerx = jefe.rect.centerx + 400
        jefe.actualizar(0.01, jugador, partida.enemigos.lista)
        self.assertEqual(jefe.mirando, 1)
        self.assertNotEqual(
            pygame.image.tobytes(jefe.imagenes_jefe[1], "RGBA"),
            pygame.image.tobytes(sprite_izquierda, "RGBA"),
        )

        vida = partida.jugador.vida
        jefe._iniciar_ataque("meteoro", tuple(partida.jugador.rect.center))
        jefe.ataque_jefe["t"] = 1.06
        jefe.actualizar(0, jugador, partida.enemigos.lista)
        self.assertEqual(jefe.ataque_jefe["fase"], "activo")
        partida.jugador.rect.centerx += jefe.radio_golpe + 200
        jefe.actualizar(0.13, partida.jugador, partida.enemigos.lista)
        self.assertEqual(partida.jugador.vida, vida)
        for tipo in ("meteoro", "aliento", "cuerpo_a_cuerpo"):
            jefe._iniciar_ataque(tipo, tuple(partida.jugador.rect.center))
            self.assertEqual(jefe.ataque_jefe["fase"], "aviso")
            if tipo == "aliento":
                self.assertEqual(jefe.ataque_jefe["advertencia"], 1.5)
            jefe.dibujar(pygame.Surface((JUEGO["width"], JUEGO["height"])))
            jefe.ataque_jefe["fase"] = "activo"
            jefe.ataque_jefe["t"] = 0.1
            jefe.dibujar(pygame.Surface((JUEGO["width"], JUEGO["height"])))

        jefe.ataque_jefe = None
        partida.jugador.rect.center = zona["rect"].center
        jefe.recibir_dano(jefe.vida_max, partida.jugador.rect.center)
        oleadas.actualizar(0, partida.jugador, partida.enemigos)
        self.assertTrue(oleadas.victoria)
        self.assertEqual(zona["matados"], 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
