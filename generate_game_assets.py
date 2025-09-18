from PIL import Image, ImageDraw
import os

OUTPUT_DIR = "assets/images"

def generate_noob_runner():
    """
    Genera una imagen de 64x64 de un 'Noob' de Roblox corriendo de perfil.
    """
    img = Image.new('RGBA', (64, 64), (0, 0, 0, 0)) # Fondo transparente
    draw = ImageDraw.Draw(img)

    # Colores del Noob
    skin = "#FFE99C"
    torso = "#0A83C8"
    legs = "#1C732F"
    outline = "#000000"

    # Piernas (en posición de correr)
    draw.rectangle([26, 44, 35, 60], fill=legs, outline=outline, width=2)
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
    """
    img = Image.new('RGBA', (32, 32), (0, 0, 0, 0)) # Fondo transparente
    draw = ImageDraw.Draw(img)

    block_fill = "#DA232A"
    outline = "#000000"
    shine = "#E74C52"

    draw.rectangle([2, 2, 29, 29], fill=block_fill, outline=outline, width=2)
    draw.rectangle([5, 5, 10, 10], fill=shine)
    
    filepath = os.path.join(OUTPUT_DIR, "obstacle.png")
    img.save(filepath)
    print(f"✔️  Imagen de obstáculo generada: {filepath}")

# --- INICIO DE NUEVA FUNCIÓN ---
def generate_sparkle_gif():
    """Genera un GIF animado de chispitas."""
    frames = []
    size = 64
    num_frames = 10

    for i in range(num_frames):
        frame = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(frame)
        
        # Estrella que se expande y contrae
        scale = i if i < num_frames / 2 else (num_frames - 1) - i
        scale *= 1.5 # Hacerla un poco más grande
        x, y = size // 2, size // 2
        
        points = [
            (x, y - 5 * scale), (x + 1 * scale, y - 1 * scale),
            (x + 5 * scale, y), (x + 1 * scale, y + 1 * scale),
            (x, y + 5 * scale), (x - 1 * scale, y + 1 * scale),
            (x - 5 * scale, y), (x - 1 * scale, y - 1 * scale)
        ]
        if scale > 0: # Evitar dibujar un polígono sin área
            draw.polygon(points, fill="#FFD700") # Color dorado

        frames.append(frame)

    filepath = os.path.join(OUTPUT_DIR, "sparkle.gif")
    frames[0].save(filepath, save_all=True, append_images=frames[1:], duration=80, loop=0, transparency=0, disposal=2)
    print(f"✔️  Animación de chispitas generada: {filepath}")
# --- FIN DE NUEVA FUNCIÓN ---

if __name__ == "__main__":
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    
    generate_noob_runner()
    generate_obstacle()
    generate_sparkle_gif() # Llamar a la nueva función
    
    print("\n¡Gráficos del juego listos!")

