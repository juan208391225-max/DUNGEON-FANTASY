from pathlib import Path
import re
from docx import Document
from docx.shared import Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH


# Script auxiliar de documentación: sustituye capturas en un documento Word y
# comprueba el orden, cantidad de imágenes y numeración antes de terminar.
ROOT = Path(r"C:\Users\Juan Jose\OneDrive\Desktop\juego")
SOURCE = ROOT / "Dungeon Fantasy - EVIDENCIA ordenada.docx"
OUTPUT = ROOT / "Dungeon Fantasy - EVIDENCIA final.docx"
ATTACHMENTS = Path(
    r"C:\Users\Juan Jose\.copilot\workspaces\352793ca-04bf-4c34-8cf5-f3062da0f067\attachments"
)

# Cada pareja contiene el archivo adjunto y el pie explicativo que debe insertarse.
CAPTURES = [
    (
        "20da3e4e-52c3-47ce-af0a-a7cd46769bfe-cad1bd6e-cc41-41d0-b018-8b7385cfdb35-clipboard.png",
        "Estilos de muro. El diccionario MUROS relaciona cada símbolo con las piezas del tileset usadas para dibujar sus caras.",
    ),
    (
        "080ba8cc-2cf1-49b1-8e3f-2ea8c1e9f085-b3271229-f06f-4b75-8e70-46fdab36859d-clipboard.png",
        "Función muro(). Recorre el contorno, conserva los huecos y permite crear paredes con partes en ruinas.",
    ),
    (
        "4e5f30ae-f5b1-41af-90db-59142cadbc29-8b69c294-9f40-4eb3-a931-a3119a7fe1ac-clipboard.png",
        "Ejemplo de construcción. Estas instrucciones sitúan la cabaña y sus objetos decorativos en el Bosque Susurrante.",
    ),
    (
        "081de4ea-3ef6-44a4-9db5-43c41a07b238-ed7cb1d7-ca09-42c1-a5b8-0cf3ddd836f0-clipboard.png",
        "Densidad de árboles. Cada zona usa una probabilidad propia y ruido para variar la distribución de árboles.",
    ),
    (
        "b17fd5a9-0e6d-47cd-84ec-7c53134c99ca-2543b453-d09b-4e2e-929c-e0d8637ed83a-clipboard.png",
        "Agua, pantano y caminos. Se definen manchas de líquidos mediante posición, tamaño, símbolo y semilla, además de las rutas principales.",
    ),
    (
        "4a6146c0-4f18-4a2c-a5eb-c1582894c16d-932b799e-3e81-4a57-b380-0e68f46f1add-clipboard.png",
        "Tipos de líquido. El símbolo de la cuadrícula se asocia con los autotiles y la fila de animación correspondiente.",
    ),
    (
        "9ee49400-32a3-4b04-8e85-7ed883321a83-6c72c629-6a86-4335-a463-fabdc44d2011-clipboard.png",
        "Validación de las zonas. Se comprueba que el destino sea transitable y existan puntos de aparición alcanzables.",
    ),
]
CAPTIONS_TO_REMOVE = (17, 18, 21, 22, 23)

# Valida entradas y recursos antes de editar el documento para evitar resultados parciales.
if not SOURCE.is_file():
    raise FileNotFoundError(SOURCE)
if OUTPUT.exists():
    raise FileExistsError(f"No se sobrescribe un archivo existente: {OUTPUT}")
for filename, _ in CAPTURES:
    image = ATTACHMENTS / filename
    if not image.is_file():
        raise FileNotFoundError(image)

# Abre la evidencia, localiza las secciones y elimina las capturas que serán reemplazadas.
doc = Document(SOURCE)
if len(doc.inline_shapes) != 52:
    raise ValueError(f"Se esperaban 52 imágenes de origen; se encontraron {len(doc.inline_shapes)}.")

