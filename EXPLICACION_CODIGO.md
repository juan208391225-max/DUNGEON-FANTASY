# Guia detallada del codigo de PRISION FANTASY

Este documento explica la version completa del juego en `PRISION FANTASY.py` y
los dos modulos que esta importa: `sonidos_acciones.py` y `guardado_mysql.py`.
Los numeros de linea se refieren a la version actual de esos archivos. Se
agrupan las lineas que forman una misma instruccion o tarea; las lineas en
blanco solo separan secciones y no ejecutan nada.
El archivo ejecuta su inicializacion y el bucle principal al ejecutarse; no
espera a que se llame a una funcion `main()`.

`principal.py` es otra version independiente y anterior del juego: tiene su
propio jugador, mapa, enemigos y bucle principal. No es un modulo que
`PRISION FANTASY.py` importe. `verificar_expansion.py` es un archivo de
pruebas, y `actualizar_evidencia_capturas.py` es una herramienta para editar
un documento Word; ninguno forma parte de la partida normal.

## 1. Conceptos de Python que aparecen en el juego

- **Variable:** nombre que guarda un valor. Por ejemplo, `VIDA_JUGADOR = 100`
  guarda el maximo de vida. Las mayusculas suelen indicar una constante de
  configuracion; no hacen que Python impida cambiarla.
- **Funcion (`def`):** bloque reutilizable. Recibe datos por sus parametros,
  ejecuta instrucciones y puede devolver un resultado con `return`.
- **Clase (`class`):** molde para crear objetos con datos y funciones. Por
  ejemplo, `Jugador` describe como crear y actualizar a un personaje.
- **Objeto / instancia:** ejemplar creado desde una clase. `Jugador(...)`
  crea un jugador; dentro de sus metodos, `self` representa ese ejemplar.
- **Ciclo `for`:** repite un bloque por cada elemento de una secuencia:
  `for enemigo in enemigos:` ejecuta el cuerpo una vez por enemigo. En
  `for i in range(5):`, `range(5)` produce 0, 1, 2, 3 y 4 (no incluye 5).
- **Ciclo `while`:** repite mientras la condicion sea verdadera. El bucle
  principal `while RUN:` mantiene abierto el juego hasta que `RUN` sea falso.
- **Lista (`[...]`):** coleccion ordenada que puede cambiar. Se usa para
  enemigos, frames de animacion, rutas y elementos visibles. `append` agrega;
  una comprension como `[p for p in lista if condicion]` crea una lista nueva
  filtrada.
- **Tupla (`(...)`):** coleccion ordenada que normalmente representa datos
  fijos. `(x, y)` es una posicion; `(20, 10)` puede ser ancho y alto; las
  configuraciones de oleada y las coordenadas suelen ser tuplas.
- **Diccionario (`{clave: valor}`):** relaciona claves y valores. Por ejemplo,
  `{"vida": 60, "dano": 12}` define atributos. `datos["vida"]` consulta la
  clave. En el juego, los diccionarios describen zonas, perfiles, estados y
  opciones.
- **Condicion (`if` / `elif` / `else`):** elige qué instrucciones ejecutar
  segun una expresion verdadera o falsa. `elif` prueba otra posibilidad si la
  anterior no se cumplio.
- **`return`:** termina una funcion y entrega un resultado. `return False`
  tambien comunica que una accion no pudo realizarse.
- **`None`:** significa que no hay un valor u objeto en ese momento. Por
  ejemplo, `self.accion = None` indica que el jugador no esta ejecutando una
  accion especial.
- **Metodo `__init__`:** se ejecuta al crear una instancia y prepara sus
  variables. `Jugador.__init__` crea la vida, posicion, animacion e inventario.
- **Herencia:** `class Cofre(Prop)` hace que `Cofre` herede la base de `Prop`
  y añada el estado de abierto/cerrado. `super().__init__(...)` llama al
  inicializador de la clase base.
- **Propiedad (`@property`):** se consulta como atributo, pero su valor se
  calcula al leerlo. `jugador.berserker_activo` devuelve si el temporizador
  berserker es mayor que cero.
- **`self`:** referencia a los datos y metodos de la instancia actual. Asi,
  `self.vida` es la vida de ese jugador o enemigo, no una variable global.
- **`global`:** declara que una funcion va a reasignar una variable definida
  fuera de ella, por ejemplo `RUN` o `partida`. No es necesario para leerla.
- **`dt`:** tiempo en segundos desde el fotograma anterior. Multiplicar una
  velocidad por `dt` hace que el movimiento dependa del tiempo real y no de
  cuantos fotogramas por segundo tenga el equipo.
- **`pygame.Rect`:** rectangulo que facilita dibujar, ubicar y comprobar
  colisiones. **`pygame.Vector2`:** vector de dos componentes para posiciones,
  direcciones y velocidades.

Ejemplo real, simplificado:

```python
for enemigo in enemigos:
    if enemigo.vivo():
        enemigo.actualizar(dt, jugador, enemigos)
```

`for` visita todos los enemigos; `if` omite a los muertos si el metodo
`actualizar` correspondiente asi lo decide; cada llamada pasa el tiempo, al
jugador y la coleccion de enemigos. La variable `enemigo` cambia de valor en
cada vuelta.

## 2. Inicio, importaciones y configuracion

### Importaciones e inicializacion — `PRISION FANTASY.py`, lineas 1-8

- `math`, `os`, `random` y `sys` aportan calculos, rutas y archivos, numeros
  aleatorios y salida del programa.
- `pygame` contiene la ventana, el teclado/raton, las superficies, el audio,
  el reloj y las herramientas 2D.
- `MySQLSaveSlots` y `AudioAcciones` importan las clases auxiliares para
  guardar partidas y reproducir efectos.
- `pygame.init()` inicializa los modulos de Pygame para poder usarlos.
- Los `print(...)` de encabezado muestran en consola en que seccion esta
  arrancando el programa; no cambian las reglas del juego.

### Configuracion de zonas, oleadas y puertas — lineas 11-85

- `ZONAS` es una **lista de diccionarios**. Cada diccionario define una zona:
  nombre, casillas limite, color, destino, distancia de aparicion, cantidad
  de enemigos, maximo simultaneo, intervalo y tipos de enemigos.
