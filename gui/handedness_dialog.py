from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from PyQt6.QtCore import Qt

class HandednessDialog(QDialog):
    """
    Una ventana emergente para que el usuario elija su preferencia de
    lateralidad (diestro o zurdo).
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Preferencia de Interfaz")
        self.setModal(True)  # Bloquea la interacción con otras ventanas
        self.selection = 'right'  # Valor por defecto si se cierra

        layout = QVBoxLayout(self)
        layout.setSpacing(15)

        label = QLabel("Para adaptar la interfaz a tu comodidad,\npor favor, elige tu preferencia:")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)

        buttons_layout = QHBoxLayout()
        
        right_button = QPushButton("👋 Diestro")
        right_button.clicked.connect(lambda: self.set_selection('right'))
        
        left_button = QPushButton("👋 Zurdo")
        left_button.clicked.connect(lambda: self.set_selection('left'))
        
        ambi_button = QPushButton("🙌 Ambidiestro")
        # El diseño para diestros suele ser cómodo para ambidiestros
        ambi_button.clicked.connect(lambda: self.set_selection('right'))

        buttons_layout.addWidget(right_button)
        buttons_layout.addWidget(left_button)
        buttons_layout.addWidget(ambi_button)
        
        layout.addLayout(buttons_layout)
        
        # Estilos para que combine con el tema de la app
        self.setStyleSheet("""
            QDialog { background-color: #393B3D; }
            QLabel { color: white; font-size: 14pt; font-family: "Gill Sans Ultra Bold"; }
            QPushButton { 
                background-color: #4D5054; 
                color: white; 
                border: 1px solid #2A2C2E; 
                border-radius: 5px; 
                padding: 10px; 
                font-size: 12pt; 
                font-weight: bold;
                font-family: "Gill Sans Ultra Bold";
            }
            QPushButton:hover { background-color: #63676B; }
        """)

    def set_selection(self, choice):
        """Guarda la elección del usuario y cierra el diálogo."""
        self.selection = choice
        self.accept()