paragraphs = list(doc.paragraphs)
section_542 = next(
    (p for p in paragraphs if p.text.strip() == "5.4.2 Fragmentos representativos del código"),
    None,
)
section_543 = next(
    (p for p in paragraphs if p.text.strip() == "5.4.3 Capturas del código y explicación"),
    None,
)
if section_542 is None or section_543 is None:
    raise ValueError("No se encontraron los apartados de programación esperados.")

# Remove the five earlier screenshots that these map-specific captures replace.
for number in CAPTIONS_TO_REMOVE:
    caption = next(
        (
            p for p in doc.paragraphs
            if re.match(rf"Figura {number}\.", p.text.strip())
        ),
        None,
    )
    if caption is None:
        raise ValueError(f"No se encontró la captura anterior de la Figura {number}.")
    parent = caption._p.getparent()
    caption_index = parent.index(caption._p)
    following = parent[caption_index + 1] if caption_index + 1 < len(parent) else None
    if following is None or not following.xpath(".//a:blip"):
        raise ValueError(f"La imagen de la Figura {number} no está después de su pie.")
    parent.remove(following)
    parent.remove(caption._p)

# Inserta imágenes y pies en el orden definido por CAPTURES.
anchor = section_543._p
intro = doc.add_paragraph(
    "Capturas de los fragmentos explicados, presentadas en el mismo orden que los apartados anteriores."
)
intro.paragraph_format.keep_with_next = True
anchor.addprevious(intro._p)
for filename, explanation in CAPTURES:
    image_paragraph = doc.add_paragraph()
    image_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    image_paragraph.paragraph_format.keep_with_next = True
    image_paragraph.add_run().add_picture(str(ATTACHMENTS / filename), width=Inches(6.0))
    anchor.addprevious(image_paragraph._p)

    caption = doc.add_paragraph()
    caption.alignment = WD_ALIGN_PARAGRAPH.CENTER
    caption.paragraph_format.keep_together = True
    caption.add_run(f"Figura 0. {explanation}")
    anchor.addprevious(caption._p)

# Renumera pies de figura en todo el documento, incluso los contenidos en tablas.
number = 0
for paragraph in doc._element.body.iter():
    if paragraph.tag.endswith("}p"):
        for text_node in paragraph.iter():
            if text_node.tag.endswith("}t") and text_node.text:
                # El contador mutable permite actualizar la numeración desde la expresión regular.
                def next_caption(match):
                    nonlocal_number[0] += 1
                    return f"Figura {nonlocal_number[0]}."

                nonlocal_number = [number]
                text_node.text = re.sub(r"Figura\s+\d+\.", next_caption, text_node.text)
                number = nonlocal_number[0]

if number != 53:
    raise ValueError(f"Se esperaban 53 pies de figura después del reemplazo; se encontraron {number}.")
if len(doc.inline_shapes) != 54:
    raise ValueError(f"Se esperaban 54 imágenes tras el reemplazo; se encontraron {len(doc.inline_shapes)}.")

# Guarda y vuelve a abrir el archivo para verificar que el resultado persistido es correcto.
doc.save(OUTPUT)

# Reopen the saved file and verify image count and new captions in the requested order.
check = Document(OUTPUT)
if len(check.inline_shapes) != 54:
    raise ValueError("El documento guardado no conserva las 54 imágenes esperadas.")
new_captions = [
    p.text.strip()
    for p in check.paragraphs
    if p.text.strip().startswith("Figura ")
]
expected = [
    f"Figura {i}. {description}"
    for i, (_, description) in enumerate(CAPTURES, start=7)
]
if new_captions[6:13] != expected:
    raise ValueError(f"El orden de las capturas nuevas no coincide: {new_captions[6:13]}")
if "Dungeon Hunter" in "\n".join(p.text for p in check.paragraphs):
    raise ValueError("Se encontró un nombre anterior del videojuego.")
print(f"OK: {OUTPUT}")
print(f"Imágenes: {len(check.inline_shapes)}; pies de figura: {len(new_captions)}.")
print("Capturas del mapa en orden:")
for caption in expected:
    print(caption)
