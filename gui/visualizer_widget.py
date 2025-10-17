from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QPixmap, QPen, QColor, QFont, QMovie, QTextDocument, QFontMetrics
from PyQt6.QtCore import Qt, QPointF, QRect

class VisualizerWidget(QWidget):
    """Un widget que dibuja una representación gráfica de una operación matemática."""

    def __init__(self, multiplication_method='traditional'):
        super().__init__()
        self.setMinimumSize(350, 400)
        self.operation_data = None
        self.fraction_data = None
        self.multiplication_method = multiplication_method # Nuevo atributo para el método de multiplicación

        try:
            # QMovie para manejar GIFs animados
            self.movie = QMovie('assets/images/roblox-dance.gif')
            self.movie.frameChanged.connect(self.update)
            self.movie.start()
        except Exception as e:
            print(f"No se pudo cargar la imagen del bloque: {e}")
            self.movie = None

    def update_visualization(self, num1, op, num2, result, multiplication_method=None):
        self.fraction_data = None
        self.operation_data = {
            "num1": num1, "op": op, "num2": num2, "result": result
        }
        if multiplication_method:
            self.multiplication_method = multiplication_method
        self.update()

    def update_fraction_visualization(self, op, f1, f2, res):
        self.operation_data = None # Limpia los datos de enteros para cambiar de modo
        self.fraction_data = {"op": op, "f1": f1, "f2": f2, "res": res}
        self.update()

    def clear_all(self):
        """Limpia ambos modos de visualización."""
        self.operation_data = None
        self.fraction_data = None
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
        result = int(self.operation_data["result"])

        VISUALIZATION_LIMIT = 10000 # Límite aumentado para el método tradicional
        if num1 > VISUALIZATION_LIMIT or num2 > VISUALIZATION_LIMIT or result > VISUALIZATION_LIMIT * VISUALIZATION_LIMIT:
            self._draw_text_message(painter, "Números muy grandes para visualizar")
            return

        if op == '+': self._draw_addition(painter, num1, num2)
        elif op == '-': self._draw_subtraction(painter, num1, num2)
        elif op == 'x':
            if self.multiplication_method == 'japanese':
                self._draw_japanese_multiplication(painter, num1, num2)
            else: # 'traditional' por defecto
                self._draw_traditional_multiplication(painter, num1, num2)
        elif op == '÷': self._draw_division(painter, num1, num2)
        else: self.operation_data = None

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
        h_line_gap = 20  # Aumentado para mayor separación
        digit_group_gap = 35
        digit_lines = {}

        # --- Dibuja líneas para num1 (colores por dígito) ---
        line_pen = QPen(QColor("#FFFFFF"), 4, cap=Qt.PenCapStyle.RoundCap)

        start_y = self.height() * 0.25
        end_y = self.height() * 0.88  # Acortado para no tocar el resultado
        current_x = self.width() * 0.5 - (len(num1_str) * digit_group_gap * 1.5) # Centrado inicial

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
        current_y = self.height() * 0.38 # Subido ligeramente

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

            # Posiciones de los conteos de dígitos del resultado
            text_pos = QPointF(avg_x - 10, self.height() - 20)
            if num1_len > 1 and num2_len > 1:
                if place_value == 2: # Centenas
                    text_pos.setX(self.width() * 0.2)
                elif place_value == 1: # Decenas
                    text_pos.setX(self.width() * 0.5 - 10)
                elif place_value == 0: # Unidades
                    text_pos.setX(self.width() * 0.8)

            painter.drawText(text_pos, str(len(points)))

        painter.restore()

    def _draw_fraction_operation(self, painter):
        if not self.fraction_data: return

        op = self.fraction_data['op']
        f1_num, f1_den = self.fraction_data['f1']
        f2_num, f2_den = self.fraction_data['f2']
        res_num, res_den = self.fraction_data['res']

        painter.setPen(QPen(QColor("white"), 2))
        painter.setFont(QFont("Gill Sans Ultra Bold", 20))

        # Posiciones de las fracciones
        x1, y1 = 50, 100
        x2, y2 = 200, 100

        # Dibujar primera fracción
        painter.drawText(x1, y1 - 20, f1_num)
        painter.drawLine(x1 - 10, y1, x1 + 30, y1)
        painter.drawText(x1, y1 + 40, f1_den)

        # Dibujar operador
        painter.drawText(x1 + 80, y1 + 15, op)

        # Dibujar segunda fracción
        painter.drawText(x2, y2 - 20, f2_num)
        painter.drawLine(x2 - 10, y2, x2 + 30, y2)
        painter.drawText(x2, y2 + 40, f2_den)

        # Dibujar líneas de guía
        pen = QPen(QColor("#DA232A"), 2, Qt.PenStyle.DashLine)
        painter.setPen(pen)

        if op in ['+', '-']: # Multiplicación cruzada
            painter.drawLine(x1, y1 - 25, x2 + 10, y2 + 25) # num1 * den2
            painter.drawLine(x2, y2 - 25, x1 + 10, y1 + 25) # num2 * den1
            painter.drawLine(x1, y1 + 25, x2 + 10, y2 + 25) # den1 * den2
        elif op == 'x': # Multiplicación directa
            painter.drawLine(x1, y1 - 25, x2 + 10, y2 - 25) # num1 * num2
            painter.drawLine(x1, y1 + 25, x2 + 10, y2 + 25) # den1 * den2

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
        self._draw_objects(painter, num1)
        columns_used = 6
        start_x_num2 = 30 + (num1 % columns_used) * 40
        start_y_num2 = 40 + (num1 // columns_used) * 40

        if num1 % columns_used != 0:
             start_y_num2 -= 40
        else:
            start_x_num2 = 30

        self._draw_objects(painter, num2, start_x=start_x_num2, start_y=start_y_num2)
        pen = QPen(QColor("#7e7e7e"), 2)
        painter.setPen(pen)
        painter.setFont(QFont("Gill Sans Ultra Bold", 20))
        plus_x = 25 + ((num1 - 1) % columns_used) * 40 + 40
        plus_y = 65 + ((num1 - 1) // columns_used) * 40
        painter.drawText(plus_x, plus_y, "+")

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

        # Colores para los dígitos del segundo número
        digit_colors = [QColor("#00A2FF"), QColor("#32CD32"), QColor("#FF4500"), QColor("#DCBC04")]

        # Determinar el ancho máximo para alinear todo a la derecha
        max_width = max(
            metrics.horizontalAdvance(num1_str),
            metrics.horizontalAdvance(f"x {num2_str}"),
            metrics.horizontalAdvance(result_str)
        )

        right_margin = 30
        x_pos_align = self.width() - right_margin
        y_pos = 80
        line_height = metrics.height() + 10

        # Dibujar num1
        painter.setPen(QColor("#FFFFFF"))
        painter.drawText(QRect(0, y_pos, x_pos_align, line_height), int(Qt.AlignmentFlag.AlignRight), num1_str)
        y_pos += line_height

        # Dibujar 'x' y num2 (con colores)
        current_draw_x = x_pos_align
        # Dibujar num2_str de derecha a izquierda con colores
        for i, digit in enumerate(reversed(num2_str)):
            color = digit_colors[i % len(digit_colors)]
            painter.setPen(color)
            char_width = metrics.horizontalAdvance(digit)
            current_draw_x -= char_width
            painter.drawText(int(current_draw_x), int(y_pos + metrics.ascent()), digit)

        # Dibujar "x "
        painter.setPen(QColor("#FFFFFF"))
        op_prefix = "x "
        op_prefix_width = metrics.horizontalAdvance(op_prefix)
        current_draw_x -= op_prefix_width
        painter.drawText(int(current_draw_x), int(y_pos + metrics.ascent()), op_prefix)
        y_pos += line_height

        # Dibujar primera línea
        painter.setPen(QPen(QColor("#7C7A7A"), 2))
        painter.drawLine(x_pos_align - max_width, y_pos, x_pos_align, y_pos)
        y_pos += 5

        # Dibujar productos parciales si num2 tiene más de 1 dígito
        if len(num2_str) > 1:
            indent = 0
            for i, digit in enumerate(reversed(num2_str)):
                color = digit_colors[i % len(digit_colors)]
                painter.setPen(color) # Establecer color para este producto parcial

                partial_product = num1 * int(digit)
                partial_str = str(partial_product) + (" " * indent)

                painter.drawText(QRect(0, y_pos, x_pos_align, line_height), int(Qt.AlignmentFlag.AlignRight), partial_str)

                y_pos += line_height
                indent += 1

            # Dibujar segunda línea
            painter.setPen(QPen(QColor("#7C7A7A"), 2))
            painter.drawLine(x_pos_align - max_width, y_pos, x_pos_align, y_pos)
            y_pos += 5

        # Dibujar el resultado final
        painter.setPen(QColor("#DA232A"))
        painter.drawText(QRect(0, y_pos, x_pos_align, line_height), int(Qt.AlignmentFlag.AlignRight), result_str)

        painter.restore()

    def _draw_division(self, painter, num1, num2):
        if num2 == 0:
            self._draw_text_message(painter, "No se puede dividir por cero")
            return

        self._draw_objects(painter, num1)
        group_size = num1 // num2
        pen = QPen(QColor("#DA232A"), 2, Qt.PenStyle.DashLine)
        painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)

        columns_used = 6
        for i in range(num2):
            start_index = i * group_size

            # Asegurarse de que el grupo no exceda el número total de objetos
            if start_index + group_size > num1:
                break

            row_start = start_index // columns_used
            col_start = start_index % columns_used

            # Coordenadas iniciales del rectángulo
            rect_x = 25 + col_start * 40
            rect_y = 35 + row_start * 40

            # Manejar grupos que abarcan varias filas
            remaining_in_row = columns_used - col_start
            if group_size <= remaining_in_row:
                # El grupo cabe en una sola fila
                rect_width = group_size * 40
                painter.drawRoundedRect(rect_x, rect_y, rect_width, 40, 10, 10)
            else:
                # El grupo abarca varias filas
                # Parte en la primera fila
                width1 = remaining_in_row * 40
                painter.drawRoundedRect(rect_x, rect_y, width1, 40, 10, 10)

                # Filas completas intermedias
                remaining_items = group_size - remaining_in_row
                full_rows = remaining_items // columns_used
                for j in range(full_rows):
                    rect_y += 40
                    painter.drawRoundedRect(25, rect_y, columns_used * 40, 40, 10, 10)

                # Parte en la última fila
                last_row_items = remaining_items % columns_used
                if last_row_items > 0:
                    rect_y += 40
                    painter.drawRoundedRect(25, rect_y, last_row_items * 40, 40, 10, 10)

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

