from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QPixmap, QPen, QColor, QFont, QMovie, QTextDocument
from PyQt6.QtCore import Qt, QPointF

class VisualizerWidget(QWidget):

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

    def paintEvent(self, event):
        painter = QPainter(self)
        # Limpia el fondo con el color del tema actual para evitar artefactos de dibujo
        painter.fillRect(self.rect(), self.palette().window().color())

        # Si hay datos de fracción, dibuja la visualización de fracción
        if self.fraction_data and self.fraction_data.get("op"):
            self._draw_fraction_operation(painter)
            return

        # Si hay datos de operación de enteros, dibuja la visualización de GIFs
        if self.operation_data and self.operation_data.get("num1") is not None:
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
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
            return

    def _draw_single_fraction(self, painter, num, den, pos):
        """Dibuja una sola fracción y devuelve las coordenadas clave para las líneas de guía."""
        font_metrics = painter.fontMetrics()
        num_str, den_str = str(num), str(den)
        num_width = font_metrics.horizontalAdvance(num_str)
        den_width = font_metrics.horizontalAdvance(den_str)
        line_width = max(num_width, den_width) + 10

        # Coordenadas del numerador
        num_pos = QPointF(pos.x() + (line_width - num_width) / 2, pos.y())
        painter.drawText(num_pos, num_str)
        
        # Coordenadas de la línea de fracción
        line_y = pos.y() + font_metrics.height() * 0.5
        painter.drawLine(QPointF(pos.x(), line_y), QPointF(pos.x() + line_width, line_y))
        
        # Coordenadas del denominador
        den_y = pos.y() + font_metrics.height() * 1.5
        den_pos = QPointF(pos.x() + (line_width - den_width) / 2, den_y)
        painter.drawText(den_pos, den_str)
        
        # Devuelve los puntos centrales para dibujar las líneas de guía
        return {
            "num_center": QPointF(num_pos.x() + num_width / 2, num_pos.y() - font_metrics.height() / 4),
            "den_center": QPointF(den_pos.x() + den_width / 2, den_pos.y() - font_metrics.height() / 4),
            "width": line_width
        }
    
    def _draw_fraction_operation(self, painter):
        """Dibuja la visualización completa de la operación de fracciones."""
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        font = QFont("Gill Sans Ultra Bold", 20)
        painter.setFont(font)
        painter.setPen(QPen(QColor("#FFFFFF"), 2))
        
        op = self.fraction_data["op"]
        f1_num, f1_den = self.fraction_data["f1"]
        f2_num, f2_den = self.fraction_data["f2"]
        res_num, res_den = self.fraction_data["res"]

        y_pos = self.height() / 2 - 40
        x_pos = 20
        
        # Dibuja la primera fracción
        f1_geom = self._draw_single_fraction(painter, f1_num, f1_den, QPointF(x_pos, y_pos))
        x_pos += f1_geom["width"] + 20
        
        # Dibuja el operador
        painter.drawText(QPointF(x_pos, y_pos + 25), op)
        x_pos += 40
        
        # Dibuja la segunda fracción
        f2_geom = self._draw_single_fraction(painter, f2_num, f2_den, QPointF(x_pos, y_pos))
        x_pos += f2_geom["width"] + 20
        
        # Dibuja el signo de igual y el resultado
        painter.drawText(QPointF(x_pos, y_pos + 25), "=")
        x_pos += 40
        self._draw_single_fraction(painter, res_num, res_den, QPointF(x_pos, y_pos))
        
        # Prepara el lápiz para las líneas de guía
        guide_pen = QPen(QColor("#DA232A"), 3, Qt.PenStyle.DashLine)
        guide_pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(guide_pen)

        if op == 'x': # Multiplicación directa -> Líneas rectas
            painter.drawLine(f1_geom["num_center"], f2_geom["num_center"])
            painter.drawLine(f1_geom["den_center"], f2_geom["den_center"])
        elif op in ['+', '-']: # Suma o resta -> Líneas cruzadas
            painter.drawLine(f1_geom["num_center"], f2_geom["den_center"])
            painter.drawLine(f1_geom["den_center"], f2_geom["num_center"])

    def _draw_text_message(self, painter, message):
        """Muestra un mensaje de texto centrado y con ajuste de línea."""
        doc = QTextDocument()

        doc.setHtml(f"<p style='color: white; font-size: 14pt; text-align: center;'>{message}</p>")
        doc.setTextWidth(self.width() - 20) # Ancho del documento con un margen
        
        painter.save()
        # Calculamos la posición Y para centrar verticalmente
        y_pos = (self.height() - doc.size().height()) / 2
        painter.translate(10, y_pos) # Movemos el pintor a la posición correcta
        doc.drawContents(painter)
        painter.restore()
        
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