- `casillas` y `destino` son tuplas. La primera contiene las esquinas
  `(columna_inicial, fila_inicial, columna_final, fila_final)`; la segunda,
  una casilla objetivo.
- Las claves `"jefe"`, `"sprite_jefe"`, `"tipo_jefe"` y `"tipos_apoyo"`
  especifican excepciones para las zonas con jefe.
- `PUERTAS_POR_OLEADA` es un diccionario cuya clave es el numero de oleada y
  cuyo valor es una tupla de coordenadas de puertas. Al completar esa oleada,
  se abren esas puertas.
- Las constantes `OLEADA_...` establecen valores por defecto y ritmos:
  enemigos por zona, limite vivo, espera, tiempo entre apariciones y puntaje.
- `BONIFICACIONES` es una tupla de tuplas: identificador interno, titulo y
  descripcion de cada mejora ofrecida al terminar una oleada.

### Configuracion de enemigos, jugador, escala y hitboxes — lineas 88-201

- Las constantes `RETROCESO_ENEMIGO`, `RADIO_DETECCION` y similares ajustan
  comportamiento compartido: vagar, perseguir, iniciar ataque, golpear y
  recuperarse. Los parametros `JEFE_...` particularizan patrones de jefes.
- `VIDA_JUGADOR`, velocidades, salto, gravedad y tiempos definen la fisica y
  el combate del personaje.
- `DANO_ATAQUE` es un diccionario que mapea el nombre de cada accion de ataque
  con el daño base. La clave debe coincidir con la accion usada por el jugador.
- `ESCALA_TILES`, `ESCALA_JUGADOR` y `ESCALA_ENEMIGOS` convierten dibujos
  originales en dimensiones de juego. `escala_jugador` y `escala_enemigos`
  guardan el producto por la escala global.
- Las `HITBOX_...` son tuplas de ancho y alto para pies, cuerpo y ataque. La
  hitbox logica puede ser distinta del tamaño visual del sprite: con ella se
  calculan golpes y obstaculos.
- `CAMARA_SUAVIDAD` y `CAMARA_LIMITADA` configuran seguimiento y limites de
  camara; `TAM_TILE` expresa el tamaño de cada casilla en pixeles.

## 3. Generacion del mapa — funcion `_crear_mapa()`, lineas 203-630

La funcion devuelve el plano como una lista de cadenas. Cada caracter de una
cadena representa una casilla. Despues, `Mapa` interpreta esos caracteres como
suelo, agua, muro, puerta u objeto.

1. **Cuadricula y aleatoriedad estable** — Se crean `celdas`, una lista de
   listas inicialmente llenas de `"."`, y `reservado`, otra cuadricula de
   valores booleanos. `rng = random.Random(19)` crea un generador local con
   semilla fija: el decorado aleatorio se repite igual en cada ejecucion.
   `Z` conserva los limites de las zonas y `VERDES` agrupa tipos de suelo
   sobre los que se puede colocar vegetacion.
2. **`valor(ix, iy, semilla)`** — Consulta o calcula un numero pseudoaleatorio
   asociado a una coordenada de la cuadricula. `lattice` guarda los resultados
   ya calculados para no recalcularlos y para mantener continuidad.
3. **`ruido(x, y, escala, semilla)`** — Convierte coordenadas a una cuadricula
   mas gruesa, obtiene los cuatro valores vecinos con `valor`, suaviza la
   fraccion (`tx`, `ty`) y mezcla los cuatro valores. El resultado genera
   variaciones que cambian gradualmente, en lugar de puntos aleatorios
   aislados.
4. **`dentro(x, y)`** — Devuelve `True` si una coordenada cae dentro de las 80
   columnas y 48 filas. Evita escribir fuera del mapa.
5. **`poner(...)`** — Si la casilla existe, guarda el caracter en `celdas[y][x]`.
   Si `reservar_celda` vale `True`, tambien marca esa posicion para protegerla
   de arboles/decoracion aleatorios posteriores.
6. **`pintar(limites, ch, ...)`** — Dos ciclos `for` recorren filas y columnas
   de un rectangulo inclusivo y llaman `poner` en cada casilla.
7. **`reservar(...)` y `reservar_circulo(...)`** — Marcan como protegidas un
   rectangulo con margen o un circulo. Se usan para que ruido, arboles y otros
   elementos no tapen caminos, destinos o edificios.
8. **`mancha(...)`** — Recorre una zona alrededor del centro `(cx, cy)`,
   normaliza la distancia por `rx` y `ry` para obtener una elipse y altera su
   contorno con ruido. Las casillas que caen dentro reciben el caracter del
   liquido o terreno.
9. **`muro(...)`** — Recorre un rectangulo pero solo escribe las casillas del
   borde. Omite coordenadas de `huecos`; con `ruina` puede dejar faltantes al
   azar, excepto en esquinas.
10. **`edificio(...)`** — Pinta el suelo interior, dibuja el perimetro, coloca
    una puerta y reserva el edificio con un margen.
11. **`puntos_circulo(...)`, `colocar(...)` y `zona_en(...)`** — Calculan
    puntos alrededor de una elipse, colocan un simbolo en multiples posiciones
    y averiguan que zona contiene una casilla.
12. **Distribucion de terreno y caminos** — Las llamadas iniciales a `pintar`
    asignan suelos de zonas; los ciclos rellenan zonas exteriores con pradera,
    caminos y conexiones. Las llamadas `muro`, `edificio`, `colocar` y
    `reservar` componen ruinas, arena, edificios, objetos y puntos de interes.
    Las tuplas de coordenadas permiten describir muchas ubicaciones sin crear
    una variable por cada una.
13. **Agua y veneno** — `mancha` y los bucles trazan rios y estanques de agua
    (`"~"`) y veneno (`"v"`). Los cruces con caminos se definen antes de
    agregar decoracion.
14. **Puertas y entradas** — Se agregan las puertas `"G"` listadas en
    `PUERTAS_POR_OLEADA`. La casilla `"P"` marca el inicio del jugador.
15. **Vegetacion probabilistica** — `DENSIDAD` es un diccionario de
    probabilidades por zona. Los ciclos visitan las casillas verdes; se calcula
    una probabilidad segun zona, borde y ruido. `rng.random()` decide si
    aparece un arbol y otro numero decide cual simbolo poner.
