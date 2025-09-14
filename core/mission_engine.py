import random

class MissionEngine:
    """Gestiona la carga y selección de misiones matemáticas con tema de Roblox."""
    def __init__(self):
        self.missions = [
            {
                "id": 1,
                "theme": "Roblox",
                "text": "Estás construyendo una pared con 40 bloques. Si cada fila usa 8 bloques, ¿cuántas filas podrás construir?",
                "answer": "5",
                "reward": "oof_sound"
            },
            {
                "id": 2,
                "theme": "Roblox",
                "text": "Ganas 15 Robux por pasar un nivel y tu amigo te da 10 más. ¿Cuántos Robux tienes ahora?",
                "answer": "25",
                "reward": "oof_sound"
            },
            {
                "id": 3,
                "theme": "Roblox",
                "text": "Estás en un 'obby' (parkour) con 50 plataformas. Ya has saltado 32. ¿Cuántas plataformas te faltan para llegar al final?",
                "answer": "18",
                "reward": "oof_sound"
            },
            {
                "id": 4,
                "theme": "Roblox",
                "text": "En 'Adopt Me!', quieres comprar una mascota que cuesta 600 bucks. Si tienes 450, ¿cuántos más necesitas conseguir?",
                "answer": "150",
                "reward": "oof_sound"
            },
            {
                "id": 5,
                "theme": "Roblox",
                "text": "Tu inventario tiene 3 espadas que hacen 10 de daño cada una. ¿Cuánto daño total hacen las tres juntas?",
                "answer": "30",
                "reward": "oof_sound"
            },
            {
                "id": 6,
                "theme": "Roblox",
                "text": "Una poción de velocidad cuesta 50 Robux. Si quieres comprar una para ti y para tus 3 amigos, ¿cuántos Robux necesitas?",
                "answer": "200",
                "reward": "oof_sound"
            },
            {
                "id": 7,
                "theme": "Roblox",
                "text": "En 'Bloxburg', una pizza cuesta 24 dólares. Si pagas con un billete de 50, ¿cuánto cambio te deben dar?",
                "answer": "26",
                "reward": "oof_sound"
            }
        ]

    def get_random_mission(self):
        """Devuelve una misión aleatoria de la lista."""
        return random.choice(self.missions)