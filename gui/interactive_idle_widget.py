from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QPixmap, QColor, QFont, QPen, QTextDocument
from PyQt6.QtCore import Qt, QTimer, QRect

class InteractiveIdleWidget(QWidget):
    """Un minijuego interactivo con dificultad progresiva y Robux persistentes."""
    
    def __init__(self, oof_sound=None, reward_manager=None, mission_complete_sound=None, jump_sound=None):
        super().__init__()

        self.setObjectName("InteractiveIdleWidget")
        self.setMinimumHeight(120)

        self.player_pixmap = QPixmap('assets/images/noob_runner.png')
        self.obstacle_pixmap = QPixmap('assets/images/obstacle.png')
        
        self.oof_sound = oof_sound
        self.reward_manager = reward_manager
        self.mission_complete_sound = mission_complete_sound
        self.jump_sound = jump_sound

        self.player_width = 50
        self.player_height = 65
        
        self.player_x = 50
        self.player_y = self.height()
        self.player_velocity_y = 0
        self.gravity = 1
        self.jump_strength = -17 
        self.is_jumping = False
        self.ground_y = 0

        self.obstacle_x = self.width()
        self.obstacle_width = 30
        self.obstacle_height = 30
        
        self.initial_obstacle_speed = 6
        self.obstacle_speed = self.initial_obstacle_speed
        self.speed_increase_interval = 1 # Aumentar velocidad cada X obstáculos
        self.speed_increase_amount = 0.75
        
        self.JUMP_GOAL = 10 # Objetivo de obstáculos para ganar Robux
        self.session_robux = 0
        
        self.game_over = False
        self.is_active = False
        self.game_won = False
        
        self.message = "Presiona 'Jugar Minijuego' para empezar"

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_game_state)

    def setText(self, text):
        self.message = text
        self.update()
        
    def start_game(self):
        if not self.is_active:
            self.restart_game()

    def stop_game(self):
        if self.is_active:
            self.is_active = False
            self.timer.stop()
            self.message = "Juego pausado. ¡Presiona 'Jugar' para continuar!"
            self.update()

    def resizeEvent(self, event):
        self.ground_y = self.height() - 15
        if not self.is_jumping:
            self.player_y = self.ground_y - self.player_height + 5
        super().resizeEvent(event)

    def jump(self):
        if self.game_over:
            self.restart_game()
        elif not self.is_jumping and self.is_active:
            if self.jump_sound:
                self.jump_sound.play()
            self.is_jumping = True
            self.player_velocity_y = self.jump_strength

    def restart_game(self):
        self.session_robux = 0
        self.obstacle_x = self.width()
        self.player_y = self.ground_y - self.player_height + 5

        self.is_jumping = False
        self.game_over = False
        self.is_active = True
        self.game_won = False

        self.message = ""
        self.obstacle_speed = self.initial_obstacle_speed
        self.timer.start(16)

    def update_game_state(self):
        if self.game_over or not self.is_active:
            return

        self.obstacle_x -= self.obstacle_speed
        if self.obstacle_x < -self.obstacle_width:
            self.obstacle_x = self.width()
            self.session_robux += 1
            
            if self.session_robux > 0 and self.session_robux % self.speed_increase_interval == 0:
                self.obstacle_speed += self.speed_increase_amount
                print(f"¡Velocidad aumentada a {self.obstacle_speed:.1f}!")

            if self.session_robux >= self.JUMP_GOAL:
                self.timer.stop()

                self.game_over = True
                self.game_won = True
                self.is_active = False

                self.message = "¡Objetivo Logrado!"

                if self.mission_complete_sound:
                    self.mission_complete_sound.play()
                if self.reward_manager and self.session_robux > 0:
                    self.reward_manager.add_robux(self.session_robux)
                self.update()
                return

        if self.is_jumping:
            self.player_y += self.player_velocity_y
            self.player_velocity_y += self.gravity
            ground_contact_y = self.ground_y - self.player_height + 5
            if self.player_y >= ground_contact_y:
                self.player_y = ground_contact_y
                self.is_jumping = False
        
        obstacle_y_pos = self.ground_y - self.obstacle_height + 5
        player_rect = QRect(int(self.player_x), int(self.player_y), self.player_width, self.player_height)
        obstacle_rect = QRect(int(self.obstacle_x), int(obstacle_y_pos), self.obstacle_width, self.obstacle_height)

        if player_rect.intersects(obstacle_rect) and not self.game_won:
            self.timer.stop()
            self.game_over = True
            self.is_active = False
            self.message = "¡Game Over! Presiona ESPACIO para reiniciar."
            if self.oof_sound:
                self.oof_sound.play()
            
            if self.reward_manager and self.session_robux > 0:
                self.reward_manager.add_robux(self.session_robux)

        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        painter.fillRect(self.rect(), QColor("#87CEEB"))
        painter.fillRect(0, self.ground_y, self.width(), 15, QColor("#228B22"))

        if self.player_pixmap and not self.player_pixmap.isNull():
            painter.drawPixmap(int(self.player_x), int(self.player_y), self.player_width, self.player_height, self.player_pixmap)
        if self.obstacle_pixmap and not self.obstacle_pixmap.isNull():
            obstacle_y_pos = self.ground_y - self.obstacle_height + 5
            painter.drawPixmap(int(self.obstacle_x), int(obstacle_y_pos), self.obstacle_width, self.obstacle_height, self.obstacle_pixmap)

        painter.save()
        
        painter.setPen(QPen(QColor("black")))
        painter.setFont(QFont("Gill Sans Ultra Bold", 11))
        
        total_robux = self.reward_manager.get_total_robux() if self.reward_manager else 0
        painter.drawText(QRect(self.width() - 150, 5, 140, 30), Qt.AlignmentFlag.AlignRight, f"Robux: {total_robux}")
        
        doc = QTextDocument()
        
        if self.game_over:
            # Si es Game Over, el texto es grande y centrado
            font_size = "13pt"
            y_offset = -20
            doc.setHtml(f"<p style='color: black; font-size: {font_size}; font-family: Gill Sans Ultra Bold; text-align: center;'>{self.message}</p>")
            doc.setTextWidth(self.width() - 20)
            text_height = doc.size().height()
            y_pos = ((self.height() - text_height) / 2) + y_offset
            painter.translate(10, y_pos)
        else:
            # Si es un mensaje normal, es pequeño y se posiciona en la parte superior
            font_size = "11pt"
            doc.setHtml(f"<p style='color: black; font-size: {font_size}; font-family: Gill Sans Ultra Bold; text-align: center;'>{self.message}</p>")
            doc.setTextWidth(self.width() - 20)
            painter.translate(10, 20) # Posición fija superior
        
        doc.drawContents(painter)
        painter.restore()