16. **Decoracion adicional** — `DECORACION` contiene, por zona, pares de
    simbolo y probabilidad. `acumulado` suma probabilidades y determina que
    decoracion poner. Un ultimo recorrido agrega piedras cerca del agua.
17. **Resultado** — `return ["".join(fila) for fila in celdas]` une cada fila
    de caracteres en una cadena y devuelve todas las filas como lista.
    `MAPA = _crear_mapa()` guarda ese resultado. `MUNDO_ANCHO` y
    `MUNDO_ALTO` convierten columnas/filas a pixeles.

La funcion usa muchas listas de coordenadas y tuplas: son una forma compacta de
decir "repite la misma operacion en cada posicion". El `for` no elige por si
mismo el tipo de objeto; lo hace el cuerpo del ciclo mediante `poner`,
`pintar`, `rng.choice` o condiciones.

## 4. Estados globales, recursos, musica y fondo — lineas 643-855

- `width` y `height` son las dimensiones internas logicas de dibujo. `RUN`,
  `JUGAR`, `CARGANDO`, `AJUSTES`, `MUSICA`, `PAUSA`, `RANURAS` y `CONTROLES`
  son banderas booleanas que indican que vista debe mostrarse.
- `camara`, `mapa`, `partida` y `captura` guardan objetos compartidos. Al inicio
  algunas referencias valen `None` porque se crean mas adelante.
- `menu_font`, `titulo_font`, `fuente_peq` y `reloj` son recursos de texto y
  temporizacion.
- `buscar_canciones()` recorre la carpeta `musica`, ordena los nombres y
  conserva archivos cuya extension sea `.mp3`, `.ogg` o `.wav`. Devuelve una
  lista de rutas.
- `canciones` es la lista encontrada; `activas` crea un diccionario por
  comprension que marca cada pista como habilitada. `actual` guarda el indice
  de reproduccion; `scroll` el desplazamiento de la lista mostrada.
- `ajustes` guarda volumen y opciones visuales. Los diccionarios `sliders`,
  `interruptores`, `ranuras_filas`, `ranuras_cargar` y `ranuras_guardar`
  relacionan una opcion o ranura con su rectangulo grafico.
- `reproducir_sonido(...)` pasa el nombre del efecto y el volumen configurado
  a `audio_acciones`. `SONIDOS_ATAQUE` agrupa sonidos que pueden reemplazarse
  entre si para que los ataques no se encimen.
- `almacen_guardados` crea el adaptador MySQL; los diccionarios y variables
  cercanos guardan ranuras leidas, mensaje de estado y progreso pendiente.
- `game_surface` es una superficie interna fija. `ventana` es la ventana
  visible; `blit_scaled()` la escala a su tamaño para mantener la misma
  resolucion logica.
- `cargar_fondo()` busca imagenes por nombre; si no encuentra ninguna,
  dibuja un degradado linea por linea.
- `FondoVideo` abre `fondo.mp4` mediante OpenCV, recuerda el intervalo de
  fotogramas, lee y convierte los frames de BGR a RGB y los dibuja. Al llegar
  al final reinicia el video. `cerrar()` libera el archivo. Si el video no se
  puede abrir, el juego muestra el fondo estatico.
- `opciones` y `opciones_pausa` son listas de diccionarios: cada opcion tiene
  texto, rectangulo y modo/accion. Los ciclos que las recorren dibujan botones
  uniformes.

## 5. Objetos del mapa y clase `Mapa` — lineas 856-1274

- **`Prop`**: recibe imagenes (`frames`), punto de anclaje (`pie`), colision,
  velocidad de animacion (`fps`) y desfase. Construye un `Rect` si el objeto
  bloquea el paso. `dibujar()` elige un frame con el reloj o el primer frame,
  y lo ubica desde sus pies compensando la camara.
- **`Cofre(Prop)`**: llama al inicializador base, conserva imagen cerrada y
  abierta, y guarda `abierto`. `abrir()` cambia el estado una sola vez;
  `dibujar()` selecciona la imagen segun ese estado.
- **`Pocion`**: almacena posicion y rectangulo para detectar contacto; al
  dibujar carga/escala el icono, muestra un aro y compensa la camara.
- Los diccionarios de clase `SUELOS`, `TERRENOS`, `MUROS`, `REJAS`,
  `LIQUIDOS`, `OBJETOS`, `DECORADOS` y `ANIMADOS` traducen los caracteres del
  plano a piezas del tileset, dimensiones, capas visuales y colisiones.
- **`Mapa.__init__`**: comprueba dimensiones regulares del plano; busca
  `mapa`; carga imagenes del tileset; crea cache de sprites, cuadriculas de
  suelo y colision, listas de objetos/cofres/animaciones y puertas; extrae la
  pieza de puerta y llama `_autotiles()` y `_construir()`.
- **`pieza(fila, col, alto)`**: forma una clave de cache; si no existe,
  recorta esa pieza del tileset, la escala y la guarda; devuelve el sprite.
- **`_firma(tile)`**: inspecciona pixeles opacos en los cuatro lados y esquinas
  de una pieza; devuelve una tupla booleana que representa su forma de borde.
- **`_autotiles(fila0)`**: con dos ciclos recorre la zona de autotiles,
  descarta tiles vacios y asocia cada imagen a su firma. Esto permite elegir
  los bordes de agua/veneno que coinciden con vecinos.
- **`_dentro(x, y)`** comprueba limites; **`_terreno_de(x, y)`** traduce el
  caracter a tipo de suelo y, si es un objeto, busca el terreno mas comun de
  sus ocho vecinos.
- **`_frames_anim(fila)`** carga y cachea los frames no vacios de una fila del
  tileset animado. **`_mismo(x, y, ch)`** revisa si la casilla vecina tiene el
  mismo caracter; fuera del mapa se trata como borde del mismo tipo.
- **`_construir()`** visita cada casilla con un `for` anidado (fila y columna).
  Para cada caracter:
  - selecciona un tile de suelo con `rng.choices(opciones, pesos)`;
  - en muros agrega pieza superior o pieza de cara y marca terreno, paso y
    vision como bloqueados;
  - en agua/veneno calcula firma de vecinos, agrega autotile y marca el paso
    bloqueado;
  - en rejas conserva el suelo, agrega la puerta y bloquea la casilla;
  - en objetos y decoracion añade la pieza visual y, cuando corresponde,
    crea un `Prop` solido;
  - en animaciones crea un `Prop` con varios frames;
  - en `"P"` actualiza el punto de inicio.
