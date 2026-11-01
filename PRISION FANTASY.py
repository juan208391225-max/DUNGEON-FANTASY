import math #calculos matematicos
import os  #acceder al sistema
import random   #aleatoriedad
import sys  # nuevas funciones relacionadas al sistema
import pygame  # Importa una biblioteca o clase auxiliar usada por el juego.
from guardado_mysql import MySQLSaveSlots  # Importa la base de datos
from sonidos_acciones import AudioAcciones  # Importa los sonidos


print("---------- INICIO DE PYGAME ----------")
pygame.init()  # Ejecuta la operacion del objeto o biblioteca indicada.l arranque



print("---------- 1. OLEADAS: CUANTOS ENEMIGOS SALEN, CUANTOS A LA VEZ Y QUE TAN RAPIDO ----------")

# Cada zona define el área, destino, límites de enemigos y tipos de encuentro.

ZONAS = [  # Asigna un valor a regiones y encuentros.
    {  # Completa los argumentos o datos usados por esta parte del juego.
        "nombre": "Bosque Susurrante", "casillas": (1, 1, 14, 15), "color": (255, 170, 60),  # Define nombre visible de la zona para este encuentro.
        "cerrada": False, "destino": (7, 8), "distancia_aparicion": 300,  # Define estado inicial de acceso a la zona para este encuentro.
        "enemigos_derrotar": 10, "max_vivos": 3, "intervalo_aparicion": 1.0,  # Define cantidad de enemigos a derrotar para este encuentro.
        "tipos_enemigos": ("goblin", "mago"),  # Define clases de enemigos del encuentro para este encuentro.
        "puertas": ((17, 7), (17, 8), (17, 9), (17, 10)),  # Cubre el ancho del paso y se abre al completar esta zona.
    },  # Cierra la coleccion o llamada abierta en las lineas anteriores.
    {  # Completa los argumentos o datos usados por esta parte del juego.
        "nombre": "Ruinas del Templo", "casillas": (19, 1, 31, 15), "color": (235, 70, 110),  # Define nombre visible de la zona para este encuentro.
        "cerrada": False, "destino": (25, 8), "distancia_aparicion": 300,  # Define estado inicial de acceso a la zona para este encuentro.
        "enemigos_derrotar": 12, "max_vivos": 3, "intervalo_aparicion": 0.8,  # Define cantidad de enemigos a derrotar para este encuentro.
        "tipos_enemigos": ("goblin", "mago"),  # Define clases de enemigos del encuentro para este encuentro.
        "puertas": ((34, 8),),  # Puertas de salida que se abren al completar esta zona.
    },  # Cierra la coleccion o llamada abierta en las lineas anteriores.
    {  # Completa los argumentos o datos usados por esta parte del juego.
        "nombre": "Pantano Venenoso", "casillas": (36, 1, 54, 15), "color": (70, 190, 150),  # Define nombre visible de la zona para este encuentro.
        "cerrada": False, "destino": (45, 8), "distancia_aparicion": 300,  # Define estado inicial de acceso a la zona para este encuentro.
        "enemigos_derrotar": 15, "max_vivos": 3, "intervalo_aparicion": 0.6,  # Define cantidad de enemigos a derrotar para este encuentro.
        "tipos_enemigos": ("bruja", "trol"),  # Define clases de enemigos del encuentro para este encuentro.
        "puertas": ((27, 18), (23, 21), (23, 24), (23, 27)),  # Rejas interiores que se abren al completar esta zona.
    },  # Cierra la coleccion o llamada abierta en las lineas anteriores.
    {  # Completa los argumentos o datos usados por esta parte del juego.
        "nombre": "Prision", "casillas": (19, 19, 33, 29), "color": (150, 130, 235),  # Define nombre visible de la zona para este encuentro.
        "cerrada": False, "destino": (26, 24), "distancia_aparicion": 300,  # Define estado inicial de acceso a la zona para este encuentro.
        "enemigos_derrotar": 15, "max_vivos": 4, "intervalo_aparicion": 0.5,  # Define cantidad de enemigos a derrotar para este encuentro.
        "tipos_enemigos": ("bruja", "trol"),  # Define clases de enemigos del encuentro para este encuentro.
        "reja_temporal": (24, 19, 4),  # Superpone una reja en la entrada mientras esta oleada está en curso.
        "puertas": ((36, 24), (42, 18), (46, 18), (50, 18), (41, 29), (44, 29)),  # Puertas de salida que se abren al completar esta zona.
    },  # Cierra la coleccion o llamada abierta en las lineas anteriores.
    {  # Completa los argumentos o datos usados por esta parte del juego.
        "nombre": "Arena del Carcelero", "casillas": (38, 18, 54, 29), "color": (245, 75, 45),  # Define nombre visible de la zona para este encuentro.
        "cerrada": False, "destino": (46, 24), "distancia_aparicion": 350,  # Define estado inicial de acceso a la zona para este encuentro.
        "enemigos_derrotar": 1, "max_vivos": 1, "intervalo_aparicion": 0.4,  # Define cantidad de enemigos a derrotar para este encuentro.
        "tipos_enemigos": (), "jefe": True, "sprite_jefe": "orco_jefe_de_guerra", "tipo_jefe": "orco",  # Define clases de enemigos del encuentro para este encuentro.
        "tipos_apoyo": ("lich", "espectro"), "max_apoyos": 3,  # Define clases de enemigos de apoyo para este encuentro.
        "puertas": ((56, 9),),  # Puertas de salida que se abren al completar esta zona.
    },  # Cierra la coleccion o llamada abierta en las lineas anteriores.
    {  # Completa los argumentos o datos usados por esta parte del juego.
        "nombre": "Aldea Abandonada", "casillas": (58, 2, 75, 16), "color": (150, 210, 95),  # Define nombre visible de la zona para este encuentro.
        "cerrada": False, "destino": (66, 9), "distancia_aparicion": 350,  # Define estado inicial de acceso a la zona para este encuentro.
        "enemigos_derrotar": 20, "max_vivos": 4, "intervalo_aparicion": 0.35,  # Define cantidad de enemigos a derrotar para este encuentro.
        "tipos_enemigos": ("lich", "espectro"),  # Define clases de enemigos del encuentro para este encuentro.
        "puertas": ((66, 20),),  # Puertas de salida que se abren al completar esta zona.
    },  # Cierra la coleccion o llamada abierta en las lineas anteriores.
    {  # Completa los argumentos o datos usados por esta parte del juego.
        "nombre": "Selva Antigua", "casillas": (39, 33, 57, 46), "color": (65, 185, 100),  # Define nombre visible de la zona para este encuentro.
        "cerrada": False, "destino": (48, 39), "distancia_aparicion": 350,  # Define estado inicial de acceso a la zona para este encuentro.
        "enemigos_derrotar": 25, "max_vivos": 5, "intervalo_aparicion": 0.25,  # Define cantidad de enemigos a derrotar para este encuentro.
        "tipos_enemigos": ("lich", "espectro"),  # Define clases de enemigos del encuentro para este encuentro.
        "puertas": ((58, 39),),  # Puertas de salida que se abren al completar esta zona.
    },  # Cierra la coleccion o llamada abierta en las lineas anteriores.
    {  # Completa los argumentos o datos usados por esta parte del juego.
        "nombre": "Desfiladero de la Mina", "casillas": (59, 19, 77, 32), "color": (215, 145, 80),  # Define nombre visible de la zona para este encuentro.
        "cerrada": False, "destino": (68, 25), "distancia_aparicion": 300,  # Define estado inicial de acceso a la zona para este encuentro.
        "enemigos_derrotar": 30, "max_vivos": 5, "intervalo_aparicion": 0.15,  # Define cantidad de enemigos a derrotar para este encuentro.
        "tipos_enemigos": ("lich", "espectro"),  # Define clases de enemigos del encuentro para este encuentro.
        "puertas": ((68, 33),),  # Puertas de salida que se abren al completar esta zona.
    },  # Cierra la coleccion o llamada abierta en las lineas anteriores.
    {  # Completa los argumentos o datos usados por esta parte del juego.
        "nombre": "Cumbre del Dragon", "casillas": (60, 35, 78, 46), "color": (225, 70, 65),  # Define nombre visible de la zona para este encuentro.
        "cerrada": False, "destino": (69, 40), "distancia_aparicion": 450,  # Define estado inicial de acceso a la zona para este encuentro.
        "enemigos_derrotar": 1, "max_vivos": 1, "intervalo_aparicion": 0.10,  # Define cantidad de enemigos a derrotar para este encuentro.
        "tipos_enemigos": (), "jefe": True, "sprite_jefe": "dragon", "tipo_jefe": "dragon",  # Define clases de enemigos del encuentro para este encuentro.
    },  # Cierra la coleccion o llamada abierta en las lineas anteriores.
]  # Cierra la coleccion o llamada abierta en las lineas anteriores.
# Mantiene una vista por numero de zona para consultas externas y compatibilidad.
PUERTAS_POR_OLEADA = {
    indice: zona.get("puertas", ())
    for indice, zona in enumerate(ZONAS, 1)
    if zona.get("puertas")
}
OLEADA_ENEMIGOS_BASE = 8  # Asigna un valor a OLEADA_ENEMIGOS_BASE.
OLEADA_ENEMIGOS_MAS = 6  # Asigna un valor a OLEADA_ENEMIGOS_MAS.
OLEADA_MAX_VIVOS_BASE = 3  # Asigna un valor a OLEADA_MAX_VIVOS_BASE.
OLEADA_MAX_VIVOS_MAS = 2  # Asigna un valor a OLEADA_MAX_VIVOS_MAS.
OLEADA_INTERVALO_BASE = 3.0  # Asigna un valor a OLEADA_INTERVALO_BASE.
OLEADA_INTERVALO_MENOS = 0.6  # Asigna un valor a OLEADA_INTERVALO_MENOS.
OLEADA_INTERVALO_MIN = 0.8  # Asigna un valor a OLEADA_INTERVALO_MIN.
OLEADA_ESPERA = 3.0  # Asigna un valor a OLEADA_ESPERA.
ENEMIGOS_OLEADA_AGRESIVOS = True  # Asigna un valor a ENEMIGOS_OLEADA_AGRESIVOS.
ENEMIGO_TIEMPO_APARICION = 0.6  # Asigna un valor a ENEMIGO_TIEMPO_APARICION.
OLEADA_MARGEN_ENTRADA = 40  # Asigna un valor a OLEADA_MARGEN_ENTRADA.
PUNTUACION_TIEMPO_MAX_REDUCCION = 300.0  # Asigna un valor a PUNTUACION_TIEMPO_MAX_REDUCCION.
MEJORAS_MAXIMAS_POR_PODER = 3  # Asigna un valor a MEJORAS_MAXIMAS_POR_PODER.
RETARDO_ELECCION_BONIFICACION = 1.0  # Asigna un valor a RETARDO_ELECCION_BONIFICACION.
BONIFICACIONES = (  # Asigna un valor a mejoras del jugador.
    ("viento", "Tajo de viento", "Cada pocos golpes conectados lanza un proyectil de largo alcance."),  # Continua la lista de datos de esta configuracion o llamada.
    ("dano", "Filo mejorado", "Aumenta el dano de todos tus ataques."),  # Continua la lista de datos de esta configuracion o llamada.
    ("berserker", "Modo berserker", "Pulsa V para ganar dano y velocidad, y recibir menos dano."),  # Continua la lista de datos de esta configuracion o llamada.
)  # Cierra la coleccion o llamada abierta en las lineas anteriores.

# Parámetros base compartidos por la IA, sus ventanas de ataque y los jefes.
print("---------- 2. ENEMIGOS: COMPORTAMIENTO COMPARTIDO ----------")  # Muestra un encabezado en la consola durante el arranque.
RETROCESO_ENEMIGO = 35  # Asigna un valor a RETROCESO_ENEMIGO.
TIEMPO_RETROCESO = 0.35  # Asigna un valor a TIEMPO_RETROCESO.

VEL_ENEMIGO_VAGAR = 60  # Asigna un valor a VEL_ENEMIGO_VAGAR.
RADIO_DETECCION = 380  # Asigna un valor a RADIO_DETECCION.
RADIO_PERDER = 650  # Asigna un valor a RADIO_PERDER.
RADIO_VAGAR = 260  # Asigna un valor a RADIO_VAGAR.
ENEMIGO_PREPARAR = 0.40  # Asigna un valor a ENEMIGO_PREPARAR.
ENEMIGO_GOLPE = 0.15  # Asigna un valor a ENEMIGO_GOLPE.
ENEMIGO_RECUPERAR = 0.35  # Asigna un valor a ENEMIGO_RECUPERAR.
ENEMIGO_UMBRAL_GIRO = 14  # Asigna un valor a ENEMIGO_UMBRAL_GIRO.
ENEMIGO_MIRA_A_LA_DERECHA = False  # Asigna un valor a ENEMIGO_MIRA_A_LA_DERECHA.
DANO_POR_CONTACTO = False  # Asigna un valor a DANO_POR_CONTACTO.
JEFE_ORCO_INTERVALO_ATAQUE = 3.0  # Asigna un valor a JEFE_ORCO_INTERVALO_ATAQUE.
JEFE_ORCO_APOYOS_POR_ATAQUE = 3  # Asigna un valor a JEFE_ORCO_APOYOS_POR_ATAQUE.
JEFE_ORCO_MULTIPLICADOR_VIDA = 20  # Asigna un valor a JEFE_ORCO_MULTIPLICADOR_VIDA.
JEFE_DRAGON_MULTIPLICADOR_VIDA = 80  # Asigna un valor a JEFE_DRAGON_MULTIPLICADOR_VIDA.
JEFE_DRAGON_TIEMPO_INICIAL = 0.5  # Asigna un valor a JEFE_DRAGON_TIEMPO_INICIAL.
JEFE_DRAGON_RECUPERACION_ATAQUE = 0.4  # Asigna un valor a JEFE_DRAGON_RECUPERACION_ATAQUE.
JEFE_DRAGON_INTERVALO_ATAQUE = 0.25  # Asigna un valor a JEFE_DRAGON_INTERVALO_ATAQUE.

# Valores de movimiento y daño consultados durante la simulación de cada fotograma.
print("---------- 3. JUGADOR: VIDA, VELOCIDAD, SALTO Y ATAQUES ----------")  # Muestra un encabezado en la consola durante el arranque.
VIDA_JUGADOR = 100  # Asigna un valor a vida maxima del jugador.
VEL_JUGADOR_CAMINAR = 300  # Asigna un valor a velocidad al caminar.
VEL_JUGADOR_CORRER = 520  # Asigna un valor a velocidad al correr.
VEL_JUGADOR_AGACHADO = 130  # Asigna un valor a velocidad agachado.
VEL_JUGADOR_RODAR = 620  # Asigna un valor a velocidad al rodar.
FUERZA_SALTO = 820  # Asigna un valor a impulso inicial del salto.
GRAVEDAD = 2400  # Asigna un valor a aceleracion de caida.
GRAVEDAD_GOLPE_ABAJO = 3800  # Asigna un valor a GRAVEDAD_GOLPE_ABAJO.
INVULNERABLE_TRAS_GOLPE = 1.2  # Asigna un valor a INVULNERABLE_TRAS_GOLPE.
ENFRIAMIENTO_ATAQUE = 0.1  # Asigna un valor a ENFRIAMIENTO_ATAQUE.
TIEMPO_COMBO = 0.5  # Asigna un valor a TIEMPO_COMBO.
ENFRIAMIENTO_GIRO = 5.0  # Asigna un valor a ENFRIAMIENTO_GIRO.
TIEMPO_ESPADA_EN_MANO = 3.0  # Asigna un valor a TIEMPO_ESPADA_EN_MANO.
DANO_ATAQUE = {  # Asigna un valor a danio base de los ataques.
    "atacar": 20,  # Define el dato asociado a la clave atacar.
    "atacar2": 20,  # Define el dato asociado a la clave atacar2.
    "atacar_dash": 25,  # Define el dato asociado a la clave atacar_dash.
    "agachado_atacar": 12,  # Define el dato asociado a la clave agachado_atacar.
    "atacar_abajo": 30,  # Define el dato asociado a la clave atacar_abajo.
    "atacar_giro": 40,  # Define el dato asociado a la clave atacar_giro.
}  # Cierra la coleccion o llamada abierta en las lineas anteriores.

# Las escalas convierten dimensiones de sprites y las hitboxes expresan colisiones lógicas.
print("---------- 4. TAMANOS: ESCALAS Y HITBOXES ----------")  # Muestra un encabezado en la consola durante el arranque.
ESCALA_GLOBAL = 1  # Asigna un valor a factor global de escala.
ESCALA_JUGADOR = 2  # Asigna un valor a escala visual del jugador.
ESCALA_ENEMIGOS = 5  # Asigna un valor a escala visual de los enemigos.
escala_jugador = ESCALA_JUGADOR * ESCALA_GLOBAL  # Asigna un valor a escala_jugador.
escala_enemigos = ESCALA_ENEMIGOS * ESCALA_GLOBAL  # Asigna un valor a escala_enemigos.


print("---------- HITBOXES ----------")  # Muestra un encabezado en la consola durante el arranque.
HITBOX_JUGADOR_PIES = (20, 10)  # Asigna un valor a HITBOX_JUGADOR_PIES.
HITBOX_JUGADOR_CUERPO = (28, 62)  # Asigna un valor a HITBOX_JUGADOR_CUERPO.
HITBOX_JUGADOR_CUERPO_AGACHADO = (28, 32)  # Asigna un valor a HITBOX_JUGADOR_CUERPO_AGACHADO.
HITBOX_ENEMIGO_PIES = (9, 5)  # Asigna un valor a HITBOX_ENEMIGO_PIES.
HITBOX_ENEMIGO_CUERPO = (11, 14)  # Asigna un valor a HITBOX_ENEMIGO_CUERPO.
HITBOX_ENEMIGO_ATAQUE = (9, 6)  # Asigna un valor a HITBOX_ENEMIGO_ATAQUE.
HITBOX_ENEMIGO_ATAQUE_POS = (5, 10)  # Asigna un valor a HITBOX_ENEMIGO_ATAQUE_POS.
HITBOX_ATAQUES = {  # Asigna un valor a HITBOX_ATAQUES.
    "atacar": (80, 60),  # Define el dato asociado a la clave atacar.
    "atacar2": (80, 60),  # Define el dato asociado a la clave atacar2.
    "atacar_dash": (75, 45),  # Define el dato asociado a la clave atacar_dash.
    "agachado_atacar": (55, 30),  # Define el dato asociado a la clave agachado_atacar.
    "atacar_abajo": (65, 55),  # Define el dato asociado a la clave atacar_abajo.
    "atacar_giro": (130, 75),  # Define el dato asociado a la clave atacar_giro.
}  # Cierra la coleccion o llamada abierta en las lineas anteriores.
HITBOX_ATAQUE_POS = {  # Asigna un valor a HITBOX_ATAQUE_POS.
    "atacar": (5, 55),  # Define el dato asociado a la clave atacar.
    "atacar2": (5, 60),  # Define el dato asociado a la clave atacar2.
    "atacar_dash": (5, 30),  # Define el dato asociado a la clave atacar_dash.
    "agachado_atacar": (5, 30),  # Define el dato asociado a la clave agachado_atacar.
    "atacar_abajo": (5, 30),  # Define el dato asociado a la clave atacar_abajo.
    "atacar_giro": (5, 30),  # Define el dato asociado a la clave atacar_giro.
}  # Cierra la coleccion o llamada abierta en las lineas anteriores.


# Opciones de seguimiento del jugador y límites de la cámara.
print("---------- 5. CAMARA Y MIRA ----------")  # Muestra un encabezado en la consola durante el arranque.
CAMARA_SUAVIDAD = 0  # Asigna un valor a CAMARA_SUAVIDAD.
CAMARA_LIMITADA = True  # Asigna un valor a CAMARA_LIMITADA.


# La generación del mapa utiliza estas medidas para convertir casillas en píxeles.
print("---------- 6. MAPA ----------")  # Muestra un encabezado en la consola durante el arranque.
ESCALA_TILES = 4  # Asigna un valor a escala de los tiles.
TAM_TILE = 32 * ESCALA_TILES  # Asigna un valor a tamano de casilla en pixeles.
JEFE_ALTURA_SPRITE = TAM_TILE * 2.5  # Asigna un valor a JEFE_ALTURA_SPRITE.


