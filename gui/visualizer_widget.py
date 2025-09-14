from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QPixmap, QPen, QColor, QFont, QMovie
from PyQt6.QtCore import Qt

class VisualizerWidget(QWidget):
    """Un widget que dibuja una representación gráfica de una operación matemática."""

    def __init__(self):
        super().__init__()
        self.setMinimumSize(350, 400)
        self.operation_data = None
        
        try:
            # --- INICIO DE MEJORA DE GIF ---
            # Usamos QMovie para manejar GIFs animados
            self.movie = QMovie('assets/images/roblox-dance.gif')
            self.movie.frameChanged.connect(self.update) # Repintar el widget en cada cuadro
            self.movie.start()
            # --- FIN DE MEJORA DE GIF ---
        except Exception as e:
            print(f"No se pudo cargar la imagen del bloque: {e}")
            self.movie = None

    def update_visualization(self, num1, op, num2, result):
        self.operation_data = {
            "num1": num1, "op": op, "num2": num2, "result": result
        }
        self.update()

    def paintEvent(self, event):
        if not self.operation_data or self.operation_data["num1"] is None:
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        op = self.operation_data["op"]
        num1 = int(self.operation_data["num1"])
        num2 = int(self.operation_data["num2"])
        result = int(self.operation_data["result"])
        
        VISUALIZATION_LIMIT = 25
        if num1 > VISUALIZATION_LIMIT or num2 > VISUALIZATION_LIMIT or result > VISUALIZATION_LIMIT:
            self._draw_text_message(painter, "Números muy grandes para visualizar")
            return

        # Llama a la función de dibujo correspondiente
        if op == '+': self._draw_addition(painter, num1, num2)
        elif op == '-': self._draw_subtraction(painter, num1, num2)
        elif op == 'x': self._draw_multiplication(painter, num1, num2)
        elif op == '÷': self._draw_division(painter, num1, num2)
        else: self.operation_data = None

    def _draw_objects(self, painter, count, start_x=30, start_y=40, columns=6, x_spacing=40, y_spacing=40):
        if not self.movie:
            self._draw_text_message(painter, "Error: Falta roblox-dance.gif")
            return
        
        # Obtenemos el cuadro actual del GIF
        current_frame = self.movie.currentPixmap()
            
        for i in range(count):
            row = i // columns
            col = i % columns
            x = start_x + col * x_spacing
            y = start_y + row * y_spacing
            # Dibujamos el cuadro actual
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
        pen = QPen(QColor("#FFFFFF"), 2)
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

    def _draw_multiplication(self, painter, num1, num2):
        """Dibuja la visualización de una multiplicación con ajuste de línea automático."""
        num1_int, num2_int = int(num1), int(num2)
        pen = QPen(QColor("#FFFFFF"), 2)
        painter.setPen(pen)
        painter.setFont(QFont("Gill Sans Ultra Bold", 10))

        # --- LÓGICA DE AJUSTE DE LÍNEA ---
        margin = 30  # Margen izquierdo y derecho
        block_width, block_height = 40, 40
        group_x_spacing, group_y_spacing = 20, 60 # Espacio entre grupos

        # Posiciones iniciales
        current_x = margin
        current_y = 55

        # Ancho disponible en el widget
        available_width = self.width() - margin

        # num1 es el número de grupos, num2 es la cantidad por grupo
        for i in range(num1_int):
            group_width = num2_int * block_width
            
            # Si el grupo actual no cabe en la línea, saltar a la siguiente
            if current_x + group_width > available_width and current_x != margin:
                current_x = margin
                current_y += group_y_spacing

            # Dibujar la etiqueta del grupo
            painter.drawText(current_x, current_y - 15, f"Grupo {i+1}")
            
            # Dibujar los bloques del grupo
            self._draw_objects(painter, num2_int, start_x=current_x, start_y=current_y, columns=num2_int)
            
            # Actualizar la posición X para el siguiente grupo
            current_x += group_width + group_x_spacing

    def _draw_division(self, painter, num1, num2):
        self._draw_objects(painter, num1)
        group_size = num1 // num2
        pen = QPen(QColor("#DA232A"), 2, Qt.PenStyle.DashLine)
        painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)

        columns_used = 6
        for i in range(num2):
            start_index = i * group_size
            row = start_index // columns_used
            col = start_index % columns_used
            rect_x = 25 + col * 40
            rect_y = 35 + row * 40
            rect_width = group_size * 40 if (col + group_size) <= columns_used else (columns_used - col) * 40
            rect_height = 40
            painter.drawRoundedRect(rect_x, rect_y, rect_width, rect_height, 10, 10)

    def _draw_text_message(self, painter, message):
        pen = QPen(QColor("#FFFFFF"), 2)
        painter.setPen(pen)
        painter.setFont(QFont("Gill Sans Ultra Bold", 14))
        painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, message)