- **`abrir_puertas(puertas)`**: recorre coordenadas; ignora las que no son
  rejas o ya estan abiertas; quita la imagen de reja, habilita el paso y
  devuelve las puertas que realmente abrio.
- **`reiniciar_progreso()`**: cierra cofres y restaura las puertas previamente
  abiertas para una nueva partida.
- **`dibujar_suelo(...)`**: rellena el fondo, calcula el rango de tiles que
  toca la camara y dibuja sus capas. Despues dibuja decoracion animada visible.
- **`props_visibles(...)`** devuelve solo objetos cercanos a la pantalla;
  **`dibujar_colisiones(...)`** dibuja hitboxes de terreno/props, para depurar.
- **`celdas_alcanzables(inicio, limite)`** hace una busqueda en anchura:
  `cola` es la lista de casillas pendientes y `vistas` evita visitar una
  casilla dos veces. Los cuatro pares `(dc, df)` son vecinos cardinales.
  Devuelve las casillas transitables conectadas al inicio.
- **`choca(rect)`** considera colision fuera del mapa, con tiles solidos y con
  `Props` solidos.
- **`hay_vista(a, b)`** muestrea puntos de la linea entre dos posiciones y
  devuelve falso si encuentra una pared que bloquea la vision.
- **`paso_libre(a, b, ancho, alto)`** mueve una caja de prueba en pequeños
  pasos entre dos puntos; devuelve falso si alguna posicion choca.
- **`camino(a, b)`** realiza busqueda en anchura sobre casillas, guarda en
  `previo` de que casilla vino cada otra, reconstruye el trayecto desde el
  destino al inicio y lo devuelve ordenado.

## 6. Oleadas y progreso — clase `Oleadas`, lineas 1275-1600

- **`__init__(zonas)`** recorre zonas con `enumerate(zonas, 1)`, es decir,
  agrega a cada una un numero de nivel que empieza en 1. Comprueba destino,
  casillas alcanzables, arquetipos y sprites de jefes. Convierte casillas a
  rectangulos de pixeles y crea una copia de configuracion por zona con estado,
  enemigos generados/derrotados y temporizadores.
- La expresion `z.get("clave", valor_por_defecto)` usa el valor del diccionario
  si existe; si no, usa el valor alternativo.
- `self.puntos` es una lista de posiciones de aparicion transitables. Las
  tuplas expresan `(x, y)` en pixeles.
- **`actual`** es una propiedad que devuelve la primera zona no completada;
  **`victoria`** es verdadera cuando ya no hay zona actual.
- **`_aviso(...)`** actualiza mensaje y duracion; **`bloquea(rect)`** comprueba
  si el rectangulo debe permanecer dentro de la zona cerrada en curso.
- **`actualizar(dt, jugador, enemigos)`** es el controlador de oleadas:
  1. Reduce temporizadores y termina si no hay zona o el jugador murio.
  2. Recorre enemigos de oleada derrotados no contados, suma bajas y calcula
     puntos con un multiplicador que baja con el tiempo.
  3. Detecta entrada a zona; pasa de `pendiente` a `preparando`, muestra aviso
     y espera; luego activa el combate.
  4. Si el jugador sale de una zona cerrada, llama `_cancelar`.
  5. Limita enemigos vivos y usa `_generar` cuando vence el intervalo.
  6. Cuando ya genero todos y no queda ninguno vivo, marca completada, abre
     puertas, reproduce sonido y muestra el resultado.
- **`_cancelar(...)`** devuelve una zona cerrada a pendiente y elimina los
  enemigos de esa oleada.
- **`_generar(...)`** prefiere puntos alejados del jugador; crea `Jefe` o
  `Enemigo` segun la configuracion, marca el enemigo como parte de la oleada y
  aumenta el contador.
- **`dibujar_perimetro(...)`** representa una barrera coloreada y animada.
  Los ciclos por zonas, lados y grosor calculan transparencias y dibujan lineas.
- **`_vineta(color)`** genera una superficie sombreada y la cachea por color;
  **`dibujar_vineta(...)`** la muestra dentro de la zona activa.
- **`direccion_flecha(...)`** calcula direccion/distancia a la zona y, si hay
  muros, usa `Mapa.camino()` para apuntar al siguiente tramo accesible.
- **`dibujar_flecha(...)`** posiciona la flecha dentro de la pantalla, la
  dibuja como poligono y agrega nombre/distancia.
- **`dibujar_hud(...)`** decide textos segun estado (pendiente, preparacion,
  activa o victoria) y muestra avisos temporales y barreras.

## 7. Animaciones y jugador — lineas 1600-2180

### Configuracion de animaciones

`CONFIG_ANIM` es un diccionario: cada nombre de animacion apunta a una tupla
`(fotogramas_por_segundo, se_repite)`. Por ejemplo, caminar se repite y morir
se reproduce una vez. La funcion `cargar_animaciones()` busca imagenes
`nombre_1.png`, `nombre_2.png`, etc., escala cada frame y crea una lista
espejada para mirar a la izquierda.

### `Jugador.__init__(x, y)`

Prepara todos los datos iniciales: posicion vectorial, rectangulo de pies,
velocidades, animacion/frame, direccion, accion, postura, estado de salto,
vida e inventario, invulnerabilidad, combo, tiempos de recarga, mejoras y
berserker. Estas variables pertenecen a cada jugador porque se guardan en
`self`.

### Propiedades y acciones del jugador

- **`berserker_activo`**: consulta si queda tiempo activo.
- **`multiplicador_dano`**: combina mejora de daño permanente y bonificacion
  temporal berserker.
- **`multiplicador_velocidad`**: aumenta la velocidad mientras berserker esta
  activo.
- **`multiplicador_dano_recibido`**: reduce daño recibido, con un limite de
  0.55 para evitar reducirlo indefinidamente.
- **`registrar_ataque()`**: suma un golpe al contador y, segun nivel de viento,
  marca `tajo_viento_pendiente` para que `Partida` cree el proyectil.
- **`activar_berserker()`**: comprueba que exista mejora y que no este activo
  ni recargando; inicia sus dos temporizadores y reproduce sonido.
