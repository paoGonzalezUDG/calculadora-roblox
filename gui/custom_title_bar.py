from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton
from PyQt6.QtGui import QMovie, QFont
from PyQt6.QtCore import Qt, QSize

class CustomTitleBar(QWidget):
    """Una barra de título personalizada con múltiples animaciones GIF."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setObjectName("CustomTitleBar")
        self.setFixedHeight(50)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 0, 5, 0)
        layout.setSpacing(10)

        # 1. Animación GIF Principal (Techno)
        self.animation_label = QLabel(self)
        self.movie = QMovie("assets/images/title-bar.gif")
        self.movie.setScaledSize(QSize(50, 50))
        self.animation_label.setMovie(self.movie)
        self.movie.start()

        # 2. Título de la ventana
        self.title_label = QLabel("Sofía calc", self)
        self.title_label.setFont(QFont("Gill Sans Ultra Bold", 12))
        self.title_label.setObjectName("TitleBarLabel")

        layout.addWidget(self.animation_label)
        layout.addWidget(self.title_label)

        gif_paths = ["assets/images/baby-zombi.gif"]
        for path in gif_paths:
            gif_label = QLabel(self)
            movie = QMovie(path)
            if not movie.isValid():
                 print(f"Advertencia: No se pudo cargar el GIF en '{path}'")
                 continue
            movie.setScaledSize(QSize(30, 40))
            gif_label.setMovie(movie)
            movie.start()
            layout.addWidget(gif_label)

        layout.addStretch() # Empuja los botones a la derecha

        # 3. Botones de control de la ventana
        self.minimize_button = QPushButton("—")
        self.maximize_button = QPushButton("⬜")
        self.close_button = QPushButton("✕")

        button_size = QSize(40, 40)
        self.minimize_button.setFixedSize(button_size)
        self.maximize_button.setFixedSize(button_size)
        self.close_button.setFixedSize(button_size)

        self.minimize_button.setObjectName("TitleBarButton")
        self.maximize_button.setObjectName("TitleBarButton")
        self.close_button.setObjectName("TitleBarButtonClose")

        if self.parent:
            self.minimize_button.clicked.connect(self.parent.showMinimized)
            self.maximize_button.clicked.connect(self.parent.toggle_maximize)
            self.close_button.clicked.connect(self.parent.close)

        layout.addWidget(self.minimize_button)
        layout.addWidget(self.maximize_button)
        layout.addWidget(self.close_button)

