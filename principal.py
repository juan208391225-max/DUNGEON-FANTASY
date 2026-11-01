import pygame
import sys
import math
import os
import random

# Inicializa Pygame y prepara las constantes, recursos y estados compartidos
# que utiliza esta versión independiente del juego.
pygame.init()

print("---------- VARIABLES Y CONSTANTES ----------")
blanco = (255, 255, 255)
negro = (0, 0, 0)
rojo = (255, 0, 0)
azul = (0, 0, 255)
verde = (90, 200, 140)
amarillo = (255, 220, 80)
width = 1549
height = 900
RUN = True
JUGAR = False
AJUSTES = False
MUSICA = False          # sub-pantalla de ajustes: elegir canciones
PAUSA = False           # juego en pausa (Esc mientras se juega)
CONTROLES = False       # pantalla que muestra los controles
MOSTRAR_HITBOX = False  # F3: dibuja las hitboxes para depurar
CURSOR_BLOQUEADO = False  # Tab: oculta el cursor y lo encierra en la ventana (solo mientras se juega)
camara = pygame.Vector2(0, 0)   # esquina superior izquierda de lo que se ve, en coordenadas del mapa
mapa = None               # el mapa (se crea al empezar con crear_mapa())
captura = None          # foto del juego al pausar, para dibujarla de fondo
modo = None
menu_font = pygame.font.Font(None, 45)
titulo_font = pygame.font.Font(None, 110)
fuente_peq = pygame.font.Font(None, 34)
reloj = pygame.time.Clock()

# ---------- ESCALAS: tamano del jugador, los enemigos y los objetos ----------
# Cambia estos numeros para agrandar o achicar. 1 = tamano original del dibujo,
# 2 = el doble, 0.5 = la mitad. Las hitboxes, sombras y zonas de golpe se ajustan solas.
ESCALA_GLOBAL = 1       # multiplica a las otras tres: con 1.5 todo crece un 50 %
ESCALA_JUGADOR = 1
ESCALA_ENEMIGOS = 5     # el goblin mide 15x16 px en su dibujo: con 5 queda de ~80 px de alto
ESCALA_OBJETOS = 1      # para los objetos que agregues (ver escalar_imagen en FUNCIONES)
# valores finales que usa el juego (no hace falta tocarlos)
escala_jugador = ESCALA_JUGADOR * ESCALA_GLOBAL
escala_enemigos = ESCALA_ENEMIGOS * ESCALA_GLOBAL
escala_objetos = ESCALA_OBJETOS * ESCALA_GLOBAL

# ---------- MAPA ----------
# Las piezas del mapa son las de 32rogues (carpeta "mapa": tiles.png, autotiles.png y animated-tiles.png).
ESCALA_TILES = 4                  # cada casilla mide 32 px en el dibujo original: con 4 mide 128 px en el juego
TAM_TILE = 32 * ESCALA_TILES
# Plano del mapa: cada letra es una casilla. Editalo como quieras (todas las filas deben tener el mismo largo).
#   .  suelo del bosque        :  camino de tierra        ~  agua (lago: no se puede cruzar)
#   #  muro de piedra          _  suelo de losas          r  suelo de losas rojas
#   T pino alto   t arbol   y arbol joven   R roca   M hongo grande   L troncos     (bloquean el paso)
#   C cofre   B barril   J jarron   F brasero encendido                             (bloquean el paso)
#   D puerta abierta   m hongos   b huesos   p pentagrama                           (decoracion: se pueden pisar)
#   P aqui aparece el jugador      g / G  aqui aparece un goblin (en el bosque / en las ruinas)
MAPA = [
    "TtttttttttttttttttttttttttttttttttttttTt",
    "tTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTtT",
    "Tt......m...Tt........t...RTT.T.......Tt",
    "tT..............~~~~~....t.....T....t.tT",
    "Tt.T..y.T..~~~~~~~~~~~~~..R..m.y.y.M..Tt",
    "tT...M...t.~~~~~~~~~~~~~~..M....T.....tT",
    "Tt....mR...~~~~~~~~~~~~~~~...m..m....TTt",
    "tT.......R..~~~~~~~~~~~~~~~..T.....mT.tT",
    "TtT..y.......~~~~~~~~~~~~~~..yT...t...Tt",
    "tT.T............~~~~~~~~~~~...........tT",
    "Tt...................~~~~~............Tt",
    "tT.t...............t.......##..#######tT",
    "Ttt...::P::::::.....T.gR...#F__F#B__C#Tt",
    "tT....::::L::::.m.......y..#____D_b__#tT",
    "Tt............:R..M........#_b__#_G__#Tt",
    "tTT.t.........:::::::::::::#____#J__F#tT",
    "Tt.T.t.yt.....:::::::::::::D__G_###D##Tt",
    "tT.m.RT.R.........t.g.....:#____#rrrr#tT",
    "Tt.....m....M.........T....#__b_#CrbC#Tt",
    "tTttR..yy...g...T..........#____#rprr#tT",
    "Tt..m....m...t......T......#BB_J#FrCF#Tt",
    "tTy.....m..y.T.....ty..m...###########tT",
    "TtTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTt",
    "tTtttttttttttttttttttttttttttttttttttttT",
]

# ---------- CAMARA ----------
MUNDO_ANCHO = len(MAPA[0]) * TAM_TILE    # el tamano del mapa en pixeles sale del plano de arriba
MUNDO_ALTO = len(MAPA) * TAM_TILE
CAMARA_SUAVIDAD = 0         # 0 = la camara va pegada al jugador (siempre centrado). Con un numero (por ejemplo 8) lo sigue con un poco de retraso
CAMARA_LIMITADA = True      # True = la camara no sale del mapa (junto a los bordes el jugador no queda centrado). False = siempre centrado
MOSTRAR_MIRA = True         # con el cursor bloqueado (Tab) dibuja una mira pequena donde apunta el raton. False = nada

# ---------- COMBATE ----------
VIDA_ENEMIGO = 60         # vida de cada enemigo
RETROCESO_ENEMIGO = 35    # pixeles que retrocede un enemigo al recibir un golpe
# Lo que dura ese retroceso. Es el ciclo de ataque del jugador (animacion del golpe 0.30 s + enfriamiento 0.05 s):
# el enemigo se aleja y no puede recibir otro golpe hasta que el jugador puede volver a atacar.
TIEMPO_RETROCESO = 0.35

# ---------- ENEMIGOS (goblin): comportamiento ----------
VEL_ENEMIGO_VAGAR = 60            # velocidad al pasear sin haber visto al jugador
VEL_ENEMIGO_PERSEGUIR = 190       # velocidad al perseguir. El jugador camina a 300 (y corre a 520): el goblin es mas lento
RADIO_DETECCION = 380             # a que distancia (px) ve al jugador y empieza a perseguirlo
RADIO_PERDER = 650                # si el jugador se aleja mas que esto, deja de perseguirlo y vuelve a pasear
RADIO_VAGAR = 260                 # lo maximo que se aleja de su sitio mientras pasea
DANO_ENEMIGO = 12                 # dano de cada golpe suyo
ENEMIGO_PREPARAR = 0.40           # segundos que se prepara antes de golpear (parpadea en rojo: tu momento para esquivar o rodar)
ENEMIGO_GOLPE = 0.15              # segundos que dura el golpe (es cuando hace dano)
ENEMIGO_RECUPERAR = 0.35          # segundos que tarda en recuperarse despues de golpear
ENEMIGO_ENFRIAMIENTO = 0.8        # segundos extra antes de poder volver a atacar
ENEMIGO_UMBRAL_GIRO = 14          # px: si el jugador esta casi justo encima o debajo, no cambia de lado: sigue mirando hacia donde miraba
ENEMIGO_MIRA_A_LA_DERECHA = False # hacia donde mira el dibujo original (el goblin mira a la izquierda)
DANO_POR_CONTACTO = False         # True: ademas hace dano solo con tocar al jugador (cuerpo contra cuerpo)

# ---------- HITBOXES: (ancho, alto) de cada caja ----------
# Medidas en pixeles del dibujo ORIGINAL: el juego las multiplica por la escala del personaje
# (escala_jugador / escala_enemigos), asi que siguen encajando si cambias las escalas.
# Pulsa F3 en el juego para ver las cajas dibujadas y ajustarlas.
# --- jugador ---
HITBOX_JUGADOR_PIES = (20, 10)              # base en el suelo: choca con los bordes y con los enemigos (solidos)
HITBOX_JUGADOR_CUERPO = (28, 62)            # donde recibe dano, de pie (sin la cabeza)
HITBOX_JUGADOR_CUERPO_AGACHADO = (28, 32)   # donde recibe dano, agachado
# --- enemigo ---
# (medidas en pixeles del dibujo del goblin, que mide 15x16; se multiplican por escala_enemigos)
HITBOX_ENEMIGO_PIES = (9, 5)                # su base en el suelo (con esto choca el jugador)
HITBOX_ENEMIGO_CUERPO = (11, 14)            # donde recibe dano
HITBOX_ENEMIGO_ATAQUE = (14, 10)            # la zona que golpea su ataque, delante de el
HITBOX_ENEMIGO_ATAQUE_POS = (3, 8)          # (separacion horizontal desde su centro, altura del centro de la caja sobre sus pies)
# --- ataques del jugador: la zona que golpea cada uno ---
HITBOX_ATAQUES = {
    "atacar": (80, 60),
    "atacar2": (80, 60),
    "atacar_dash": (75, 45),
    "agachado_atacar": (55, 30),
    "atacar_abajo": (65, 55),
    "atacar_giro": (130, 75),
}
# donde nace la caja de cada golpe: (separacion horizontal desde el centro del jugador, altura del CENTRO de
# la caja sobre los pies). Sube la altura para subir la caja. El giro se centra en el jugador (ignora la separacion).
HITBOX_ATAQUE_POS = {
    "atacar": (5, 55),
    "atacar2": (5, 60),
    "atacar_dash": (5, 30),
    "agachado_atacar": (5, 30),
    "atacar_abajo": (5, 30),
    "atacar_giro": (5, 30),
}

# ---------- MUSICA: lista de reproduccion ----------
# Pon tus canciones (.mp3 / .ogg / .wav) en una carpeta llamada "musica"
# junto a este archivo (incluida drama.mp3).
MUSICA_EXT = (".mp3", ".ogg", ".wav")


# Reúne las pistas de audio disponibles en la carpeta configurable del menú.
def buscar_canciones():
    rutas = []
    if os.path.isdir("musica"):
        for n in sorted(os.listdir("musica")):
            if n.lower().endswith(MUSICA_EXT):
                rutas.append(os.path.join("musica", n))
    return rutas


canciones = buscar_canciones()
activas = {c: True for c in canciones}   # cuales se reproducen
actual = -1                              # indice de la cancion que suena
scroll = 0                               # desplazamiento de la lista en pantalla
FILAS_VISIBLES = 7

# valores de las opciones y posición de sus controles en coordenadas de game_surface
ajustes = {"musica": 0.5, "efectos": 0.5, "pantalla_completa": True, "mostrar_fps": False}
sliders = {   # barras de volumen
    "musica": pygame.Rect(800, 294, 400, 12),
    "efectos": pygame.Rect(800, 374, 400, 12),
}
interruptores = {
    "pantalla_completa": pygame.Rect(800, 438, 120, 48),
    "mostrar_fps": pygame.Rect(800, 518, 120, 48),
}
arrastrando = None

print("---------- VENTANA ----------")

game_surface = pygame.Surface((width, height))
ventana = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("PRISION FANTASY")


# ---------- FONDO PERSONALIZADO ----------
# Guarda tu imagen como "fondo.png" (o .jpg) junto al juego. Si no existe,
# se dibuja un degradado como fondo.
# Carga el fondo del menú si existe; si no, genera un degradado de respaldo.
def cargar_fondo():
    for ruta in ("fondo.png", "fondo.jpg", "fondo.jpeg"):
        if os.path.exists(ruta):
            img = pygame.image.load(ruta).convert()
            return pygame.transform.smoothscale(img, (width, height))
    s = pygame.Surface((width, height))
    for y in range(height):
        t = y / height
        pygame.draw.line(s, (int(20 + 30 * t), int(15 + 10 * t), int(50 + 60 * t)), (0, y), (width, y))
    return s


