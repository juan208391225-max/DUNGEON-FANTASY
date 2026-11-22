import math
import os
import random
import sys
import pygame
from guardado_mysql import MySQLSaveSlots
from sonidos_acciones import AudioAcciones


# Inicializa Pygame antes de cargar cualquier recurso.
print("---------- INICIO DE PYGAME ----------")
pygame.init()



print("---------- 1. OLEADAS: CUANTOS ENEMIGOS SALEN, CUANTOS A LA VEZ Y QUE TAN RAPIDO ----------")

# Cada zona define el área, destino, límites de enemigos y tipos de encuentro.

ZONAS = [
    {
        "nombre": "Bosque Susurrante", "casillas": (1, 1, 14, 15), "color": (255, 170, 60),
        "cerrada": False, "destino": (7, 8), "distancia_aparicion": 300,
        "enemigos_derrotar": 10, "max_vivos": 3, "intervalo_aparicion": 1.0,
        "tipos_enemigos": ("goblin", "mago"),
        "puertas": ((17, 7), (17, 8), (17, 9), (17, 10)),
    },
    {
        "nombre": "Ruinas del Templo", "casillas": (19, 1, 31, 15), "color": (235, 70, 110),
        "cerrada": False, "destino": (25, 8), "distancia_aparicion": 300,
        "enemigos_derrotar": 12, "max_vivos": 3, "intervalo_aparicion": 0.8,
        "tipos_enemigos": ("goblin", "mago"),
        "puertas": ((34, 8),),
    },
    {
        "nombre": "Pantano Venenoso", "casillas": (36, 1, 54, 15), "color": (70, 190, 150),
        "cerrada": False, "destino": (45, 8), "distancia_aparicion": 300,
        "enemigos_derrotar": 15, "max_vivos": 3, "intervalo_aparicion": 0.6,
        "tipos_enemigos": ("bruja", "trol"),
        "puertas": ((27, 18), (23, 21), (23, 24), (23, 27)),
    },
    {
        "nombre": "Prision", "casillas": (19, 19, 33, 29), "color": (150, 130, 235),
        "cerrada": False, "destino": (26, 24), "distancia_aparicion": 300,
        "enemigos_derrotar": 15, "max_vivos": 4, "intervalo_aparicion": 0.5,
        "tipos_enemigos": ("bruja", "trol"),
        "reja_temporal": (24, 19, 4),
        "puertas": ((36, 24), (42, 18), (46, 18), (50, 18), (41, 29), (44, 29)),
    },
    {
        "nombre": "Arena del Carcelero", "casillas": (38, 18, 54, 29), "color": (245, 75, 45),
        "cerrada": False, "destino": (46, 24), "distancia_aparicion": 350,
        "enemigos_derrotar": 1, "max_vivos": 1, "intervalo_aparicion": 0.4,
        "tipos_enemigos": (), "jefe": True, "sprite_jefe": "orco_jefe_de_guerra", "tipo_jefe": "orco",
        "tipos_apoyo": ("lich", "espectro"), "max_apoyos": 3,
        "puertas": ((56, 9),),
    },
    {
        "nombre": "Aldea Abandonada", "casillas": (58, 2, 75, 16), "color": (150, 210, 95),
        "cerrada": False, "destino": (66, 9), "distancia_aparicion": 350,
        "enemigos_derrotar": 20, "max_vivos": 4, "intervalo_aparicion": 0.35,
        "tipos_enemigos": ("lich", "espectro"),
        "puertas": ((66, 20),),
    },
    {
        "nombre": "Selva Antigua", "casillas": (39, 33, 57, 46), "color": (65, 185, 100),
        "cerrada": False, "destino": (48, 39), "distancia_aparicion": 350,
        "enemigos_derrotar": 25, "max_vivos": 5, "intervalo_aparicion": 0.25,
        "tipos_enemigos": ("lich", "espectro"),
        "puertas": ((58, 39),),
    },
    {
        "nombre": "Desfiladero de la Mina", "casillas": (59, 19, 77, 32), "color": (215, 145, 80),
        "cerrada": False, "destino": (68, 25), "distancia_aparicion": 300,
        "enemigos_derrotar": 30, "max_vivos": 5, "intervalo_aparicion": 0.15,
        "tipos_enemigos": ("lich", "espectro"),
        "puertas": ((68, 33),),
    },
    {
        "nombre": "Cumbre del Dragon", "casillas": (60, 35, 78, 46), "color": (225, 70, 65),
        "cerrada": False, "destino": (69, 40), "distancia_aparicion": 450,
        "enemigos_derrotar": 1, "max_vivos": 1, "intervalo_aparicion": 0.10,
        "tipos_enemigos": (), "jefe": True, "sprite_jefe": "dragon", "tipo_jefe": "dragon",
    },
]
# Mantiene una vista por numero de zona para consultas externas y compatibilidad.
PUERTAS_POR_OLEADA = {
    indice: zona.get("puertas", ())
    for indice, zona in enumerate(ZONAS, 1)
    if zona.get("puertas")
}
OLEADA_ENEMIGOS_BASE = 8
OLEADA_ENEMIGOS_MAS = 6
OLEADA_MAX_VIVOS_BASE = 3
OLEADA_MAX_VIVOS_MAS = 2
OLEADA_INTERVALO_BASE = 3.0
OLEADA_INTERVALO_MENOS = 0.6
OLEADA_INTERVALO_MIN = 0.8
OLEADA_ESPERA = 3.0
ENEMIGOS_OLEADA_AGRESIVOS = True
ENEMIGO_TIEMPO_APARICION = 0.6
OLEADA_MARGEN_ENTRADA = 40
PUNTUACION_TIEMPO_MAX_REDUCCION = 300.0
MEJORAS_MAXIMAS_POR_PODER = 3
RETARDO_ELECCION_BONIFICACION = 1.0
BONIFICACIONES = (
    ("viento", "Tajo de viento", "Cada pocos golpes conectados lanza un proyectil de largo alcance."),
    ("dano", "Filo mejorado", "Aumenta el dano de todos tus ataques."),
    ("berserker", "Modo berserker", "Pulsa V para ganar dano y velocidad, y recibir menos dano."),
)

# Parámetros base compartidos por la IA, sus ventanas de ataque y los jefes.
print("---------- 2. ENEMIGOS: COMPORTAMIENTO COMPARTIDO ----------")
RETROCESO_ENEMIGO = 35
TIEMPO_RETROCESO = 0.35

VEL_ENEMIGO_VAGAR = 60
RADIO_DETECCION = 380
RADIO_PERDER = 650
RADIO_VAGAR = 260
ENEMIGO_PREPARAR = 0.40
ENEMIGO_GOLPE = 0.15
ENEMIGO_RECUPERAR = 0.35
ENEMIGO_UMBRAL_GIRO = 14
ENEMIGO_MIRA_A_LA_DERECHA = False
DANO_POR_CONTACTO = False
JEFE_ORCO_INTERVALO_ATAQUE = 3.0
JEFE_ORCO_APOYOS_POR_ATAQUE = 3
JEFE_ORCO_MULTIPLICADOR_VIDA = 20
JEFE_DRAGON_MULTIPLICADOR_VIDA = 80
JEFE_DRAGON_TIEMPO_INICIAL = 0.5
JEFE_DRAGON_RECUPERACION_ATAQUE = 0.4
JEFE_DRAGON_INTERVALO_ATAQUE = 0.25

# Valores de movimiento y daño consultados durante la simulación de cada fotograma.
print("---------- 3. JUGADOR: VIDA, VELOCIDAD, SALTO Y ATAQUES ----------")
VIDA_JUGADOR = 100
VEL_JUGADOR_CAMINAR = 300
VEL_JUGADOR_CORRER = 520
VEL_JUGADOR_AGACHADO = 130
VEL_JUGADOR_RODAR = 620
FUERZA_SALTO = 820
GRAVEDAD = 2400
GRAVEDAD_GOLPE_ABAJO = 3800
INVULNERABLE_TRAS_GOLPE = 1.2
ENFRIAMIENTO_ATAQUE = 0.1
TIEMPO_COMBO = 0.5
ENFRIAMIENTO_GIRO = 5.0
TIEMPO_ESPADA_EN_MANO = 3.0
DANO_ATAQUE = {
    "atacar": 20,
    "atacar2": 20,
    "atacar_dash": 25,
    "agachado_atacar": 12,
    "atacar_abajo": 30,
    "atacar_giro": 40,
}

# Las escalas convierten dimensiones de sprites y las hitboxes expresan colisiones lógicas.
print("---------- 4. TAMANOS: ESCALAS Y HITBOXES ----------")
ESCALA_GLOBAL = 1
ESCALA_JUGADOR = 2
ESCALA_ENEMIGOS = 5
escala_jugador = ESCALA_JUGADOR * ESCALA_GLOBAL
escala_enemigos = ESCALA_ENEMIGOS * ESCALA_GLOBAL


# Cajas de colision de jugador, enemigos y ataques, en pixeles antes de aplicar la escala.
print("---------- HITBOXES ----------")
HITBOX_JUGADOR_PIES = (20, 10)
HITBOX_JUGADOR_CUERPO = (28, 62)
HITBOX_JUGADOR_CUERPO_AGACHADO = (28, 32)
HITBOX_ENEMIGO_PIES = (9, 5)
HITBOX_ENEMIGO_CUERPO = (11, 14)
HITBOX_ENEMIGO_ATAQUE = (9, 6)
HITBOX_ENEMIGO_ATAQUE_POS = (5, 10)
HITBOX_ATAQUES = {
    "atacar": (80, 60),
    "atacar2": (80, 60),
    "atacar_dash": (75, 45),
    "agachado_atacar": (55, 30),
    "atacar_abajo": (65, 55),
    "atacar_giro": (130, 75),
}
HITBOX_ATAQUE_POS = {
    "atacar": (5, 55),
    "atacar2": (5, 60),
    "atacar_dash": (5, 30),
    "agachado_atacar": (5, 30),
    "atacar_abajo": (5, 30),
    "atacar_giro": (5, 30),
}


# Opciones de seguimiento del jugador y límites de la cámara.
print("---------- 5. CAMARA Y MIRA ----------")
CAMARA_SUAVIDAD = 0
CAMARA_LIMITADA = True


# La generación del mapa utiliza estas medidas para convertir casillas en píxeles.
print("---------- 6. MAPA ----------")
ESCALA_TILES = 4
TAM_TILE = 32 * ESCALA_TILES
JEFE_ALTURA_SPRITE = TAM_TILE * 2.5


# Genera de forma determinista el plano del mundo, sus zonas y su decoración.
def _crear_mapa():
    ancho, alto = 80, 48
    celdas = [["."] * ancho for _ in range(alto)]
    reservado = [[False] * ancho for _ in range(alto)]
    rng = random.Random(19)
    Z = [z["casillas"] for z in ZONAS]
    VERDES = (".", ";", ",")
    lattice = {}

    # Produce valores pseudoaleatorios estables para cada punto de la cuadrícula de ruido.
    def valor(ix, iy, semilla):
        clave = (ix, iy, semilla)
        if clave not in lattice:
            lattice[clave] = random.Random(ix * 73856093 ^ iy * 19349663 ^ semilla * 83492791).random()
        return lattice[clave]

    # Interpola el ruido entre puntos para formar variaciones suaves del terreno.
    def ruido(x, y, escala, semilla):
        fx, fy = x / escala, y / escala
        ix, iy = math.floor(fx), math.floor(fy)
        tx, ty = fx - ix, fy - iy
        tx, ty = tx * tx * (3 - 2 * tx), ty * ty * (3 - 2 * ty)
        a, b = valor(ix, iy, semilla), valor(ix + 1, iy, semilla)
        c, d = valor(ix, iy + 1, semilla), valor(ix + 1, iy + 1, semilla)
        return (a * (1 - tx) + b * tx) * (1 - ty) + (c * (1 - tx) + d * tx) * ty

    # Comprueba si una coordenada cae dentro de los limites del mapa.
    def dentro(x, y):
        return 0 <= x < ancho and 0 <= y < alto

    # Escribe un símbolo dentro del mapa y opcionalmente protege esa casilla de decorado posterior.
    def poner(x, y, ch, reservar_celda=True):
        if dentro(x, y):
            celdas[y][x] = ch
            if reservar_celda:
                reservado[y][x] = True

    # Rellena un rectángulo de casillas con el símbolo indicado.
    def pintar(limites, ch, reservar_celdas=False):
        x0, y0, x1, y1 = limites
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                poner(x, y, ch, reservar_celdas)

    # Evita que la generación aleatoria altere una estructura y su margen circundante.
    def reservar(limites, margen=0):
        x0, y0, x1, y1 = limites
        for y in range(y0 - margen, y1 + margen + 1):
            for x in range(x0 - margen, x1 + margen + 1):
                if dentro(x, y):
                    reservado[y][x] = True

    # Reserva un área circular para mantener despejados destinos y puntos de interés.
    def reservar_circulo(cx, cy, radio):
        for y in range(int(cy - radio) - 1, int(cy + radio) + 2):
            for x in range(int(cx - radio) - 1, int(cx + radio) + 2):
                if dentro(x, y) and math.hypot(x - cx, y - cy) <= radio:
                    reservado[y][x] = True

    # Dibuja una mancha ovalada con borde irregular controlado por ruido.
    def mancha(cx, cy, rx, ry, ch, semilla=0):
        for y in range(int(cy - ry) - 2, int(cy + ry) + 3):
            for x in range(int(cx - rx) - 2, int(cx + rx) + 3):
                if dentro(x, y):
                    d = math.hypot((x - cx) / rx, (y - cy) / ry)
                    if d <= 1.0 + 0.4 * (ruido(x, y, 2.5, 40 + semilla) - 0.5):
                        poner(x, y, ch)

    # Construye el contorno de un muro, respetando puertas, huecos y partes derruidas.
    def muro(limites, ch, huecos=(), ruina=0.0):
        x0, y0, x1, y1 = limites
        huecos = set(huecos)
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                if x not in (x0, x1) and y not in (y0, y1):
                    continue
                if (x, y) in huecos:
                    reservado[y][x] = True
                    continue
                esquina = x in (x0, x1) and y in (y0, y1)
                if ruina and not esquina and rng.random() < ruina:
                    reservado[y][x] = True
                    continue
                poner(x, y, ch)

    # Combina suelo interior, perímetro, puerta y zona protegida para crear un edificio.
    def edificio(limites, ch, suelo, puerta, puerta_ch="D"):
        x0, y0, x1, y1 = limites
        pintar((x0 + 1, y0 + 1, x1 - 1, y1 - 1), suelo, True)
        muro(limites, ch)
        poner(puerta[0], puerta[1], puerta_ch)
        reservar(limites, 1)

    # Distribuye coordenadas alrededor de una elipse para colocar objetos en círculo.
    def puntos_circulo(cx, cy, radio, cantidad, fase=0.0):
        return [(round(cx + radio * math.cos(fase + 2 * math.pi * i / cantidad)),
                 round(cy + radio * math.sin(fase + 2 * math.pi * i / cantidad) * 0.8)) for i in range(cantidad)]

    # Coloca el mismo elemento en una colección de coordenadas.
    def colocar(ch, puntos):
        for x, y in puntos:
            poner(x, y, ch)

    # Devuelve el índice de la zona que contiene la casilla o None si está fuera de ellas.
    def zona_en(x, y):
        for i, (x0, y0, x1, y1) in enumerate(Z):
            if x0 <= x <= x1 and y0 <= y <= y1:
                return i
        return None

    pintar(Z[1], "_")
    pintar(Z[2], ",")
    pintar(Z[3], "_")
    pintar(Z[4], "r")
    pintar(Z[5], ";")
    pintar(Z[7], ":")
    pintar(Z[8], "r")
    for y in range(alto):
        for x in range(ancho):
            if celdas[y][x] == "." and zona_en(x, y) is None and ruido(x, y, 7.0, 3) > 0.62:
                celdas[y][x] = ";"

    for z in ZONAS:
        reservar_circulo(z["destino"][0], z["destino"][1], 3.6)

    for y in range(0, 32):
        cx = 55 + (1 if math.sin(y / 3.2) > 0.2 else 0)
        for x in (cx, cx + 1):
            poner(x, y, "~")
    mancha(56.5, 30.5, 3.0, 2.2, "~", 1)
    mancha(7, 23, 5.2, 3.2, "~", 2)
    mancha(11.5, 13, 2.2, 1.3, "~", 3)
    mancha(73.5, 8.5, 1.8, 1.0, "~", 4)
    mancha(54.5, 43.5, 2.3, 1.7, "~", 5)
    mancha(39, 4, 3.2, 2.2, "v", 6)
    mancha(51.5, 12.5, 3.0, 2.0, "v", 7)
    mancha(45.5, 13.5, 2.5, 1.4, "v", 8)
    mancha(53, 4, 1.3, 2.0, "v", 9)

    CAMINOS = ((13, 7, 65, 10), (24, 9, 27, 39), (24, 21, 70, 25),
               (48, 24, 51, 40), (65, 8, 68, 41), (50, 37, 70, 40))
    for camino in CAMINOS:
        pintar(camino, ":", True)
    for y0, y1 in ((7, 10), (21, 25)):
        pintar((55, y0, 58, y1), "_", True)

    for limites in ((8, 30, 23, 31), (8, 32, 9, 32), (16, 26, 17, 29), (28, 38, 31, 39), (32, 41, 33, 42)):
        pintar(limites, ":", True)

    c0, f0, c1, f1 = Z[0]
    edificio((2, 2, 6, 5), "d", ":", (4, 5))
    colocar("C", [(5, 3)])
    colocar("B", [(3, 3)])
    colocar("O", [(10, 9)])
    colocar("L", [(10, 7), (12, 10), (11, 9)])
    colocar("B", [(9, 10)])
    colocar("M", [(3, 12), (5, 13), (2, 14), (6, 11), (4, 10)])
    for x, y in puntos_circulo(10, 4, 2.3, 7):
        poner(x, y, "R")
    poner(10, 4, "p")
    reservar_circulo(10, 4, 3.5)
    reservar_circulo(7, 12, 2.5)
    reservar_circulo(11.5, 13, 3.2)

    muro((20, 2, 28, 6), "#", huecos=[(23, 6), (24, 6), (25, 6)], ruina=0.18)
    pintar((21, 3, 27, 5), "_", True)
    colocar("S", [(24, 3)])
    colocar("F", [(21, 3), (27, 3)])
    colocar("K", [(22, 5), (26, 5)])
    poner(24, 4, "p")
    muro((29, 2, 31, 5), "k", huecos=[(30, 5)], ruina=0.3)
    colocar("R", [(30, 3), (29, 6)])
    reservar((20, 2, 31, 6), 1)
    for y in (11, 13, 15):
        colocar("#", [(23, y), (28, y)])
    for puntos in (((20, 11), (21, 11), (22, 11), (20, 12), (20, 13)), ((29, 11), (30, 11), (31, 11), (31, 12))):
        colocar("k", puntos)
    colocar("K", [(30, 13)])
    colocar("Z", [(30, 14)])
    colocar("N", [(21, 14)])
    colocar("S", [(21, 13)])
    colocar("R", [(19, 15), (22, 15), (29, 15), (31, 14), (19, 6)])
    colocar("b", [(22, 13), (30, 12), (29, 14)])

    edificio((44, 2, 50, 5), "c", "g", (47, 5))
    colocar("F", [(45, 3), (49, 3)])
    colocar("N", [(48, 4)])
    colocar("J", [(46, 4), (46, 3)])
    poner(47, 3, "p")
    edificio((37, 11, 41, 14), "d", ":", (39, 14))
    colocar("J", [(38, 12), (40, 12)])
    colocar("B", [(38, 13)])
    colocar("C", [(40, 13)])
    colocar("O", [(43, 12)])
    colocar("L", [(44, 11), (42, 13)])
    colocar("M", [(43, 6), (36, 6), (43, 15), (36, 9)])
    colocar("R", [(48, 11), (43, 3), (41, 6)])
    colocar("b", [(44, 12), (43, 13), (36, 12)])
    colocar("K", [(36, 14)])

    muro(Z[3], "#", huecos=[(x, Z[3][1]) for x in range(24, 28)] + [(x, Z[3][3]) for x in range(24, 28)]
         + [(Z[3][2], y) for y in range(21, 26)])
    pintar((20, 20, 32, 28), "_", True)
    pintar((24, 19, 27, 29), ":", True)
    pintar((24, 21, 33, 25), ":", True)
    pintar((20, 20, 22, 22), "g", True)
    pintar((20, 24, 22, 25), "g", True)
    pintar((20, 27, 22, 28), "g", True)
    colocar("#", [(23, y) for y in range(20, 29)])
    colocar("#", [(x, 23) for x in range(20, 23)] + [(x, 26) for x in range(20, 23)])
    colocar("G", [(23, 21), (23, 24), (23, 27)])
    poner(21, 21, "b")
    poner(22, 22, "x")
    poner(20, 24, "x")
    colocar("J", [(22, 25)])
    colocar("C", [(22, 27)])
    poner(21, 28, "b")
    colocar("#", [(28, 20), (29, 20)])
    colocar("F", [(30, 20), (32, 20), (32, 26), (28, 28)])
    colocar("B", [(30, 27)])
    colocar("X", [(31, 28)])
    colocar("C", [(29, 28)])
    poner(31, 27, "Q")
    poner(29, 26, "U")
    colocar("x", [(30, 26), (32, 27), (28, 27)])
    colocar("b", [(32, 28), (30, 28)])
    reservar(Z[3], 0)

    muro(Z[4], "l", huecos=[(38, y) for y in range(22, 25)] + [(54, y) for y in range(22, 25)]
         + [(x, Z[4][3]) for x in range(48, 52)])
    pintar((39, 19, 53, 28), "r", True)
    pintar((38, 22, 38, 24), ":", True)
    pintar((54, 22, 54, 24), ":", True)
    pintar((48, 29, 51, 29), ":", True)
    colocar("l", [(39, 20), (39, 26), (53, 20), (53, 26), (43, 22), (49, 22), (43, 26), (49, 26)])
    colocar("G", [(42, 18), (46, 18), (50, 18), (41, 29), (44, 29)])
    colocar("F", [(40, 20), (52, 20), (40, 27), (52, 27)])
    colocar("e", [(44, 24), (48, 24), (46, 22), (46, 26)])
    colocar("x", [(45, 23), (47, 25), (46, 25), (44, 25)])
    colocar("b", [(47, 23), (45, 25), (42, 24), (50, 24), (41, 22), (51, 26)])
    reservar(Z[4], 0)

    edificio((59, 3, 63, 6), "d", ":", (61, 6))
    colocar("B", [(60, 4)])
    colocar("J", [(62, 4)])
    edificio((70, 3, 74, 6), "d", ":", (72, 6))
    colocar("C", [(71, 4)])
    colocar("X", [(73, 4)])
    edificio((70, 11, 75, 15), "d", ":", (72, 15))
    colocar("X", [(71, 12), (72, 12), (74, 12)])
    colocar("B", [(71, 14)])
    colocar("L", [(74, 14)])
    for fila, ch in ((12, "w"), (13, "z"), (14, "w"), (15, "z")):
        for x in range(59, 65):
            poner(x, fila, ch)
    colocar("t", [(59, 11), (61, 11), (63, 11)])
    colocar("L", [(58, 13), (69, 16), (69, 8)])
    colocar("B", [(58, 5)])
    colocar("R", [(60, 16), (64, 3), (68, 5)])
    colocar("A", [(69, 13)])
    reservar_circulo(73.5, 8.5, 3.0)

    muro((40, 41, 46, 45), "k", huecos=[(46, 43), (40, 43)], ruina=0.22)
    pintar((41, 42, 45, 44), "_", True)
    colocar("S", [(43, 43)])
    colocar("F", [(41, 42), (45, 42)])
    poner(43, 42, "p")
    colocar("Z", [(42, 44)])
    colocar("K", [(44, 44)])
    reservar((40, 41, 46, 45), 1)
    colocar("M", [(41, 35), (43, 37), (45, 34), (40, 38), (44, 39), (42, 34)])
    colocar("O", [(54, 35)])
    colocar("B", [(55, 35)])
    colocar("C", [(53, 36)])
    colocar("L", [(55, 36), (53, 34)])
    colocar("T", [(55, 33), (56, 34), (54, 33)])
    colocar("R", [(47, 44), (52, 41), (56, 41), (40, 40)])
    reservar_circulo(54.5, 43.5, 3.2)

    c0, f0, c1, f1 = Z[7]
    for x in range(c0, c1 + 1):
        grosor_norte = 3 if 71 <= x <= 75 else 1 + int(ruido(x, 0, 2.0, 11) * 2.6)
        for y in range(f0, f0 + grosor_norte):
            if not reservado[y][x]:
                poner(x, y, "d")
        for y in range(f1, f1 - 1 - int(ruido(x, 1, 2.0, 12) * 2.6), -1):
            if not reservado[y][x]:
                poner(x, y, "d")
    for y in range(f0, f1 + 1):
        for k in range(1 + int(ruido(0, y, 2.0, 13) * 2.4)):
            if not reservado[y][c0 + k]:
                poner(c0 + k, y, "d")
        for k in range(2 + int(ruido(1, y, 2.0, 14) * 1.6)):
            if not reservado[y][c1 - k]:
                poner(c1 - k, y, "d")
    for cx, cy, rx, ry, semilla in ((62.5, 28, 1.7, 1.2, 15), (72, 28.5, 2.2, 1.2, 16), (72.5, 23.5, 1.4, 0.9, 17)):
        mancha(cx, cy, rx, ry, "d", semilla)
    poner(73, 21, "D")
    colocar("X", [(72, 22), (75, 22)])
    colocar("L", [(74, 22)])
    colocar("B", [(71, 21)])
    colocar("R", [(61, 27), (75, 26), (69, 28), (60, 28), (64, 29), (76, 24)])
    colocar("b", [(66, 27), (73, 25), (62, 26)])
    colocar("C", [(74, 30)])
    reservar(Z[7], 0)

    c0, f0, c1, f1 = Z[8]
    pintar((c0 + 1, f0 + 1, c1 - 1, f1 - 1), "r", True)
    for y in range(f0 + 1, f1):
        for x in range(c0 + 1, c1):
            if ruido(x, y, 3.0, 21) > 0.66:
                celdas[y][x] = "o"
    muro(Z[8], "i", huecos=[(x, f0) for x in range(65, 69)] + [(c0, y) for y in range(37, 41)])
    pintar((65, f0, 68, f0), ":", True)
    pintar((c0, 37, c0, 40), ":", True)
    colocar("i", [(61, 36), (61, 44), (77, 36), (77, 44)])
    colocar("F", [(63, 37), (76, 37), (63, 44), (76, 44)])
    colocar("C", [(74, 38), (75, 38), (75, 41), (74, 42), (76, 40)])
    colocar("A", [(76, 38), (75, 40)])
    colocar("S", [(62, 42), (64, 36)])
    colocar("R", [(66, 43), (72, 37), (72, 44), (70, 44), (66, 37), (77, 42)])
    colocar("b", [(65, 41), (67, 39), (71, 41), (73, 39), (70, 42), (68, 43), (73, 43), (64, 40)])
    colocar("x", [(69, 42), (71, 39)])
    poner(72, 42, "p")
    reservar(Z[8], 0)

    muro((3, 33, 13, 42), "c", huecos=[(8, 33), (9, 33)], ruina=0.12)
    pintar((4, 34, 12, 41), "o", True)
    for y in (35, 37, 39):
        for x in (5, 7, 9, 11):
            poner(x, y, rng.choice("KKSN"))
    poner(8, 38, "p")
    colocar("F", [(5, 41), (11, 41), (5, 34), (11, 34)])
    colocar("b", [(6, 36), (10, 38), (8, 35), (6, 40), (10, 40)])
    reservar((3, 33, 13, 42), 1)

    edificio((14, 22, 18, 25), "d", ":", (16, 25))
    colocar("B", [(15, 23)])
    colocar("J", [(17, 23)])
    colocar("O", [(15, 27)])
    colocar("L", [(13, 28), (19, 26)])
    colocar("R", [(13, 20), (12, 27), (2, 26), (12, 22)])
    reservar_circulo(7, 23, 6.0)

    edificio((32, 33, 36, 36), "d", ":", (34, 36))
    colocar("C", [(33, 34)])
    colocar("J", [(35, 34)])
    colocar("O", [(32, 40)])
    colocar("L", [(29, 40), (34, 41), (30, 41)])
    colocar("B", [(28, 41), (34, 39)])
    colocar("X", [(30, 37), (35, 39)])
    colocar("C", [(35, 41)])
    colocar("b", [(33, 40), (31, 38), (33, 42)])
    reservar_circulo(32, 40, 4.0)
    edificio((30, 43, 35, 46), "#", "_", (32, 43))
    colocar("F", [(31, 44), (34, 44)])
    colocar("C", [(33, 45)])
    colocar("S", [(31, 45)])

    colocar("R", [(35, 18), (36, 27), (35, 31), (34, 20), (36, 19), (16, 3), (17, 13), (16, 12), (33, 12), (34, 12)])
    colocar("M", [(35, 5), (34, 13), (16, 5), (17, 12), (36, 32), (47, 31)])
    colocar("R", [(60, 34), (64, 17), (70, 17), (76, 17)])
    colocar("C", [(77, 12)])

    for x, y in ((23, 6), (28, 6), (23, 11), (28, 11), (12, 6), (12, 11), (35, 6), (35, 11), (46, 6), (46, 11),
                 (55, 6), (58, 6), (55, 11), (58, 11), (55, 20), (58, 20), (55, 26), (58, 26),
                 (23, 30), (28, 30), (23, 38), (28, 38), (47, 30), (52, 30), (47, 36), (52, 41),
                 (64, 7), (69, 7), (64, 11), (69, 11), (64, 27), (69, 27), (64, 33), (69, 33), (64, 42), (69, 42)):
        if dentro(x, y) and celdas[y][x] in VERDES:
            poner(x, y, "q")

    DENSIDAD = {None: 0.55, 0: 0.42, 1: 0.10, 2: 0.15, 3: 0.0, 4: 0.0, 5: 0.09, 6: 0.66, 7: 0.0, 8: 0.0}
    for y in range(alto):
        for x in range(ancho):
            if celdas[y][x] not in VERDES or reservado[y][x]:
                continue
            zona = zona_en(x, y)
            borde = min(x, y, ancho - 1 - x, alto - 1 - y)
            if zona is None and borde <= 1:
                p = 0.93
            elif zona is None and borde <= 3:
                p = 0.62
            else:
                p = DENSIDAD[zona] * (0.3 + 1.5 * ruido(x, y, 5.0, 1) ** 1.3)
            if rng.random() >= p:
                continue
            r = rng.random()
            if zona == 2:
                celdas[y][x] = "y" if r < 0.55 else ("t" if r < 0.9 else "T")
            elif zona == 6:
                celdas[y][x] = "T" if r < 0.58 else ("t" if r < 0.88 else "y")
            else:
                celdas[y][x] = "T" if r < 0.36 else ("t" if r < 0.76 else "y")

    DECORACION = {
        None: (("h", 0.07), ("f", 0.05), ("m", 0.02), ("b", 0.004)),
        0: (("h", 0.10), ("f", 0.04), ("m", 0.05), ("b", 0.004)),
        2: (("s", 0.05), ("j", 0.05), ("m", 0.04), ("b", 0.015)),
        5: (("f", 0.22), ("h", 0.05)),
        6: (("h", 0.14), ("m", 0.06), ("f", 0.02)),
    }
    for y in range(alto):
        for x in range(ancho):
            if celdas[y][x] not in VERDES:
                continue
            tabla = DECORACION.get(zona_en(x, y), ())
            r = rng.random()
            acumulado = 0.0
            for ch, prob in tabla:
                acumulado += prob
                if r < acumulado:
                    celdas[y][x] = ch
                    break
    for y in range(alto):
        for x in range(ancho):
            if celdas[y][x] in VERDES and any(dentro(x + dx, y + dy) and celdas[y + dy][x + dx] in ("~", "v")
                                              for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                if rng.random() < 0.55:
                    celdas[y][x] = "j"

    celdas[8][7] = "P"
    for zona in ZONAS:
        for x, y in zona.get("puertas", ()):
            celdas[y][x] = "G"
    return ["".join(fila) for fila in celdas]


# El plano generado se comparte entre renderizado, navegación y zonas de oleadas.
MAPA = _crear_mapa()

MUNDO_ANCHO = len(MAPA[0]) * TAM_TILE
MUNDO_ALTO = len(MAPA) * TAM_TILE

# Fin de las constantes de configuracion y del plano del mundo.
print("---------- FIN DE LA CONFIGURACION ----------")

print("---------- ESTADO DE LA PARTIDA Y RECURSOS GRAFICOS ----------")
# Estados de interfaz y referencias globales compartidas entre el bucle y las pantallas.
print("---------- ESTADO INTERNO, COLORES Y FUENTES ----------")
blanco = (255, 255, 255)
negro = (0, 0, 0)
amarillo = (255, 220, 80)
width = 1549
height = 900
RUN = True
JUGAR = False
CARGANDO = False
TIEMPO_CARGA = 1.8
tiempo_carga_restante = 0.0
AJUSTES = False
MUSICA = False
PAUSA = False
RANURAS = False
CONTROLES = False
MOSTRAR_HITBOX = False
MOSTRAR_HUD = True
MOSTRAR_CONTROLES = True
CURSOR_BLOQUEADO = False
camara = pygame.Vector2(0, 0)
mapa = None
partida = None
captura = None
menu_font = pygame.font.Font(None, 45)
titulo_font = pygame.font.Font(None, 110)
fuente_peq = pygame.font.Font(None, 34)
reloj = pygame.time.Clock()

# Busca las canciones de la carpeta 'musica' y prepara la lista de reproduccion.
print("---------- MUSICA: LISTA DE REPRODUCCION ----------")
MUSICA_EXT = (".mp3", ".ogg", ".wav")


# Descubre las pistas reproducibles en la carpeta de música del proyecto.
def buscar_canciones():
    rutas = []
    if os.path.isdir("musica"):
        for n in sorted(os.listdir("musica")):
            if n.lower().endswith(MUSICA_EXT):
                rutas.append(os.path.join("musica", n))
    return rutas


canciones = buscar_canciones()
activas = {c: True for c in canciones}
actual = -1
scroll = 0
FILAS_VISIBLES = 7

ajustes = {"musica": 0.0, "efectos": 0.5, "pantalla_completa": True, "mostrar_fps": False}
audio_acciones = AudioAcciones(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "sonidos")
)
audio_acciones.cargar()

