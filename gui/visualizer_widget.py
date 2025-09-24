from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QPixmap, QPen, QColor, QFont, QMovie, QTextDocument
from PyQt6.QtCore import Qt, QPointF

class VisualizerWidget(QWidget):
    """Un widget que dibuja una representación gráfica de una operación matemática."""

    def __init__(self):
        super().__init__()
        self.setMinimumSize(350, 400)
        self.operation_data = None
        self.fraction_data = None
        
        try:
            # QMovie para manejar GIFs animados
            self.movie = QMovie('assets/images/roblox-dance.gif')
            self.movie.frameChanged.connect(self.update)
            self.movie.start()
        except Exception as e:
            print(f"No se pudo cargar la imagen del bloque: {e}")
            self.movie = None

    def update_visualization(self, num1, op, num2, result):
        self.fraction_data = None
        self.operation_data = {
            "num1": num1, "op": op, "num2": num2, "result": result
        }
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
        
        VISUALIZATION_LIMIT = 100
        if num1 > VISUALIZATION_LIMIT or num2 > VISUALIZATION_LIMIT or result > VISUALIZATION_LIMIT:
            self._draw_text_message(painter, "Números muy grandes para visualizar")
            return

        if op == '+': self._draw_addition(painter, num1, num2)
        elif op == '-': self._draw_subtraction(painter, num1, num2)
        elif op == 'x': self._draw_multiplication(painter, num1, num2)
        elif op == '÷': self._draw_division(painter, num1, num2)
        else: self.operation_data = None

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

    def _draw_multiplication(self, painter, num1, num2):
        num1_int, num2_int = int(num1), int(num2)
        pen = QPen(QColor("#7E7E7E"), 2)
        painter.setPen(pen)
        painter.setFont(QFont("Gill Sans Ultra Bold", 10))

        margin = 30
        block_width, block_height = 40, 40
        group_x_spacing, group_y_spacing = 20, 60

        current_x = margin
        current_y = 55

        available_width = self.width() - margin

        for i in range(num1_int):
            group_width = num2_int * block_width
            
            if current_x + group_width > available_width and current_x != margin:
                current_x = margin
                current_y += group_y_spacing

            painter.drawText(current_x, current_y - 15, f"Grupo {i+1}")
            
            self._draw_objects(painter, num2_int, start_x=current_x, start_y=current_y, columns=num2_int)
            
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
        """Muestra un mensaje de texto centrado y con ajuste de línea."""
        doc = QTextDocument()
        doc.setHtml(f"<p style='color: #7e7e7e; font-size: 14pt; text-align: center;'>{message}</p>")
        doc.setTextWidth(self.width() - 20)
        
        painter.save()
        y_pos = (self.height() - doc.size().height()) / 2
        painter.translate(10, y_pos)
        doc.drawContents(painter)
        painter.restore()
