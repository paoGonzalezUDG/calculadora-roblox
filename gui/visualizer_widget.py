import random

from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt6.QtGui import QPainter, QPixmap, QPen, QColor, QFont, QMovie, QTextDocument, QFontMetrics
from PyQt6.QtCore import Qt, QPointF, QRect, QTimer, QSize, QLineF

class VisualizerWidget(QWidget):
    """Un widget que dibuja una representación gráfica de una operación matemática."""

    def __init__(self, multiplication_method='traditional', division_method='traditional', parent=None):
        super().__init__(parent)
        self.setObjectName("VisualizerPanel")
        self.setMinimumSize(350, 400)

        self.operation_data = None
        self.fraction_data = None

        self.is_displaying_operation = False

        self.multiplication_method = multiplication_method
        self.division_method = division_method # Nuevo atributo
        self.movie = QMovie('assets/images/roblox-dance.gif')

        if self.movie.isValid():
            self.movie.start()
            self.movie.frameChanged.connect(self.update)
        else:
            print("Advertencia: No se pudo cargar 'roblox-dance.gif'")
            self.movie = None

        self._setup_welcome_screen()
        self.fact_timer = QTimer(self)
        self.fact_timer.timeout.connect(self._change_fun_fact)
        self.fact_timer.start(15000) # Cambia cada 15 segundos

    def _setup_welcome_screen(self):
        """Configura los widgets para el estado inactivo."""
        self.welcome_layout = QVBoxLayout(self)
        self.welcome_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.welcome_layout.setSpacing(15)

        self.welcome_gif_label = QLabel(self)
        welcome_movie = QMovie("assets/images/minecraft-fox.gif")
        if welcome_movie.isValid():
            welcome_movie.setScaledSize(QSize(225, 253))
            self.welcome_gif_label.setMovie(welcome_movie)
            welcome_movie.start()
        else:
            self.welcome_gif_label.setText("?")

        self.welcome_text_label = QLabel(self)
        self.welcome_text_label.setObjectName("WelcomeFactLabel")
        self.welcome_text_label.setWordWrap(True)
        self.welcome_text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.fun_facts = [
            "¿Sabías que un 'stack' completo en Minecraft (64 bloques) es el resultado de 8x8 o 4x4x4?",
            "En muchos juegos, la probabilidad de conseguir un objeto raro se calcula con fracciones y porcentajes.",
            "Los mundos de juegos como Roblox y Minecraft se construyen usando coordenadas (X, Y, Z), ¡igual que en un plano cartesiano!",
            "La velocidad de tu personaje y el daño de tus armas son solo números que se suman, restan y multiplican constantemente.",
            "¡Cada misión que completas aquí te hace más rápido para resolver problemas en tus juegos favoritos!",
            "Entender la división te ayuda a saber cuántos recursos necesitas para 'craftear' múltiples objetos en Minecraft.",
            "Las fracciones son útiles para dividir botines entre amigos en juegos multijugador como Roblox.",
            "Los patrones de construcción en Minecraft a menudo siguen secuencias matemáticas como la serie de Fibonacci.",
            "Calcular áreas y perímetros es esencial para diseñar estructuras eficientes en tus juegos favoritos.",
            "El sistema 'DevEx' para cambiar Robux por dinero real usa tasas de conversión y porcentajes, como en el mundo financiero.",
            "Las matemáticas son la clave para entender y dominar tus juegos favoritos.",
            "Los saltos perfectos en un 'obby' se calculan usando vectores y ángulos. ¡Pura geometría para no caerse!",
            "Los circuitos de Redstone funcionan con lógica booleana. Una antorcha encendida es un 1 (verdadero) y una apagada es un 0 (falso).",
            "Para que los mundos parezcan infinitos, los juegos usan algoritmos de generación procedural que crean terreno usando secuencias matemáticas.",
            "La lógica matemática detrás de los videojuegos puede ayudarte a mejorar en ellos.",
            "Las fracciones te ayudan a compartir recursos de manera justa en juegos multijugador.",
            "La multiplicación rápida puede ayudarte a calcular puntos y recompensas en tus juegos favoritos.",
            "Entender la división es útil para administrar tu inventario en juegos como Minecraft.",
            "Las matemáticas son el lenguaje universal de los videojuegos.",
            "Las coordenadas (X, Y, Z) que ves al presionar F3 son un plano cartesiano en 3D que te ayuda a navegar por el mundo.",
            "La práctica constante de habilidades matemáticas puede llevarte a la victoria en tus juegos favoritos.",
            "La colaboración y el trabajo en equipo son esenciales para resolver problemas en juegos multijugador.",
            "Los desarrolladores usan fórmulas para calcular el daño de una espada o la velocidad de un coche en sus juegos.",
            "Un solo bloque de agua puede hidratar un área de 9x9 bloques de tierra, ¡un total de 80 cultivos!",
            "La economía de juegos como 'Adopt Me!' se basa en la probabilidad. ¡Conseguir una mascota legendaria es un evento estadístico muy raro!",
            "La física de los juegos calcula la parábola de tu salto para saber exactamente dónde aterrizarás.",
            "¡Diviértete y disfruta del viaje mientras aprendes y juegas!",
            "Para hacer TNT se necesita una proporción de 5 de pólvora por 4 de arena.",
            "La probabilidad de conseguir una mascota legendaria es un cálculo de fracciones.",
            "Repartir un premio de Robux entre jugadores es un simple problema de división."
        ]

        self.welcome_layout.addStretch()
        self.welcome_layout.addWidget(self.welcome_gif_label)
        self.welcome_layout.addWidget(self.welcome_text_label)
        self.welcome_layout.addStretch()

        self._change_fun_fact()

    def _change_fun_fact(self):
        """Elige y muestra un nuevo dato curioso."""
        fact = random.choice(self.fun_facts)
        self.welcome_text_label.setText(f"<b style='color: #36D14F;font-size: 16pt;'>¿Sabías que...?</b><br>{fact}")

    def clear_all(self):
        """Limpia ambos modos de visualización."""
        self.is_displaying_operation = False
        self.operation_data = None
        self.fraction_data = None
        # Muestra los elementos de bienvenida
        for i in range(self.welcome_layout.count()):
            widget = self.welcome_layout.itemAt(i).widget()
            if widget:
                widget.show()
        self._change_fun_fact() # Muestra un nuevo dato al limpiar
        self.fact_timer.start()
        self.update()

    def update_visualization(self, num1, op, num2, result, multiplication_method=None, division_method=None, **kwargs):
        """Prepara los datos para visualizar una operación simple."""
        self.is_displaying_operation = True
        self.fraction_data = None
        self.multiplication_method = kwargs.get('multiplication_method', self.multiplication_method)
        self.division_method = kwargs.get('division_method', self.division_method)
        self.operation_data = {"type": "simple", "num1": num1, "op": op, "num2": num2, "result": result}
        # Oculta los elementos de bienvenida
        for i in range(self.welcome_layout.count()):
            widget = self.welcome_layout.itemAt(i).widget()
            if widget:
                widget.hide()
        self.fact_timer.stop()

        """self.operation_data = {
            "num1": num1, "op": op, "num2": num2, "result": result
        }
        if multiplication_method:
            self.multiplication_method = multiplication_method
        if division_method: # Nuevo
            self.division_method = division_method"""

        self.update()

    def update_fraction_visualization(self, op, f1, f2, res):
        self.is_displaying_operation = True
        self.operation_data = None # Limpia los datos de enteros para cambiar de modo
        self.fraction_data = {"op": op, "f1": f1, "f2": f2, "res": res}
        # Oculta los elementos de bienvenida
        for i in range(self.welcome_layout.count()):
            widget = self.welcome_layout.itemAt(i).widget()
            if widget:
                widget.hide()
        self.fact_timer.stop()

        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        if self.fraction_data:
            self._draw_fraction_operation(painter)
            return

        if not self.operation_data or self.operation_data["num1"] is None:
            return

        op = self.operation_data["op"]
        num1 = int(self.operation_data["num1"])
        num2 = int(self.operation_data["num2"])
        result = self.operation_data["result"] # Puede ser float para división

        VISUALIZATION_LIMIT = 10000
        if num1 > VISUALIZATION_LIMIT or num2 > VISUALIZATION_LIMIT:
            self._draw_text_message(painter, "Números muy grandes para visualizar")
            return

        if op == '+': self._draw_addition(painter, num1, num2)
        elif op == '-': self._draw_subtraction(painter, num1, num2)
        elif op == 'x':
            if self.multiplication_method == 'japanese':
                self._draw_japanese_multiplication(painter, num1, num2)
            else:
                self._draw_traditional_multiplication(painter, num1, int(result))
        elif op == '÷':
            # Nueva lógica para seleccionar el método de división
            if self.division_method == 'japanese':
                self._draw_japanese_division(painter, num1, num2)
            else: # 'traditional' por defecto
                self._draw_traditional_division(painter, num1, num2)
        else:
            self.operation_data = None

    def get_intersection(self, line1, line2):
        """Calcula el punto de intersección de dos segmentos de línea."""
        p1, p2 = line1
        p3, p4 = line2

        x1, y1 = p1.x(), p1.y()
        x2, y2 = p2.x(), p2.y()
        x3, y3 = p3.x(), p3.y()
        x4, y4 = p4.x(), p4.y()

        den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        if den == 0:
            return None # Las líneas son paralelas

        t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
        u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / den

        if 0 <= t <= 1 and 0 <= u <= 1:
            ix = x1 + t * (x2 - x1)
            iy = y1 + t * (y2 - y1)
            return QPointF(ix, iy)

        return None

    def _draw_japanese_multiplication(self, painter, num1, num2):
        """Dibuja la multiplicación usando el método de líneas japonés."""
        num1_str = str(int(num1))
        num2_str = str(int(num2))

        if len(num1_str) > 2 or len(num2_str) > 2 or num1 == 0 or num2 == 0:
            self._draw_text_message(painter, "El método japonés se muestra\npara números de 1 o 2 dígitos.")
            return

        painter.save()

        # Colores para los dígitos del primer número
        digit_colors = [QColor("#DCBC04"), QColor("#FF4500"), QColor("#32CD32")]

        # --- Dibuja el texto de la operación en la parte superior con colores ---
        operation_font = QFont("Gill Sans Ultra Bold", 24)
        painter.setFont(operation_font)
        metrics = QFontMetrics(operation_font)

        # Calcular ancho total para centrar
        num1_width = sum([metrics.horizontalAdvance(char) for char in num1_str])
        operator_width = metrics.horizontalAdvance(" x ")
        num2_width = metrics.horizontalAdvance(num2_str)
        total_width = num1_width + operator_width + num2_width

        current_x = (self.width() - total_width) / 2
        y_pos = metrics.ascent() + 10

        # Dibujar num1 dígito por dígito con color
        for i, digit in enumerate(num1_str):
            painter.setPen(digit_colors[i % len(digit_colors)])
            painter.drawText(QPointF(current_x, y_pos), digit)
            current_x += metrics.horizontalAdvance(digit)

        # Dibujar 'x'
        painter.setPen(QColor("#7C7A7A"))
        painter.drawText(QPointF(current_x, y_pos), " x ")
        current_x += metrics.horizontalAdvance(" x ")

        # Dibujar num2
        painter.setPen(QColor("#00A2FF"))
        painter.drawText(QPointF(current_x, y_pos), num2_str)

        # --- Parámetros de Dibujo ---
        v_line_gap = 15
        h_line_gap = 20
        digit_group_gap = 35
        digit_lines = {}

        # --- Dibuja líneas para num1 (colores por dígito) ---
        line_pen = QPen(QColor("#FFFFFF"), 4, cap=Qt.PenCapStyle.RoundCap)

        start_y = self.height() * 0.25
        end_y = self.height() * 0.88
        current_x = self.width() * 0.5 - (len(num1_str) * digit_group_gap * 1.5)

        for i, digit in enumerate(num1_str):
            line_pen.setColor(digit_colors[i % len(digit_colors)])
            painter.setPen(line_pen)

            key = (1, i)
            digit_lines[key] = []
            for j in range(int(digit)):
                p1 = QPointF(current_x, start_y)
                p2 = QPointF(current_x, end_y)
                painter.drawLine(p1, p2)
                digit_lines[key].append((p1, p2))
                current_x += v_line_gap
            current_x += digit_group_gap

        # --- Dibuja líneas para num2 (azules) ---
        line_pen.setColor(QColor("#00A2FF"))
        painter.setPen(line_pen)

        start_x = self.width() * 0.1
        end_x = self.width() * 0.9
        current_y = self.height() * 0.38

        for i, digit in enumerate(num2_str):
            key = (2, i)
            digit_lines[key] = []
            for j in range(int(digit)):
                p1 = QPointF(start_x, current_y)
                p2 = QPointF(end_x, current_y)
                painter.drawLine(p1,p2)
                digit_lines[key].append((p1,p2))
                current_y += h_line_gap
            current_y += digit_group_gap

        # --- Encuentra y agrupa las intersecciones ---
        intersection_groups = {}
        num1_len, num2_len = len(num1_str), len(num2_str)

        for i in range(num1_len):
            for j in range(num2_len):
                place_value = (num1_len - 1 - i) + (num2_len - 1 - j)
                if place_value not in intersection_groups:
                    intersection_groups[place_value] = []

                for l1 in digit_lines.get((1, i), []):
                    for l2 in digit_lines.get((2, j), []):
                        p = self.get_intersection(l1, l2)
                        if p:
                            intersection_groups[place_value].append(p)

        # --- Dibuja las intersecciones y los conteos ---
        colors = [QColor("#FF5555"), QColor("#55FF55"), QColor("#FFFF55"), QColor("#FF55FF")]
        painter.setFont(QFont("Gill Sans Ultra Bold", 18))

        for place_value, points in sorted(intersection_groups.items()):
            if not points: continue

            color = colors[place_value % len(colors)]
            painter.setPen(color)
            painter.setBrush(color)

            for p in points:
                painter.drawEllipse(p, 6, 6)

            avg_x = sum(p.x() for p in points) / len(points)

            text_pos = QPointF(avg_x - 10, self.height() - 20)
            if num1_len > 1 and num2_len > 1:
                if place_value == 2:
                    text_pos.setX(self.width() * 0.2)
                elif place_value == 1:
                    text_pos.setX(self.width() * 0.5 - 10)
                elif place_value == 0:
                    text_pos.setX(self.width() * 0.8)

            painter.drawText(text_pos, str(len(points)))

        painter.restore()

    def _draw_fraction_operation(self, painter):
        if not self.fraction_data: return

        op = self.fraction_data['op']
        f1_num, f1_den = self.fraction_data['f1']
        f2_num, f2_den = self.fraction_data['f2']

        painter.setPen(QPen(QColor("#7D7C7C"), 2))
        painter.setFont(QFont("Gill Sans Ultra Bold", 20))

        w, h = self.width(), self.height()
        f1_x, f2_x = w * 0.25, w * 0.75
        y_num, y_den = h * 0.4, h * 0.6
        line_y = (y_num + y_den) / 2 - 10

        # Dibujar fracciones
        painter.drawText(QPointF(f1_x, y_num), f1_num)
        painter.drawLine(int(f1_x - 15), int(line_y), int(f1_x + 25), int(line_y))
        painter.drawText(QPointF(f1_x, y_den), f1_den)

        painter.drawText(QPointF(w * 0.5 - 10, line_y + 10), op)

        painter.drawText(QPointF(f2_x, y_num), f2_num)
        painter.drawLine(int(f2_x - 15), int(line_y), int(f2_x + 25), int(line_y))
        painter.drawText(QPointF(f2_x, y_den), f2_den)

        # Dibujar líneas de guía
        pen = QPen(QColor("#DA232A"), 2, Qt.PenStyle.DashLine)
        painter.setPen(pen)

        p1_num_pt = QPointF(f1_x + 5, y_num - 20)
        p1_den_pt = QPointF(f1_x + 5, y_den - 10)
        p2_num_pt = QPointF(f2_x + 5, y_num - 20)
        p2_den_pt = QPointF(f2_x + 5, y_den - 10)

        if op in ['+', '-'] and f1_den == f2_den:
            op_point = QPointF(w * 0.5, y_num - 20)
            painter.drawLine(p1_num_pt, op_point)
            painter.drawLine(p2_num_pt, op_point)
            painter.drawLine(p1_den_pt, p2_den_pt)
        elif op in ['+', '-'] and f1_den != f2_den:
            painter.drawLine(p1_num_pt, p2_den_pt)
            painter.drawLine(p2_num_pt, p1_den_pt)
            painter.drawLine(p1_den_pt, p2_den_pt)
        elif op == 'x':
            painter.drawLine(p1_num_pt, p2_num_pt)
            painter.drawLine(p1_den_pt, p2_den_pt)
        elif op == '÷':
            painter.drawLine(p1_num_pt, p2_den_pt)
            painter.drawLine(p1_den_pt, p2_num_pt)

    def _draw_objects(self, painter, count, start_x=30, start_y=40, columns=6, x_spacing=40, y_spacing=40):
        if not self.movie:
            self._draw_text_message(painter, "Error: Falta roblox-dance.gif")
            return

        current_frame = self.movie.currentPixmap()
        for i in range(count):
            row = i // columns
            col = i % columns
            x = start_x + col * x_spacing
            y = start_y + row * y_spacing
            painter.drawPixmap(x, y, 32, 32, current_frame)

    def _draw_addition(self, painter, num1, num2):
        columns = 6
        x_spacing = 40
        y_spacing = 40
        start_x = 30
        start_y = 40

        if not self.movie:
            self._draw_text_message(painter, "Error: Falta roblox-dance.gif")
            return
        current_frame = self.movie.currentPixmap()

        for i in range(num1):
            row = i // columns
            col = i % columns
            x = start_x + col * x_spacing
            y = start_y + row * y_spacing
            painter.drawPixmap(x, y, 32, 32, current_frame)

        rows_used_by_num1 = (num1 + columns - 1) // columns if num1 > 0 else 0
        second_part_start_row = rows_used_by_num1

        plus_x = start_x
        plus_y = start_y + second_part_start_row * y_spacing
        pen = QPen(QColor("#7e7e7e"), 2)
        painter.setPen(pen)
        painter.setFont(QFont("Gill Sans Ultra Bold", 20))
        painter.drawText(int(plus_x + 4), int(plus_y + 28), "+")

        for i in range(num2):
            grid_pos = i + 1
            row_offset = grid_pos // columns
            col = grid_pos % columns

            x = start_x + col * x_spacing
            y = start_y + (second_part_start_row + row_offset) * y_spacing
            painter.drawPixmap(x, y, 32, 32, current_frame)

    def _draw_subtraction(self, painter, num1, num2):
        self._draw_objects(painter, num1)
        pen = QPen(QColor("#DA232A"), 3)
        painter.setPen(pen)

        columns_used = 6
        for i in range(num1 - num2, num1):
            row = i // columns_used
            col = i % columns_used
            x = 30 + col * 40
            y = 40 + row * 40
            painter.drawLine(x, y, x + 32, y + 32)
            painter.drawLine(x + 32, y, x, y + 32)

    def _draw_traditional_multiplication(self, painter, num1, num2):
        painter.save()
        font = QFont("Gill Sans Ultra Bold", 22)
        painter.setFont(font)
        metrics = QFontMetrics(font)

        num1_str = str(num1)
        num2_str = str(num2)
        result_str = str(num1 * num2)

        digit_colors = [QColor("#00A2FF"), QColor("#32CD32"), QColor("#FF4500"), QColor("#DCBC04")]

        max_width = max(
            metrics.horizontalAdvance(num1_str),
            metrics.horizontalAdvance(f"x {num2_str}"),
            metrics.horizontalAdvance(result_str)
        )

        right_margin = 30
        x_pos_align = self.width() - right_margin
        y_pos = 80
        line_height = metrics.height() + 10

        painter.setPen(QColor("#FFFFFF"))
        painter.drawText(QRect(0, y_pos, x_pos_align, line_height), int(Qt.AlignmentFlag.AlignRight), num1_str)
        y_pos += line_height

        current_draw_x = x_pos_align
        for i, digit in enumerate(reversed(num2_str)):
            color = digit_colors[i % len(digit_colors)]
            painter.setPen(color)
            char_width = metrics.horizontalAdvance(digit)
            current_draw_x -= char_width
            painter.drawText(int(current_draw_x), int(y_pos + metrics.ascent()), digit)

        painter.setPen(QColor("#FFFFFF"))
        op_prefix = "x "
        op_prefix_width = metrics.horizontalAdvance(op_prefix)
        current_draw_x -= op_prefix_width
        painter.drawText(int(current_draw_x), int(y_pos + metrics.ascent()), op_prefix)
        y_pos += line_height

        painter.setPen(QPen(QColor("#7C7A7A"), 2))
        painter.drawLine(x_pos_align - max_width, y_pos, x_pos_align, y_pos)
        y_pos += 5

        if len(num2_str) > 1:
            indent = 0
            for i, digit in enumerate(reversed(num2_str)):
                color = digit_colors[i % len(digit_colors)]
                painter.setPen(color)

                partial_product = num1 * int(digit)
                partial_str = str(partial_product) + (" " * indent)

                painter.drawText(QRect(0, y_pos, x_pos_align, line_height), int(Qt.AlignmentFlag.AlignRight), partial_str)

                y_pos += line_height
                indent += 1

            painter.setPen(QPen(QColor("#7C7A7A"), 2))
            painter.drawLine(x_pos_align - max_width, y_pos, x_pos_align, y_pos)
            y_pos += 5

        painter.setPen(QColor("#DA232A"))
        painter.drawText(QRect(0, y_pos, x_pos_align, line_height), int(Qt.AlignmentFlag.AlignRight), result_str)

        painter.restore()

    def _draw_traditional_division(self, painter, num1, num2):
        if num2 == 0:
            self._draw_text_message(painter, "No se puede dividir por cero")
            return

        self._draw_objects(painter, num1)
        quotient = num1 // num2
        pen = QPen(QColor("#DA232A"), 2, Qt.PenStyle.DashLine)
        painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)

        columns_used = 6
        for i in range(num2):
            start_index = i * quotient
            if start_index + quotient > num1: break

            row_start = start_index // columns_used
            col_start = start_index % columns_used
            rect_x = 25 + col_start * 40
            rect_y = 35 + row_start * 40

            remaining_in_row = columns_used - col_start
            if quotient <= remaining_in_row:
                rect_width = quotient * 40
                painter.drawRoundedRect(rect_x, rect_y, rect_width, 40, 10, 10)
            else:
                width1 = remaining_in_row * 40
                painter.drawRoundedRect(rect_x, rect_y, width1, 40, 10, 10)
                remaining_items = quotient - remaining_in_row
                full_rows = remaining_items // columns_used
                for j in range(full_rows):
                    rect_y += 40
                    painter.drawRoundedRect(25, rect_y, columns_used * 40, 40, 10, 10)
                last_row_items = remaining_items % columns_used
                if last_row_items > 0:
                    rect_y += 40
                    painter.drawRoundedRect(25, rect_y, last_row_items * 40, 40, 10, 10)

    def _draw_japanese_division(self, painter, num1, num2):
        if num2 == 0:
            self._draw_text_message(painter, "No se puede dividir por cero.")
            return
        if num1 > 50 or num2 > 9: # Límite para que sea legible
            self._draw_text_message(painter, "El método japonés se muestra para\ndividendos pequeños y divisores de 1 dígito.")
            return

        painter.save()

        quotient = num1 // num2
        remainder = num1 % num2

        # --- Colores ---
        dividend_color = QColor("#00A2FF")
        divisor_color = QColor("#DA232A")
        intersection_color = QColor("#FF9900")

        # --- Dibuja el texto de la operación con colores ---
        operation_font = QFont("Gill Sans Ultra Bold", 24)
        painter.setFont(operation_font)
        metrics = QFontMetrics(operation_font)

        parts = [
            (str(num1), dividend_color), (" ÷ ", QColor("#FFFFFF")),
            (str(num2), divisor_color), (" = ", QColor("#FFFFFF")),
            (str(quotient), QColor("#FFFFFF"))
        ]
        if remainder > 0:
            parts.extend([(" R: ", QColor("#FFFFFF")), (str(remainder), QColor("#CCCCCC"))])

        total_width = sum([metrics.horizontalAdvance(part[0]) for part in parts])
        current_x = (self.width() - total_width) / 2
        y_pos = metrics.ascent() + 10

        for text, color in parts:
            painter.setPen(color)
            painter.drawText(QPointF(current_x, y_pos), text)
            current_x += metrics.horizontalAdvance(text)

        # --- Parámetros de Dibujo ---
        line_pen = QPen(QColor("#FFFFFF"), 4, cap=Qt.PenCapStyle.RoundCap)
        h_line_gap = 15

        # --- Dibuja líneas para el DIVIDENDO (horizontales, azules) ---
        dividend_lines = []
        start_x, end_x = self.width() * 0.1, self.width() * 0.9
        current_y = self.height() * 0.3
        line_pen.setColor(dividend_color)
        painter.setPen(line_pen)
        for _ in range(num1):
            p1 = QPointF(start_x, current_y)
            p2 = QPointF(end_x, current_y)
            painter.drawLine(p1, p2)
            dividend_lines.append((p1,p2))
            current_y += h_line_gap

        # --- Dibuja líneas para el DIVISOR y encuentra intersecciones ---
        divisor_line_groups = []
        v_start_y, v_end_y = self.height() * 0.25, self.height() * 0.9
        v_line_gap = (self.width() * 0.8) / (quotient + 1)
        line_pen.setColor(divisor_color)
        painter.setPen(line_pen)

        for i in range(quotient):
            group_lines = []
            group_x = self.width() * 0.1 + (i + 1) * v_line_gap
            for j in range(num2):
                x_pos = group_x + j * 12
                p1 = QPointF(x_pos, v_start_y)
                p2 = QPointF(x_pos, v_end_y)
                painter.drawLine(p1, p2)
                group_lines.append((p1, p2))
            divisor_line_groups.append(group_lines)

        # --- Dibuja las intersecciones (bolitas naranjas) ---
        painter.setBrush(intersection_color)
        painter.setPen(Qt.PenStyle.NoPen)
        for h_line in dividend_lines:
            for group in divisor_line_groups:
                for v_line in group:
                    p = self.get_intersection(h_line, v_line)
                    if p:
                        painter.drawEllipse(p, 5, 5)

        # --- Dibuja el resultado en la parte inferior ---
        painter.setFont(QFont("Gill Sans Ultra Bold", 28))
        painter.setPen(intersection_color) # CAMBIO: Usar color naranja
        result_text = str(quotient)
        result_metrics = QFontMetrics(painter.font())
        result_width = result_metrics.horizontalAdvance(result_text)
        result_x = (self.width() - result_width) / 2
        # Ajusta la posición Y para que esté más abajo, con un margen inferior de 5px.
        result_y = self.height() - result_metrics.descent() - 5
        painter.drawText(QPointF(result_x, result_y), result_text)

        painter.restore()

    def _draw_text_message(self, painter, message):
        """Muestra un mensaje de texto centrado y con ajuste de línea."""
        doc = QTextDocument()
        doc.setHtml(f"<p style='color: #7e7e7e; font-size: 14pt; text-align: center;'>{message}</p>")
        doc.setTextWidth(self.width() - 20)

        painter.save()
        y_pos = (self.height() - doc.size().height()) / 2
        painter.translate(10, y_pos)
        doc.drawContents(painter)
        painter.restore()

