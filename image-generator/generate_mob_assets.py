from PIL import Image, ImageDraw
import os

def create_map_cow(path="assets/images/map_cow.png"):
    """Crea una imagen de una vaca de Minecraft."""
    img = Image.new('RGBA', (80, 60), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    # Colores
    blanco = "#E0E0E0"
    negro = "#3B3B3B"
    nariz = "#F7C5C6"

    # Cuerpo y cabeza
    draw.rectangle([10, 20, 70, 55], fill=blanco) # Cuerpo
    draw.rectangle([50, 5, 80, 30], fill=blanco) # Cabeza
    # Manchas
    draw.rectangle([15, 25, 30, 40], fill=negro)
    draw.rectangle([55, 40, 65, 50], fill=negro)
    draw.rectangle([60, 10, 70, 20], fill=negro)
    # Nariz y ojos
    draw.rectangle([70, 20, 80, 30], fill=nariz)
    draw.point((72, 12), fill=negro)
    draw.point((78, 12), fill=negro)
    img.save(path)
    print(f"Imagen '{path}' creada.")

def create_map_zombie(path="assets/images/map_zombie.png"):
    """Crea una imagen de un zombi de Minecraft."""
    img = Image.new('RGBA', (60, 100), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    # Colores
    piel = "#749D61"
    camisa = "#4A7B7B"
    pantalon = "#3A3A5A"

    # Cuerpo
    draw.rectangle([15, 25, 45, 70], fill=camisa) # Torso
    draw.rectangle([15, 70, 45, 95], fill=pantalon) # Pantalones
    # Cabeza
    draw.rectangle([10, 0, 50, 30], fill=piel)
    # Ojos (vacíos)
    draw.rectangle([18, 10, 24, 16], fill="black")
    draw.rectangle([36, 10, 42, 16], fill="black")
    img.save(path)
    print(f"Imagen '{path}' creada.")

def create_map_pig_king(path="assets/images/map_pig_king.png"):
    """Crea una imagen del cerdo con corona (Technoblade)."""
    img = Image.new('RGBA', (80, 70), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    # Colores
    rosa = "#F0A8A8"
    nariz = "#E08A8A"
    corona = "#FFD700"
    gema = "#D92A2A"

    # Cuerpo y cabeza
    draw.rectangle([5, 25, 75, 65], fill=rosa) # Cuerpo
    draw.rectangle([50, 10, 80, 40], fill=rosa) # Cabeza
    # Nariz y ojos
    draw.rectangle([75, 20, 85, 30], fill=nariz)
    draw.point((72, 18), fill="black")
    draw.point((78, 18), fill="black")
    # Corona
    draw.rectangle([50, 0, 80, 10], fill=corona)
    draw.rectangle([52, 2, 56, 6], fill=gema)
    draw.rectangle([62, 2, 66, 6], fill="#2A75D9") # Gema azul
    draw.rectangle([72, 2, 76, 6], fill=gema)
    img.save(path)
    print(f"Imagen '{path}' creada.")

if __name__ == "__main__":
    if not os.path.exists("assets/images"):
        os.makedirs("assets/images")
    create_map_cow()
    create_map_zombie()
    create_map_pig_king()
    print("\n¡Personajes del mapa generados!")