- **`beber_pocion()`**: verifica inventario, vida faltante y que el jugador
  siga vivo; consume una pocion y cura hasta 30 sin exceder vida maxima.
- **`poner_anim(...)`**: cambia la animacion, el sentido y/o reinicia el frame.
- **`avanzar_anim(dt)`**: aumenta o reduce el indice del frame segun FPS y
  `dt`; si termina, repite animaciones ciclicas o marca `anim_terminada`.
- **`progreso()`**: calcula que fraccion de la animacion ya transcurrio.
- **`elegir_imagen()`**: toma de `ANIMACIONES` el frame correspondiente a la
  animacion y orientacion actual.
- **`empezar(nombre, lado)`**: guarda accion, reproduce el sonido asociado,
  reinicia el registro de enemigos golpeados por este ataque, informa el golpe
  a la mejora de viento y pone la animacion.
- **`recibir_dano(...)`**: ignora daño si esta muerto, rodando o invulnerable;
  descuenta vida, muestra numero flotante, activa invulnerabilidad y, si sobrevive,
  calcula retroceso y animacion de herido. Si la vida llega a cero llama `morir`.
- **`morir()`**: marca la derrota, detiene el estado de accion, restablece salto
  y pone animacion/sonidos de muerte.
- **`celebrar()`**: programa una pose de victoria una sola vez.
- **`cuerpo()`** devuelve hitbox que recibe daño, mas baja cuando esta agachado.
- **`hitbox()`** devuelve `None` si no esta en ventana activa de ataque; si lo
  esta, calcula el rectangulo delante del jugador (o centrado para giro).
- **`pulsaciones(teclas, raton)`** compara botones actuales con `self.prev`.
  `nuevas` solo vale verdadero en el fotograma en que se presiona una tecla,
  no mientras se mantiene. Asi saltar/rodar/giro no se vuelven a disparar
  cada fotograma.
- **`decidir_accion(...)`** aplica prioridades: agacharse/levantarse; ataque
  aereo; salto; rodar; giro; pocion; pose de victoria; ataque normal/embestida;
  postura agachada.
- **`iniciar_rodar(direccion)`** normaliza una direccion o usa el lado al que
  mira el personaje y comienza la animacion de esquiva.
- **`_mover_chocando(paso)`** desplaza por separado eje horizontal y vertical.
  Si un paso completo choca, retrocede y prueba paso a paso para detenerse
  junto a la pared sin atravesarla.

### `Jugador.actualizar(teclas, dt)` — simulacion de cada fotograma

1. Reduce enfriamientos e invulnerabilidad y actualiza barras de vida y
   berserker usando `dt`.
2. Lee mouse y teclas; calcula presiones nuevas con `pulsaciones`.
3. Si esta muerto, detiene pasos, avanza animacion de muerte y termina el metodo
   con `return`.
4. Calcula `dx`, `dy` desde WASD/flechas; crea vector de movimiento y lo
   normaliza para que una diagonal no sea mas rapida. Calcula correr, agacharse,
   direccion a la que apunta el raton y si el ataque puede ejecutarse.
5. Si no hay accion activa, llama `decidir_accion`.
6. Segun accion (`rodar`, `atacar_dash`, `atacar_giro`, salto/ataque abajo,
   herido o movimiento libre), determina `mov`; multiplica por velocidad y
   `dt`, y usa `_mover_chocando`.
7. Limita el rectangulo al mapa, sincroniza `pos`, detecta bordes y actualiza
   altura/velocidad vertical del salto con gravedad. Al tocar el suelo, inicia
   aterrizaje cuando corresponde.
8. Si no hay accion, elige animacion segun estado en aire, agachado, pared,
   carrera, caminata o quietud.
9. Reproduce pasos en bucle al caminar/correr y detiene los otros pasos.
10. Avanza animacion. Si una accion finita termino, cambia postura o configura
    recarga y combo despues de un ataque.
11. Actualiza la imagen elegida para dibujar.

### `Jugador.dibujar(...)`

Dibuja sombra; hace parpadear al personaje si tiene invulnerabilidad; calcula
la posicion visual compensada por altura y camara; si berserker esta activo,
dibuja aura y particulas con seno/coseno; al final dibuja el sprite.

## 8. Enemigos, jefes y ataques — lineas 2181-3070

### Perfiles de enemigo — lineas 2181-2220 aproximadamente

Los diccionarios `ENEMIGO_GOBLIN`, `ENEMIGO_DISTANCIA`, `ENEMIGO_BRUJA`,
`ENEMIGO_NIVEL_2`, `ENEMIGO_DISTANCIA_NIVEL_2` y `ENEMIGO_ESPECTRO` almacenan
estadisticas por tipo: sprite, vida, daño, velocidad, puntos, alcance, tipo
de ataque, escala y, para ataques a distancia, color/tamaño/sprite de proyectil.
`ARQUETIPOS_ENEMIGO` permite buscar esos datos con una clave textual como
`"goblin"` o `"lich"`.

### `Enemigo`

- **`__init__(...)`** busca el perfil; rechaza tipos desconocidos; calcula
  escala e hitbox; copia vida y atributos; carga y cachea variantes visuales;
  inicializa estado de IA, temporizadores, ruta y muerte.
- **`vivo()`** devuelve si `vida > 0`.
- **`cuerpo()`**, **`zona_ataque(lado)`** crean rectangulos de colision para
  recibir daño y atacar.
- **`recibir_dano(...)`** ignora impactos cuando esta muerto, en retroceso o
  apareciendo; descuenta vida, muestra daño, calcula empuje, interrumpe ataque
  y reproduce sonido de golpe o derrota.
- **`_area()`** determina el area en la que puede moverse.
- **`_mover(...)`** intenta moverlo por ejes y cancela el eje que choque con
  obstaculos/mapa; luego recorta la posicion al mundo.
- **`_retroceder(dt)`** aplica empuje que va disminuyendo y termina el tiempo
  de retroceso.
- **`_vagar(dt, obstaculos)`** alterna pausas y direcciones aleatorias; si se
  aleja de su posicion inicial, tiende a regresar.
