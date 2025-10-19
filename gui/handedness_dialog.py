import sys
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QWidget, QFrame
from PyQt6.QtCore import Qt, QPoint, QSize
from PyQt6.QtGui import QFont, QIcon, QPixmap, QMovie

class CustomDialogTitleBar(QWidget):
    """Una barra de título simple para diálogos personalizados."""
    def __init__(self, title, parent_dialog=None):
        super().__init__(parent_dialog)
        self.parent_dialog = parent_dialog
        self.setObjectName("CustomDialogTitleBar")
        self.setFixedHeight(40)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 0, 5, 0)
        layout.setSpacing(10)

        # Ícono animado (GIF)
        self.icon_label = QLabel(self)
        self.icon_movie = QMovie("assets/images/title_gif_1.gif")
        if self.icon_movie.isValid():
            self.icon_movie.setScaledSize(QSize(40, 40))
            self.icon_label.setMovie(self.icon_movie)
            self.icon_movie.start()
        else:
            print("Advertencia: No se pudo cargar 'assets/images/title_gif_1.gif'")

        # Título
        self.title_label = QLabel(title, self)
        self.title_label.setFont(QFont("Gill Sans", 10))
        self.title_label.setObjectName("TitleBarLabel")

        layout.addWidget(self.icon_label)
        layout.addWidget(self.title_label)
        layout.addStretch()

        # Botón de cerrar
        self.close_button = QPushButton("✕")
        self.close_button.setFixedSize(30, 30)
        self.close_button.setObjectName("TitleBarButtonClose")
        if self.parent_dialog:
            self.close_button.clicked.connect(self.parent_dialog.reject) # Usar reject para cancelar

        layout.addWidget(self.close_button)

class HandednessDialog(QDialog):
    """
    Un diálogo inicial para que el usuario elija su preferencia de interfaz
    con una barra de título personalizada.
    """
    def __init__(self, parent=None):
        super().__init__(parent)

        # --- Ventana sin marco ---
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.old_pos = None

        self.selection = 'right'
        self.setModal(True)
        self.setMinimumSize(480, 220)

        # Contenedor principal para bordes y sombra
        main_container = QFrame(self)
        main_container.setObjectName("HandednessDialogContainer")

        # Layout principal
        main_layout = QVBoxLayout(main_container)
        main_layout.setContentsMargins(1, 1, 1, 1)
        main_layout.setSpacing(0)

        # --- Barra de Título Personalizada ---
        self.title_bar = CustomDialogTitleBar("Preferencia de Interfaz", self)

        # Contenido del diálogo
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(20, 15, 20, 20)
        content_layout.setSpacing(20)

        # Etiqueta de instrucción
        instruction_label = QLabel("Para adaptar la interfaz a tu comodidad,\npor favor, elige tu preferencia:", self)
        instruction_label.setFont(QFont("Gill Sans Ultra Bold", 14))
        instruction_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        instruction_label.setWordWrap(True)

        # Botones de selección
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(15)

        self.right_button = QPushButton("Diestro ✋")
        self.left_button = QPushButton("🤚 Zurdo")
        self.ambi_button = QPushButton("🙌 Ambidiestro")

        self.right_button.clicked.connect(lambda: self.set_selection('right'))
        self.left_button.clicked.connect(lambda: self.set_selection('left'))
        self.ambi_button.clicked.connect(lambda: self.set_selection('ambidextrous'))

        buttons_layout.addWidget(self.right_button)
        buttons_layout.addWidget(self.left_button)
        buttons_layout.addWidget(self.ambi_button)

        content_layout.addWidget(instruction_label)
        content_layout.addLayout(buttons_layout)

        main_layout.addWidget(self.title_bar)
        main_layout.addWidget(content_widget)

        # Layout para el QDialog principal
        dialog_layout = QVBoxLayout(self)
        dialog_layout.addWidget(main_container)

        self.setStyleSheet("""
            #HandednessDialogContainer {
                background-color: #2A2C2E;
                border: 1px solid #111;
                border-radius: 8px;
            }
            QLabel {
                color: white;
            }
            #TitleBarLabel {
                color: #CCCCCC;
            }
            QPushButton {
                background-color: #4A4E51;
                color: white;
                border: 1px solid #333;
                border-radius: 8px;
                padding: 15px;
                font-family: "Gill Sans Ultra Bold";
                font-size: 11pt;
            }
            QPushButton:hover {
                background-color: #5A5E61;
                border: 1px solid #777;
            }
             #TitleBarButtonClose {
                font-family: "Arial";
                font-size: 14pt;
                font-weight: bold;
                background-color: transparent;
                border: none;
                color: #AAA;
                border-radius: 5px;
            }
            #TitleBarButtonClose:hover {
                background-color: #E81123;
                color: white;
            }
        """)

    def set_selection(self, handedness):
        """Establece la selección y cierra el diálogo."""
        self.selection = handedness
        self.accept()

    # --- Métodos para mover la ventana ---
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton and self.title_bar.underMouse():
            self.old_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if self.old_pos:
            delta = QPoint(event.globalPosition().toPoint() - self.old_pos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.old_pos = event.globalPosition().toPoint()

    def mouseReleaseEvent(self, event):
        self.old_pos = None

