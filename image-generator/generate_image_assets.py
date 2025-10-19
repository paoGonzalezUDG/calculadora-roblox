from PIL import Image, ImageDraw

def create_noob_head(path="assets/images/noob_head.png"):
    """Crea un ícono pixel art de una cabeza de noob de Roblox."""
    img = Image.new('RGBA', (40, 40), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Colores
    amarillo_roblox = "#F5C841"
    negro_pixel = "#232428"

    # Cabeza
    draw.rectangle([5, 5, 35, 35], fill=amarillo_roblox)

    # Ojos
    draw.rectangle([12, 12, 16, 18], fill=negro_pixel)
    draw.rectangle([24, 12, 28, 18], fill=negro_pixel)

    # Boca
    draw.rectangle([16, 25, 24, 28], fill=negro_pixel)

    img.save(path)
    print(f"Imagen '{path}' creada exitosamente.")

def create_level_dot(path="assets/images/level_dot.png"):
    """Crea un ícono de nivel completado (círculo verde con estrella)."""
    img = Image.new('RGBA', (35, 35), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Círculo verde
    draw.ellipse([2, 2, 33, 33], fill="#2ECC71", outline="#27AE60", width=2)

    # Estrella blanca en el centro
    centro_x, centro_y = 17.5, 17.5
    radio = 8
    puntos = []
    for i in range(5):
        angulo = -90 + i * 144  # Ángulo para cada punta de la estrella
        angulo_rad = angulo * (3.14159 / 180)
        puntos.append((centro_x + radio * (0.5 if i % 2 == 1 else 1) * 2**0.5 * (-1)**i * (i % 2 - 0.5) * 2,
                       centro_y + radio * (0.5 if i % 2 == 1 else 1) * 2**0.5 * (-1)**i * (i % 2 - 0.5) * 2))

    # Reajuste de puntos para una estrella más simple
    star_points = [
        (17.5, 7), (20.5, 15), (28.5, 15), (22.5, 20),
        (24.5, 28), (17.5, 23), (10.5, 28), (12.5, 20),
        (6.5, 15), (14.5, 15)
    ]
    draw.polygon(star_points, fill="white")

    img.save(path)
    print(f"Imagen '{path}' creada exitosamente.")

def create_level_dot_locked(path="assets/images/level_dot_locked.png"):
    """Crea un ícono de nivel bloqueado (círculo gris con candado)."""
    img = Image.new('RGBA', (30, 30), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Círculo gris
    draw.ellipse([2, 2, 28, 28], fill="#95A5A6", outline="#7F8C8D", width=2)

    # Candado negro
    # Arco superior
    draw.arc([9, 6, 21, 16], start=180, end=0, fill="#2C3E50", width=3)
    # Cuerpo del candado
    draw.rectangle([7, 14, 23, 24], fill="#2C3E50")

    img.save(path)
    print(f"Imagen '{path}' creada exitosamente.")

if __name__ == "__main__":
    import os
    # Asegurarse de que el directorio de imágenes exista
    if not os.path.exists("assets/images"):
        os.makedirs("assets/images")
        print("Directorio 'assets/images' creado.")

    create_noob_head()
    create_level_dot()
    create_level_dot_locked()
    print("\n¡Todos los recursos gráficos del mapa han sido generados!")
