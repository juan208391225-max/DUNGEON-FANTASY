# Sonidos por accion

Los archivos de sonido se ponen en la carpeta `sonidos`. En `sonidos_acciones.py`, asigna el nombre del archivo a cada variable `SONIDO_...`; por ejemplo:

```python
SONIDO_ATAQUE_ESPADA = "ataque_espada.wav"
```

Se aceptan formatos compatibles con Pygame, normalmente WAV u OGG. Cada evento usa su propio objeto `Sound`; los sonidos pueden superponerse en canales independientes, mientras que los pasos se reproducen en bucle y los ataques sustituyen al efecto de ataque anterior. El volumen se toma del control **Efectos**.

| Variable | Accion | Palabras clave para buscar |
|---|---|---|
| `SONIDO_PASOS_CAMINAR` | Pasos mientras camina | `footsteps walk`, `pasos caminar` |
| `SONIDO_PASOS_CORRER` | Pasos mientras corre | `footsteps run`, `pasos correr` |
| `SONIDO_SALTO` | Inicio del salto | `character jump`, `salto videojuego` |
| `SONIDO_ATERRIZAJE` | Aterrizar tras saltar | `character landing`, `impacto aterrizaje` |
| `SONIDO_RODAR` | Rodar/esquivar | `dodge roll`, `rodar personaje` |
| `SONIDO_ATAQUE_ESPADA` | Ataques normales de espada | `sword swing`, `sword slash` |
| `SONIDO_ATAQUE_EMBESTIDA` | Ataque corriendo/embestida | `sword dash attack`, `dash slash` |
| `SONIDO_ATAQUE_AEREO` | Ataque hacia abajo en el aire | `downward sword attack`, `air slash` |
| `SONIDO_ATAQUE_GIRO` | Ataque giratorio | `spinning sword attack`, `spin slash` |
| `SONIDO_GOLPE_ENEMIGO` | Enemigo recibe un golpe y sobrevive | `enemy hit`, `monster hurt` |
| `SONIDO_DERROTA_ENEMIGO` | Enemigo derrotado | `enemy death`, `monster death` |
| `SONIDO_DANO_JUGADOR` | Jugador recibe dano | `player hurt`, `character damage` |
| `SONIDO_DERROTA_JUGADOR` | Jugador muere | `player death`, `game over death` |
| `SONIDO_PERDER_PARTIDA` | Sonido de derrota/fin de partida | `game over`, `defeat jingle` |
| `SONIDO_VICTORIA` | Victoria final | `victory fanfare`, `level complete` |
| `SONIDO_CURACION_POCION` | Beber pocion y curarse | `potion drink`, `healing potion` |
| `SONIDO_ABRIR_COFRE` | Abrir cofre | `treasure chest open` |
| `SONIDO_RECOGER_POCION` | Recoger pocion del suelo | `item pickup`, `potion pickup` |
| `SONIDO_ACTIVAR_BERSERKER` | Activar Berserker | `power up`, `rage power up` |
| `SONIDO_ATAQUE_ENEMIGO_CUERPO` | Ataque cuerpo a cuerpo del enemigo | `enemy melee attack`, `monster attack swing` |
| `SONIDO_ATAQUE_ENEMIGO_DISTANCIA` | Lanzamiento de proyectil enemigo | `magic projectile cast`, `spell cast` |
| `SONIDO_ATAQUE_JEFE` | Aviso/ataque del jefe | `boss attack`, `boss roar` |
| `SONIDO_INICIO_OLEADA` | Comienza una oleada | `wave start`, `battle begins` |
| `SONIDO_COMPLETAR_OLEADA` | Se completa una oleada | `wave complete`, `objective complete` |

Los sonidos disponibles ya estan asignados en `sonidos_acciones.py` y las versiones WAV recortadas estan en `sonidos`. Los archivos originales se conservan. Caminar usa el clip propio `caminar.mpeg` convertido a `pasos_caminar.wav`; correr mantiene su clip separado. Ambos se repiten mientras el personaje se mueve y paran al detenerse. Los ataques interrumpen el efecto de ataque anterior para que no se acumulen.

| Archivo asignado | Accion en el juego |
|---|---|
| `pasos_caminar.wav` / `pasos_correr.wav` | Clips distintos de caminar y correr en bucle; se detienen al parar y se sustituyen al cambiar entre caminar y correr. |
| `salto.wav` / `aterrizaje.wav` | Despegue del salto y aterrizaje. |
| `ataque_espada.wav` / `ataque_embestida.wav` | Ataques normales y embestida; un nuevo ataque corta el sonido anterior. |
| `ataque_enemigo_cuerpo.wav` | Ataque cuerpo a cuerpo del enemigo; usa el mismo audio que el clip suministrado para embestida. |
| `golpe_enemigo.wav` / `derrota_enemigo.wav` | Enemigo herido y enemigo derrotado. |
| `golpe_PERSONAJE- copia.wav` / `derrota_jugador.wav` | Jugador herido y jugador derrotado. El clip de herida actualmente es identico al de golpe del enemigo. |
| `victoria.wav` | Victoria final. |
| `curacion_pocion.wav` / `abrir_cofre.wav` | Curacion y apertura de cofre. |
| `recoger_pocion.wav` | Recoger una pocion del suelo. |
| `activar_berserker.wav` | Activacion del modo Berserker. |
| `ataque_enemigo_distancia.wav` / `ataque_jefe.wav` | Ataque a distancia de enemigo y ataque del jefe. |
| `inicio_oleada.wav` | Inicio de una oleada. |

La configuracion conserva **24 eventos de audio editables** en `sonidos_acciones.py`.