# Genera de forma determinista el plano del mundo, sus zonas y su decoración.
def _crear_mapa():  # Define la funcion _crear_mapa: genera las casillas, zonas, caminos y decoracion del mundo.
    ancho, alto = 80, 48  # Asigna un valor a ancho.
    celdas = [["."] * ancho for _ in range(alto)]  # Asigna un valor a rejilla de caracteres del mapa.
    reservado = [[False] * ancho for _ in range(alto)]  # Asigna un valor a casillas protegidas.
    rng = random.Random(19)  # Asigna un valor a generador aleatorio con semilla fija.
    Z = [z["casillas"] for z in ZONAS]  # Asigna un valor a Z.
    VERDES = (".", ";", ",")  # Asigna un valor a VERDES.
    lattice = {}  # Asigna un valor a cache de valores del ruido.

    # Produce valores pseudoaleatorios estables para cada punto de la cuadrícula de ruido.
    def valor(ix, iy, semilla):  # Define la funcion valor: obtiene un valor pseudoaleatorio estable.
        clave = (ix, iy, semilla)  # Asigna un valor a clave.
        if clave not in lattice:  # Comprueba una condicion que controla el bloque siguiente.
            lattice[clave] = random.Random(ix * 73856093 ^ iy * 19349663 ^ semilla * 83492791).random()  # Asigna un valor a lattice[clave].
        return lattice[clave]  # Devuelve el resultado y termina la funcion.

    # Interpola el ruido entre puntos para formar variaciones suaves del terreno.
    def ruido(x, y, escala, semilla):  # Define la funcion ruido: suaviza variaciones del terreno mediante interpolacion.
        fx, fy = x / escala, y / escala  # Asigna un valor a fx.
        ix, iy = math.floor(fx), math.floor(fy)  # Asigna un valor a ix.
        tx, ty = fx - ix, fy - iy  # Asigna un valor a tx.
        tx, ty = tx * tx * (3 - 2 * tx), ty * ty * (3 - 2 * ty)  # Asigna un valor a tx.
        a, b = valor(ix, iy, semilla), valor(ix + 1, iy, semilla)  # Asigna un valor a a.
        c, d = valor(ix, iy + 1, semilla), valor(ix + 1, iy + 1, semilla)  # Asigna un valor a c.
        return (a * (1 - tx) + b * tx) * (1 - ty) + (c * (1 - tx) + d * tx) * ty  # Devuelve el resultado y termina la funcion.

    def dentro(x, y):  # Define la funcion dentro: comprueba si una coordenada cae dentro del mapa.
        return 0 <= x < ancho and 0 <= y < alto  # Devuelve el resultado y termina la funcion.

    # Escribe un símbolo dentro del mapa y opcionalmente protege esa casilla de decorado posterior.
    def poner(x, y, ch, reservar_celda=True):  # Define la funcion poner: escribe un simbolo en una casilla.
        if dentro(x, y):  # Comprueba una condicion que controla el bloque siguiente.
            celdas[y][x] = ch  # Asigna un valor a celdas[y][x].
            if reservar_celda:  # Comprueba una condicion que controla el bloque siguiente.
                reservado[y][x] = True  # Asigna un valor a reservado[y][x].

    # Rellena un rectángulo de casillas con el símbolo indicado.
    def pintar(limites, ch, reservar_celdas=False):  # Define la funcion pintar: rellena un rectangulo de casillas.
        x0, y0, x1, y1 = limites  # Asigna un valor a x0.
        for y in range(y0, y1 + 1):  # Inicia un ciclo que procesa cada elemento indicado.
            for x in range(x0, x1 + 1):  # Inicia un ciclo que procesa cada elemento indicado.
                poner(x, y, ch, reservar_celdas)  # Escribe un simbolo en una casilla.

    # Evita que la generación aleatoria altere una estructura y su margen circundante.
    def reservar(limites, margen=0):  # Define la funcion reservar: protege casillas contra cambios aleatorios.
        x0, y0, x1, y1 = limites  # Asigna un valor a x0.
        for y in range(y0 - margen, y1 + margen + 1):  # Inicia un ciclo que procesa cada elemento indicado.
            for x in range(x0 - margen, x1 + margen + 1):  # Inicia un ciclo que procesa cada elemento indicado.
                if dentro(x, y):  # Comprueba una condicion que controla el bloque siguiente.
                    reservado[y][x] = True  # Asigna un valor a reservado[y][x].

    # Reserva un área circular para mantener despejados destinos y puntos de interés.
    def reservar_circulo(cx, cy, radio):  # Define la funcion reservar_circulo: protege un area circular.
        for y in range(int(cy - radio) - 1, int(cy + radio) + 2):  # Inicia un ciclo que procesa cada elemento indicado.
            for x in range(int(cx - radio) - 1, int(cx + radio) + 2):  # Inicia un ciclo que procesa cada elemento indicado.
                if dentro(x, y) and math.hypot(x - cx, y - cy) <= radio:  # Comprueba una condicion que controla el bloque siguiente.
                    reservado[y][x] = True  # Asigna un valor a reservado[y][x].

    # Dibuja una mancha ovalada con borde irregular controlado por ruido.
    def mancha(cx, cy, rx, ry, ch, semilla=0):  # Define la funcion mancha: dibuja una mancha de terreno o liquido.
        for y in range(int(cy - ry) - 2, int(cy + ry) + 3):  # Inicia un ciclo que procesa cada elemento indicado.
            for x in range(int(cx - rx) - 2, int(cx + rx) + 3):  # Inicia un ciclo que procesa cada elemento indicado.
                if dentro(x, y):  # Comprueba una condicion que controla el bloque siguiente.
                    d = math.hypot((x - cx) / rx, (y - cy) / ry)  # Asigna un valor a d.
                    if d <= 1.0 + 0.4 * (ruido(x, y, 2.5, 40 + semilla) - 0.5):  # Comprueba una condicion que controla el bloque siguiente.
                        poner(x, y, ch)  # Escribe un simbolo en una casilla.

    # Construye el contorno de un muro, respetando puertas, huecos y partes derruidas.
    def muro(limites, ch, huecos=(), ruina=0.0):  # Define la funcion muro: construye el contorno de un muro.
        x0, y0, x1, y1 = limites  # Asigna un valor a x0.
        huecos = set(huecos)  # Asigna un valor a huecos.
        for y in range(y0, y1 + 1):  # Inicia un ciclo que procesa cada elemento indicado.
            for x in range(x0, x1 + 1):  # Inicia un ciclo que procesa cada elemento indicado.
                if x not in (x0, x1) and y not in (y0, y1):  # Comprueba una condicion que controla el bloque siguiente.
                    continue  # Pasa a la siguiente vuelta del ciclo.
                if (x, y) in huecos:  # Comprueba una condicion que controla el bloque siguiente.
                    reservado[y][x] = True  # Asigna un valor a reservado[y][x].
                    continue  # Pasa a la siguiente vuelta del ciclo.
                esquina = x in (x0, x1) and y in (y0, y1)  # Asigna un valor a esquina.
                if ruina and not esquina and rng.random() < ruina:  # Comprueba una condicion que controla el bloque siguiente.
                    reservado[y][x] = True  # Asigna un valor a reservado[y][x].
                    continue  # Pasa a la siguiente vuelta del ciclo.
                poner(x, y, ch)  # Escribe un simbolo en una casilla.

    # Combina suelo interior, perímetro, puerta y zona protegida para crear un edificio.
    def edificio(limites, ch, suelo, puerta, puerta_ch="D"):  # Define la funcion edificio: construye suelo, paredes, puerta y margen protegido.
        x0, y0, x1, y1 = limites  # Asigna un valor a x0.
        pintar((x0 + 1, y0 + 1, x1 - 1, y1 - 1), suelo, True)  # Rellena el area del mapa.
        muro(limites, ch)  # Dibuja un muro en el area indicada.
        poner(puerta[0], puerta[1], puerta_ch)  # Escribe un simbolo en una casilla.
        reservar(limites, 1)  # Protege casillas contra cambios aleatorios.

    # Distribuye coordenadas alrededor de una elipse para colocar objetos en círculo.
    def puntos_circulo(cx, cy, radio, cantidad, fase=0.0):  # Define la funcion puntos_circulo: calcula posiciones alrededor de una elipse.
        return [(round(cx + radio * math.cos(fase + 2 * math.pi * i / cantidad)),  # Devuelve el resultado y termina la funcion.
                 round(cy + radio * math.sin(fase + 2 * math.pi * i / cantidad) * 0.8)) for i in range(cantidad)]  # Completa los argumentos o datos usados por esta parte del juego.

    # Coloca el mismo elemento en una colección de coordenadas.
    def colocar(ch, puntos):  # Define la funcion colocar: coloca un simbolo en varias coordenadas.
        for x, y in puntos:  # Inicia un ciclo que procesa cada elemento indicado.
            poner(x, y, ch)  # Escribe un simbolo en una casilla.

    # Devuelve el índice de la zona que contiene la casilla o None si está fuera de ellas.
    def zona_en(x, y):  # Define la funcion zona_en: busca que zona contiene una casilla.
        for i, (x0, y0, x1, y1) in enumerate(Z):  # Inicia un ciclo que procesa cada elemento indicado.
            if x0 <= x <= x1 and y0 <= y <= y1:  # Comprueba una condicion que controla el bloque siguiente.
                return i  # Devuelve el resultado y termina la funcion.
        return None  # Devuelve el resultado y termina la funcion.

    pintar(Z[1], "_")  # Rellena el area del mapa.
    pintar(Z[2], ",")  # Rellena el area del mapa.
    pintar(Z[3], "_")  # Rellena el area del mapa.
    pintar(Z[4], "r")  # Rellena el area del mapa.
    pintar(Z[5], ";")  # Rellena el area del mapa.
    pintar(Z[7], ":")  # Rellena el area del mapa.
    pintar(Z[8], "r")  # Rellena el area del mapa.
    for y in range(alto):  # Inicia un ciclo que procesa cada elemento indicado.
        for x in range(ancho):  # Inicia un ciclo que procesa cada elemento indicado.
            if celdas[y][x] == "." and zona_en(x, y) is None and ruido(x, y, 7.0, 3) > 0.62:  # Comprueba una condicion que controla el bloque siguiente.
                celdas[y][x] = ";"  # Asigna un valor a celdas[y][x].

    for z in ZONAS:  # Inicia un ciclo que procesa cada elemento indicado.
        reservar_circulo(z["destino"][0], z["destino"][1], 3.6)  # Protege el area circular de cambios aleatorios.

    for y in range(0, 32):  # Inicia un ciclo que procesa cada elemento indicado.
        cx = 55 + (1 if math.sin(y / 3.2) > 0.2 else 0)  # Asigna un valor a cx.
        for x in (cx, cx + 1):  # Inicia un ciclo que procesa cada elemento indicado.
            poner(x, y, "~")  # Escribe un simbolo en una casilla.
    mancha(56.5, 30.5, 3.0, 2.2, "~", 1)  # Crea un terreno o liquido irregular.
    mancha(7, 23, 5.2, 3.2, "~", 2)  # Crea un terreno o liquido irregular.
    mancha(11.5, 13, 2.2, 1.3, "~", 3)  # Crea un terreno o liquido irregular.
    mancha(73.5, 8.5, 1.8, 1.0, "~", 4)  # Crea un terreno o liquido irregular.
    mancha(54.5, 43.5, 2.3, 1.7, "~", 5)  # Crea un terreno o liquido irregular.
    mancha(39, 4, 3.2, 2.2, "v", 6)  # Crea un terreno o liquido irregular.
    mancha(51.5, 12.5, 3.0, 2.0, "v", 7)  # Crea un terreno o liquido irregular.
    mancha(45.5, 13.5, 2.5, 1.4, "v", 8)  # Crea un terreno o liquido irregular.
    mancha(53, 4, 1.3, 2.0, "v", 9)  # Crea un terreno o liquido irregular.

    CAMINOS = ((13, 7, 65, 10), (24, 9, 27, 39), (24, 21, 70, 25),  # Asigna un valor a CAMINOS.
               (48, 24, 51, 40), (65, 8, 68, 41), (50, 37, 70, 40))  # Completa los argumentos o datos usados por esta parte del juego.
    for camino in CAMINOS:  # Inicia un ciclo que procesa cada elemento indicado.
        pintar(camino, ":", True)  # Rellena el area del mapa.
    for y0, y1 in ((7, 10), (21, 25)):  # Inicia un ciclo que procesa cada elemento indicado.
        pintar((55, y0, 58, y1), "_", True)  # Rellena el area del mapa.

    for limites in ((8, 30, 23, 31), (8, 32, 9, 32), (16, 26, 17, 29), (28, 38, 31, 39), (32, 41, 33, 42)):  # Inicia un ciclo que procesa cada elemento indicado.
        pintar(limites, ":", True)  # Rellena el area del mapa.

    c0, f0, c1, f1 = Z[0]  # Asigna un valor a c0.
    edificio((2, 2, 6, 5), "d", ":", (4, 5))  # Construye un edificio y su entrada.
    colocar("C", [(5, 3)])  # Coloca elementos en las coordenadas listadas. El simbolo 'C' representa cofre.
    colocar("B", [(3, 3)])  # Coloca elementos en las coordenadas listadas. El simbolo 'B' representa barril.
    colocar("O", [(10, 9)])  # Coloca elementos en las coordenadas listadas. El simbolo 'O' representa objeto animado.
    colocar("L", [(10, 7), (12, 10), (11, 9)])  # Coloca elementos en las coordenadas listadas. El simbolo 'L' representa troncos.
    colocar("B", [(9, 10)])  # Coloca elementos en las coordenadas listadas. El simbolo 'B' representa barril.
    colocar("M", [(3, 12), (5, 13), (2, 14), (6, 11), (4, 10)])  # Coloca elementos en las coordenadas listadas. El simbolo 'M' representa hongo.
    for x, y in puntos_circulo(10, 4, 2.3, 7):  # Inicia un ciclo que procesa cada elemento indicado.
        poner(x, y, "R")  # Escribe un simbolo en una casilla.
    poner(10, 4, "p")  # Escribe un simbolo en una casilla.
    reservar_circulo(10, 4, 3.5)  # Protege el area circular de cambios aleatorios.
    reservar_circulo(7, 12, 2.5)  # Protege el area circular de cambios aleatorios.
    reservar_circulo(11.5, 13, 3.2)  # Protege el area circular de cambios aleatorios.

    muro((20, 2, 28, 6), "#", huecos=[(23, 6), (24, 6), (25, 6)], ruina=0.18)  # Dibuja el perimetro de las ruinas y deja huecos en la entrada.
    pintar((21, 3, 27, 5), "_", True)  # Rellena el area del mapa.
    colocar("S", [(24, 3)])  # Coloca elementos en las coordenadas listadas. El simbolo 'S' representa elemento de escenario.
    colocar("F", [(21, 3), (27, 3)])  # Coloca elementos en las coordenadas listadas. El simbolo 'F' representa brasero animado.
    colocar("K", [(22, 5), (26, 5)])  # Coloca elementos en las coordenadas listadas. El simbolo 'K' representa objeto de ruina.
    poner(24, 4, "p")  # Escribe un simbolo en una casilla.
    muro((29, 2, 31, 5), "k", huecos=[(30, 5)], ruina=0.3)  # Dibuja un muro en el area indicada.
    colocar("R", [(30, 3), (29, 6)])  # Coloca elementos en las coordenadas listadas. El simbolo 'R' representa roca.
    reservar((20, 2, 31, 6), 1)  # Protege casillas contra cambios aleatorios.
    for y in (11, 13, 15):  # Inicia un ciclo que procesa cada elemento indicado.
        colocar("#", [(23, y), (28, y)])  # Coloca dos columnas de muro en las filas listadas.
    for puntos in (((20, 11), (21, 11), (22, 11), (20, 12), (20, 13)), ((29, 11), (30, 11), (31, 11), (31, 12))):  # Inicia un ciclo que procesa cada elemento indicado.
        colocar("k", puntos)  # Coloca elementos en las coordenadas listadas. El simbolo 'k' representa pared de ruina.
    colocar("K", [(30, 13)])  # Coloca elementos en las coordenadas listadas. El simbolo 'K' representa objeto de ruina.
    colocar("Z", [(30, 14)])  # Coloca elementos en las coordenadas listadas. El simbolo 'Z' representa elemento de escenario.
    colocar("N", [(21, 14)])  # Coloca elementos en las coordenadas listadas. El simbolo 'N' representa objeto de ruina.
    colocar("S", [(21, 13)])  # Coloca elementos en las coordenadas listadas. El simbolo 'S' representa elemento de escenario.
    colocar("R", [(19, 15), (22, 15), (29, 15), (31, 14), (19, 6)])  # Coloca elementos en las coordenadas listadas. El simbolo 'R' representa roca.
    colocar("b", [(22, 13), (30, 12), (29, 14)])  # Coloca elementos en las coordenadas listadas. El simbolo 'b' representa huesos.

    edificio((44, 2, 50, 5), "c", "g", (47, 5))  # Construye un edificio y su entrada.
    colocar("F", [(45, 3), (49, 3)])  # Coloca elementos en las coordenadas listadas. El simbolo 'F' representa brasero animado.
    colocar("N", [(48, 4)])  # Coloca elementos en las coordenadas listadas. El simbolo 'N' representa objeto de ruina.
    colocar("J", [(46, 4), (46, 3)])  # Coloca elementos en las coordenadas listadas. El simbolo 'J' representa jarron.
    poner(47, 3, "p")  # Escribe un simbolo en una casilla.
    edificio((37, 11, 41, 14), "d", ":", (39, 14))  # Construye un edificio y su entrada.
    colocar("J", [(38, 12), (40, 12)])  # Coloca elementos en las coordenadas listadas. El simbolo 'J' representa jarron.
    colocar("B", [(38, 13)])  # Coloca elementos en las coordenadas listadas. El simbolo 'B' representa barril.
    colocar("C", [(40, 13)])  # Coloca elementos en las coordenadas listadas. El simbolo 'C' representa cofre.
    colocar("O", [(43, 12)])  # Coloca elementos en las coordenadas listadas. El simbolo 'O' representa objeto animado.
    colocar("L", [(44, 11), (42, 13)])  # Coloca elementos en las coordenadas listadas. El simbolo 'L' representa troncos.
    colocar("M", [(43, 6), (36, 6), (43, 15), (36, 9)])  # Coloca elementos en las coordenadas listadas. El simbolo 'M' representa hongo.
    colocar("R", [(48, 11), (43, 3), (41, 6)])  # Coloca elementos en las coordenadas listadas. El simbolo 'R' representa roca.
    colocar("b", [(44, 12), (43, 13), (36, 12)])  # Coloca elementos en las coordenadas listadas. El simbolo 'b' representa huesos.
    colocar("K", [(36, 14)])  # Coloca elementos en las coordenadas listadas. El simbolo 'K' representa objeto de ruina.

    muro(Z[3], "#", huecos=[(x, Z[3][1]) for x in range(24, 28)] + [(x, Z[3][3]) for x in range(24, 28)]  # Levanta los bordes de la prision y deja huecos para accesos.
         + [(Z[3][2], y) for y in range(21, 26)])  # Completa los argumentos o datos usados por esta parte del juego.
    pintar((20, 20, 32, 28), "_", True)  # Rellena el area del mapa.
    pintar((24, 19, 27, 29), ":", True)  # Rellena el area del mapa.
    pintar((24, 21, 33, 25), ":", True)  # Rellena el area del mapa.
    pintar((20, 20, 22, 22), "g", True)  # Rellena el area del mapa.
    pintar((20, 24, 22, 25), "g", True)  # Rellena el area del mapa.
    pintar((20, 27, 22, 28), "g", True)  # Rellena el area del mapa.
    colocar("#", [(23, y) for y in range(20, 29)])  # Forma una pared vertical dentro de la prision.
    colocar("#", [(x, 23) for x in range(20, 23)] + [(x, 26) for x in range(20, 23)])  # Separa las celdas con dos paredes horizontales.
    colocar("G", [(23, 21), (23, 24), (23, 27)])  # Coloca elementos en las coordenadas listadas. El simbolo 'G' representa reja desbloqueable.
    poner(21, 21, "b")  # Escribe un simbolo en una casilla.
    poner(22, 22, "x")  # Escribe un simbolo en una casilla.
    poner(20, 24, "x")  # Escribe un simbolo en una casilla.
    colocar("J", [(22, 25)])  # Coloca elementos en las coordenadas listadas. El simbolo 'J' representa jarron.
    colocar("C", [(22, 27)])  # Coloca elementos en las coordenadas listadas. El simbolo 'C' representa cofre.
    poner(21, 28, "b")  # Escribe un simbolo en una casilla.
    colocar("#", [(28, 20), (29, 20)])  # Agrega dos casillas de muro al recinto.
    colocar("F", [(30, 20), (32, 20), (32, 26), (28, 28)])  # Coloca elementos en las coordenadas listadas. El simbolo 'F' representa brasero animado.
    colocar("B", [(30, 27)])  # Coloca elementos en las coordenadas listadas. El simbolo 'B' representa barril.
    colocar("X", [(31, 28)])  # Coloca elementos en las coordenadas listadas. El simbolo 'X' representa mueble.
    colocar("C", [(29, 28)])  # Coloca elementos en las coordenadas listadas. El simbolo 'C' representa cofre.
    poner(31, 27, "Q")  # Escribe un simbolo en una casilla.
    poner(29, 26, "U")  # Escribe un simbolo en una casilla.
    colocar("x", [(30, 26), (32, 27), (28, 27)])  # Coloca elementos en las coordenadas listadas. El simbolo 'x' representa un elemento del plano.
    colocar("b", [(32, 28), (30, 28)])  # Coloca elementos en las coordenadas listadas. El simbolo 'b' representa huesos.
    reservar(Z[3], 0)  # Protege casillas contra cambios aleatorios.

    muro(Z[4], "l", huecos=[(38, y) for y in range(22, 25)] + [(54, y) for y in range(22, 25)]  # Dibuja un muro en el area indicada.
         + [(x, Z[4][3]) for x in range(48, 52)])  # Completa los argumentos o datos usados por esta parte del juego.
    pintar((39, 19, 53, 28), "r", True)  # Rellena el area del mapa.
    pintar((38, 22, 38, 24), ":", True)  # Rellena el area del mapa.
    pintar((54, 22, 54, 24), ":", True)  # Rellena el area del mapa.
    pintar((48, 29, 51, 29), ":", True)  # Rellena el area del mapa.
    colocar("l", [(39, 20), (39, 26), (53, 20), (53, 26), (43, 22), (49, 22), (43, 26), (49, 26)])  # Coloca elementos en las coordenadas listadas. El simbolo 'l' representa pared de arena.
    colocar("G", [(42, 18), (46, 18), (50, 18), (41, 29), (44, 29)])  # Coloca elementos en las coordenadas listadas. El simbolo 'G' representa reja desbloqueable.
    colocar("F", [(40, 20), (52, 20), (40, 27), (52, 27)])  # Coloca elementos en las coordenadas listadas. El simbolo 'F' representa brasero animado.
    colocar("e", [(44, 24), (48, 24), (46, 22), (46, 26)])  # Coloca elementos en las coordenadas listadas. El simbolo 'e' representa un elemento del plano.
    colocar("x", [(45, 23), (47, 25), (46, 25), (44, 25)])  # Coloca elementos en las coordenadas listadas. El simbolo 'x' representa un elemento del plano.
    colocar("b", [(47, 23), (45, 25), (42, 24), (50, 24), (41, 22), (51, 26)])  # Coloca elementos en las coordenadas listadas. El simbolo 'b' representa huesos.
    reservar(Z[4], 0)  # Protege casillas contra cambios aleatorios.

    edificio((59, 3, 63, 6), "d", ":", (61, 6))  # Construye un edificio y su entrada.
    colocar("B", [(60, 4)])  # Coloca elementos en las coordenadas listadas. El simbolo 'B' representa barril.
    colocar("J", [(62, 4)])  # Coloca elementos en las coordenadas listadas. El simbolo 'J' representa jarron.
    edificio((70, 3, 74, 6), "d", ":", (72, 6))  # Construye un edificio y su entrada.
    colocar("C", [(71, 4)])  # Coloca elementos en las coordenadas listadas. El simbolo 'C' representa cofre.
    colocar("X", [(73, 4)])  # Coloca elementos en las coordenadas listadas. El simbolo 'X' representa mueble.
    edificio((70, 11, 75, 15), "d", ":", (72, 15))  # Construye un edificio y su entrada.
    colocar("X", [(71, 12), (72, 12), (74, 12)])  # Coloca elementos en las coordenadas listadas. El simbolo 'X' representa mueble.
    colocar("B", [(71, 14)])  # Coloca elementos en las coordenadas listadas. El simbolo 'B' representa barril.
    colocar("L", [(74, 14)])  # Coloca elementos en las coordenadas listadas. El simbolo 'L' representa troncos.
    for fila, ch in ((12, "w"), (13, "z"), (14, "w"), (15, "z")):  # Inicia un ciclo que procesa cada elemento indicado.
        for x in range(59, 65):  # Inicia un ciclo que procesa cada elemento indicado.
            poner(x, fila, ch)  # Escribe un simbolo en una casilla.
    colocar("t", [(59, 11), (61, 11), (63, 11)])  # Coloca elementos en las coordenadas listadas. El simbolo 't' representa arbol.
    colocar("L", [(58, 13), (69, 16), (69, 8)])  # Coloca elementos en las coordenadas listadas. El simbolo 'L' representa troncos.
    colocar("B", [(58, 5)])  # Coloca elementos en las coordenadas listadas. El simbolo 'B' representa barril.
    colocar("R", [(60, 16), (64, 3), (68, 5)])  # Coloca elementos en las coordenadas listadas. El simbolo 'R' representa roca.
    colocar("A", [(69, 13)])  # Coloca elementos en las coordenadas listadas. El simbolo 'A' representa decoracion.
    reservar_circulo(73.5, 8.5, 3.0)  # Protege el area circular de cambios aleatorios.

    muro((40, 41, 46, 45), "k", huecos=[(46, 43), (40, 43)], ruina=0.22)  # Dibuja un muro en el area indicada.
    pintar((41, 42, 45, 44), "_", True)  # Rellena el area del mapa.
    colocar("S", [(43, 43)])  # Coloca elementos en las coordenadas listadas. El simbolo 'S' representa elemento de escenario.
    colocar("F", [(41, 42), (45, 42)])  # Coloca elementos en las coordenadas listadas. El simbolo 'F' representa brasero animado.
    poner(43, 42, "p")  # Escribe un simbolo en una casilla.
    colocar("Z", [(42, 44)])  # Coloca elementos en las coordenadas listadas. El simbolo 'Z' representa elemento de escenario.
    colocar("K", [(44, 44)])  # Coloca elementos en las coordenadas listadas. El simbolo 'K' representa objeto de ruina.
    reservar((40, 41, 46, 45), 1)  # Protege casillas contra cambios aleatorios.
    colocar("M", [(41, 35), (43, 37), (45, 34), (40, 38), (44, 39), (42, 34)])  # Coloca elementos en las coordenadas listadas. El simbolo 'M' representa hongo.
    colocar("O", [(54, 35)])  # Coloca elementos en las coordenadas listadas. El simbolo 'O' representa objeto animado.
    colocar("B", [(55, 35)])  # Coloca elementos en las coordenadas listadas. El simbolo 'B' representa barril.
    colocar("C", [(53, 36)])  # Coloca elementos en las coordenadas listadas. El simbolo 'C' representa cofre.
    colocar("L", [(55, 36), (53, 34)])  # Coloca elementos en las coordenadas listadas. El simbolo 'L' representa troncos.
    colocar("T", [(55, 33), (56, 34), (54, 33)])  # Coloca elementos en las coordenadas listadas. El simbolo 'T' representa pino.
    colocar("R", [(47, 44), (52, 41), (56, 41), (40, 40)])  # Coloca elementos en las coordenadas listadas. El simbolo 'R' representa roca.
    reservar_circulo(54.5, 43.5, 3.2)  # Protege el area circular de cambios aleatorios.

    c0, f0, c1, f1 = Z[7]  # Asigna un valor a c0.
    for x in range(c0, c1 + 1):  # Inicia un ciclo que procesa cada elemento indicado.
        grosor_norte = 3 if 71 <= x <= 75 else 1 + int(ruido(x, 0, 2.0, 11) * 2.6)  # Completa los argumentos o datos usados por esta parte del juego.
        for y in range(f0, f0 + grosor_norte):  # Inicia un ciclo que procesa cada elemento indicado.
            if not reservado[y][x]:  # Comprueba una condicion que controla el bloque siguiente.
                poner(x, y, "d")  # Escribe un simbolo en una casilla.
        for y in range(f1, f1 - 1 - int(ruido(x, 1, 2.0, 12) * 2.6), -1):  # Inicia un ciclo que procesa cada elemento indicado.
            if not reservado[y][x]:  # Comprueba una condicion que controla el bloque siguiente.
                poner(x, y, "d")  # Escribe un simbolo en una casilla.
    for y in range(f0, f1 + 1):  # Inicia un ciclo que procesa cada elemento indicado.
        for k in range(1 + int(ruido(0, y, 2.0, 13) * 2.4)):  # Inicia un ciclo que procesa cada elemento indicado.
            if not reservado[y][c0 + k]:  # Comprueba una condicion que controla el bloque siguiente.
                poner(c0 + k, y, "d")  # Escribe un simbolo en una casilla.
        for k in range(2 + int(ruido(1, y, 2.0, 14) * 1.6)):  # Inicia un ciclo que procesa cada elemento indicado.
            if not reservado[y][c1 - k]:  # Comprueba una condicion que controla el bloque siguiente.
                poner(c1 - k, y, "d")  # Escribe un simbolo en una casilla.
    for cx, cy, rx, ry, semilla in ((62.5, 28, 1.7, 1.2, 15), (72, 28.5, 2.2, 1.2, 16), (72.5, 23.5, 1.4, 0.9, 17)):  # Inicia un ciclo que procesa cada elemento indicado.
        mancha(cx, cy, rx, ry, "d", semilla)  # Crea un terreno o liquido irregular.
    poner(73, 21, "D")  # Escribe un simbolo en una casilla.
    colocar("X", [(72, 22), (75, 22)])  # Coloca elementos en las coordenadas listadas. El simbolo 'X' representa mueble.
    colocar("L", [(74, 22)])  # Coloca elementos en las coordenadas listadas. El simbolo 'L' representa troncos.
    colocar("B", [(71, 21)])  # Coloca elementos en las coordenadas listadas. El simbolo 'B' representa barril.
    colocar("R", [(61, 27), (75, 26), (69, 28), (60, 28), (64, 29), (76, 24)])  # Coloca elementos en las coordenadas listadas. El simbolo 'R' representa roca.
    colocar("b", [(66, 27), (73, 25), (62, 26)])  # Coloca elementos en las coordenadas listadas. El simbolo 'b' representa huesos.
    colocar("C", [(74, 30)])  # Coloca elementos en las coordenadas listadas. El simbolo 'C' representa cofre.
    reservar(Z[7], 0)  # Protege casillas contra cambios aleatorios.

    c0, f0, c1, f1 = Z[8]  # Asigna un valor a c0.
    pintar((c0 + 1, f0 + 1, c1 - 1, f1 - 1), "r", True)  # Rellena el area del mapa.
    for y in range(f0 + 1, f1):  # Inicia un ciclo que procesa cada elemento indicado.
        for x in range(c0 + 1, c1):  # Inicia un ciclo que procesa cada elemento indicado.
            if ruido(x, y, 3.0, 21) > 0.66:  # Comprueba una condicion que controla el bloque siguiente.
                celdas[y][x] = "o"  # Asigna un valor a celdas[y][x].
    muro(Z[8], "i", huecos=[(x, f0) for x in range(65, 69)] + [(c0, y) for y in range(37, 41)])  # Dibuja un muro en el area indicada.
    pintar((65, f0, 68, f0), ":", True)  # Rellena el area del mapa.
    pintar((c0, 37, c0, 40), ":", True)  # Rellena el area del mapa.
    colocar("i", [(61, 36), (61, 44), (77, 36), (77, 44)])  # Coloca elementos en las coordenadas listadas. El simbolo 'i' representa pared de zona.
    colocar("F", [(63, 37), (76, 37), (63, 44), (76, 44)])  # Coloca elementos en las coordenadas listadas. El simbolo 'F' representa brasero animado.
    colocar("C", [(74, 38), (75, 38), (75, 41), (74, 42), (76, 40)])  # Coloca elementos en las coordenadas listadas. El simbolo 'C' representa cofre.
    colocar("A", [(76, 38), (75, 40)])  # Coloca elementos en las coordenadas listadas. El simbolo 'A' representa decoracion.
    colocar("S", [(62, 42), (64, 36)])  # Coloca elementos en las coordenadas listadas. El simbolo 'S' representa elemento de escenario.
    colocar("R", [(66, 43), (72, 37), (72, 44), (70, 44), (66, 37), (77, 42)])  # Coloca elementos en las coordenadas listadas. El simbolo 'R' representa roca.
    colocar("b", [(65, 41), (67, 39), (71, 41), (73, 39), (70, 42), (68, 43), (73, 43), (64, 40)])  # Coloca elementos en las coordenadas listadas. El simbolo 'b' representa huesos.
    colocar("x", [(69, 42), (71, 39)])  # Coloca elementos en las coordenadas listadas. El simbolo 'x' representa un elemento del plano.
    poner(72, 42, "p")  # Escribe un simbolo en una casilla.
    reservar(Z[8], 0)  # Protege casillas contra cambios aleatorios.

    muro((3, 33, 13, 42), "c", huecos=[(8, 33), (9, 33)], ruina=0.12)  # Dibuja un muro en el area indicada.
    pintar((4, 34, 12, 41), "o", True)  # Rellena el area del mapa.
    for y in (35, 37, 39):  # Inicia un ciclo que procesa cada elemento indicado.
        for x in (5, 7, 9, 11):  # Inicia un ciclo que procesa cada elemento indicado.
            poner(x, y, rng.choice("KKSN"))  # Escribe un simbolo en una casilla.
    poner(8, 38, "p")  # Escribe un simbolo en una casilla.
    colocar("F", [(5, 41), (11, 41), (5, 34), (11, 34)])  # Coloca elementos en las coordenadas listadas. El simbolo 'F' representa brasero animado.
    colocar("b", [(6, 36), (10, 38), (8, 35), (6, 40), (10, 40)])  # Coloca elementos en las coordenadas listadas. El simbolo 'b' representa huesos.
    reservar((3, 33, 13, 42), 1)  # Protege casillas contra cambios aleatorios.

    edificio((14, 22, 18, 25), "d", ":", (16, 25))  # Construye un edificio y su entrada.
    colocar("B", [(15, 23)])  # Coloca elementos en las coordenadas listadas. El simbolo 'B' representa barril.
    colocar("J", [(17, 23)])  # Coloca elementos en las coordenadas listadas. El simbolo 'J' representa jarron.
    colocar("O", [(15, 27)])  # Coloca elementos en las coordenadas listadas. El simbolo 'O' representa objeto animado.
    colocar("L", [(13, 28), (19, 26)])  # Coloca elementos en las coordenadas listadas. El simbolo 'L' representa troncos.
    colocar("R", [(13, 20), (12, 27), (2, 26), (12, 22)])  # Coloca elementos en las coordenadas listadas. El simbolo 'R' representa roca.
    reservar_circulo(7, 23, 6.0)  # Protege el area circular de cambios aleatorios.

    edificio((32, 33, 36, 36), "d", ":", (34, 36))  # Construye un edificio y su entrada.
    colocar("C", [(33, 34)])  # Coloca elementos en las coordenadas listadas. El simbolo 'C' representa cofre.
    colocar("J", [(35, 34)])  # Coloca elementos en las coordenadas listadas. El simbolo 'J' representa jarron.
    colocar("O", [(32, 40)])  # Coloca elementos en las coordenadas listadas. El simbolo 'O' representa objeto animado.
    colocar("L", [(29, 40), (34, 41), (30, 41)])  # Coloca elementos en las coordenadas listadas. El simbolo 'L' representa troncos.
    colocar("B", [(28, 41), (34, 39)])  # Coloca elementos en las coordenadas listadas. El simbolo 'B' representa barril.
    colocar("X", [(30, 37), (35, 39)])  # Coloca elementos en las coordenadas listadas. El simbolo 'X' representa mueble.
    colocar("C", [(35, 41)])  # Coloca elementos en las coordenadas listadas. El simbolo 'C' representa cofre.
    colocar("b", [(33, 40), (31, 38), (33, 42)])  # Coloca elementos en las coordenadas listadas. El simbolo 'b' representa huesos.
    reservar_circulo(32, 40, 4.0)  # Protege el area circular de cambios aleatorios.
    edificio((30, 43, 35, 46), "#", "_", (32, 43))  # Crea un edificio de losas con paredes de piedra y puerta.
    colocar("F", [(31, 44), (34, 44)])  # Coloca elementos en las coordenadas listadas. El simbolo 'F' representa brasero animado.
    colocar("C", [(33, 45)])  # Coloca elementos en las coordenadas listadas. El simbolo 'C' representa cofre.
    colocar("S", [(31, 45)])  # Coloca elementos en las coordenadas listadas. El simbolo 'S' representa elemento de escenario.

    colocar("R", [(35, 18), (36, 27), (35, 31), (34, 20), (36, 19), (16, 3), (17, 13), (16, 12), (33, 12), (34, 12)])  # Coloca elementos en las coordenadas listadas. El simbolo 'R' representa roca.
    colocar("M", [(35, 5), (34, 13), (16, 5), (17, 12), (36, 32), (47, 31)])  # Coloca elementos en las coordenadas listadas. El simbolo 'M' representa hongo.
    colocar("R", [(60, 34), (64, 17), (70, 17), (76, 17)])  # Coloca elementos en las coordenadas listadas. El simbolo 'R' representa roca.
    colocar("C", [(77, 12)])  # Coloca elementos en las coordenadas listadas. El simbolo 'C' representa cofre.

    for x, y in ((23, 6), (28, 6), (23, 11), (28, 11), (12, 6), (12, 11), (35, 6), (35, 11), (46, 6), (46, 11),  # Inicia un ciclo que procesa cada elemento indicado.
                 (55, 6), (58, 6), (55, 11), (58, 11), (55, 20), (58, 20), (55, 26), (58, 26),  # Continua la lista de datos de esta configuracion o llamada.
                 (23, 30), (28, 30), (23, 38), (28, 38), (47, 30), (52, 30), (47, 36), (52, 41),  # Continua la lista de datos de esta configuracion o llamada.
                 (64, 7), (69, 7), (64, 11), (69, 11), (64, 27), (69, 27), (64, 33), (69, 33), (64, 42), (69, 42)):  # Inicia el bloque de instrucciones de esta estructura.
        if dentro(x, y) and celdas[y][x] in VERDES:  # Comprueba una condicion que controla el bloque siguiente.
            poner(x, y, "q")  # Escribe un simbolo en una casilla.

    DENSIDAD = {None: 0.55, 0: 0.42, 1: 0.10, 2: 0.15, 3: 0.0, 4: 0.0, 5: 0.09, 6: 0.66, 7: 0.0, 8: 0.0}  # Asigna un valor a densidad de arboles por zona.
    for y in range(alto):  # Inicia un ciclo que procesa cada elemento indicado.
        for x in range(ancho):  # Inicia un ciclo que procesa cada elemento indicado.
            if celdas[y][x] not in VERDES or reservado[y][x]:  # Comprueba una condicion que controla el bloque siguiente.
                continue  # Pasa a la siguiente vuelta del ciclo.
            zona = zona_en(x, y)  # Asigna un valor a zona.
            borde = min(x, y, ancho - 1 - x, alto - 1 - y)  # Asigna un valor a borde.
            if zona is None and borde <= 1:  # Comprueba una condicion que controla el bloque siguiente.
                p = 0.93  # Asigna un valor a p.
            elif zona is None and borde <= 3:  # Comprueba una condicion alternativa.
                p = 0.62  # Asigna un valor a p.
            else:  # Inicia la alternativa si las condiciones anteriores son falsas.
                p = DENSIDAD[zona] * (0.3 + 1.5 * ruido(x, y, 5.0, 1) ** 1.3)  # Asigna un valor a p.
            if rng.random() >= p:  # Comprueba una condicion que controla el bloque siguiente.
                continue  # Pasa a la siguiente vuelta del ciclo.
            r = rng.random()  # Asigna un valor a r.
            if zona == 2:  # Comprueba una condicion que controla el bloque siguiente.
                celdas[y][x] = "y" if r < 0.55 else ("t" if r < 0.9 else "T")  # Asigna un valor a celdas[y][x].
            elif zona == 6:  # Comprueba una condicion alternativa.
                celdas[y][x] = "T" if r < 0.58 else ("t" if r < 0.88 else "y")  # Asigna un valor a celdas[y][x].
            else:  # Inicia la alternativa si las condiciones anteriores son falsas.
                celdas[y][x] = "T" if r < 0.36 else ("t" if r < 0.76 else "y")  # Asigna un valor a celdas[y][x].

    DECORACION = {  # Asigna un valor a probabilidades de decoracion por zona.
        None: (("h", 0.07), ("f", 0.05), ("m", 0.02), ("b", 0.004)),  # Continua la lista de datos de esta configuracion o llamada.
        0: (("h", 0.10), ("f", 0.04), ("m", 0.05), ("b", 0.004)),  # Continua la lista de datos de esta configuracion o llamada.
        2: (("s", 0.05), ("j", 0.05), ("m", 0.04), ("b", 0.015)),  # Continua la lista de datos de esta configuracion o llamada.
        5: (("f", 0.22), ("h", 0.05)),  # Continua la lista de datos de esta configuracion o llamada.
        6: (("h", 0.14), ("m", 0.06), ("f", 0.02)),  # Continua la lista de datos de esta configuracion o llamada.
    }  # Cierra la coleccion o llamada abierta en las lineas anteriores.
    for y in range(alto):  # Inicia un ciclo que procesa cada elemento indicado.
        for x in range(ancho):  # Inicia un ciclo que procesa cada elemento indicado.
            if celdas[y][x] not in VERDES:  # Comprueba una condicion que controla el bloque siguiente.
                continue  # Pasa a la siguiente vuelta del ciclo.
            tabla = DECORACION.get(zona_en(x, y), ())  # Asigna un valor a tabla.
            r = rng.random()  # Asigna un valor a r.
            acumulado = 0.0  # Asigna un valor a acumulado.
            for ch, prob in tabla:  # Inicia un ciclo que procesa cada elemento indicado.
                acumulado += prob  # Asigna un valor a acumulado +.
                if r < acumulado:  # Comprueba una condicion que controla el bloque siguiente.
                    celdas[y][x] = ch  # Asigna un valor a celdas[y][x].
                    break  # Termina anticipadamente el ciclo.
    for y in range(alto):  # Inicia un ciclo que procesa cada elemento indicado.
        for x in range(ancho):  # Inicia un ciclo que procesa cada elemento indicado.
            if celdas[y][x] in VERDES and any(dentro(x + dx, y + dy) and celdas[y + dy][x + dx] in ("~", "v")  # Comprueba una condicion que controla el bloque siguiente.
                                              for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):  # Inicia un ciclo que procesa cada elemento indicado.
                if rng.random() < 0.55:  # Comprueba una condicion que controla el bloque siguiente.
                    celdas[y][x] = "j"  # Asigna un valor a celdas[y][x].

    celdas[8][7] = "P"  # Asigna un valor a celdas[8][7].
    for zona in ZONAS:  # Recorre las zonas para colocar sus puertas de salida.
        for x, y in zona.get("puertas", ()):  # Recorre solo las puertas asociadas a esta zona.
            celdas[y][x] = "G"  # Asigna un valor a celdas[y][x].
    return ["".join(fila) for fila in celdas]  # Devuelve el resultado y termina la funcion.


