from PIL import Image, ImageDraw
import os
import random

def create_mission_map_background(path="assets/images/mission_map_background.png"):
    """Crea una textura de hierba simple y repetible."""
    size = 100
    img = Image.new('RGBA', (size, size), "#5D9C59") # Verde base
    draw = ImageDraw.Draw(img)

    # Dibuja algunas briznas de hierba de diferentes tonos
    for _ in range(250):
        x = random.randint(0, size)
        y = random.randint(0, size)
        length = random.randint(3, 6)

        # Tonos de verde
        color = random.choice(["#78B978", "#4A8A4A", "#6EAC6E"])

        draw.line([(x, y), (x + length, y)], fill=color, width=1)

    img.save(path)
    print(f"Imagen '{path}' creada exitosamente.")

def create_mission_map_tree(path="assets/images/mission_map_tree.png"):
    """Crea una imagen de un árbol simple de estilo low-poly."""
    img = Image.new('RGBA', (80, 120), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Colores
    tronco = "#6F4E37"
    hojas1 = "#2C5F2D"
    hojas2 = "#3E8E41"
    hojas3 = "#57C84D"

    # Tronco
    draw.rectangle([35, 90, 45, 115], fill=tronco)

    # Hojas (tres triángulos superpuestos)
    draw.polygon([(40, 10), (10, 50), (70, 50)], fill=hojas3)
    draw.polygon([(40, 30), (15, 70), (65, 70)], fill=hojas2)
    draw.polygon([(40, 50), (20, 95), (60, 95)], fill=hojas1)

    img.save(path)
    print(f"Imagen '{path}' creada exitosamente.")


if __name__ == "__main__":
    if not os.path.exists("assets/images"):
        os.makedirs("assets/images")
        print("Directorio 'assets/images' creado.")

    create_mission_map_background()
    create_mission_map_tree()

    print("\n¡Recursos del mapa de misiones generados!")
