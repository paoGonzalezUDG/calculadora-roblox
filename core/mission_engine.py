import random

class MissionEngine:
    """Gestiona la carga y selección de misiones matemáticas con tema de Roblox."""
    def __init__(self):
        self.missions = [
            {"id": 1, "theme": "Roblox", "text": "Estás construyendo una pared con 40 bloques. Si cada fila usa 8 bloques, ¿cuántas filas podrás construir?", "answer": "5", "reward": "oof_sound", "operation_type": "División"},
            {"id": 2, "theme": "Roblox", "text": "Ganas 15 Robux por pasar un nivel y tu amigo te da 10 más. ¿Cuántos Robux tienes ahora?", "answer": "25", "reward": "oof_sound", "operation_type": "Suma"},
            {"id": 3, "theme": "Roblox", "text": "Estás en un 'obby' (parkour) con 50 plataformas. Ya has saltado 32. ¿Cuántas plataformas te faltan para llegar al final?", "answer": "18", "reward": "oof_sound", "operation_type": "Resta"},
            {"id": 4, "theme": "Roblox", "text": "En 'Adopt Me!', quieres comprar una mascota que cuesta 600 bucks. Si tienes 450, ¿cuántos más necesitas conseguir?", "answer": "150", "reward": "oof_sound", "operation_type": "Resta"},
            {"id": 5, "theme": "Roblox", "text": "Tu inventario tiene 3 espadas que hacen 10 de daño cada una. ¿Cuánto daño total hacen las tres juntas?", "answer": "30", "reward": "oof_sound", "operation_type": "Multiplicación"},
            {"id": 6, "theme": "Roblox", "text": "Una poción de velocidad cuesta 50 Robux. Si quieres comprar una para ti y para tus 3 amigos, ¿cuántos Robux necesitas?", "answer": "200", "reward": "oof_sound", "operation_type": "Multiplicación"},
            {"id": 7, "theme": "Roblox", "text": "En 'Bloxburg', una pizza cuesta 24 dólares. Si pagas con un billete de 50, ¿cuánto cambio te deben dar?", "answer": "26", "reward": "oof_sound", "operation_type": "Resta"},
            {"id": 8, "theme": "Roblox", "text": "Si un sombrero cuesta 75 Robux y compras 2, ¿cuántos Robux gastas?", "answer": "150", "reward": "oof_sound", "operation_type": "Multiplicación"},
            {"id": 9, "theme": "Roblox", "text": "En un juego tienes 120 monedas. Compras una espada por 85. ¿Cuántas monedas te quedan?", "answer": "35", "reward": "oof_sound", "operation_type": "Resta"},
            {"id": 10, "theme": "Roblox", "text": "Si ganas 25 Robux cada vez que completas una misión y completas 4, ¿cuántos Robux ganas?", "answer": "100", "reward": "oof_sound", "operation_type": "Multiplicación"},
            {"id": 11, "theme": "Roblox", "text": "Un cofre tiene 60 gemas y las compartes con 5 amigos. ¿Cuántas gemas recibe cada uno?", "answer": "12", "reward": "oof_sound", "operation_type": "División"},
            {"id": 12, "theme": "Roblox", "text": "En un obby hay 80 obstáculos. Ya pasaste 65. ¿Cuántos faltan?", "answer": "15", "reward": "oof_sound", "operation_type": "Resta"},
            {"id": 13, "theme": "Roblox", "text": "Un accesorio cuesta 45 Robux y tienes 90. ¿Cuántos accesorios puedes comprar?", "answer": "2", "reward": "oof_sound", "operation_type": "División"},
            {"id": 14, "theme": "Roblox", "text": "Si recolectas 12 bloques cada minuto, ¿cuántos bloques tendrás en 6 minutos?", "answer": "72", "reward": "oof_sound", "operation_type": "Multiplicación"},
            {"id": 15, "theme": "Roblox", "text": "Tu mascota necesita 250 bucks para una poción. Si ya tienes 175, ¿cuánto falta?", "answer": "75", "reward": "oof_sound", "operation_type": "Resta"},
            {"id": 16, "theme": "Roblox", "text": "Si un pase de juego cuesta 400 Robux y ya tienes 150, ¿cuántos más necesitas?", "answer": "250", "reward": "oof_sound", "operation_type": "Resta"},
            {"id": 17, "theme": "Roblox", "text": "Recolectas 5 gemas por nivel. ¿Cuántas gemas tendrás tras jugar 9 niveles?", "answer": "45", "reward": "oof_sound", "operation_type": "Multiplicación"},
            {"id": 18, "theme": "Roblox", "text": "En un servidor hay 18 jugadores. Si 7 se van, ¿cuántos quedan?", "answer": "11", "reward": "oof_sound", "operation_type": "Resta"},
            {"id": 19, "theme": "Roblox", "text": "Construyes una torre con 120 bloques y quieres 10 pisos iguales. ¿Cuántos bloques tendrá cada piso?", "answer": "12", "reward": "oof_sound", "operation_type": "División"},
            {"id": 20, "theme": "Roblox", "text": "Compras 3 mascotas y cada una cuesta 150 bucks. ¿Cuánto gastas en total?", "answer": "450", "reward": "oof_sound", "operation_type": "Multiplicación"},
            {"id": 21, "theme": "Roblox", "text": "Si ganas 200 Robux y luego gastas 125 en un accesorio, ¿cuántos Robux te quedan?", "answer": "75", "reward": "oof_sound", "operation_type": "Resta"},
            {"id": 22, "theme": "Roblox", "text": "En 'Tower of Hell' subes 7 pisos y cada piso tiene 15 escalones. ¿Cuántos escalones subiste en total?", "answer": "105", "reward": "oof_sound", "operation_type": "Multiplicación"},
            {"id": 23, "theme": "Roblox", "text": "Tienes 64 bloques y quieres hacer torres de 8 bloques cada una. ¿Cuántas torres podrás construir?", "answer": "8", "reward": "oof_sound", "operation_type": "División"},
            {"id": 24, "theme": "Roblox", "text": "Si 3 espadas cuestan 270 Robux en total, ¿cuánto cuesta cada una?", "answer": "90", "reward": "oof_sound", "operation_type": "División"},
            {"id": 25, "theme": "Roblox", "text": "En 'Brookhaven' una casa cuesta 750 bucks. Si ya tienes 500, ¿cuánto más necesitas?", "answer": "250", "reward": "oof_sound", "operation_type": "Resta"},
            {"id": 26, "theme": "Roblox", "text": "Un huevo de mascota cuesta 600 bucks. Si compras 2, ¿cuánto pagas en total?", "answer": "1200", "reward": "oof_sound", "operation_type": "Multiplicación"},
            {"id": 27, "theme": "Roblox", "text": "Un coche cuesta 900 Robux. Si ya tienes 1,200, ¿cuánto te sobra después de comprarlo?", "answer": "300", "reward": "oof_sound", "operation_type": "Resta"},
            {"id": 28, "theme": "Roblox", "text": "Un evento reparte 240 monedas entre 12 jugadores. ¿Cuántas recibe cada uno?", "answer": "20", "reward": "oof_sound", "operation_type": "División"},
            {"id": 29, "theme": "Roblox", "text": "Tienes 2 mascotas. Una cuesta 300 y otra 450 bucks. ¿Cuánto gastaste en total?", "answer": "750", "reward": "oof_sound", "operation_type": "Suma"},
            {"id": 30, "theme": "Roblox", "text": "En una carrera avanzas 60 metros. Otro jugador avanza 45. ¿Cuántos metros más avanzaste?", "answer": "15", "reward": "oof_sound", "operation_type": "Resta"},
            {"id": 31, "theme": "Roblox", "text": "Si cada caja trae 12 pociones y compras 4 cajas, ¿cuántas pociones tienes?", "answer": "48", "reward": "oof_sound", "operation_type": "Multiplicación"},
            {"id": 32, "theme": "Roblox", "text": "Una mascota se alimenta con 3 galletas al día. ¿Cuántas galletas necesitará en 7 días?", "answer": "21", "reward": "oof_sound", "operation_type": "Multiplicación"},
            {"id": 33, "theme": "Roblox", "text": "Si tienes 500 Robux y gastas 3/5 en ropa, ¿cuántos Robux gastaste?", "answer": "300", "reward": "oof_sound", "operation_type": "Fracción"},
            {"id": 34, "theme": "Roblox", "text": "De 120 bloques usaste 1/4 para hacer una base. ¿Cuántos bloques usaste?", "answer": "30", "reward": "oof_sound", "operation_type": "Fracción"},
            {"id": 35, "theme": "Roblox", "text": "Si ganas 2/3 de 90 monedas en un reto, ¿cuántas monedas ganas?", "answer": "60", "reward": "oof_sound", "operation_type": "Fracción"},
            {"id": 36, "theme": "Roblox", "text": "Un jugador tiene 150 Robux y gasta 2/5 en pociones. ¿Cuánto gasta?", "answer": "60", "reward": "oof_sound", "operation_type": "Fracción"},
            {"id": 37, "theme": "Roblox", "text": "Si recoges 3/10 de 200 bloques, ¿cuántos bloques recogiste?", "answer": "60", "reward": "oof_sound", "operation_type": "Fracción"},
            {"id": 38, "theme": "Roblox", "text": "En un obby superas 80 obstáculos. Si completas 3/4, ¿cuántos obstáculos pasaste?", "answer": "60", "reward": "oof_sound", "operation_type": "Fracción"},
            {"id": 39, "theme": "Roblox", "text": "Tienes 5/8 de 64 Robux. ¿Cuántos Robux son?", "answer": "40", "reward": "oof_sound", "operation_type": "Fracción"},
            {"id": 40, "theme": "Roblox", "text": "Si un escudo cuesta 2/3 de 90 Robux, ¿cuánto cuesta?", "answer": "60", "reward": "oof_sound", "operation_type": "Fracción"},
            {"id": 41, "theme": "Roblox", "text": "En un servidor hay 48 jugadores. Si 1/2 son de tu equipo, ¿cuántos jugadores tienes en tu equipo?", "answer": "24", "reward": "oof_sound", "operation_type": "Fracción"},
            {"id": 42, "theme": "Roblox", "text": "Si gastas 1/5 de 200 Robux en decoraciones, ¿cuánto gastaste?", "answer": "40", "reward": "oof_sound", "operation_type": "Fracción"},
            {"id": 43, "theme": "Roblox", "text": "De 300 monedas, usas 3/10 para comprar comida. ¿Cuántas monedas gastas?", "answer": "90", "reward": "oof_sound", "operation_type": "Fracción"},
            {"id": 44, "theme": "Roblox", "text": "Tienes 100 bloques. Usas 7/10 en una torre. ¿Cuántos bloques usaste?", "answer": "70", "reward": "oof_sound", "operation_type": "Fracción"},
            {"id": 45, "theme": "Roblox", "text": "De 72 Robux, gastas 3/4 en un arma. ¿Cuánto gastaste?", "answer": "54", "reward": "oof_sound", "operation_type": "Fracción"},
            {"id": 46, "theme": "Roblox", "text": "Si ganas 5/6 de 120 puntos en un reto, ¿cuántos puntos ganas?", "answer": "100", "reward": "oof_sound", "operation_type": "Fracción"},
            {"id": 47, "theme": "Roblox", "text": "Si completas 2/5 de 150 plataformas, ¿cuántas pasaste?", "answer": "60", "reward": "oof_sound", "operation_type": "Fracción"},
            {"id": 48, "theme": "Roblox", "text": "Un evento da 3/4 de 80 monedas a cada jugador. ¿Cuántas monedas son?", "answer": "60", "reward": "oof_sound", "operation_type": "Fracción"},
            {"id": 49, "theme": "Roblox", "text": "Tienes 2/3 de 90 Robux guardados. ¿Cuánto es eso?", "answer": "60", "reward": "oof_sound", "operation_type": "Fracción"},
            {"id": 50, "theme": "Roblox", "text": "Si una mascota cuesta 5/10 de 200 bucks, ¿cuánto cuesta?", "answer": "100", "reward": "oof_sound", "operation_type": "Fracción"}
        ]

    def get_random_mission(self):
        """Devuelve una misión aleatoria de la lista."""
        return random.choice(self.missions)