# El plano generado se comparte entre renderizado, navegación y zonas de oleadas.
MAPA = _crear_mapa()  # Asigna un valor a plano del mundo.

MUNDO_ANCHO = len(MAPA[0]) * TAM_TILE  # Asigna un valor a ancho total del mundo.
MUNDO_ALTO = len(MAPA) * TAM_TILE  # Asigna un valor a alto total del mundo.

print("---------- FIN DE LA CONFIGURACION ----------")  # Muestra un encabezado en la consola durante el arranque.

print("---------- ESTADO DE LA PARTIDA Y RECURSOS GRAFICOS ----------")  # Muestra un encabezado en la consola durante el arranque.
# Estados de interfaz y referencias globales compartidas entre el bucle y las pantallas.
print("---------- ESTADO INTERNO, COLORES Y FUENTES ----------")  # Muestra un encabezado en la consola durante el arranque.
blanco = (255, 255, 255)  # Asigna un valor a blanco.
negro = (0, 0, 0)  # Asigna un valor a negro.
amarillo = (255, 220, 80)  # Asigna un valor a amarillo.
width = 1549  # Asigna un valor a width.
height = 900  # Asigna un valor a height.
RUN = True  # Asigna un valor a RUN.
JUGAR = False  # Asigna un valor a JUGAR.
CARGANDO = False  # Asigna un valor a CARGANDO.
TIEMPO_CARGA = 1.8  # Asigna un valor a TIEMPO_CARGA.
tiempo_carga_restante = 0.0  # Asigna un valor a tiempo_carga_restante.
AJUSTES = False  # Asigna un valor a AJUSTES.
MUSICA = False  # Asigna un valor a MUSICA.
PAUSA = False  # Asigna un valor a PAUSA.
RANURAS = False  # Asigna un valor a RANURAS.
CONTROLES = False  # Asigna un valor a CONTROLES.
MOSTRAR_HITBOX = False  # Asigna un valor a MOSTRAR_HITBOX.
MOSTRAR_HUD = True  # Asigna un valor a MOSTRAR_HUD.
MOSTRAR_CONTROLES = True  # Asigna un valor a MOSTRAR_CONTROLES.
CURSOR_BLOQUEADO = False  # Asigna un valor a CURSOR_BLOQUEADO.
camara = pygame.Vector2(0, 0)  # Asigna un valor a camara.
mapa = None  # Asigna un valor a mapa.
partida = None  # Asigna un valor a partida.
captura = None  # Asigna un valor a captura.
menu_font = pygame.font.Font(None, 45)  # Asigna un valor a menu_font.
titulo_font = pygame.font.Font(None, 110)  # Asigna un valor a titulo_font.
fuente_peq = pygame.font.Font(None, 34)  # Asigna un valor a fuente_peq.
reloj = pygame.time.Clock()  # Asigna un valor a reloj.

print("---------- MUSICA: LISTA DE REPRODUCCION ----------")  # Muestra un encabezado en la consola durante el arranque.
MUSICA_EXT = (".mp3", ".ogg", ".wav")  # Asigna un valor a MUSICA_EXT.


# Descubre las pistas reproducibles en la carpeta de música del proyecto.
def buscar_canciones():  # Define la funcion buscar_canciones: busca pistas compatibles en la carpeta de musica.
    rutas = []  # Asigna un valor a rutas.
    if os.path.isdir("musica"):  # Comprueba una condicion que controla el bloque siguiente.
        for n in sorted(os.listdir("musica")):  # Inicia un ciclo que procesa cada elemento indicado.
            if n.lower().endswith(MUSICA_EXT):  # Comprueba una condicion que controla el bloque siguiente.
                rutas.append(os.path.join("musica", n))  # Completa los argumentos o datos usados por esta parte del juego.
    return rutas  # Devuelve el resultado y termina la funcion.


canciones = buscar_canciones()  # Asigna un valor a canciones.
activas = {c: True for c in canciones}  # Asigna un valor a activas.
actual = -1  # Asigna un valor a actual.
scroll = 0  # Asigna un valor a scroll.
FILAS_VISIBLES = 7  # Asigna un valor a FILAS_VISIBLES.

ajustes = {"musica": 0.0, "efectos": 0.5, "pantalla_completa": True, "mostrar_fps": False}  # Asigna un valor a ajustes.
audio_acciones = AudioAcciones(  # Asigna un valor a audio_acciones.
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "sonidos")  # Ejecuta la operacion del objeto o biblioteca indicada.
)  # Cierra la coleccion o llamada abierta en las lineas anteriores.
audio_acciones.cargar()  # Ejecuta la operacion del objeto o biblioteca indicada.

SONIDOS_ATAQUE = (  # Asigna un valor a SONIDOS_ATAQUE.
    "ataque_espada",  # Continua la lista de datos de esta configuracion o llamada.
    "ataque_embestida",  # Continua la lista de datos de esta configuracion o llamada.
    "ataque_aereo",  # Continua la lista de datos de esta configuracion o llamada.
    "ataque_giro",  # Continua la lista de datos de esta configuracion o llamada.
    "ataque_enemigo_cuerpo",  # Continua la lista de datos de esta configuracion o llamada.
    "ataque_enemigo_distancia",  # Continua la lista de datos de esta configuracion o llamada.
    "ataque_jefe",  # Continua la lista de datos de esta configuracion o llamada.
)  # Cierra la coleccion o llamada abierta en las lineas anteriores.


# Aplica el volumen de efectos y delega la reproducción al gestor de sonidos.
def reproducir_sonido(nombre, bloquear_si_activo=(), reemplazar=()):  # Define la funcion reproducir_sonido: agrupa instrucciones relacionadas.
    return audio_acciones.reproducir(  # Devuelve el resultado y termina la funcion.
        nombre,  # Continua la lista de datos de esta configuracion o llamada.
        ajustes["efectos"],  # Continua la lista de datos de esta configuracion o llamada.
        bloquear_si_activo=bloquear_si_activo,  # Asigna un valor a bloquear_si_activo.
        reemplazar=reemplazar,  # Asigna un valor a reemplazar.
    )  # Cierra la coleccion o llamada abierta en las lineas anteriores.


