import csv
import os
from collections import defaultdict
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from .bar_chart_widget import BarChartWidget

HISTORY_FILE = "mission_history.csv"

class EvaluationDialog(QDialog):
    """
    Una ventana emergente que calcula y muestra el dominio de las operaciones
    en una gráfica de barras.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Evaluación de Dominio")
        self.setModal(True)
        self.setMinimumSize(600, 450)

        main_layout = QVBoxLayout(self)

        title = QLabel("Progreso en Misiones por Tipo de Operación")
        title.setFont(QFont("Gill Sans Ultra Bold", 14))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.chart = BarChartWidget()

        main_layout.addWidget(title)
        main_layout.addWidget(self.chart)

        self._calculate_and_display_data()

    def _calculate_and_display_data(self):
        """Lee el historial, calcula los porcentajes y actualiza la gráfica."""
        if not os.path.exists(HISTORY_FILE):
            print("Archivo de historial no encontrado.")
            return

        # Usamos defaultdict para facilitar la suma
        totals = defaultdict(int)
        corrects = defaultdict(int)

        try:
            with open(HISTORY_FILE, mode='r', newline='', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    op_type = row.get("Tipo de Operacion")
                    result = row.get("Resultado")

                    if op_type and result:
                        op_type = op_type.strip()
                        totals[op_type] += 1
                        if result.strip().lower() == 'correcto':
                            corrects[op_type] += 1
        except Exception as e:
            print(f"Error al procesar el historial: {e}")
            return

        # Calcular porcentajes
        percentages = {}
        # Definir el orden deseado de las operaciones
        operation_order = ["Suma", "Resta", "Multiplicación", "División", "Fracción"]

        for op in operation_order:
            if totals[op] > 0:
                percentages[op] = (corrects[op] / totals[op]) * 100

        self.chart.set_data(percentages)