fondo_menu = cargar_fondo()
velo = pygame.Surface((width, height), pygame.SRCALPHA)
velo.fill((0, 0, 0, 120))   # oscurece el fondo para que se lea el texto

# botones del menú principal (rectángulos uniformes)
opciones = []
for texto, y, valor in [
    ("jugar", 390, "jugar"),
    ("controles", 465, "controles"),
    ("ajustes", 540, "ajustes"),
    ("salir", 615, "salir"),
]:
    rect = pygame.Rect(0, 0, 340, 62)
    rect.center = (width // 2, y)
    opciones.append({"texto": texto, "rect": rect, "modo": valor})

boton_canciones = pygame.Rect(0, 0, 380, 56)
boton_canciones.center = (width // 2, 620)
boton_anterior = pygame.Rect(0, 0, 260, 56)
boton_anterior.center = (width // 2 - 200, 690)
boton_siguiente = pygame.Rect(0, 0, 260, 56)
boton_siguiente.center = (width // 2 + 200, 690)
boton_volver_musica = pygame.Rect(0, 0, 260, 56)
boton_volver_musica.center = (width // 2, 780)
boton_volver_controles = pygame.Rect(0, 0, 260, 56)
boton_volver_controles.center = (width // 2, 810)

# botones del menú de pausa
opciones_pausa = []
for texto, y, valor in [
    ("reanudar", 400, "reanudar"),
    ("controles", 470, "controles"),
    ("ajustes", 540, "ajustes"),
    ("menu principal", 610, "menu"),
]:
    rect = pygame.Rect(0, 0, 400, 62)
    rect.center = (width // 2, y)
    opciones_pausa.append({"texto": texto, "rect": rect, "modo": valor})

print("------------CLASES U OBJETOS------------")

# ---------- MAPA ----------
class Prop:
    """Objeto del mapa que se dibuja ordenado por profundidad junto a los personajes (arboles, rocas, barriles...).
    'pie' es el punto del suelo donde se apoya; 'colision' = (ancho, alto) de la caja con la que bloquea el paso."""
    # Conserva sprites, punto de apoyo y colisión para dibujar cada objeto con profundidad.
    def __init__(self, frames, pie, colision=None, fps=0):
        self.frames = frames
        self.fps = fps
        self.pie = pie
        self.solido = colision is not None
        ancho, alto = colision if colision else (1, 1)
        self.rect = pygame.Rect(0, 0, int(ancho), int(alto))
        self.rect.midbottom = pie

    def dibujar(self, superficie, cam=(0, 0)):
        if self.fps and len(self.frames) > 1:
            imagen = self.frames[int(pygame.time.get_ticks() / 1000 * self.fps) % len(self.frames)]
        else:
            imagen = self.frames[0]
        superficie.blit(imagen, imagen.get_rect(midbottom=(self.pie[0] - cam[0], self.pie[1] - cam[1])))


class Mapa:
    """Mapa por casillas hecho a partir del plano de texto MAPA, con las piezas de 32rogues."""
    # Suelos: (piezas posibles, probabilidad de cada una). Las piezas son (fila, columna) de tiles.png (se cuenta desde 1).
    SUELOS = {
        "bosque": ([(14, 1), (15, 2), (15, 3), (15, 4), (14, 2), (14, 3)], [60, 10, 10, 10, 5, 5]),
        "camino": ([(9, 2), (9, 3), (9, 4)], [1, 1, 1]),
        "losa": ([(10, 2), (10, 3), (10, 4)], [1, 1, 1]),
        "losa_roja": ([(12, 2), (12, 3), (12, 4)], [1, 1, 1]),
    }
    TERRENOS = {".": "bosque", ":": "camino", "_": "losa", "r": "losa_roja"}
    MURO_SUPERIOR = (3, 1)                       # parte de arriba del muro
    MURO_FRENTE = ([(3, 2), (3, 3)], [3, 1])     # cara del muro que se ve por delante
    # Objetos que bloquean el paso: letra -> (piezas posibles, casillas de alto, caja de colision (ancho, alto) en px del dibujo original)
    OBJETOS = {
        "T": ([(25, 4)], 2, (12, 11)),
        "t": ([(26, 3)], 1, (9, 9)),
        "y": ([(26, 1), (26, 2)], 1, (6, 6)),
        "R": ([(19, 1), (19, 2)], 1, (20, 11)),
        "M": ([(21, 2)], 1, (10, 7)),
        "L": ([(18, 7)], 1, (20, 11)),
        "C": ([(18, 1)], 1, (20, 11)),
        "B": ([(18, 5)], 1, (16, 11)),
        "J": ([(18, 3)], 1, (16, 11)),
    }
    # Decoracion que se dibuja sobre el suelo y se puede pisar
    DECORADOS = {"m": [(21, 1)], "b": [(22, 1), (22, 2)], "p": [(17, 15)], "D": [(17, 4)]}
    BRASERO = 2        # fila de animated-tiles.png con el brasero encendido (6 frames)

    # Convierte el plano de caracteres en capas de suelo, decoración, colisiones y puntos de inicio.
    def __init__(self, plano):
        self.plano = plano
        self.filas = len(plano)
        self.cols = len(plano[0])
        assert all(len(f) == self.cols for f in plano), "todas las filas del plano deben tener el mismo largo"
        for base in (os.getcwd(), os.path.dirname(os.path.abspath(__file__))):
            carpeta = os.path.join(base, "mapa")
            if os.path.isdir(carpeta):
                break
        else:
            print("No encuentro la carpeta 'mapa' junto a este archivo (descomprime mapa.zip).")
            pygame.quit()
            sys.exit()
        self.hoja_tiles = pygame.image.load(os.path.join(carpeta, "tiles.png")).convert_alpha()
        self.hoja_auto = pygame.image.load(os.path.join(carpeta, "autotiles.png")).convert_alpha()
        self.hoja_anim = pygame.image.load(os.path.join(carpeta, "animated-tiles.png")).convert_alpha()
        self._cache = {}
        self.suelo = [[[] for _ in range(self.cols)] for _ in range(self.filas)]     # capas del suelo de cada casilla
        self.terreno_solido = [[False] * self.cols for _ in range(self.filas)]       # muros y agua
        self.bloqueada = [[False] * self.cols for _ in range(self.filas)]            # muros, agua y objetos solidos (para buscar caminos)
        self.bloquea_vista = [[False] * self.cols for _ in range(self.filas)]        # muros
        self.props = []
        self.solidos_en = {}                                                         # (fila, col) -> objetos solidos de esa casilla
        self.inicio = (self.cols * TAM_TILE // 2, self.filas * TAM_TILE // 2)
        self.goblins = []
        self._agua = self._autotiles(1)       # filas 1-4 de autotiles.png: agua
        self._construir()

    # ---------- piezas ----------
    # Extrae y escala una pieza del tileset; la caché evita procesarla varias veces.
    def pieza(self, fila, col, alto=1):
        """Una pieza de tiles.png (fila y columna desde 1) ya a la escala del juego."""
        clave = (fila, col, alto)
        if clave not in self._cache:
            img = self.hoja_tiles.subsurface(((col - 1) * 32, (fila - 1) * 32, 32, 32 * alto)).copy()
            self._cache[clave] = escalar_imagen(img, ESCALA_TILES)
        return self._cache[clave]

    @staticmethod
    def _firma(tile):
        """Que vecinos tiene (N, E, S, W y las 4 diagonales) una pieza del autotile, mirando donde esta transparente."""
        def opaco(x, y):
            return tile.get_at((x, y)).a > 0
        n, e, s, w = opaco(16, 0), opaco(31, 16), opaco(16, 31), opaco(0, 16)
        def esquina(x0, y0, lados):
            # la diagonal tambien es agua si la pieza no tiene la muesca en esa esquina
            if not all(lados):
                return False
            return all(tile.get_at((x, y)).a > 0 for y in range(y0, y0 + 6) for x in range(x0, x0 + 6))
        return (n, e, s, w, esquina(0, 0, (n, w)), esquina(26, 0, (n, e)), esquina(0, 26, (s, w)), esquina(26, 26, (s, e)))

    # Clasifica los autotiles según sus bordes opacos para unir correctamente el agua.
    def _autotiles(self, fila0):
        """Lee las 47 piezas del autotile (12x4 casillas desde la fila 'fila0') y las guarda segun sus vecinos."""
        piezas = {}
        for f in range(4):
            for c in range(12):
                tile = self.hoja_auto.subsurface((c * 32, (fila0 - 1 + f) * 32, 32, 32)).copy()
                if pygame.mask.from_surface(tile).count() == 0:
                    continue
                piezas.setdefault(self._firma(tile), escalar_imagen(tile, ESCALA_TILES))
        return piezas

    # ---------- construccion ----------
    def _dentro(self, x, y):
        return 0 <= x < self.cols and 0 <= y < self.filas

    def _terreno_de(self, x, y):
        """Que suelo hay en una casilla; los objetos toman el suelo mas comun de sus vecinas."""
        ch = self.plano[y][x]
        if ch in self.TERRENOS:
            return self.TERRENOS[ch]
        if ch == "D":
            return "losa"
        votos = {}
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                if self._dentro(x + dx, y + dy) and self.plano[y + dy][x + dx] in self.TERRENOS:
                    t = self.TERRENOS[self.plano[y + dy][x + dx]]
                    votos[t] = votos.get(t, 0) + 1
        return max(votos, key=votos.get) if votos else "bosque"

    def _frames_brasero(self):
        frames = []
        for c in range(self.hoja_anim.get_width() // 32):
            img = self.hoja_anim.subsurface((c * 32, (self.BRASERO - 1) * 32, 32, 32)).copy()
            if pygame.mask.from_surface(img).count() > 0:
                frames.append(escalar_imagen(img, ESCALA_TILES))
        return frames

    # Interpreta cada símbolo del plano y construye sus capas, objetos y restricciones.
    def _construir(self):
        rng = random.Random(7)
        T = TAM_TILE
        def agua(x, y):
            return not self._dentro(x, y) or self.plano[y][x] == "~"
        for y in range(self.filas):
            for x in range(self.cols):
                ch = self.plano[y][x]
                capas = self.suelo[y][x]
                centro = ((x + 0.5) * T, (y + 0.5) * T)
                pie = ((x + 0.5) * T, (y + 1) * T - 2 * ESCALA_TILES)
                if ch == "#":
                    abajo = self.plano[y + 1][x] if self._dentro(x, y + 1) else "."
                    if abajo == "#":
                        capas.append(self.pieza(*self.MURO_SUPERIOR))
                    else:
                        opciones, pesos = self.MURO_FRENTE
                        capas.append(self.pieza(*rng.choices(opciones, pesos)[0]))
                    self.terreno_solido[y][x] = self.bloqueada[y][x] = self.bloquea_vista[y][x] = True
                    continue
                opciones, pesos = self.SUELOS[self._terreno_de(x, y)] if ch != "~" else self.SUELOS["bosque"]
                capas.append(self.pieza(*rng.choices(opciones, pesos)[0]))
                if ch == "~":
                    n, e, s, w = agua(x, y - 1), agua(x + 1, y), agua(x, y + 1), agua(x - 1, y)
                    firma = (n, e, s, w, n and w and agua(x - 1, y - 1), n and e and agua(x + 1, y - 1),
                             s and w and agua(x - 1, y + 1), s and e and agua(x + 1, y + 1))
                    capas.append(self._agua.get(firma) or self._agua[(True,) * 8])
                    self.terreno_solido[y][x] = self.bloqueada[y][x] = True
                elif ch in self.DECORADOS:
                    capas.append(self.pieza(*rng.choice(self.DECORADOS[ch])))
                elif ch in self.OBJETOS:
                    piezas, alto, (cw, chh) = self.OBJETOS[ch]
                    fila, col = rng.choice(piezas)
                    prop = Prop([self.pieza(fila, col, alto)], pie, (cw * ESCALA_TILES, chh * ESCALA_TILES))
                    self.props.append(prop)
                    self.solidos_en.setdefault((y, x), []).append(prop)
                    self.bloqueada[y][x] = True
                elif ch == "F":
                    prop = Prop(self._frames_brasero(), pie, (14 * ESCALA_TILES, 9 * ESCALA_TILES), fps=8)
                    self.props.append(prop)
                    self.solidos_en.setdefault((y, x), []).append(prop)
                    self.bloqueada[y][x] = True
                elif ch == "P":
                    self.inicio = (centro[0], centro[1] + 10)
                elif ch in "gG":
                    self.goblins.append((centro[0], (y + 1) * T - 3 * ESCALA_TILES))

    # ---------- dibujo ----------
    # Dibuja únicamente las casillas visibles, transformando coordenadas de mundo a pantalla.
    def dibujar_suelo(self, superficie, cam):
        T = TAM_TILE
        superficie.fill((14, 18, 18))                  # fuera del mapa
        c0, c1 = max(0, cam[0] // T), min(self.cols - 1, (cam[0] + width) // T)
        f0, f1 = max(0, cam[1] // T), min(self.filas - 1, (cam[1] + height) // T)
        for f in range(f0, f1 + 1):
            for c in range(c0, c1 + 1):
                x, y = c * T - cam[0], f * T - cam[1]
                for capa in self.suelo[f][c]:
                    superficie.blit(capa, (x, y))

    def props_visibles(self, cam):
        """Objetos que se ven en pantalla (se dibujan junto a los personajes, ordenados por profundidad)."""
        x0, x1 = cam[0] - TAM_TILE, cam[0] + width + TAM_TILE
        y0, y1 = cam[1], cam[1] + height + 2 * TAM_TILE
        return [p for p in self.props if x0 <= p.pie[0] <= x1 and y0 <= p.pie[1] <= y1]

    def dibujar_colisiones(self, superficie, cam):
        """Depuracion (F3): casillas que bloquean (rojo) y cajas de colision de los objetos (naranja)."""
        T = TAM_TILE
        for f in range(max(0, cam[1] // T), min(self.filas, (cam[1] + height) // T + 1)):
            for c in range(max(0, cam[0] // T), min(self.cols, (cam[0] + width) // T + 1)):
                if self.terreno_solido[f][c]:
                    pygame.draw.rect(superficie, (255, 40, 40), (c * T - cam[0], f * T - cam[1], T, T), 1)
        for p in self.props_visibles(cam):
            if p.solido:
                pygame.draw.rect(superficie, (255, 160, 0), p.rect.move(-cam[0], -cam[1]), 2)

    # ---------- colisiones y caminos ----------
    # Comprueba límites, terreno bloqueado y colisiones exactas con objetos sólidos.
    def choca(self, rect):
        """True si la caja choca con un muro, agua, objeto solido o se sale del mapa."""
        T = TAM_TILE
        if rect.left < 0 or rect.top < 0 or rect.right > self.cols * T or rect.bottom > self.filas * T:
            return True
        for f in range(rect.top // T, (rect.bottom - 1) // T + 1):
            for c in range(rect.left // T, (rect.right - 1) // T + 1):
                if self.terreno_solido[f][c]:
                    return True
                for p in self.solidos_en.get((f, c), ()):
                    if rect.colliderect(p.rect):
                        return True
        return False

    def hay_vista(self, a, b):
        """True si no hay ningun muro entre los puntos a y b (los arboles y el agua no tapan la vista)."""
        T = TAM_TILE
        pasos = max(1, int(math.hypot(b[0] - a[0], b[1] - a[1]) // 32))
        for i in range(1, pasos):
            x = a[0] + (b[0] - a[0]) * i / pasos
            y = a[1] + (b[1] - a[1]) * i / pasos
            c, f = int(x // T), int(y // T)
            if self._dentro(c, f) and self.bloquea_vista[f][c]:
                return False
        return True

    def paso_libre(self, a, b, ancho, alto):
        """True si una caja de ese tamano puede ir en linea recta de a a b sin chocar con nada."""
        pasos = max(1, int(math.hypot(b[0] - a[0], b[1] - a[1]) // 16))
        caja = pygame.Rect(0, 0, int(ancho), int(alto))
        for i in range(pasos + 1):
            caja.center = (a[0] + (b[0] - a[0]) * i / pasos, a[1] + (b[1] - a[1]) * i / pasos)
            if self.choca(caja):
                return False
        return True

    # Busca una ruta ortogonal por casillas transitables y devuelve sus puntos en píxeles.
    def camino(self, a, b):
        """Ruta (lista de puntos) de a a b rodeando muros, agua y objetos. Lista vacia si no hay camino."""
        T = TAM_TILE
        ini = (min(self.filas - 1, max(0, int(a[1] // T))), min(self.cols - 1, max(0, int(a[0] // T))))
        fin = (min(self.filas - 1, max(0, int(b[1] // T))), min(self.cols - 1, max(0, int(b[0] // T))))
        if ini == fin:
            return [b]
        previo = {ini: None}
        cola = [ini]
        for f, c in cola:                                    # busqueda en anchura sobre las casillas
            if (f, c) == fin:
                break
            for df, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nf, nc = f + df, c + dc
                if self._dentro(nc, nf) and (nf, nc) not in previo and (not self.bloqueada[nf][nc] or (nf, nc) == fin):
                    previo[(nf, nc)] = (f, c)
                    cola.append((nf, nc))
        if fin not in previo:
            return []
        ruta, nodo = [], fin
        while nodo != ini:
            ruta.append(((nodo[1] + 0.5) * T, (nodo[0] + 0.5) * T))
            nodo = previo[nodo]
        ruta.reverse()
        ruta[-1] = tuple(b)
        return ruta


# ---------- ANIMACIONES DEL JUGADOR ----------
# Los frames estan en la carpeta "jugador" (quieto_1.png, quieto_2.png, ...).

# nombre de la animacion: (frames por segundo, ¿se repite?)
CONFIG_ANIM = {
    "quieto": (6, True),
    "quieto_espada": (6, True),
    "caminar": (12, True),
    "correr": (16, True),
    "empujar": (6, True),
    "pared": (6, True),
    "agacharse": (16, False),
    "agachado_quieto": (6, True),
    "agachado_atacar": (18, False),
    "atacar": (20, False),
    "atacar2": (20, False),
    "atacar_dash": (20, False),
    "atacar_giro": (24, False),
    "atacar_abajo": (22, False),
    "saltar": (10, False),
    "caer": (10, False),
    "aterrizar": (16, False),
    "rodar": (24, False),
    "herido": (14, False),
    "morir": (10, False),
    "beber": (8, False),
    "victoria": (8, True),
}

# dano que hace cada ataque a un enemigo
DANO_ATAQUE = {
    "atacar": 15,
    "atacar2": 20,
    "atacar_dash": 25,
    "agachado_atacar": 12,
    "atacar_abajo": 30,
    "atacar_giro": 25,
}


class Jugador:
    # Controla el estado completo del jugador: movimiento, animaciones, combate y supervivencia.
    def __init__(self, x, y):
        self.pos = pygame.Vector2(x, y)
        # solo los pies: es lo que se mueve y choca con los bordes
        self.rect = pygame.Rect(0, 0, int(HITBOX_JUGADOR_PIES[0] * escala_jugador), int(HITBOX_JUGADOR_PIES[1] * escala_jugador))
        self.rect.center = self.pos

        self.vel_caminar = 300      # pixeles por segundo
        self.vel_correr = 520
        self.vel_agachado = 130
        self.vel_rodar = 620
        self.vel_aire = 300         # velocidad horizontal mientras salta

        # animacion
        self.anim = "quieto"
        self.indice_frame = 0.0
        self.reversa = False        # True = reproducir al reves (para levantarse)
        self.anim_terminada = False
        self.mirando = 1            # 1 = derecha, -1 = izquierda
        self.imagen = ANIMACIONES["quieto"]["der"][0]
        # altura del personaje: la cabeza no debe salirse por arriba de la pantalla
        self.alto_cuerpo = self.imagen.get_bounding_rect().height

        # estado
        self.accion = None          # accion en curso que no se puede interrumpir (ataque, rodar...)
        self.agachado = False
        self.muerto = False
        self.z = 0.0                # altura del salto
        self.vz = 0.0
        self.en_aire = False
        self.dir_accion = pygame.Vector2(1, 0)   # direccion del rodar / embestida
        self.empuje = pygame.Vector2(0, 0)       # retroceso al ser herido
        self.combo = 0
        self.t_combo = 0.0          # tiempo para encadenar el siguiente golpe
        self.tiempo_espada = 0.0    # mientras sea > 0 se ve con la espada en mano
        self.cd_giro = 0.0
        self.vida_max = 100
        self.vida = self.vida_max
        self.vida_visible = float(self.vida_max)   # la barra blanca que baja despacio tras un golpe
        self.invulnerable = 0.0                    # segundos sin poder recibir dano tras un golpe
        self.golpeados = set()                     # enemigos ya golpeados por el ataque actual
        self.celebrar_pendiente = False
        self.victoria_hecha = False
        self.prev = {}              # teclas del frame anterior (para detectar "recien pulsada")
        # 0.3 para no atacar al instante con el mismo clic con el que se elige "jugar" en el menu
        self.enfriamiento = 0.3

    # ---------- animacion ----------
    # Cambia la animación activa y reinicia su fotograma solo cuando corresponde.
    def poner_anim(self, nombre, reversa=False, reiniciar=False):
        if reiniciar or nombre != self.anim or reversa != self.reversa:
            self.anim = nombre
            self.reversa = reversa
            self.anim_terminada = False
            n = len(ANIMACIONES[nombre]["der"])
            self.indice_frame = n - 0.001 if reversa else 0.0

    def avanzar_anim(self, dt):
        fps, repite = CONFIG_ANIM[self.anim]
        n = len(ANIMACIONES[self.anim]["der"])
        if self.reversa:
            self.indice_frame -= fps * dt
            if self.indice_frame < 0:
                if repite:
                    self.indice_frame += n
                else:
                    self.indice_frame = 0.0
                    self.anim_terminada = True
        else:
            self.indice_frame += fps * dt
            if self.indice_frame >= n:
                if repite:
                    self.indice_frame %= n
                else:
                    self.indice_frame = n - 0.001   # se queda en el ultimo frame
                    self.anim_terminada = True

    def progreso(self):
        """0 -> 1 mientras avanza la animacion actual."""
        n = len(ANIMACIONES[self.anim]["der"])
        p = self.indice_frame / n
        return 1 - p if self.reversa else p

    def elegir_imagen(self):
        frames = ANIMACIONES[self.anim]["der" if self.mirando == 1 else "izq"]
        self.imagen = frames[min(int(self.indice_frame), len(frames) - 1)]

    # ---------- acciones ----------
    def empezar(self, nombre, lado=None):
        self.accion = nombre
        if nombre in HITBOX_ATAQUES:
            self.golpeados = set()      # cada ataque golpea una sola vez a cada enemigo
        if lado is not None:
            self.mirando = lado
        if nombre == "levantarse":
            self.poner_anim("agacharse", reversa=True, reiniciar=True)
        else:
            self.poner_anim(nombre, reiniciar=True)

    # Aplica daño, invulnerabilidad y retroceso según la fuente del impacto.
    def recibir_dano(self, cantidad=10, origen=None):
        """Quita vida y lanza la animacion de herido. 'origen' es de donde viene el golpe
        (el jugador retrocede en sentido contrario). Devuelve True si el golpe entro."""
        if self.muerto or self.accion == "rodar" or self.invulnerable > 0:   # rodando no te hacen dano
            return False
        self.vida = max(0, self.vida - cantidad)
        self.invulnerable = 1.2
        if self.vida <= 0:
            self.morir()
            return True
        self.agachado = False
        retroceso = pygame.Vector2(-self.mirando, 0)
        if origen is not None:
            alejar = pygame.Vector2(self.rect.center) - pygame.Vector2(origen)
            if alejar.length() > 0:
                retroceso = alejar.normalize()
        self.empuje = retroceso * 320
        self.empezar("herido")
        return True

    def morir(self):
        self.muerto = True
        self.accion = None
        self.agachado = False
        self.z, self.vz, self.en_aire = 0.0, 0.0, False
        self.poner_anim("morir", reiniciar=True)

    def celebrar(self):
        """Pide la pose de victoria (una sola vez). Empieza cuando el jugador esta libre y quieto."""
        if not self.victoria_hecha and not self.muerto:
            self.victoria_hecha = True
            self.celebrar_pendiente = True

    def cuerpo(self):
        """Hitbox del cuerpo (la zona donde puede recibir dano): de los pies al cuello, SIN la cabeza.
        Sigue al personaje cuando salta y se acorta cuando esta agachado.
        Medidas en las variables HITBOX_JUGADOR_CUERPO y HITBOX_JUGADOR_CUERPO_AGACHADO."""
        ancho, alto = HITBOX_JUGADOR_CUERPO_AGACHADO if self.agachado else HITBOX_JUGADOR_CUERPO
        zona = pygame.Rect(0, 0, int(ancho * escala_jugador), int(alto * escala_jugador))
        zona.midbottom = (self.rect.centerx, self.rect.bottom - self.z)
        return zona

    def hitbox(self):
        """Zona que golpea el ataque actual. None si no esta atacando."""
        if self.accion not in HITBOX_ATAQUES:
            return None
        n = len(ANIMACIONES[self.anim]["der"])
        if not 1 <= int(self.indice_frame) <= n - 2:    # solo en los frames del golpe
            return None
        ancho, alto = HITBOX_ATAQUES[self.accion]
        zona = pygame.Rect(0, 0, int(ancho * escala_jugador), int(alto * escala_jugador))
        separacion, altura = HITBOX_ATAQUE_POS[self.accion]
        y = self.rect.bottom - altura * escala_jugador - self.z
        if self.accion == "atacar_giro":
            zona.center = (self.rect.centerx, y)
        elif self.mirando == 1:
            zona.midleft = (self.rect.centerx + separacion * escala_jugador, y)
        else:
            zona.midright = (self.rect.centerx - separacion * escala_jugador, y)
        return zona

    def pulsaciones(self, teclas, raton):
        """Devuelve las teclas de accion que se acaban de pulsar en este frame."""
        ahora = {
            "saltar": teclas[pygame.K_SPACE],
            "rodar": teclas[pygame.K_r],
            "giro": teclas[pygame.K_e] or raton[2],
            "beber": teclas[pygame.K_q],
        }
        nuevas = {k: bool(v) and not self.prev.get(k, False) for k, v in ahora.items()}
        self.prev = {k: bool(v) for k, v in ahora.items()}
        return nuevas

    # Prioriza acciones no interrumpibles y decide la animación/ataque a partir de controles.
    def decidir_accion(self, nuevas, ataca, mueve, corre, direccion, lado_raton, quiere_agachar):
        """Se llama cuando el jugador esta libre: elige si empieza alguna accion."""
        if self.agachado:
            if nuevas["rodar"]:
                self.agachado = False
                self.iniciar_rodar(direccion)
            elif ataca:
                self.empezar("agachado_atacar", lado_raton)
            elif not quiere_agachar:
                self.empezar("levantarse")
            return

        if self.en_aire:
            if ataca:
                self.empezar("atacar_abajo", lado_raton)
            return

        if nuevas["saltar"]:
            self.en_aire = True
            self.vz = 820
            self.z = 1.0
            self.vel_aire = self.vel_correr if corre else self.vel_caminar
            self.poner_anim("saltar", reiniciar=True)
        elif nuevas["rodar"]:
            self.iniciar_rodar(direccion)
        elif nuevas["giro"] and self.cd_giro <= 0:
            self.cd_giro = 0.6
            self.empezar("atacar_giro", lado_raton)
        elif nuevas["beber"]:
            self.empezar("beber")
        elif self.celebrar_pendiente and not mueve and not ataca:
            self.celebrar_pendiente = False
            self.empezar("victoria")
        elif ataca:
            if corre:
                # embestida hacia donde apunta el raton
                centro = pygame.Vector2(self.rect.centerx, self.rect.bottom - 40)
                objetivo = pos_raton_mundo() - centro
                self.dir_accion = objetivo.normalize() if objetivo.length() > 0 else pygame.Vector2(lado_raton, 0)
                self.empezar("atacar_dash", lado_raton)
            else:
                if self.t_combo <= 0:
                    self.combo = 0          # paso mucho tiempo: vuelve al primer golpe
                self.empezar(("atacar", "atacar2")[self.combo], lado_raton)
                self.combo = 1 - self.combo
        elif quiere_agachar:
            self.empezar("agacharse")

    def iniciar_rodar(self, direccion):
        self.dir_accion = pygame.Vector2(direccion) if direccion.length() > 0 else pygame.Vector2(self.mirando, 0)
        lado = self.mirando
        if self.dir_accion.x != 0:
            lado = 1 if self.dir_accion.x > 0 else -1
        self.empezar("rodar", lado)

    # ---------- bucle ----------
    # Desplaza al jugador en pasos pequeños para resolver colisiones con el mapa.
    def _mover_chocando(self, paso):
        """Avanza 'paso' pixeles sin atravesar muros, agua ni objetos del mapa (se desliza por los lados)."""
        atascado = mapa_choca(self.rect)           # si ya esta dentro de algo (al reaparecer), que pueda salir
        for eje in (0, 1):
            d = paso[eje]
            if d == 0:
                continue
            self.pos[eje] += d
            self.rect.center = self.pos
            if not atascado and mapa_choca(self.rect):
                self.pos[eje] -= d
                signo = 1 if d > 0 else -1
                for _ in range(int(abs(d))):       # acercarse hasta tocar el obstaculo
                    self.pos[eje] += signo
                    self.rect.center = self.pos
                    if mapa_choca(self.rect):
                        self.pos[eje] -= signo
                        break
        self.rect.center = self.pos

    # Actualiza temporizadores, entrada, física, colisiones y animación durante un fotograma.
    def actualizar(self, teclas, dt):
        self.enfriamiento -= dt
        self.cd_giro -= dt
        self.t_combo -= dt
        self.tiempo_espada -= dt
        self.invulnerable -= dt
        if self.vida_visible > self.vida:       # la barra blanca alcanza a la roja poco a poco
            self.vida_visible = max(self.vida, self.vida_visible - 40 * dt)
        else:
            self.vida_visible = self.vida
        raton = pygame.mouse.get_pressed()
        nuevas = self.pulsaciones(teclas, raton)

        # ----- muerto: se queda en el suelo (el juego se reinicia con Enter)
        if self.muerto:
            self.poner_anim("morir")
            self.avanzar_anim(dt)
            self.elegir_imagen()
            return

        dx = (teclas[pygame.K_d] or teclas[pygame.K_RIGHT]) - (teclas[pygame.K_a] or teclas[pygame.K_LEFT])
        dy = (teclas[pygame.K_s] or teclas[pygame.K_DOWN]) - (teclas[pygame.K_w] or teclas[pygame.K_UP])
        direccion = pygame.Vector2(dx, dy)
        mueve = direccion.length() > 0
        if mueve:
            direccion = direccion.normalize()   # evita ir mas rapido en diagonal
        corre = mueve and (teclas[pygame.K_LSHIFT] or teclas[pygame.K_RSHIFT])
        quiere_agachar = teclas[pygame.K_c] or teclas[pygame.K_LCTRL]
        lado_raton = -1 if pos_raton_mundo().x < self.rect.centerx else 1
        ataca = raton[0] and self.enfriamiento <= 0

        # la pose de victoria se corta con cualquier movimiento, ataque o accion
        if self.accion == "victoria" and (mueve or ataca or any(nuevas.values())):
            self.accion = None
        if self.accion is None:
            self.decidir_accion(nuevas, ataca, mueve, corre, direccion, lado_raton, quiere_agachar)

        # ----- movimiento segun lo que este haciendo
        a = self.accion
        p = self.progreso()
        mov = pygame.Vector2(0, 0)
        if a == "rodar":
            mov = self.dir_accion * self.vel_rodar * (1 - 0.5 * p)
        elif a == "atacar_dash":
            mov = self.dir_accion * 520 * max(0.0, 1 - 1.4 * p)
        elif a == "atacar_giro":
            mov = direccion * self.vel_caminar * 0.5
        elif a == "atacar_abajo":
            mov = direccion * self.vel_aire * 0.5 if self.en_aire else mov
        elif a == "herido":
            mov = self.empuje * (1 - p)
        elif a is None:
            if self.en_aire:
                mov = direccion * self.vel_aire
            elif self.agachado:
                mov = direccion * self.vel_agachado
            else:
                mov = direccion * (self.vel_correr if corre else self.vel_caminar)
        self._mover_chocando(mov * dt)
        # Mantener dentro del mapa (la cabeza del personaje tambien debe verse)
        area = pygame.Rect(0, self.alto_cuerpo - self.rect.h, MUNDO_ANCHO, MUNDO_ALTO - self.alto_cuerpo + self.rect.h)
        self.rect.clamp_ip(area)
        self.pos.update(self.rect.center)
        toca_izq = self.rect.left <= 0 and direccion.x < 0
        toca_der = self.rect.right >= MUNDO_ANCHO and direccion.x > 0
        contra_pared = toca_izq or toca_der

        # ----- salto (gravedad)
        if self.en_aire:
            g = 3800 if self.accion == "atacar_abajo" else 2400
            self.vz -= g * dt
            self.z += self.vz * dt
            if self.z <= 0:
                self.z, self.vz, self.en_aire = 0.0, 0.0, False
                if self.accion is None:
                    self.empezar("aterrizar")

        # ----- que animacion toca si no esta haciendo ninguna accion
        if self.accion is None:
            if self.en_aire:
                if contra_pared:
                    self.mirando = 1 if toca_der else -1
                    self.poner_anim("pared")
                else:
                    self.mirando = lado_raton
                    self.poner_anim("saltar" if self.vz > 0 else "caer")
            elif self.agachado:
                self.mirando = lado_raton
                self.poner_anim("agachado_quieto")
            elif contra_pared:
                self.mirando = 1 if toca_der else -1
                self.poner_anim("empujar")
            elif mueve and corre:
                self.mirando = (1 if direccion.x > 0 else -1) if direccion.x != 0 else lado_raton
                self.poner_anim("correr")
            elif mueve:
                self.mirando = lado_raton      # el jugador mira hacia donde esta el raton
                self.poner_anim("caminar")
            else:
                self.mirando = lado_raton
                self.poner_anim("quieto_espada" if self.tiempo_espada > 0 else "quieto")

        self.avanzar_anim(dt)

        # ----- fin de la accion cuando termina su animacion
        if self.accion is not None and self.anim_terminada:
            terminada = self.accion
            self.accion = None
            if terminada == "agacharse":
                self.agachado = True
            elif terminada == "levantarse":
                self.agachado = False
            elif terminada in HITBOX_ATAQUES:
                self.enfriamiento = 0.05
                self.t_combo = 0.5
                self.tiempo_espada = 3.0       # se queda con la espada en mano un rato

        self.elegir_imagen()

    def dibujar(self, superficie, cam=(0, 0)):
        # sombra en el suelo (se encoge cuando el jugador salta)
        factor = max(0.4, 1 - self.z / 400)
        sombra = pygame.Surface((max(1, int(30 * escala_jugador * factor)), max(1, int(9 * escala_jugador * factor))), pygame.SRCALPHA)
        pygame.draw.ellipse(sombra, (0, 0, 0, 90), sombra.get_rect())
        superficie.blit(sombra, sombra.get_rect(center=(self.rect.centerx - cam[0], self.rect.bottom - 2 - cam[1])))
        imagen = self.imagen
        if self.invulnerable > 0 and not self.muerto and self.accion != "rodar":
            if int(self.invulnerable * 16) % 2 == 0:   # parpadea mientras es invulnerable
                imagen = con_transparencia(imagen, 110)
        superficie.blit(imagen, imagen.get_rect(midbottom=(self.rect.centerx - cam[0], self.rect.bottom - self.z - cam[1])))


class Enemigo:
    # Enemigo básico con patrulla, detección, persecución, ataque y retroceso.
    """Goblin: pasea al azar hasta ver al jugador; entonces lo persigue (mas lento que el) y lo ataca.
    Siempre mira al jugador. Se le puede golpear y retrocede un poco al recibir un golpe."""
    def __init__(self, x, y):
        # medidas en pixeles del dibujo original: se multiplican por escala_enemigos
        self.rect = pygame.Rect(0, 0, int(HITBOX_ENEMIGO_PIES[0] * escala_enemigos), int(HITBOX_ENEMIGO_PIES[1] * escala_enemigos))   # su base en el suelo (con esto choca el jugador)
        self.rect.midbottom = (x, y)
        self.pos = pygame.Vector2(self.rect.midbottom)
        self.casa = pygame.Vector2(self.rect.midbottom)   # su sitio: de aqui no se aleja mucho al pasear
        self.dano = DANO_ENEMIGO
        self.vida_max = VIDA_ENEMIGO
        self.vida = self.vida_max
        # imagenes: normal, en alerta (rojo, al prepararse a golpear) y destello (blanco, al recibir un golpe), mirando a cada lado
        base = escalar_imagen(cargar_sprite_enemigo("goblin"), escala_enemigos)
        alerta = base.copy()
        alerta.fill((150, 0, 0, 0), special_flags=pygame.BLEND_RGB_ADD)
        destello = base.copy()
        destello.fill((170, 170, 170, 0), special_flags=pygame.BLEND_RGB_ADD)
        self.imagenes = {}
        for nombre, img in (("normal", base), ("alerta", alerta), ("destello", destello)):
            volteada = pygame.transform.flip(img, True, False)
            der, izq = (img, volteada) if ENEMIGO_MIRA_A_LA_DERECHA else (volteada, img)
            self.imagenes[(nombre, 1)] = der
            self.imagenes[(nombre, -1)] = izq
        self.alto_img = base.get_height()
        # estado
        self.estado = "vagar"                       # "vagar" (pasea al azar) o "perseguir"
        self.mirando = random.choice((-1, 1))       # 1 = derecha, -1 = izquierda
        self.t_vagar = random.uniform(0.2, 1.2)     # tiempo que le queda a lo que esta haciendo al pasear
        self.dir_vagar = pygame.Vector2(0, 0)       # rumbo al pasear (0,0 = parado)
        self.ataque = None                          # {"fase", "t", "golpeo", "lado"} mientras ataca
        self.t_cd = random.uniform(0.0, 0.5)        # enfriamiento entre ataques
        self.ruta = []                              # camino que sigue para rodear obstaculos al perseguir
        self.t_ruta = 0.0                           # tiempo hasta recalcular la ruta
        self.retroceso = pygame.Vector2(0, 0)       # velocidad del retroceso al recibir un golpe
        self.t_retroceso = 0.0                      # tiempo de retroceso que queda
        self.t_muerte = None                        # segundos desde que murio (se desvanece)
        self.eliminado = False                      # True cuando ya se puede quitar de la lista

    def vivo(self):
        return self.vida > 0

    def cuerpo(self):
        """Hitbox de cuerpo completo del enemigo."""
        zona = pygame.Rect(0, 0, int(HITBOX_ENEMIGO_CUERPO[0] * escala_enemigos), int(HITBOX_ENEMIGO_CUERPO[1] * escala_enemigos))
        zona.midbottom = self.rect.midbottom
        return zona

    def zona_ataque(self, lado):
        """Caja que golpea su ataque, delante de el (lado: 1 derecha, -1 izquierda)."""
        ancho, alto = HITBOX_ENEMIGO_ATAQUE
        separacion, altura = HITBOX_ENEMIGO_ATAQUE_POS
        zona = pygame.Rect(0, 0, int(ancho * escala_enemigos), int(alto * escala_enemigos))
        y = self.rect.bottom - altura * escala_enemigos
        if lado == 1:
            zona.midleft = (self.rect.centerx + separacion * escala_enemigos, y)
        else:
            zona.midright = (self.rect.centerx - separacion * escala_enemigos, y)
        return zona

    def recibir_dano(self, cantidad, origen):
        """Quita vida y lo empuja lejos de 'origen'. Devuelve True si el golpe entro.
        Mientras retrocede no puede recibir otro golpe (asi cada ataque cuenta una vez).
        Un golpe lo interrumpe si estaba atacando, y hace que persiga al jugador."""
        if not self.vivo() or self.t_retroceso > 0:
            return False
        self.vida = max(0, self.vida - cantidad)
        alejar = pygame.Vector2(self.rect.center) - pygame.Vector2(origen)
        if alejar.length() == 0:
            alejar = pygame.Vector2(1, 0)
        self.t_retroceso = TIEMPO_RETROCESO
        # empieza rapido y frena hasta parar: en total recorre RETROCESO_ENEMIGO pixeles
        self.retroceso = alejar.normalize() * (2 * RETROCESO_ENEMIGO / TIEMPO_RETROCESO)
        self.ataque = None
        self.estado = "perseguir"
        if self.vida <= 0:
            self.t_muerte = 0.0
        return True

    def _area(self):
        """Zona por la que puede andar (que ni el cuerpo ni la cabeza se salgan de la pantalla)."""
        return pygame.Rect(0, self.alto_img - self.rect.h, MUNDO_ANCHO, MUNDO_ALTO - self.alto_img + self.rect.h)

    def _mover(self, direccion, vel, dt, obstaculos):
        """Anda en 'direccion' sin meterse en los obstaculos (el jugador y otros goblins).
        Devuelve True si llego a moverse."""
        antes = pygame.Vector2(self.pos)
        paso = direccion * vel * dt
        atascado = self.rect.collidelist(obstaculos) != -1 or mapa_choca(self.rect)   # si ya se solapa con algo, que pueda salir
        for eje in (0, 1):                                      # por ejes: asi se desliza por los lados
            self.pos[eje] += paso[eje]
            self.rect.midbottom = self.pos
            if not atascado and (self.rect.collidelist(obstaculos) != -1 or mapa_choca(self.rect)):
                self.pos[eje] -= paso[eje]
        self.rect.midbottom = self.pos
        antes_rect = self.rect.copy()
        self.rect.clamp_ip(self._area())
        if self.rect != antes_rect:                             # topo con el borde de la pantalla
            self.pos.update(self.rect.midbottom)
        return (self.pos - antes).length() > 0.01

    def _retroceder(self, dt):
        paso = self.retroceso * (self.t_retroceso / TIEMPO_RETROCESO) * dt
        for eje in (0, 1):                                      # el retroceso tampoco atraviesa muros ni objetos
            self.pos[eje] += paso[eje]
            self.rect.midbottom = self.pos
            if mapa_choca(self.rect):
                self.pos[eje] -= paso[eje]
        self.rect.midbottom = self.pos
        antes_rect = self.rect.copy()
        self.rect.clamp_ip(self._area())
        if self.rect != antes_rect:
            self.pos.update(self.rect.midbottom)
        self.t_retroceso -= dt

    # Elige y recorre destinos cercanos cuando el jugador no está a su alcance.
    def _vagar(self, dt, obstaculos):
        """Antes de ver al jugador: camina un rato en una direccion al azar, descansa, y repite."""
        self.t_vagar -= dt
        if self.t_vagar <= 0:
            if self.dir_vagar.length() > 0:                    # estaba andando: descansa un rato
                self.dir_vagar = pygame.Vector2(0, 0)
                self.t_vagar = random.uniform(0.6, 1.8)
            else:                                              # estaba parado: elige un rumbo al azar
                angulo = random.uniform(0, 2 * math.pi)
                lejos = self.casa - pygame.Vector2(self.rect.midbottom)
                if lejos.length() > RADIO_VAGAR:               # se alejo mucho: vuelve hacia su sitio
                    angulo = math.atan2(lejos.y, lejos.x) + random.uniform(-0.8, 0.8)
                self.dir_vagar = pygame.Vector2(math.cos(angulo), math.sin(angulo))
                self.t_vagar = random.uniform(0.6, 1.6)
        if self.dir_vagar.length() > 0:
            if abs(self.dir_vagar.x) > 0.25:                   # mira hacia donde camina
                self.mirando = 1 if self.dir_vagar.x > 0 else -1
            if not self._mover(self.dir_vagar, VEL_ENEMIGO_VAGAR, dt, obstaculos):
                self.t_vagar = 0                               # choco con algo: cambia de idea

    # Acerca al enemigo al jugador usando el camino calculado alrededor de obstáculos.
    def _perseguir(self, dt, jugador, obstaculos):
        yo = pygame.Vector2(self.rect.center)
        el = pygame.Vector2(jugador.rect.center)
        dx = el.x - yo.x
        # siempre mira al jugador; si esta casi justo encima o debajo, mantiene hacia donde miraba
        if abs(dx) > ENEMIGO_UMBRAL_GIRO:
            self.mirando = 1 if dx > 0 else -1
        if self.t_cd <= 0 and self.zona_ataque(self.mirando).colliderect(jugador.cuerpo()):
            self.ataque = {"fase": "preparar", "t": 0.0, "golpeo": False, "lado": self.mirando}
            return
        destino = el
        if mapa is not None and not mapa.paso_libre(self.rect.center, jugador.rect.center, self.rect.w, self.rect.h):
            # hay algo en medio: sigue una ruta que lo rodea (se recalcula cada poco)
            self.t_ruta -= dt
            if self.t_ruta <= 0 or not self.ruta:
                self.ruta = mapa.camino(self.rect.center, jugador.rect.center)
                self.t_ruta = 0.4
            while len(self.ruta) > 1 and (pygame.Vector2(self.ruta[0]) - yo).length() < 24:
                self.ruta.pop(0)
            if self.ruta:
                destino = pygame.Vector2(self.ruta[0])
        else:
            self.ruta = []
        if (destino - yo).length() > 1:
            self._mover((destino - yo).normalize(), VEL_ENEMIGO_PERSEGUIR, dt, obstaculos)

    # Ejecuta preparación, ventana de daño y recuperación del ataque enemigo.
    def _atacar(self, dt, jugador):
        """Ataque en tres fases: se prepara (aviso), golpea (hace dano) y se recupera."""
        a = self.ataque
        a["t"] += dt
        if a["fase"] == "preparar":
            if a["t"] >= ENEMIGO_PREPARAR:
                a["fase"], a["t"] = "golpe", 0.0
        elif a["fase"] == "golpe":
            if not a["golpeo"] and not jugador.muerto and self.zona_ataque(a["lado"]).colliderect(jugador.cuerpo()):
                a["golpeo"] = True                             # un golpe solo hace dano una vez
                jugador.recibir_dano(self.dano, self.rect.center)
            if a["t"] >= ENEMIGO_GOLPE:
                a["fase"], a["t"] = "recuperar", 0.0
        elif a["t"] >= ENEMIGO_RECUPERAR:
            self.ataque = None
            self.t_cd = ENEMIGO_ENFRIAMIENTO

    # Coordina IA, movimiento, ataques y separación respecto a otros enemigos.
    def actualizar(self, dt, jugador, otros):
        self.t_cd -= dt
        if self.t_retroceso > 0:
            self._retroceder(dt)
        if self.t_muerte is not None:
            self.t_muerte += dt
            if self.t_muerte >= 0.6:
                self.eliminado = True
            return
        if self.t_retroceso > 0:                               # herido: no hace nada hasta recuperarse
            return
        if self.ataque is not None:
            self._atacar(dt, jugador)
            return
        yo = pygame.Vector2(self.rect.center)
        distancia = (pygame.Vector2(jugador.rect.center) - yo).length()
        if self.estado == "vagar":
            if (distancia < RADIO_DETECCION and not jugador.muerto and             # lo ve: empieza a perseguirlo
                    (distancia < RADIO_DETECCION / 2 or mapa is None or mapa.hay_vista(self.rect.center, jugador.rect.center))):
                self.estado = "perseguir"
        elif distancia > RADIO_PERDER or jugador.muerto:               # lo perdio de vista
            self.estado = "vagar"
            self.t_vagar, self.dir_vagar = 0.0, pygame.Vector2(0, 0)
        obstaculos = [jugador.rect] + [o.rect for o in otros if o is not self and o.vivo()]
        if self.estado == "perseguir":
            self._perseguir(dt, jugador, obstaculos)
        else:
            self._vagar(dt, obstaculos)

    def _desplazamiento(self):
        """Cuanto se corre el dibujo hacia delante/atras durante el ataque: se echa atras al prepararse y se lanza al golpear."""
        a = self.ataque
        if a is None:
            return 0
        if a["fase"] == "preparar":
            return -a["lado"] * 3 * escala_enemigos * (a["t"] / ENEMIGO_PREPARAR)
        if a["fase"] == "golpe":
            return a["lado"] * 5 * escala_enemigos
        return a["lado"] * 5 * escala_enemigos * (1 - a["t"] / ENEMIGO_RECUPERAR)

    def dibujar(self, superficie, cam=(0, 0)):
        sombra = pygame.Surface((int(self.rect.w * 1.5), int(self.rect.h * 1.1)), pygame.SRCALPHA)
        pygame.draw.ellipse(sombra, (0, 0, 0, 90), sombra.get_rect())
        superficie.blit(sombra, sombra.get_rect(center=(self.rect.centerx - cam[0], self.rect.bottom - 2 - cam[1])))
        lado = self.ataque["lado"] if self.ataque else self.mirando
        variante = "normal"
        if self.t_retroceso > TIEMPO_RETROCESO - 0.12:                   # destello blanco justo al recibir el golpe
            variante = "destello"
        elif self.ataque and self.ataque["fase"] == "preparar":          # parpadea en rojo: va a golpear
            variante = "alerta" if int(self.ataque["t"] * 16) % 2 == 0 else "normal"
        imagen = self.imagenes[(variante, lado)]
        if self.t_muerte is not None:                                    # al morir se desvanece
            imagen = con_transparencia(imagen, 255 * max(0.0, 1 - self.t_muerte / 0.6))
        pos_img = imagen.get_rect(midbottom=(self.rect.centerx + self._desplazamiento() - cam[0], self.rect.bottom - cam[1]))
        superficie.blit(imagen, pos_img)
        if self.vivo() and self.vida < self.vida_max:                    # barra de vida solo cuando ya fue golpeado
            ancho, alto = imagen.get_width(), max(4, int(1.6 * escala_enemigos))
            barra = pygame.Rect(0, 0, ancho, alto)
            barra.midbottom = (self.rect.centerx - cam[0], pos_img.top - 6)
            pygame.draw.rect(superficie, (35, 10, 14), barra)
            pygame.draw.rect(superficie, (210, 40, 55), (barra.x, barra.y, int(ancho * self.vida / self.vida_max), alto))
            pygame.draw.rect(superficie, blanco, barra, 2)


print("---------- FUNCIONES ----------")
# Escala la superficie lógica al tamaño de la ventana física.
def blit_scaled():
    scaled = pygame.transform.scale(game_surface, ventana.get_size())
    ventana.blit(scaled, (0, 0))


def dibujar_texto(texto, color, y):
    # Renderiza el rótulo centrado en la superficie interna.
    render = menu_font.render(texto, True, color)
    game_surface.blit(render, render.get_rect(center=(width // 2, y)))


# Convierte coordenadas de ventana a las coordenadas internas usadas por la interfaz.
def pos_en_juego(pos):
    """Convierte una posición de la pantalla real a la de game_surface."""
    sx, sy = ventana.get_size()
    return (pos[0] * width / sx, pos[1] * height / sy)


# zona clicable de un botón de texto (el texto con un margen)
def zona_boton(texto, y):
    # Calcula el área de clic ampliada respecto del texto para facilitar la selección.
    return menu_font.render(texto, True, blanco).get_rect(center=(width // 2, y)).inflate(60, 24)


# dibuja un botón de texto que cambia de color cuando el ratón está encima
def dibujar_boton(texto, color, color_hover, y):
    # Dibuja el rótulo con un color diferente cuando el cursor está sobre su zona activa.
    zona = zona_boton(texto, y)
    encima = zona.collidepoint(pos_en_juego(pygame.mouse.get_pos()))   # ¿el ratón está dentro?
    dibujar_texto(texto, color_hover if encima else color, y)
    return zona


# botón con caja redondeada (menú principal y pantalla de canciones)
# Dibuja un botón rectangular y cambia su aspecto cuando el puntero lo señala.
def dibujar_boton_caja(texto, rect):
    encima = rect.collidepoint(pos_en_juego(pygame.mouse.get_pos()))
    relleno = (70, 60, 110) if encima else (35, 30, 60)
    borde = amarillo if encima else (150, 150, 190)
    pygame.draw.rect(game_surface, relleno, rect, border_radius=14)
    pygame.draw.rect(game_surface, borde, rect, width=3, border_radius=14)
    render = menu_font.render(texto, True, amarillo if encima else blanco)
    game_surface.blit(render, render.get_rect(center=rect.center))


def dibujar_fondo():
    # Compone la imagen/degradado y el velo translúcido del fondo de menú.
    game_surface.blit(fondo_menu, (0, 0))
    game_surface.blit(velo, (0, 0))


# ---------- MUSICA ----------
# Sincroniza el volumen de la lista musical con la opción guardada en ajustes.
def aplicar_volumen():
    if pygame.mixer.get_init():   # por si el PC no tiene audio disponible
        pygame.mixer.music.set_volume(ajustes["musica"])


def nombre_cancion(ruta):
    # Elimina ruta y extensión para mostrar solo el nombre legible de la pista.
    return os.path.splitext(os.path.basename(ruta))[0]


def hay_activas():
    # Informa si queda al menos una canción habilitada para reproducción.
    return any(activas.values())


# Carga y reproduce una pista; si falla, la deshabilita en la lista.
def reproducir(indice):
    """Reproduce la cancion 'indice' una sola vez. Devuelve False si falla."""
    global actual
    try:
        pygame.mixer.music.load(canciones[indice])
        pygame.mixer.music.play(0)    # 0 = una vez; al terminar pasamos a la siguiente
        aplicar_volumen()
        actual = indice
        return True
    except pygame.error:
        activas[canciones[indice]] = False   # archivo dañado: se desactiva
        return False


# Busca la siguiente pista habilitada, admitiendo avanzar o retroceder circularmente.
def siguiente(paso=1):
    """Salta a la siguiente (o anterior) cancion activa, dando la vuelta a la lista."""
    global actual
    if not canciones or not pygame.mixer.get_init():
        return
    n = len(canciones)
    for k in range(1, n + 1):
        idx = (actual + paso * k) % n
        if activas[canciones[idx]] and reproducir(idx):
            return
    pygame.mixer.music.stop()   # no queda ninguna activa
    actual = -1


def alternar_cancion(indice):
    # Cambia el estado de activación de una pista y gestiona la pista actual.
    activas[canciones[indice]] = not activas[canciones[indice]]
    # si se desactiva la que esta sonando, pasa a la siguiente
    if indice == actual and not activas[canciones[indice]]:
        siguiente()


# Comprueba si terminó la canción actual y continúa con otra habilitada.
def revisar_musica():
    """Se llama cada frame: cuando una cancion termina, empieza la siguiente."""
    if (canciones and pygame.mixer.get_init() and hay_activas()
            and not pygame.mixer.music.get_busy()):
        siguiente()


# cambia entre pantalla completa y ventana
# Cambia entre pantalla completa y modo ventana según la preferencia del usuario.
def aplicar_pantalla():
    global ventana
    if ajustes["pantalla_completa"]:
        ventana = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    else:
        ventana = pygame.display.set_mode((1280, 720))


# barra de volumen con perilla y porcentaje
def dibujar_slider(texto, clave):
    # Dibuja etiqueta, barra, nivel y porcentaje del ajuste indicado.
    barra = sliders[clave]
    valor = ajustes[clave]
    etiqueta = menu_font.render(texto, True, blanco)
    game_surface.blit(etiqueta, etiqueta.get_rect(midleft=(450, barra.centery)))
    pygame.draw.rect(game_surface, (80, 80, 80), barra, border_radius=6)               # barra vacía
    relleno = pygame.Rect(barra.left, barra.top, int(barra.width * valor), barra.height)
    pygame.draw.rect(game_surface, amarillo, relleno, border_radius=6)                 # parte llena
    pygame.draw.circle(game_surface, blanco, (barra.left + int(barra.width * valor), barra.centery), 14)  # perilla
    porcentaje = menu_font.render(f"{int(valor * 100)}%", True, blanco)
    game_surface.blit(porcentaje, porcentaje.get_rect(midleft=(barra.right + 40, barra.centery)))


def dibujar_interruptor(texto, clave):
    # Representa el valor booleano del ajuste con colores y texto de estado.
    caja = interruptores[clave]
    activo = ajustes[clave]
    etiqueta = menu_font.render(texto, True, blanco)
    game_surface.blit(etiqueta, etiqueta.get_rect(midleft=(450, caja.centery)))
    pygame.draw.rect(game_surface, (60, 160, 90) if activo else (160, 60, 60), caja, border_radius=10)
    estado = menu_font.render("SI" if activo else "NO", True, blanco)
    game_surface.blit(estado, estado.get_rect(center=caja.center))


def texto_ahora_suena():
    # Devuelve el rótulo de la pista actual o un mensaje de silencio.
    if 0 <= actual < len(canciones):
        return "Ahora suena: " + nombre_cancion(canciones[actual])[:50]
    return "Ahora suena: (nada)"


# la pantalla de ajustes
# Renderiza los controles de volumen, pantalla, FPS y acceso a la lista musical.
def show_ajustes():
    dibujar_fondo()
    dibujar_texto("AJUSTES", blanco, 150)
    sonando = fuente_peq.render(texto_ahora_suena(), True, amarillo)
    game_surface.blit(sonando, sonando.get_rect(center=(width // 2, 215)))
    dibujar_slider("Musica", "musica")
    dibujar_slider("Efectos", "efectos")
    dibujar_interruptor("Pantalla completa", "pantalla_completa")
    dibujar_interruptor("Mostrar FPS", "mostrar_fps")
    dibujar_boton_caja("elegir canciones", boton_canciones)
    dibujar_boton("volver", blanco, amarillo, 710)


# filas visibles de la lista de canciones: [(indice, rect), ...]
def filas_visibles():
    # Calcula índices y rectángulos de las filas dentro de la ventana de desplazamiento.
    fin = min(len(canciones), scroll + FILAS_VISIBLES)
    return [(i, pygame.Rect(350, 230 + v * 62, 850, 52)) for v, i in enumerate(range(scroll, fin))]


def rect_check(fila):
    # Rectángulo clicable para activar o desactivar una canción.
    return pygame.Rect(fila.x + 14, fila.centery - 16, 32, 32)


def rect_sonar(fila):
    # Rectángulo clicable del botón que reproduce inmediatamente una pista.
    return pygame.Rect(fila.right - 170, fila.y + 6, 160, 40)


# Muestra la lista de pistas, su activación y los controles de reproducción.
def show_musica():
    dibujar_fondo()
    dibujar_texto("CANCIONES", blanco, 130)
    sonando = fuente_peq.render(texto_ahora_suena(), True, amarillo)
    game_surface.blit(sonando, sonando.get_rect(center=(width // 2, 185)))
    mouse = pos_en_juego(pygame.mouse.get_pos())

    if not canciones:
        aviso = fuente_peq.render("No hay canciones. Pon archivos .mp3/.ogg/.wav en la carpeta 'musica'.",
                                  True, blanco)
        game_surface.blit(aviso, aviso.get_rect(center=(width // 2, 400)))

    for i, fila in filas_visibles():
        ruta = canciones[i]
        sonando_ahora = (i == actual)
        pygame.draw.rect(game_surface, (70, 60, 110) if sonando_ahora else (35, 30, 60), fila, border_radius=10)
        # casilla de "reproducir esta cancion"
        caja = rect_check(fila)
        pygame.draw.rect(game_surface, blanco, caja, width=3, border_radius=6)
        if activas[ruta]:
            pygame.draw.rect(game_surface, (60, 200, 110), caja.inflate(-12, -12), border_radius=4)
        nombre = fuente_peq.render(nombre_cancion(ruta)[:45], True, amarillo if sonando_ahora else blanco)
        game_surface.blit(nombre, nombre.get_rect(midleft=(fila.x + 70, fila.centery)))
        # boton "sonar ahora"
        zona = rect_sonar(fila)
        hover = zona.collidepoint(mouse)
        pygame.draw.rect(game_surface, (90, 80, 140) if hover else (55, 50, 90), zona, border_radius=8)
        txt = fuente_peq.render("sonar ahora", True, amarillo if hover else blanco)
        game_surface.blit(txt, txt.get_rect(center=zona.center))

    if len(canciones) > FILAS_VISIBLES:
        pista = fuente_peq.render("(rueda del raton para ver mas)", True, (200, 200, 200))
        game_surface.blit(pista, pista.get_rect(center=(width // 2, 665)))

    dibujar_boton_caja("anterior", boton_anterior)
    dibujar_boton_caja("siguiente", boton_siguiente)
    dibujar_boton_caja("volver", boton_volver_musica)


# Interpreta clics en la lista de música y actualiza reproducción/selección.
def click_musica(click):
    global MUSICA
    for i, fila in filas_visibles():
        if rect_check(fila).inflate(10, 10).collidepoint(click):
            alternar_cancion(i)
            return
        if rect_sonar(fila).collidepoint(click):
            activas[canciones[i]] = True
            reproducir(i)
            return
    if boton_anterior.collidepoint(click):
        siguiente(-1)
    elif boton_siguiente.collidepoint(click):
        siguiente(1)
    elif boton_volver_musica.collidepoint(click):
        MUSICA = False


# Delega la prueba de colisión al mapa existente.
def mapa_choca(rect):
    """True si la caja choca con algo del mapa (muros, agua, objetos)."""
    return mapa is not None and mapa.choca(rect)


# Construye el mapa a partir del plano de caracteres MAPA.
def crear_mapa():
    return Mapa(MAPA)


def camara_pos():
    """Posicion de la camara en pixeles enteros (asi el dibujo no tiembla)."""
    return (round(camara.x), round(camara.y))


def pos_raton_mundo():
    """Donde esta el raton en el mapa (no en la pantalla): para apuntar aunque la camara se mueva."""
    cx, cy = camara_pos()
    mx, my = pos_en_juego(pygame.mouse.get_pos())
    return pygame.Vector2(mx + cx, my + cy)


# Sigue al jugador y limita el desplazamiento de cámara al área del mundo.
def actualizar_camara(jugador, dt, forzar=False):
    """Centra la camara en el jugador. forzar=True la coloca de golpe (al empezar o reiniciar)."""
    objetivo = pygame.Vector2(jugador.rect.centerx - width / 2, jugador.rect.bottom - 90 - height / 2)
    if CAMARA_LIMITADA:
        for eje, mundo, pantalla in ((0, MUNDO_ANCHO, width), (1, MUNDO_ALTO, height)):
            if mundo <= pantalla:
                objetivo[eje] = (mundo - pantalla) / 2          # el mapa cabe en pantalla: centrado
            else:
                objetivo[eje] = max(0, min(objetivo[eje], mundo - pantalla))
    if forzar or CAMARA_SUAVIDAD <= 0:
        camara.update(objetivo)
    else:
        camara.update(camara + (objetivo - camara) * min(1.0, CAMARA_SUAVIDAD * dt))


def dibujar_suelo(superficie, cam):
    # Mantiene una interfaz simple para dibujar el terreno del mapa actual.
    mapa.dibujar_suelo(superficie, cam)


def dibujar_mira(superficie):
    # Dibuja una mira alternativa cuando el cursor del sistema está oculto.
    """Mira pequena en la posicion del raton (se usa con el cursor oculto)."""
    x, y = (int(v) for v in pos_en_juego(pygame.mouse.get_pos()))
    for color, grosor in (((0, 0, 0), 4), ((255, 255, 255), 2)):
        pygame.draw.line(superficie, color, (x - 13, y), (x - 5, y), grosor)
        pygame.draw.line(superficie, color, (x + 5, y), (x + 13, y), grosor)
        pygame.draw.line(superficie, color, (x, y - 13), (x, y - 5), grosor)
        pygame.draw.line(superficie, color, (x, y + 5), (x, y + 13), grosor)
    pygame.draw.circle(superficie, (255, 255, 255), (x, y), 2)


# Devuelve una copia con el canal alfa multiplicado, sin alterar el sprite original.
def con_transparencia(imagen, alpha):
    """Copia de la imagen con transparencia 'alpha' (0 = invisible, 255 = normal), aplicada pixel a pixel.
    No usar set_alpha en sprites con transparencia: en algunas versiones de pygame dibuja un rectangulo
    alrededor del personaje."""
    copia = imagen.copy()
    copia.fill((255, 255, 255, max(0, min(255, int(alpha)))), special_flags=pygame.BLEND_RGBA_MULT)
    return copia


def escalar_imagen(imagen, escala):
    """Cambia el tamano de una imagen. Para tus enemigos y objetos con sprite:
    escalar_imagen(pygame.image.load("caja.png").convert_alpha(), escala_objetos)"""
    if escala == 1:
        return imagen
    tam = (max(1, round(imagen.get_width() * escala)), max(1, round(imagen.get_height() * escala)))
    return pygame.transform.scale(imagen, tam)   # scale (sin suavizar) mantiene el pixel art nitido


SPRITES_ENEMIGOS = {}


# Carga y cachea el sprite del enemigo, recortando sus márgenes transparentes.
def cargar_sprite_enemigo(nombre):
    """Carga enemigos/<nombre>.png recortado a su dibujo (sin el margen transparente). Se lee una sola vez."""
    if nombre not in SPRITES_ENEMIGOS:
        for base in (os.getcwd(), os.path.dirname(os.path.abspath(__file__))):
            ruta = os.path.join(base, "enemigos", nombre + ".png")
            if os.path.exists(ruta):
                break
        else:
            print(f"No encuentro enemigos/{nombre}.png junto a este archivo (descomprime enemigos.zip).")
            pygame.quit()
            sys.exit()
        img = pygame.image.load(ruta).convert_alpha()
        SPRITES_ENEMIGOS[nombre] = img.subsurface(img.get_bounding_rect()).copy()
    return SPRITES_ENEMIGOS[nombre]


# Instancia un enemigo en cada punto de aparición marcado en el mapa.
def crear_enemigos():
    """Un goblin por cada 'g' o 'G' del plano del mapa."""
    return [Enemigo(x, y) for x, y in mapa.goblins]


def colision_enemigos(jugador, enemigos):
    """Los enemigos son solidos: los pies del jugador no los atraviesan (salvo que este en el aire).
    Si DANO_POR_CONTACTO esta activado, tocarlos tambien hace dano."""
    if jugador.muerto:
        return
    cuerpo = jugador.cuerpo()
    for e in enemigos:
        if not e.vivo():
            continue
        if DANO_POR_CONTACTO and cuerpo.colliderect(e.cuerpo()):
            jugador.recibir_dano(e.dano, e.rect.center)
        if jugador.z < 50 and jugador.rect.colliderect(e.rect):
            # sacar al jugador del enemigo por el lado por el que menos se solapan
            salidas = [
                (e.rect.right - jugador.rect.left, (1, 0)),
                (jugador.rect.right - e.rect.left, (-1, 0)),
                (e.rect.bottom - jugador.rect.top, (0, 1)),
                (jugador.rect.bottom - e.rect.top, (0, -1)),
            ]
            distancia, (sx, sy) = min(salidas)
            jugador.rect.move_ip(sx * distancia, sy * distancia)
            jugador.pos.update(jugador.rect.center)


# Aplica el daño de la hitbox de ataque, evitando golpear dos veces al mismo enemigo.
def golpes_del_jugador(jugador, enemigos):
    """Si el ataque del jugador toca el cuerpo de un enemigo, le hace dano (una vez por ataque)."""
    zona = jugador.hitbox()
    if zona is None:
        return
    dano = DANO_ATAQUE[jugador.accion]
    for e in enemigos:
        if e.vivo() and e not in jugador.golpeados and zona.colliderect(e.cuerpo()):
            if e.recibir_dano(dano, jugador.rect.center):
                jugador.golpeados.add(e)


def dibujar_hitboxes(superficie, jugador, enemigos, cam=(0, 0)):
    """Depuracion (F3): azul = pies, verde = cuerpo del jugador, amarillo = su golpe,
    rojo = cuerpo del enemigo, naranja = pies del enemigo, magenta = zona de ataque del enemigo."""
    if mapa is not None:
        mapa.dibujar_colisiones(superficie, cam)
    pygame.draw.rect(superficie, (0, 200, 255), jugador.rect.move(-cam[0], -cam[1]), 2)
    pygame.draw.rect(superficie, (80, 255, 80), jugador.cuerpo().move(-cam[0], -cam[1]), 2)
    golpe = jugador.hitbox()
    if golpe is not None:
        pygame.draw.rect(superficie, (255, 255, 0), golpe.move(-cam[0], -cam[1]), 3)
    for e in enemigos:
        pygame.draw.rect(superficie, (255, 150, 0), e.rect.move(-cam[0], -cam[1]), 2)
        pygame.draw.rect(superficie, (255, 60, 60), e.cuerpo().move(-cam[0], -cam[1]), 2)
        if e.vivo():
            lado = e.ataque["lado"] if e.ataque else e.mirando
            grosor = 4 if e.ataque and e.ataque["fase"] == "golpe" else 1
            pygame.draw.rect(superficie, (255, 60, 255), e.zona_ataque(lado).move(-cam[0], -cam[1]), grosor)


def dibujar_barra_vida(superficie, jugador):
    # Presenta la vida del jugador y la animación de pérdida reciente.
    x, y, ancho, alto = 20, 70, 320, 26
    frac = jugador.vida / jugador.vida_max
    visible = jugador.vida_visible / jugador.vida_max
    pygame.draw.rect(superficie, (35, 10, 14), (x, y, ancho, alto), border_radius=8)
    if visible > frac:   # lo que se acaba de perder, en claro
        pygame.draw.rect(superficie, (240, 215, 215), (x, y, int(ancho * visible), alto), border_radius=8)
    if frac > 0:
        pygame.draw.rect(superficie, (210, 40, 55), (x, y, int(ancho * frac), alto), border_radius=8)
    pygame.draw.rect(superficie, blanco, (x, y, ancho, alto), width=3, border_radius=8)
    texto = fuente_peq.render(f"VIDA {jugador.vida}/{jugador.vida_max}", True, blanco)
    superficie.blit(texto, texto.get_rect(midleft=(x + ancho + 14, y + alto // 2)))


# Carga frames de cada animación y crea versiones orientadas a izquierda y derecha.
def cargar_animaciones():
    """Carga los frames de la carpeta 'jugador' (nombre_1.png, nombre_2.png, ...).
    Para cada animacion guarda la version mirando a la derecha y a la izquierda."""
    carpeta = None
    for base in (os.getcwd(), os.path.dirname(os.path.abspath(__file__))):
        if os.path.isdir(os.path.join(base, "jugador")):
            carpeta = os.path.join(base, "jugador")
            break
    if carpeta is None:
        print("No encuentro la carpeta 'jugador' junto a este archivo (descomprime jugador_frames.zip).")
        pygame.quit()
        sys.exit()
    animaciones = {}
    for nombre in CONFIG_ANIM:
        frames = []
        n = 1
        while os.path.exists(os.path.join(carpeta, f"{nombre}_{n}.png")):
            img = pygame.image.load(os.path.join(carpeta, f"{nombre}_{n}.png")).convert_alpha()
            frames.append(escalar_imagen(img, escala_jugador))
            n += 1
        if not frames:
            print(f"Faltan los frames de '{nombre}' en {carpeta}")
            pygame.quit()
            sys.exit()
        animaciones[nombre] = {"der": frames, "izq": [pygame.transform.flip(f, True, False) for f in frames]}
    return animaciones


def cargar_spritesheet(ruta, ancho, alto, cantidad):
    # Divide una hoja horizontal en la cantidad indicada de imágenes de tamaño fijo.
    hoja = pygame.image.load(ruta).convert_alpha()
    return [hoja.subsurface((i * ancho, 0, ancho, alto)) for i in range(cantidad)]


# Dibuja el título, fondo y opciones de navegación del menú principal.
def show_menu():
    dibujar_fondo()
    # panel semitransparente detrás de los botones
    panel = pygame.Surface((520, 460), pygame.SRCALPHA)
    pygame.draw.rect(panel, (10, 10, 30, 150), panel.get_rect(), border_radius=24)
    game_surface.blit(panel, panel.get_rect(center=(width // 2, 440)))
    # título con sombra y un pequeño vaivén
    y_titulo = 215 + math.sin(pygame.time.get_ticks() / 600) * 6
    sombra = titulo_font.render("PRISION FANTASY", True, negro)
    titulo = titulo_font.render("PRISION FANTASY", True, amarillo)
    game_surface.blit(sombra, sombra.get_rect(center=(width // 2 + 4, y_titulo + 4)))
    game_surface.blit(titulo, titulo.get_rect(center=(width // 2, y_titulo)))
    for op in opciones:
        dibujar_boton_caja(op["texto"], op["rect"])
    ayuda = fuente_peq.render("1 = jugar    2 = ajustes    3 = controles", True, (200, 200, 200))
    game_surface.blit(ayuda, ayuda.get_rect(center=(width // 2, height - 40)))


# lista de controles que muestra la pantalla "controles": (accion, tecla)
LISTA_CONTROLES = [
    ("Mover", "W A S D  /  flechas"),
    ("Correr", "Shift (mientras te mueves)"),
    ("Saltar", "Espacio"),
    ("Rodar", "R"),
    ("Agacharse", "C  /  Ctrl (mantener)"),
    ("Atacar (combo)", "clic izquierdo"),
    ("Embestida", "clic izquierdo corriendo"),
    ("Golpe hacia abajo", "clic izquierdo en el aire"),
    ("Giro", "clic derecho  /  E"),
    ("Beber", "Q"),
    ("Pausa", "Esc"),
    ("Ver hitboxes", "F3"),
    ("Bloquear / ocultar cursor", "Tab"),
    ("Reiniciar", "Enter (al morir o ganar)"),
]


# Presenta los controles y conserva el fondo de pausa cuando se abre desde el juego.
def show_controles():
    if PAUSA and captura is not None:
        game_surface.blit(captura, (0, 0))
        game_surface.blit(velo, (0, 0))
    else:
        dibujar_fondo()
    panel = pygame.Surface((960, 670), pygame.SRCALPHA)
    pygame.draw.rect(panel, (10, 10, 30, 170), panel.get_rect(), border_radius=24)
    game_surface.blit(panel, panel.get_rect(center=(width // 2, 440)))
    dibujar_texto("CONTROLES", blanco, 110)
    for i, (accion, tecla) in enumerate(LISTA_CONTROLES):
        y = 190 + i * 42
        a = fuente_peq.render(accion, True, amarillo)
        t = fuente_peq.render(tecla, True, blanco)
        game_surface.blit(a, a.get_rect(midright=(width // 2 - 20, y)))
        game_surface.blit(t, t.get_rect(midleft=(width // 2 + 20, y)))
    dibujar_boton_caja("volver", boton_volver_controles)


# Renderiza la captura congelada del juego y las acciones disponibles durante la pausa.
def show_pausa():
    # el juego congelado de fondo, oscurecido
    if captura is not None:
        game_surface.blit(captura, (0, 0))
    game_surface.blit(velo, (0, 0))
    panel = pygame.Surface((560, 420), pygame.SRCALPHA)
    pygame.draw.rect(panel, (10, 10, 30, 180), panel.get_rect(), border_radius=24)
    game_surface.blit(panel, panel.get_rect(center=(width // 2, 480)))
    titulo = titulo_font.render("PAUSA", True, amarillo)
    game_surface.blit(titulo, titulo.get_rect(center=(width // 2, 300)))
    for op in opciones_pausa:
        dibujar_boton_caja(op["texto"], op["rect"])


# Inicializa los recursos y entidades antes del bucle interactivo de Pygame.
print("---------- BUCLE PRINCIPAL ----------")
dt = 0
ANIMACIONES = cargar_animaciones()
mapa = crear_mapa()
jugador = Jugador(*mapa.inicio)
enemigos = crear_enemigos()
actualizar_camara(jugador, 0, True)
fuente_ayuda = pygame.font.Font(None, 26)
ayuda_juego = [fuente_ayuda.render(t, True, blanco) for t in (
    "WASD mover   Shift correr   Espacio saltar   R rodar   C agacharse   Q beber",
    "Clic izq atacar (combo)   Clic der / E giro   en el aire: atacar = golpe hacia abajo   F3 ver hitboxes",
)]
aplicar_volumen()
siguiente()   # arranca la lista de reproducción
# Bucle de eventos, actualización de estados y renderizado; termina al elegir salir.
while RUN:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUN = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F3:
                MOSTRAR_HITBOX = not MOSTRAR_HITBOX
            if event.key == pygame.K_TAB:
                CURSOR_BLOQUEADO = not CURSOR_BLOQUEADO
            if event.key == pygame.K_RETURN and JUGAR and not PAUSA and (jugador.muerto or not enemigos):
                jugador = Jugador(*mapa.inicio)    # reiniciar la partida
                enemigos = crear_enemigos()
                actualizar_camara(jugador, 0, True)
            if event.key == pygame.K_ESCAPE:
                if CONTROLES:
                    CONTROLES = False
                elif MUSICA:
                    MUSICA = False
                elif AJUSTES:
                    AJUSTES = False
                elif JUGAR and PAUSA:
                    PAUSA = False                     # Esc en pausa = reanudar
                    jugador.enfriamiento = 0.3
                elif JUGAR:
                    captura = game_surface.copy()     # foto del juego para el fondo
                    PAUSA = True
                else:
                    RUN = False
            if not JUGAR and not AJUSTES and not CONTROLES:
                if event.key == pygame.K_1:
                    modo = "jugar"
                    JUGAR = True
                elif event.key == pygame.K_2:
                    modo = "ajustes"
                    AJUSTES = True
                elif event.key == pygame.K_3:
                    CONTROLES = True
        if event.type == pygame.MOUSEWHEEL and AJUSTES and MUSICA:
            maximo = max(0, len(canciones) - FILAS_VISIBLES)
            scroll = max(0, min(maximo, scroll - event.y))
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and (not JUGAR or PAUSA):
            click = pos_en_juego(event.pos)
            if CONTROLES:
                if boton_volver_controles.collidepoint(click):
                    CONTROLES = False
            elif not AJUSTES and JUGAR:
                # menú de pausa
                for op in opciones_pausa:
                    if op["rect"].collidepoint(click):
                        if op["modo"] == "reanudar":
                            PAUSA = False
                            jugador.enfriamiento = 0.3
                        elif op["modo"] == "controles":
                            CONTROLES = True
                        elif op["modo"] == "ajustes":
                            AJUSTES = True
                        else:   # volver al menú principal
                            JUGAR = False
                            PAUSA = False
                            jugador = Jugador(*mapa.inicio)
                            enemigos = crear_enemigos()
                            actualizar_camara(jugador, 0, True)
            elif not AJUSTES:
                for op in opciones:
                    if op["rect"].collidepoint(click):
                        if op["modo"] == "ajustes":
                            modo, AJUSTES = op["modo"], True
                        elif op["modo"] == "controles":
                            CONTROLES = True
                        elif op["modo"] == "salir":
                            RUN = False
                        else:
                            modo, JUGAR = op["modo"], True
            elif MUSICA:
                click_musica(click)
            else:
                for clave, barra in sliders.items():
                    if barra.inflate(40, 40).collidepoint(click):
                        arrastrando = clave
                for clave, caja in interruptores.items():
                    if caja.collidepoint(click):
                        ajustes[clave] = not ajustes[clave]
                        if clave == "pantalla_completa":
                            aplicar_pantalla()
                if boton_canciones.collidepoint(click):
                    MUSICA = True
                if zona_boton("volver", 710).collidepoint(click):
                    AJUSTES = False
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            arrastrando = None
    if AJUSTES and not MUSICA and arrastrando:
        barra = sliders[arrastrando]
        mx = pos_en_juego(pygame.mouse.get_pos())[0]
        ajustes[arrastrando] = max(0, min(1, (mx - barra.left) / barra.width))
        aplicar_volumen()

    # la música sigue sola con la siguiente canción, también durante el juego
    revisar_musica()

    # cursor: con Tab se oculta y se encierra en la ventana, solo mientras se juega (en los menus siempre se ve)
    cursor_oculto = CURSOR_BLOQUEADO and JUGAR and not PAUSA and not AJUSTES and not CONTROLES
    pygame.mouse.set_visible(not cursor_oculto)
    pygame.event.set_grab(cursor_oculto)

    if CONTROLES:
        show_controles()
    elif AJUSTES and MUSICA:
        show_musica()
    elif AJUSTES:
        show_ajustes()
    elif JUGAR and PAUSA:
        show_pausa()
    elif not JUGAR:
        show_menu()
    else:
        jugador.actualizar(pygame.key.get_pressed(), dt)
        for e in enemigos:
            e.actualizar(dt, jugador, enemigos)
        golpes_del_jugador(jugador, enemigos)
        colision_enemigos(jugador, enemigos)
        enemigos = [e for e in enemigos if not e.eliminado]    # los muertos ya desvanecidos se quitan
        if not enemigos:
            jugador.celebrar()                                 # todos derrotados: pose de victoria
        actualizar_camara(jugador, dt)
        cam = camara_pos()
        dibujar_suelo(game_surface, cam)
        # el que tiene los pies mas abajo se dibuja delante
        for ent in sorted(mapa.props_visibles(cam) + enemigos + [jugador], key=lambda o: o.rect.bottom):
            ent.dibujar(game_surface, cam)
        if MOSTRAR_HITBOX:
            dibujar_hitboxes(game_surface, jugador, enemigos, cam)
        dibujar_barra_vida(game_surface, jugador)
        restantes = fuente_peq.render(f"Enemigos: {sum(e.vivo() for e in enemigos)}", True, blanco)
        game_surface.blit(restantes, (20, 108))
        if jugador.muerto or not enemigos:
            texto = "Has muerto - pulsa Enter para reiniciar" if jugador.muerto else "Victoria! - pulsa Enter para jugar otra vez"
            aviso = menu_font.render(texto, True, amarillo)
            game_surface.blit(aviso, aviso.get_rect(center=(width // 2, 130)))
        for i, linea in enumerate(ayuda_juego):
            game_surface.blit(linea, (20, height - 54 + i * 24))
        if cursor_oculto and MOSTRAR_MIRA:
            dibujar_mira(game_surface)
        if ajustes["mostrar_fps"]:
            fps = menu_font.render(f"FPS: {int(reloj.get_fps())}", True, blanco)
            game_surface.blit(fps, (20, 20))
    blit_scaled()
    pygame.display.flip()
    dt = reloj.tick(60) / 1000


pygame.quit()
sys.exit()