- **`_perseguir(...)`** calcula distancia y direccion al jugador. Enemigos
  a distancia disparan si tienen linea de vista y estan en rango; enemigos
  cuerpo a cuerpo inician ataque cuando su hitbox alcanza al jugador. Si una
  pared bloquea, recalculan una ruta; en caso contrario se mueven directo.
- **`_atacar(...)`** recorre fases temporizadas `preparar`, `golpe` y
  `recuperar`. En el golpe crea proyectil o aplica daño cuerpo a cuerpo; luego
  establece recarga.
- **`actualizar(...)`** procesa aparicion, retroceso y muerte; decide si
  persigue o vaga por distancia/vision; crea lista de obstaculos (jugador y
  otros vivos) y llama el comportamiento correspondiente.
- **`_desplazamiento()`** agrega desplazamiento visual corto al ataque.
- **`dibujar(...)`** representa sombra, orientacion, alerta, destello o
  desvanecimiento; dibuja aviso del ataque a distancia y barra de vida.

### `EnemigoProyectil`

Guarda origen, direccion, velocidad, daño, apariencia, alcance y recorrido.
`actualizar(dt, jugador)` avanza con vector por velocidad-tiempo, actualiza la
hitbox y elimina el proyectil cuando impacta al jugador, supera alcance o choca
con el mapa. `dibujar(...)` usa sprite si existe o formas geometricas.

### `Jefe(Enemigo)`

Hereda del enemigo, pero configura una hitbox/sprite mayores, vida y daño
propios, nombre, apoyos y temporizadores. Los metodos geometricos calculan
direccion, poligono/area del aliento, area de lluvia de espadas y zona cercana.
`_punto_en_poligono` usa cruces de rayos; `_aliento_colisiona` combina esquinas,
puntos y bordes para comprobar si el cuerpo del jugador cruza el aliento.

- **`_invocar_apoyos()`** escoge tipo y posicion al azar, crea enemigos aliados
  al jefe y los deja en una lista pendiente para agregarlos sin modificar la
  lista mientras se recorre.
- **`_iniciar_ataque(tipo, objetivo)`** guarda un diccionario de estado para el
  patron: fase, temporizador, objetivo, lado y angulo. Lluvia de espadas alterna
  orientacion y puede invocar apoyos.
- **`_impacto(jugador)`** calcula la colision adecuada a meteoro, aliento,
  lluvia o ataque cercano y aplica daño una vez que corresponde.
- **`actualizar(...)`** reduce aparicion/recarga, avanza fases aviso-activo-
  recuperacion y escoge siguiente ataque segun clase/distancia. Fuera del ataque,
  persigue al jugador.
- **`_dibujar_aliento(...)` y `dibujar(...)`** muestran avisos de zonas,
  meteorito, armas, aliento, sombra, sprite, animacion y desvanecimiento.

### `TajoViento`

Representa el proyectil especial de la mejora de viento. Calcula direccion al
raton, perpendicular, velocidad, alcance y daño; `_actualizar_rect()` crea una
caja envolvente rotada; `_colisiona()` comprueba solapamiento proyectando las
formas sobre cuatro ejes; `actualizar()` avanza y daña cada enemigo solo una
vez; `dibujar()` pinta tres trazos para el efecto de tajo.

### `Enemigos`

Es un contenedor para lista de enemigos y lista de proyectiles hostiles.
`__iter__` permite escribir `for e in enemigos`; `__len__` permite `len(...)`;
`agregar` inserta; `jefe_vivo` busca el primer jefe vivo. `actualizar` recorre
una copia (`tuple(self.lista)`) para permitir incorporar apoyos de jefe sin
alterar el ciclo en curso, actualiza proyectiles, quita eliminados, procesa
golpes del jugador y separa al jugador de enemigos. `_golpes_del_jugador`
calcula daño segun la accion activa y registra a quien ya golpeo ese ataque;
`_chocar_con_jugador` aplica daño por contacto si la opcion global lo permite
y separa cuerpos que se solapan.

### Numeros de daño

`NumerosDano` conserva una lista de diccionarios, uno por texto flotante
(`texto`, `x`, `y`, tiempo `t` y color). `agregar` crea un nuevo numero;
`actualizar(dt)` lo eleva y elimina al pasar su duracion; `dibujar` crea borde,
transparencia y lo pinta en pantalla. `texto_dano(...)` es una funcion corta
que delega a la instancia global `numeros_dano`.

## 9. Estado y coordinacion de la partida — clase `Partida`, lineas 3180-3408

- **`__init__()`** reinicia cofres/puertas, crea jugador, contenedor de
  enemigos y `Oleadas`; inicializa puntajes, proyectiles, pociones y mejoras;
  calcula rectangulos de tarjetas y centra la camara.
- **`terminada`** devuelve si el jugador murio o gano y ya no falta elegir una
  bonificacion.
- **`elegir_bonificacion(indice)`** valida que haya eleccion pendiente y el
  indice sea correcto; aumenta el nivel de esa mejora sin pasar el maximo.
- **`actualizar(dt, teclas)`** ordena el fotograma: bloquea durante la eleccion
  de bonificacion; actualiza al jugador, crea tajo de viento pendiente, actualiza
  enemigos/proyectiles/oleadas, elimina proyectiles, sincroniza puntos, recoge
  pociones, detecta oleadas completadas, programa recompensas, celebra victoria,
  actualiza daño flotante y camara.
- **`cofre_cercano()`** busca un cofre cerrado dentro de un rectangulo ampliado
  del jugador. `puede_abrir_cofre()` exige cofre cerca y ningun enemigo vivo.
- **`abrir_cofre()`** valida condiciones, marca el cofre abierto, crea una
  pocion en el mundo y muestra aviso.
- **`_recoger_pociones()`** recorre pociones mundanas; por cada colision aumenta
  inventario y registra la recogida; luego filtra la lista para quitar objetos
  recogidos.
- **`dibujar(...)`** dibuja primero suelo y perimetro; junta entidades en una
  lista y las ordena por `rect.bottom` para simular profundidad; despues agrega
  HUD, vida, flecha, puntuacion, cofres, estado de mejora, jefe, controles y
  overlays.
- **`_dibujar_eleccion_bonificacion()`** recorre configuracion de poderes y
  tarjetas; muestra nivel, disponibilidad y textos segun el poder. El diccionario
  interno `lineas` escoge descripcion segun su clave.
