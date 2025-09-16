import sys
import pygame

from PyQt6.QtCore import Qt, QThread
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QGridLayout, 
                             QPushButton, QLineEdit, QHBoxLayout, QLabel,
                             QMessageBox)
from PyQt6.QtGui import QFont, QKeyEvent

from core.calculator_logic import CalculatorLogic
from core.audio_listener import AudioListener
from core.mission_engine import MissionEngine
from core.reward_manager import RewardManager

import re

from gui.visualizer_widget import VisualizerWidget
from gui.interactive_idle_widget import InteractiveIdleWidget

sys.path.append('..')

class MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()
        
        self.mission_engine = MissionEngine()
        self.reward_manager = RewardManager()
        self.current_mission = None

        pygame.mixer.init()

        try:
            self.oof_sound = pygame.mixer.Sound('assets/sounds/oof.wav')
            self.fnaf_sound = pygame.mixer.Sound('assets/sounds/fnaf_sound.wav')
        except pygame.error as e:
            print(f"Error al cargar un sonido: {e}")

            self.oof_sound = None
            self.fnaf_sound = None

        self.logic = CalculatorLogic()
        self.setWindowTitle("Sofi calc")        
        self.resize(800, 600)
        
        self.current_theme = 'roblox_dark' 

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_h_layout = QHBoxLayout(self.central_widget)
        self.left_v_layout = QVBoxLayout()
        
        top_layout = self._create_display_and_theme_button()

        self.mission_widget = InteractiveIdleWidget(oof_sound=self.oof_sound)
        
        # --- Layout para los botones de Misión y Juego ---
        mission_controls_layout = QHBoxLayout()
        self.new_mission_button = QPushButton("🚀 Nueva Misión")
        self.new_mission_button.setObjectName("NewMissionButton")
        self.new_mission_button.clicked.connect(self._start_new_mission)
        
        self.play_game_button = QPushButton("🕹️ Jugar Minijuego") # Nuevo botón
        self.play_game_button.setObjectName("PlayGameButton")
        self.play_game_button.clicked.connect(self._start_minigame)
        
        mission_controls_layout.addWidget(self.new_mission_button)
        mission_controls_layout.addWidget(self.play_game_button)

        buttons_layout = self._create_buttons()

        self.left_v_layout.addLayout(top_layout)
        self.left_v_layout.addWidget(self.mission_widget)
        self.left_v_layout.addWidget(self.new_mission_button)
        self.left_v_layout.addLayout(buttons_layout)

        left_container = QWidget()
        left_container.setLayout(self.left_v_layout)

        self.visualizer = VisualizerWidget()
        self.visualizer.setObjectName("VisualizerPanel")

        self.main_h_layout.addWidget(left_container)
        self.main_h_layout.addWidget(self.visualizer)

        self._apply_base_styles()
        self.load_stylesheet(f'gui/themes/{self.current_theme}_theme.qss')
        #self._setup_audio_listener()
    
    def keyPressEvent(self, event: QKeyEvent):
        key = event.key()
        if key == Qt.Key.Key_Space or key == Qt.Key.Key_Return:
            if not self.mission_widget.is_active:
                self._start_minigame() # Si no está activo, iniciarlo
            else:
                self.mission_widget.jump() # Si ya está activo, saltar
        else:
            super().keyPressEvent(event)

    def _start_minigame(self):
        if self.current_mission:
            self.current_mission = None
        self.mission_widget.start_game()
    
    def _start_new_mission(self):
        """Carga una nueva misión y detiene el minijuego."""
        self.mission_widget.stop_game() # Detiene el juego
        self.current_mission = self.mission_engine.get_random_mission()
        self.mission_widget.setText(self.current_mission["text"])
        self.logic.clear_expression()
        self.display.setText("")

        self.visualizer.update_visualization(None, None, None, None)
        self.visualizer.update_fraction_visualization(None, None, None, None)

    def _create_buttons(self):
        buttons_layout = QGridLayout()
        self.buttons = {} 
        
        button_map = {
            'C': (0, 0, 1, 1), 'a/b': (0, 1, 1, 1), '⌫': (0, 2, 1, 1), '÷': (0, 3, 1, 1),
            '7': (1, 0, 1, 1), '8': (1, 1, 1, 1), '9': (1, 2, 1, 1), 'x': (1, 3, 1, 1),
            '4': (2, 0, 1, 1), '5': (2, 1, 1, 1), '6': (2, 2, 1, 1), '-': (2, 3, 1, 1),
            '1': (3, 0, 1, 1), '2': (3, 1, 1, 1), '3': (3, 2, 1, 1), '+': (3, 3, 1, 1),
            '0': (4, 0, 1, 2), '.': (4, 2, 1, 1), '=': (4, 3, 1, 1),
        }

        for text, pos in button_map.items():
            button = QPushButton(text)
            button.setFont(QFont("Gill Sans Ultra Bold", 14))
            button.clicked.connect(self._on_button_click)
            buttons_layout.addWidget(button, pos[0], pos[1], pos[2], pos[3])

            self.buttons[text] = button

        return buttons_layout
    
    def _on_button_click(self):
        button = self.sender()
        text = button.text()

        if text == 'a/b':
            if self.current_mission:
                self.current_mission = None
                self.mission_widget.setText("Misión cancelada. ¡Calculadora lista!")
            self.logic.add_to_expression('/')
            self.display.setText(self.logic.current_expression)
            return

        if text == '=':
            expression = self.logic.current_expression
            
            if self.current_mission:
                user_answer = self.display.text()
                if user_answer == self.current_mission["answer"]:
                    # Lógica de respuesta correcta...
                    if self.fnaf_sound: self.fnaf_sound.play()
                    reward_id = self.current_mission["reward"]
                    just_unlocked = self.reward_manager.unlock_reward(reward_id)
                    self._show_styled_message_box(
                        "¡CORRECTO!", f"¡Has desbloqueado '{reward_id}'!" if just_unlocked else "¡Misión completada!", "success"
                    )
                    self.current_mission = None
                    self.mission_widget.setText("¡Misión completada! Presiona 'Nueva Misión' para otra.")
                else:
                    # Lógica de respuesta incorrecta...
                    if self.oof_sound: self.oof_sound.play()
                    self._show_styled_message_box("¡INCORRECTO!", "Esa no es la respuesta. ¡Inténtalo de nuevo!", "error")
                return # Detiene la ejecución aquí para el modo misión

            # Modo Calculadora Normal
            result = self.logic.evaluate_expression()
            self.display.setText(result)

            # Lógica del Visualizador
            fraction_match = re.search(r'(\d+)/(\d+)\s*([+\-x])\s*(\d+)/(\d+)', expression)
            
            if fraction_match:
                # Si encuentra una operación de fracciones, la envía al visualizador
                f1_num, f1_den, op, f2_num, f2_den = fraction_match.groups()
                # Parsea el resultado, que puede ser una fracción o un entero
                if '/' in result:
                    res_num, res_den = result.split('/')
                else:
                    res_num, res_den = result, '1'
                
                self.visualizer.update_fraction_visualization(op, (f1_num, f1_den), (f2_num, f2_den), (res_num, res_den))
            elif result != "Error":
                match = re.search(r'(\d+\.?\d*)([+\-x÷])(\d+\.?\d*)', expression)
                if match:
                    num1, op, num2 = match.groups()
                    self.visualizer.update_visualization(float(num1), op, float(num2), float(result))
                else:
                    self.visualizer.update_visualization(None, None, None, None)
            else:
                self.visualizer.update_visualization(None, None, None, None)
        
        elif text == '⌫':
            if self.reward_manager.is_unlocked("oof_sound") and self.oof_sound:
                self.oof_sound.play()
            
            self.logic.delete_last()
            self.display.setText(self.logic.current_expression)

            self.visualizer.update_visualization(None, None, None, None)
            self.visualizer.update_fraction_visualization(None, None, None, None)
        
        elif text == 'C':
            self.logic.clear_expression()
            self.display.setText("")

            self.visualizer.update_visualization(None, None, None, None)
            self.visualizer.update_fraction_visualization(None, None, None, None)

            self.current_mission = None
            self.mission_widget.setText("¡Presiona 'Nueva Misión' o ESPACIO para saltar!")
        
        else:
            # cancelamos la misión para permitir el cálculo normal.
            if self.current_mission and text in "+-x÷a/b":
                self.current_mission = None
                self.mission_widget.setText("Misión cancelada. ¡Calculadora lista!")
            
            if self.current_mission: # Modo Misión
                if text in "0123456789.":
                    self.logic.add_to_expression(text)
                    self.display.setText(self.logic.current_expression)
            else: # Modo calculadora normal
                self.logic.add_to_expression(text)
                self.display.setText(self.logic.current_expression)
    
    def _show_styled_message_box(self, title, text, style_type="info"):
        """Muestra una ventana emergente con estilos personalizados."""
        msg_box = QMessageBox()
        
        if style_type == "success":
            msg_box.setIcon(QMessageBox.Icon.Information)
            msg_box.setWindowTitle("¡Felicidades!")
            style_sheet = """
                QMessageBox { background-color: #393B3D; border: 2px solid #DA232A; border-radius: 8px; }
                QMessageBox QLabel { color: #FFFFFF; font-size: 14pt; padding: 10px; }
                QMessageBox QPushButton { background-color: #DA232A; color: #FFFFFF; border: none; border-radius: 5px; padding: 8px 15px; font-weight: bold; font-size: 12pt; min-width: 80px; }
                QMessageBox QPushButton:hover { background-color: #E74C52; }
            """
        elif style_type == "error":
            msg_box.setIcon(QMessageBox.Icon.Warning)
            msg_box.setWindowTitle("¡Error!")
            style_sheet = """
                QMessageBox { background-color: #393B3D; border: 2px solid #FFCC00; border-radius: 8px; }
                QMessageBox QLabel { color: #FFFFFF; font-size: 14pt; padding: 10px; }
                QMessageBox QPushButton { background-color: #FFCC00; color: #2A2C2E; border: none; border-radius: 5px; padding: 8px 15px; font-weight: bold; font-size: 12pt; min-width: 80px; }
                QMessageBox QPushButton:hover { background-color: #FFE066; }
            """
        
        msg_box.setStyleSheet(style_sheet)
        msg_box.setText(f"<h3>{title}</h3>")
        msg_box.setInformativeText(text)
        msg_box.exec()

    def _play_activation_sound(self): pass
    def _setup_audio_listener(self): pass
    def stop_audio_thread(self): pass

    def _create_display_and_theme_button(self):
        top_layout = QHBoxLayout()
        
        self.display = QLineEdit()
        self.display.setFixedHeight(70)
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.display.setReadOnly(True)
        self.display.setFont(QFont("Gill Sans Ultra Bold", 28))

        self.theme_button = QPushButton("🧱☀️")
        self.theme_button.setFixedSize(50, 50)
        self.theme_button.setFont(QFont("Arial", 18))
        self.theme_button.clicked.connect(self._toggle_theme)

        top_layout.addWidget(self.display)
        top_layout.addWidget(self.theme_button)

        return top_layout

    def _toggle_theme(self):        
        if self.current_theme == 'dark':
            self.current_theme = 'light'
            self.theme_button.setText("🌙")
        elif self.current_theme == 'light':
            self.current_theme = 'roblox_dark'
            self.theme_button.setText("🧱")
        elif self.current_theme == 'roblox_dark':
            self.current_theme = 'roblox_light'
            self.theme_button.setText("🧱☀️")
        else:
            self.current_theme = 'dark'
            self.theme_button.setText("☀️")
            
        stylesheet_path = f'gui/themes/{self.current_theme}_theme.qss'

        self.load_stylesheet(stylesheet_path)

        print(f"Tema cambiado a: {self.current_theme}")

    def _apply_base_styles(self):
        for button in self.buttons.values():
            button.setMinimumSize(80, 70)
        self.theme_button.setObjectName("ThemeButton")
    
    def load_stylesheet(self, file_path):
        """Carga una hoja de estilos QSS para aplicar un tema."""
        try:
            with open(file_path, "r") as f: self.setStyleSheet(f.read())
        except FileNotFoundError:
            print(f"Error: No se encontró el archivo de tema en {file_path}")