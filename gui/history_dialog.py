import csv
import os
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem,
                             QPushButton, QHeaderView)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor

HISTORY_FILE = "mission_history.csv"

class HistoryDialog(QDialog):
    """
    Una ventana emergente que muestra el historial de misiones desde un archivo CSV.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Historial de Misiones")
        self.setModal(True)
        self.setMinimumSize(960, 500)

        layout = QVBoxLayout(self)

        self.table_widget = QTableWidget()
        layout.addWidget(self.table_widget)

        self.close_button = QPushButton("Cerrar")
        self.close_button.clicked.connect(self.accept)
        layout.addWidget(self.close_button, alignment=Qt.AlignmentFlag.AlignRight)

        self.load_history_data()

        if parent:
            self.setStyleSheet(parent.styleSheet())

        self.table_widget.setStyleSheet("""
            QTableWidget {
                gridline-color: #555555;
                font-size: 10pt;
                font-family: "Gill Sans";
            }
            QHeaderView::section {
                /* 2. Cambiar color de fondo del encabezado a azul */
                background-color: #0078D7;
                color: white;
                padding: 4px;
                border: 1px solid #2A2C2E;
                font-weight: bold;
            }
            QTableWidgetItem {
                padding: 5px;
            }
        """)


    def load_history_data(self):
        """Lee el archivo CSV y puebla la tabla."""
        if not os.path.exists(HISTORY_FILE):
            self.table_widget.setRowCount(1)
            self.table_widget.setColumnCount(1)
            self.table_widget.setHorizontalHeaderLabels(["Info"])
            self.table_widget.setItem(0, 0, QTableWidgetItem("Aún no hay historial de misiones."))
            self.table_widget.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
            return

        try:
            with open(HISTORY_FILE, mode='r', newline='', encoding='utf-8-sig') as f:
                reader = list(csv.reader(f))
                if not reader or len(reader) < 2:
                    self.table_widget.setRowCount(1)
                    self.table_widget.setColumnCount(1)
                    self.table_widget.setHorizontalHeaderLabels(["Info"])
                    self.table_widget.setItem(0, 0, QTableWidgetItem("El historial está vacío."))
                    self.table_widget.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
                    return

                headers_original = reader[0]
                data_rows = reader[1:]

                # 2. Modificar encabezados para que se ajusten en dos líneas
                headers_display = [
                    "Fecha y\nHora", "Texto de la\nMisión", "Respuesta\ndel Usuario",
                    "Respuesta\nCorrecta", "Resultado", "Tipo de\nOperación"
                ]

                if len(headers_display) != len(headers_original):
                    headers_display = headers_original

                self.table_widget.setColumnCount(len(headers_original))
                self.table_widget.setHorizontalHeaderLabels(headers_display)
                self.table_widget.setRowCount(len(data_rows))

                # Ajustar altura y alineación del encabezado
                self.table_widget.horizontalHeader().setFixedHeight(50)
                # CORRECCIÓN: Se elimina Qt.AlignmentFlag.TextWordWrap que causaba el error.
                self.table_widget.horizontalHeader().setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)


                for row_idx, row_data in enumerate(data_rows):
                    for col_idx, cell_data in enumerate(row_data):
                        item = QTableWidgetItem(cell_data)
                        if headers_original[col_idx] == "Resultado":
                            if "Correcto" in cell_data:
                                item.setForeground(QColor("#33FF33"))
                            elif "Incorrecto" in cell_data:
                                item.setForeground(QColor("#FF3333"))
                        self.table_widget.setItem(row_idx, col_idx, item)

                header = self.table_widget.horizontalHeader()

                mission_text_index = -1
                try:
                    # Buscar por el texto original del encabezado
                    mission_text_index = headers_original.index("Texto de la Misión")
                except ValueError:
                    try:
                        mission_text_index = headers_original.index("Texto de la Mision") # Fallback para CSVs antiguos
                    except ValueError:
                         mission_text_index = 1 # Último recurso

                for i in range(len(headers_original)):
                    if i == mission_text_index:
                        header.setSectionResizeMode(i, QHeaderView.ResizeMode.Stretch)
                    else:
                        header.setSectionResizeMode(i, QHeaderView.ResizeMode.ResizeToContents)

                self.table_widget.setWordWrap(True)
                self.table_widget.resizeRowsToContents()

        except Exception as e:
            print(f"Error al leer el archivo de historial: {e}")