print("---------- GUARDADO DE PARTIDAS ----------")  # Muestra un encabezado en la consola durante el arranque.
almacen_guardados = MySQLSaveSlots()  # Asigna un valor a almacen_guardados.
ranuras_guardadas = {}  # Asigna un valor a ranuras_guardadas.
estado_ranuras = ""  # Asigna un valor a estado_ranuras.
ranura_activa = None  # Asigna un valor a ranura_activa.
progreso_carga_pendiente = None  # Asigna un valor a progreso_carga_pendiente.
ranuras_boton = pygame.Rect(0, 0, 380, 56)  # Asigna un valor a ranuras_boton.
ranuras_boton.center = (width // 2, 690)  # Asigna un valor a ranuras_boton.center.
ranuras_filas = {  # Asigna un valor a ranuras_filas.
    numero: pygame.Rect(150, 240 + (numero - 1) * 145, 1300, 112)  # Completa los argumentos o datos usados por esta parte del juego.
    for numero in (1, 2, 3)  # Inicia un ciclo que procesa cada elemento indicado.
}  # Cierra la coleccion o llamada abierta en las lineas anteriores.
ranuras_cargar = {  # Asigna un valor a ranuras_cargar.
    numero: pygame.Rect(1000, 270 + (numero - 1) * 145, 180, 54)  # Completa los argumentos o datos usados por esta parte del juego.
    for numero in (1, 2, 3)  # Inicia un ciclo que procesa cada elemento indicado.
}  # Cierra la coleccion o llamada abierta en las lineas anteriores.
ranuras_guardar = {  # Asigna un valor a ranuras_guardar.
    numero: pygame.Rect(1200, 270 + (numero - 1) * 145, 180, 54)  # Completa los argumentos o datos usados por esta parte del juego.
    for numero in (1, 2, 3)  # Inicia un ciclo que procesa cada elemento indicado.
}  # Cierra la coleccion o llamada abierta en las lineas anteriores.
boton_ranuras_final = pygame.Rect(0, 0, 380, 56)  # Asigna un valor a boton_ranuras_final.
boton_ranuras_final.center = (width // 2, 205)  # Asigna un valor a boton_ranuras_final.center.
sliders = {  # Asigna un valor a sliders.
    "musica": pygame.Rect(800, 294, 400, 12),  # Define el dato asociado a la clave musica.
    "efectos": pygame.Rect(800, 374, 400, 12),  # Define el dato asociado a la clave efectos.
}  # Cierra la coleccion o llamada abierta en las lineas anteriores.
interruptores = {  # Asigna un valor a interruptores.
    "pantalla_completa": pygame.Rect(800, 438, 120, 48),  # Define el dato asociado a la clave pantalla_completa.
    "mostrar_fps": pygame.Rect(800, 518, 120, 48),  # Define el dato asociado a la clave mostrar_fps.
}  # Cierra la coleccion o llamada abierta en las lineas anteriores.
arrastrando = None  # Asigna un valor a arrastrando.

print("---------- CONFIGURACION DE VENTANA ----------")  # Muestra un encabezado en la consola durante el arranque.

game_surface = pygame.Surface((width, height))  # Asigna un valor a game_surface.
ventana = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)  # Asigna un valor a ventana.
pygame.display.set_caption("DUNGEON FANTASY")  # Ejecuta la operacion del objeto o biblioteca indicada.


print("---------- FONDO PERSONALIZADO Y VIDEO ----------")  # Muestra un encabezado en la consola durante el arranque.
# Carga una imagen estática de menú o genera un degradado como alternativa.
def cargar_fondo():  # Define la funcion cargar_fondo: carga una imagen o genera un fondo degradado.
    carpeta_proyecto = os.path.dirname(os.path.abspath(__file__))  # Asigna un valor a carpeta_proyecto.
    for nombre in ("fondo.png", "fondo.jpg", "fondo.jpeg"):  # Inicia un ciclo que procesa cada elemento indicado.
        ruta = os.path.join(carpeta_proyecto, nombre)  # Asigna un valor a ruta.
        if os.path.exists(ruta):  # Comprueba una condicion que controla el bloque siguiente.
            img = pygame.image.load(ruta).convert()  # Asigna un valor a img.
            return pygame.transform.smoothscale(img, (width, height))  # Devuelve el resultado y termina la funcion.
    s = pygame.Surface((width, height))  # Asigna un valor a s.
    for y in range(height):  # Inicia un ciclo que procesa cada elemento indicado.
        t = y / height  # Asigna un valor a t.
        pygame.draw.line(s, (int(20 + 30 * t), int(15 + 10 * t), int(50 + 60 * t)), (0, y), (width, y))  # Ejecuta la operacion del objeto o biblioteca indicada.
    return s  # Devuelve el resultado y termina la funcion.


class FondoVideo:  # Define la clase FondoVideo: agrupa instrucciones relacionadas.
    # Gestiona la lectura cíclica y conversión de fotogramas de un vídeo para Pygame.
    def __init__(self, ruta):  # Define la funcion __init__: agrupa instrucciones relacionadas.
        import cv2  # Importa una biblioteca o clase auxiliar usada por el juego.

        self.cv2 = cv2  # Ejecuta la operacion del objeto o biblioteca indicada.
        self.captura = cv2.VideoCapture(ruta)  # Ejecuta la operacion del objeto o biblioteca indicada.
        if not self.captura.isOpened():  # Comprueba una condicion que controla el bloque siguiente.
            self.captura.release()  # Ejecuta la operacion del objeto o biblioteca indicada.
            raise RuntimeError(f"No se pudo abrir el video de fondo: {ruta}")  # Informa del error y detiene esta operacion.
        fps = self.captura.get(cv2.CAP_PROP_FPS)  # Asigna un valor a fps.
        self.intervalo = 1.0 / fps if fps > 0 else 1.0 / 30  # Ejecuta la operacion del objeto o biblioteca indicada.
        self.siguiente_frame = 0  # Ejecuta la operacion del objeto o biblioteca indicada.
        self.superficie = None  # Ejecuta la operacion del objeto o biblioteca indicada.
        self._leer_frame()  # Ejecuta la operacion del objeto o biblioteca indicada.

    # Lee el siguiente fotograma; al llegar al final, reinicia el vídeo desde el comienzo.
    def _leer_frame(self):  # Define la funcion _leer_frame: agrupa instrucciones relacionadas.
        correcto, frame = self.captura.read()  # Asigna un valor a correcto.
        if not correcto:  # Comprueba una condicion que controla el bloque siguiente.
            self.captura.set(self.cv2.CAP_PROP_POS_FRAMES, 0)  # Ejecuta la operacion del objeto o biblioteca indicada.
            correcto, frame = self.captura.read()  # Asigna un valor a correcto.
        if not correcto:  # Comprueba una condicion que controla el bloque siguiente.
            raise RuntimeError("No se pudo leer un fotograma de fondo.mp4")  # Informa del error y detiene esta operacion.
        frame = self.cv2.resize(frame, (width, height), interpolation=self.cv2.INTER_AREA)  # Asigna un valor a frame.
        frame = self.cv2.cvtColor(frame, self.cv2.COLOR_BGR2RGB)  # Asigna un valor a frame.
        self.superficie = pygame.image.frombuffer(frame.tobytes(), (width, height), "RGB").copy()  # Ejecuta la operacion del objeto o biblioteca indicada.
        self.siguiente_frame = pygame.time.get_ticks() + self.intervalo * 1000  # Ejecuta la operacion del objeto o biblioteca indicada.

    # Actualiza el fotograma cuando vence su intervalo y lo dibuja en la superficie.
    def dibujar(self, superficie):  # Define la funcion dibujar: dibuja el elemento en pantalla.
        if pygame.time.get_ticks() >= self.siguiente_frame:  # Comprueba una condicion que controla el bloque siguiente.
            self._leer_frame()  # Ejecuta la operacion del objeto o biblioteca indicada.
        superficie.blit(self.superficie, (0, 0))  # Completa los argumentos o datos usados por esta parte del juego.

    def cerrar(self):  # Define la funcion cerrar: agrupa instrucciones relacionadas.
        self.captura.release()  # Ejecuta la operacion del objeto o biblioteca indicada.


fondo_menu = cargar_fondo()  # Asigna un valor a fondo_menu.
video_fondo = None  # Asigna un valor a video_fondo.
ruta_video_fondo = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fondo.mp4")  # Asigna un valor a ruta_video_fondo.
if os.path.isfile(ruta_video_fondo):  # Comprueba una condicion que controla el bloque siguiente.
    try:  # Inicia el bloque de instrucciones de esta estructura.
        video_fondo = FondoVideo(ruta_video_fondo)  # Asigna un valor a video_fondo.
    except (ImportError, OSError, RuntimeError) as error:  # Inicia el bloque de instrucciones de esta estructura.
        print(f"Aviso: se usara el fondo estatico; {error}")  # Muestra un encabezado en la consola durante el arranque.
velo = pygame.Surface((width, height), pygame.SRCALPHA)  # Asigna un valor a velo.
velo.fill((0, 0, 0, 120))  # Completa los argumentos o datos usados por esta parte del juego.

opciones = []  # Asigna un valor a opciones.
for texto, y, valor in [  # Inicia un ciclo que procesa cada elemento indicado.
    ("jugar", 390, "jugar"),  # Continua la lista de datos de esta configuracion o llamada.
    ("controles", 465, "controles"),  # Continua la lista de datos de esta configuracion o llamada.
    ("ajustes", 540, "ajustes"),  # Continua la lista de datos de esta configuracion o llamada.
    ("salir", 615, "salir"),  # Continua la lista de datos de esta configuracion o llamada.
]:  # Inicia el bloque de instrucciones de esta estructura.
    rect = pygame.Rect(0, 0, 340, 62)  # Asigna un valor a rect.
    rect.center = (width // 2, y)  # Asigna un valor a rect.center.
    opciones.append({"texto": texto, "rect": rect, "modo": valor})  # Completa los argumentos o datos usados por esta parte del juego.

boton_canciones = pygame.Rect(0, 0, 380, 56)  # Asigna un valor a boton_canciones.
boton_canciones.center = (width // 2, 600)  # Asigna un valor a boton_canciones.center.
boton_anterior = pygame.Rect(0, 0, 260, 56)  # Asigna un valor a boton_anterior.
boton_anterior.center = (width // 2 - 200, 690)  # Asigna un valor a boton_anterior.center.
boton_siguiente = pygame.Rect(0, 0, 260, 56)  # Asigna un valor a boton_siguiente.
boton_siguiente.center = (width // 2 + 200, 690)  # Asigna un valor a boton_siguiente.center.
boton_volver_musica = pygame.Rect(0, 0, 260, 56)  # Asigna un valor a boton_volver_musica.
boton_volver_musica.center = (width // 2, 840)  # Asigna un valor a boton_volver_musica.center.
boton_volver_controles = pygame.Rect(0, 0, 260, 56)  # Asigna un valor a boton_volver_controles.
boton_volver_controles.center = (width // 2, 840)  # Asigna un valor a boton_volver_controles.center.

opciones_pausa = []  # Asigna un valor a opciones_pausa.
for texto, y, valor in [  # Inicia un ciclo que procesa cada elemento indicado.
    ("reanudar", 400, "reanudar"),  # Continua la lista de datos de esta configuracion o llamada.
    ("controles", 470, "controles"),  # Continua la lista de datos de esta configuracion o llamada.
    ("ajustes", 540, "ajustes"),  # Continua la lista de datos de esta configuracion o llamada.
    ("menu principal", 610, "menu"),  # Continua la lista de datos de esta configuracion o llamada.
]:  # Inicia el bloque de instrucciones de esta estructura.
    rect = pygame.Rect(0, 0, 400, 62)  # Asigna un valor a rect.
    rect.center = (width // 2, y)  # Asigna un valor a rect.center.
    opciones_pausa.append({"texto": texto, "rect": rect, "modo": valor})  # Completa los argumentos o datos usados por esta parte del juego.

print("------------CLASES U OBJETOS------------")  # Muestra un encabezado en la consola durante el arranque.

print("---------- CLASES DEL MAPA ----------")  # Muestra un encabezado en la consola durante el arranque.
class Prop:  # Define la clase Prop: representa un objeto del escenario con colision opcional.
    # Elemento visual del mapa, anclado por los pies y opcionalmente animado/ sólido.
    def __init__(self, frames, pie, colision=None, fps=0, desfase=0.0):  # Define la funcion __init__: agrupa instrucciones relacionadas.
        self.frames = frames  # Ejecuta la operacion del objeto o biblioteca indicada.
        self.fps = fps  # Ejecuta la operacion del objeto o biblioteca indicada.
        self.desfase = desfase  # Ejecuta la operacion del objeto o biblioteca indicada.
        self.pie = pie  # Ejecuta la operacion del objeto o biblioteca indicada.
        self.solido = colision is not None  # Ejecuta la operacion del objeto o biblioteca indicada.
        ancho, alto = colision if colision else (1, 1)  # Asigna un valor a ancho.
        self.rect = pygame.Rect(0, 0, int(ancho), int(alto))  # Ejecuta la operacion del objeto o biblioteca indicada.
        self.rect.midbottom = pie  # Ejecuta la operacion del objeto o biblioteca indicada.

    def dibujar(self, superficie, cam=(0, 0)):  # Define la funcion dibujar: dibuja el elemento en pantalla.
        if self.fps and len(self.frames) > 1:  # Comprueba una condicion que controla el bloque siguiente.
            imagen = self.frames[int(pygame.time.get_ticks() / 1000 * self.fps + self.desfase) % len(self.frames)]  # Asigna un valor a imagen.
        else:  # Inicia la alternativa si las condiciones anteriores son falsas.
            imagen = self.frames[0]  # Asigna un valor a imagen.
        superficie.blit(imagen, imagen.get_rect(midbottom=(self.pie[0] - cam[0], self.pie[1] - cam[1])))  # Asigna un valor a superficie.blit(imagen.


class Cofre(Prop):  # Define la clase Cofre: representa un cofre con estado abierto/cerrado.
    # Prop con dos estados visuales; abrirlo solo cambia el estado una vez.
    def __init__(self, imagen, imagen_abierta, pie, colision):  # Define la funcion __init__: agrupa instrucciones relacionadas.
        super().__init__([imagen], pie, colision)  # Ejecuta la operacion del objeto o biblioteca indicada.
        self.abierto = False  # Ejecuta la operacion del objeto o biblioteca indicada.
        self.imagen_abierta = pygame.transform.scale(imagen_abierta, imagen.get_size())  # Ejecuta la operacion del objeto o biblioteca indicada.

    def abrir(self):  # Define la funcion abrir: marca el cofre como abierto una sola vez.
        if self.abierto:  # Comprueba una condicion que controla el bloque siguiente.
            return False  # Devuelve el resultado y termina la funcion.
        self.abierto = True  # Ejecuta la operacion del objeto o biblioteca indicada.
        return True  # Devuelve el resultado y termina la funcion.

    def dibujar(self, superficie, cam=(0, 0)):  # Define la funcion dibujar: dibuja el elemento en pantalla.
        imagen = self.imagen_abierta if self.abierto else self.frames[0]  # Asigna un valor a imagen.
        superficie.blit(imagen, imagen.get_rect(midbottom=(self.pie[0] - cam[0], self.pie[1] - cam[1])))  # Asigna un valor a superficie.blit(imagen.


class Pocion:  # Define la clase Pocion: representa una pocion recogible.
    # Objeto recogible situado en el mundo, con rectángulo para detectar contacto.
    def __init__(self, pos):  # Define la funcion __init__: agrupa instrucciones relacionadas.
        self.pos = pygame.Vector2(pos)  # Ejecuta la operacion del objeto o biblioteca indicada.
        self.rect = pygame.Rect(0, 0, 16 * ESCALA_TILES, 16 * ESCALA_TILES)  # Ejecuta la operacion del objeto o biblioteca indicada.
        self.rect.center = self.pos  # Ejecuta la operacion del objeto o biblioteca indicada.

    def dibujar(self, superficie, cam=(0, 0)):  # Define la funcion dibujar: dibuja el elemento en pantalla.
        tamano = 18 * ESCALA_TILES  # Asigna un valor a tamano.
        imagen = cargar_imagen_pocion((tamano, tamano))  # Asigna un valor a imagen.
        centro = (self.rect.centerx - cam[0], self.rect.centery - cam[1])  # Asigna un valor a centro.
        pygame.draw.circle(superficie, (245, 70, 90), centro, self.rect.width // 2 + 6 * ESCALA_TILES, 3)  # Ejecuta la operacion del objeto o biblioteca indicada.
        superficie.blit(imagen, imagen.get_rect(center=centro))  # Asigna un valor a superficie.blit(imagen.


class Mapa:  # Define la clase Mapa: interpreta el plano como elementos del mundo.
    # Interpreta el plano en tiles, colisiones, decoraciones, cofres, líquidos y puertas.
    SUELOS = {  # Asigna un valor a SUELOS.
        "bosque": ([(14, 1), (15, 2), (15, 3), (15, 4), (14, 2), (14, 3)], [60, 10, 10, 10, 5, 5]),  # Define el dato asociado a la clave bosque.
        "camino": ([(9, 2), (9, 3), (9, 4)], [1, 1, 1]),  # Define el dato asociado a la clave camino.
        "losa": ([(10, 2), (10, 3), (10, 4)], [1, 1, 1]),  # Define el dato asociado a la clave losa.
        "losa_roja": ([(12, 2), (12, 3), (12, 4)], [1, 1, 1]),  # Define el dato asociado a la clave losa_roja.
        "pradera": ([(14, 1), (15, 2), (15, 3), (15, 4)], [30, 25, 25, 20]),  # Define el dato asociado a la clave pradera.
        "barro": ([(14, 1), (14, 2), (14, 3), (14, 4)], [45, 20, 20, 15]),  # Define el dato asociado a la clave barro.
        "hueso": ([(16, 1), (16, 2), (16, 3), (16, 4)], [6, 2, 2, 2]),  # Define el dato asociado a la clave hueso.
        "mazmorra": ([(7, 1), (7, 2), (7, 3), (7, 4)], [8, 2, 2, 2]),  # Define el dato asociado a la clave mazmorra.
    }  # Cierra la coleccion o llamada abierta en las lineas anteriores.
    TERRENOS = {  # Asigna un valor a TERRENOS.
        ".": "bosque", ":": "camino", "_": "losa", "r": "losa_roja",  # Define el dato asociado a la clave ..
        ";": "pradera", ",": "barro", "o": "hueso", "g": "mazmorra",  # Define el dato asociado a la clave ;.
    }  # Cierra la coleccion o llamada abierta en las lineas anteriores.
    MUROS = {  # Asigna un valor a MUROS.
        "#": ((3, 1), ([(3, 2), (3, 3)], [3, 1])),  # Asocia el caracter # con las piezas graficas del muro de piedra.
        "d": ((1, 1), ([(1, 2)], [1])),  # Define el dato asociado a la clave d.
        "k": ((2, 1), ([(2, 2)], [1])),  # Define el dato asociado a la clave k.
        "i": ((4, 1), ([(4, 2)], [1])),  # Define el dato asociado a la clave i.
        "l": ((5, 1), ([(5, 2)], [1])),  # Define el dato asociado a la clave l.
        "c": ((6, 1), ([(6, 2)], [1])),  # Define el dato asociado a la clave c.
    }  # Cierra la coleccion o llamada abierta en las lineas anteriores.
    REJAS = {"G": (17, 7)}  # Asigna un valor a REJAS.
    LIQUIDOS = {"~": ("_agua", 11), "v": ("_veneno", 12)}  # Asigna un valor a LIQUIDOS.
    OBJETOS = {  # Asigna un valor a OBJETOS.
        "T": ([(25, 4)], 2, (12, 11)),  # Define el dato asociado a la clave T.
        "t": ([(26, 3)], 1, (9, 9)),  # Define el dato asociado a la clave t.
        "y": ([(26, 1), (26, 2)], 1, (6, 6)),  # Define el dato asociado a la clave y.
        "R": ([(19, 1), (19, 2)], 1, (20, 11)),  # Define el dato asociado a la clave R.
        "M": ([(21, 2)], 1, (10, 7)),  # Define el dato asociado a la clave M.
        "L": ([(18, 7)], 1, (20, 11)),  # Define el dato asociado a la clave L.
        "C": ([(18, 1)], 1, (20, 11)),  # Define el dato asociado a la clave C.
        "A": ([(18, 2)], 1, (20, 11)),  # Define el dato asociado a la clave A.
        "B": ([(18, 5)], 1, (16, 11)),  # Define el dato asociado a la clave B.
        "J": ([(18, 3)], 1, (16, 11)),  # Define el dato asociado a la clave J.
        "X": ([(18, 6)], 1, (14, 10)),  # Define el dato asociado a la clave X.
        "K": ([(24, 1), (24, 2)], 1, (14, 10)),  # Define el dato asociado a la clave K.
        "N": ([(24, 3)], 1, (14, 10)),  # Define el dato asociado a la clave N.
        "S": ([(24, 4), (24, 5)], 1, (20, 12)),  # Define el dato asociado a la clave S.
        "Z": ([(24, 6)], 1, (20, 12)),  # Define el dato asociado a la clave Z.
    }  # Cierra la coleccion o llamada abierta en las lineas anteriores.
    DECORADOS = {  # Asigna un valor a DECORADOS.
        "m": [(21, 1)],  # Define el dato asociado a la clave m.
        "b": [(22, 1), (22, 2)],  # Define el dato asociado a la clave b.
        "p": [(17, 15)],  # Define el dato asociado a la clave p.
        "D": [(17, 4)],  # Define el dato asociado a la clave D.
        "Q": [(17, 8)],  # Define el dato asociado a la clave Q.
        "U": [(17, 13)],  # Define el dato asociado a la clave U.
        "e": [(17, 16)],  # Define el dato asociado a la clave e.
        "f": [(20, 1), (20, 2), (20, 7), (20, 10), (20, 12), (20, 14), (20, 15), (20, 16)],  # Define el dato asociado a la clave f.
        "h": [(20, 3), (20, 4), (20, 5)],  # Define el dato asociado a la clave h.
        "j": [(20, 6)],  # Define el dato asociado a la clave j.
        "w": [(20, 8)],  # Define el dato asociado a la clave w.
        "z": [(20, 9), (20, 7)],  # Define el dato asociado a la clave z.
        "x": [(23, 1), (23, 2)],  # Define el dato asociado a la clave x.
        "s": [(23, 3), (23, 4)],  # Define el dato asociado a la clave s.
    }  # Cierra la coleccion o llamada abierta en las lineas anteriores.
    ANIMADOS = {  # Asigna un valor a ANIMADOS.
        "F": (2, (14, 9), 8),  # Define el dato asociado a la clave F.
        "O": (4, (16, 10), 8),  # Define el dato asociado a la clave O.
        "q": (8, (8, 8), 5),  # Define el dato asociado a la clave q.
    }  # Cierra la coleccion o llamada abierta en las lineas anteriores.

    # Carga los tilesets y crea las estructuras que usan dibujo, navegación y colisiones.
    def __init__(self, plano):  # Define la funcion __init__: agrupa instrucciones relacionadas.
        self.plano = plano  # Ejecuta la operacion del objeto o biblioteca indicada.
        self.filas = len(plano)  # Ejecuta la operacion del objeto o biblioteca indicada.
        self.cols = len(plano[0])  # Ejecuta la operacion del objeto o biblioteca indicada.
        assert all(len(f) == self.cols for f in plano), "todas las filas del plano deben tener el mismo largo"  # Completa los argumentos o datos usados por esta parte del juego.
        for base in (os.getcwd(), os.path.dirname(os.path.abspath(__file__))):  # Inicia un ciclo que procesa cada elemento indicado.
            carpeta = os.path.join(base, "mapa")  # Asigna un valor a carpeta.
            if os.path.isdir(carpeta):  # Comprueba una condicion que controla el bloque siguiente.
                break  # Termina anticipadamente el ciclo.
        else:  # Inicia la alternativa si las condiciones anteriores son falsas.
            print("No encuentro la carpeta 'mapa' junto a este archivo (descomprime mapa.zip).")  # Muestra un encabezado en la consola durante el arranque.
            if video_fondo is not None:  # Comprueba una condicion que controla el bloque siguiente.
               video_fondo.cerrar()  # Completa los argumentos o datos usados por esta parte del juego.
            pygame.quit()  # Ejecuta la operacion del objeto o biblioteca indicada.
            sys.exit()  # Ejecuta la operacion del objeto o biblioteca indicada.
        self.hoja_tiles = pygame.image.load(os.path.join(carpeta, "tiles.png")).convert_alpha()  # Ejecuta la operacion del objeto o biblioteca indicada.
        self.hoja_auto = pygame.image.load(os.path.join(carpeta, "autotiles.png")).convert_alpha()  # Ejecuta la operacion del objeto o biblioteca indicada.
        self.hoja_anim = pygame.image.load(os.path.join(carpeta, "animated-tiles.png")).convert_alpha()  # Ejecuta la operacion del objeto o biblioteca indicada.
        self.imagen_cofre_abierto = pygame.image.load(  # Ejecuta la operacion del objeto o biblioteca indicada.
            os.path.join(carpeta, "cofre_abierto.png")  # Ejecuta la operacion del objeto o biblioteca indicada.
        ).convert_alpha()  # Completa los argumentos o datos usados por esta parte del juego.
        self._cache = {}  # Ejecuta la operacion del objeto o biblioteca indicada.
        self.suelo = [[[] for _ in range(self.cols)] for _ in range(self.filas)]  # Ejecuta la operacion del objeto o biblioteca indicada.
        self.terreno_solido = [[False] * self.cols for _ in range(self.filas)]  # Ejecuta la operacion del objeto o biblioteca indicada.
        self.bloqueada = [[False] * self.cols for _ in range(self.filas)]  # Ejecuta la operacion del objeto o biblioteca indicada.
        self.bloquea_vista = [[False] * self.cols for _ in range(self.filas)]  # Ejecuta la operacion del objeto o biblioteca indicada.
        self.props = []
        self.cofres = []  # Guarda en el objeto cofres cuyo estado puede reiniciarse.
        self.solidos_en = {}  # Guarda en el objeto objetos solidos indexados por casilla.
        self.animados = []  # Guarda en el objeto elementos graficos animados del mapa.
        self.puertas_abiertas = set()  # Guarda en el objeto coordenadas de puertas ya desbloqueadas.
        self.suelo_puerta = {}  # Guarda en el objeto suelo que queda visible al abrir cada puerta.
        self.reja_temporal = None
        self.puerta_img = escalar_imagen(  # Guarda en el objeto sprite de una reja cerrada.
            self.hoja_tiles.subsurface(((17 - 1) * 32, (7 - 1) * 32, 32, 32)).copy(),  # Consulta o modifica el estado del objeto actual.
            ESCALA_TILES,  # Continua la lista de argumentos o valores de esta instruccion.
        )  # Cierra la llamada o coleccion de datos iniciada anteriormente.
        self.inicio = (self.cols * TAM_TILE // 2, self.filas * TAM_TILE // 2)  # Guarda en el objeto posicion inicial del jugador.
        self._agua = self._autotiles(1)  # Carga tiles de borde para el tipo de liquido indicado.
        self._veneno = self._autotiles(5)  # Carga tiles de borde para el tipo de liquido indicado.
        self._construir()  # Construye las capas y colisiones de todas las casillas.

    # Extrae del tileset una imagen escalada y la conserva en caché.
    def pieza(self, fila, col, alto=1):  # Define la metodo pieza: extrae, escala y cachea una pieza grafica del tileset.
        clave = (fila, col, alto)  # Calcula o guarda clave para el resto del metodo.
        if clave not in self._cache:  # Evalua la condicion que decide el comportamiento siguiente.
            img = self.hoja_tiles.subsurface(((col - 1) * 32, (fila - 1) * 32, 32, 32 * alto)).copy()  # Calcula o guarda img para el resto del metodo.
            self._cache[clave] = escalar_imagen(img, ESCALA_TILES)  # Guarda en el objeto _cache[clave].
        return self._cache[clave]  # Devuelve el dato calculado por este metodo.

    @staticmethod  # Aporta un dato o una instruccion para el comportamiento indicado.
    def _firma(tile):  # Define la metodo _firma: describe los bordes opacos de un autotile.
        def opaco(x, y):  # Define la metodo opaco: consulta la transparencia de un pixel.
            return tile.get_at((x, y)).a > 0  # Devuelve el dato calculado por este metodo.
        n, e, s, w = opaco(16, 0), opaco(31, 16), opaco(16, 31), opaco(0, 16)  # Calcula o guarda n para el resto del metodo.
        def esquina(x0, y0, lados):  # Define la metodo esquina: comprueba si una esquina del autotile esta cubierta.
            if not all(lados):  # Evalua la condicion que decide el comportamiento siguiente.
                return False  # Devuelve False para comunicar el resultado de la comprobacion.
            return all(tile.get_at((x, y)).a > 0 for y in range(y0, y0 + 6) for x in range(x0, x0 + 6))  # Devuelve el dato calculado por este metodo.
        return (n, e, s, w, esquina(0, 0, (n, w)), esquina(26, 0, (n, e)), esquina(0, 26, (s, w)), esquina(26, 26, (s, e)))  # Devuelve el dato calculado por este metodo.

    # Indexa las piezas de agua o veneno por la forma de sus bordes transparentes.
    def _autotiles(self, fila0):  # Define la metodo _autotiles: carga y clasifica las piezas graficas del liquido.
        piezas = {}  # Calcula o guarda piezas para el resto del metodo.
        for f in range(4):  # Repite la operacion por cada indice o paso de este rango.
            for c in range(12):  # Repite la operacion por cada indice o paso de este rango.
                tile = self.hoja_auto.subsurface((c * 32, (fila0 - 1 + f) * 32, 32, 32)).copy()  # Calcula o guarda tile para el resto del metodo.
                if pygame.mask.from_surface(tile).count() == 0:  # Evalua la condicion que decide el comportamiento siguiente.
                    continue  # Salta al siguiente elemento del ciclo.
                piezas.setdefault(self._firma(tile), escalar_imagen(tile, ESCALA_TILES))  # Aporta un dato o una instruccion para el comportamiento indicado.
        return piezas  # Devuelve el dato calculado por este metodo.

    def _dentro(self, x, y):  # Define la metodo _dentro: comprueba si una casilla esta dentro del mapa.
        return 0 <= x < self.cols and 0 <= y < self.filas  # Devuelve el dato calculado por este metodo.

    def _terreno_de(self, x, y):  # Define la metodo _terreno_de: elige el terreno que corresponde a una casilla.
        ch = self.plano[y][x]  # Calcula o guarda ch para el resto del metodo.
        if ch in self.TERRENOS:  # Evalua la condicion que decide el comportamiento siguiente.
            return self.TERRENOS[ch]  # Devuelve el dato calculado por este metodo.
        if ch == "D":  # Evalua la condicion que decide el comportamiento siguiente.
            return "losa"  # Devuelve el dato calculado por este metodo.
        votos = {}  # Calcula o guarda votos para el resto del metodo.
        for dy in (-1, 0, 1):  # Inicia un ciclo para procesar cada elemento indicado.
            for dx in (-1, 0, 1):  # Inicia un ciclo para procesar cada elemento indicado.
                if self._dentro(x + dx, y + dy) and self.plano[y + dy][x + dx] in self.TERRENOS:  # Evalua la condicion que decide el comportamiento siguiente.
                    t = self.TERRENOS[self.plano[y + dy][x + dx]]  # Calcula o guarda reloj interno utilizado para animaciones y calculos de tiempo para el resto del metodo.
                    votos[t] = votos.get(t, 0) + 1  # Calcula o guarda votos[t] para el resto del metodo.
        return max(votos, key=votos.get) if votos else "bosque"  # Devuelve el dato calculado por este metodo.

    def _frames_anim(self, fila):  # Define la metodo _frames_anim: carga y conserva los fotogramas de una animacion.
        clave = ("anim", fila)  # Calcula o guarda clave para el resto del metodo.
        if clave not in self._cache:  # Evalua la condicion que decide el comportamiento siguiente.
            frames = []  # Calcula o guarda frames para el resto del metodo.
            for c in range(self.hoja_anim.get_width() // 32):  # Repite la operacion por cada indice o paso de este rango.
                img = self.hoja_anim.subsurface((c * 32, (fila - 1) * 32, 32, 32)).copy()  # Calcula o guarda img para el resto del metodo.
                if pygame.mask.from_surface(img).count() > 0:  # Evalua la condicion que decide el comportamiento siguiente.
                    frames.append(escalar_imagen(img, ESCALA_TILES))  # Aporta un dato o una instruccion para el comportamiento indicado.
            self._cache[clave] = frames  # Guarda en el objeto _cache[clave].
        return self._cache[clave]  # Devuelve el dato calculado por este metodo.

    def _mismo(self, x, y, ch):  # Define la metodo _mismo: comprueba si una casilla vecina comparte el mismo liquido.
        return not self._dentro(x, y) or self.plano[y][x] == ch  # Devuelve el dato calculado por este metodo.

    # Recorre el plano y materializa terrenos, líquidos, muros, decoraciones y objetos.
    def _construir(self):  # Define la metodo _construir: crea las capas graficas y colisiones del mapa.
        rng = random.Random(7)  # Calcula o guarda rng para el resto del metodo.
        T = TAM_TILE  # Calcula o guarda T para el resto del metodo.
        for y in range(self.filas):  # Repite la operacion por cada indice o paso de este rango.
            for x in range(self.cols):  # Repite la operacion por cada indice o paso de este rango.
                ch = self.plano[y][x]  # Calcula o guarda ch para el resto del metodo.
                capas = self.suelo[y][x]  # Calcula o guarda capas para el resto del metodo.
                centro = ((x + 0.5) * T, (y + 0.5) * T)  # Calcula o guarda centro para el resto del metodo.
                pie = ((x + 0.5) * T, (y + 1) * T - 2 * ESCALA_TILES)  # Calcula o guarda pie para el resto del metodo.
                if ch in self.MUROS:  # si la casilla es muro, crea su grafico y la marca solida
                    superior, (opciones, pesos) = self.MUROS[ch]  # Calcula o guarda superior para el resto del metodo.
                    abajo = self.plano[y + 1][x] if self._dentro(x, y + 1) else "."  # Calcula o guarda abajo para el resto del metodo.
                    if abajo in self.MUROS:  # Evalua la condicion que decide el comportamiento siguiente.
                        capas.append(self.pieza(*superior))  # Aporta un dato o una instruccion para el comportamiento indicado.
                    else:  # Inicia el caso alternativo cuando la condicion anterior no se cumple.
                        capas.append(self.pieza(*rng.choices(opciones, pesos)[0]))  # Aporta un dato o una instruccion para el comportamiento indicado.
                    self.terreno_solido[y][x] = self.bloqueada[y][x] = self.bloquea_vista[y][x] = True  # Guarda en el objeto terreno_solido[y][x].
                    continue  # Salta al siguiente elemento del ciclo.
                opciones, pesos = self.SUELOS[self._terreno_de(x, y)]  # Calcula o guarda opciones para el resto del metodo.
                capas.append(self.pieza(*rng.choices(opciones, pesos)[0]))  # Aporta un dato o una instruccion para el comportamiento indicado.
                if ch in self.LIQUIDOS:  # si la casilla es agua o veneno, crea su borde y la bloquea
                    atributo, fila_anim = self.LIQUIDOS[ch]  # Calcula o guarda atributo para el resto del metodo.
                    n, e, s, w = self._mismo(x, y - 1, ch), self._mismo(x + 1, y, ch), self._mismo(x, y + 1, ch), self._mismo(x - 1, y, ch)  # Calcula o guarda n para el resto del metodo.
                    firma = (n, e, s, w, n and w and self._mismo(x - 1, y - 1, ch), n and e and self._mismo(x + 1, y - 1, ch),  # Calcula o guarda firma para el resto del metodo.
                             s and w and self._mismo(x - 1, y + 1, ch), s and e and self._mismo(x + 1, y + 1, ch))  # Aporta un dato o una instruccion para el comportamiento indicado.
                    piezas = getattr(self, atributo)  # Calcula o guarda piezas para el resto del metodo.
                    capas.append(piezas.get(firma) or piezas[(True,) * 8])  # Aporta un dato o una instruccion para el comportamiento indicado.
                    self.terreno_solido[y][x] = self.bloqueada[y][x] = True  # Guarda en el objeto terreno_solido[y][x].
                    if rng.random() < 0.4:  # Evalua la condicion que decide el comportamiento siguiente.
                        frames = self._frames_anim(fila_anim)  # Obtiene los fotogramas para la animacion del terreno.
                        self.animados.append(Prop(frames, ((x + 0.5) * T, (y + 1) * T), fps=5, desfase=rng.random() * len(frames)))  # Guarda en el objeto elementos graficos animados del mapa.
                elif ch in self.REJAS:  # si es una reja, guarda el suelo y bloquea el paso
                    self.suelo_puerta[(x, y)] = capas[0]  # Guarda en el objeto suelo_puerta[(x, y)].
                    capas.append(self.pieza(*self.REJAS[ch]))  # Aporta un dato o una instruccion para el comportamiento indicado.
                    self.terreno_solido[y][x] = self.bloqueada[y][x] = True  # Guarda en el objeto terreno_solido[y][x].
                elif ch in self.DECORADOS:  # si es decoracion, agrega su tile visual
                    capas.append(self.pieza(*rng.choice(self.DECORADOS[ch])))  # Aporta un dato o una instruccion para el comportamiento indicado.
                elif ch in self.OBJETOS:  # si es un objeto, crea su sprite y colision solida
                    piezas, alto, (cw, chh) = self.OBJETOS[ch]  # Calcula o guarda piezas para el resto del metodo.
                    fila, col = rng.choice(piezas)  # Calcula o guarda fila para el resto del metodo.
                    imagen = self.pieza(fila, col, alto)  # Calcula o guarda sprite que se dibuja en el fotograma actual para el resto del metodo.
                    if ch == "C":  # Evalua la condicion que decide el comportamiento siguiente.
                        prop = Cofre(  # Calcula o guarda prop para el resto del metodo.
                            imagen,  # Continua la lista de argumentos o valores de esta instruccion.
                            self.imagen_cofre_abierto,  # Consulta o modifica el estado del objeto actual.
                            pie,  # Continua la lista de argumentos o valores de esta instruccion.
                            (cw * ESCALA_TILES, chh * ESCALA_TILES),  # Continua la lista de argumentos o valores de esta instruccion.
                        )  # Cierra la llamada o coleccion de datos iniciada anteriormente.
                        self.cofres.append(prop)  # Consulta o modifica el estado del objeto actual.
                    else:  # Inicia el caso alternativo cuando la condicion anterior no se cumple.
                        prop = Prop([imagen], pie, (cw * ESCALA_TILES, chh * ESCALA_TILES))  # Calcula o guarda prop para el resto del metodo.
                    self.props.append(prop)  # Consulta o modifica el estado del objeto actual.
                    self.solidos_en.setdefault((y, x), []).append(prop)  # Consulta o modifica el estado del objeto actual.
                    self.bloqueada[y][x] = True  # Guarda en el objeto bloqueada[y][x].
                elif ch in self.ANIMADOS:  # si es animado, crea y registra sus fotogramas
                    fila_anim, (cw, chh), fps = self.ANIMADOS[ch]  # Calcula o guarda fila_anim para el resto del metodo.
                    prop = Prop(self._frames_anim(fila_anim), pie, (cw * ESCALA_TILES, chh * ESCALA_TILES),  # Obtiene los fotogramas para la animacion del terreno.
                                fps=fps, desfase=rng.random() * 6)  # Calcula o guarda fps para el resto del metodo.
                    self.props.append(prop)  # Consulta o modifica el estado del objeto actual.
                    self.solidos_en.setdefault((y, x), []).append(prop)  # Consulta o modifica el estado del objeto actual.
                    self.bloqueada[y][x] = True  # Guarda en el objeto bloqueada[y][x].
                elif ch == "P":  # si es el marcador P, establece el inicio del jugador
                    self.inicio = (centro[0], centro[1] + 10)  # Guarda en el objeto posicion inicial del jugador.

    # Convierte las puertas seleccionadas en casillas transitables y devuelve las abiertas.
    def abrir_puertas(self, puertas):  # Define la metodo abrir_puertas: abre las puertas indicadas y actualiza sus colisiones.
        abiertas = []  # Calcula o guarda abiertas para el resto del metodo.
        for x, y in puertas:  # Inicia un ciclo para procesar cada elemento indicado.
            posicion = (x, y)  # Calcula o guarda posicion para el resto del metodo.
            if posicion not in self.suelo_puerta or posicion in self.puertas_abiertas:  # Evalua la condicion que decide el comportamiento siguiente.
                continue  # Salta al siguiente elemento del ciclo.
            self.suelo[y][x] = [self.suelo_puerta[posicion]]  # Guarda en el objeto suelo[y][x].
            self.terreno_solido[y][x] = False  # Guarda en el objeto terreno_solido[y][x].
            self.bloqueada[y][x] = False  # Guarda en el objeto bloqueada[y][x].
            self.bloquea_vista[y][x] = False  # Guarda en el objeto bloquea_vista[y][x].
            self.puertas_abiertas.add(posicion)  # Consulta o modifica el estado del objeto actual.
            abiertas.append(posicion)  # Aporta un dato o una instruccion para el comportamiento indicado.
        return abiertas  # Devuelve el dato calculado por este metodo.

    # Restaura cofres y puertas a su estado inicial para una partida nueva.
    def reiniciar_progreso(self):  # Define la metodo reiniciar_progreso: restaura cofres y puertas al estado inicial.
        for cofre in self.cofres:  # Recorre los cofres para restaurar su estado.
            cofre.abierto = False  # Calcula o guarda cofre.abierto para el resto del metodo.
        for x, y in self.puertas_abiertas:  # Recorre las puertas que se deben volver a cerrar.
            self.suelo[y][x] = [self.suelo_puerta[(x, y)], self.puerta_img]  # Guarda en el objeto suelo[y][x].
            self.terreno_solido[y][x] = True  # Guarda en el objeto terreno_solido[y][x].
            self.bloqueada[y][x] = True  # Guarda en el objeto bloqueada[y][x].
            self.bloquea_vista[y][x] = False  # Guarda en el objeto bloquea_vista[y][x].
        self.puertas_abiertas.clear()  # Consulta o modifica el estado del objeto actual.
        self.reja_temporal = None

    def dibujar_suelo(self, superficie, cam):  # Define la metodo dibujar_suelo: dibuja las casillas visibles y las animaciones del suelo.
        T = TAM_TILE  # Calcula o guarda T para el resto del metodo.
        superficie.fill((14, 18, 18))  # Aporta un dato o una instruccion para el comportamiento indicado.
        c0, c1 = max(0, cam[0] // T), min(self.cols - 1, (cam[0] + width) // T)  # Calcula o guarda c0 para el resto del metodo.
        f0, f1 = max(0, cam[1] // T), min(self.filas - 1, (cam[1] + height) // T)  # Calcula o guarda f0 para el resto del metodo.
        for f in range(f0, f1 + 1):  # Repite la operacion por cada indice o paso de este rango.
            for c in range(c0, c1 + 1):  # Repite la operacion por cada indice o paso de este rango.
                x, y = c * T - cam[0], f * T - cam[1]  # Calcula o guarda x para el resto del metodo.
                for capa in self.suelo[f][c]:  # Inicia un ciclo para procesar cada elemento indicado.
                    superficie.blit(capa, (x, y))  # Pinta el sprite o capa sobre la superficie de juego.
        if self.reja_temporal is not None:
            x, y, ancho = self.reja_temporal
            for columna in range(ancho):
                superficie.blit(
                    self.puerta_img,
                    (int((x + columna) * T - cam[0]), int(y * T - cam[1])),
                )
        x0, x1 = cam[0] - T, cam[0] + width + T  # Calcula o guarda x0 para el resto del metodo.
        y0, y1 = cam[1], cam[1] + height + T  # Calcula o guarda y0 para el resto del metodo.
        for animado in self.animados:  # Inicia un ciclo para procesar cada elemento indicado.
            if x0 <= animado.pie[0] <= x1 and y0 <= animado.pie[1] <= y1:  # Evalua la condicion que decide el comportamiento siguiente.
                animado.dibujar(superficie, cam)  # Aporta un dato o una instruccion para el comportamiento indicado.

    def props_visibles(self, cam):  # Define la metodo props_visibles: filtra los objetos que aparecen dentro de la camara.
        x0, x1 = cam[0] - TAM_TILE, cam[0] + width + TAM_TILE  # Calcula o guarda x0 para el resto del metodo.
        y0, y1 = cam[1], cam[1] + height + 2 * TAM_TILE  # Calcula o guarda y0 para el resto del metodo.
        return [p for p in self.props if x0 <= p.pie[0] <= x1 and y0 <= p.pie[1] <= y1]  # Devuelve el dato calculado por este metodo.

    def dibujar_colisiones(self, superficie, cam):  # Define la metodo dibujar_colisiones: muestra las cajas de colision para depuracion.
        T = TAM_TILE  # Calcula o guarda T para el resto del metodo.
        for f in range(max(0, cam[1] // T), min(self.filas, (cam[1] + height) // T + 1)):  # Repite la operacion por cada indice o paso de este rango.
            for c in range(max(0, cam[0] // T), min(self.cols, (cam[0] + width) // T + 1)):  # Repite la operacion por cada indice o paso de este rango.
                if self.terreno_solido[f][c]:  # Evalua la condicion que decide el comportamiento siguiente.
                    pygame.draw.rect(superficie, (255, 40, 40), (c * T - cam[0], f * T - cam[1], T, T), 1)  # Dibuja el elemento de interfaz o efecto visual indicado.
        for p in self.props_visibles(cam):  # Inicia un ciclo para procesar cada elemento indicado.
            if p.solido:  # Evalua la condicion que decide el comportamiento siguiente.
                pygame.draw.rect(superficie, (255, 160, 0), p.rect.move(-cam[0], -cam[1]), 2)  # Dibuja el elemento de interfaz o efecto visual indicado.

    # Calcula por búsqueda en anchura qué casillas libres se conectan con el destino.
    def celdas_alcanzables(self, inicio, limite):  # Define la metodo celdas_alcanzables: busca las casillas libres conectadas con el inicio.
        c0, f0, c1, f1 = limite  # Calcula o guarda c0 para el resto del metodo.
        vistas = {inicio}  # Calcula o guarda vistas para el resto del metodo.
        cola = [inicio]  # Calcula o guarda cola para el resto del metodo.
        for c, f in cola:  # Inicia un ciclo para procesar cada elemento indicado.
            for dc, df in ((1, 0), (-1, 0), (0, 1), (0, -1)):  # Inicia un ciclo para procesar cada elemento indicado.
                nc, nf = c + dc, f + df  # Calcula o guarda nc para el resto del metodo.
                if c0 <= nc <= c1 and f0 <= nf <= f1 and (nc, nf) not in vistas and not self.bloqueada[nf][nc]:  # Evalua la condicion que decide el comportamiento siguiente.
                    vistas.add((nc, nf))  # Aporta un dato o una instruccion para el comportamiento indicado.
                    cola.append((nc, nf))  # Aporta un dato o una instruccion para el comportamiento indicado.
        return vistas  # Devuelve el dato calculado por este metodo.

    # Detecta solapamiento con límites, terreno sólido y rectángulos de objetos.
    def choca(self, rect):  # Define la metodo choca: comprueba colisiones con limites, suelo y objetos.
        T = TAM_TILE  # Calcula o guarda T para el resto del metodo.
        if rect.left < 0 or rect.top < 0 or rect.right > self.cols * T or rect.bottom > self.filas * T:  # Evalua la condicion que decide el comportamiento siguiente.
            return True  # Devuelve True para comunicar el resultado de la comprobacion.
        if self.reja_temporal is not None:
            x, y, ancho = self.reja_temporal
            barrera = pygame.Rect(x * T, y * T, ancho * T, T)
            if rect.colliderect(barrera):
                return True
        for f in range(rect.top // T, (rect.bottom - 1) // T + 1):  # Repite la operacion por cada indice o paso de este rango.
            for c in range(rect.left // T, (rect.right - 1) // T + 1):  # Repite la operacion por cada indice o paso de este rango.
                if self.terreno_solido[f][c]:  # Evalua la condicion que decide el comportamiento siguiente.
                    return True  # Devuelve True para comunicar el resultado de la comprobacion.
                for p in self.solidos_en.get((f, c), ()):  # Inicia un ciclo para procesar cada elemento indicado.
                    if rect.colliderect(p.rect):  # Evalua la condicion que decide el comportamiento siguiente.
                        return True  # Devuelve True para comunicar el resultado de la comprobacion.
        return False  # Devuelve False para comunicar el resultado de la comprobacion.

    def hay_vista(self, a, b):  # Define la metodo hay_vista: comprueba si un muro bloquea la vision entre dos puntos.
        T = TAM_TILE  # Calcula o guarda T para el resto del metodo.
        pasos = max(1, int(math.hypot(b[0] - a[0], b[1] - a[1]) // 32))  # Calcula o guarda pasos para el resto del metodo.
        for i in range(1, pasos):  # Repite la operacion por cada indice o paso de este rango.
            x = a[0] + (b[0] - a[0]) * i / pasos  # Calcula o guarda x para el resto del metodo.
            y = a[1] + (b[1] - a[1]) * i / pasos  # Calcula o guarda y para el resto del metodo.
            c, f = int(x // T), int(y // T)  # Calcula o guarda c para el resto del metodo.
            if self._dentro(c, f) and self.bloquea_vista[f][c]:  # Evalua la condicion que decide el comportamiento siguiente.
                return False  # Devuelve False para comunicar el resultado de la comprobacion.
        return True  # Devuelve True para comunicar el resultado de la comprobacion.

    def paso_libre(self, a, b, ancho, alto):  # Define la metodo paso_libre: verifica si un rectangulo puede recorrer una linea sin chocar.
        pasos = max(1, int(math.hypot(b[0] - a[0], b[1] - a[1]) // 16))  # Calcula o guarda pasos para el resto del metodo.
        caja = pygame.Rect(0, 0, int(ancho), int(alto))  # Crea un rectangulo usado como posicion o hitbox.
        for i in range(pasos + 1):  # Repite la operacion por cada indice o paso de este rango.
            caja.center = (a[0] + (b[0] - a[0]) * i / pasos, a[1] + (b[1] - a[1]) * i / pasos)  # Calcula o guarda caja.center para el resto del metodo.
            if self.choca(caja):  # Evalua la condicion que decide el comportamiento siguiente.
                return False  # Devuelve False para comunicar el resultado de la comprobacion.
        return True  # Devuelve True para comunicar el resultado de la comprobacion.

    # Devuelve una ruta de casillas transitables entre dos puntos del mapa.
    def camino(self, a, b):  # Define la metodo camino: busca y reconstruye una ruta transitable entre dos puntos.
        T = TAM_TILE  # Calcula o guarda T para el resto del metodo.
        ini = (min(self.filas - 1, max(0, int(a[1] // T))), min(self.cols - 1, max(0, int(a[0] // T))))  # Calcula o guarda ini para el resto del metodo.
        fin = (min(self.filas - 1, max(0, int(b[1] // T))), min(self.cols - 1, max(0, int(b[0] // T))))  # Calcula o guarda fin para el resto del metodo.
        if ini == fin:  # Evalua la condicion que decide el comportamiento siguiente.
            return [b]  # Devuelve el dato calculado por este metodo.
        previo = {ini: None}  # Calcula o guarda previo para el resto del metodo.
        cola = [ini]  # Calcula o guarda cola para el resto del metodo.
        for f, c in cola:  # Inicia un ciclo para procesar cada elemento indicado.
            if (f, c) == fin:  # Evalua la condicion que decide el comportamiento siguiente.
                break  # Termina el ciclo porque ya se encontro el resultado.
            for df, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):  # Inicia un ciclo para procesar cada elemento indicado.
                nf, nc = f + df, c + dc  # Calcula o guarda nf para el resto del metodo.
                if self._dentro(nc, nf) and (nf, nc) not in previo and (not self.bloqueada[nf][nc] or (nf, nc) == fin):  # Evalua la condicion que decide el comportamiento siguiente.
                    previo[(nf, nc)] = (f, c)  # Calcula o guarda previo[(nf para el resto del metodo.
                    cola.append((nf, nc))  # Aporta un dato o una instruccion para el comportamiento indicado.
        if fin not in previo:  # Evalua la condicion que decide el comportamiento siguiente.
            return []  # Devuelve el dato calculado por este metodo.
        ruta, nodo = [], fin  # Calcula o guarda ruta para el resto del metodo.
        while nodo != ini:  # Repite el bloque hasta completar la condicion del ciclo.
            ruta.append(((nodo[1] + 0.5) * T, (nodo[0] + 0.5) * T))  # Aporta un dato o una instruccion para el comportamiento indicado.
            nodo = previo[nodo]  # Calcula o guarda nodo para el resto del metodo.
        ruta.reverse()  # Aporta un dato o una instruccion para el comportamiento indicado.
        ruta[-1] = tuple(b)  # Calcula o guarda ruta[-1] para el resto del metodo.
        return ruta  # Devuelve el dato calculado por este metodo.


print("---------- CLASE DE OLEADAS Y PROGRESO ----------")  # Aporta un dato o una instruccion para el comportamiento indicado.
class Oleadas:  # Define la clase Oleadas: agrupa instrucciones relacionadas.
    # Valida las zonas y dirige el progreso, los avisos, las apariciones y la puntuación.
    def __init__(self, zonas):  # Define la metodo __init__: inicializa los datos y el estado inicial del objeto.
        T = TAM_TILE  # Calcula o guarda T para el resto del metodo.
        self.zonas = []  # Guarda en el objeto datos preparados de todas las oleadas.
        self.puntuacion = 0  # Guarda en el objeto puntos acumulados por derrotar enemigos.
        for nivel, z in enumerate(zonas, 1):  # Inicia un ciclo para procesar cada elemento indicado.
            c0, f0, c1, f1 = z["casillas"]  # Calcula o guarda c0 para el resto del metodo.
            dc, df = z["destino"]  # Calcula o guarda dc para el resto del metodo.
            if not mapa._dentro(dc, df) or mapa.bloqueada[df][dc]:  # Evalua la condicion que decide el comportamiento siguiente.
                raise ValueError(f"El destino de la zona {z['nombre']} no es transitable: {(dc, df)}")  # Informa que la configuracion no permite continuar.
            libres = mapa.celdas_alcanzables((dc, df), (c0, f0, c1, f1))  # Calcula o guarda libres para el resto del metodo.
            if not libres:  # Evalua la condicion que decide el comportamiento siguiente.
                raise ValueError(f"La zona {z['nombre']} no tiene puntos de aparicion alcanzables")  # Informa que la configuracion no permite continuar.
            tipos_enemigos = tuple(z.get("tipos_enemigos", ("goblin",)))  # Calcula o guarda tipos_enemigos para el resto del metodo.
            if not z.get("jefe") and not tipos_enemigos:  # Evalua la condicion que decide el comportamiento siguiente.
                raise ValueError(f"La zona {z['nombre']} necesita al menos un tipo de enemigo")  # Informa que la configuracion no permite continuar.
            for tipo in tipos_enemigos:  # Revisa los enemigos para contar bajas o actualizar el encuentro.
                if tipo not in ARQUETIPOS_ENEMIGO:  # Evalua la condicion que decide el comportamiento siguiente.
                    raise ValueError(  # Informa que la configuracion no permite continuar.
                        f"Arquetipo de enemigo desconocido: {tipo} en la zona {z['nombre']}"  # Aporta un dato o una instruccion para el comportamiento indicado.
                    )  # Cierra la llamada o coleccion de datos iniciada anteriormente.
            tipos_apoyo = tuple(z.get("tipos_apoyo", ()))  # Calcula o guarda tipos_apoyo para el resto del metodo.
            for tipo in tipos_apoyo:  # Inicia un ciclo para procesar cada elemento indicado.
                if tipo not in ARQUETIPOS_ENEMIGO:  # Evalua la condicion que decide el comportamiento siguiente.
                    raise ValueError(  # Informa que la configuracion no permite continuar.
                        f"Arquetipo de apoyo desconocido: {tipo} en la zona {z['nombre']}"  # Aporta un dato o una instruccion para el comportamiento indicado.
                    )  # Cierra la llamada o coleccion de datos iniciada anteriormente.
            sprite_jefe = z.get("sprite_jefe", "goblin")  # Calcula o guarda sprite_jefe para el resto del metodo.
            if z.get("jefe") and not os.path.isfile(ruta_sprite_enemigo(sprite_jefe)):  # Evalua la condicion que decide el comportamiento siguiente.
                raise ValueError(  # Informa que la configuracion no permite continuar.
                    f"No existe el sprite enemigos/{sprite_jefe}.png configurado para el jefe de {z['nombre']}"  # Aporta un dato o una instruccion para el comportamiento indicado.
                )  # Cierra la llamada o coleccion de datos iniciada anteriormente.
            self.zonas.append({  # Consulta o modifica el estado del objeto actual.
                "nivel": nivel, "nombre": z["nombre"], "color": z["color"], "cerrada": z.get("cerrada", True),  # Define los datos de configuracion asociados a nivel.
                "rect": pygame.Rect(c0 * T, f0 * T, (c1 - c0 + 1) * T, (f1 - f0 + 1) * T),  # Crea un rectangulo usado como posicion o hitbox.
                "destino": ((dc + 0.5) * T, (df + 0.5) * T),  # Define los datos de configuracion asociados a destino.
                "dist": z.get("distancia_aparicion", 600),  # Define los datos de configuracion asociados a dist.
                "total": 1 if z.get("jefe") else z.get(  # Define los datos de configuracion asociados a total.
                    "enemigos_derrotar", z.get("enemigos", OLEADA_ENEMIGOS_BASE + OLEADA_ENEMIGOS_MAS * (nivel - 1))  # Aporta un dato o una instruccion para el comportamiento indicado.
                ),  # Cierra la llamada o coleccion de datos iniciada anteriormente.
                "jefe": z.get("jefe", False),  # Define los datos de configuracion asociados a jefe.
                "sprite_jefe": sprite_jefe,  # Define los datos de configuracion asociados a sprite_jefe.
                "tipo_jefe": z.get("tipo_jefe", "dragon" if sprite_jefe == "dragon" else "goblin"),  # Define los datos de configuracion asociados a tipo_jefe.
                "puertas": tuple(z.get("puertas", ())),
                "reja_temporal": z.get("reja_temporal"),
                "tipos_apoyo": tipos_apoyo,  # Define los datos de configuracion asociados a tipos_apoyo.
                "max_apoyos": z.get("max_apoyos", 0),  # Define los datos de configuracion asociados a max_apoyos.
                "max_vivos": z.get("max_vivos", OLEADA_MAX_VIVOS_BASE + OLEADA_MAX_VIVOS_MAS * (nivel - 1)),  # Define los datos de configuracion asociados a max_vivos.
                "intervalo": z.get(  # Define los datos de configuracion asociados a intervalo.
                    "intervalo_aparicion",  # Continua la lista de argumentos o valores de esta instruccion.
                    z.get("intervalo", max(OLEADA_INTERVALO_MIN, OLEADA_INTERVALO_BASE - OLEADA_INTERVALO_MENOS * (nivel - 1)))  # Aporta un dato o una instruccion para el comportamiento indicado.
                ),  # Cierra la llamada o coleccion de datos iniciada anteriormente.
                "tipos_enemigos": tipos_enemigos,  # Define los datos de configuracion asociados a tipos_enemigos.
                "puntos": [((c + 0.5) * T, (f + 1) * T - 3 * ESCALA_TILES) for c, f in sorted(libres)],  # Define los datos de configuracion asociados a puntos.
                "estado": "pendiente",  # Define los datos de configuracion asociados a estado.
                "generados": 0, "matados": 0, "t_prep": 0.0, "t_spawn": 0.0,  # Define los datos de configuracion asociados a generados.
                "tiempo_oleada": 0.0, "puntos_ganados": 0,  # Define los datos de configuracion asociados a tiempo_oleada.
            })  # Aporta un dato o una instruccion para el comportamiento indicado.
        self.t = 0.0  # Guarda en el objeto reloj interno utilizado para animaciones y calculos de tiempo.
        self.aviso, self.t_aviso = [], 0.0  # Guarda en el objeto aviso, self.
        self.t_barrera = 0.0  # Guarda en el objeto tiempo restante del aviso de barrera.
        self.objetivo_flecha, self.t_ruta = None, -1.0  # Guarda en el objeto objetivo_flecha, self.
        self._vinetas = {}  # Guarda en el objeto cache de efectos de color por zona.

    @property  # Aporta un dato o una instruccion para el comportamiento indicado.
    def actual(self):  # Define la metodo actual: devuelve la primera zona que no se ha completado.
        for z in self.zonas:  # Recorre las zonas para buscar la activa o dibujar sus limites.
            if z["estado"] != "completada":  # Evalua la condicion que decide el comportamiento siguiente.
                return z  # Devuelve el dato calculado por este metodo.
        return None  # Devuelve el dato calculado por este metodo.

    @property  # Aporta un dato o una instruccion para el comportamiento indicado.
    def victoria(self):  # Define la metodo victoria: indica si todas las zonas ya se completaron.
        return self.actual is None  # Devuelve el dato calculado por este metodo.

    def _aviso(self, lineas, segundos=3.0):  # Define la metodo _aviso: guarda el mensaje de interfaz y cuanto tiempo se muestra.
        self.aviso, self.t_aviso = lineas, segundos  # Guarda en el objeto aviso, self.

    def bloquea(self, rect):  # Define la metodo bloquea: determina si la barrera impide salir de la zona activa.
        z = self.actual  # Calcula o guarda altura visual del salto sobre el suelo para el resto del metodo.
        if z is None or not z["cerrada"] or z["estado"] not in ("preparando", "activa"):  # Evalua la condicion que decide el comportamiento siguiente.
            return False  # Devuelve False para comunicar el resultado de la comprobacion.
        return not z["rect"].contains(rect)  # Devuelve el dato calculado por este metodo.

    # Avanza el estado de la zona activa, contabiliza bajas y gestiona sus recompensas.
    def actualizar(self, dt, jugador, enemigos):  # Define la metodo actualizar: actualiza movimiento, combate, vida y animacion del jugador.
        self.t += dt  # Guarda en el objeto t +.
        self.t_aviso -= dt  # Guarda en el objeto t_aviso -.
        self.t_barrera -= dt  # Guarda en el objeto t_barrera -.
        z = self.actual  # Calcula o guarda altura visual del salto sobre el suelo para el resto del metodo.
        if z is None or jugador.muerto:  # Evalua la condicion que decide el comportamiento siguiente.
            return  # Aporta un dato o una instruccion para el comportamiento indicado.
        for e in enemigos:  # Revisa los enemigos para contar bajas o actualizar el encuentro.
            if e.de_oleada and not e.vivo() and not e.contado:  # Evalua la condicion que decide el comportamiento siguiente.
                e.contado = True  # Calcula o guarda e.contado para el resto del metodo.
                z["matados"] += 1  # Guarda el resultado de esta operacion en la estructura indicada.
                base = e.puntos_base  # Calcula o guarda base para el resto del metodo.
                multiplicador = max(  # Calcula o guarda multiplicador para el resto del metodo.
                    0.3,  # Continua la lista de argumentos o valores de esta instruccion.
                    1.0 - 0.7 * z["tiempo_oleada"] / PUNTUACION_TIEMPO_MAX_REDUCCION,  # Continua la lista de argumentos o valores de esta instruccion.
                )  # Cierra la llamada o coleccion de datos iniciada anteriormente.
                puntos = round(base * multiplicador)  # Calcula o guarda puntos para el resto del metodo.
                self.puntuacion += puntos  # Guarda en el objeto puntuacion +.
                z["puntos_ganados"] += puntos  # Guarda el resultado de esta operacion en la estructura indicada.
        dentro = z["rect"].collidepoint(jugador.rect.center)  # Calcula o guarda dentro para el resto del metodo.
        if z["estado"] == "pendiente":  # si la oleada espera, comprueba la entrada del jugador
            if z["rect"].inflate(-2 * OLEADA_MARGEN_ENTRADA, -2 * OLEADA_MARGEN_ENTRADA).contains(jugador.rect):  # Evalua la condicion que decide el comportamiento siguiente.
                z.update(estado="preparando", generados=0, matados=0, t_prep=OLEADA_ESPERA, t_spawn=0.0)  # Calcula o guarda z.update(estado para el resto del metodo.
                if z["reja_temporal"] is not None:
                    mapa.reja_temporal = z["reja_temporal"]
                reproducir_sonido("inicio_oleada")  # Reproduce el efecto de sonido de esta accion.
                self._aviso([f"OLEADA {z['nivel']} - {z['nombre']}"] + (["Zona cerrada: elimina a todos para poder salir"] if z["cerrada"] else []), 3.0)  # Programa el aviso que se mostrara en pantalla.
        elif not dentro and z["cerrada"]:  # Evalua la condicion que decide el comportamiento siguiente.
            self._cancelar(z, enemigos)  # Cancela la oleada y elimina los enemigos activos de ella.
        elif z["estado"] == "preparando" and dentro:  # si el jugador sigue dentro, cuenta la preparacion
            z["t_prep"] -= dt  # Guarda el resultado de esta operacion en la estructura indicada.
            if z["t_prep"] <= 0:  # Evalua la condicion que decide el comportamiento siguiente.
                z.update(estado="activa", tiempo_oleada=0.0, puntos_ganados=0)  # Calcula o guarda z.update(estado para el resto del metodo.
                self._aviso([f"OLEADA {z['nivel']}!"], 2.0)  # Programa el aviso que se mostrara en pantalla.
        if z["jefe"] and z["tipo_jefe"] == "orco":  # Evalua la condicion que decide el comportamiento siguiente.
            jefe_orco = next(  # Calcula o guarda jefe_orco para el resto del metodo.
                (e for e in enemigos if getattr(e, "tipo_jefe", None) == "orco" and not e.vivo()),  # Continua la lista de argumentos o valores de esta instruccion.
                None,  # Continua la lista de argumentos o valores de esta instruccion.
            )  # Cierra la llamada o coleccion de datos iniciada anteriormente.
            if jefe_orco is not None:  # Evalua la condicion que decide el comportamiento siguiente.
                enemigos.lista[:] = [e for e in enemigos if e is jefe_orco]  # Calcula o guarda enemigos.lista[:] para el resto del metodo.
                enemigos.proyectiles.clear()  # Aporta un dato o una instruccion para el comportamiento indicado.
        if z["estado"] == "activa":  # si la oleada esta activa, avanza su cronometro
            z["tiempo_oleada"] += dt  # Guarda el resultado de esta operacion en la estructura indicada.
        if z["estado"] == "activa" and dentro:  # si la oleada activa tiene al jugador dentro, gestiona apariciones
            vivos = sum(1 for e in enemigos if e.de_oleada and e.vivo())  # Calcula o guarda vivos para el resto del metodo.
            z["t_spawn"] = max(0.0, z["t_spawn"] - dt)  # Guarda el resultado de esta operacion en la estructura indicada.
            if z["generados"] < z["total"]:  # Evalua la condicion que decide el comportamiento siguiente.
                if vivos < z["max_vivos"] and z["t_spawn"] <= 0:  # Evalua la condicion que decide el comportamiento siguiente.
                    self._generar(z, jugador, enemigos)  # Crea el siguiente enemigo de la oleada.
                    z["t_spawn"] = z["intervalo"]  # Guarda el resultado de esta operacion en la estructura indicada.
            elif vivos == 0:  # si ya no quedan enemigos vivos, completa la oleada
                z["estado"] = "completada"  # Guarda el resultado de esta operacion en la estructura indicada.
                reproducir_sonido("completar_oleada")  # Reproduce el efecto de sonido de esta accion.
                if z["reja_temporal"] is not None:
                    mapa.reja_temporal = None
                puertas_abiertas = mapa.abrir_puertas(z["puertas"])  # Abre solo las puertas de la zona que acaba de completarse.
                if self.victoria:  # Evalua la condicion que decide el comportamiento siguiente.
                    self._aviso(["TODAS LAS OLEADAS COMPLETADAS!"], 5.0)  # Programa el aviso que se mostrara en pantalla.
                else:  # Inicia el caso alternativo cuando la condicion anterior no se cumple.
                    lineas = [f"OLEADA {z['nivel']} COMPLETADA!"]  # Calcula o guarda lineas para el resto del metodo.
                    if z["cerrada"]:  # Evalua la condicion que decide el comportamiento siguiente.
                        lineas.append("La zona se ha abierto: puedes salir")  # Aporta un dato o una instruccion para el comportamiento indicado.
                    if puertas_abiertas:  # Evalua la condicion que decide el comportamiento siguiente.
                        lineas.append("Las puertas de la siguiente zona se han abierto")  # Aporta un dato o una instruccion para el comportamiento indicado.
                    self._aviso(lineas, 4.0)  # Programa el aviso que se mostrara en pantalla.
        if self.bloquea(jugador.rect.inflate(16, 16)) and not self.bloquea(jugador.rect):  # Evalua la condicion que decide el comportamiento siguiente.
            self.t_barrera = 1.2  # Guarda en el objeto tiempo restante del aviso de barrera.

    # Reinicia una oleada cerrada cuando el jugador abandona su zona.
    def _cancelar(self, z, enemigos):  # Define la metodo _cancelar: reinicia la oleada si el jugador abandona una zona cerrada.
        z.update(  # Aporta un dato o una instruccion para el comportamiento indicado.
            estado="pendiente", generados=0, matados=0,  # Calcula o guarda estado para el resto del metodo.
            tiempo_oleada=0.0, puntos_ganados=0,  # Calcula o guarda tiempo_oleada para el resto del metodo.
        )  # Cierra la llamada o coleccion de datos iniciada anteriormente.
        for e in enemigos:  # Revisa los enemigos para contar bajas o actualizar el encuentro.
            if e.de_oleada and e.vivo():  # Evalua la condicion que decide el comportamiento siguiente.
                e.vida = 0  # Calcula o guarda e.vida para el resto del metodo.
                e.t_muerte = 0.0  # Calcula o guarda e.t_muerte para el resto del metodo.
                e.contado = True  # Calcula o guarda e.contado para el resto del metodo.
        self._aviso(["Has salido de la zona: la oleada se detuvo", "Vuelve a entrar para empezarla de nuevo"], 4.0)  # Programa el aviso que se mostrara en pantalla.

    # Crea un enemigo o jefe en una casilla válida, lejos del jugador si es posible.
    def _generar(self, z, jugador, enemigos):  # Define la metodo _generar: crea un enemigo o jefe en un punto de aparicion valido.
        jx, jy = jugador.rect.center  # Calcula o guarda jx para el resto del metodo.
        lejos = [p for p in z["puntos"] if math.hypot(p[0] - jx, p[1] - jy) >= z["dist"]]  # Aporta un dato o una instruccion para el comportamiento indicado.
        punto = random.choice(lejos) if lejos else max(z["puntos"], key=lambda p: math.hypot(p[0] - jx, p[1] - jy))  # Elige una opcion aleatoria de la lista.
        if z["jefe"]:  # Evalua la condicion que decide el comportamiento siguiente.
            e = Jefe(  # Calcula o guarda e para el resto del metodo.
                punto[0], punto[1], aparicion=ENEMIGO_TIEMPO_APARICION,  # Calcula o guarda punto[0] para el resto del metodo.
                tipo=z["tipo_jefe"], sprite=z["sprite_jefe"],  # Calcula o guarda tipo para el resto del metodo.
                tipos_apoyo=z["tipos_apoyo"], puntos_apoyo=z["puntos"],  # Calcula o guarda tipos_apoyo para el resto del metodo.
                max_apoyos=z["max_apoyos"],  # Calcula o guarda max_apoyos para el resto del metodo.
            )  # Cierra la llamada o coleccion de datos iniciada anteriormente.
        else:  # Inicia el caso alternativo cuando la condicion anterior no se cumple.
            tipo = random.choice(z["tipos_enemigos"])  # Elige una opcion aleatoria de la lista.
            e = Enemigo(  # Calcula o guarda e para el resto del metodo.
                punto[0], punto[1], agresivo=ENEMIGOS_OLEADA_AGRESIVOS,  # Calcula o guarda punto[0] para el resto del metodo.
                aparicion=ENEMIGO_TIEMPO_APARICION, tipo=tipo,  # Calcula o guarda aparicion para el resto del metodo.
            )  # Cierra la llamada o coleccion de datos iniciada anteriormente.
        e.de_oleada = True  # Calcula o guarda e.de_oleada para el resto del metodo.
        enemigos.agregar(e)  # Aporta un dato o una instruccion para el comportamiento indicado.
        z["generados"] += 1  # Guarda el resultado de esta operacion en la estructura indicada.

    def dibujar_perimetro(self, superficie, cam):  # Define la metodo dibujar_perimetro: dibuja el limite visual de las zonas cerradas.
        pantalla = superficie.get_rect()  # Calcula o guarda pantalla para el resto del metodo.
        G = 44  # Calcula o guarda G para el resto del metodo.
        for z in self.zonas:  # Recorre las zonas para buscar la activa o dibujar sus limites.
            if z["estado"] == "completada" or not z["cerrada"]:  # Evalua la condicion que decide el comportamiento siguiente.
                continue  # Salta al siguiente elemento del ciclo.
            r = z["rect"].move(-cam[0], -cam[1])  # Calcula o guarda r para el resto del metodo.
            if not r.colliderect(pantalla):  # Evalua la condicion que decide el comportamiento siguiente.
                continue  # Salta al siguiente elemento del ciclo.
            activa = z["estado"] in ("preparando", "activa")  # Calcula o guarda activa para el resto del metodo.
            fuerza = 0.65 + 0.35 * math.sin(self.t * 4) if activa else 0.30  # Calcula o guarda fuerza para el resto del metodo.
            r0, g0, b0 = z["color"]  # Calcula o guarda r0 para el resto del metodo.
            for lado in ("arriba", "abajo", "izq", "der"):  # Inicia un ciclo para procesar cada elemento indicado.
                horizontal = lado in ("arriba", "abajo")  # Calcula o guarda horizontal para el resto del metodo.
                # Calcula donde dibujar la banda luminosa en el borde seleccionado de la zona.
                pos = (r.x, r.y if lado in ("arriba", "izq") else r.bottom - G) if horizontal else \
                      (r.x if lado == "izq" else r.right - G, r.y)  # Completa la posicion horizontal o vertical de la banda.
                tam = (r.w, G) if horizontal else (G, r.h)  # Calcula o guarda tam para el resto del metodo.
                vis = pygame.Rect(pos, tam).clip(pantalla)  # Crea un rectangulo usado como posicion o hitbox.
                if vis.w <= 0 or vis.h <= 0:  # Evalua la condicion que decide el comportamiento siguiente.
                    continue  # Salta al siguiente elemento del ciclo.
                banda = pygame.Surface(vis.size, pygame.SRCALPHA)  # Crea una superficie grafica para dibujar un efecto.
                for k in range(G):  # Repite la operacion por cada indice o paso de este rango.
                    d = k if lado in ("arriba", "izq") else G - 1 - k  # Calcula o guarda d para el resto del metodo.
                    a = int(150 * fuerza * (1 - d / G) ** 1.6)  # Calcula o guarda a para el resto del metodo.
                    if horizontal:  # Evalua la condicion que decide el comportamiento siguiente.
                        fila = pos[1] + k - vis.y  # Calcula o guarda fila para el resto del metodo.
                        if 0 <= fila < vis.h:  # Evalua la condicion que decide el comportamiento siguiente.
                            pygame.draw.line(banda, (r0, g0, b0, a), (0, fila), (vis.w, fila))  # Dibuja el elemento de interfaz o efecto visual indicado.
                    else:  # Inicia el caso alternativo cuando la condicion anterior no se cumple.
                        col = pos[0] + k - vis.x  # Calcula o guarda col para el resto del metodo.
                        if 0 <= col < vis.w:  # Evalua la condicion que decide el comportamiento siguiente.
                            pygame.draw.line(banda, (r0, g0, b0, a), (col, 0), (col, vis.h))  # Dibuja el elemento de interfaz o efecto visual indicado.
                superficie.blit(banda, vis.topleft)  # Pinta el sprite o capa sobre la superficie de juego.
            brillo = 0.45 + 0.55 * fuerza  # Calcula o guarda brillo para el resto del metodo.
            pygame.draw.rect(superficie, (int(r0 * brillo), int(g0 * brillo), int(b0 * brillo)), r, 4)  # Dibuja el elemento de interfaz o efecto visual indicado.

    def _vineta(self, color):  # Define la metodo _vineta: genera y cachea el efecto de color de una zona.
        if color not in self._vinetas:  # Evalua la condicion que decide el comportamiento siguiente.
            pequena = pygame.Surface((48, 27), pygame.SRCALPHA)  # Crea una superficie grafica para dibujar un efecto.
            for y in range(27):  # Repite la operacion por cada indice o paso de este rango.
                for x in range(48):  # Repite la operacion por cada indice o paso de este rango.
                    d = math.hypot((x - 23.5) / 23.5, (y - 13) / 13) / 1.414  # Calcula o guarda d para el resto del metodo.
                    pequena.set_at((x, y), (*color, int(95 * min(1.0, max(0.0, (d - 0.45) / 0.55)) ** 2)))  # Aporta un dato o una instruccion para el comportamiento indicado.
            self._vinetas[color] = pygame.transform.smoothscale(pequena, (width, height))  # Guarda en el objeto _vinetas[color].
        return self._vinetas[color]  # Devuelve el dato calculado por este metodo.

    def dibujar_vineta(self, superficie, jugador):  # Define la metodo dibujar_vineta: aplica el color ambiental de la zona activa.
        z = self.actual  # Calcula o guarda altura visual del salto sobre el suelo para el resto del metodo.
        if z is not None and z["estado"] in ("preparando", "activa") and z["rect"].collidepoint(jugador.rect.center):  # Evalua la condicion que decide el comportamiento siguiente.
            superficie.blit(self._vineta(z["color"]), (0, 0))  # Pinta el sprite o capa sobre la superficie de juego.

    def direccion_flecha(self, jugador):  # Define la metodo direccion_flecha: calcula la direccion y ruta hasta el siguiente objetivo.
        z = self.actual  # Calcula o guarda altura visual del salto sobre el suelo para el resto del metodo.
        if z is None or jugador.muerto or z["rect"].collidepoint(jugador.rect.center):  # Evalua la condicion que decide el comportamiento siguiente.
            return None  # Devuelve el dato calculado por este metodo.
        origen = pygame.Vector2(jugador.rect.center)  # Crea un vector para posicion, direccion o movimiento.
        destino = pygame.Vector2(z["destino"])  # Crea un vector para posicion, direccion o movimiento.
        objetivo = destino  # Calcula o guarda objetivo para el resto del metodo.
        if not mapa.paso_libre(origen, destino, jugador.rect.w, jugador.rect.h):  # Evalua la condicion que decide el comportamiento siguiente.
            if self.t >= self.t_ruta:  # Evalua la condicion que decide el comportamiento siguiente.
                self.t_ruta = self.t + 0.4  # Guarda en el objeto momento en que se vuelve a calcular la ruta guia.
                self.objetivo_flecha = None  # Guarda en el objeto proximo punto transitable de la ruta guia.
                for p in mapa.camino(origen, destino):  # Inicia un ciclo para procesar cada elemento indicado.
                    if not mapa.paso_libre(origen, p, jugador.rect.w, jugador.rect.h):  # Evalua la condicion que decide el comportamiento siguiente.
                        break  # Termina el ciclo porque ya se encontro el resultado.
                    self.objetivo_flecha = pygame.Vector2(p)  # Crea un vector para posicion, direccion o movimiento.
            if self.objetivo_flecha is not None:  # Evalua la condicion que decide el comportamiento siguiente.
                objetivo = self.objetivo_flecha  # Calcula o guarda objetivo para el resto del metodo.
        d = objetivo - origen  # Calcula o guarda d para el resto del metodo.
        if d.length() < 1:  # Evalua la condicion que decide el comportamiento siguiente.
            d = destino - origen if (destino - origen).length() >= 1 else pygame.Vector2(1, 0)  # Crea un vector para posicion, direccion o movimiento.
        return d.normalize(), (destino - origen).length() / TAM_TILE  # Devuelve el dato calculado por este metodo.

    def dibujar_flecha(self, superficie, jugador, cam):  # Define la metodo dibujar_flecha: dibuja la guia hacia la zona de la siguiente oleada.
        guia = self.direccion_flecha(jugador)  # Calcula o guarda guia para el resto del metodo.
        if guia is None:  # Evalua la condicion que decide el comportamiento siguiente.
            return  # Aporta un dato o una instruccion para el comportamiento indicado.
        direccion, distancia = guia  # Calcula o guarda direccion para el resto del metodo.
        z = self.actual  # Calcula o guarda altura visual del salto sobre el suelo para el resto del metodo.
        centro = pygame.Vector2(jugador.rect.centerx - cam[0], jugador.rect.bottom - 90 - cam[1])  # Crea un vector para posicion, direccion o movimiento.
        pivote = centro + direccion * (170 + 6 * math.sin(self.t * 6))  # Calcula o guarda pivote para el resto del metodo.
        pivote.x = max(220, min(width - 220, pivote.x))  # Calcula o guarda pivote.x para el resto del metodo.
        pivote.y = max(290, min(height - 230, pivote.y))  # Calcula o guarda pivote.y para el resto del metodo.
        perp = pygame.Vector2(-direccion.y, direccion.x)  # Crea un vector para posicion, direccion o movimiento.
        puntos = [pivote + direccion * 34, pivote - direccion * 14 + perp * 24, pivote - direccion * 2, pivote - direccion * 14 - perp * 24]  # Calcula o guarda puntos para el resto del metodo.
        pygame.draw.polygon(superficie, (0, 0, 0), puntos, 6)  # Dibuja el elemento de interfaz o efecto visual indicado.
        pygame.draw.polygon(superficie, z["color"], puntos)  # Dibuja el elemento de interfaz o efecto visual indicado.
        texto_borde(superficie, f"{z['nombre']} - {int(distancia)} casillas", fuente_peq, z["color"], (pivote.x, pivote.y + 44))  # Aporta un dato o una instruccion para el comportamiento indicado.

    def dibujar_hud(self, superficie):  # Define la metodo dibujar_hud: muestra progreso, enemigos restantes y avisos de oleada.
        z = self.actual  # Calcula o guarda altura visual del salto sobre el suelo para el resto del metodo.
        if z is None:  # Evalua la condicion que decide el comportamiento siguiente.
            lineas = ["Campana completada: el Carcelero ha sido derrotado"]  # Calcula o guarda lineas para el resto del metodo.
        else:  # Inicia el caso alternativo cuando la condicion anterior no se cumple.
            lineas = [f"OLEADA {z['nivel']}/{len(self.zonas)} - {z['nombre']}"]  # Calcula o guarda lineas para el resto del metodo.
            if z["estado"] == "pendiente":  # si la oleada espera, comprueba la entrada del jugador
                lineas.append("Entra en la zona (sigue la flecha)")  # Aporta un dato o una instruccion para el comportamiento indicado.
            elif z["estado"] == "preparando":  # Evalua la condicion que decide el comportamiento siguiente.
                lineas.append(f"Comienza en {max(1, math.ceil(z['t_prep']))}...")  # Aporta un dato o una instruccion para el comportamiento indicado.
            else:  # Inicia el caso alternativo cuando la condicion anterior no se cumple.
                restantes = z["total"] - z["matados"]  # Calcula o guarda restantes para el resto del metodo.
                objetivo = "Jefe restante" if z["jefe"] else "Enemigos restantes"  # Calcula o guarda objetivo para el resto del metodo.
                lineas.append(f"{objetivo}: {restantes}" + ("   (zona cerrada)" if z["cerrada"] else ""))  # Aporta un dato o una instruccion para el comportamiento indicado.
        for i, linea in enumerate(lineas):  # Inicia un ciclo para procesar cada elemento indicado.
            texto_borde(superficie, linea, fuente_peq, blanco, (20, 108 + i * 28), centrado=False)  # Calcula o guarda texto_borde(superficie para el resto del metodo.
        if self.t_aviso > 0:  # Evalua la condicion que decide el comportamiento siguiente.
            color = z["color"] if z is not None else amarillo  # Calcula o guarda color para el resto del metodo.
            for i, linea in enumerate(self.aviso):  # Inicia un ciclo para procesar cada elemento indicado.
                texto_borde(superficie, linea, menu_font if i == 0 else fuente_peq, color if i == 0 else blanco, (width // 2, 190 + i * 50))  # Aporta un dato o una instruccion para el comportamiento indicado.
        if self.t_barrera > 0:  # Evalua la condicion que decide el comportamiento siguiente.
            texto_borde(superficie, "No puedes salir hasta terminar la oleada", menu_font, (255, 120, 90), (width // 2, height - 190))  # Aporta un dato o una instruccion para el comportamiento indicado.


print("---------- CONFIGURACION DE ANIMACIONES DEL JUGADOR ----------")  # Aporta un dato o una instruccion para el comportamiento indicado.
CONFIG_ANIM = {  # Calcula o guarda CONFIG_ANIM para el resto del metodo.
    "quieto": (6, True),  # Define los datos de configuracion asociados a quieto.
    "quieto_espada": (6, True),  # Define los datos de configuracion asociados a quieto_espada.
    "caminar": (12, True),  # Define los datos de configuracion asociados a caminar.
    "correr": (16, True),  # Define los datos de configuracion asociados a correr.
    "empujar": (6, True),  # Define los datos de configuracion asociados a empujar.
    "pared": (6, True),  # Define los datos de configuracion asociados a pared.
    "agacharse": (16, False),  # Define los datos de configuracion asociados a agacharse.
    "agachado_quieto": (6, True),  # Define los datos de configuracion asociados a agachado_quieto.
    "agachado_atacar": (18, False),  # Define los datos de configuracion asociados a agachado_atacar.
    "atacar": (20, False),  # Define los datos de configuracion asociados a atacar.
    "atacar2": (20, False),  # Define los datos de configuracion asociados a atacar2.
    "atacar_dash": (20, False),  # Define los datos de configuracion asociados a atacar_dash.
    "atacar_giro": (24, False),  # Define los datos de configuracion asociados a atacar_giro.
    "atacar_abajo": (22, False),  # Define los datos de configuracion asociados a atacar_abajo.
    "saltar": (10, False),  # Define los datos de configuracion asociados a saltar.
    "caer": (10, False),  # Define los datos de configuracion asociados a caer.
    "aterrizar": (16, False),  # Define los datos de configuracion asociados a aterrizar.
    "rodar": (24, False),  # Define los datos de configuracion asociados a rodar.
    "herido": (14, False),  # Define los datos de configuracion asociados a herido.
    "morir": (10, False),  # Define los datos de configuracion asociados a morir.
    "beber": (8, False),  # Define los datos de configuracion asociados a beber.
    "victoria": (8, True),  # Define los datos de configuracion asociados a victoria.
}  # Cierra la llamada o coleccion de datos iniciada anteriormente.


print("---------- CLASE DEL JUGADOR ----------")  # Aporta un dato o una instruccion para el comportamiento indicado.
class Jugador:  # Define la clase Jugador: agrupa instrucciones relacionadas.
    # Mantiene posición, hitboxes, animación, vida, inventario y poderes del personaje.
    def __init__(self, x, y):  # Define la metodo __init__: inicializa los datos y el estado inicial del objeto.
        self.pos = pygame.Vector2(x, y)  # Crea un vector para posicion, direccion o movimiento.
        self.rect = pygame.Rect(0, 0, int(HITBOX_JUGADOR_PIES[0] * escala_jugador), int(HITBOX_JUGADOR_PIES[1] * escala_jugador))  # Crea un rectangulo usado como posicion o hitbox.
        self.rect.center = self.pos  # Guarda en el objeto hitbox de pies o rectangulo que ocupa el personaje.

        self.vel_caminar = VEL_JUGADOR_CAMINAR  # Guarda en el objeto velocidad al caminar.
        self.vel_correr = VEL_JUGADOR_CORRER  # Guarda en el objeto velocidad al correr.
        self.vel_agachado = VEL_JUGADOR_AGACHADO  # Guarda en el objeto velocidad mientras esta agachado.
        self.vel_rodar = VEL_JUGADOR_RODAR  # Guarda en el objeto velocidad durante la rodada.
        self.vel_aire = VEL_JUGADOR_CAMINAR  # Guarda en el objeto velocidad horizontal mientras esta en el aire.

        self.anim = "quieto"  # Guarda en el objeto nombre de la animacion actual.
        self.indice_frame = 0.0  # Guarda en el objeto posicion actual dentro de los fotogramas.
        self.reversa = False  # Guarda en el objeto si la animacion se reproduce al reves.
        self.anim_terminada = False  # Guarda en el objeto si ya concluyo una animacion no repetida.
        self.mirando = 1  # Guarda en el objeto orientacion horizontal del personaje.
        self.imagen = ANIMACIONES["quieto"]["der"][0]  # Guarda en el objeto sprite que se dibuja en el fotograma actual.
        self.alto_cuerpo = self.imagen.get_bounding_rect().height  # Guarda en el objeto altura de la imagen usada para ubicar la hitbox corporal.

        self.accion = None  # Guarda en el objeto accion especial o ataque que se esta ejecutando.
        self.agachado = False  # Guarda en el objeto estado de postura del jugador.
        self.muerto = False  # Guarda en el objeto estado de derrota del jugador.
        self.z = 0.0  # Guarda en el objeto altura visual del salto sobre el suelo.
        self.vz = 0.0  # Guarda en el objeto velocidad vertical del salto.
        self.en_aire = False  # Guarda en el objeto indica si el jugador esta saltando o cayendo.
        self.dir_accion = pygame.Vector2(1, 0)  # Crea un vector para posicion, direccion o movimiento.
        self.empuje = pygame.Vector2(0, 0)  # Crea un vector para posicion, direccion o movimiento.
        self.combo = 0  # Guarda en el objeto siguiente golpe de la secuencia alternada.
        self.t_combo = 0.0  # Guarda en el objeto tiempo disponible para continuar el combo.
        self.tiempo_espada = 0.0  # Guarda en el objeto tiempo restante de la animacion de espada.
        self.cd_giro = 0.0  # Guarda en el objeto tiempo de enfriamiento del ataque giratorio.
        self.vida_max = VIDA_JUGADOR  # Guarda en el objeto vida maxima.
        self.vida = self.vida_max  # Guarda en el objeto vida actual.
        self.vida_visible = float(self.vida_max)  # Guarda en el objeto valor suavizado que se muestra en la barra de vida.
        self.pociones = 0  # Guarda en el objeto cantidad de pociones del inventario.
        self.invulnerable = 0.0  # Guarda en el objeto tiempo restante sin recibir otro dano.
        self.golpeados = set()  # Guarda en el objeto enemigos ya alcanzados por este ataque.
        self.celebrar_pendiente = False  # Guarda en el objeto si queda por iniciar la celebracion de victoria.
        self.victoria_hecha = False  # Guarda en el objeto si la celebracion ya fue activada.
        self.prev = {}  # Guarda en el objeto estados de teclas del fotograma anterior.
        self.enfriamiento = 0.3  # Guarda en el objeto tiempo restante hasta el siguiente ataque.
        self.bonificaciones = {"viento": 0, "dano": 0, "berserker": 0}  # Guarda en el objeto niveles de mejoras permanentes del jugador.
        self.ataques_lanzados = 0  # Guarda en el objeto contador para la mejora del tajo de viento.
        self.ataque_id = 0  # Guarda en el objeto identificador del ataque actual.
        self.tajo_viento_pendiente = False  # Guarda en el objeto si hay un proyectil de viento por generar.
        self.berserker_tiempo = 0.0  # Guarda en el objeto duracion restante del modo berserker.
        self.berserker_enfriamiento = 0.0  # Guarda en el objeto tiempo hasta poder activar berserker otra vez.

    @property  # Aporta un dato o una instruccion para el comportamiento indicado.
    def berserker_activo(self):  # Define la metodo berserker_activo: indica si el poder berserker esta activo.
        return self.berserker_tiempo > 0  # Devuelve el dato calculado por este metodo.

    @property  # Aporta un dato o una instruccion para el comportamiento indicado.
    def multiplicador_dano(self):  # Define la metodo multiplicador_dano: calcula el aumento de dano de las mejoras activas.
        return (1 + self.bonificaciones["dano"] * 0.15) * (1.0 + 0.2 * self.bonificaciones["berserker"] if self.berserker_activo else 1.0)  # Devuelve el dato calculado por este metodo.

    @property  # Aporta un dato o una instruccion para el comportamiento indicado.
    def multiplicador_velocidad(self):  # Define la metodo multiplicador_velocidad: calcula el aumento de velocidad berserker.
        return 1.0 + 0.12 * self.bonificaciones["berserker"] if self.berserker_activo else 1.0  # Devuelve el dato calculado por este metodo.

    @property  # Aporta un dato o una instruccion para el comportamiento indicado.
    def multiplicador_dano_recibido(self):  # Define la metodo multiplicador_dano_recibido: calcula la reduccion de dano berserker.
        return max(0.55, 1.0 - 0.12 * self.bonificaciones["berserker"]) if self.berserker_activo else 1.0  # Devuelve el dato calculado por este metodo.

    # Cuenta golpes y activa el proyectil de viento con la frecuencia de la mejora.
    def registrar_ataque(self):  # Define la metodo registrar_ataque: cuenta ataques y prepara el tajo de viento mejorado.
        nivel = self.bonificaciones["viento"]  # Calcula o guarda nivel para el resto del metodo.
        if nivel == 0:  # Evalua la condicion que decide el comportamiento siguiente.
            return False  # Devuelve False para comunicar el resultado de la comprobacion.
        self.ataques_lanzados += 1  # Guarda en el objeto ataques_lanzados +.
        cada_cuantos = max(1, 4 - nivel)  # Calcula o guarda cada_cuantos para el resto del metodo.
        if self.ataques_lanzados >= cada_cuantos:  # Evalua la condicion que decide el comportamiento siguiente.
            self.ataques_lanzados = 0  # Guarda en el objeto contador para la mejora del tajo de viento.
            self.tajo_viento_pendiente = True  # Guarda en el objeto si hay un proyectil de viento por generar.
            return True  # Devuelve True para comunicar el resultado de la comprobacion.
        return False  # Devuelve False para comunicar el resultado de la comprobacion.

    # Activa temporalmente el poder berserker si está mejorado y no está en enfriamiento.
    def activar_berserker(self):  # Define la metodo activar_berserker: activa el poder berserker si esta disponible.
        nivel = self.bonificaciones["berserker"]  # Calcula o guarda nivel para el resto del metodo.
        if nivel and self.berserker_enfriamiento <= 0 and not self.berserker_activo:  # Evalua la condicion que decide el comportamiento siguiente.
            self.berserker_tiempo = 5.0 + 2.0 * nivel  # Guarda en el objeto duracion restante del modo berserker.
            self.berserker_enfriamiento = 20.0 - 2.0 * nivel  # Guarda en el objeto tiempo hasta poder activar berserker otra vez.
            reproducir_sonido("activar_berserker")  # Reproduce el efecto de sonido de esta accion.
            return True  # Devuelve True para comunicar el resultado de la comprobacion.
        return False  # Devuelve False para comunicar el resultado de la comprobacion.

    # Consume una poción y recupera hasta 30 puntos sin exceder la vida máxima.
    def beber_pocion(self):  # Define la metodo beber_pocion: consume una pocion y recupera vida.
        if self.pociones <= 0 or self.vida >= self.vida_max or self.muerto:  # Evalua la condicion que decide el comportamiento siguiente.
            return False  # Devuelve False para comunicar el resultado de la comprobacion.
        self.pociones -= 1  # Guarda en el objeto pociones -.
        self.vida = min(self.vida_max, self.vida + 30)  # Guarda en el objeto vida actual.
        self.vida_visible = max(self.vida_visible, float(self.vida))  # Guarda en el objeto valor suavizado que se muestra en la barra de vida.
        return True  # Devuelve True para comunicar el resultado de la comprobacion.

    # Cambia la animación y configura su dirección de reproducción y fotograma inicial.
    def poner_anim(self, nombre, reversa=False, reiniciar=False):  # Define la metodo poner_anim: cambia la animacion y reinicia sus fotogramas si hace falta.
        if reiniciar or nombre != self.anim or reversa != self.reversa:  # Evalua la condicion que decide el comportamiento siguiente.
            self.anim = nombre  # Guarda en el objeto nombre de la animacion actual.
            self.reversa = reversa  # Guarda en el objeto si la animacion se reproduce al reves.
            self.anim_terminada = False  # Guarda en el objeto si ya concluyo una animacion no repetida.
            n = len(ANIMACIONES[nombre]["der"])  # Calcula o guarda n para el resto del metodo.
            self.indice_frame = n - 0.001 if reversa else 0.0  # Guarda en el objeto posicion actual dentro de los fotogramas.

    def avanzar_anim(self, dt):  # Define la metodo avanzar_anim: avanza la animacion segun el tiempo y su velocidad.
        fps, repite = CONFIG_ANIM[self.anim]  # Calcula o guarda fps para el resto del metodo.
        n = len(ANIMACIONES[self.anim]["der"])  # Calcula o guarda n para el resto del metodo.
        if self.reversa:  # Evalua la condicion que decide el comportamiento siguiente.
            self.indice_frame -= fps * dt  # Guarda en el objeto indice_frame -.
            if self.indice_frame < 0:  # Evalua la condicion que decide el comportamiento siguiente.
                if repite:  # Evalua la condicion que decide el comportamiento siguiente.
                    self.indice_frame += n  # Guarda en el objeto indice_frame +.
                else:  # Inicia el caso alternativo cuando la condicion anterior no se cumple.
                    self.indice_frame = 0.0  # Guarda en el objeto posicion actual dentro de los fotogramas.
                    self.anim_terminada = True  # Guarda en el objeto si ya concluyo una animacion no repetida.
        else:  # Inicia el caso alternativo cuando la condicion anterior no se cumple.
            self.indice_frame += fps * dt  # Guarda en el objeto indice_frame +.
            if self.indice_frame >= n:  # Evalua la condicion que decide el comportamiento siguiente.
                if repite:  # Evalua la condicion que decide el comportamiento siguiente.
                    self.indice_frame %= n  # Guarda en el objeto indice_frame %.
                else:  # Inicia el caso alternativo cuando la condicion anterior no se cumple.
                    self.indice_frame = n - 0.001  # Guarda en el objeto posicion actual dentro de los fotogramas.
                    self.anim_terminada = True  # Guarda en el objeto si ya concluyo una animacion no repetida.

    def progreso(self):  # Define la metodo progreso: calcula cuanto ha avanzado la animacion actual.
        n = len(ANIMACIONES[self.anim]["der"])  # Calcula o guarda n para el resto del metodo.
        p = self.indice_frame / n  # Calcula o guarda p para el resto del metodo.
        return 1 - p if self.reversa else p  # Devuelve el dato calculado por este metodo.

    def elegir_imagen(self):  # Define la metodo elegir_imagen: selecciona el fotograma y orientacion que se dibujan.
        frames = ANIMACIONES[self.anim]["der" if self.mirando == 1 else "izq"]  # Aporta un dato o una instruccion para el comportamiento indicado.
        self.imagen = frames[min(int(self.indice_frame), len(frames) - 1)]  # Guarda en el objeto sprite que se dibuja en el fotograma actual.

    def empezar(self, nombre, lado=None):  # Define la metodo empezar: inicia una accion, anima al jugador y reproduce su sonido.
        self.accion = nombre  # Guarda en el objeto accion especial o ataque que se esta ejecutando.
        sonidos_accion = {  # Calcula o guarda sonidos_accion para el resto del metodo.
            "rodar": "rodar",  # Define los datos de configuracion asociados a rodar.
            "atacar": "ataque_espada",  # Define los datos de configuracion asociados a atacar.
            "atacar2": "ataque_espada",  # Define los datos de configuracion asociados a atacar2.
            "atacar_dash": "ataque_embestida",  # Define los datos de configuracion asociados a atacar_dash.
            "atacar_abajo": "ataque_aereo",  # Define los datos de configuracion asociados a atacar_abajo.
            "atacar_giro": "ataque_giro",  # Define los datos de configuracion asociados a atacar_giro.
            "agachado_atacar": "ataque_espada",  # Define los datos de configuracion asociados a agachado_atacar.
            "herido": "dano_jugador",  # Define los datos de configuracion asociados a herido.
            "morir": "derrota_jugador",  # Define los datos de configuracion asociados a morir.
            "victoria": "victoria",  # Define los datos de configuracion asociados a victoria.
            "beber": "curacion_pocion",  # Define los datos de configuracion asociados a beber.
        }  # Cierra la llamada o coleccion de datos iniciada anteriormente.
        sonido = sonidos_accion.get(nombre)  # Calcula o guarda sonido para el resto del metodo.
        if sonido:  # Evalua la condicion que decide el comportamiento siguiente.
            reproducir_sonido(  # Reproduce el efecto de sonido de esta accion.
                sonido,  # Continua la lista de argumentos o valores de esta instruccion.
                reemplazar=SONIDOS_ATAQUE if nombre in HITBOX_ATAQUES else (),  # Calcula o guarda reemplazar para el resto del metodo.
            )  # Cierra la llamada o coleccion de datos iniciada anteriormente.
        if nombre in HITBOX_ATAQUES:  # Evalua la condicion que decide el comportamiento siguiente.
            self.ataque_id += 1  # Guarda en el objeto ataque_id +.
            self.golpeados = set()  # Guarda en el objeto enemigos ya alcanzados por este ataque.
            self.registrar_ataque()  # Consulta o modifica el estado del objeto actual.
        if lado is not None:  # Evalua la condicion que decide el comportamiento siguiente.
            self.mirando = lado  # Guarda en el objeto orientacion horizontal del personaje.
        if nombre == "levantarse":  # Evalua la condicion que decide el comportamiento siguiente.
            self.poner_anim("agacharse", reversa=True, reiniciar=True)  # Cambia la animacion visual del jugador.
        else:  # Inicia el caso alternativo cuando la condicion anterior no se cumple.
            self.poner_anim(nombre, reiniciar=True)  # Cambia la animacion visual del jugador.

    # Aplica defensas, muestra el daño y decide si el jugador es herido o derrotado.
    def recibir_dano(self, cantidad=10, origen=None):  # Define la metodo recibir_dano: aplica defensas, quita vida y decide si hiere o mata.
        if self.muerto or self.accion == "rodar" or self.invulnerable > 0:  # Evalua la condicion que decide el comportamiento siguiente.
            return False  # Devuelve False para comunicar el resultado de la comprobacion.
        dano_final = max(1, round(cantidad * self.multiplicador_dano_recibido))  # Calcula o guarda dano_final para el resto del metodo.
        self.vida = max(0, self.vida - dano_final)  # Guarda en el objeto vida actual.
        texto_dano(dano_final, self.rect.centerx, self.rect.bottom - self.alto_cuerpo - self.z, (255, 70, 70))  # Aporta un dato o una instruccion para el comportamiento indicado.
        self.invulnerable = INVULNERABLE_TRAS_GOLPE  # Guarda en el objeto tiempo restante sin recibir otro dano.
        if self.vida <= 0:  # Evalua la condicion que decide el comportamiento siguiente.
            self.morir()  # Consulta o modifica el estado del objeto actual.
            return True  # Devuelve True para comunicar el resultado de la comprobacion.
        self.agachado = False  # Guarda en el objeto estado de postura del jugador.
        retroceso = pygame.Vector2(-self.mirando, 0)  # Crea un vector para posicion, direccion o movimiento.
        if origen is not None:  # Evalua la condicion que decide el comportamiento siguiente.
            alejar = pygame.Vector2(self.rect.center) - pygame.Vector2(origen)  # Crea un vector para posicion, direccion o movimiento.
            if alejar.length() > 0:  # Evalua la condicion que decide el comportamiento siguiente.
                retroceso = alejar.normalize()  # Calcula o guarda retroceso para el resto del metodo.
        self.empuje = retroceso * 320  # Guarda en el objeto velocidad de retroceso despues de recibir dano.
        self.empezar("herido")  # Inicia la accion y su animacion correspondiente.
        return True  # Devuelve True para comunicar el resultado de la comprobacion.

    def morir(self):  # Define la metodo morir: marca la derrota y prepara la animacion final.
        self.muerto = True  # Guarda en el objeto estado de derrota del jugador.
        reproducir_sonido("derrota_jugador")  # Reproduce el efecto de sonido de esta accion.
        reproducir_sonido("perder_partida")  # Reproduce el efecto de sonido de esta accion.
        self.accion = None  # Guarda en el objeto accion especial o ataque que se esta ejecutando.
        self.agachado = False  # Guarda en el objeto estado de postura del jugador.
        self.z, self.vz, self.en_aire = 0.0, 0.0, False  # Guarda en el objeto z, self.
        self.poner_anim("morir", reiniciar=True)  # Cambia la animacion visual del jugador.

    def celebrar(self):  # Define la metodo celebrar: programa la animacion de victoria una sola vez.
        if not self.victoria_hecha and not self.muerto:  # Evalua la condicion que decide el comportamiento siguiente.
            self.victoria_hecha = True  # Guarda en el objeto si la celebracion ya fue activada.
            self.celebrar_pendiente = True  # Guarda en el objeto si queda por iniciar la celebracion de victoria.

    def cuerpo(self):  # Define la metodo cuerpo: calcula la hitbox corporal segun la postura del jugador.
        ancho, alto = HITBOX_JUGADOR_CUERPO_AGACHADO if self.agachado else HITBOX_JUGADOR_CUERPO  # Calcula o guarda ancho para el resto del metodo.
        zona = pygame.Rect(0, 0, int(ancho * escala_jugador), int(alto * escala_jugador))  # Crea un rectangulo usado como posicion o hitbox.
        zona.midbottom = (self.rect.centerx, self.rect.bottom - self.z)  # Calcula o guarda zona.midbottom para el resto del metodo.
        return zona  # Devuelve el dato calculado por este metodo.

    def hitbox(self):  # Define la metodo hitbox: calcula la zona activa de impacto del ataque actual.
        if self.accion not in HITBOX_ATAQUES:  # Evalua la condicion que decide el comportamiento siguiente.
            return None  # Devuelve el dato calculado por este metodo.
        n = len(ANIMACIONES[self.anim]["der"])  # Calcula o guarda n para el resto del metodo.
        if not 1 <= int(self.indice_frame) <= n - 2:  # Evalua la condicion que decide el comportamiento siguiente.
            return None  # Devuelve el dato calculado por este metodo.
        ancho, alto = HITBOX_ATAQUES[self.accion]  # Calcula o guarda ancho para el resto del metodo.
        zona = pygame.Rect(0, 0, int(ancho * escala_jugador), int(alto * escala_jugador))  # Crea un rectangulo usado como posicion o hitbox.
        separacion, altura = HITBOX_ATAQUE_POS[self.accion]  # Calcula o guarda separacion para el resto del metodo.
        y = self.rect.bottom - altura * escala_jugador - self.z  # Calcula o guarda y para el resto del metodo.
        if self.accion == "atacar_giro":  # Evalua la condicion que decide el comportamiento siguiente.
            zona.center = (self.rect.centerx, y)  # Calcula o guarda zona.center para el resto del metodo.
        elif self.mirando == 1:  # Evalua la condicion que decide el comportamiento siguiente.
            zona.midleft = (self.rect.centerx + separacion * escala_jugador, y)  # Calcula o guarda zona.midleft para el resto del metodo.
        else:  # Inicia el caso alternativo cuando la condicion anterior no se cumple.
            zona.midright = (self.rect.centerx - separacion * escala_jugador, y)  # Calcula o guarda zona.midright para el resto del metodo.
        return zona  # Devuelve el dato calculado por este metodo.

    def pulsaciones(self, teclas, raton):  # Define la metodo pulsaciones: detecta teclas y botones recien pulsados.
        ahora = {  # Calcula o guarda ahora para el resto del metodo.
            "saltar": teclas[pygame.K_SPACE],  # Define los datos de configuracion asociados a saltar.
            "rodar": teclas[pygame.K_r] or raton[2],  # Define los datos de configuracion asociados a rodar.
            "giro": teclas[pygame.K_e],  # Define los datos de configuracion asociados a giro.
            "beber": teclas[pygame.K_q],  # Define los datos de configuracion asociados a beber.
            "berserker": teclas[pygame.K_v],  # Define los datos de configuracion asociados a berserker.
        }  # Cierra la llamada o coleccion de datos iniciada anteriormente.
        nuevas = {k: bool(v) and not self.prev.get(k, False) for k, v in ahora.items()}  # Calcula o guarda nuevas para el resto del metodo.
        self.prev = {k: bool(v) for k, v in ahora.items()}  # Guarda en el objeto estados de teclas del fotograma anterior.
        return nuevas  # Devuelve el dato calculado por este metodo.

    # Traduce entradas recientes y estado físico en saltos, ataques, esquivas o poses.
    def decidir_accion(self, nuevas, ataca, mueve, corre, direccion, lado_raton, quiere_agachar):  # Define la metodo decidir_accion: elige salto, ataque, rodada, pocion o postura.
        if self.agachado:  # Evalua la condicion que decide el comportamiento siguiente.
            if nuevas["rodar"]:  # Evalua la condicion que decide el comportamiento siguiente.
                self.agachado = False  # Guarda en el objeto estado de postura del jugador.
                self.iniciar_rodar(direccion)  # Consulta o modifica el estado del objeto actual.
            elif ataca:  # si el ataque esta disponible, elige el golpe correspondiente
                self.empezar("agachado_atacar", lado_raton)  # Inicia la accion y su animacion correspondiente.
            elif not quiere_agachar:  # Evalua la condicion que decide el comportamiento siguiente.
                self.empezar("levantarse")  # Inicia la accion y su animacion correspondiente.
            return  # Aporta un dato o una instruccion para el comportamiento indicado.

        if self.en_aire:  # si esta saltando, integra la gravedad y la altura
            if ataca:  # Evalua la condicion que decide el comportamiento siguiente.
                self.empezar("atacar_abajo", lado_raton)  # Inicia la accion y su animacion correspondiente.
            return  # Aporta un dato o una instruccion para el comportamiento indicado.

        if nuevas["saltar"]:  # si se acaba de pulsar salto, inicia el impulso vertical
            self.en_aire = True  # Guarda en el objeto indica si el jugador esta saltando o cayendo.
            self.vz = FUERZA_SALTO  # Guarda en el objeto velocidad vertical del salto.
            self.z = 1.0  # Guarda en el objeto altura visual del salto sobre el suelo.
            self.vel_aire = self.vel_correr if corre else self.vel_caminar  # Guarda en el objeto velocidad horizontal mientras esta en el aire.
            reproducir_sonido("salto")  # Reproduce el efecto de sonido de esta accion.
            self.poner_anim("saltar", reiniciar=True)  # Cambia la animacion visual del jugador.
        elif nuevas["rodar"]:  # si se pulsa rodada, empieza la esquiva
            self.iniciar_rodar(direccion)  # Consulta o modifica el estado del objeto actual.
        elif nuevas["giro"] and self.cd_giro <= 0:  # si el giro esta disponible, inicia su ataque
            self.cd_giro = ENFRIAMIENTO_GIRO  # Guarda en el objeto tiempo de enfriamiento del ataque giratorio.
            self.empezar("atacar_giro", lado_raton)  # Inicia la accion y su animacion correspondiente.
        elif nuevas["beber"]:  # si se pide beber, intenta consumir una pocion
            if self.beber_pocion():  # Evalua la condicion que decide el comportamiento siguiente.
                self.empezar("beber")  # Inicia la accion y su animacion correspondiente.
        elif self.celebrar_pendiente and not mueve and not ataca:  # Evalua la condicion que decide el comportamiento siguiente.
            self.celebrar_pendiente = False  # Guarda en el objeto si queda por iniciar la celebracion de victoria.
            self.empezar("victoria")  # Inicia la accion y su animacion correspondiente.
        elif ataca:  # si el ataque esta disponible, elige el golpe correspondiente
            if corre:  # Evalua la condicion que decide el comportamiento siguiente.
                centro = pygame.Vector2(self.rect.centerx, self.rect.bottom - 40)  # Crea un vector para posicion, direccion o movimiento.
                objetivo = pos_raton_mundo() - centro  # Calcula o guarda objetivo para el resto del metodo.
                self.dir_accion = objetivo.normalize() if objetivo.length() > 0 else pygame.Vector2(lado_raton, 0)  # Crea un vector para posicion, direccion o movimiento.
                self.empezar("atacar_dash", lado_raton)  # Inicia la accion y su animacion correspondiente.
            else:  # Inicia el caso alternativo cuando la condicion anterior no se cumple.
                if self.t_combo <= 0:  # Evalua la condicion que decide el comportamiento siguiente.
                    self.combo = 0  # Guarda en el objeto siguiente golpe de la secuencia alternada.
                self.empezar(("atacar", "atacar2")[self.combo], lado_raton)  # Inicia la accion y su animacion correspondiente.
                self.combo = 1 - self.combo  # Guarda en el objeto siguiente golpe de la secuencia alternada.
        elif quiere_agachar:  # Evalua la condicion que decide el comportamiento siguiente.
            self.empezar("agacharse")  # Inicia la accion y su animacion correspondiente.

    def iniciar_rodar(self, direccion):  # Define la metodo iniciar_rodar: prepara la direccion y animacion de la rodada.
        self.dir_accion = pygame.Vector2(direccion) if direccion.length() > 0 else pygame.Vector2(self.mirando, 0)  # Crea un vector para posicion, direccion o movimiento.
        lado = self.mirando  # Calcula o guarda lado para el resto del metodo.
        if self.dir_accion.x != 0:  # Evalua la condicion que decide el comportamiento siguiente.
            lado = 1 if self.dir_accion.x > 0 else -1  # Calcula o guarda lado para el resto del metodo.
        self.empezar("rodar", lado)  # Inicia la accion y su animacion correspondiente.

    def _mover_chocando(self, paso):  # Define la metodo _mover_chocando: mueve al jugador por ejes sin atravesar obstaculos.
        atascado = mapa_choca(self.rect)  # Calcula o guarda atascado para el resto del metodo.
        for eje in (0, 1):  # Inicia un ciclo para procesar cada elemento indicado.
            d = paso[eje]  # Calcula o guarda d para el resto del metodo.
            if d == 0:  # Evalua la condicion que decide el comportamiento siguiente.
                continue  # Salta al siguiente elemento del ciclo.
            self.pos[eje] += d  # Guarda en el objeto pos[eje] +.
            self.rect.center = self.pos  # Guarda en el objeto hitbox de pies o rectangulo que ocupa el personaje.
            if not atascado and mapa_choca(self.rect):  # Evalua la condicion que decide el comportamiento siguiente.
                self.pos[eje] -= d  # Guarda en el objeto pos[eje] -.
                signo = 1 if d > 0 else -1  # Calcula o guarda signo para el resto del metodo.
                for _ in range(int(abs(d))):  # Repite la operacion por cada indice o paso de este rango.
                    self.pos[eje] += signo  # Guarda en el objeto pos[eje] +.
                    self.rect.center = self.pos  # Guarda en el objeto hitbox de pies o rectangulo que ocupa el personaje.
                    if mapa_choca(self.rect):  # Evalua la condicion que decide el comportamiento siguiente.
                        self.pos[eje] -= signo  # Guarda en el objeto pos[eje] -.
                        break  # Termina el ciclo porque ya se encontro el resultado.
        self.rect.center = self.pos  # Guarda en el objeto hitbox de pies o rectangulo que ocupa el personaje.

    # Avanza lógica, desplazamiento, salto, invulnerabilidad, audio y animación del jugador.
    def actualizar(self, teclas, dt):  # Define la metodo actualizar: actualiza movimiento, combate, vida y animacion del jugador.
        self.enfriamiento -= dt  # Guarda en el objeto enfriamiento -.
        self.cd_giro -= dt  # Guarda en el objeto cd_giro -.
        self.t_combo -= dt  # Guarda en el objeto t_combo -.
        self.tiempo_espada -= dt  # Guarda en el objeto tiempo_espada -.
        self.invulnerable -= dt  # Guarda en el objeto invulnerable -.
        self.berserker_tiempo = max(0.0, self.berserker_tiempo - dt)  # Guarda en el objeto duracion restante del modo berserker.
        self.berserker_enfriamiento = max(0.0, self.berserker_enfriamiento - dt)  # Guarda en el objeto tiempo hasta poder activar berserker otra vez.
        if self.vida_visible > self.vida:  # Evalua la condicion que decide el comportamiento siguiente.
            self.vida_visible = max(self.vida, self.vida_visible - 40 * dt)  # Guarda en el objeto valor suavizado que se muestra en la barra de vida.
        else:  # Inicia el caso alternativo cuando la condicion anterior no se cumple.
            self.vida_visible = self.vida  # Guarda en el objeto valor suavizado que se muestra en la barra de vida.
        raton = pygame.mouse.get_pressed()  # Calcula o guarda raton para el resto del metodo.
        nuevas = self.pulsaciones(teclas, raton)  # Calcula o guarda nuevas para el resto del metodo.

        if self.muerto:  # si el jugador murio, solo conserva su animacion de derrota
            audio_acciones.detener("pasos_caminar", "pasos_correr")  # Aporta un dato o una instruccion para el comportamiento indicado.
            self.poner_anim("morir")  # Cambia la animacion visual del jugador.
            self.avanzar_anim(dt)  # Avanza el fotograma de la animacion con el tiempo.
            self.elegir_imagen()  # Elige la imagen que representa el fotograma actual.
            return  # Aporta un dato o una instruccion para el comportamiento indicado.

        dx = (teclas[pygame.K_d] or teclas[pygame.K_RIGHT]) - (teclas[pygame.K_a] or teclas[pygame.K_LEFT])  # Calcula o guarda dx para el resto del metodo.
        dy = (teclas[pygame.K_s] or teclas[pygame.K_DOWN]) - (teclas[pygame.K_w] or teclas[pygame.K_UP])  # Calcula o guarda dy para el resto del metodo.
        direccion = pygame.Vector2(dx, dy)  # Crea un vector para posicion, direccion o movimiento.
        mueve = direccion.length() > 0  # Calcula o guarda mueve para el resto del metodo.
        if mueve:  # Evalua la condicion que decide el comportamiento siguiente.
            direccion = direccion.normalize()  # Calcula o guarda direccion para el resto del metodo.
        corre = mueve and (teclas[pygame.K_LSHIFT] or teclas[pygame.K_RSHIFT])  # Calcula o guarda corre para el resto del metodo.
        quiere_agachar = teclas[pygame.K_c] or teclas[pygame.K_LCTRL]  # Calcula o guarda quiere_agachar para el resto del metodo.
        lado_raton = -1 if pos_raton_mundo().x < self.rect.centerx else 1  # Calcula o guarda lado_raton para el resto del metodo.
        ataca = raton[0] and self.enfriamiento <= 0  # Aporta un dato o una instruccion para el comportamiento indicado.

        if self.accion == "victoria" and (mueve or ataca or any(nuevas.values())):  # Evalua la condicion que decide el comportamiento siguiente.
            self.accion = None  # Guarda en el objeto accion especial o ataque que se esta ejecutando.
        if nuevas["berserker"]:  # Evalua la condicion que decide el comportamiento siguiente.
            self.activar_berserker()  # Consulta o modifica el estado del objeto actual.
        if self.accion is None:  # si no hay accion bloqueando al jugador, decide una nueva
            self.decidir_accion(nuevas, ataca, mueve, corre, direccion, lado_raton, quiere_agachar)  # Consulta o modifica el estado del objeto actual.

        a = self.accion  # Calcula o guarda a para el resto del metodo.
        p = self.progreso()  # Calcula o guarda p para el resto del metodo.
        mov = pygame.Vector2(0, 0)  # Crea un vector para posicion, direccion o movimiento.
        if a == "rodar":  # Evalua la condicion que decide el comportamiento siguiente.
            mov = self.dir_accion * self.vel_rodar * (1 - 0.5 * p)  # Calcula o guarda mov para el resto del metodo.
        elif a == "atacar_dash":  # Evalua la condicion que decide el comportamiento siguiente.
            mov = self.dir_accion * 520 * max(0.0, 1 - 1.4 * p)  # Calcula o guarda mov para el resto del metodo.
        elif a == "atacar_giro":  # Evalua la condicion que decide el comportamiento siguiente.
            mov = direccion * self.vel_caminar * 0.5  # Calcula o guarda mov para el resto del metodo.
        elif a == "atacar_abajo":  # Evalua la condicion que decide el comportamiento siguiente.
            mov = direccion * self.vel_aire * 0.5 if self.en_aire else mov  # Calcula o guarda mov para el resto del metodo.
        elif a == "herido":  # Evalua la condicion que decide el comportamiento siguiente.
            mov = self.empuje * (1 - p)  # Calcula o guarda mov para el resto del metodo.
        elif a is None:  # Evalua la condicion que decide el comportamiento siguiente.
            if self.en_aire:  # si esta saltando, integra la gravedad y la altura
                mov = direccion * self.vel_aire  # Calcula o guarda mov para el resto del metodo.
            elif self.agachado:  # si sigue agachado, conserva esa animacion y movimiento
                mov = direccion * self.vel_agachado  # Calcula o guarda mov para el resto del metodo.
            else:  # Inicia el caso alternativo cuando la condicion anterior no se cumple.
                mov = direccion * (self.vel_correr if corre else self.vel_caminar)  # Calcula o guarda mov para el resto del metodo.
        self._mover_chocando(mov * self.multiplicador_velocidad * dt)  # Mueve al jugador respetando las colisiones del mapa.
        area = pygame.Rect(0, self.alto_cuerpo - self.rect.h, MUNDO_ANCHO, MUNDO_ALTO - self.alto_cuerpo + self.rect.h)  # Crea un rectangulo usado como posicion o hitbox.
        self.rect.clamp_ip(area)  # Consulta o modifica el estado del objeto actual.
        self.pos.update(self.rect.center)  # Consulta o modifica el estado del objeto actual.
        toca_izq = self.rect.left <= 0 and direccion.x < 0  # Aporta un dato o una instruccion para el comportamiento indicado.
        toca_der = self.rect.right >= MUNDO_ANCHO and direccion.x > 0  # Aporta un dato o una instruccion para el comportamiento indicado.
        contra_pared = toca_izq or toca_der  # Calcula o guarda contra_pared para el resto del metodo.

        if self.en_aire:  # si esta saltando, integra la gravedad y la altura
            g = GRAVEDAD_GOLPE_ABAJO if self.accion == "atacar_abajo" else GRAVEDAD  # Aporta un dato o una instruccion para el comportamiento indicado.
            self.vz -= g * dt  # Guarda en el objeto vz -.
            self.z += self.vz * dt  # Guarda en el objeto z +.
            if self.z <= 0:  # Evalua la condicion que decide el comportamiento siguiente.
                self.z, self.vz, self.en_aire = 0.0, 0.0, False  # Guarda en el objeto z, self.
                if self.accion is None:  # si no hay accion bloqueando al jugador, decide una nueva
                    reproducir_sonido("aterrizaje")  # Reproduce el efecto de sonido de esta accion.
                    self.empezar("aterrizar")  # Inicia la accion y su animacion correspondiente.

        if self.accion is None:  # si no hay accion bloqueando al jugador, decide una nueva
            if self.en_aire:  # si esta saltando, integra la gravedad y la altura
                if contra_pared:  # Evalua la condicion que decide el comportamiento siguiente.
                    self.mirando = 1 if toca_der else -1  # Guarda en el objeto orientacion horizontal del personaje.
                    self.poner_anim("pared")  # Cambia la animacion visual del jugador.
                else:  # Inicia el caso alternativo cuando la condicion anterior no se cumple.
                    self.mirando = lado_raton  # Guarda en el objeto orientacion horizontal del personaje.
                    self.poner_anim("saltar" if self.vz > 0 else "caer")  # Cambia la animacion visual del jugador.
            elif self.agachado:  # si sigue agachado, conserva esa animacion y movimiento
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

    def vivo(self):
        return self.vida > 0

    def cuerpo(self):
        zona = pygame.Rect(0, 0, int(HITBOX_ENEMIGO_CUERPO[0] * self.escala), int(HITBOX_ENEMIGO_CUERPO[1] * self.escala))
        zona.midbottom = self.rect.midbottom
        return zona

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

    def _area(self):
        return pygame.Rect(0, self.alto_img - self.rect.h, MUNDO_ANCHO, MUNDO_ALTO - self.alto_img + self.rect.h)

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

    def _desplazamiento(self):
        a = self.ataque
        if a is None:
            return 0
        if a["fase"] == "preparar":
            return -a["lado"] * 3 * self.escala * (a["t"] / ENEMIGO_PREPARAR)
        if a["fase"] == "golpe":
            return a["lado"] * 5 * self.escala
        return a["lado"] * 5 * self.escala * (1 - a["t"] / ENEMIGO_RECUPERAR)

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

    def dibujar(self, superficie, cam=(0, 0)):
        centro = (self.rect.centerx - cam[0], self.rect.centery - cam[1])
        if self.imagen is not None:
            superficie.blit(self.imagen, self.imagen.get_rect(center=centro))
            return
        pygame.draw.ellipse(superficie, self.color, self.rect.move(-cam[0], -cam[1]))
        pygame.draw.circle(superficie, self.color_brillo, centro, self.radio_exterior)
        pygame.draw.circle(superficie, (235, 250, 255), centro, self.radio_interior)


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

    def _angulo_hacia(self, objetivo):
        diferencia = pygame.Vector2(objetivo) - pygame.Vector2(self.rect.center)
        if diferencia.length_squared() == 0:
            return self.angulo_mirada
        return math.atan2(diferencia.y, diferencia.x)

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

    def _zona_cuerpo_a_cuerpo(self, lado=None):
        lado = self.mirando if lado is None else lado
        zona = pygame.Rect(0, 0, 190, 150)
        y = self.rect.centery + 25
        if lado == 1:
            zona.midleft = (self.rect.centerx + self.rect.w // 3, y)
        else:
            zona.midright = (self.rect.centerx - self.rect.w // 3, y)
        return zona

    @staticmethod
    def _zona_lluvia_espadas(ataque):
        ancho, alto = (1280, 300) if ataque["orientacion"] == "horizontal" else (320, 1040)
        zona = pygame.Rect(0, 0, ancho, alto)
        zona.center = ataque["objetivo"]
        return zona

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

    def cuerpo(self):
        zona = pygame.Rect(0, 0, int(self.rect.w * 0.9), int(self.rect.h * 1.65))
        zona.midbottom = self.rect.midbottom
        return zona

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


print("---------- ADMINISTRACION Y COLISIONES DE ENEMIGOS ----------")
class Enemigos:
    # Agrupa enemigos y proyectiles y centraliza actualización, daño y separación física.
    def __init__(self):
        self.lista = []
        self.proyectiles = []

    def __iter__(self):
        return iter(self.lista)

    def __len__(self):
        return len(self.lista)

    def agregar(self, enemigo):
        self.lista.append(enemigo)

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

    def _golpes_del_jugador(self, jugador):
        zona = jugador.hitbox()
        if zona is None:
            return
        dano = round(DANO_ATAQUE[jugador.accion] * jugador.multiplicador_dano)
        for e in self.lista:
            if e.vivo() and e not in jugador.golpeados and zona.colliderect(e.cuerpo()):
                if e.recibir_dano(dano, jugador.rect.center):
                    jugador.golpeados.add(e)

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


print("---------- INDICADORES DE DANO ----------")
class NumerosDano:
    # Administra textos flotantes que ascienden y se desvanecen con el tiempo.
    DURACION = 0.9
    SUBIDA = 110

    def __init__(self):
        self.lista = []
        self.fuente = pygame.font.Font(None, 48)

    def agregar(self, cantidad, x, y, color):
        self.lista.append({"texto": str(int(cantidad)), "x": x + random.uniform(-16, 16),
                           "y": y, "t": 0.0, "color": color})

    def actualizar(self, dt):
        for n in self.lista:
            n["t"] += dt
            n["y"] -= self.SUBIDA * (1 - n["t"] / self.DURACION) * dt
        self.lista = [n for n in self.lista if n["t"] < self.DURACION]

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


def texto_dano(cantidad, x, y, color):
    numeros_dano.agregar(cantidad, x, y, color)


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

    def cofre_cercano(self):
        cercano = self.jugador.rect.inflate(110, 110)
        return next(
            (cofre for cofre in mapa.cofres if not cofre.abierto and cercano.colliderect(cofre.rect)),
            None,
        )

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


def filas_visibles():
    fin = min(len(canciones), scroll + FILAS_VISIBLES)
    return [(i, pygame.Rect(350, 230 + v * 62, 850, 52)) for v, i in enumerate(range(scroll, fin))]


def rect_check(fila):
    return pygame.Rect(fila.x + 14, fila.centery - 16, 32, 32)


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