- **`_dibujar_barra_jefe(...)`** dibuja nombre y barra proporcional a
  `vida / vida_max`.
- **`_dibujar_hitboxes(...)`** dibuja en colores diferentes cajas de jugador,
  ataque, enemigos y colisiones del mapa para depuracion.

## 10. Funciones de interfaz, ajustes y musica — lineas 3410-3845

- **`blit_scaled()`** escala la superficie logica y la presenta en la ventana.
- **`dibujar_texto(...)`** centra texto en `game_surface`.
- **`pos_en_juego(pos)`** escala un punto del raton desde la ventana a
  coordenadas logicas; asi los clics siguen coincidiendo al cambiar tamaño.
- **`zona_boton(...)`** calcula rectangulo de texto ampliado para ser clicable.
- **`dibujar_boton(...)`** detecta hover, cambia color, dibuja y devuelve zona.
- **`dibujar_boton_caja(...)`** representa boton con relleno, borde y color de
  hover.
- **`dibujar_fondo()`** elige video o imagen/gradiente y coloca encima velo
  oscuro transparente.
- **`aplicar_volumen()`** aplica el volumen configurado al reproductor de
  musica.
- **`nombre_cancion(ruta)`** elimina directorios y extension.
- **`renderizar_texto_ajustado(...)`** recorta texto hasta que cabe; si puede,
  agrega puntos suspensivos.
- **`hay_activas()`** revisa si alguna pista esta habilitada.
- **`reproducir(indice)`** carga y reproduce una pista, actualiza `actual`;
  ante error de Pygame la deshabilita y devuelve falso.
- **`siguiente(paso)`** recorre circularmente pistas con modulo `%`; `paso=1`
  avanza y `paso=-1` retrocede. Si no hay pista util, para la musica.
- **`alternar_cancion(indice)`** habilita/deshabilita pista; si desactiva la
  actual, salta a otra.
- **`revisar_musica()`** inicia la siguiente pista cuando la actual termina.
- **`aplicar_pantalla()`** crea ventana fullscreen o tamaño fijo segun ajustes.
- **`dibujar_slider(...)`** muestra pista, relleno, indicador y porcentaje.
- **`dibujar_interruptor(...)`** representa booleano con estado SI/NO.
- **`texto_ahora_suena()`** devuelve el nombre de cancion actual o "(nada)".

## 11. Guardado, carga y ranuras — `PRISION FANTASY.py`, lineas 3570-3767

- **`refrescar_ranuras()`** consulta MySQL y crea un diccionario indexado por
  numero de ranura. Si falla, vacia resultados y guarda el mensaje para mostrarlo.
- **`validar_progreso_guardado(progreso)`** verifica tipo/version, rango de zonas,
  vida, pociones, puntaje, mejoras y cofres. Rechaza estructuras inesperadas
  antes de incorporarlas a la partida.
- **`capturar_progreso_guardado(partida_actual)`** construye un diccionario
  serializable: version, avance, vida, pociones, puntaje, mejoras y cofres
  abiertos; limita valores y pasa el resultado por validacion.
- **`aplicar_progreso_guardado(...)`** vuelve a validar; marca zonas completadas,
  abre las puertas que corresponden y restaura recompensas, vida, inventario,
  puntajes, mejoras y cofres.
- **`guardar_en_ranura(numero)`** crea el progreso y lo envia al almacenamiento;
  actualiza la interfaz con exito o error.
- **`cargar_desde_ranura(numero)`** obtiene la ranura seleccionada, indica si
  esta vacia, valida su payload y programa la carga de pantalla.
- **`show_ajustes()`** dibuja opciones de volumen, pantalla, FPS, musica y ranuras.
- **`show_ranuras()`** recorre las tres filas y presenta datos de cada guardado,
  habilitando botones segun contexto (cargar desde menu, guardar pausado/final).

## 12. Recursos del mundo y pantallas de juego — lineas 3768-4135

- **Musica:** `filas_visibles()` construye rectangulos de las pistas a mostrar;
  `rect_check()` y `rect_sonar()` calculan areas de los controles de cada fila.
  `show_musica()` dibuja la lista y estados; `click_musica(click)` alterna una
  pista, la reproduce directamente o cambia a anterior/siguiente.
- **Colisiones y camara:** `mapa_choca(rect)` consulta colision; `texto_borde`
  dibuja texto con contorno; `camara_pos()` calcula posicion de camara;
  `pos_raton_mundo()` transforma raton a coordenadas del mundo; `actualizar_camara`
  sigue al jugador y recorta al mapa.
- **Dibujo y carga de sprites:** `dibujar_mira`, `rect_translucido`,
  `con_transparencia` y `escalar_imagen` dibujan mira, rellenos y sprites con
  transparencia/tamaño. `ruta_sprite_enemigo`, `cargar_sprite_enemigo`,
  `cargar_imagen_proyectil` y `cargar_imagen_pocion` buscan y preparan archivos.
- **HUD/animaciones:** `dibujar_barra_vida` presenta vida; `cargar_animaciones`
  lee frames del directorio `jugador`, valida que existan y crea versiones
  invertidas. Si faltan recursos obligatorios, muestra error y sale.
- **`show_menu()`** muestra fondo, panel, titulo y opciones.
- **`iniciar_carga()`** cambia banderas y establece cuenta regresiva.
- **`show_carga(dt)`** reduce temporizador, calcula porcentaje, dibuja barra y,
  al llegar a cero, crea `Partida` y aplica progreso pendiente si lo hay.
- **`LISTA_CONTROLES`** es una lista de tuplas `(accion, tecla)`; la pantalla
  recorre y muestra cada pareja.
- **`show_controles()`** conserva captura pausada si se abrio desde pausa; si
  no, usa fondo; dibuja panel y controles.
- **`show_pausa()`** muestra la captura del juego oscurecida con opciones.
- **`manejar_eventos()`** procesa la cola de Pygame:
  - `QUIT` detiene el ciclo.
  - `KEYDOWN` alterna HUD/controles/hitboxes/cursor, abre cofres, elige mejoras,
    reinicia partida, gestiona Escape y atajos de menu.
  - `MOUSEWHEEL` cambia el scroll de canciones.
  - `MOUSEBUTTONDOWN` convierte coordenadas, detecta que panel esta activo y
    ejecuta el boton correspondiente.
  - `MOUSEBUTTONUP` deja de arrastrar slider.
  - Mientras un slider se arrastra, actualiza su valor entre 0 y 1 y aplica
    volumen.
