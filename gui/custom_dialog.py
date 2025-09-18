from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtGui import QMovie, QFont
from PyQt6.QtCore import Qt, QSize

class CustomVictoryDialog(QDialog):
    """
    Ventana emergente personalizada para mostrar un mensaje de victoria o derrota
    con un GIF animado.
    """
    def __init__(self, message, parent=None):
        super().__init__(parent)

        self.setWindowTitle("¡Victoria!")
        self.setFixedSize(350, 400)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(15)

        self.gif_label = QLabel(self)
        self.gif_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        try:
            self.movie = QMovie("assets/images/victory.gif")
            self.movie.setScaledSize(QSize(200, 200))
            self.gif_label.setMovie(self.movie)
            self.movie.start()
        except Exception as e:
            print(f"Error al cargar victory.gif: {e}")
            self.gif_label.setText("🎉")

        self.title_label = QLabel("¡CORRECTO!", self)
        self.title_label.setFont(QFont("Gill Sans Ultra Bold", 22))
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.message_label = QLabel(message, self)
        self.message_label.setFont(QFont("Gill Sans Ultra Bold", 12))
        self.message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.message_label.setWordWrap(True)

        self.ok_button = QPushButton("¡Genial!", self)
        self.ok_button.clicked.connect(self.accept)

        layout.addWidget(self.gif_label)
        layout.addWidget(self.title_label)
        layout.addWidget(self.message_label)
        layout.addWidget(self.ok_button)

        self.setStyleSheet("""
            QDialog {
                background-color: #393B3D;
                border: 2px solid #DA232A;
                border-radius: 10px;
            }
            QLabel {
                color: #FFFFFF;
            }
            QPushButton {
                background-color: #DA232A;
                color: #FFFFFF;
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
                font-size: 14pt;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #E74C52;
            }
        """)

class CustomDefeatDialog(QDialog):
    """
    Una ventana emergente personalizada para mostrar un mensaje de error
    con un GIF animado.
    """
    def __init__(self, message, parent=None):
        super().__init__(parent)

        self.setWindowTitle("¡Error!")
        self.setFixedSize(350, 400)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(15)

        self.gif_label = QLabel(self)
        self.gif_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        try:
            self.movie = QMovie("assets/images/defeat.gif")
            self.movie.setScaledSize(QSize(200, 200))
            self.gif_label.setMovie(self.movie)
            self.movie.start()
        except Exception as e:
            print(f"Error al cargar defeat.gif: {e}")
            self.gif_label.setText("❌") # Emoji de respaldo

        self.title_label = QLabel("¡INCORRECTO!", self)
        self.title_label.setFont(QFont("Gill Sans Ultra Bold", 22))
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.message_label = QLabel(message, self)
        self.message_label.setFont(QFont("Gill Sans Ultra Bold", 12))
        self.message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.message_label.setWordWrap(True)

        self.ok_button = QPushButton("Reintentar", self)
        self.ok_button.clicked.connect(self.accept)

        layout.addWidget(self.gif_label)
        layout.addWidget(self.title_label)
        layout.addWidget(self.message_label)
        layout.addWidget(self.ok_button)

        self.setStyleSheet("""
            QDialog {
                background-color: #393B3D;
                border: 2px solid #FFCC00; /* Borde amarillo para advertencia */
                border-radius: 10px;
            }
            QLabel {
                color: #FFFFFF;
            }
            QPushButton {
                background-color: #FFCC00; /* Botón amarillo */
                color: #2A2C2E; /* Texto oscuro para contraste */
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
                font-size: 14pt;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #FFE066;
            }
        """)

