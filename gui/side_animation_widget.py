from PyQt6.QtWidgets import QWidget, QLabel
from PyQt6.QtGui import QMovie
from PyQt6.QtCore import QSize, QTimer, QPropertyAnimation, QRect, QEasingCurve, Qt

class SideAnimationWidget(QWidget):
    """
    Un widget que muestra una animación de un personaje (zombi) que se desliza
    hacia la vista desde fuera de la ventana después de un retraso.
    """
    def __init__(self, gif_path, parent=None):
        super().__init__(parent)
        # Hacemos el fondo del widget transparente para que solo se vea el GIF
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        # Permitimos que el widget se dibuje fuera de los límites de su layout
        self.setAttribute(Qt.WidgetAttribute.WA_LayoutUsesWidgetRect)

        self.animation_label = QLabel(self)
        self.movie = QMovie(gif_path)
        self.animation_label.setMovie(self.movie)
        self.movie.start()

        # Posición inicial (fuera de la pantalla a la derecha)
        self.start_geometry = QRect(0, 0, 0, 0)
        self.end_geometry = QRect(0, 0, 0, 0)

        self.animation = QPropertyAnimation(self.animation_label, b"geometry")
        self.animation.setDuration(1500) # Duración de la animación de deslizamiento
        self.animation.setEasingCurve(QEasingCurve.Type.OutCubic)

        # Temporizador para retrasar la aparición
        self.appear_timer = QTimer(self)
        self.appear_timer.setSingleShot(True)
        self.appear_timer.timeout.connect(self.start_slide_in_animation)
        self.appear_timer.start(15000) # 15 segundos

    def update_animation_positions(self):
        """Calcula las posiciones de inicio y fin de la animación."""
        parent_rect = self.parentWidget().rect()

        # El GIF tendrá la altura del padre (la ventana)
        gif_height = parent_rect.height()
        # Calculamos el ancho manteniendo la proporción del GIF original
        gif_width = int(gif_height * (self.movie.currentPixmap().width() / self.movie.currentPixmap().height()))

        self.movie.setScaledSize(QSize(gif_width, gif_height))

        # Posición inicial: Justo fuera del borde derecho de la ventana
        start_x = parent_rect.width()
        # Posición final: Asomándose un poco desde la derecha
        end_x = parent_rect.width() - int(gif_width * 0.75) # Se asoma un 75%

        self.start_geometry = QRect(start_x, 0, gif_width, gif_height)
        self.end_geometry = QRect(end_x, 0, gif_width, gif_height)

        # Colocamos el QLabel en su posición inicial
        self.animation_label.setGeometry(self.start_geometry)

    def start_slide_in_animation(self):
        """Inicia la animación para que el zombi se deslice hacia la vista."""
        print("Iniciando animación del zombi...")
        self.update_animation_positions()
        self.animation.setStartValue(self.start_geometry)
        self.animation.setEndValue(self.end_geometry)
        self.animation.start()

    def resizeEvent(self, event):
        """Ajusta las posiciones si la ventana cambia de tamaño."""
        super().resizeEvent(event)
        # Si la animación ya terminó, ajustamos la posición final del zombi
        if not self.appear_timer.isActive() and self.animation.state() != QPropertyAnimation.State.Running:
            self.update_animation_positions()
            self.animation_label.setGeometry(self.end_geometry)