- **`estado_cursor()`** decide si ocultar y capturar el cursor dentro del juego.
- **`actualizar_y_dibujar(dt)`** elige una sola pantalla por prioridad:
  carga, controles, ranuras, musica, ajustes, pausa, menu o juego. En juego
  actualiza y dibuja `partida`; opcionalmente muestra FPS.

## 13. Bucle principal — lineas 4283-4330

1. `dt = 0` inicializa el tiempo del primer frame.
2. `ANIMACIONES = cargar_animaciones()` prepara sprites.
3. `mapa = Mapa(MAPA)` convierte el plano de caracteres en el mundo jugable.
4. `partida = Partida()` crea el estado inicial.
5. `ayuda_juego` prepara textos de controles ya renderizados.
6. Se aplican volumenes y se intenta iniciar la lista de musica.
7. `while RUN:` es el ciclo que mantiene abierto el juego. En cada vuelta:
   - `manejar_eventos()` recoge acciones de ventana, teclado y raton;
   - `revisar_musica()` avanza musica terminada;
   - `actualizar_y_dibujar(dt)` actualiza simulacion y pinta el estado actual;
   - `blit_scaled()` copia la superficie interna a la ventana;
   - `pygame.display.flip()` presenta el frame;
   - `reloj.tick(60) / 1000` limita a 60 FPS y calcula `dt` en segundos.
8. Al salir del `while`, `pygame.quit()` libera Pygame y `sys.exit()` termina
   el proceso.

Este orden es importante: primero se leen eventos, luego se actualiza el juego,
despues se dibuja y finalmente se presenta el frame. `dt` hace que movimiento,
animaciones y temporizadores mantengan ritmo aunque el equipo dibuje menos de
60 frames por segundo.

## 14. Modulo de audio — `sonidos_acciones.py`

- Las constantes `SONIDO_...` guardan nombres de archivos. Una cadena vacia
  significa que esa accion no tiene sonido configurado.
- `ARCHIVOS_SONIDO` es un diccionario de nombre logico a archivo `.wav`.
- `AudioAcciones.__init__` copia configuracion y crea diccionarios para sonidos,
  canales pausados y errores.
- **`cargar()`** limpia estado anterior, filtra configuraciones vacias,
  comprueba que el mixer de Pygame exista y carga cada archivo. Errores de
  archivo/audio se anotan en `errores` y se muestran en consola.
- **`reproducir(...)`** busca sonido; opcionalmente no lo inicia si otro sonido
  bloqueador esta activo; detiene sonidos que deben reemplazarse; limita volumen
  entre 0 y 1; reproduce y registra el canal.
- **`reproducir_bucle(...)`** reutiliza canal activo si el mismo sonido ya esta
  en bucle; si no, llama `reproducir` con `loops=-1`.
- **`detener(*nombres)`** acepta varios nombres, detiene sus canales y elimina
  marcas de pausa.
- **`pausar(*nombres)`** pausa canales activos y registra cuales quedaron
  pausados.
- **`reanudar(*nombres)`** reanuda solo canales registrados y limpia su marca.

El `*` en `*nombres` permite pasar cero, uno o varios sonidos:
`detener("pasos_caminar", "pasos_correr")`.

## 15. Modulo de MySQL — `guardado_mysql.py`

- **`ConfiguracionMySQLError`** es un error de configuracion especifico.
- **`MySQLSaveSlots.__init__(configuracion, connector)`** usa la configuracion
  recibida o lee variables de entorno `PRISION_DB_...`; `connector` permite
  reemplazar MySQL por un conector de prueba.
- **`_connect()`** verifica host, usuario, contraseña y base; importa
  `mysql.connector` si no se inyecto otro conector; abre conexion con timeout.
  Si falta configuracion o la dependencia, comunica el problema con una
  excepcion explicita.
- **`listar()`** abre cursor, ejecuta un `SELECT` parametrizado para el jugador,
  lee filas, convierte JSON a diccionario si hace falta y devuelve una lista de
  diccionarios. `finally` cierra cursor y conexion incluso si falla la consulta.
- **`guardar(ranura, progreso)`** solo acepta ranuras 1, 2 o 3; serializa
  progreso con `json.dumps`; ejecuta `INSERT ... ON DUPLICATE KEY UPDATE` para
  crear o actualizar; `commit()` confirma y `finally` libera recursos.

`mysql_schema.sql` crea `save_slots`, tabla con identificador de jugador,
numero de ranura, datos JSON y fecha de actualizacion. Su clave primaria
compuesta evita que el mismo jugador tenga dos registros de la misma ranura.
`requirements-mysql.txt` declara el conector Python requerido para usar MySQL.

## 16. Otros archivos Python del proyecto

- **`principal.py`**: variante independiente anterior. Incluye su propia
  configuracion, mapa escrito directamente como lista de cadenas, clases
  `Jugador`/`Enemigo`, UI y bucle. No usa oleadas avanzadas, jefes, cofres,
  mejora de poderes ni guardado MySQL de la version principal. No se debe
  confundir con `PRISION FANTASY.py`.
- **`verificar_expansion.py`**: conjunto de pruebas. Configura controladores
  dummy para no abrir ventanas ni necesitar audio real, importa el juego
  interceptando salida, define sustitutos falsos de conexion/cursor y ejecuta
  pruebas `unittest` de audio, interfaz, guardados, oleadas, mapa y combate.
- **`actualizar_evidencia_capturas.py`**: script de automatizacion documental.
  Abre un `.docx`, valida capturas, sustituye imagenes y pies, renumera figuras,
  guarda otro documento y vuelve a abrirlo para verificarlo. No es necesario
  para iniciar o jugar.

## 17. Resumen del recorrido de una partida

`pygame.init()` -> carga configuracion -> genera `MAPA` -> carga imagenes/audio
-> crea `Mapa` y `Partida` -> el bucle lee entradas -> jugador y enemigos se
actualizan -> `Oleadas` crea encuentros y abre rutas -> `Partida` recoge
recompensas y dibuja -> Pygame presenta el frame. Al final de una oleada se
puede elegir mejora; las ranuras guardan el progreso JSON en MySQL.
