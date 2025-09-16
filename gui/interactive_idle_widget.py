from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QPixmap, QColor, QFont, QKeyEvent, QPen, QTextDocument
from PyQt6.QtCore import Qt, QTimer, QRect

class InteractiveIdleWidget(QWidget):
    """Un minijuego interactivo de correr y saltar con temática de Roblox."""
    
    def __init__(self, oof_sound=None):
        super().__init__()
        self.setObjectName("InteractiveIdleWidget")
        self.setMinimumHeight(120)

        self.player_pixmap = QPixmap('assets/images/noob_runner.png')
        self.obstacle_pixmap = QPixmap('assets/images/obstacle.png')
        self.oof_sound = oof_sound

        # Mejoras de diseño y juego
        self.player_width = 50
        self.player_height = 60
        
        self.player_x = 50
        self.player_y = self.height()
        self.player_velocity_y = 0
        self.gravity = 1
        self.jump_strength = -14 
        self.is_jumping = False
        self.ground_level = 0

        self.obstacle_x = self.width()
        self.obstacle_width = 30
        self.obstacle_height = 30
        self.obstacle_speed = 6
        
        self.score = 0
        self.game_over = False
        self.is_active = False
        self.message = "Presiona ESPACIO para jugar"

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_game_state)

    def setText(self, text):
        self.message = text
        self.update()
        
    def start_game(self):
        if not self.is_active:
            self.is_active = True
            self.restart_game()
            self.message = ""

    def stop_game(self):
        self.is_active = False
        self.game_over = False
        self.timer.stop()
        self.message = "Juego en pausa. ¡Resuelve la misión!"
        self.update()

    def resizeEvent(self, event):
        self.ground_y = self.height() - 10
        self.ground_level = self.ground_y - self.player_height
        if not self.is_jumping:
            self.player_y = self.ground_level
        super().resizeEvent(event)

    def jump(self):
        if self.game_over:
            self.restart_game()
        elif not self.is_jumping and self.is_active:
            self.is_jumping = True
            self.player_velocity_y = self.jump_strength

    def restart_game(self):
        self.score = 0
        self.obstacle_x = self.width()
        self.player_y = self.ground_level
        self.is_jumping = False
        self.game_over = False
        self.is_active = True
        self.message = ""
        self.timer.start(16)

    def update_game_state(self):
        if self.game_over or not self.is_active:
            return

        self.obstacle_x -= self.obstacle_speed
        if self.obstacle_x < -self.obstacle_width:
            self.obstacle_x = self.width()
            self.score += 1

        if self.is_jumping:
            self.player_y += self.player_velocity_y
            self.player_velocity_y += self.gravity
            if self.player_y >= self.ground_level:
                self.player_y = self.ground_level
                self.is_jumping = False
        
        # CORRECCIÓN 1: Alinear obstáculo con el jugador
        obstacle_y_pos = self.ground_y - self.obstacle_height
        player_rect = QRect(self.player_x, self.player_y, self.player_width, self.player_height)
        obstacle_rect = QRect(self.obstacle_x, obstacle_y_pos, self.obstacle_width, self.obstacle_height)

        if player_rect.intersects(obstacle_rect):
            self.timer.stop()
            self.game_over = True
            self.is_active = False
            self.message = "¡Game Over! Presiona ESPACIO para reiniciar."
            if self.oof_sound:
                self.oof_sound.play()

        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        painter.fillRect(self.rect(), QColor("#87CEEB"))
        painter.fillRect(0, self.ground_y, self.width(), 10, QColor("#228B22"))

        if self.player_pixmap and not self.player_pixmap.isNull():
            painter.drawPixmap(self.player_x, self.player_y, self.player_width, self.player_height, self.player_pixmap)
        if self.obstacle_pixmap and not self.obstacle_pixmap.isNull():
            # CORRECCIÓN 1: Alinear obstáculo con el jugador
            obstacle_y_pos = self.ground_y - self.obstacle_height
            painter.drawPixmap(self.obstacle_x, obstacle_y_pos, self.obstacle_width, self.obstacle_height, self.obstacle_pixmap)

        painter.save()
        
        painter.setPen(QPen(QColor("black")))
        painter.setFont(QFont("Gill Sans Ultra Bold", 11))
        painter.drawText(QRect(self.width() - 110, 5, 100, 30), Qt.AlignmentFlag.AlignRight, f"Puntos: {self.score}")
        
        doc = QTextDocument()
        font_size = "13pt" if self.game_over else "11pt"
        doc.setHtml(f"<p style='color: black; font-size: {font_size}; font-family: Gill Sans Ultra Bold; text-align: center;'>{self.message}</p>")
        doc.setTextWidth(self.width() - 20)
        
        if self.game_over:
            text_height = doc.size().height()
            # CORRECCIÓN 2: Subir el texto de "Game Over"
            y_pos = ((self.height() - text_height) / 2) - 40
            painter.translate(10, y_pos)
        else:
            painter.translate(10, 30) 
        
        doc.drawContents(painter)
        painter.restore()

