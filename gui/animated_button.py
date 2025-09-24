from PyQt6.QtWidgets import QPushButton, QLabel
from PyQt6.QtGui import QMovie
from PyQt6.QtCore import QSize

class AnimatedButton(QPushButton):
    """Un botón que puede mostrar una animación GIF encima de sí mismo."""
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        
        self.animation_label = QLabel(self)
        self.movie = QMovie('assets/images/sparkle.gif')
        self.movie.setScaledSize(QSize(60, 60)) # Ajustar tamaño del GIF
        self.animation_label.setMovie(self.movie)
        self.animation_label.hide() # Oculto por defecto

    def start_animation(self):
        """Inicia y muestra la animación."""
        # Centrar el GIF en el botón
        self.animation_label.move(
            (self.width() - self.movie.scaledSize().width()) // 2,
            (self.height() - self.movie.scaledSize().height()) // 2
        )
        self.animation_label.show()
        self.movie.start()
        
        self.movie.setLoopCount(1) # Reproducir solo una vez
        self.movie.finished.connect(self.stop_animation)

    def stop_animation(self):
        """Detiene y oculta la animación."""
        self.movie.stop()
        self.animation_label.hide()