SONIDOS_ATAQUE = (
    "ataque_espada",
    "ataque_embestida",
    "ataque_aereo",
    "ataque_giro",
    "ataque_enemigo_cuerpo",
    "ataque_enemigo_distancia",
    "ataque_jefe",
)


# Aplica el volumen de efectos y delega la reproducción al gestor de sonidos.
def reproducir_sonido(nombre, bloquear_si_activo=(), reemplazar=()):
    return audio_acciones.reproducir(
        nombre,
        ajustes["efectos"],
        bloquear_si_activo=bloquear_si_activo,
        reemplazar=reemplazar,
    )


# Prepara el almacen MySQL, las ranuras de guardado y los rectangulos de la interfaz de ajustes.
print("---------- GUARDADO DE PARTIDAS ----------")
almacen_guardados = MySQLSaveSlots()
ranuras_guardadas = {}
estado_ranuras = ""
ranura_activa = None
progreso_carga_pendiente = None
ranuras_boton = pygame.Rect(0, 0, 380, 56)
ranuras_boton.center = (width // 2, 690)
ranuras_filas = {
    numero: pygame.Rect(150, 240 + (numero - 1) * 145, 1300, 112)
    for numero in (1, 2, 3)
}
ranuras_cargar = {
    numero: pygame.Rect(1000, 270 + (numero - 1) * 145, 180, 54)
    for numero in (1, 2, 3)
}
ranuras_guardar = {
    numero: pygame.Rect(1200, 270 + (numero - 1) * 145, 180, 54)
    for numero in (1, 2, 3)
}
boton_ranuras_final = pygame.Rect(0, 0, 380, 56)
boton_ranuras_final.center = (width // 2, 205)
sliders = {
    "musica": pygame.Rect(800, 294, 400, 12),
    "efectos": pygame.Rect(800, 374, 400, 12),
}
interruptores = {
    "pantalla_completa": pygame.Rect(800, 438, 120, 48),
    "mostrar_fps": pygame.Rect(800, 518, 120, 48),
}
arrastrando = None

# Crea la superficie logica del juego y la ventana en pantalla completa.
print("---------- CONFIGURACION DE VENTANA ----------")

game_surface = pygame.Surface((width, height))
ventana = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("DUNGEON FANTASY")


print("---------- FONDO PERSONALIZADO Y VIDEO ----------")
# Carga una imagen estática de menú o genera un degradado como alternativa.
def cargar_fondo():
    carpeta_proyecto = os.path.dirname(os.path.abspath(__file__))
    for nombre in ("fondo.png", "fondo.jpg", "fondo.jpeg"):
        ruta = os.path.join(carpeta_proyecto, nombre)
        if os.path.exists(ruta):
            img = pygame.image.load(ruta).convert()
            return pygame.transform.smoothscale(img, (width, height))
    s = pygame.Surface((width, height))
    for y in range(height):
        t = y / height
        pygame.draw.line(s, (int(20 + 30 * t), int(15 + 10 * t), int(50 + 60 * t)), (0, y), (width, y))
    return s


# Reproduce un video en bucle como fondo del menu, leyendo fotogramas con OpenCV.
class FondoVideo:
    # Gestiona la lectura cíclica y conversión de fotogramas de un vídeo para Pygame.
    def __init__(self, ruta):
        import cv2

        self.cv2 = cv2
        self.captura = cv2.VideoCapture(ruta)
        if not self.captura.isOpened():
            self.captura.release()
            raise RuntimeError(f"No se pudo abrir el video de fondo: {ruta}")
        fps = self.captura.get(cv2.CAP_PROP_FPS)
        self.intervalo = 1.0 / fps if fps > 0 else 1.0 / 30
        self.siguiente_frame = 0
        self.superficie = None
        self._leer_frame()

    # Lee el siguiente fotograma; al llegar al final, reinicia el vídeo desde el comienzo.
    def _leer_frame(self):
        correcto, frame = self.captura.read()
        if not correcto:
            self.captura.set(self.cv2.CAP_PROP_POS_FRAMES, 0)
            correcto, frame = self.captura.read()
        if not correcto:
            raise RuntimeError("No se pudo leer un fotograma de fondo.mp4")
        frame = self.cv2.resize(frame, (width, height), interpolation=self.cv2.INTER_AREA)
        frame = self.cv2.cvtColor(frame, self.cv2.COLOR_BGR2RGB)
        self.superficie = pygame.image.frombuffer(frame.tobytes(), (width, height), "RGB").copy()
        self.siguiente_frame = pygame.time.get_ticks() + self.intervalo * 1000

    # Actualiza el fotograma cuando vence su intervalo y lo dibuja en la superficie.
    def dibujar(self, superficie):
        if pygame.time.get_ticks() >= self.siguiente_frame:
            self._leer_frame()
        superficie.blit(self.superficie, (0, 0))

    # Libera el archivo de video abierto.
    def cerrar(self):
        self.captura.release()


fondo_menu = cargar_fondo()
video_fondo = None
ruta_video_fondo = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fondo.mp4")
if os.path.isfile(ruta_video_fondo):
    try:
        video_fondo = FondoVideo(ruta_video_fondo)
    except (ImportError, OSError, RuntimeError) as error:
        print(f"Aviso: se usara el fondo estatico; {error}")
velo = pygame.Surface((width, height), pygame.SRCALPHA)
velo.fill((0, 0, 0, 120))

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
boton_canciones.center = (width // 2, 600)
boton_anterior = pygame.Rect(0, 0, 260, 56)
boton_anterior.center = (width // 2 - 200, 690)
boton_siguiente = pygame.Rect(0, 0, 260, 56)
boton_siguiente.center = (width // 2 + 200, 690)
boton_volver_musica = pygame.Rect(0, 0, 260, 56)
boton_volver_musica.center = (width // 2, 840)
boton_volver_controles = pygame.Rect(0, 0, 260, 56)
boton_volver_controles.center = (width // 2, 840)

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

# A partir de aqui se definen las clases del juego.
print("------------CLASES U OBJETOS------------")

# Objetos del escenario (props, cofres, pociones) y el mapa con sus colisiones y dibujo.
print("---------- CLASES DEL MAPA ----------")
class Prop:
    # Elemento visual del mapa, anclado por los pies y opcionalmente animado/ sólido.
    def __init__(self, frames, pie, colision=None, fps=0, desfase=0.0):
        self.frames = frames
        self.fps = fps
        self.desfase = desfase
        self.pie = pie
        self.solido = colision is not None
        ancho, alto = colision if colision else (1, 1)
        self.rect = pygame.Rect(0, 0, int(ancho), int(alto))
        self.rect.midbottom = pie

    # Dibuja el fotograma actual del objeto (animado o fijo), anclado por los pies.
    def dibujar(self, superficie, cam=(0, 0)):
        if self.fps and len(self.frames) > 1:
            imagen = self.frames[int(pygame.time.get_ticks() / 1000 * self.fps + self.desfase) % len(self.frames)]
        else:
            imagen = self.frames[0]
        superficie.blit(imagen, imagen.get_rect(midbottom=(self.pie[0] - cam[0], self.pie[1] - cam[1])))


# Prop con dos estados visuales (cerrado/abierto); abrirlo solo cambia el estado una vez.
class Cofre(Prop):
    # Prop con dos estados visuales; abrirlo solo cambia el estado una vez.
    def __init__(self, imagen, imagen_abierta, pie, colision):
        super().__init__([imagen], pie, colision)
        self.abierto = False
        self.imagen_abierta = pygame.transform.scale(imagen_abierta, imagen.get_size())

    # Marca el cofre como abierto y devuelve False si ya lo estaba.
    def abrir(self):
        if self.abierto:
            return False
        self.abierto = True
        return True

    # Dibuja la imagen del cofre segun su estado, anclada por los pies.
    def dibujar(self, superficie, cam=(0, 0)):
        imagen = self.imagen_abierta if self.abierto else self.frames[0]
        superficie.blit(imagen, imagen.get_rect(midbottom=(self.pie[0] - cam[0], self.pie[1] - cam[1])))


# Objeto recogible del mundo, con un rectangulo para detectar el contacto del jugador.
class Pocion:
    # Objeto recogible situado en el mundo, con rectángulo para detectar contacto.
    def __init__(self, pos):
        self.pos = pygame.Vector2(pos)
        self.rect = pygame.Rect(0, 0, 16 * ESCALA_TILES, 16 * ESCALA_TILES)
        self.rect.center = self.pos

    # Dibuja la pocion con un aro rojo a su alrededor.
    def dibujar(self, superficie, cam=(0, 0)):
        tamano = 18 * ESCALA_TILES
        imagen = cargar_imagen_pocion((tamano, tamano))
        centro = (self.rect.centerx - cam[0], self.rect.centery - cam[1])
        pygame.draw.circle(superficie, (245, 70, 90), centro, self.rect.width // 2 + 6 * ESCALA_TILES, 3)
        superficie.blit(imagen, imagen.get_rect(center=centro))


# Interpreta el plano de texto como suelos, muros, objetos, liquidos, rejas y colisiones, y lo dibuja.
class Mapa:
    # Interpreta el plano en tiles, colisiones, decoraciones, cofres, líquidos y puertas.
    SUELOS = {
        "bosque": ([(14, 1), (15, 2), (15, 3), (15, 4), (14, 2), (14, 3)], [60, 10, 10, 10, 5, 5]),
        "camino": ([(9, 2), (9, 3), (9, 4)], [1, 1, 1]),
        "losa": ([(10, 2), (10, 3), (10, 4)], [1, 1, 1]),
        "losa_roja": ([(12, 2), (12, 3), (12, 4)], [1, 1, 1]),
        "pradera": ([(14, 1), (15, 2), (15, 3), (15, 4)], [30, 25, 25, 20]),
        "barro": ([(14, 1), (14, 2), (14, 3), (14, 4)], [45, 20, 20, 15]),
        "hueso": ([(16, 1), (16, 2), (16, 3), (16, 4)], [6, 2, 2, 2]),
        "mazmorra": ([(7, 1), (7, 2), (7, 3), (7, 4)], [8, 2, 2, 2]),
    }
    TERRENOS = {
        ".": "bosque", ":": "camino", "_": "losa", "r": "losa_roja",
        ";": "pradera", ",": "barro", "o": "hueso", "g": "mazmorra",
    }
    MUROS = {
        "#": ((3, 1), ([(3, 2), (3, 3)], [3, 1])),
        "d": ((1, 1), ([(1, 2)], [1])),
        "k": ((2, 1), ([(2, 2)], [1])),
        "i": ((4, 1), ([(4, 2)], [1])),
        "l": ((5, 1), ([(5, 2)], [1])),
        "c": ((6, 1), ([(6, 2)], [1])),
    }
    REJAS = {"G": (17, 7)}
    LIQUIDOS = {"~": ("_agua", 11), "v": ("_veneno", 12)}
    OBJETOS = {
        "T": ([(25, 4)], 2, (12, 11)),
        "t": ([(26, 3)], 1, (9, 9)),
        "y": ([(26, 1), (26, 2)], 1, (6, 6)),
        "R": ([(19, 1), (19, 2)], 1, (20, 11)),
        "M": ([(21, 2)], 1, (10, 7)),
        "L": ([(18, 7)], 1, (20, 11)),
        "C": ([(18, 1)], 1, (20, 11)),
        "A": ([(18, 2)], 1, (20, 11)),
        "B": ([(18, 5)], 1, (16, 11)),
        "J": ([(18, 3)], 1, (16, 11)),
        "X": ([(18, 6)], 1, (14, 10)),
        "K": ([(24, 1), (24, 2)], 1, (14, 10)),
        "N": ([(24, 3)], 1, (14, 10)),
        "S": ([(24, 4), (24, 5)], 1, (20, 12)),
        "Z": ([(24, 6)], 1, (20, 12)),
    }
    DECORADOS = {
        "m": [(21, 1)],
        "b": [(22, 1), (22, 2)],
        "p": [(17, 15)],
        "D": [(17, 4)],
        "Q": [(17, 8)],
        "U": [(17, 13)],
        "e": [(17, 16)],
        "f": [(20, 1), (20, 2), (20, 7), (20, 10), (20, 12), (20, 14), (20, 15), (20, 16)],
        "h": [(20, 3), (20, 4), (20, 5)],
        "j": [(20, 6)],
        "w": [(20, 8)],
        "z": [(20, 9), (20, 7)],
        "x": [(23, 1), (23, 2)],
        "s": [(23, 3), (23, 4)],
    }
    ANIMADOS = {
        "F": (2, (14, 9), 8),
        "O": (4, (16, 10), 8),
        "q": (8, (8, 8), 5),
    }

    # Carga los tilesets y crea las estructuras que usan dibujo, navegación y colisiones.
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
            if video_fondo is not None:
               video_fondo.cerrar()
            pygame.quit()
            sys.exit()
        self.hoja_tiles = pygame.image.load(os.path.join(carpeta, "tiles.png")).convert_alpha()
        self.hoja_auto = pygame.image.load(os.path.join(carpeta, "autotiles.png")).convert_alpha()
        self.hoja_anim = pygame.image.load(os.path.join(carpeta, "animated-tiles.png")).convert_alpha()
        self.imagen_cofre_abierto = pygame.image.load(
            os.path.join(carpeta, "cofre_abierto.png")
        ).convert_alpha()
        self._cache = {}
        self.suelo = [[[] for _ in range(self.cols)] for _ in range(self.filas)]
        self.terreno_solido = [[False] * self.cols for _ in range(self.filas)]
        self.bloqueada = [[False] * self.cols for _ in range(self.filas)]
        self.bloquea_vista = [[False] * self.cols for _ in range(self.filas)]
        self.props = []
        self.cofres = []
        self.solidos_en = {}
        self.animados = []
        self.puertas_abiertas = set()
        self.suelo_puerta = {}
        self.reja_temporal = None
        self.puerta_img = escalar_imagen(
            self.hoja_tiles.subsurface(((17 - 1) * 32, (7 - 1) * 32, 32, 32)).copy(),
            ESCALA_TILES,
        )
        self.inicio = (self.cols * TAM_TILE // 2, self.filas * TAM_TILE // 2)
        self._agua = self._autotiles(1)
        self._veneno = self._autotiles(5)
        self._construir()

    # Extrae del tileset una imagen escalada y la conserva en caché.
    def pieza(self, fila, col, alto=1):
        clave = (fila, col, alto)
        if clave not in self._cache:
            img = self.hoja_tiles.subsurface(((col - 1) * 32, (fila - 1) * 32, 32, 32 * alto)).copy()
            self._cache[clave] = escalar_imagen(img, ESCALA_TILES)
        return self._cache[clave]

    # Describe los bordes opacos y esquinas de un autotile para poder emparejarlo con sus vecinos.
    @staticmethod
    def _firma(tile):
        # Indica si un pixel del tile no es transparente.
        def opaco(x, y):
            return tile.get_at((x, y)).a > 0
        n, e, s, w = opaco(16, 0), opaco(31, 16), opaco(16, 31), opaco(0, 16)
        # Comprueba si una esquina del autotile esta cubierta de pixeles opacos.
        def esquina(x0, y0, lados):
            if not all(lados):
                return False
            return all(tile.get_at((x, y)).a > 0 for y in range(y0, y0 + 6) for x in range(x0, x0 + 6))
        return (n, e, s, w, esquina(0, 0, (n, w)), esquina(26, 0, (n, e)), esquina(0, 26, (s, w)), esquina(26, 26, (s, e)))

    # Indexa las piezas de agua o veneno por la forma de sus bordes transparentes.
    def _autotiles(self, fila0):
        piezas = {}
        for f in range(4):
            for c in range(12):
                tile = self.hoja_auto.subsurface((c * 32, (fila0 - 1 + f) * 32, 32, 32)).copy()
                if pygame.mask.from_surface(tile).count() == 0:
                    continue
                piezas.setdefault(self._firma(tile), escalar_imagen(tile, ESCALA_TILES))
        return piezas

    # Comprueba si una casilla esta dentro del mapa.
    def _dentro(self, x, y):
        return 0 <= x < self.cols and 0 <= y < self.filas

    # Elige el terreno de una casilla; si no tiene uno propio, toma el mas frecuente entre sus vecinas.
    def _terreno_de(self, x, y):
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

    # Carga y guarda en cache los fotogramas de una fila de tiles animados.
    def _frames_anim(self, fila):
        clave = ("anim", fila)
        if clave not in self._cache:
            frames = []
            for c in range(self.hoja_anim.get_width() // 32):
                img = self.hoja_anim.subsurface((c * 32, (fila - 1) * 32, 32, 32)).copy()
                if pygame.mask.from_surface(img).count() > 0:
                    frames.append(escalar_imagen(img, ESCALA_TILES))
            self._cache[clave] = frames
        return self._cache[clave]

    # Indica si la casilla vecina es del mismo liquido (o queda fuera del mapa).
    def _mismo(self, x, y, ch):
        return not self._dentro(x, y) or self.plano[y][x] == ch

    # Recorre el plano y materializa terrenos, líquidos, muros, decoraciones y objetos.
    def _construir(self):
        rng = random.Random(7)
        T = TAM_TILE
        for y in range(self.filas):
            for x in range(self.cols):
                ch = self.plano[y][x]
                capas = self.suelo[y][x]
                centro = ((x + 0.5) * T, (y + 0.5) * T)
                pie = ((x + 0.5) * T, (y + 1) * T - 2 * ESCALA_TILES)
                if ch in self.MUROS:
                    superior, (opciones, pesos) = self.MUROS[ch]
                    abajo = self.plano[y + 1][x] if self._dentro(x, y + 1) else "."
                    if abajo in self.MUROS:
                        capas.append(self.pieza(*superior))
                    else:
                        capas.append(self.pieza(*rng.choices(opciones, pesos)[0]))
                    self.terreno_solido[y][x] = self.bloqueada[y][x] = self.bloquea_vista[y][x] = True
                    continue
                opciones, pesos = self.SUELOS[self._terreno_de(x, y)]
                capas.append(self.pieza(*rng.choices(opciones, pesos)[0]))
                if ch in self.LIQUIDOS:
                    atributo, fila_anim = self.LIQUIDOS[ch]
                    n, e, s, w = self._mismo(x, y - 1, ch), self._mismo(x + 1, y, ch), self._mismo(x, y + 1, ch), self._mismo(x - 1, y, ch)
                    firma = (n, e, s, w, n and w and self._mismo(x - 1, y - 1, ch), n and e and self._mismo(x + 1, y - 1, ch),
                             s and w and self._mismo(x - 1, y + 1, ch), s and e and self._mismo(x + 1, y + 1, ch))
                    piezas = getattr(self, atributo)
                    capas.append(piezas.get(firma) or piezas[(True,) * 8])
                    self.terreno_solido[y][x] = self.bloqueada[y][x] = True
                    if rng.random() < 0.4:
                        frames = self._frames_anim(fila_anim)
                        self.animados.append(Prop(frames, ((x + 0.5) * T, (y + 1) * T), fps=5, desfase=rng.random() * len(frames)))
                elif ch in self.REJAS:
                    self.suelo_puerta[(x, y)] = capas[0]
                    capas.append(self.pieza(*self.REJAS[ch]))
                    self.terreno_solido[y][x] = self.bloqueada[y][x] = True
                elif ch in self.DECORADOS:
                    capas.append(self.pieza(*rng.choice(self.DECORADOS[ch])))
                elif ch in self.OBJETOS:
                    piezas, alto, (cw, chh) = self.OBJETOS[ch]
                    fila, col = rng.choice(piezas)
                    imagen = self.pieza(fila, col, alto)
                    if ch == "C":
                        prop = Cofre(
                            imagen,
                            self.imagen_cofre_abierto,
                            pie,
                            (cw * ESCALA_TILES, chh * ESCALA_TILES),
                        )
                        self.cofres.append(prop)
                    else:
                        prop = Prop([imagen], pie, (cw * ESCALA_TILES, chh * ESCALA_TILES))
                    self.props.append(prop)
                    self.solidos_en.setdefault((y, x), []).append(prop)
                    self.bloqueada[y][x] = True
                elif ch in self.ANIMADOS:
                    fila_anim, (cw, chh), fps = self.ANIMADOS[ch]
                    prop = Prop(self._frames_anim(fila_anim), pie, (cw * ESCALA_TILES, chh * ESCALA_TILES),
                                fps=fps, desfase=rng.random() * 6)
                    self.props.append(prop)
                    self.solidos_en.setdefault((y, x), []).append(prop)
                    self.bloqueada[y][x] = True
                elif ch == "P":
                    self.inicio = (centro[0], centro[1] + 10)

    # Convierte las puertas seleccionadas en casillas transitables y devuelve las abiertas.
    def abrir_puertas(self, puertas):
        abiertas = []
        for x, y in puertas:
            posicion = (x, y)
            if posicion not in self.suelo_puerta or posicion in self.puertas_abiertas:
                continue
            self.suelo[y][x] = [self.suelo_puerta[posicion]]
            self.terreno_solido[y][x] = False
            self.bloqueada[y][x] = False
            self.bloquea_vista[y][x] = False
            self.puertas_abiertas.add(posicion)
            abiertas.append(posicion)
        return abiertas

    # Restaura cofres y puertas a su estado inicial para una partida nueva.
    def reiniciar_progreso(self):
        for cofre in self.cofres:
            cofre.abierto = False
        for x, y in self.puertas_abiertas:
            self.suelo[y][x] = [self.suelo_puerta[(x, y)], self.puerta_img]
            self.terreno_solido[y][x] = True
            self.bloqueada[y][x] = True
            self.bloquea_vista[y][x] = False
        self.puertas_abiertas.clear()
        self.reja_temporal = None

    # Dibuja las casillas visibles, la reja temporal y los elementos animados del suelo.
    def dibujar_suelo(self, superficie, cam):
        T = TAM_TILE
        superficie.fill((14, 18, 18))
        c0, c1 = max(0, cam[0] // T), min(self.cols - 1, (cam[0] + width) // T)
        f0, f1 = max(0, cam[1] // T), min(self.filas - 1, (cam[1] + height) // T)
        for f in range(f0, f1 + 1):
            for c in range(c0, c1 + 1):
                x, y = c * T - cam[0], f * T - cam[1]
                for capa in self.suelo[f][c]:
                    superficie.blit(capa, (x, y))
        if self.reja_temporal is not None:
            x, y, ancho = self.reja_temporal
            for columna in range(ancho):
                superficie.blit(
                    self.puerta_img,
                    (int((x + columna) * T - cam[0]), int(y * T - cam[1])),
                )
        x0, x1 = cam[0] - T, cam[0] + width + T
        y0, y1 = cam[1], cam[1] + height + T
        for animado in self.animados:
            if x0 <= animado.pie[0] <= x1 and y0 <= animado.pie[1] <= y1:
                animado.dibujar(superficie, cam)

    # Devuelve los objetos del mapa que caen dentro de la camara.
    def props_visibles(self, cam):
        x0, x1 = cam[0] - TAM_TILE, cam[0] + width + TAM_TILE
        y0, y1 = cam[1], cam[1] + height + 2 * TAM_TILE
        return [p for p in self.props if x0 <= p.pie[0] <= x1 and y0 <= p.pie[1] <= y1]

    # Dibuja las cajas de colision del terreno y los objetos (modo depuracion).
    def dibujar_colisiones(self, superficie, cam):
        T = TAM_TILE
        for f in range(max(0, cam[1] // T), min(self.filas, (cam[1] + height) // T + 1)):
            for c in range(max(0, cam[0] // T), min(self.cols, (cam[0] + width) // T + 1)):
                if self.terreno_solido[f][c]:
                    pygame.draw.rect(superficie, (255, 40, 40), (c * T - cam[0], f * T - cam[1], T, T), 1)
        for p in self.props_visibles(cam):
            if p.solido:
                pygame.draw.rect(superficie, (255, 160, 0), p.rect.move(-cam[0], -cam[1]), 2)

    # Calcula por búsqueda en anchura qué casillas libres se conectan con el destino.
    def celdas_alcanzables(self, inicio, limite):
        c0, f0, c1, f1 = limite
        vistas = {inicio}
        cola = [inicio]
        for c, f in cola:
            for dc, df in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nc, nf = c + dc, f + df
                if c0 <= nc <= c1 and f0 <= nf <= f1 and (nc, nf) not in vistas and not self.bloqueada[nf][nc]:
                    vistas.add((nc, nf))
                    cola.append((nc, nf))
        return vistas

    # Detecta solapamiento con límites, terreno sólido y rectángulos de objetos.
    def choca(self, rect):
        T = TAM_TILE
        if rect.left < 0 or rect.top < 0 or rect.right > self.cols * T or rect.bottom > self.filas * T:
            return True
        if self.reja_temporal is not None:
            x, y, ancho = self.reja_temporal
            barrera = pygame.Rect(x * T, y * T, ancho * T, T)
            if rect.colliderect(barrera):
                return True
        for f in range(rect.top // T, (rect.bottom - 1) // T + 1):
            for c in range(rect.left // T, (rect.right - 1) // T + 1):
                if self.terreno_solido[f][c]:
                    return True
                for p in self.solidos_en.get((f, c), ()):
                    if rect.colliderect(p.rect):
                        return True
        return False

    # Comprueba si algun muro bloquea la linea de vision entre dos puntos.
    def hay_vista(self, a, b):
        T = TAM_TILE
        pasos = max(1, int(math.hypot(b[0] - a[0], b[1] - a[1]) // 32))
        for i in range(1, pasos):
            x = a[0] + (b[0] - a[0]) * i / pasos
            y = a[1] + (b[1] - a[1]) * i / pasos
            c, f = int(x // T), int(y // T)
            if self._dentro(c, f) and self.bloquea_vista[f][c]:
                return False
        return True

    # Verifica si un rectangulo puede recorrer una linea recta sin chocar.
    def paso_libre(self, a, b, ancho, alto):
        pasos = max(1, int(math.hypot(b[0] - a[0], b[1] - a[1]) // 16))
        caja = pygame.Rect(0, 0, int(ancho), int(alto))
        for i in range(pasos + 1):
            caja.center = (a[0] + (b[0] - a[0]) * i / pasos, a[1] + (b[1] - a[1]) * i / pasos)
            if self.choca(caja):
                return False
        return True

    # Devuelve una ruta de casillas transitables entre dos puntos del mapa.
    def camino(self, a, b):
        T = TAM_TILE
        ini = (min(self.filas - 1, max(0, int(a[1] // T))), min(self.cols - 1, max(0, int(a[0] // T))))
        fin = (min(self.filas - 1, max(0, int(b[1] // T))), min(self.cols - 1, max(0, int(b[0] // T))))
        if ini == fin:
            return [b]
        previo = {ini: None}
        cola = [ini]
        for f, c in cola:
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


# Controla las oleadas por zona: progreso, avisos, apariciones, barreras y puntuacion.
print("---------- CLASE DE OLEADAS Y PROGRESO ----------")
class Oleadas:
    # Valida las zonas y dirige el progreso, los avisos, las apariciones y la puntuación.
    def __init__(self, zonas):
        T = TAM_TILE
        self.zonas = []
        self.puntuacion = 0
        for nivel, z in enumerate(zonas, 1):
            c0, f0, c1, f1 = z["casillas"]
            dc, df = z["destino"]
            if not mapa._dentro(dc, df) or mapa.bloqueada[df][dc]:
                raise ValueError(f"El destino de la zona {z['nombre']} no es transitable: {(dc, df)}")
            libres = mapa.celdas_alcanzables((dc, df), (c0, f0, c1, f1))
            if not libres:
                raise ValueError(f"La zona {z['nombre']} no tiene puntos de aparicion alcanzables")
            tipos_enemigos = tuple(z.get("tipos_enemigos", ("goblin",)))
            if not z.get("jefe") and not tipos_enemigos:
                raise ValueError(f"La zona {z['nombre']} necesita al menos un tipo de enemigo")
            for tipo in tipos_enemigos:
                if tipo not in ARQUETIPOS_ENEMIGO:
                    raise ValueError(
                        f"Arquetipo de enemigo desconocido: {tipo} en la zona {z['nombre']}"
                    )
            tipos_apoyo = tuple(z.get("tipos_apoyo", ()))
            for tipo in tipos_apoyo:
                if tipo not in ARQUETIPOS_ENEMIGO:
                    raise ValueError(
                        f"Arquetipo de apoyo desconocido: {tipo} en la zona {z['nombre']}"
                    )
            sprite_jefe = z.get("sprite_jefe", "goblin")
            if z.get("jefe") and not os.path.isfile(ruta_sprite_enemigo(sprite_jefe)):
                raise ValueError(
                    f"No existe el sprite enemigos/{sprite_jefe}.png configurado para el jefe de {z['nombre']}"
                )
            self.zonas.append({
                "nivel": nivel, "nombre": z["nombre"], "color": z["color"], "cerrada": z.get("cerrada", True),
                "rect": pygame.Rect(c0 * T, f0 * T, (c1 - c0 + 1) * T, (f1 - f0 + 1) * T),
                "destino": ((dc + 0.5) * T, (df + 0.5) * T),
                "dist": z.get("distancia_aparicion", 600),
                "total": 1 if z.get("jefe") else z.get(
                    "enemigos_derrotar", z.get("enemigos", OLEADA_ENEMIGOS_BASE + OLEADA_ENEMIGOS_MAS * (nivel - 1))
                ),
                "jefe": z.get("jefe", False),
                "sprite_jefe": sprite_jefe,
                "tipo_jefe": z.get("tipo_jefe", "dragon" if sprite_jefe == "dragon" else "goblin"),
                "puertas": tuple(z.get("puertas", ())),
                "reja_temporal": z.get("reja_temporal"),
                "tipos_apoyo": tipos_apoyo,
                "max_apoyos": z.get("max_apoyos", 0),
                "max_vivos": z.get("max_vivos", OLEADA_MAX_VIVOS_BASE + OLEADA_MAX_VIVOS_MAS * (nivel - 1)),
                "intervalo": z.get(
                    "intervalo_aparicion",
                    z.get("intervalo", max(OLEADA_INTERVALO_MIN, OLEADA_INTERVALO_BASE - OLEADA_INTERVALO_MENOS * (nivel - 1)))
                ),
                "tipos_enemigos": tipos_enemigos,
                "puntos": [((c + 0.5) * T, (f + 1) * T - 3 * ESCALA_TILES) for c, f in sorted(libres)],
                "estado": "pendiente",
                "generados": 0, "matados": 0, "t_prep": 0.0, "t_spawn": 0.0,
                "tiempo_oleada": 0.0, "puntos_ganados": 0,
            })
        self.t = 0.0
        self.aviso, self.t_aviso = [], 0.0
        self.t_barrera = 0.0
        self.objetivo_flecha, self.t_ruta = None, -1.0
        self._vinetas = {}

    # Devuelve la primera zona que aun no se ha completado, o None si todas lo estan.
    @property
    def actual(self):
        for z in self.zonas:
            if z["estado"] != "completada":
                return z
        return None

    # Indica si todas las zonas ya se completaron.
    @property
    def victoria(self):
        return self.actual is None

    # Guarda las lineas del mensaje en pantalla y cuantos segundos se muestra.
    def _aviso(self, lineas, segundos=3.0):
        self.aviso, self.t_aviso = lineas, segundos

    # Determina si la barrera de la zona activa impide que el rectangulo salga de ella.
    def bloquea(self, rect):
        z = self.actual
        if z is None or not z["cerrada"] or z["estado"] not in ("preparando", "activa"):
            return False
        return not z["rect"].contains(rect)

    # Avanza el estado de la zona activa, contabiliza bajas y gestiona sus recompensas.
    def actualizar(self, dt, jugador, enemigos):
        self.t += dt
        self.t_aviso -= dt
        self.t_barrera -= dt
        z = self.actual
        if z is None or jugador.muerto:
            return
        for e in enemigos:
            if e.de_oleada and not e.vivo() and not e.contado:
                e.contado = True
                z["matados"] += 1
                base = e.puntos_base
                multiplicador = max(
                    0.3,
                    1.0 - 0.7 * z["tiempo_oleada"] / PUNTUACION_TIEMPO_MAX_REDUCCION,
                )
                puntos = round(base * multiplicador)
                self.puntuacion += puntos
                z["puntos_ganados"] += puntos
        dentro = z["rect"].collidepoint(jugador.rect.center)
        if z["estado"] == "pendiente":
            if z["rect"].inflate(-2 * OLEADA_MARGEN_ENTRADA, -2 * OLEADA_MARGEN_ENTRADA).contains(jugador.rect):
                z.update(estado="preparando", generados=0, matados=0, t_prep=OLEADA_ESPERA, t_spawn=0.0)
                if z["reja_temporal"] is not None:
                    mapa.reja_temporal = z["reja_temporal"]
                reproducir_sonido("inicio_oleada")
                self._aviso([f"OLEADA {z['nivel']} - {z['nombre']}"] + (["Zona cerrada: elimina a todos para poder salir"] if z["cerrada"] else []), 3.0)
        elif not dentro and z["cerrada"]:
            self._cancelar(z, enemigos)
        elif z["estado"] == "preparando" and dentro:
            z["t_prep"] -= dt
            if z["t_prep"] <= 0:
                z.update(estado="activa", tiempo_oleada=0.0, puntos_ganados=0)
                self._aviso([f"OLEADA {z['nivel']}!"], 2.0)
        if z["jefe"] and z["tipo_jefe"] == "orco":
            jefe_orco = next(
                (e for e in enemigos if getattr(e, "tipo_jefe", None) == "orco" and not e.vivo()),
                None,
            )
            if jefe_orco is not None:
                enemigos.lista[:] = [e for e in enemigos if e is jefe_orco]
                enemigos.proyectiles.clear()
        if z["estado"] == "activa":
            z["tiempo_oleada"] += dt
        if z["estado"] == "activa" and dentro:
            vivos = sum(1 for e in enemigos if e.de_oleada and e.vivo())
            z["t_spawn"] = max(0.0, z["t_spawn"] - dt)
            if z["generados"] < z["total"]:
                if vivos < z["max_vivos"] and z["t_spawn"] <= 0:
                    self._generar(z, jugador, enemigos)
                    z["t_spawn"] = z["intervalo"]
            elif vivos == 0:
                z["estado"] = "completada"
                reproducir_sonido("completar_oleada")
                if z["reja_temporal"] is not None:
                    mapa.reja_temporal = None
                puertas_abiertas = mapa.abrir_puertas(z["puertas"])
                if self.victoria:
                    self._aviso(["TODAS LAS OLEADAS COMPLETADAS!"], 5.0)
                else:
                    lineas = [f"OLEADA {z['nivel']} COMPLETADA!"]
                    if z["cerrada"]:
                        lineas.append("La zona se ha abierto: puedes salir")
                    if puertas_abiertas:
                        lineas.append("Las puertas de la siguiente zona se han abierto")
                    self._aviso(lineas, 4.0)
        if self.bloquea(jugador.rect.inflate(16, 16)) and not self.bloquea(jugador.rect):
            self.t_barrera = 1.2

    # Reinicia una oleada cerrada cuando el jugador abandona su zona.
    def _cancelar(self, z, enemigos):
        z.update(
            estado="pendiente", generados=0, matados=0,
            tiempo_oleada=0.0, puntos_ganados=0,
        )
        for e in enemigos:
            if e.de_oleada and e.vivo():
                e.vida = 0
                e.t_muerte = 0.0
                e.contado = True
        self._aviso(["Has salido de la zona: la oleada se detuvo", "Vuelve a entrar para empezarla de nuevo"], 4.0)

    # Crea un enemigo o jefe en una casilla válida, lejos del jugador si es posible.
    def _generar(self, z, jugador, enemigos):
        jx, jy = jugador.rect.center
        lejos = [p for p in z["puntos"] if math.hypot(p[0] - jx, p[1] - jy) >= z["dist"]]
        punto = random.choice(lejos) if lejos else max(z["puntos"], key=lambda p: math.hypot(p[0] - jx, p[1] - jy))
        if z["jefe"]:
            e = Jefe(
                punto[0], punto[1], aparicion=ENEMIGO_TIEMPO_APARICION,
                tipo=z["tipo_jefe"], sprite=z["sprite_jefe"],
                tipos_apoyo=z["tipos_apoyo"], puntos_apoyo=z["puntos"],
                max_apoyos=z["max_apoyos"],
            )
        else:
            tipo = random.choice(z["tipos_enemigos"])
            e = Enemigo(
                punto[0], punto[1], agresivo=ENEMIGOS_OLEADA_AGRESIVOS,
                aparicion=ENEMIGO_TIEMPO_APARICION, tipo=tipo,
            )
        e.de_oleada = True
        enemigos.agregar(e)
        z["generados"] += 1

    # Dibuja las bandas luminosas y el borde de las zonas cerradas.
    def dibujar_perimetro(self, superficie, cam):
        pantalla = superficie.get_rect()
        G = 44
        for z in self.zonas:
            if z["estado"] == "completada" or not z["cerrada"]:
                continue
            r = z["rect"].move(-cam[0], -cam[1])
            if not r.colliderect(pantalla):
                continue
            activa = z["estado"] in ("preparando", "activa")
            fuerza = 0.65 + 0.35 * math.sin(self.t * 4) if activa else 0.30
            r0, g0, b0 = z["color"]
            for lado in ("arriba", "abajo", "izq", "der"):
                horizontal = lado in ("arriba", "abajo")
                # Calcula donde dibujar la banda luminosa en el borde seleccionado de la zona.
                pos = (r.x, r.y if lado in ("arriba", "izq") else r.bottom - G) if horizontal else \
                      (r.x if lado == "izq" else r.right - G, r.y)
                tam = (r.w, G) if horizontal else (G, r.h)
                vis = pygame.Rect(pos, tam).clip(pantalla)
                if vis.w <= 0 or vis.h <= 0:
                    continue
                banda = pygame.Surface(vis.size, pygame.SRCALPHA)
                for k in range(G):
                    d = k if lado in ("arriba", "izq") else G - 1 - k
                    a = int(150 * fuerza * (1 - d / G) ** 1.6)
                    if horizontal:
                        fila = pos[1] + k - vis.y
                        if 0 <= fila < vis.h:
                            pygame.draw.line(banda, (r0, g0, b0, a), (0, fila), (vis.w, fila))
                    else:
                        col = pos[0] + k - vis.x
                        if 0 <= col < vis.w:
                            pygame.draw.line(banda, (r0, g0, b0, a), (col, 0), (col, vis.h))
                superficie.blit(banda, vis.topleft)
            brillo = 0.45 + 0.55 * fuerza
            pygame.draw.rect(superficie, (int(r0 * brillo), int(g0 * brillo), int(b0 * brillo)), r, 4)

    # Genera y guarda en cache el efecto de color de borde de una zona.
    def _vineta(self, color):
        if color not in self._vinetas:
            pequena = pygame.Surface((48, 27), pygame.SRCALPHA)
            for y in range(27):
                for x in range(48):
                    d = math.hypot((x - 23.5) / 23.5, (y - 13) / 13) / 1.414
                    pequena.set_at((x, y), (*color, int(95 * min(1.0, max(0.0, (d - 0.45) / 0.55)) ** 2)))
            self._vinetas[color] = pygame.transform.smoothscale(pequena, (width, height))
        return self._vinetas[color]

    # Aplica el color ambiental de la zona activa mientras el jugador esta dentro.
    def dibujar_vineta(self, superficie, jugador):
        z = self.actual
        if z is not None and z["estado"] in ("preparando", "activa") and z["rect"].collidepoint(jugador.rect.center):
            superficie.blit(self._vineta(z["color"]), (0, 0))

    # Calcula la direccion y la distancia hacia la siguiente zona, rodeando obstaculos.
    def direccion_flecha(self, jugador):
        z = self.actual
        if z is None or jugador.muerto or z["rect"].collidepoint(jugador.rect.center):
            return None
        origen = pygame.Vector2(jugador.rect.center)
        destino = pygame.Vector2(z["destino"])
        objetivo = destino
        if not mapa.paso_libre(origen, destino, jugador.rect.w, jugador.rect.h):
            if self.t >= self.t_ruta:
                self.t_ruta = self.t + 0.4
                self.objetivo_flecha = None
                for p in mapa.camino(origen, destino):
                    if not mapa.paso_libre(origen, p, jugador.rect.w, jugador.rect.h):
                        break
                    self.objetivo_flecha = pygame.Vector2(p)
            if self.objetivo_flecha is not None:
                objetivo = self.objetivo_flecha
        d = objetivo - origen
        if d.length() < 1:
            d = destino - origen if (destino - origen).length() >= 1 else pygame.Vector2(1, 0)
        return d.normalize(), (destino - origen).length() / TAM_TILE

    # Dibuja la flecha guia hacia la siguiente zona con su nombre y distancia.
    def dibujar_flecha(self, superficie, jugador, cam):
        guia = self.direccion_flecha(jugador)
        if guia is None:
            return
        direccion, distancia = guia
        z = self.actual
        centro = pygame.Vector2(jugador.rect.centerx - cam[0], jugador.rect.bottom - 90 - cam[1])
        pivote = centro + direccion * (170 + 6 * math.sin(self.t * 6))
        pivote.x = max(220, min(width - 220, pivote.x))
        pivote.y = max(290, min(height - 230, pivote.y))
        perp = pygame.Vector2(-direccion.y, direccion.x)
        puntos = [pivote + direccion * 34, pivote - direccion * 14 + perp * 24, pivote - direccion * 2, pivote - direccion * 14 - perp * 24]
        pygame.draw.polygon(superficie, (0, 0, 0), puntos, 6)
        pygame.draw.polygon(superficie, z["color"], puntos)
        texto_borde(superficie, f"{z['nombre']} - {int(distancia)} casillas", fuente_peq, z["color"], (pivote.x, pivote.y + 44))

    # Muestra el progreso de la oleada, los enemigos restantes y los avisos.
    def dibujar_hud(self, superficie):
        z = self.actual
        if z is None:
            lineas = ["Campana completada: el Carcelero ha sido derrotado"]
        else:
            lineas = [f"OLEADA {z['nivel']}/{len(self.zonas)} - {z['nombre']}"]
            if z["estado"] == "pendiente":
                lineas.append("Entra en la zona (sigue la flecha)")
            elif z["estado"] == "preparando":
                lineas.append(f"Comienza en {max(1, math.ceil(z['t_prep']))}...")
            else:
                restantes = z["total"] - z["matados"]
                objetivo = "Jefe restante" if z["jefe"] else "Enemigos restantes"
                lineas.append(f"{objetivo}: {restantes}" + ("   (zona cerrada)" if z["cerrada"] else ""))
        for i, linea in enumerate(lineas):
            texto_borde(superficie, linea, fuente_peq, blanco, (20, 108 + i * 28), centrado=False)
        if self.t_aviso > 0:
            color = z["color"] if z is not None else amarillo
            for i, linea in enumerate(self.aviso):
                texto_borde(superficie, linea, menu_font if i == 0 else fuente_peq, color if i == 0 else blanco, (width // 2, 190 + i * 50))
        if self.t_barrera > 0:
            texto_borde(superficie, "No puedes salir hasta terminar la oleada", menu_font, (255, 120, 90), (width // 2, height - 190))


# Velocidad (fps) y si se repite cada animacion del jugador.
print("---------- CONFIGURACION DE ANIMACIONES DEL JUGADOR ----------")
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


# Personaje controlado por el jugador: movimiento, combate, vida, mejoras y animacion.
print("---------- CLASE DEL JUGADOR ----------")
class Jugador:
    # Mantiene posición, hitboxes, animación, vida, inventario y poderes del personaje.
    def __init__(self, x, y):
        self.pos = pygame.Vector2(x, y)
        self.rect = pygame.Rect(0, 0, int(HITBOX_JUGADOR_PIES[0] * escala_jugador), int(HITBOX_JUGADOR_PIES[1] * escala_jugador))
        self.rect.center = self.pos

        self.vel_caminar = VEL_JUGADOR_CAMINAR
        self.vel_correr = VEL_JUGADOR_CORRER
        self.vel_agachado = VEL_JUGADOR_AGACHADO
        self.vel_rodar = VEL_JUGADOR_RODAR
        self.vel_aire = VEL_JUGADOR_CAMINAR

        self.anim = "quieto"
        self.indice_frame = 0.0
        self.reversa = False
        self.anim_terminada = False
        self.mirando = 1
        self.imagen = ANIMACIONES["quieto"]["der"][0]
        self.alto_cuerpo = self.imagen.get_bounding_rect().height

        self.accion = None
        self.agachado = False
        self.muerto = False
        self.z = 0.0
        self.vz = 0.0
        self.en_aire = False
        self.dir_accion = pygame.Vector2(1, 0)
        self.empuje = pygame.Vector2(0, 0)
        self.combo = 0
        self.t_combo = 0.0
        self.tiempo_espada = 0.0
        self.cd_giro = 0.0
        self.vida_max = VIDA_JUGADOR
        self.vida = self.vida_max
        self.vida_visible = float(self.vida_max)
        self.pociones = 0
        self.invulnerable = 0.0
        self.golpeados = set()
        self.celebrar_pendiente = False
        self.victoria_hecha = False
        self.prev = {}
        self.enfriamiento = 0.3
        self.bonificaciones = {"viento": 0, "dano": 0, "berserker": 0}
        self.ataques_lanzados = 0
        self.ataque_id = 0
        self.tajo_viento_pendiente = False
        self.berserker_tiempo = 0.0
        self.berserker_enfriamiento = 0.0

    # Indica si el poder berserker esta activo.
    @property
    def berserker_activo(self):
        return self.berserker_tiempo > 0

    # Multiplicador de dano por las mejoras de dano y berserker.
    @property
    def multiplicador_dano(self):
        return (1 + self.bonificaciones["dano"] * 0.15) * (1.0 + 0.2 * self.bonificaciones["berserker"] if self.berserker_activo else 1.0)

    # Multiplicador de velocidad mientras el berserker esta activo.
    @property
    def multiplicador_velocidad(self):
        return 1.0 + 0.12 * self.bonificaciones["berserker"] if self.berserker_activo else 1.0

    # Reduccion del dano recibido mientras el berserker esta activo.
    @property
    def multiplicador_dano_recibido(self):
        return max(0.55, 1.0 - 0.12 * self.bonificaciones["berserker"]) if self.berserker_activo else 1.0

    # Cuenta golpes y activa el proyectil de viento con la frecuencia de la mejora.
    def registrar_ataque(self):
        nivel = self.bonificaciones["viento"]
        if nivel == 0:
            return False
        self.ataques_lanzados += 1
        cada_cuantos = max(1, 4 - nivel)
        if self.ataques_lanzados >= cada_cuantos:
            self.ataques_lanzados = 0
            self.tajo_viento_pendiente = True
            return True
        return False

    # Activa temporalmente el poder berserker si está mejorado y no está en enfriamiento.
    def activar_berserker(self):
        nivel = self.bonificaciones["berserker"]
        if nivel and self.berserker_enfriamiento <= 0 and not self.berserker_activo:
            self.berserker_tiempo = 5.0 + 2.0 * nivel
            self.berserker_enfriamiento = 20.0 - 2.0 * nivel
            reproducir_sonido("activar_berserker")
            return True
        return False

    # Consume una poción y recupera hasta 30 puntos sin exceder la vida máxima.
    def beber_pocion(self):
        if self.pociones <= 0 or self.vida >= self.vida_max or self.muerto:
            return False
        self.pociones -= 1
        self.vida = min(self.vida_max, self.vida + 30)
        self.vida_visible = max(self.vida_visible, float(self.vida))
        return True

    # Cambia la animación y configura su dirección de reproducción y fotograma inicial.
    def poner_anim(self, nombre, reversa=False, reiniciar=False):
        if reiniciar or nombre != self.anim or reversa != self.reversa:
            self.anim = nombre
            self.reversa = reversa
            self.anim_terminada = False
            n = len(ANIMACIONES[nombre]["der"])
            self.indice_frame = n - 0.001 if reversa else 0.0

    # Avanza el fotograma de la animacion segun el tiempo, repitiendo o terminando.
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
                    self.indice_frame = n - 0.001
                    self.anim_terminada = True

    # Devuelve cuanto ha avanzado la animacion actual (de 0 a 1).
    def progreso(self):
        n = len(ANIMACIONES[self.anim]["der"])
        p = self.indice_frame / n
        return 1 - p if self.reversa else p

    # Selecciona el fotograma y la orientacion que se dibujan.
    def elegir_imagen(self):
        frames = ANIMACIONES[self.anim]["der" if self.mirando == 1 else "izq"]
        self.imagen = frames[min(int(self.indice_frame), len(frames) - 1)]

    # Inicia una accion: reproduce su sonido, prepara su ataque y arranca su animacion.
    def empezar(self, nombre, lado=None):
        self.accion = nombre
        sonidos_accion = {
            "rodar": "rodar",
            "atacar": "ataque_espada",
            "atacar2": "ataque_espada",
            "atacar_dash": "ataque_embestida",
            "atacar_abajo": "ataque_aereo",
            "atacar_giro": "ataque_giro",
            "agachado_atacar": "ataque_espada",
            "herido": "dano_jugador",
            "morir": "derrota_jugador",
            "victoria": "victoria",
            "beber": "curacion_pocion",
        }
        sonido = sonidos_accion.get(nombre)
        if sonido:
            reproducir_sonido(
                sonido,
                reemplazar=SONIDOS_ATAQUE if nombre in HITBOX_ATAQUES else (),
            )
        if nombre in HITBOX_ATAQUES:
            self.ataque_id += 1
            self.golpeados = set()
            self.registrar_ataque()
        if lado is not None:
            self.mirando = lado
        if nombre == "levantarse":
            self.poner_anim("agacharse", reversa=True, reiniciar=True)
        else:
            self.poner_anim(nombre, reiniciar=True)

    # Aplica defensas, muestra el daño y decide si el jugador es herido o derrotado.
    def recibir_dano(self, cantidad=10, origen=None):
        if self.muerto or self.accion == "rodar" or self.invulnerable > 0:
            return False
        dano_final = max(1, round(cantidad * self.multiplicador_dano_recibido))
        self.vida = max(0, self.vida - dano_final)
        texto_dano(dano_final, self.rect.centerx, self.rect.bottom - self.alto_cuerpo - self.z, (255, 70, 70))
        self.invulnerable = INVULNERABLE_TRAS_GOLPE
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

    # Marca la derrota, reproduce los sonidos y prepara la animacion final.
    def morir(self):
        self.muerto = True
        reproducir_sonido("derrota_jugador")
        reproducir_sonido("perder_partida")
        self.accion = None
        self.agachado = False
        self.z, self.vz, self.en_aire = 0.0, 0.0, False
        self.poner_anim("morir", reiniciar=True)

    # Programa la animacion de victoria una sola vez.
    def celebrar(self):
        if not self.victoria_hecha and not self.muerto:
            self.victoria_hecha = True
            self.celebrar_pendiente = True

    # Calcula la hitbox corporal segun la postura (de pie o agachado).
    def cuerpo(self):
        ancho, alto = HITBOX_JUGADOR_CUERPO_AGACHADO if self.agachado else HITBOX_JUGADOR_CUERPO
        zona = pygame.Rect(0, 0, int(ancho * escala_jugador), int(alto * escala_jugador))
        zona.midbottom = (self.rect.centerx, self.rect.bottom - self.z)
        return zona

    # Calcula la zona activa de impacto del ataque actual, solo en los fotogramas de golpe.
    def hitbox(self):
        if self.accion not in HITBOX_ATAQUES:
            return None
        n = len(ANIMACIONES[self.anim]["der"])
        if not 1 <= int(self.indice_frame) <= n - 2:
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

    # Detecta las teclas y botones recien pulsados comparando con el fotograma anterior.
    def pulsaciones(self, teclas, raton):
        ahora = {
            "saltar": teclas[pygame.K_SPACE],
            "rodar": teclas[pygame.K_r] or raton[2],
            "giro": teclas[pygame.K_e],
            "beber": teclas[pygame.K_q],
            "berserker": teclas[pygame.K_v],
        }
        nuevas = {k: bool(v) and not self.prev.get(k, False) for k, v in ahora.items()}
        self.prev = {k: bool(v) for k, v in ahora.items()}
        return nuevas

    # Traduce entradas recientes y estado físico en saltos, ataques, esquivas o poses.
    def decidir_accion(self, nuevas, ataca, mueve, corre, direccion, lado_raton, quiere_agachar):
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
            self.vz = FUERZA_SALTO
            self.z = 1.0
            self.vel_aire = self.vel_correr if corre else self.vel_caminar
            reproducir_sonido("salto")
            self.poner_anim("saltar", reiniciar=True)
        elif nuevas["rodar"]:
            self.iniciar_rodar(direccion)
        elif nuevas["giro"] and self.cd_giro <= 0:
            self.cd_giro = ENFRIAMIENTO_GIRO
            self.empezar("atacar_giro", lado_raton)
        elif nuevas["beber"]:
            if self.beber_pocion():
                self.empezar("beber")
        elif self.celebrar_pendiente and not mueve and not ataca:
            self.celebrar_pendiente = False
            self.empezar("victoria")
        elif ataca:
            if corre:
                centro = pygame.Vector2(self.rect.centerx, self.rect.bottom - 40)
                objetivo = pos_raton_mundo() - centro
                self.dir_accion = objetivo.normalize() if objetivo.length() > 0 else pygame.Vector2(lado_raton, 0)
                self.empezar("atacar_dash", lado_raton)
            else:
                if self.t_combo <= 0:
                    self.combo = 0
                self.empezar(("atacar", "atacar2")[self.combo], lado_raton)
                self.combo = 1 - self.combo
        elif quiere_agachar:
            self.empezar("agacharse")

    # Prepara la direccion y la animacion de la rodada.
    def iniciar_rodar(self, direccion):
        self.dir_accion = pygame.Vector2(direccion) if direccion.length() > 0 else pygame.Vector2(self.mirando, 0)
        lado = self.mirando
        if self.dir_accion.x != 0:
            lado = 1 if self.dir_accion.x > 0 else -1
        self.empezar("rodar", lado)

    # Mueve al jugador eje por eje sin atravesar obstaculos.
    def _mover_chocando(self, paso):
        atascado = mapa_choca(self.rect)
        for eje in (0, 1):
            d = paso[eje]
            if d == 0:
                continue
            self.pos[eje] += d
            self.rect.center = self.pos
            if not atascado and mapa_choca(self.rect):
                self.pos[eje] -= d
                signo = 1 if d > 0 else -1
                for _ in range(int(abs(d))):
                    self.pos[eje] += signo
                    self.rect.center = self.pos
                    if mapa_choca(self.rect):
                        self.pos[eje] -= signo
                        break
        self.rect.center = self.pos

    # Avanza lógica, desplazamiento, salto, invulnerabilidad, audio y animación del jugador.
    def actualizar(self, teclas, dt):
        self.enfriamiento -= dt
        self.cd_giro -= dt
        self.t_combo -= dt
        self.tiempo_espada -= dt
        self.invulnerable -= dt
        self.berserker_tiempo = max(0.0, self.berserker_tiempo - dt)
        self.berserker_enfriamiento = max(0.0, self.berserker_enfriamiento - dt)
        if self.vida_visible > self.vida:
            self.vida_visible = max(self.vida, self.vida_visible - 40 * dt)
        else:
            self.vida_visible = self.vida
        raton = pygame.mouse.get_pressed()
        nuevas = self.pulsaciones(teclas, raton)

        if self.muerto:
            audio_acciones.detener("pasos_caminar", "pasos_correr")
            self.poner_anim("morir")
            self.avanzar_anim(dt)
            self.elegir_imagen()
            return

        dx = (teclas[pygame.K_d] or teclas[pygame.K_RIGHT]) - (teclas[pygame.K_a] or teclas[pygame.K_LEFT])
        dy = (teclas[pygame.K_s] or teclas[pygame.K_DOWN]) - (teclas[pygame.K_w] or teclas[pygame.K_UP])
        direccion = pygame.Vector2(dx, dy)
        mueve = direccion.length() > 0
        if mueve:
            direccion = direccion.normalize()
        corre = mueve and (teclas[pygame.K_LSHIFT] or teclas[pygame.K_RSHIFT])
        quiere_agachar = teclas[pygame.K_c] or teclas[pygame.K_LCTRL]
        lado_raton = -1 if pos_raton_mundo().x < self.rect.centerx else 1
        ataca = raton[0] and self.enfriamiento <= 0

        if self.accion == "victoria" and (mueve or ataca or any(nuevas.values())):
            self.accion = None
        if nuevas["berserker"]:
            self.activar_berserker()
        if self.accion is None:
            self.decidir_accion(nuevas, ataca, mueve, corre, direccion, lado_raton, quiere_agachar)

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
        self._mover_chocando(mov * self.multiplicador_velocidad * dt)
        area = pygame.Rect(0, self.alto_cuerpo - self.rect.h, MUNDO_ANCHO, MUNDO_ALTO - self.alto_cuerpo + self.rect.h)
        self.rect.clamp_ip(area)
        self.pos.update(self.rect.center)
        toca_izq = self.rect.left <= 0 and direccion.x < 0
        toca_der = self.rect.right >= MUNDO_ANCHO and direccion.x > 0
        contra_pared = toca_izq or toca_der

        if self.en_aire:
            g = GRAVEDAD_GOLPE_ABAJO if self.accion == "atacar_abajo" else GRAVEDAD
            self.vz -= g * dt
            self.z += self.vz * dt
            if self.z <= 0:
                self.z, self.vz, self.en_aire = 0.0, 0.0, False
                if self.accion is None:
                    reproducir_sonido("aterrizaje")
                    self.empezar("aterrizar")

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
                self.mirando = lado_raton
                self.poner_anim("caminar")
            else:
                self.mirando = lado_raton
                self.poner_anim("quieto_espada" if self.tiempo_espada > 0 else "quieto")

        if self.anim in ("caminar", "correr") and mueve:
            sonido_pasos = "pasos_correr" if self.anim == "correr" else "pasos_caminar"
            otro_sonido_pasos = "pasos_caminar" if sonido_pasos == "pasos_correr" else "pasos_correr"
            audio_acciones.reproducir_bucle(
                sonido_pasos,
                ajustes["efectos"],
                reemplazar=(otro_sonido_pasos,),
            )
        else:
            audio_acciones.detener("pasos_caminar", "pasos_correr")

        self.avanzar_anim(dt)

        if self.accion is not None and self.anim_terminada:
            terminada = self.accion
            self.accion = None
            if terminada == "agacharse":
                self.agachado = True
            elif terminada == "levantarse":
                self.agachado = False
            elif terminada in HITBOX_ATAQUES:
                self.enfriamiento = ENFRIAMIENTO_ATAQUE / self.multiplicador_velocidad
                self.t_combo = TIEMPO_COMBO
                self.tiempo_espada = TIEMPO_ESPADA_EN_MANO

        self.elegir_imagen()

    # Dibuja la sombra, el sprite (con parpadeo al ser golpeado) y el aura del berserker.
    def dibujar(self, superficie, cam=(0, 0)):
        factor = max(0.4, 1 - self.z / 400)
        sombra = pygame.Surface((max(1, int(30 * escala_jugador * factor)), max(1, int(9 * escala_jugador * factor))), pygame.SRCALPHA)
        pygame.draw.ellipse(sombra, (0, 0, 0, 90), sombra.get_rect())
        superficie.blit(sombra, sombra.get_rect(center=(self.rect.centerx - cam[0], self.rect.bottom - 2 - cam[1])))
        imagen = self.imagen
        if self.invulnerable > 0 and not self.muerto and self.accion != "rodar":
            if int(self.invulnerable * 16) % 2 == 0:
                imagen = con_transparencia(imagen, 110)
        imagen_rect = imagen.get_rect(
            midbottom=(self.rect.centerx - cam[0], self.rect.bottom - self.z - cam[1])
        )
        if self.berserker_activo:
            aura_rect = imagen_rect.inflate(imagen_rect.width // 2, imagen_rect.height // 4)
            aura = pygame.Surface(aura_rect.size, pygame.SRCALPHA)
            pulso = 0.5 + 0.5 * math.sin(pygame.time.get_ticks() * 0.009)
            pygame.draw.ellipse(
                aura, (255, 55, 15, 28 + int(pulso * 18)), aura.get_rect().inflate(-2, -2)
            )
            pygame.draw.ellipse(
                aura, (255, 105, 25, 105 + int(pulso * 45)),
                aura.get_rect().inflate(-8, -8), max(2, int(3 + pulso * 2)),
            )
            pygame.draw.ellipse(
                aura, (255, 220, 105, 145 + int(pulso * 55)),
                aura.get_rect().inflate(-16, -14), 2,
            )
            centro = aura.get_rect().center
            for i in range(6):
                angulo = pygame.time.get_ticks() * 0.002 + i * math.tau / 6
                x = centro[0] + int(math.cos(angulo) * aura_rect.width * 0.38)
                y = centro[1] + int(math.sin(angulo) * aura_rect.height * 0.38)
                radio = 2 + int((0.5 + 0.5 * math.sin(angulo * 2)) * 2)
                pygame.draw.circle(aura, (255, 190, 70, 190), (x, y), radio)
            superficie.blit(aura, aura_rect.topleft)
        superficie.blit(imagen, imagen_rect)


# Cada perfil agrupa sprite, atributos de combate y apariencia del proyectil si aplica.
ENEMIGO_GOBLIN = {
    "sprite": "goblin",
    "vida": 60,
    "dano": 12,
    "velocidad": 190,
    "puntos": 100,
    "ataque": "cuerpo_a_cuerpo",
    "alcance": 95,
    "enfriamiento": 0.8,
    "escala": 1.0,
}
ENEMIGO_DISTANCIA = {
    "sprite": "goblin_mago",
    "vida": 48,
    "dano": 10,
    "velocidad": 155,
    "puntos": 120,
    "ataque": "distancia",
    "alcance": 440,
    "enfriamiento": 1.8,
    "escala": 1.0,
    "proyectil_color": (200, 45, 35),
    "proyectil_brillo": (255, 190, 75),
    "proyectil_tamano": (34, 24),
    "proyectil_radio": (8, 4),
    "proyectil_sprite": "proyectil_mago.png",
    "proyectil_visual": (84, 80),
}
ENEMIGO_BRUJA = {
    "sprite": "bruja",
    "vida": 75,
    "dano": 20,
    "velocidad": 165,
    "puntos": 160,
    "ataque": "distancia",
    "alcance": 520,
    "enfriamiento": 1.55,
    "escala": 1.45,
    "proyectil_color": (150, 65, 225),
    "proyectil_brillo": (220, 170, 255),
    "proyectil_tamano": (48, 36),
    "proyectil_radio": (12, 6),
    "proyectil_sprite": "proyectil_mago.png",
    "proyectil_visual": (94, 90),
}
ENEMIGO_NIVEL_2 = {
    "sprite": "trol",
    "vida": 105,
    "dano": 30,
    "velocidad": 220,
    "puntos": 190,
    "ataque": "cuerpo_a_cuerpo",
    "alcance": 120,
    "enfriamiento": 0.7,
    "escala": 1.45,
}
ENEMIGO_DISTANCIA_NIVEL_2 = {
    "sprite": "lich",
    "vida": 95,
    "dano": 30,
    "velocidad": 180,
    "puntos": 220,
    "ataque": "distancia",
    "alcance": 600,
    "enfriamiento": 1.25,
    "escala": 1.45,
    "proyectil_color": (40, 115, 255),
    "proyectil_brillo": (135, 220, 255),
    "proyectil_tamano": (58, 42),
    "proyectil_radio": (15, 8),
    "proyectil_sprite": "proyectil_lich.png",
    "proyectil_visual": (110, 106),
}
ENEMIGO_ESPECTRO = {
    "sprite": "espectro",
    "vida": 145,
    "dano": 40,
    "velocidad": 205,
    "puntos": 250,
    "ataque": "cuerpo_a_cuerpo",
    "alcance": 145,
    "enfriamiento": 0.9,
    "escala": 1.6,
}

# La bruja y el trol aparecen en oleadas 3-4; lich y espectro los sustituyen desde la 5.
# Las zonas usan estas claves para escoger un perfil compatible de enemigo.
ARQUETIPOS_ENEMIGO = {
    "goblin": ENEMIGO_GOBLIN,
    "mago": ENEMIGO_DISTANCIA,
    "bruja": ENEMIGO_BRUJA,
    "trol": ENEMIGO_NIVEL_2,
    "lich": ENEMIGO_DISTANCIA_NIVEL_2,
    "espectro": ENEMIGO_ESPECTRO,
}


# Enemigos comunes con IA compartida y jefes con patrones de ataque propios.
print("---------- CLASES DE ENEMIGOS Y JEFES ----------")
class Enemigo:
    # Implementa perfiles de arquetipo con IA compartida, combate cuerpo a cuerpo o a distancia.
    def __init__(self, x, y, agresivo=False, aparicion=0.0, tipo="goblin", perfil=None):
        perfil = ARQUETIPOS_ENEMIGO.get(tipo) if perfil is None else perfil
        if perfil is None:
            raise ValueError(f"Arquetipo de enemigo desconocido: {tipo}")
        self.escala = escala_enemigos * perfil.get("escala", 1.0)
        self.rect = pygame.Rect(0, 0, int(HITBOX_ENEMIGO_PIES[0] * self.escala), int(HITBOX_ENEMIGO_PIES[1] * self.escala))
        self.rect.midbottom = (x, y)
        self.pos = pygame.Vector2(self.rect.midbottom)
        self.casa = pygame.Vector2(self.rect.midbottom)
        self.dano = perfil["dano"]
        self.vida_max = perfil["vida"]
        self.vida = self.vida_max
        self.puntos_base = perfil["puntos"]
        self.tipo = tipo
        self.perfil = perfil
        self.alcance_ataque = perfil["alcance"]
        self.intervalo_ataque = perfil["enfriamiento"]
        self.tipo_ataque = perfil["ataque"]
        nombre_sprite = perfil["sprite"]
        if Enemigo._imagenes is None:
            Enemigo._imagenes = {}
        clave_imagen = (nombre_sprite, self.escala)
        if clave_imagen not in Enemigo._imagenes:
            base = escalar_imagen(cargar_sprite_enemigo(nombre_sprite), self.escala)
            alerta = base.copy()
            alerta.fill((150, 0, 0, 0), special_flags=pygame.BLEND_RGB_ADD)
            destello = base.copy()
            destello.fill((170, 170, 170, 0), special_flags=pygame.BLEND_RGB_ADD)
            imagenes = {}
            for nombre, img in (("normal", base), ("alerta", alerta), ("destello", destello)):
                volteada = pygame.transform.flip(img, True, False)
                der, izq = (img, volteada) if ENEMIGO_MIRA_A_LA_DERECHA else (volteada, img)
                imagenes[(nombre, 1)] = der
                imagenes[(nombre, -1)] = izq
            Enemigo._imagenes[clave_imagen] = (imagenes, base.get_height())
        self.imagenes, self.alto_img = Enemigo._imagenes[clave_imagen]
        self.estado = "perseguir" if agresivo else "vagar"
        self.mirando = random.choice((-1, 1))
        self.t_vagar = random.uniform(0.2, 1.2)
        self.dir_vagar = pygame.Vector2(0, 0)
        self.ataque = None
        self.t_cd = random.uniform(0.0, 0.5)
        self.ruta = []
        self.t_ruta = 0.0
        self.retroceso = pygame.Vector2(0, 0)
        self.t_retroceso = 0.0
        self.t_muerte = None
        self.eliminado = False
        self.agresivo = agresivo
        self.t_aparicion = aparicion
        self.aparicion_total = aparicion
        self.de_oleada = False
        self.contado = False

    # Indica si el enemigo conserva vida.
    def vivo(self):
        return self.vida > 0

    # Calcula la hitbox corporal del enemigo.
    def cuerpo(self):
        zona = pygame.Rect(0, 0, int(HITBOX_ENEMIGO_CUERPO[0] * self.escala), int(HITBOX_ENEMIGO_CUERPO[1] * self.escala))
        zona.midbottom = self.rect.midbottom
        return zona

    # Calcula la zona de ataque cuerpo a cuerpo segun el lado al que mira.
    def zona_ataque(self, lado):
        ancho, alto = HITBOX_ENEMIGO_ATAQUE
        separacion, altura = HITBOX_ENEMIGO_ATAQUE_POS
        zona = pygame.Rect(0, 0, int(ancho * self.escala), int(alto * self.escala))
        y = self.rect.bottom - altura * self.escala
        if lado == 1:
            zona.midleft = (self.rect.centerx + separacion * self.escala, y)
        else:
            zona.midright = (self.rect.centerx - separacion * self.escala, y)
        return zona

    # Reduce la vida, muestra el impacto y aplica retroceso o estado de muerte.
    def recibir_dano(self, cantidad, origen):
        if not self.vivo() or self.t_retroceso > 0 or self.t_aparicion > 0:
            return False
        self.vida = max(0, self.vida - cantidad)
        texto_dano(cantidad, self.rect.centerx, self.rect.bottom - self.alto_img, (255, 230, 80))
        alejar = pygame.Vector2(self.rect.center) - pygame.Vector2(origen)
        if alejar.length() == 0:
            alejar = pygame.Vector2(1, 0)
        self.t_retroceso = TIEMPO_RETROCESO
        self.retroceso = alejar.normalize() * (2 * RETROCESO_ENEMIGO / TIEMPO_RETROCESO)
        self.ataque = None
        self.estado = "perseguir"
        if self.vida <= 0:
            self.t_muerte = 0.0
            reproducir_sonido("derrota_enemigo")
        else:
            reproducir_sonido("golpe_enemigo")
        return True

    # Rectangulo del mundo dentro del que puede moverse el enemigo.
    def _area(self):
        return pygame.Rect(0, self.alto_img - self.rect.h, MUNDO_ANCHO, MUNDO_ALTO - self.alto_img + self.rect.h)

    # Mueve al enemigo eje por eje respetando el mapa y los otros obstaculos.
    def _mover(self, direccion, vel, dt, obstaculos):
        antes = pygame.Vector2(self.pos)
        paso = direccion * vel * dt
        atascado = self.rect.collidelist(obstaculos) != -1 or mapa_choca(self.rect)
        for eje in (0, 1):
            self.pos[eje] += paso[eje]
            self.rect.midbottom = self.pos
            if not atascado and (self.rect.collidelist(obstaculos) != -1 or mapa_choca(self.rect)):
                self.pos[eje] -= paso[eje]
        self.rect.midbottom = self.pos
        antes_rect = self.rect.copy()
        self.rect.clamp_ip(self._area())
        if self.rect != antes_rect:
            self.pos.update(self.rect.midbottom)
        return (self.pos - antes).length() > 0.01

    # Aplica el retroceso tras recibir un golpe.
    def _retroceder(self, dt):
        paso = self.retroceso * (self.t_retroceso / TIEMPO_RETROCESO) * dt
        for eje in (0, 1):
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

    # Comportamiento de patrulla aleatoria cuando no persigue al jugador.
    def _vagar(self, dt, obstaculos):
        self.t_vagar -= dt
        if self.t_vagar <= 0:
            if self.dir_vagar.length() > 0:
                self.dir_vagar = pygame.Vector2(0, 0)
                self.t_vagar = random.uniform(0.6, 1.8)
            else:
                angulo = random.uniform(0, 2 * math.pi)
                lejos = self.casa - pygame.Vector2(self.rect.midbottom)
                if lejos.length() > RADIO_VAGAR:
                    angulo = math.atan2(lejos.y, lejos.x) + random.uniform(-0.8, 0.8)
                self.dir_vagar = pygame.Vector2(math.cos(angulo), math.sin(angulo))
                self.t_vagar = random.uniform(0.6, 1.6)
        if self.dir_vagar.length() > 0:
            if abs(self.dir_vagar.x) > 0.25:
                self.mirando = 1 if self.dir_vagar.x > 0 else -1
            if not self._mover(self.dir_vagar, VEL_ENEMIGO_VAGAR, dt, obstaculos):
                self.t_vagar = 0

    # Persigue al objetivo, elige alcance de ataque y calcula rutas cuando hay obstáculos.
    def _perseguir(self, dt, jugador, obstaculos, proyectiles):
        yo = pygame.Vector2(self.rect.center)
        el = pygame.Vector2(jugador.rect.center)
        dx = el.x - yo.x
        if abs(dx) > ENEMIGO_UMBRAL_GIRO:
            self.mirando = 1 if dx > 0 else -1
        distancia = (el - yo).length()
        if self.tipo_ataque == "distancia":
            en_rango = distancia <= self.alcance_ataque
            if self.t_cd <= 0 and en_rango and (mapa is None or mapa.hay_vista(self.rect.center, jugador.rect.center)):
                direccion = el - yo
                direccion = direccion.normalize() if direccion.length() else pygame.Vector2(self.mirando, 0)
                if abs(direccion.x) > 0.2:
                    self.mirando = 1 if direccion.x > 0 else -1
                self.ataque = {"fase": "preparar", "t": 0.0, "golpeo": False,
                               "lado": self.mirando, "tipo": "distancia",
                               "direccion": direccion, "origen": tuple(self.rect.center)}
                return
            if en_rango and distancia > self.alcance_ataque * 0.62:
                return
        elif self.t_cd <= 0 and self.zona_ataque(self.mirando).colliderect(jugador.cuerpo()):
            self.ataque = {"fase": "preparar", "t": 0.0, "golpeo": False, "lado": self.mirando,
                           "tipo": "cuerpo_a_cuerpo"}
            return
        destino = el
        if mapa is not None and not mapa.paso_libre(self.rect.center, jugador.rect.center, self.rect.w, self.rect.h):
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
            self._mover((destino - yo).normalize(), self.perfil["velocidad"], dt, obstaculos)

    # Completa el aviso, disparo/impacto y recuperación de ataques del arquetipo.
    def _atacar(self, dt, jugador, proyectiles):
        a = self.ataque
        a["t"] += dt
        if a["fase"] == "preparar":
            if a["t"] >= ENEMIGO_PREPARAR:
                a["fase"], a["t"] = "golpe", 0.0
                reproducir_sonido(
                    "ataque_enemigo_distancia"
                    if a["tipo"] == "distancia" else "ataque_enemigo_cuerpo",
                    reemplazar=SONIDOS_ATAQUE,
                )
        elif a["fase"] == "golpe":
            if not a["golpeo"] and not jugador.muerto:
                if a["tipo"] == "distancia":
                    proyectiles.append(EnemigoProyectil(self, a))
                    a["golpeo"] = True
                elif self.zona_ataque(a["lado"]).colliderect(jugador.cuerpo()):
                    a["golpeo"] = True
                    jugador.recibir_dano(self.dano, self.rect.center)
            if a["t"] >= ENEMIGO_GOLPE:
                a["fase"], a["t"] = "recuperar", 0.0
        elif a["t"] >= ENEMIGO_RECUPERAR:
            self.ataque = None
            self.t_cd = self.intervalo_ataque

    # Actualiza aparición, retroceso, muerte y comportamiento de persecución o patrulla.
    def actualizar(self, dt, jugador, otros, proyectiles=None):
        proyectiles = [] if proyectiles is None else proyectiles
        self.t_cd -= dt
        if self.t_aparicion > 0:
            self.t_aparicion -= dt
            return
        if self.t_retroceso > 0:
            self._retroceder(dt)
        if self.t_muerte is not None:
            self.t_muerte += dt
            if self.t_muerte >= 0.6:
                self.eliminado = True
            return
        if self.t_retroceso > 0:
            return
        if self.ataque is not None:
            self._atacar(dt, jugador, proyectiles)
            return
        yo = pygame.Vector2(self.rect.center)
        distancia = (pygame.Vector2(jugador.rect.center) - yo).length()
        if self.estado == "vagar":
            if (distancia < RADIO_DETECCION and not jugador.muerto and
                    (distancia < RADIO_DETECCION / 2 or mapa is None or mapa.hay_vista(self.rect.center, jugador.rect.center))):
                self.estado = "perseguir"
        elif (distancia > RADIO_PERDER and not self.agresivo) or jugador.muerto:
            self.estado = "vagar"
            self.t_vagar, self.dir_vagar = 0.0, pygame.Vector2(0, 0)
        obstaculos = [jugador.rect] + [o.rect for o in otros if o is not self and o.vivo()]
        if self.estado == "perseguir":
            self._perseguir(dt, jugador, obstaculos, proyectiles)
        else:
            self._vagar(dt, obstaculos)

    # Desplazamiento visual del sprite durante las fases del ataque.
    def _desplazamiento(self):
        a = self.ataque
        if a is None:
            return 0
        if a["fase"] == "preparar":
            return -a["lado"] * 3 * self.escala * (a["t"] / ENEMIGO_PREPARAR)
        if a["fase"] == "golpe":
            return a["lado"] * 5 * self.escala
        return a["lado"] * 5 * self.escala * (1 - a["t"] / ENEMIGO_RECUPERAR)

    # Dibuja sombra, sprite con sus efectos (alerta, destello, desvanecido), aviso de disparo y barra de vida.
    def dibujar(self, superficie, cam=(0, 0)):
        sombra = pygame.Surface((int(self.rect.w * 1.5), int(self.rect.h * 1.1)), pygame.SRCALPHA)
        pygame.draw.ellipse(sombra, (0, 0, 0, 90), sombra.get_rect())
        superficie.blit(sombra, sombra.get_rect(center=(self.rect.centerx - cam[0], self.rect.bottom - 2 - cam[1])))
        lado = self.ataque["lado"] if self.ataque else self.mirando
        variante = "normal"
        if self.t_retroceso > TIEMPO_RETROCESO - 0.12:
            variante = "destello"
        elif self.ataque and self.ataque["fase"] == "preparar":
            variante = "alerta" if int(self.ataque["t"] * 16) % 2 == 0 else "normal"
        imagen = self.imagenes[(variante, lado)]
        if self.t_muerte is not None:
            imagen = con_transparencia(imagen, 255 * max(0.0, 1 - self.t_muerte / 0.6))
        elif self.t_aparicion > 0:
            imagen = con_transparencia(imagen, 255 * (1 - self.t_aparicion / max(0.01, self.aparicion_total)))
        pos_img = imagen.get_rect(midbottom=(self.rect.centerx + self._desplazamiento() - cam[0], self.rect.bottom - cam[1]))
        superficie.blit(imagen, pos_img)
        if self.ataque and self.ataque["tipo"] == "distancia" and self.ataque["fase"] == "preparar":
            objetivo = self.ataque["origen"]
            fin = pygame.Vector2(objetivo) + self.ataque["direccion"] * self.alcance_ataque
            color_aviso = self.perfil.get("proyectil_color", (255, 95, 65))
            pygame.draw.line(superficie, (*color_aviso, 170),
                             (objetivo[0] - cam[0], objetivo[1] - cam[1]),
                             (round(fin.x) - cam[0], round(fin.y) - cam[1]), max(3, int(3 * self.escala / escala_enemigos)))
        if self.vivo() and self.vida < self.vida_max:
            ancho, alto = imagen.get_width(), max(4, int(1.6 * self.escala))
            barra = pygame.Rect(0, 0, ancho, alto)
            barra.midbottom = (self.rect.centerx - cam[0], pos_img.top - 6)
            pygame.draw.rect(superficie, (35, 10, 14), barra)
            pygame.draw.rect(superficie, (210, 40, 55), (barra.x, barra.y, int(ancho * self.vida / self.vida_max), alto))
            pygame.draw.rect(superficie, blanco, barra, 2)


Enemigo._imagenes = None


# Proyectiles disparados por los enemigos a distancia.
print("---------- PROYECTILES DE ENEMIGOS ----------")
class EnemigoProyectil:
    # Proyectil enemigo configurable que viaja, impacta al jugador o desaparece al agotarse.
    def __init__(self, enemigo, ataque):
        self.pos = pygame.Vector2(ataque["origen"])
        self.direccion = pygame.Vector2(ataque["direccion"])
        self.velocidad = 470
        self.dano = enemigo.dano
        self.color = enemigo.perfil.get("proyectil_color", (200, 45, 35))
        self.color_brillo = enemigo.perfil.get("proyectil_brillo", (255, 190, 75))
        ancho, alto = enemigo.perfil.get("proyectil_tamano", (34, 24))
        self.radio_exterior, self.radio_interior = enemigo.perfil.get("proyectil_radio", (8, 4))
        self.rect = pygame.Rect(0, 0, ancho, alto)
        self.rect.center = self.pos
        self.imagen = None
        sprite_proyectil = enemigo.perfil.get("proyectil_sprite")
        if sprite_proyectil:
            visual = enemigo.perfil.get("proyectil_visual", self.rect.size)
            self.imagen = cargar_imagen_proyectil(sprite_proyectil, visual)
        self.alcance = enemigo.alcance_ataque + 120
        self.recorrido = 0.0
        self.eliminado = False

    # Mueve el proyectil y lo elimina al golpear al jugador, chocar o agotar su alcance.
    def actualizar(self, dt, jugador):
        if self.eliminado:
            return
        paso = self.velocidad * dt
        self.pos += self.direccion * paso
        self.recorrido += paso
        self.rect.center = (round(self.pos.x), round(self.pos.y))
        if self.rect.colliderect(jugador.cuerpo()):
            jugador.recibir_dano(self.dano, self.pos)
            self.eliminado = True
        elif self.recorrido >= self.alcance or mapa.choca(self.rect):
            self.eliminado = True

    # Dibuja el proyectil con su sprite o con circulos de color.
    def dibujar(self, superficie, cam=(0, 0)):
        centro = (self.rect.centerx - cam[0], self.rect.centery - cam[1])
        if self.imagen is not None:
            superficie.blit(self.imagen, self.imagen.get_rect(center=centro))
            return
        pygame.draw.ellipse(superficie, self.color, self.rect.move(-cam[0], -cam[1]))
        pygame.draw.circle(superficie, self.color_brillo, centro, self.radio_exterior)
        pygame.draw.circle(superficie, (235, 250, 255), centro, self.radio_interior)


# Enemigo jefe con patrones de ataque propios (meteoro, aliento, cuerpo a cuerpo, lluvia de armas) y apoyos.
class Jefe(Enemigo):
    # Extiende al enemigo con patrones de jefe, áreas de impacto y efectos de combate propios.
    def __init__(
        self, x, y, aparicion=0.0, tipo="goblin", sprite=None,
        tipos_apoyo=(), puntos_apoyo=(), max_apoyos=0,
    ):
        super().__init__(x, y, agresivo=True, aparicion=aparicion, tipo=tipo, perfil=ENEMIGO_GOBLIN)
        self.es_jefe = True
        self.tipo_jefe = tipo
        self.nombre_jefe = {
            "goblin": "REY GOBLIN",
            "orco": "JEFE ORCO",
            "dragon": "EL CARCELERO",
        }.get(tipo, "JEFE")
        self.rect.size = (int(HITBOX_ENEMIGO_PIES[0] * self.escala * 1.6),
                          int(HITBOX_ENEMIGO_PIES[1] * self.escala * 1.6))
        self.rect.midbottom = (x, y)
        self.pos.update(self.rect.midbottom)
        self.casa.update(self.rect.midbottom)
        self.vida_max = (
            360 if tipo == "goblin"
            else 280 * JEFE_ORCO_MULTIPLICADOR_VIDA if tipo == "orco"
            else 210 * JEFE_DRAGON_MULTIPLICADOR_VIDA
        )
        self.vida = self.vida_max
        self.dano = 21 if tipo == "goblin" else 28 if tipo == "orco" else 24
        self.velocidad_jefe = 175 if tipo == "goblin" else 160 if tipo == "orco" else 145
        self.radio_golpe = 0 if tipo == "goblin" else 150 if tipo == "dragon" else 112
        self.puntos_base = {"goblin": 600, "orco": 800, "dragon": 1000}.get(tipo, 500)
        self.angulo_mirada = math.pi
        self.ataque_jefe = None
        self.t_cd = (
            JEFE_ORCO_INTERVALO_ATAQUE if tipo == "orco"
            else JEFE_DRAGON_TIEMPO_INICIAL if tipo == "dragon"
            else 0.8
        )
        self.indice_ataque = 0
        self.tipos_apoyo = tuple(tipos_apoyo)
        self.puntos_apoyo = tuple(puntos_apoyo)
        self.max_apoyos = max(0, max_apoyos)
        self.apoyos_generados = 0
        self.apoyos_pendientes = []
        self.imagen_meteoro = (
            cargar_imagen_proyectil("proyectil_mago.png", (180, 172))
            if tipo == "dragon" else None
        )
        self.imagenes_lluvia = (
            {
                "hacha": pygame.transform.rotate(
                    cargar_imagen_proyectil("ataque rey orco.png", (80, 80)), 180,
                ),
                "espada": pygame.transform.rotate(
                    cargar_imagen_proyectil("ataque jefe orco.png", (80, 80)), -45,
                ),
            }
            if tipo == "orco" else {}
        )
        sprite = cargar_sprite_enemigo(tipo if sprite is None else sprite)
        altura_jefe = JEFE_ALTURA_SPRITE if tipo == "dragon" else TAM_TILE * 1.55
        escala_jefe = altura_jefe / sprite.get_height()
        self.imagen_jefe = escalar_imagen(sprite, escala_jefe)
        self.imagen_jefe.fill((75, 12, 35, 0), special_flags=pygame.BLEND_RGB_ADD)
        self.imagenes_jefe = {
            1: pygame.transform.flip(self.imagen_jefe, True, False) if not ENEMIGO_MIRA_A_LA_DERECHA else self.imagen_jefe,
            -1: self.imagen_jefe if not ENEMIGO_MIRA_A_LA_DERECHA else pygame.transform.flip(self.imagen_jefe, True, False),
        }

    # Calcula el angulo desde el jefe hasta un objetivo.
    def _angulo_hacia(self, objetivo):
        diferencia = pygame.Vector2(objetivo) - pygame.Vector2(self.rect.center)
        if diferencia.length_squared() == 0:
            return self.angulo_mirada
        return math.atan2(diferencia.y, diferencia.x)

    # Calcula el punto de la boca desde donde sale el aliento.
    def _origen_aliento(self, angulo=None, origen=None):
        angulo = self.angulo_mirada if angulo is None else angulo
        if origen is not None:
            centro = pygame.Vector2(origen.center)
            ancho_imagen, alto_imagen = self.imagen_jefe.get_size()
            centro.y -= alto_imagen / 2
        else:
            centro = pygame.Vector2(
                self.rect.centerx,
                self.rect.bottom - self.imagen_jefe.get_height() / 2,
            )
            ancho_imagen, alto_imagen = self.imagen_jefe.get_size()
        giro = angulo - math.pi
        local_x = -ancho_imagen * 0.43
        local_y = -alto_imagen * 0.04
        return centro + pygame.Vector2(
            local_x * math.cos(giro) - local_y * math.sin(giro),
            local_x * math.sin(giro) + local_y * math.cos(giro),
        )

    # Construye el polígono direccional del aliento para dibujo y detección de impactos.
    def _vertices_aliento(self, angulo=None, origen=None):
        angulo = self.angulo_mirada if angulo is None else angulo
        direccion = pygame.Vector2(math.cos(angulo), math.sin(angulo))
        perpendicular = pygame.Vector2(-direccion.y, direccion.x)
        inicio = self._origen_aliento(angulo, origen)
        alcance = 560
        return (
            inicio - perpendicular * 24,
            inicio + direccion * alcance - perpendicular * 150,
            inicio + direccion * alcance + perpendicular * 150,
            inicio + perpendicular * 24,
        )

    # Rectangulo que envuelve el poligono del aliento.
    def _zona_aliento(self, origen=None, lado=None, angulo=None):
        if angulo is None:
            angulo = self.angulo_mirada if lado is None else (0 if lado == 1 else math.pi)
        vertices = self._vertices_aliento(angulo, origen)
        xs = [p.x for p in vertices]
        ys = [p.y for p in vertices]
        return pygame.Rect(
            math.floor(min(xs)), math.floor(min(ys)),
            max(1, math.ceil(max(xs)) - math.floor(min(xs))),
            max(1, math.ceil(max(ys)) - math.floor(min(ys))),
        )

    @staticmethod
    # Determina si un punto está dentro del polígono mediante intersecciones de rayos.
    def _punto_en_poligono(punto, vertices):
        dentro = False
        x, y = punto
        anterior = vertices[-1]
        for actual in vertices:
            if (actual.y > y) != (anterior.y > y):
                cruce = (anterior.x - actual.x) * (y - actual.y) / (
                    anterior.y - actual.y
                ) + actual.x
                if x < cruce:
                    dentro = not dentro
            anterior = actual
        return dentro

    # Comprueba la intersección entre el aliento poligonal y la hitbox rectangular.
    def _aliento_colisiona(self, rect, angulo=None):
        vertices = self._vertices_aliento(angulo)
        esquinas = (
            pygame.Vector2(rect.topleft), pygame.Vector2(rect.topright),
            pygame.Vector2(rect.bottomright), pygame.Vector2(rect.bottomleft),
        )
        if any(self._punto_en_poligono(p, vertices) for p in esquinas):
            return True
        if any(rect.collidepoint(round(p.x), round(p.y)) for p in vertices):
            return True
        return any(
            rect.clipline(tuple(vertices[i]), tuple(vertices[(i + 1) % len(vertices)]))
            for i in range(len(vertices))
        )

    # Zona de impacto del ataque cuerpo a cuerpo del jefe.
    def _zona_cuerpo_a_cuerpo(self, lado=None):
        lado = self.mirando if lado is None else lado
        zona = pygame.Rect(0, 0, 190, 150)
        y = self.rect.centery + 25
        if lado == 1:
            zona.midleft = (self.rect.centerx + self.rect.w // 3, y)
        else:
            zona.midright = (self.rect.centerx - self.rect.w // 3, y)
        return zona

    # Zona rectangular que cubre la lluvia de armas segun su orientacion.
    @staticmethod
    def _zona_lluvia_espadas(ataque):
        ancho, alto = (1280, 300) if ataque["orientacion"] == "horizontal" else (320, 1040)
        zona = pygame.Rect(0, 0, ancho, alto)
        zona.center = ataque["objetivo"]
        return zona

    # Alterna hacha y espada para cada proyectil de la lluvia.
    @staticmethod
    def _arma_lluvia(indice):
        return "hacha" if indice % 2 == 0 else "espada"

    # Programa enemigos de apoyo para que Enemigos los agregue al ciclo de actualización.
    def _invocar_apoyos(self):
        if not self.tipos_apoyo or not self.puntos_apoyo:
            return
        cantidad = min(
            JEFE_ORCO_APOYOS_POR_ATAQUE,
            self.max_apoyos - self.apoyos_generados,
        )
        for _ in range(max(0, cantidad)):
            tipo = random.choice(self.tipos_apoyo)
            punto = random.choice(self.puntos_apoyo)
            apoyo = Enemigo(
                punto[0], punto[1], agresivo=True,
                aparicion=ENEMIGO_TIEMPO_APARICION, tipo=tipo,
            )
            apoyo.invocado_por_jefe = True
            self.apoyos_pendientes.append(apoyo)
            self.apoyos_generados += 1

    # Crea el estado temporizado de un patrón e inicia sus avisos visuales y sonoros.
    def _iniciar_ataque(self, tipo, objetivo):
        lado = 1 if objetivo[0] >= self.rect.centerx else -1
        self.mirando = lado
        angulo = self._angulo_hacia(objetivo)
        self.angulo_mirada = angulo
        advertencia = {
            "meteoro": 0.8,
            "aliento": 1.5,
            "cuerpo_a_cuerpo": 0.65,
            "lluvia_espadas": 1.5,
        }[tipo]
        self.ataque_jefe = {
            "tipo": tipo,
            "fase": "aviso",
            "t": 0.0,
            "advertencia": advertencia,
            "golpeo": False,
            "objetivo": tuple(objetivo),
            "lado": lado,
            "angulo": angulo,
        }
        if tipo == "lluvia_espadas":
            self.ataque_jefe["orientacion"] = ("horizontal", "vertical")[self.indice_ataque % 2]
            self.indice_ataque += 1
            self._invocar_apoyos()

    # Evalúa la geometría del patrón activo y aplica daño si alcanza al jugador.
    def _impacto(self, jugador):
        ataque = self.ataque_jefe
        objetivo = pygame.Vector2(ataque["objetivo"])
        if ataque["tipo"] == "meteoro":
            acertado = pygame.Vector2(jugador.rect.center).distance_to(objetivo) <= self.radio_golpe + max(jugador.rect.size) / 2
            dano = self.dano
        elif ataque["tipo"] == "aliento":
            acertado = self._aliento_colisiona(
                jugador.cuerpo(), ataque.get("angulo", self.angulo_mirada)
            )
            dano = self.dano + 8
        elif ataque["tipo"] == "lluvia_espadas":
            acertado = self._zona_lluvia_espadas(ataque).colliderect(jugador.rect)
            dano = self.dano + 10
        else:
            zona = self._zona_cuerpo_a_cuerpo(ataque["lado"])
            acertado = zona.colliderect(jugador.cuerpo())
            dano = self.dano + 12
        if acertado:
            jugador.recibir_dano(dano, self.rect.center)
        return acertado

    # Hitbox corporal del jefe, mas grande que la del enemigo comun.
    def cuerpo(self):
        zona = pygame.Rect(0, 0, int(self.rect.w * 0.9), int(self.rect.h * 1.65))
        zona.midbottom = self.rect.midbottom
        return zona

    # Reduce la vida del jefe y activa su muerte al llegar a cero.
    def recibir_dano(self, cantidad, origen):
        if not self.vivo() or self.t_aparicion > 0:
            return False
        self.vida = max(0, self.vida - cantidad)
        texto_dano(cantidad, self.rect.centerx, self.rect.bottom - self.imagen_jefe.get_height(), (255, 230, 80))
        if self.vida <= 0:
            self.t_muerte = 0.0
            self.ataque_jefe = None
            reproducir_sonido("derrota_enemigo")
        else:
            reproducir_sonido("golpe_enemigo")
        return True

    # Controla las fases de ataque del jefe y elige nuevos patrones según distancia/tipo.
    def actualizar(self, dt, jugador, otros, proyectiles=None):
        if self.t_aparicion > 0:
            self.t_aparicion = max(0.0, self.t_aparicion - dt)
            return
        if self.t_muerte is not None:
            self.t_muerte += dt
            if self.t_muerte >= 0.8:
                self.eliminado = True
            return
        if self.t_retroceso > 0:
            self._retroceder(dt)
            return
        self.t_cd -= dt
        jugador_pos = pygame.Vector2(jugador.rect.center)
        yo = pygame.Vector2(self.rect.center)
        diferencia = jugador_pos - yo
        self.angulo_mirada = self._angulo_hacia(jugador.rect.center)
        if abs(diferencia.x) > ENEMIGO_UMBRAL_GIRO:
            self.mirando = 1 if diferencia.x > 0 else -1
        if self.ataque_jefe is not None:
            ataque = self.ataque_jefe
            if ataque["tipo"] == "aliento":
                ataque["angulo"] = self.angulo_mirada
            ataque["t"] += dt
            if ataque["fase"] == "aviso" and ataque["t"] >= ataque["advertencia"]:
                ataque["fase"], ataque["t"] = "activo", 0.0
                reproducir_sonido("ataque_jefe", reemplazar=SONIDOS_ATAQUE)
            elif ataque["fase"] == "activo":
                if not ataque["golpeo"] and not jugador.muerto:
                    acertado = self._impacto(jugador)
                    if ataque["tipo"] != "aliento" or acertado:
                        ataque["golpeo"] = True
                duracion = 1.0 if ataque["tipo"] == "aliento" else 0.55 if ataque["tipo"] == "lluvia_espadas" else 0.22
                if ataque["t"] >= duracion:
                    ataque["fase"], ataque["t"] = "recuperacion", 0.0
            elif ataque["fase"] == "recuperacion" and ataque["t"] >= (
                JEFE_DRAGON_RECUPERACION_ATAQUE
                if self.tipo_jefe == "dragon" else 0.7
            ):
                self.ataque_jefe = None
                if self.tipo_jefe != "orco":
                    self.t_cd = (
                        JEFE_DRAGON_INTERVALO_ATAQUE
                        if self.tipo_jefe == "dragon" else 0.5
                    )
            return

        if self.t_cd <= 0:
            if self.tipo_jefe == "orco":
                self._iniciar_ataque("lluvia_espadas", tuple(jugador.rect.center))
                self.t_cd = JEFE_ORCO_INTERVALO_ATAQUE
                return
            elif self.tipo_jefe == "goblin":
                if diferencia.length() < 260:
                    tipo = "cuerpo_a_cuerpo"
                    self._iniciar_ataque(tipo, tuple(jugador.rect.center))
                    return
            elif diferencia.length() < 235:
                tipo = "cuerpo_a_cuerpo"
            elif diferencia.length() < 560:
                tipo = "aliento"
            else:
                tipo = "meteoro"
            if self.tipo_jefe != "goblin":
                self._iniciar_ataque(tipo, tuple(jugador.rect.center))
                return
        if self.tipo_jefe == "orco":
            return
        if diferencia.length() > (185 if self.tipo_jefe == "goblin" else 220):
            obstaculos = [jugador.rect] + [o.rect for o in otros if o is not self and o.vivo()]
            if diferencia.length() > 1:
                self._mover(diferencia.normalize(), self.velocidad_jefe, dt, obstaculos)

    # Dibuja el aliento como poligonos concentricos con particulas, en aviso o activo.
    def _dibujar_aliento(self, superficie, cam, ataque, pulso):
        vertices = self._vertices_aliento(ataque.get("angulo", self.angulo_mirada))
        xs = [p.x - cam[0] for p in vertices]
        ys = [p.y - cam[1] for p in vertices]
        limite = pygame.Rect(
            math.floor(min(xs)), math.floor(min(ys)),
            max(1, math.ceil(max(xs)) - math.floor(min(xs))),
            max(1, math.ceil(max(ys)) - math.floor(min(ys))),
        ).inflate(12, 12).clip(superficie.get_rect())
        if not limite:
            return
        capa = pygame.Surface(limite.size, pygame.SRCALPHA)
        puntos = [(round(x - limite.left), round(y - limite.top)) for x, y in zip(xs, ys)]
        aviso = ataque["fase"] == "aviso"
        color_exterior = (255, 105, 25, 55 if aviso else 115)
        color_medio = (255, 75, 15, 25 if aviso else 175)
        color_nucleo = (255, 220, 90, 15 if aviso else 210)
        pygame.draw.polygon(capa, color_exterior, puntos)

        centro = pygame.Vector2(
            sum(p[0] for p in puntos) / len(puntos),
            sum(p[1] for p in puntos) / len(puntos),
        )
        medio = [
            (round(centro.x + (x - centro.x) * 0.67),
             round(centro.y + (y - centro.y) * 0.67))
            for x, y in puntos
        ]
        nucleo = [
            (round(centro.x + (x - centro.x) * 0.34),
             round(centro.y + (y - centro.y) * 0.34))
            for x, y in puntos
        ]
        pygame.draw.polygon(capa, color_medio, medio)
        pygame.draw.polygon(capa, color_nucleo, nucleo)
        borde = (255, 210, 105, 190) if aviso else (255, 130, 35, 230)
        pygame.draw.lines(capa, borde, True, puntos, 3 if aviso else 2)
        superficie.blit(capa, limite.topleft)

        direccion = pygame.Vector2(math.cos(ataque.get("angulo", self.angulo_mirada)),
                                   math.sin(ataque.get("angulo", self.angulo_mirada)))
        perpendicular = pygame.Vector2(-direccion.y, direccion.x)
        origen = self._origen_aliento(ataque.get("angulo", self.angulo_mirada))
        cantidad = 7 if aviso else 17
        for i in range(cantidad):
            avance = (i / cantidad + ataque["t"] * (0.5 if aviso else 1.35)) % 1.0
            ancho = 24 + 126 * avance
            deriva = math.sin(i * 2.7 + ataque["t"] * 11) * ancho * 0.64
            posicion = origen + direccion * (560 * avance) + perpendicular * deriva
            centro_particula = (round(posicion.x - cam[0]), round(posicion.y - cam[1]))
            radio = max(2, int((5 + pulso * 8) * (0.55 + avance)))
            pygame.draw.circle(
                superficie,
                (255, 205, 80) if i % 3 == 0 else (255, 95, 25),
                centro_particula, radio,
            )

    # Dibuja los avisos y efectos del ataque activo, la sombra y el sprite del jefe.
    def dibujar(self, superficie, cam=(0, 0)):
        ataque = self.ataque_jefe
        if ataque:
            pulso = 0.5 + 0.5 * math.sin(ataque["t"] * 12)
            if ataque["tipo"] == "lluvia_espadas":
                zona_mundo = self._zona_lluvia_espadas(ataque)
                zona = zona_mundo.move(-cam[0], -cam[1])
                advertencia = ataque["fase"] == "aviso"
                borde = (255, 205, 75) if advertencia else (255, 90, 35)
                rect_translucido(superficie, borde, 28 if advertencia else 45, zona, 18)
                pygame.draw.rect(superficie, borde, zona, 5, border_radius=18)
                cantidad = 13
                for i in range(cantidad):
                    fraccion = (i + 0.5) / cantidad
                    x_mundo = zona_mundo.left + round(zona_mundo.w * fraccion)
                    y_objetivo = zona_mundo.top + round(
                        zona_mundo.h * (0.25 + 0.25 * (i % 3))
                    )
                    y_inicio = zona_mundo.top - 130
                    imagen_arma = self.imagenes_lluvia[self._arma_lluvia(i)]
                    if advertencia:
                        y_mundo = y_inicio - 22 * (i % 3)
                        imagen_arma = con_transparencia(imagen_arma, 175 + int(55 * pulso))
                    else:
                        retraso = i * 0.014
                        duracion_caida = 0.33
                        avance = max(0.0, min(1.0, (ataque["t"] - retraso) / duracion_caida))
                        y_mundo = y_inicio + (y_objetivo - y_inicio) * avance ** 2
                        if 0 < avance < 1:
                            x_pantalla = round(x_mundo - cam[0])
                            y_pantalla = round(y_mundo - cam[1])
                            pygame.draw.line(
                                superficie, (255, 170, 65),
                                (x_pantalla, y_pantalla - 58),
                                (x_pantalla, y_pantalla - 18), 3,
                            )
                    centro_arma = (round(x_mundo - cam[0]), round(y_mundo - cam[1]))
                    superficie.blit(imagen_arma, imagen_arma.get_rect(center=centro_arma))
            elif ataque["tipo"] == "meteoro":
                tx, ty = ataque["objetivo"]
                radio = int(self.radio_golpe * (0.82 + 0.18 * pulso))
                centro = (int(tx - cam[0]), int(ty - cam[1]))
                pygame.draw.circle(superficie, (255, 90, 35), centro, radio, 3)
                pygame.draw.circle(superficie, (255, 190, 70), centro, max(8, int(radio * (0.12 + 0.08 * pulso))), 2)
                if ataque["fase"] == "activo":
                    avance = min(1.0, ataque["t"] / 0.22)
                    meteor_y = int(ty - cam[1] - 320 * (1 - avance))
                    pygame.draw.line(superficie, (255, 125, 45), (centro[0], meteor_y - 50), (centro[0], meteor_y + 40), 24)
                    if self.imagen_meteoro is not None:
                        superficie.blit(
                            self.imagen_meteoro,
                            self.imagen_meteoro.get_rect(center=(centro[0], meteor_y)),
                        )
            elif ataque["tipo"] == "aliento":
                self._dibujar_aliento(superficie, cam, ataque, pulso)
            else:
                zona = self._zona_cuerpo_a_cuerpo(ataque["lado"]).move(-cam[0], -cam[1])
                pygame.draw.rect(superficie, (255, 80, 55), zona, 3, border_radius=24)
                if ataque["fase"] == "activo":
                    centro = (zona.centerx, zona.centery)
                    radio = int(55 + pulso * 35)
                    caja_arco = pygame.Rect(centro[0] - radio, centro[1] - radio, radio * 2, radio * 2)
                    pygame.draw.arc(superficie, (255, 225, 135), caja_arco, 0.3, 2.8, 12)
                    pygame.draw.arc(superficie, (255, 90, 45), caja_arco.inflate(22, 22), 0.3, 2.8, 6)

        sombra = pygame.Surface((self.rect.w * 2, self.rect.h), pygame.SRCALPHA)
        pygame.draw.ellipse(sombra, (0, 0, 0, 115), sombra.get_rect())
        superficie.blit(sombra, sombra.get_rect(center=(self.rect.centerx - cam[0], self.rect.bottom - cam[1])))
        imagen = self.imagenes_jefe[self.mirando]
        if self.t_muerte is not None:
            imagen = con_transparencia(imagen, 255 * max(0.0, 1 - self.t_muerte / 0.8))
        elif self.t_aparicion > 0:
            imagen = con_transparencia(imagen, 255 * (1 - self.t_aparicion / max(0.01, self.aparicion_total)))
        animacion_idle = math.sin(pygame.time.get_ticks() / 180) * 5 if ataque is None else 0
        destino = imagen.get_rect(midbottom=(self.rect.centerx - cam[0], self.rect.bottom - cam[1] + animacion_idle))
        superficie.blit(imagen, destino)


# Ataque especial de la mejora 'Tajo de viento'.
print("---------- ATAQUES ESPECIALES DEL JUGADOR ----------")
class TajoViento:
    # Ataque de bonificación que viaja en la dirección apuntada y puede golpear varios enemigos.
    def __init__(self, jugador, objetivo=None):
        origen = pygame.Vector2(
            jugador.rect.centerx,
            jugador.rect.centery - 20 * escala_jugador,
        )
        objetivo = pos_raton_mundo() if objetivo is None else pygame.Vector2(objetivo)
        vector_ataque = pygame.Vector2(objetivo) - origen
        if vector_ataque.length_squared() == 0:
            vector_ataque.update(jugador.mirando, 0)
        self.direccion = vector_ataque.normalize()
        self.perpendicular = pygame.Vector2(-self.direccion.y, self.direccion.x)
        self.pos = origen + self.direccion * 45
        self.velocidad = 850
        self.alcance = 850
        self.recorrido = 0.0
        self.dano = round((18 + 7 * jugador.bonificaciones["viento"]) * jugador.multiplicador_dano)
        ancho, alto = HITBOX_ATAQUES["atacar"]
        self.hitbox_ancho = ancho * escala_jugador
        self.hitbox_alto = alto * escala_jugador
        self.rect = pygame.Rect(0, 0, 1, 1)
        self._actualizar_rect()
        self.enemigos_golpeados = set()
        self.eliminado = False

    # Recalcula el rectangulo que envuelve el tajo segun su direccion.
    def _actualizar_rect(self):
        mitad_ancho = (
            abs(self.direccion.x) * self.hitbox_ancho
            + abs(self.perpendicular.x) * self.hitbox_alto
        ) / 2
        mitad_alto = (
            abs(self.direccion.y) * self.hitbox_ancho
            + abs(self.perpendicular.y) * self.hitbox_alto
        ) / 2
        self.rect.size = (math.ceil(mitad_ancho * 2), math.ceil(mitad_alto * 2))
        self.rect.center = (round(self.pos.x), round(self.pos.y))

    # Refina el solapamiento de rectángulos mediante proyecciones sobre ejes del tajo.
    def _colisiona(self, rect):
        if not self.rect.colliderect(rect):
            return False
        vertices = (
            pygame.Vector2(rect.topleft),
            pygame.Vector2(rect.topright),
            pygame.Vector2(rect.bottomright),
            pygame.Vector2(rect.bottomleft),
        )
        for eje in (pygame.Vector2(1, 0), pygame.Vector2(0, 1), self.direccion, self.perpendicular):
            limites_tajo = (
                -self.hitbox_ancho / 2 if eje == self.direccion else -self.hitbox_alto / 2,
                self.hitbox_ancho / 2 if eje == self.direccion else self.hitbox_alto / 2,
            )
            centro = self.pos.dot(eje)
            min_tajo, max_tajo = centro + limites_tajo[0], centro + limites_tajo[1]
            proyecciones = [vertice.dot(eje) for vertice in vertices]
            if max(proyecciones) < min_tajo or min(proyecciones) > max_tajo:
                return False
        return True

    # Avanza el tajo, danya a los enemigos que toca y lo elimina al agotar su alcance.
    def actualizar(self, dt, enemigos):
        paso = self.velocidad * dt
        self.pos += self.direccion * paso
        self.recorrido += paso
        self._actualizar_rect()
        for enemigo in enemigos:
            if enemigo.vivo() and enemigo not in self.enemigos_golpeados and self._colisiona(enemigo.cuerpo()):
                if enemigo.recibir_dano(self.dano, self.pos):
                    self.enemigos_golpeados.add(enemigo)
        if self.recorrido >= self.alcance:
            self.eliminado = True

    # Dibuja el tajo como tres lineas concentricas.
    def dibujar(self, superficie, cam=(0, 0)):
        cx, cy = int(self.rect.centerx - cam[0]), int(self.rect.centery - cam[1])
        centro = pygame.Vector2(cx, cy)
        avance = self.direccion
        lado = self.perpendicular
        mitad_ancho, mitad_alto = self.hitbox_ancho / 2, self.hitbox_alto / 2
        vertices = (
            centro - avance * mitad_ancho - lado * mitad_alto * 0.45,
            centro - avance * mitad_ancho * 0.35 + lado * mitad_alto,
            centro + avance * mitad_ancho + lado * mitad_alto * 0.25,
        )
        puntos = tuple((round(p.x), round(p.y)) for p in vertices)
        pygame.draw.lines(superficie, (55, 165, 225), False, puntos, max(8, int(mitad_alto / 3)))
        pygame.draw.lines(superficie, (160, 235, 255), False, puntos, max(4, int(mitad_alto / 7)))
        pygame.draw.lines(superficie, (245, 255, 255), False, puntos, max(2, int(mitad_alto / 16)))


# Agrupa los enemigos y proyectiles y gestiona su actualizacion, dano y separacion fisica.
print("---------- ADMINISTRACION Y COLISIONES DE ENEMIGOS ----------")
class Enemigos:
    # Agrupa enemigos y proyectiles y centraliza actualización, daño y separación física.
    def __init__(self):
        self.lista = []
        self.proyectiles = []

    # Permite recorrer directamente los enemigos de la lista.
    def __iter__(self):
        return iter(self.lista)

    # Devuelve la cantidad de enemigos.
    def __len__(self):
        return len(self.lista)

    # Anade un enemigo a la lista.
    def agregar(self, enemigo):
        self.lista.append(enemigo)

    # Devuelve el jefe vivo, o None si no hay.
    def jefe_vivo(self):
        return next((e for e in self.lista if getattr(e, "es_jefe", False) and e.vivo()), None)

    # Actualiza entidades, limpia las eliminadas y procesa ataques y colisiones de contacto.
    def actualizar(self, dt, jugador, proyectiles=()):
        for e in tuple(self.lista):
            e.actualizar(dt, jugador, self.lista, self.proyectiles)
            apoyos = getattr(e, "apoyos_pendientes", ())
            if apoyos:
                self.lista.extend(apoyos)
                e.apoyos_pendientes.clear()
        for proyectil in self.proyectiles:
            proyectil.actualizar(dt, jugador)
        self.proyectiles = [p for p in self.proyectiles if not p.eliminado]
        self._golpes_del_jugador(jugador)
        for proyectil in proyectiles:
            proyectil.actualizar(dt, self.lista)
        self._chocar_con_jugador(jugador)
        self.lista = [e for e in self.lista if not e.eliminado]

    # Aplica el dano de los ataques del jugador a los enemigos alcanzados.
    def _golpes_del_jugador(self, jugador):
        zona = jugador.hitbox()
        if zona is None:
            return
        dano = round(DANO_ATAQUE[jugador.accion] * jugador.multiplicador_dano)
        for e in self.lista:
            if e.vivo() and e not in jugador.golpeados and zona.colliderect(e.cuerpo()):
                if e.recibir_dano(dano, jugador.rect.center):
                    jugador.golpeados.add(e)

    # Separa al jugador de los enemigos y aplica dano por contacto si esta activado.
    def _chocar_con_jugador(self, jugador):
        if jugador.muerto:
            return
        cuerpo = jugador.cuerpo()
        for e in self.lista:
            if not e.vivo() or e.t_aparicion > 0:
                continue
            if DANO_POR_CONTACTO and cuerpo.colliderect(e.cuerpo()):
                jugador.recibir_dano(e.dano, e.rect.center)
            if jugador.z < 50 and jugador.rect.colliderect(e.rect):
                salidas = [
                    (e.rect.right - jugador.rect.left, (1, 0)),
                    (jugador.rect.right - e.rect.left, (-1, 0)),
                    (e.rect.bottom - jugador.rect.top, (0, 1)),
                    (jugador.rect.bottom - e.rect.top, (0, -1)),
                ]
                distancia, (sx, sy) = min(salidas)
                jugador.rect.move_ip(sx * distancia, sy * distancia)
                jugador.pos.update(jugador.rect.center)


# Numeros flotantes que muestran el dano causado y recibido.
print("---------- INDICADORES DE DANO ----------")
class NumerosDano:
    # Administra textos flotantes que ascienden y se desvanecen con el tiempo.
    DURACION = 0.9
    SUBIDA = 110

    # Crea la lista de textos y la fuente usada para mostrarlos.
    def __init__(self):
        self.lista = []
        self.fuente = pygame.font.Font(None, 48)

    # Anade un texto de dano con una pequena variacion horizontal.
    def agregar(self, cantidad, x, y, color):
        self.lista.append({"texto": str(int(cantidad)), "x": x + random.uniform(-16, 16),
                           "y": y, "t": 0.0, "color": color})

    # Hace subir los textos y elimina los que ya terminaron.
    def actualizar(self, dt):
        for n in self.lista:
            n["t"] += dt
            n["y"] -= self.SUBIDA * (1 - n["t"] / self.DURACION) * dt
        self.lista = [n for n in self.lista if n["t"] < self.DURACION]

    # Dibuja cada texto con contorno y desvanecido progresivo.
    def dibujar(self, superficie, cam=(0, 0)):
        for n in self.lista:
            p = n["t"] / self.DURACION
            alpha = 255 * (1 - max(0.0, (p - 0.5) / 0.5))
            base = self.fuente.render(n["texto"], True, n["color"])
            borde = self.fuente.render(n["texto"], True, (0, 0, 0))
            w, h = base.get_size()
            img = pygame.Surface((w + 4, h + 4), pygame.SRCALPHA)
            for dx, dy in ((0, 0), (2, 0), (4, 0), (0, 2), (4, 2), (0, 4), (2, 4), (4, 4)):
                img.blit(borde, (dx, dy))
            img.blit(base, (2, 2))
            img = con_transparencia(img, alpha)
            superficie.blit(img, img.get_rect(center=(n["x"] - cam[0], n["y"] - cam[1])))


numeros_dano = NumerosDano()


# Atajo para mostrar un numero de dano flotante.
def texto_dano(cantidad, x, y, color):
    numeros_dano.agregar(cantidad, x, y, color)


# Clase que coordina una partida completa: jugador, enemigos, oleadas, recompensas y dibujo.
print("---------- CLASE PRINCIPAL DE LA PARTIDA ----------")
class Partida:
    # Coordina estado global de una partida: jugador, oleadas, recompensas y renderizado.
    def __init__(self):
        mapa.reiniciar_progreso()
        self.jugador = Jugador(*mapa.inicio)
        self.enemigos = Enemigos()
        self.oleadas = Oleadas(ZONAS)
        self.puntuacion = 0
        self.bestscore = 0
        self.proyectiles = []
        self.pociones_mundo = []
        self.recompensas_entregadas = 0
        self.bonificacion_pendiente = False
        self.retraso_bonificacion = 0.0
        self.tarjetas_bonificacion = [
            pygame.Rect(width // 2 - 570 + i * 390, height // 2 - 25, 365, 250)
            for i in range(len(BONIFICACIONES))
        ]
        actualizar_camara(self.jugador, 0, True)
        numeros_dano.lista.clear()

    # Indica si la partida acabo por muerte o por victoria.
    @property
    def terminada(self):
        return self.jugador.muerto or (
            self.oleadas.victoria and not self.bonificacion_pendiente and self.retraso_bonificacion <= 0
        )

    # Aplica una mejora elegida y evita exceder el nivel máximo configurado.
    def elegir_bonificacion(self, indice):
        if not self.bonificacion_pendiente or not 0 <= indice < len(BONIFICACIONES):
            return False
        poder = BONIFICACIONES[indice][0]
        nivel = self.jugador.bonificaciones[poder]
        if nivel >= MEJORAS_MAXIMAS_POR_PODER:
            return False
        self.jugador.bonificaciones[poder] = nivel + 1
        self.bonificacion_pendiente = False
        self.oleadas._aviso([f"{BONIFICACIONES[indice][1]} mejorado a nivel {nivel + 1}"], 3.0)
        return True

    # Ejecuta un paso de simulación y coordina recompensas, puntuación y cámara.
    def actualizar(self, dt, teclas):
        if self.bonificacion_pendiente:
            return
        if self.retraso_bonificacion > 0:
            self.retraso_bonificacion = max(0.0, self.retraso_bonificacion - dt)
            if self.retraso_bonificacion == 0:
                self.bonificacion_pendiente = True
            return
        self.jugador.actualizar(teclas, dt)
        if self.jugador.tajo_viento_pendiente:
            self.proyectiles.append(TajoViento(self.jugador, pos_raton_mundo()))
            self.jugador.tajo_viento_pendiente = False
        self.enemigos.actualizar(dt, self.jugador, self.proyectiles)
        self.proyectiles = [p for p in self.proyectiles if not p.eliminado]
        self.oleadas.actualizar(dt, self.jugador, self.enemigos)
        self.puntuacion = self.oleadas.puntuacion
        self.bestscore = max(self.bestscore, self.puntuacion)
        self._recoger_pociones()
        completadas = sum(z["estado"] == "completada" for z in self.oleadas.zonas)
        if completadas > self.recompensas_entregadas:
            self.recompensas_entregadas = completadas
            self.retraso_bonificacion = RETARDO_ELECCION_BONIFICACION
        if self.oleadas.victoria:
            if not self.bonificacion_pendiente and self.retraso_bonificacion <= 0:
                self.jugador.celebrar()
        numeros_dano.actualizar(dt)
        actualizar_camara(self.jugador, dt)

    # Devuelve el cofre cerrado mas cercano al jugador, si hay alguno.
    def cofre_cercano(self):
        cercano = self.jugador.rect.inflate(110, 110)
        return next(
            (cofre for cofre in mapa.cofres if not cofre.abierto and cercano.colliderect(cofre.rect)),
            None,
        )

    # Un cofre solo se puede abrir cuando esta cerca y no quedan enemigos vivos.
    def puede_abrir_cofre(self):
        return self.cofre_cercano() is not None and not any(
            enemigo.vivo() for enemigo in self.enemigos
        )

    # Comprueba condiciones de combate, abre el cofre y genera una poción recogible.
    def abrir_cofre(self):
        if not self.puede_abrir_cofre():
            return False
        cofre = self.cofre_cercano()
        if cofre is None or not cofre.abrir():
            return False
        reproducir_sonido("abrir_cofre")
        self.pociones_mundo.append(Pocion(cofre.rect.center))
        self.oleadas._aviso(["Cofre abierto: ha aparecido una pocion"], 2.5)
        return True

    # Añade al inventario las pociones que tocan al jugador y las retira del mundo.
    def _recoger_pociones(self):
        recogidas = []
        for pocion in self.pociones_mundo:
            if self.jugador.rect.colliderect(pocion.rect):
                self.jugador.pociones += 1
                reproducir_sonido("recoger_pocion")
                recogidas.append(pocion)
        if recogidas:
            self.pociones_mundo = [p for p in self.pociones_mundo if p not in recogidas]
            self.oleadas._aviso(["Pocion recogida: pulsa Q para curarte 30 de vida"], 2.5)

    # Dibuja el mundo por profundidad y presenta HUD, hitboxes y avisos de progreso.
    def dibujar(self, superficie, cursor_oculto):
        cam = camara_pos()
        mapa.dibujar_suelo(superficie, cam)
        self.oleadas.dibujar_perimetro(superficie, cam)
        entidades = (
            mapa.props_visibles(cam) + self.enemigos.lista
            + self.enemigos.proyectiles + self.proyectiles + self.pociones_mundo + [self.jugador]
        )
        for ent in sorted(entidades, key=lambda o: o.rect.bottom):
            ent.dibujar(superficie, cam)
        if MOSTRAR_HITBOX:
            self._dibujar_hitboxes(superficie, cam)
        self.oleadas.dibujar_vineta(superficie, self.jugador)
        if MOSTRAR_HUD:
            numeros_dano.dibujar(superficie, cam)
            texto_borde(
                superficie, f"PUNTOS: {self.puntuacion}", fuente_peq, amarillo,
                (20, 12), centrado=False,
            )
            texto_borde(
                superficie, f"BEST SCORE: {self.bestscore}", fuente_peq, (255, 210, 135),
                (20, 40), centrado=False,
            )
            self.oleadas.dibujar_flecha(superficie, self.jugador, cam)
            dibujar_barra_vida(superficie, self.jugador)
            self.oleadas.dibujar_hud(superficie)
            icono_pocion = cargar_imagen_pocion((64, 64))
            superficie.blit(icono_pocion, (20, 184))
            texto_borde(superficie, str(self.jugador.pociones), fuente_peq, (255, 150, 165),
                        (90, 202), centrado=False)
            if (not self.bonificacion_pendiente and self.retraso_bonificacion <= 0
                    and not self.terminada and self.puede_abrir_cofre()):
                texto_borde(superficie, "F - Abrir cofre", menu_font, (255, 225, 130),
                            (width // 2, height - 115))
            if self.jugador.bonificaciones["berserker"]:
                estado = (f"BERSERKER ACTIVO {self.jugador.berserker_tiempo:.1f}s"
                          if self.jugador.berserker_activo else f"BERSERKER - recarga {self.jugador.berserker_enfriamiento:.1f}s")
                texto_borde(superficie, estado, fuente_peq, (255, 115, 70), (20, 254), centrado=False)
            jefe = self.enemigos.jefe_vivo()
            if jefe is not None:
                self._dibujar_barra_jefe(superficie, jefe)
            if self.terminada:
                texto = "Has muerto - pulsa Enter para reiniciar" if self.jugador.muerto else "Victoria! - pulsa Enter para jugar otra vez"
                aviso = menu_font.render(texto, True, amarillo)
                superficie.blit(aviso, aviso.get_rect(center=(width // 2, 130 if self.jugador.muerto else 120)))
                dibujar_boton_caja("guardar progreso", boton_ranuras_final)
            if MOSTRAR_CONTROLES:
                for i, linea in enumerate(ayuda_juego):
                    superficie.blit(linea, (20, height - 54 + i * 24))
            if cursor_oculto and MOSTRAR_MIRA:
                dibujar_mira(superficie)
            if self.retraso_bonificacion > 0:
                velo_premio = pygame.Surface((width, height), pygame.SRCALPHA)
                velo_premio.fill((5, 8, 18, 175))
                superficie.blit(velo_premio, (0, 0))
                texto_borde(superficie, "OLEADA COMPLETADA", titulo_font, amarillo, (width // 2, height // 2 - 24))
                texto_borde(superficie, "Preparando tu recompensa...", menu_font, blanco,
                            (width // 2, height // 2 + 48))
            elif self.bonificacion_pendiente:
                self._dibujar_eleccion_bonificacion(superficie)

    # Dibuja la pantalla de eleccion de mejora con sus tres tarjetas.
    def _dibujar_eleccion_bonificacion(self, superficie):
        velo_premio = pygame.Surface((width, height), pygame.SRCALPHA)
        velo_premio.fill((5, 8, 18, 220))
        superficie.blit(velo_premio, (0, 0))
        texto_borde(superficie, "OLEADA COMPLETADA", titulo_font, amarillo, (width // 2, 135))
        texto_borde(superficie, "Elige una mejora permanente para esta partida", menu_font, blanco, (width // 2, 215))
        for i, (poder, nombre, descripcion) in enumerate(BONIFICACIONES):
            nivel = self.jugador.bonificaciones[poder]
            disponible = nivel < MEJORAS_MAXIMAS_POR_PODER
            tarjeta = self.tarjetas_bonificacion[i]
            color = ((45, 95, 125) if poder == "viento" else
                     (125, 75, 50) if poder == "dano" else (135, 45, 55))
            fondo = color if disponible else (48, 48, 54)
            pygame.draw.rect(superficie, fondo, tarjeta, border_radius=16)
            pygame.draw.rect(superficie, amarillo if disponible else (100, 100, 100), tarjeta, 3, border_radius=16)
            texto_borde(superficie, f"{i + 1}. {nombre}", menu_font, blanco, (tarjeta.centerx, tarjeta.y + 38))
            texto_borde(superficie, f"Nivel {nivel} -> {nivel + 1}" if disponible else "MAXIMO",
                        fuente_peq, amarillo if disponible else (180, 180, 180), (tarjeta.centerx, tarjeta.y + 84))
            lineas = {
                "viento": (f"Cada {max(1, 4 - nivel - 1)} golpe(s) conectados",
                           "lanza un tajo de largo alcance."),
                "dano": (f"+15% de dano por nivel", "mejora todos los ataques."),
                "berserker": (f"Pulsa V: {5 + 2 * (nivel + 1)}s de poder",
                              "mas dano y velocidad,", "menos dano recibido."),
            }[poder]
            for linea, y in zip(lineas, (tarjeta.y + 137, tarjeta.y + 167, tarjeta.y + 197)):
                texto_borde(superficie, linea, fuente_peq, blanco if disponible else (160, 160, 160),
                            (tarjeta.centerx, y))
            texto_borde(superficie, "Clic para elegir", fuente_peq, (210, 225, 240),
                        (tarjeta.centerx, tarjeta.bottom - 27))
        texto_borde(superficie, "Las mejoras se acumulan hasta nivel 3 por poder", fuente_peq, blanco,
                    (width // 2, height - 72))

    # Dibuja el nombre y la barra de vida del jefe.
    @staticmethod
    def _dibujar_barra_jefe(superficie, jefe):
        ancho, alto = 520, 24
        x, y = (width - ancho) // 2, 42
        texto_borde(superficie, jefe.nombre_jefe, fuente_peq, (255, 205, 130), (width // 2, 20))
        barra = pygame.Rect(x, y, ancho, alto)
        pygame.draw.rect(superficie, (35, 10, 14), barra, border_radius=6)
        pygame.draw.rect(superficie, (190, 35, 55),
                         (x, y, int(ancho * jefe.vida / jefe.vida_max), alto), border_radius=6)
        pygame.draw.rect(superficie, blanco, barra, 2, border_radius=6)

    # Dibuja las hitboxes del jugador, enemigos y mapa (modo depuracion).
    def _dibujar_hitboxes(self, superficie, cam):
        mapa.dibujar_colisiones(superficie, cam)
        j = self.jugador
        pygame.draw.rect(superficie, (0, 200, 255), j.rect.move(-cam[0], -cam[1]), 2)
        pygame.draw.rect(superficie, (80, 255, 80), j.cuerpo().move(-cam[0], -cam[1]), 2)
        golpe = j.hitbox()
        if golpe is not None:
            pygame.draw.rect(superficie, (255, 255, 0), golpe.move(-cam[0], -cam[1]), 3)
        for e in self.enemigos:
            pygame.draw.rect(superficie, (255, 150, 0), e.rect.move(-cam[0], -cam[1]), 2)
            pygame.draw.rect(superficie, (255, 60, 60), e.cuerpo().move(-cam[0], -cam[1]), 2)
            if e.vivo():
                lado = e.ataque["lado"] if e.ataque else e.mirando
                grosor = 4 if e.ataque and e.ataque["fase"] == "golpe" else 1
                pygame.draw.rect(superficie, (255, 60, 255), e.zona_ataque(lado).move(-cam[0], -cam[1]), grosor)


print("---------- FUNCIONES GENERALES DE INTERFAZ ----------")
# Presenta la superficie lógica a la resolución actual de la ventana.
def blit_scaled():
    scaled = pygame.transform.scale(game_surface, ventana.get_size())
    ventana.blit(scaled, (0, 0))


# Renderiza un texto centrado horizontalmente en la superficie principal.
def dibujar_texto(texto, color, y):
    render = menu_font.render(texto, True, color)
    game_surface.blit(render, render.get_rect(center=(width // 2, y)))


# Traduce posiciones de ventana a coordenadas internas antes de detectar clics.
def pos_en_juego(pos):
    sx, sy = ventana.get_size()
    return (pos[0] * width / sx, pos[1] * height / sy)


# Calcula el rectangulo de interaccion de un boton de texto.
def zona_boton(texto, y):
    return menu_font.render(texto, True, blanco).get_rect(center=(width // 2, y)).inflate(60, 24)


# Dibuja un botón de texto y comunica su rectángulo de interacción.
def dibujar_boton(texto, color, color_hover, y):
    zona = zona_boton(texto, y)
    encima = zona.collidepoint(pos_en_juego(pygame.mouse.get_pos()))
    dibujar_texto(texto, color_hover if encima else color, y)
    return zona


# Renderiza un botón con caja y respuesta visual cuando el puntero está encima.
def dibujar_boton_caja(texto, rect):
    encima = rect.collidepoint(pos_en_juego(pygame.mouse.get_pos()))
    relleno = (70, 60, 110) if encima else (35, 30, 60)
    borde = amarillo if encima else (150, 150, 190)
    pygame.draw.rect(game_surface, relleno, rect, border_radius=14)
    pygame.draw.rect(game_surface, borde, rect, width=3, border_radius=14)
    render = menu_font.render(texto, True, amarillo if encima else blanco)
    game_surface.blit(render, render.get_rect(center=rect.center))


# Compone el fondo del menú y la capa oscura que mejora la legibilidad.
def dibujar_fondo():
    if video_fondo is None:
        game_surface.blit(fondo_menu, (0, 0))
    else:
        video_fondo.dibujar(game_surface)
    game_surface.blit(velo, (0, 0))


print("---------- FUNCIONES DE REPRODUCCION DE MUSICA ----------")
# Aplica el nivel configurado a la música de fondo de Pygame.
def aplicar_volumen():
    if pygame.mixer.get_init():
        pygame.mixer.music.set_volume(ajustes["musica"])


# Devuelve el nombre de la cancion sin carpeta ni extension.
def nombre_cancion(ruta):
    return os.path.splitext(os.path.basename(ruta))[0]


# Ajusta textos largos a varias líneas dentro del ancho disponible.
def renderizar_texto_ajustado(texto, fuente, color, ancho_maximo):
    contenido = str(texto)
    while contenido and fuente.size(contenido)[0] > ancho_maximo:
        contenido = contenido[:-1]
    if contenido != str(texto) and ancho_maximo >= fuente.size("...")[0]:
        while contenido and fuente.size(contenido + "...")[0] > ancho_maximo:
            contenido = contenido[:-1]
        contenido += "..."
    return fuente.render(contenido, True, color)


# Indica si queda alguna cancion activada.
def hay_activas():
    return any(activas.values())


# Inicia una pista y actualiza el índice actual, desactivando archivos que no se leen.
def reproducir(indice):
    global actual
    try:
        pygame.mixer.music.load(canciones[indice])
        pygame.mixer.music.play(0)
        aplicar_volumen()
        actual = indice
        return True
    except pygame.error:
        activas[canciones[indice]] = False
        return False


# Avanza circularmente por las pistas activas hasta encontrar una reproducible.
def siguiente(paso=1):
    global actual
    if not canciones or not pygame.mixer.get_init():
        return
    n = len(canciones)
    for k in range(1, n + 1):
        idx = (actual + paso * k) % n
        if activas[canciones[idx]] and reproducir(idx):
            return
    pygame.mixer.music.stop()
    actual = -1


# Activa/desactiva una pista y sustituye la reproducción si se deshabilita la actual.
def alternar_cancion(indice):
    activas[canciones[indice]] = not activas[canciones[indice]]
    if indice == actual and not activas[canciones[indice]]:
        siguiente()


# Mantiene la lista en reproducción cuando la pista actual termina.
def revisar_musica():
    if (canciones and pygame.mixer.get_init() and hay_activas()
            and not pygame.mixer.music.get_busy()):
        siguiente()


# Reconfigura la ventana de Pygame conforme a la opción de pantalla completa.
def aplicar_pantalla():
    global ventana
    if ajustes["pantalla_completa"]:
        ventana = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    else:
        ventana = pygame.display.set_mode((1280, 720))


# Dibuja el valor actual de un control deslizante de volumen.
def dibujar_slider(texto, clave):
    barra = sliders[clave]
    valor = ajustes[clave]
    etiqueta = menu_font.render(texto, True, blanco)
    game_surface.blit(etiqueta, etiqueta.get_rect(midleft=(450, barra.centery)))
    pygame.draw.rect(game_surface, (80, 80, 80), barra, border_radius=6)
    relleno = pygame.Rect(barra.left, barra.top, int(barra.width * valor), barra.height)
    pygame.draw.rect(game_surface, amarillo, relleno, border_radius=6)
    pygame.draw.circle(game_surface, blanco, (barra.left + int(barra.width * valor), barra.centery), 14)
    porcentaje = menu_font.render(f"{int(valor * 100)}%", True, blanco)
    game_surface.blit(porcentaje, porcentaje.get_rect(midleft=(barra.right + 40, barra.centery)))


# Representa una opción booleana como interruptor visual.
def dibujar_interruptor(texto, clave):
    caja = interruptores[clave]
    activo = ajustes[clave]
    etiqueta = menu_font.render(texto, True, blanco)
    game_surface.blit(etiqueta, etiqueta.get_rect(midleft=(450, caja.centery)))
    pygame.draw.rect(game_surface, (60, 160, 90) if activo else (160, 60, 60), caja, border_radius=10)
    estado = menu_font.render("SI" if activo else "NO", True, blanco)
    game_surface.blit(estado, estado.get_rect(center=caja.center))


# Texto que indica la cancion que suena actualmente.
def texto_ahora_suena():
    if 0 <= actual < len(canciones):
        return "Ahora suena: " + nombre_cancion(canciones[actual])[:50]
    return "Ahora suena: (nada)"


print("---------- FUNCIONES DE GUARDADO Y CARGA ----------")
# Consulta el almacenamiento y actualiza el estado que muestra la pantalla de guardados.
def refrescar_ranuras():
    global ranuras_guardadas, estado_ranuras
    try:
        ranuras_guardadas = {
            registro["slot"]: registro
            for registro in almacen_guardados.listar()
        }
        estado_ranuras = "Ranuras sincronizadas con MySQL."
    except Exception as error:
        ranuras_guardadas = {}
        estado_ranuras = f"Error MySQL: {error}"


# Verifica la forma y rangos mínimos del progreso antes de aplicarlo al juego.
def validar_progreso_guardado(progreso):
    if not isinstance(progreso, dict) or progreso.get("version") != 1:
        raise ValueError("El guardado no tiene un formato compatible.")
    zonas = progreso.get("zonas_completadas")
    vida = progreso.get("vida")
    pociones = progreso.get("pociones")
    mejoras = progreso.get("mejoras")
    posicion = progreso.get("posicion")
    if type(zonas) is not int or not 0 <= zonas <= len(ZONAS):
        raise ValueError("El guardado contiene un avance de zonas invalido.")
    if type(vida) is not int or not 1 <= vida <= VIDA_JUGADOR:
        raise ValueError("El guardado contiene una vida invalida.")
    if type(pociones) is not int or not 0 <= pociones <= 999:
        raise ValueError("El guardado contiene una cantidad de pociones invalida.")
    if posicion is not None and (
        not isinstance(posicion, list)
        or len(posicion) != 2
        or any(type(coordenada) is not int for coordenada in posicion)
        or not 0 <= posicion[0] < MUNDO_ANCHO
        or not 0 <= posicion[1] < MUNDO_ALTO
    ):
        raise ValueError("El guardado contiene una posicion invalida.")
    puntuacion = progreso.get("puntuacion", 0)
    bestscore = progreso.get("bestscore", puntuacion)
    if type(puntuacion) is not int or not 0 <= puntuacion <= 1_000_000_000_000:
        raise ValueError("El guardado contiene una puntuacion invalida.")
    if type(bestscore) is not int or not puntuacion <= bestscore <= 1_000_000_000_000:
        raise ValueError("El guardado contiene un bestscore invalido.")
    poderes = {poder for poder, _, _ in BONIFICACIONES}
    if not isinstance(mejoras, dict) or set(mejoras) != poderes:
        raise ValueError("El guardado contiene mejoras invalidas.")
    if any(type(nivel) is not int or not 0 <= nivel <= MEJORAS_MAXIMAS_POR_PODER
           for nivel in mejoras.values()):
        raise ValueError("El guardado contiene niveles de mejora invalidos.")
    cofres_abiertos = progreso.get("cofres_abiertos", [])
    if (not isinstance(cofres_abiertos, list)
            or any(type(indice) is not int or not 0 <= indice < len(mapa.cofres)
                   for indice in cofres_abiertos)
            or len(set(cofres_abiertos)) != len(cofres_abiertos)):
        raise ValueError("El guardado contiene cofres abiertos invalidos.")
    return progreso


# Serializa los datos recuperables de la partida en una estructura JSON-compatible.
def capturar_progreso_guardado(partida_actual):
    progreso = {
        "version": 1,
        "zonas_completadas": sum(
            zona["estado"] == "completada" for zona in partida_actual.oleadas.zonas
        ),
        "vida": max(1, min(VIDA_JUGADOR, int(partida_actual.jugador.vida))),
        "posicion": [
            round(partida_actual.jugador.rect.centerx),
            round(partida_actual.jugador.rect.centery),
        ],
        "pociones": max(0, min(999, int(partida_actual.jugador.pociones))),
        "puntuacion": max(0, int(partida_actual.puntuacion)),
        "bestscore": max(int(partida_actual.bestscore), int(partida_actual.puntuacion)),
        "mejoras": dict(partida_actual.jugador.bonificaciones),
        "cofres_abiertos": [
            indice for indice, cofre in enumerate(mapa.cofres) if cofre.abierto
        ],
    }
    return validar_progreso_guardado(progreso)


# Restaura el progreso validado en mapa, jugador, oleadas y puntuación.
def aplicar_progreso_guardado(partida_actual, progreso):
    validar_progreso_guardado(progreso)
    zonas_completadas = progreso["zonas_completadas"]
    zonas_terminadas = partida_actual.oleadas.zonas[:zonas_completadas]
    for zona in zonas_terminadas:
        zona["estado"] = "completada"
        mapa.abrir_puertas(zona["puertas"])
    partida_actual.recompensas_entregadas = zonas_completadas
    partida_actual.jugador.vida = progreso["vida"]
    partida_actual.jugador.vida_visible = float(progreso["vida"])
    if "posicion" in progreso:
        partida_actual.jugador.rect.center = progreso["posicion"]
        partida_actual.jugador.pos.update(partida_actual.jugador.rect.center)
    partida_actual.jugador.pociones = progreso["pociones"]
    partida_actual.puntuacion = progreso.get("puntuacion", 0)
    partida_actual.bestscore = progreso.get("bestscore", partida_actual.puntuacion)
    partida_actual.oleadas.puntuacion = partida_actual.puntuacion
    partida_actual.jugador.bonificaciones.update(progreso["mejoras"])
    cofres_abiertos = progreso.get("cofres_abiertos", [])
    for indice in cofres_abiertos:
        mapa.cofres[indice].abierto = True


# Guarda la partida actual en la ranura solicitada y conserva el error para mostrarlo.
def guardar_en_ranura(numero):
    global estado_ranuras, ranuras_guardadas, ranura_activa
    try:
        progreso = capturar_progreso_guardado(partida)
        almacen_guardados.guardar(numero, progreso)
        ranuras_guardadas[numero] = {
            "slot": numero,
            "payload": progreso,
            "updated_at": "Ahora",
        }
        ranura_activa = numero
        estado_ranuras = f"Partida guardada en la ranura {numero}."
    except Exception as error:
        estado_ranuras = f"No se pudo guardar en MySQL: {error}"


# Lee y valida una ranura; aplica sus datos a la partida si la carga es correcta.
def cargar_desde_ranura(numero):
    global progreso_carga_pendiente, ranura_activa, estado_ranuras
    registro = ranuras_guardadas.get(numero)
    if registro is None:
        estado_ranuras = f"La ranura {numero} esta vacia."
        return
    try:
        progreso_carga_pendiente = validar_progreso_guardado(registro["payload"])
    except (KeyError, TypeError, ValueError) as error:
        estado_ranuras = f"No se pudo cargar la ranura {numero}: {error}"
        return
    ranura_activa = numero
    iniciar_carga()


print("---------- PANTALLA DE AJUSTES Y RANURAS ----------")
# Renderiza ajustes de sonido/pantalla y acceso a las canciones y ranuras guardadas.
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
    dibujar_boton_caja("partidas guardadas", ranuras_boton)
    dibujar_boton("volver", blanco, amarillo, 790)


# Dibuja el contenido, acciones y mensajes de error de las tres ranuras.
def show_ranuras():
    dibujar_fondo()
    dibujar_texto("PARTIDAS GUARDADAS", blanco, 135)
    ayuda = fuente_peq.render(
        "Carga desde el menu; guarda desde la pausa o al terminar la partida.",
        True, (220, 220, 220),
    )
    game_surface.blit(ayuda, ayuda.get_rect(center=(width // 2, 190)))
    mouse = pos_en_juego(pygame.mouse.get_pos())
    for numero, fila in ranuras_filas.items():
        registro = ranuras_guardadas.get(numero)
        pygame.draw.rect(game_surface, (48, 40, 75), fila, border_radius=14)
        pygame.draw.rect(game_surface, (160, 145, 190), fila, 2, border_radius=14)
        game_surface.blit(
            menu_font.render(f"Ranura {numero}", True, amarillo),
            (fila.x + 26, fila.y + 18),
        )
        if registro:
            progreso = registro["payload"]
            if isinstance(progreso, dict):
                detalle = (
                    f"Zonas: {progreso.get('zonas_completadas', '?')}/{len(ZONAS)}"
                    f"    Vida: {progreso.get('vida', '?')}"
                    f"    Pociones: {progreso.get('pociones', '?')}"
                )
                detalle += (
                    f"    Score: {progreso.get('puntuacion', 0)}"
                    f"    Best: {progreso.get('bestscore', progreso.get('puntuacion', 0))}"
                )
                subtitulo = f"{detalle}    Guardado: {registro.get('updated_at', '')}"
            else:
                subtitulo = "Guardado invalido"
        else:
            subtitulo = "Vacia"
        texto = renderizar_texto_ajustado(subtitulo, fuente_peq, blanco, 790)
        game_surface.blit(texto, (fila.x + 28, fila.y + 67))
        se_puede_cargar = (
            registro is not None and isinstance(registro.get("payload"), dict) and not JUGAR
        )
        se_puede_guardar = JUGAR and (PAUSA or partida.terminada)
        for rect, etiqueta, habilitado in (
            (ranuras_cargar[numero], "Cargar", se_puede_cargar),
            (ranuras_guardar[numero], "Guardar", se_puede_guardar),
        ):
            color = (65, 125, 95) if habilitado else (65, 65, 75)
            if rect.collidepoint(mouse) and habilitado:
                color = (90, 165, 120)
            pygame.draw.rect(game_surface, color, rect, border_radius=10)
            pygame.draw.rect(game_surface, (205, 205, 215), rect, 2, border_radius=10)
            etiqueta_img = fuente_peq.render(etiqueta, True, blanco)
            game_surface.blit(etiqueta_img, etiqueta_img.get_rect(center=rect.center))
    mensaje = renderizar_texto_ajustado(
        estado_ranuras, fuente_peq,
        (255, 170, 135) if "Error" in estado_ranuras or "No se pudo" in estado_ranuras else blanco,
        width - 80,
    )
    game_surface.blit(mensaje, mensaje.get_rect(center=(width // 2, 700)))
    dibujar_boton("volver", blanco, amarillo, 770)


# Calcula las filas de la lista de canciones visibles segun el desplazamiento.
def filas_visibles():
    fin = min(len(canciones), scroll + FILAS_VISIBLES)
    return [(i, pygame.Rect(350, 230 + v * 62, 850, 52)) for v, i in enumerate(range(scroll, fin))]


# Rectangulo de la casilla de activar/desactivar una cancion.
def rect_check(fila):
    return pygame.Rect(fila.x + 14, fila.centery - 16, 32, 32)


# Rectangulo del boton 'sonar ahora' de una fila.
def rect_sonar(fila):
    return pygame.Rect(fila.right - 170, fila.y + 6, 160, 40)


print("---------- PANTALLA Y CONTROLES DE MUSICA ----------")
# Muestra pistas seleccionables, estado de reproducción y controles de navegación.
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
        caja = rect_check(fila)
        pygame.draw.rect(game_surface, blanco, caja, width=3, border_radius=6)
        if activas[ruta]:
            pygame.draw.rect(game_surface, (60, 200, 110), caja.inflate(-12, -12), border_radius=4)
        zona = rect_sonar(fila)
        nombre = renderizar_texto_ajustado(
            nombre_cancion(ruta), fuente_peq, amarillo if sonando_ahora else blanco,
            zona.x - (fila.x + 70) - 16,
        )
        game_surface.blit(nombre, nombre.get_rect(midleft=(fila.x + 70, fila.centery)))
        hover = zona.collidepoint(mouse)
        pygame.draw.rect(game_surface, (90, 80, 140) if hover else (55, 50, 90), zona, border_radius=8)
        txt = fuente_peq.render("sonar ahora", True, amarillo if hover else blanco)
        game_surface.blit(txt, txt.get_rect(center=zona.center))

    if len(canciones) > FILAS_VISIBLES:
        pista = fuente_peq.render("(rueda del raton para ver mas)", True, (200, 200, 200))
        game_surface.blit(pista, pista.get_rect(center=(width // 2, 745)))

    dibujar_boton_caja("anterior", boton_anterior)
    dibujar_boton_caja("siguiente", boton_siguiente)
    dibujar_boton_caja("volver", boton_volver_musica)


# Ejecuta la acción asociada al elemento de música pulsado.
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


print("---------- DIBUJO, CAMARA Y COORDENADAS ----------")
# Centraliza las colisiones con el mapa y permite consultarlas antes de crearlo.
def mapa_choca(rect):
    return (mapa is not None and mapa.choca(rect)) or (partida is not None and partida.oleadas.bloquea(rect))


# Dibuja texto con contorno oscuro para mantener el contraste sobre el escenario.
def texto_borde(superficie, texto, fuente, color, pos, centrado=True):
    for dx, dy in ((-2, 0), (2, 0), (0, -2), (0, 2), (2, 2)):
        sombra = fuente.render(texto, True, (0, 0, 0))
        superficie.blit(sombra, sombra.get_rect(**({"center": (pos[0] + dx, pos[1] + dy)} if centrado else {"topleft": (pos[0] + dx, pos[1] + dy)})))
    render = fuente.render(texto, True, color)
    superficie.blit(render, render.get_rect(**({"center": pos} if centrado else {"topleft": pos})))


# Devuelve la cámara redondeada para evitar vibraciones de píxel al dibujar.
def camara_pos():
    return (round(camara.x), round(camara.y))


# Convierte la ubicación del cursor en ventana a coordenadas del mapa.
def pos_raton_mundo():
    cx, cy = camara_pos()
    mx, my = pos_en_juego(pygame.mouse.get_pos())
    return pygame.Vector2(mx + cx, my + cy)


# Centra o suaviza el seguimiento del jugador y limita la cámara al mundo.
def actualizar_camara(jugador, dt, forzar=False):
    objetivo = pygame.Vector2(jugador.rect.centerx - width / 2, jugador.rect.bottom - 90 - height / 2)
    if CAMARA_LIMITADA:
        for eje, mundo, pantalla in ((0, MUNDO_ANCHO, width), (1, MUNDO_ALTO, height)):
            if mundo <= pantalla:
                objetivo[eje] = (mundo - pantalla) / 2
            else:
                objetivo[eje] = max(0, min(objetivo[eje], mundo - pantalla))
    if forzar or CAMARA_SUAVIDAD <= 0:
        camara.update(objetivo)
    else:
        camara.update(camara + (objetivo - camara) * min(1.0, CAMARA_SUAVIDAD * dt))


# Efectos visuales y carga/escalado de sprites con cache.
print("---------- EFECTOS VISUALES Y SPRITES ----------")
def dibujar_mira(superficie):
    x, y = (int(v) for v in pos_en_juego(pygame.mouse.get_pos()))
    for color, grosor in (((0, 0, 0), 4), ((255, 255, 255), 2)):
        pygame.draw.line(superficie, color, (x - 13, y), (x - 5, y), grosor)
        pygame.draw.line(superficie, color, (x + 5, y), (x + 13, y), grosor)
        pygame.draw.line(superficie, color, (x, y - 13), (x, y - 5), grosor)
        pygame.draw.line(superficie, color, (x, y + 5), (x, y + 13), grosor)
    pygame.draw.circle(superficie, (255, 255, 255), (x, y), 2)


# Dibuja un rectángulo redondeado con alfa sin cambiar la superficie de destino.
def rect_translucido(superficie, color, alpha, rect, radio=0):
    visible = rect.clip(superficie.get_rect())
    if visible.w <= 0 or visible.h <= 0:
        return
    capa = pygame.Surface(visible.size, pygame.SRCALPHA)
    pygame.draw.rect(capa, (*color, alpha),
                     pygame.Rect(rect.x - visible.x, rect.y - visible.y, rect.w, rect.h), border_radius=radio)
    superficie.blit(capa, visible.topleft)


# Devuelve una copia de sprite cuyo canal alfa refleja el nivel solicitado.
def con_transparencia(imagen, alpha):
    copia = imagen.copy()
    copia.fill((255, 255, 255, max(0, min(255, int(alpha)))), special_flags=pygame.BLEND_RGBA_MULT)
    return copia


# Cambia el tamaño de una imagen conservando el estilo pixel art.
def escalar_imagen(imagen, escala):
    if escala == 1:
        return imagen
    tam = (max(1, round(imagen.get_width() * escala)), max(1, round(imagen.get_height() * escala)))
    return pygame.transform.scale(imagen, tam)


SPRITES_ENEMIGOS = {}
IMAGENES_PROYECTILES = {}
IMAGENES_POCIONES = {}


# Busca la ruta del sprite en las ubicaciones permitidas del proyecto.
def ruta_sprite_enemigo(nombre):
    for base in (os.getcwd(), os.path.dirname(os.path.abspath(__file__))):
        ruta = os.path.join(base, "enemigos", nombre + ".png")
        if os.path.isfile(ruta):
            return ruta
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "enemigos", nombre + ".png")


# Carga una imagen de enemigo y reutiliza la copia recortada desde una caché.
def cargar_sprite_enemigo(nombre):
    if nombre not in SPRITES_ENEMIGOS:
        ruta = ruta_sprite_enemigo(nombre)
        if not os.path.isfile(ruta):
            if nombre not in {perfil["sprite"] for perfil in ARQUETIPOS_ENEMIGO.values()}:
                raise FileNotFoundError(f"No encuentro enemigos/{nombre}.png junto a este archivo.")
            ruta = ruta_sprite_enemigo("goblin")
            print(f"Aviso: falta enemigos/{nombre}.png; usando goblin.png hasta que anadas su imagen.")
        img = pygame.image.load(ruta).convert_alpha()
        SPRITES_ENEMIGOS[nombre] = img.subsurface(img.get_bounding_rect()).copy()
    return SPRITES_ENEMIGOS[nombre]


# Carga y escala un recurso visual usado por proyectiles o ataques especiales.
def cargar_imagen_proyectil(nombre, tamano):
    clave = (nombre, tuple(tamano))
    if clave not in IMAGENES_PROYECTILES:
        ruta = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ataques", nombre)
        if not os.path.isfile(ruta):
            raise FileNotFoundError(f"No encuentro ataques/{nombre} junto a este archivo.")
        imagen = pygame.image.load(ruta).convert_alpha()
        IMAGENES_PROYECTILES[clave] = pygame.transform.smoothscale(imagen, tamano)
    return IMAGENES_PROYECTILES[clave]


# Obtiene la imagen de poción para el mundo y el HUD.
def cargar_imagen_pocion(tamano):
    clave = tuple(tamano)
    if clave not in IMAGENES_POCIONES:
        ruta = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pociones", "pocion_roja.png")
        if not os.path.isfile(ruta):
            raise FileNotFoundError("No encuentro pociones/pocion_roja.png junto a este archivo.")
        imagen = pygame.image.load(ruta).convert_alpha()
        IMAGENES_POCIONES[clave] = pygame.transform.scale(imagen, tamano)
    return IMAGENES_POCIONES[clave]


print("---------- HUD Y ANIMACIONES ----------")
# Representa vida actual y vida pendiente de animación junto al personaje.
def dibujar_barra_vida(superficie, jugador):
    x, y, ancho, alto = 20, 78, 320, 26
    frac = jugador.vida / jugador.vida_max
    visible = jugador.vida_visible / jugador.vida_max
    pygame.draw.rect(superficie, (35, 10, 14), (x, y, ancho, alto), border_radius=8)
    if visible > frac:
        pygame.draw.rect(superficie, (240, 215, 215), (x, y, int(ancho * visible), alto), border_radius=8)
    if frac > 0:
        pygame.draw.rect(superficie, (210, 40, 55), (x, y, int(ancho * frac), alto), border_radius=8)
    pygame.draw.rect(superficie, blanco, (x, y, ancho, alto), width=3, border_radius=8)
    texto = fuente_peq.render(f"VIDA {jugador.vida}/{jugador.vida_max}", True, blanco)
    superficie.blit(texto, texto.get_rect(midleft=(x + ancho + 14, y + alto // 2)))


# Lee los fotogramas de jugador y crea variantes para ambas orientaciones.
def cargar_animaciones():
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


# Dibuja la portada y las opciones principales del juego.
def show_menu():
    dibujar_fondo()
    panel = pygame.Surface((520, 460), pygame.SRCALPHA)
    pygame.draw.rect(panel, (10, 10, 30, 150), panel.get_rect(), border_radius=24)
    game_surface.blit(panel, panel.get_rect(center=(width // 2, 440)))
    y_titulo = 215 + math.sin(pygame.time.get_ticks() / 600) * 6
    sombra = titulo_font.render("DUNGEON FANTASY", True, negro)
    titulo = titulo_font.render("DUNGEON FANTASY", True, amarillo)
    game_surface.blit(sombra, sombra.get_rect(center=(width // 2 + 4, y_titulo + 4)))
    game_surface.blit(titulo, titulo.get_rect(center=(width // 2, y_titulo)))
    for op in opciones:
        dibujar_boton_caja(op["texto"], op["rect"])
    ayuda = fuente_peq.render("1 = jugar    2 = ajustes    3 = controles", True, (200, 200, 200))
    game_surface.blit(ayuda, ayuda.get_rect(center=(width // 2, height - 40)))


print("---------- CARGA DE PARTIDA Y PANTALLAS DE JUEGO ----------")
# Prepara una transición breve antes de crear una partida jugable.
def iniciar_carga():
    global JUGAR, CARGANDO, tiempo_carga_restante, PAUSA
    JUGAR = True
    CARGANDO = True
    PAUSA = False
    tiempo_carga_restante = TIEMPO_CARGA


# Actualiza y dibuja la pantalla de carga, avanzando hacia el inicio de partida.
def show_carga(dt):
    global CARGANDO, tiempo_carga_restante, partida, progreso_carga_pendiente
    tiempo_carga_restante = max(0.0, tiempo_carga_restante - dt)
    progreso = 1 - tiempo_carga_restante / TIEMPO_CARGA

    dibujar_fondo()
    panel = pygame.Surface((720, 340), pygame.SRCALPHA)
    pygame.draw.rect(panel, (10, 10, 30, 205), panel.get_rect(), border_radius=26)
    pygame.draw.rect(panel, (150, 150, 190, 180), panel.get_rect(), 2, border_radius=26)
    game_surface.blit(panel, panel.get_rect(center=(width // 2, height // 2)))

    titulo = titulo_font.render("CARGANDO", True, amarillo)
    game_surface.blit(titulo, titulo.get_rect(center=(width // 2, height // 2 - 82)))
    texto_borde(game_surface, "Preparando el mundo...", menu_font, blanco,
                (width // 2, height // 2 - 14))

    barra = pygame.Rect(width // 2 - 250, height // 2 + 38, 500, 28)
    pygame.draw.rect(game_surface, (35, 35, 55), barra, border_radius=12)
    relleno = barra.copy()
    relleno.width = int(barra.width * progreso)
    if relleno.width > 0:
        pygame.draw.rect(game_surface, (75, 175, 220), relleno, border_radius=12)
    pygame.draw.rect(game_surface, blanco, barra, 2, border_radius=12)
    porcentaje = fuente_peq.render(f"{int(progreso * 100)}%", True, blanco)
    game_surface.blit(porcentaje, porcentaje.get_rect(center=(width // 2, height // 2 + 98)))

    if tiempo_carga_restante <= 0:
        partida = Partida()
        if progreso_carga_pendiente is not None:
            aplicar_progreso_guardado(partida, progreso_carga_pendiente)
            progreso_carga_pendiente = None
        CARGANDO = False
        siguiente()


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
    ("Beber pocion (+30 vida) / abrir cofre", "Q / F"),
    ("Pausa", "Esc"),
    ("Ver hitboxes", "F3"),
    ("Bloquear / ocultar cursor", "Tab"),
    ("Activar modo berserker (con mejora)", "V"),
    ("Reiniciar", "Enter (al morir o ganar)"),
]


# Presenta el listado de controles conservando el fondo de pausa si aplica.
def show_controles():
    if PAUSA and captura is not None:
        game_surface.blit(captura, (0, 0))
        game_surface.blit(velo, (0, 0))
    else:
        dibujar_fondo()
    panel = pygame.Surface((960, 780), pygame.SRCALPHA)
    pygame.draw.rect(panel, (10, 10, 30, 170), panel.get_rect(), border_radius=24)
    game_surface.blit(panel, panel.get_rect(center=(width // 2, 480)))
    dibujar_texto("CONTROLES", blanco, 120)
    for i, (accion, tecla) in enumerate(LISTA_CONTROLES):
        y = 185 + i * 40
        a = fuente_peq.render(accion, True, amarillo)
        t = fuente_peq.render(tecla, True, blanco)
        game_surface.blit(a, a.get_rect(midright=(width // 2 - 20, y)))
        game_surface.blit(t, t.get_rect(midleft=(width // 2 + 20, y)))
    dibujar_boton_caja("volver", boton_volver_controles)


# Dibuja la pantalla de pausa sobre la imagen congelada de la partida.
def show_pausa():
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


print("---------- EVENTOS, CURSOR Y NAVEGACION ----------")
# Procesa teclado, ratón y ventanas y traduce los eventos a estados de interfaz/juego.
def manejar_eventos():
    global RUN, JUGAR, AJUSTES, MUSICA, PAUSA, CONTROLES, MOSTRAR_HITBOX, MOSTRAR_HUD
    global MOSTRAR_CONTROLES, CURSOR_BLOQUEADO, RANURAS, estado_ranuras
    global captura, scroll, arrastrando, partida
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUN = False
        if CARGANDO:
            continue
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F4 and JUGAR and not PAUSA:
                MOSTRAR_HUD = not MOSTRAR_HUD
            if event.key == pygame.K_h and JUGAR and not PAUSA:
                MOSTRAR_CONTROLES = not MOSTRAR_CONTROLES
            if (event.key == pygame.K_f and JUGAR and not PAUSA
                    and not partida.bonificacion_pendiente and not partida.terminada):
                partida.abrir_cofre()
            if partida.bonificacion_pendiente and event.key in (pygame.K_1, pygame.K_2, pygame.K_3):
                partida.elegir_bonificacion(event.key - pygame.K_1)
            if event.key == pygame.K_F3:
                MOSTRAR_HITBOX = not MOSTRAR_HITBOX
            if event.key == pygame.K_TAB:
                CURSOR_BLOQUEADO = not CURSOR_BLOQUEADO
            if event.key == pygame.K_RETURN and JUGAR and not PAUSA and partida.terminada:
                partida = Partida()
            if event.key == pygame.K_ESCAPE:
                if CONTROLES:
                    CONTROLES = False
                elif RANURAS:
                    RANURAS = False
                elif MUSICA:
                    MUSICA = False
                elif AJUSTES:
                    AJUSTES = False
                elif JUGAR and PAUSA:
                    PAUSA = False
                    partida.jugador.enfriamiento = 0.3
                elif JUGAR and partida.bonificacion_pendiente:
                    pass
                elif JUGAR:
                    audio_acciones.detener("pasos_caminar", "pasos_correr")
                    captura = game_surface.copy()
                    PAUSA = True
                else:
                    RUN = False
            if not JUGAR and not AJUSTES and not CONTROLES:
                if event.key == pygame.K_1:
                    iniciar_carga()
                elif event.key == pygame.K_2:
                    AJUSTES = True
                elif event.key == pygame.K_3:
                    CONTROLES = True
        if event.type == pygame.MOUSEWHEEL and AJUSTES and MUSICA:
            maximo = max(0, len(canciones) - FILAS_VISIBLES)
            scroll = max(0, min(maximo, scroll - event.y))
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and (
                not JUGAR or PAUSA or partida.bonificacion_pendiente or partida.terminada or RANURAS):
            click = pos_en_juego(event.pos)
            if CONTROLES:
                if boton_volver_controles.collidepoint(click):
                    CONTROLES = False
            elif RANURAS:
                if zona_boton("volver", 770).collidepoint(click):
                    RANURAS = False
                else:
                    for numero in (1, 2, 3):
                        if (ranuras_guardar[numero].collidepoint(click) and JUGAR
                                and (PAUSA or partida.terminada)):
                            guardar_en_ranura(numero)
                            break
                        if ranuras_cargar[numero].collidepoint(click) and not JUGAR:
                            cargar_desde_ranura(numero)
                            if progreso_carga_pendiente is not None:
                                RANURAS = False
                                AJUSTES = False
                            break
            elif JUGAR and partida.bonificacion_pendiente:
                for i, tarjeta in enumerate(partida.tarjetas_bonificacion):
                    if tarjeta.collidepoint(click):
                        partida.elegir_bonificacion(i)
                        break
            elif JUGAR and partida.terminada and not PAUSA:
                if boton_ranuras_final.collidepoint(click):
                    RANURAS = True
                    refrescar_ranuras()
            elif not AJUSTES and JUGAR:
                for op in opciones_pausa:
                    if op["rect"].collidepoint(click):
                        if op["modo"] == "reanudar":
                            PAUSA = False
                            partida.jugador.enfriamiento = 0.3
                        elif op["modo"] == "controles":
                            CONTROLES = True
                        elif op["modo"] == "ajustes":
                            AJUSTES = True
                        else:
                            JUGAR = False
                            PAUSA = False
                            partida = Partida()
            elif not AJUSTES:
                for op in opciones:
                    if op["rect"].collidepoint(click):
                        if op["modo"] == "ajustes":
                            AJUSTES = True
                        elif op["modo"] == "controles":
                            CONTROLES = True
                        elif op["modo"] == "salir":
                            RUN = False
                        else:
                            iniciar_carga()
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
                if ranuras_boton.collidepoint(click):
                    RANURAS = True
                    refrescar_ranuras()
                if zona_boton("volver", 790).collidepoint(click):
                    AJUSTES = False
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            arrastrando = None
    if AJUSTES and not MUSICA and arrastrando:
        barra = sliders[arrastrando]
        mx = pos_en_juego(pygame.mouse.get_pos())[0]
        ajustes[arrastrando] = max(0, min(1, (mx - barra.left) / barra.width))
        aplicar_volumen()


# Sincroniza visibilidad y captura del cursor con la opción de control del jugador.
def estado_cursor():
    oculto = (CURSOR_BLOQUEADO and JUGAR and not CARGANDO and not PAUSA and not AJUSTES
              and not RANURAS and not CONTROLES)
    pygame.mouse.set_visible(not oculto)
    pygame.event.set_grab(oculto)
    return oculto


# Ejecuta la actualización del estado activo y representa la pantalla correspondiente.
def actualizar_y_dibujar(dt):
    cursor_oculto = estado_cursor()
    if CARGANDO:
        show_carga(dt)
    elif CONTROLES:
        show_controles()
    elif RANURAS:
        show_ranuras()
    elif AJUSTES and MUSICA:
        show_musica()
    elif AJUSTES:
        show_ajustes()
    elif JUGAR and PAUSA:
        show_pausa()
    elif not JUGAR:
        show_menu()
    else:
        partida.actualizar(dt, pygame.key.get_pressed())
        partida.dibujar(game_surface, cursor_oculto)
        if ajustes["mostrar_fps"] and MOSTRAR_HUD:
            fps = menu_font.render(f"FPS: {int(reloj.get_fps())}", True, blanco)
            game_surface.blit(fps, fps.get_rect(topright=(width - 20, 12)))


# Carga los recursos, crea la partida y ejecuta el ciclo principal: eventos, musica, actualizar, dibujar.
print("---------- BUCLE PRINCIPAL ----------")
dt = 0
# Carga recursos gráficos y crea el estado inicial antes de aceptar eventos.
ANIMACIONES = cargar_animaciones()
mapa = Mapa(MAPA)
partida = Partida()
fuente_ayuda = pygame.font.Font(None, 26)
ayuda_juego = [fuente_ayuda.render(t, True, blanco) for t in (
    "WASD mover   Shift correr   Espacio saltar   R / clic der rodar   C agacharse   Q pocion (+30 vida)",
    "F abrir cofre (cerca y sin combate)   Clic izq atacar   E giro   V berserker   F3 hitboxes",
)]
aplicar_volumen()
siguiente()
while RUN:
    manejar_eventos()
    revisar_musica()
    actualizar_y_dibujar(dt)
    blit_scaled()
    pygame.display.flip()
    dt = reloj.tick(60) / 1000


pygame.quit()
sys.exit()
