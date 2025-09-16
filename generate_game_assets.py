from PIL import Image, ImageDraw
import os

OUTPUT_DIR = "assets/images"

def generate_noob_runner():
    """
    Genera una imagen de 64x64 de un 'Noob' de Roblox corriendo de perfil.
    Esto hará que el salto y la carrera se vean mucho más naturales.
    """
    img = Image.new('RGBA', (64, 64), (0, 0, 0, 0)) # Fondo transparente
    draw = ImageDraw.Draw(img)

    # Colores del Noob
    skin = "#FFE99C"
    torso = "#0A83C8"
    legs = "#1C732F"
    outline = "#000000"

    # Piernas (en posición de correr)
    # Pierna trasera
    draw.rectangle([26, 44, 35, 60], fill=legs, outline=outline, width=2)
    # Pierna delantera
    draw.rectangle([36, 44, 45, 60], fill=legs, outline=outline, width=2)

    # Torso
    draw.rectangle([25, 20, 46, 45], fill=torso, outline=outline, width=2)

    # Cabeza
    draw.rectangle([22, 4, 49, 22], fill=skin, outline=outline, width=2)
    # Ojo
    draw.rectangle([40, 10, 43, 13], fill=outline)

    # Brazo
    draw.rectangle([28, 22, 36, 38], fill=skin, outline=outline, width=2)
    
    filepath = os.path.join(OUTPUT_DIR, "noob_runner.png")
    img.save(filepath)
    print(f"✔️  Imagen del jugador generada: {filepath}")

def generate_obstacle():
    """
    Genera un obstáculo simple de 32x32, como un bloque rojo.
    Su tamaño es perfecto para que el jugador de 40x40 salte sobre él.
    """
    img = Image.new('RGBA', (32, 32), (0, 0, 0, 0)) # Fondo transparente
    draw = ImageDraw.Draw(img)

    # Colores del bloque
    block_fill = "#DA232A" # Rojo Roblox
    outline = "#000000"
    shine = "#E74C52"

    # Dibuja el bloque
    draw.rectangle([2, 2, 29, 29], fill=block_fill, outline=outline, width=2)
    # Añade un pequeño brillo para darle estilo
    draw.rectangle([5, 5, 10, 10], fill=shine)
    
    filepath = os.path.join(OUTPUT_DIR, "obstacle.png")
    img.save(filepath)
    print(f"✔️  Imagen de obstáculo generada: {filepath}")


if __name__ == "__main__":
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    
    generate_noob_runner()
    generate_obstacle()
    
    print("\n¡Gráficos del juego listos! Ahora tu minijuego se verá genial.")
