import os
from PIL import Image, ImageDraw

# --- Configuración ---
SIZE = (10, 10)
OUTPUT_DIR = "assets/images"
COLORS = {
    "black": (0, 0, 0, 255),
    "white": (255, 255, 255, 255)
}

# --- Funciones para dibujar cada patrón ---

def draw_plus(draw, color):
    """Dibuja un patrón de cruces."""
    draw.line((2, 5, 8, 5), fill=color, width=1)
    draw.line((5, 2, 5, 8), fill=color, width=1)

def draw_minus(draw, color):
    """Dibuja un patrón de líneas horizontales."""
    draw.line((1, 5, 9, 5), fill=color, width=1)

def draw_multiply(draw, color):
    """Dibuja un patrón de puntos en 'x'."""
    draw.point([(3, 3), (7, 3), (5, 5), (3, 7), (7, 7)], fill=color)

def draw_divide(draw, color):
    """Dibuja una línea diagonal."""
    draw.line((1, 9, 9, 1), fill=color, width=1)

# --- Lógica principal del script ---

def generate_pattern(name, draw_func, color_name):
    """Función genérica para crear y guardar una imagen de patrón."""
    
    # Crea una nueva imagen con fondo transparente (RGBA)
    image = Image.new("RGBA", SIZE, (255, 255, 255, 0))
    draw = ImageDraw.Draw(image)
    
    color_value = COLORS[color_name]
    draw_func(draw, color_value)
    
    # Guarda el archivo
    filename = f"{name}_pattern_{color_name}.png"
    filepath = os.path.join(OUTPUT_DIR, filename)
    image.save(filepath)
    print(f"✔️  Creado: {filepath}")

if __name__ == "__main__":
    # Asegurarse de que el directorio de salida exista
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"Directorio creado: {OUTPUT_DIR}")

    patterns = {
        "plus": draw_plus,
        "minus": draw_minus,
        "multiply": draw_multiply,
        "divide": draw_divide
    }

    # Generar todas las combinaciones (4 patrones x 2 colores)
    for name, func in patterns.items():
        for color_name in COLORS:
            generate_pattern(name, func, color_name)
            
    print("\n¡Las 8 imágenes de patrones han sido generadas exitosamente!")