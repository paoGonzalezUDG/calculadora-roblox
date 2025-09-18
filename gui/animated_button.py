from PyQt6.QtWidgets import QPushButton, QLabel, QGridLayout
from PyQt6.QtGui import QMovie
from PyQt6.QtCore import QTimer, QSize, Qt

class AnimatedButton(QPushButton):
    """Un botón que reproduce una animación de chispitas al ser presionado."""

    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.animation_label = QLabel(self)
        # Permite que los clics del mouse "atraviesen" la etiqueta y lleguen al botón
        self.animation_label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.animation_label.setVisible(False)
        
        try:
            self.movie = QMovie("assets/images/sparkle.gif")
            # Ajusta el tamaño del GIF para que encaje bien en el botón
            self.movie.setScaledSize(QSize(60, 60)) 
            self.animation_label.setMovie(self.movie)
        except Exception as e:
            self.movie = None
            print(f"No se pudo cargar la animación 'sparkle.gif': {e}")

        # Usamos un layout para centrar la animación sobre el texto del botón
        layout = QGridLayout(self)
        layout.addWidget(self.animation_label, 0, 0, Qt.AlignmentFlag.AlignCenter)

    def play_animation(self):
        """Muestra y reproduce la animación."""
        if self.movie:
            self.animation_label.setVisible(True)
            self.movie.start()
            # Detiene la animación y la oculta después de 1 segundo
            QTimer.singleShot(1000, self.stop_animation)

    def stop_animation(self):
        """Detiene y oculta la animación."""
        if self.movie:
            self.movie.stop()
            self.animation_label.setVisible(False)
