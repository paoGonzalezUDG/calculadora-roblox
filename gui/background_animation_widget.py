from PyQt6.QtWidgets import QWidget, QLabel
from PyQt6.QtGui import QMovie
from PyQt6.QtCore import QPropertyAnimation, QRect, QTimer, QEasingCurve
import random

class BackgroundAnimationWidget(QWidget):
    """
    Un widget que muestra una animación de un personaje corriendo
    esporádicamente por el fondo.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setContentsMargins(0, 0, 0, 0)
        self.setStyleSheet("background-color: transparent;")

        self.animation_label = QLabel(self)
        try:
            # Asegúrate de tener un GIF en esta ruta
            self.movie = QMovie("assets/images/running_noob.gif")
            self.animation_label.setMovie(self.movie)
            self.movie.start()
        except Exception as e:
            print(f"Error al cargar el GIF para la animación de fondo: {e}")
            self.animation_label.setText("🏃") # Fallback a emoji

        self.animation_label.hide() # Oculto al inicio

        self.animation = QPropertyAnimation(self.animation_label, b"geometry")
        self.animation.setEasingCurve(QEasingCurve.Type.Linear)

        # Timer para iniciar la animación aleatoriamente
        self.start_timer = QTimer(self)
        self.start_timer.timeout.connect(self.start_run_animation)
        # Inicia la primera animación entre 8 y 15 segundos después de abrir la app
        self.start_timer.start(random.randint(8000, 15000))

    def start_run_animation(self):
        """Prepara e inicia la animación del personaje corriendo."""
        if self.animation.state() == QPropertyAnimation.State.Running:
            return # No iniciar si ya está en curso

        # Reiniciar el timer para la próxima aparición (entre 10 y 20 segundos)
        self.start_timer.setInterval(random.randint(10000, 20000))

        parent_width = self.parent().width() if self.parent() else self.width()
        parent_height = self.parent().height() if self.parent() else self.height()

        char_height = 100 # Altura del personaje en pantalla
        char_width = 70  # Ancho del personaje en pantalla

        # Posición inicial (fuera de la pantalla a la izquierda)
        start_pos = QRect(-char_width, parent_height - char_height - 20, char_width, char_height)
        # Posición final (fuera de la pantalla a la derecha)
        end_pos = QRect(parent_width, parent_height - char_height - 20, char_width, char_height)

        self.animation_label.setGeometry(start_pos)
        self.animation_label.show()

        self.animation.setDuration(random.randint(4000, 6000)) # Duración del recorrido
        self.animation.setStartValue(start_pos)
        self.animation.setEndValue(end_pos)
        self.animation.finished.connect(self.animation_label.hide) # Ocultar al terminar
        self.animation.start()

    def resizeEvent(self, event):
        """Se asegura de que la animación se recalcule si la ventana cambia de tamaño."""
        super().resizeEvent(event)

