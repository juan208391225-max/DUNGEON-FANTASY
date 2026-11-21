import os
import shutil

print("🚀 Organizando el proyecto DUNGEON-FANTASY...")

# 1. Crear carpetas organizadoras
os.makedirs('docs', exist_ok=True)
os.makedirs('assets/audio', exist_ok=True)
os.makedirs('assets/images', exist_ok=True)

# 2. Mover evidencias, videos y comprimidos fuera de la raíz
IGNORAR = ['organizar_repo.py', '_repo.py', '.git', '.venv', '.gitignore']

for archivo in os.listdir('.'):
    # Evitar mover carpetas o scripts principales
    if os.path.isdir(archivo) or archivo in IGNORAR:
        continue

    ext = os.path.splitext(archivo)[1].lower()

    if ext in ['.docx', '.pdf', '.mp4', '.zip']:
        shutil.move(archivo, os.path.join('docs', archivo))
        print(f"📄 Movido a /docs: {archivo}")
    elif ext in ['.mp3', '.wav', '.ogg']:
        shutil.move(archivo, os.path.join('assets', 'audio', archivo))
        print(f"🎵 Movido a /assets/audio: {archivo}")
    elif ext in ['.png', '.jpg', '.jpeg']:
        shutil.move(archivo, os.path.join('assets', 'images', archivo))
        print(f"🖼️ Movido a /assets/images: {archivo}")

# 3. Crear .gitignore para ignorar la carpeta docs y temporales
gitignore_text = """.idea/
.venv/
__pycache__/
*.pyc
docs/
*.docx
*.mp4
*.zip
"""

with open('.gitignore', 'w', encoding='utf-8') as f:
    f.write(gitignore_text)
print("✅ .gitignore creado")

# 4. Crear README.md profesional
readme_text = """# 🗡️ DUNGEON FANTASY

> An interactive 2D RPG / Dungeon Crawler game built with **Python**, **Pygame**, and **MySQL**, developed as part of my software engineering portfolio during 10th Grade and SENA Software Programming Technician program.

---

## 📌 Project Overview

**Dungeon Fantasy** is a Python desktop game where players navigate dungeon levels, interact with game elements, and save their progress. This repository showcases practical application of object-oriented programming, Pygame event loops, sprite rendering, and relational database management with MySQL.

## 🛠️ Tech Stack & Tools

- **Language:** Python 3.x
- **Game Engine:** Pygame
- **Database:** MySQL (Player data & progress persistence)
- **IDE:** PyCharm / VS Code

---

## 📂 Project Structure

```text
DUNGEON-FANTASY/
├── assets/
│   ├── audio/      # Sound effects and soundtrack (.mp3)
│   └── images/     # Sprites, maps, and visual elements
├── jugador/        # Player sprites and logic
├── enemigos/       # Enemy logic
├── mapa/           # Map rendering
├── main.py         # Main game loop
├── .gitignore      # Git ignore rules
└── README.md       # Project documentation
```

---

## ▶️ How to Run

```bash
pip install pygame mysql-connector-python
python main.py
```
"""

with open('README.md', 'w', encoding='utf-8') as f:
    f.write(readme_text)
print("✅ README.md creado")

print("🎉 ¡Proyecto organizado!")