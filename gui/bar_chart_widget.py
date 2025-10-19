from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QColor, QFont, QPen, QBrush
from PyQt6.QtCore import Qt, QRectF

class BarChartWidget(QWidget):
    """
    Un widget reutilizable que dibuja una gráfica de barras vertical
    para mostrar el dominio de las operaciones.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(300)
        self.data = {}
        self.bar_colors = [
            QColor("#00A2FF"), # Suma
            QColor("#DA232A"), # Resta
            QColor("#28A745"), # Multiplicación
            QColor("#FFCC00"), # División
            QColor("#8A2BE2")  # Fracciones
        ]

    def set_data(self, data_dict):
        """
        Establece los datos para la gráfica.
        El diccionario debe tener la forma {'Suma': 80, 'Resta': 50, ...}.
        """
        self.data = data_dict
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        if not self.data:
            painter.setFont(QFont("Gill Sans", 12))
            painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, "No hay suficientes datos para generar la gráfica.")
            return

        # --- Márgenes y dimensiones ---
        margin_top, margin_bottom, margin_left, margin_right = 30, 60, 40, 20
        chart_width = self.width() - margin_left - margin_right
        chart_height = self.height() - margin_top - margin_bottom
        num_bars = len(self.data)

        if num_bars == 0:
            return

        bar_width = (chart_width / num_bars) * 0.6
        bar_spacing = (chart_width / num_bars) * 0.4

        # --- Eje Y (Líneas y etiquetas) ---
        painter.setFont(QFont("Gill Sans", 9))
        painter.setPen(QColor("#AAAAAA"))
        for i in range(11):
            y = margin_top + (i / 10) * chart_height
            painter.drawLine(margin_left - 5, int(y), self.width() - margin_right, int(y))
            painter.drawText(0, int(y) - 5, margin_left - 10, 20, Qt.AlignmentFlag.AlignRight, f"{100 - i * 10}%")

        # --- Dibujar las barras ---
        painter.setFont(QFont("Gill Sans Ultra Bold", 10))
        for i, (label, value) in enumerate(self.data.items()):
            bar_x = margin_left + i * (bar_width + bar_spacing) + (bar_spacing / 2)
            bar_height = (value / 100) * chart_height
            bar_y = margin_top + chart_height - bar_height

            # Barra
            color = self.bar_colors[i % len(self.bar_colors)]
            painter.setBrush(QBrush(color))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRect(int(bar_x), int(bar_y), int(bar_width), int(bar_height))

            # Etiqueta de la operación (abajo)
            painter.setPen(QColor("white"))
            rect = QRectF(bar_x - 10, margin_top + chart_height + 5, bar_width + 20, 50)
            # CORRECCIÓN: Se elimina Qt.AlignmentFlag.TextWordWrap que causaba el error.
            painter.drawText(rect, Qt.AlignmentFlag.AlignHCenter, label)

            # Etiqueta del valor (encima de la barra)
            painter.drawText(QRectF(bar_x, bar_y - 20, bar_width, 20), Qt.AlignmentFlag.AlignCenter, f"{value:.0f}%")

